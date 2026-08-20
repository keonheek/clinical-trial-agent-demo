"""POST /api/live -> run the full pipeline on a vignette the reviewer types in, live.

The precomputed patients prove polish; this is the act that proves the system actually thinks:
a judge hands us a patient we have never seen, and the same logic tree runs on it in front of
them. There is no server-side session -- every step is stateless and the browser carries the
state between them, because a Vercel invocation has a hard 60s ceiling and the whole pipeline
does not fit in one:

  step="start"   1 LLM call + a ClinicalTrials.gov fetch   (~10s)
                 vignette -> extracted fields + patient need + candidate trials
  step="match"   2 LLM calls, ONE trial                    (~20s)
                 the browser fires these in parallel, one request per candidate trial
  step="finish"  1 LLM call                                (~10s)
                 the ranked recommendation -- the required deliverable, lands first
  step="questions" 2 LLM calls                              (~20s, retry-prone)
                 clarifying questions, fetched after the ranking is already on screen

Every step is capped and rate-limited: this endpoint spends a metered key on text a stranger
typed. Answer rounds for a live patient go to /api/answer with patient_id "LIVE" (see the
live-mode branch there).
"""
import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault("LLM_BACKEND", "anthropic")

import anthropic_client
anthropic_client.CACHE_DIR = "/tmp/cache"  # the only writable dir in a Vercel invocation

import fetch_trials
import ranking
from action_policy import apply_trial_level_actions, enrich_questions
from patient_need import classify_patient_need
from pipeline import (apply_recommendation, detect_gaps, estimate_raw_criteria_count,
                      extract_patient, generate_questions, match_trial, parse_criteria, recommend)
from build_trial_intent import classify_trial_intent

# --- caps: this endpoint runs a stranger's text through a metered key -------------------
MAX_VIGNETTE = 1500
MAX_TRIALS = 4
MAX_CRITERIA_PER_TRIAL = 30
RATE_LIMIT_PER_MIN = int(os.environ.get("LIVE_RATE_LIMIT", "6"))
_recent = {}
# Optional shared passcode: set LIVE_DEMO_KEY in the Vercel project to require it (the client
# sends it as "key"). Unset = open, which is the demo-day default -- see README.
DEMO_KEY = os.environ.get("LIVE_DEMO_KEY", "")


def _rate_limited(ip):
    now = time.time()
    window = [t for t in _recent.get(ip, []) if now - t < 60]
    if len(window) >= RATE_LIMIT_PER_MIN:
        _recent[ip] = window
        return True
    window.append(now)
    _recent[ip] = window
    return False


CONDITION_SYS = """You name the condition a clinical-trial registry should be searched for.
Given a patient vignette, respond with the single best ClinicalTrials.gov condition search term:
the disease name a trialist would use, 1-4 words, no punctuation, no patient details, no hedging.
If the diagnosis is not yet established, name the condition being worked up.
Respond with ONLY {"condition": "<term>"} -- no markdown fences, no commentary."""


def _search_query(text, fields):
    """What to search ClinicalTrials.gov for.

    The shared extractor emits symptoms/labs/imaging findings, never a diagnosis field (it is
    frozen -- the eval labels pair with its output), so the live path names the condition
    itself with one small call. Falls back to the longest extracted clinical value, then to the
    vignette's own words, so a registry search always happens even if this call fails."""
    try:
        from pipeline import call_groq
        out = call_groq("live-condition", CONDITION_SYS, str(text)[:MAX_VIGNETTE])
        term = str(out.get("condition", "")).strip()
        if 2 < len(term) < 80:
            return term
    except Exception as e:  # noqa: BLE001 -- naming the condition must never fail the step
        print(f"[live] condition naming failed: {e}")
    vals = [str(f.get("value", "")) for f in (fields or [])
            if str(f.get("name", "")).lower() not in ("age", "sex")]
    if vals:
        return max(vals, key=len)[:120]
    return " ".join(str(text).split()[:12])[:120]


def _trial_public(t):
    """Only the fields the client needs to carry between steps."""
    return {"nct_id": t.get("nct_id"), "title": t.get("title", ""), "phase": t.get("phase", "NA"),
            "conditions": t.get("conditions", [])[:6],
            "eligibility_criteria_raw": (t.get("eligibility_criteria_raw", "") or "")[:12000]}


def step_start(body):
    text = str(body.get("text", "")).strip()[:MAX_VIGNETTE]
    if len(text) < 40:
        return {"error": "환자 정보를 조금 더 자세히 입력해 주세요 (최소 40자)."}
    patient = {"patient_id": "LIVE", "text": text}
    fields, _dropped = extract_patient(patient)
    need = classify_patient_need(text)
    query = _search_query(text, fields)
    try:
        studies = fetch_trials.fetch_condition(query, 8)
        pool = [s for s in (fetch_trials.normalize(x) for x in studies)
                if s.get("eligibility_criteria_raw")]
    except Exception as e:  # noqa: BLE001 -- a registry hiccup must say so, not 500
        return {"error": f"ClinicalTrials.gov 검색 실패: {e}"}
    if not pool and len(query.split()) > 1:  # a narrower term often has no recruiting trials
        short = " ".join(query.split()[-2:])
        try:
            pool = [s2 for s2 in (fetch_trials.normalize(x) for x in fetch_trials.fetch_condition(short, 8))
                    if s2.get("eligibility_criteria_raw")]
            if pool:
                query = short
        except Exception:  # noqa: BLE001
            pass
    if not pool:
        return {"error": f"'{query}' 로 모집 중인 시험을 찾지 못했습니다. 진단명을 더 명확히 적어 주세요."}
    candidates = [_trial_public(t) for t in pool[:MAX_TRIALS]]
    return {"patient": patient, "extraction": fields, "patient_need": need,
            "query_used": query, "candidates": candidates,
            "coverage": {c["nct_id"]: estimate_raw_criteria_count(c["eligibility_criteria_raw"])
                         for c in candidates},
            "intent": {c["nct_id"]: classify_trial_intent(c) for c in candidates}}


def step_match(body):
    text = str(body.get("text", "")).strip()[:MAX_VIGNETTE]
    trial = body.get("trial")
    fields = body.get("extraction")
    if not text or not isinstance(trial, dict) or not isinstance(fields, list):
        return {"error": "invalid match request"}
    patient = {"patient_id": "LIVE", "text": text}
    criteria = parse_criteria(trial)[:MAX_CRITERIA_PER_TRIAL]
    matched = match_trial(patient, fields, criteria, nct_id=trial.get("nct_id"))
    return {"nct_id": trial.get("nct_id"), "criteria": matched}


# Wall-clock ceiling per invocation. A Vercel function is killed at 60s; a single unparseable
# LLM response costs 2+4+8+16s of backoff, which is exactly how the first live test blew past
# it (84s). Every step now watches the clock and degrades instead of dying.
STEP_BUDGET_S = float(os.environ.get("LIVE_STEP_BUDGET", "45"))


def step_finish(body):
    text = str(body.get("text", "")).strip()[:MAX_VIGNETTE]
    trials = body.get("trials")
    if not text or not isinstance(trials, list) or not trials:
        return {"error": "invalid finish request"}
    patient = {"patient_id": "LIVE", "text": text}
    trials = [dict(t, criteria=list(t.get("criteria", []))[:MAX_CRITERIA_PER_TRIAL])
              for t in trials[:MAX_TRIALS]]
    # Intent and coverage decide the "does it help" and "how sure" parts of the order, so the
    # server derives them here rather than trusting the client to have carried step 1's maps:
    # a client that forgot them silently produced "purpose unconfirmed" on every live trial.
    coverage_in = body.get("coverage") if isinstance(body.get("coverage"), dict) else {}
    for t in trials:
        if not isinstance(t.get("trial_intent"), dict):
            t["trial_intent"] = classify_trial_intent(t)
        raw = coverage_in.get(t.get("nct_id"))
        if isinstance(raw, int) and raw > 0:
            t["coverage"] = {"parsed": len(t.get("criteria", [])), "raw_estimated": raw}
    # The ranking is the required deliverable, so it gets its own step and lands fast; the
    # question chain (2 more calls, retry-prone) is a separate request the browser makes after
    # the ranking is already on screen -- same split the answer round uses.
    recs, need = recommend(patient, trials, True)
    apply_recommendation(trials, recs)
    apply_trial_level_actions(trials)
    return {"trials": trials, "patient_need": need,
            "ranking": {"version": ranking.RANKING_VERSION, "rule_ko": ranking.RANKING_RULE_KO,
                        "hard_exclusion_holds": ranking.hard_exclusion_holds(trials)}}


def step_questions(body):
    """Clarifying questions for a live patient: detect_gaps -> generate_questions over the
    matched trials. Runs after the ranking is displayed; a failure costs questions, not the
    recommendation."""
    t0 = time.monotonic()
    text = str(body.get("text", "")).strip()[:MAX_VIGNETTE]
    trials = body.get("trials")
    if not text or not isinstance(trials, list) or not trials:
        return {"error": "invalid questions request"}
    patient = {"patient_id": "LIVE", "text": text}
    trials = [dict(t, criteria=list(t.get("criteria", []))[:MAX_CRITERIA_PER_TRIAL])
              for t in trials[:MAX_TRIALS]]
    flat = [{"nct_id": t["nct_id"], "text": c.get("text", ""), "verdict": c.get("verdict"),
             "action": c.get("action"), "effect": c.get("effect")}
            for t in trials for c in t["criteria"]]
    try:
        gaps = detect_gaps(patient, flat)
        if time.monotonic() - t0 > STEP_BUDGET_S:   # gap detection already ate the budget
            return {"questions": [], "questions_error": "확인 질문 생성 시간이 초과되었습니다."}
        questions = generate_questions(patient, gaps)
        enrich_questions(questions, gaps, trials)
        return {"questions": questions}
    except Exception as e:  # noqa: BLE001 -- never lose the already-delivered ranking
        return {"questions": [], "questions_error": f"확인 질문 생성 실패: {e}"}


STEPS = {"start": step_start, "match": step_match, "finish": step_finish,
         "questions": step_questions}


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        ip = self.headers.get("x-forwarded-for", "?").split(",")[0].strip()
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length) or b"{}")
        except Exception:  # noqa: BLE001
            body, length = {}, 0
        if DEMO_KEY and str(body.get("key", "")) != DEMO_KEY:
            result = {"error": "이 데모의 실시간 입력은 발표자 코드가 필요합니다."}
        elif _rate_limited(ip):
            result = {"error": "요청이 너무 잦습니다. 잠시 후 다시 시도해 주세요."}
        else:
            fn = STEPS.get(str(body.get("step", "")))
            if not fn:
                result = {"error": "unknown step"}
            else:
                try:
                    result = fn(body)
                except Exception as e:  # noqa: BLE001
                    result = {"error": f"{type(e).__name__}: {e}"}
        payload = json.dumps(result, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)
