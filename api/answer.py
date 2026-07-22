"""POST /api/answer -> re-evaluate only the criteria a human answer affects, re-rank, return.

Serverless functions share no memory, so the browser holds the session state (the current
trials array and the accumulated extended_record) and sends it back on every call. This module
is a pure function of its request body: patient_id + question + answer + trials + extended_record
in, updated trials + verdict_changes + extended_record out.

Reuses pipeline.py's rematch_affected_criteria/recommend/effect_of directly (same functions
live_server.py uses locally) -- no matching logic duplicated here. The only new piece is
find_affected(), a token-overlap heuristic standing in for live_server.py's gap-detector-based
mapping, so this endpoint makes exactly two LLM calls (rematch, recommend) instead of three.

Never raises past do_POST: any failure comes back as HTTP 200 {"error": "..."}.
"""
import json
import os
import re
import sys
from http.server import BaseHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault("LLM_BACKEND", "anthropic")

import anthropic_client
# Vercel's Python runtime filesystem is read-only except /tmp. anthropic_client's on-disk
# cache is a nice-to-have (repeat calls within one invocation, none across cold starts), not
# a correctness requirement, so point it at the one writable directory instead of editing the
# shared file.
anthropic_client.CACHE_DIR = "/tmp/cache"

from pipeline import rematch_affected_criteria, recommend, effect_of, VALID_VERDICTS, classify_action

with open(os.path.join(ROOT, "patients.json"), encoding="utf-8") as f:
    PATIENTS = json.load(f)
PATIENTS_BY_ID = {p["patient_id"]: p for p in PATIENTS}
KNOWN_IDS = set(PATIENTS_BY_ID)

# The client resends its trials array on every call, but every legitimate criterion for these
# fixed patients originated in traces.json -- so anything not in that whitelist is either a bug
# or an attempt to inject text into a prompt running on the metered key. Whitelist per patient:
# {(nct_id, criterion_text) -> criterion_type}.
with open(os.path.join(ROOT, "traces.json"), encoding="utf-8") as f:
    _TRACES = json.load(f)
KNOWN_CRITERIA = {}
for _p in _TRACES:
    KNOWN_CRITERIA[_p["patient_id"]] = {
        (t["nct_id"], c["text"]): c["type"]
        for t in _p.get("trials", []) for c in t.get("criteria", [])
    }
del _TRACES

# ---------------------------------------------------------------------------
# cost guards -- this endpoint spends a real metered API key
# ---------------------------------------------------------------------------
MAX_ANSWER_LEN = 600
MAX_QUESTION_LEN = 300
MAX_AFFECTED = 12
MAX_BODY_BYTES = 128 * 1024      # real sessions serialize to a few KB
MAX_TRIALS = 6                   # traces hold 4 per patient
MAX_CRITERIA_PER_TRIAL = 16      # traces max is 13
RATE_LIMIT_PER_MIN = 10          # per client IP, per warm instance (cheap brake, not a wall)

_recent_calls = {}               # ip -> [monotonic-ish timestamps]


def _rate_limited(ip):
    import time
    now = time.time()
    window = [t for t in _recent_calls.get(ip, []) if now - t < 60]
    if len(window) >= RATE_LIMIT_PER_MIN:
        _recent_calls[ip] = window
        return True
    window.append(now)
    _recent_calls[ip] = window
    return False


def _validate_trials(patient_id, trials):
    """Reject anything the frozen traces never produced. Returns an error string or None."""
    if len(trials) > MAX_TRIALS:
        return "too many trials"
    known = KNOWN_CRITERIA.get(patient_id, {})
    for t in trials:
        criteria = t.get("criteria", [])
        if len(criteria) > MAX_CRITERIA_PER_TRIAL:
            return "too many criteria"
        for c in criteria:
            key = (t.get("nct_id"), c.get("text"))
            if key not in known:
                return "unknown criterion for this patient"
            if c.get("type") != known[key]:
                return "criterion type mismatch"
            if c.get("verdict") is not None and c.get("verdict") not in VALID_VERDICTS:
                return "invalid verdict value"
    return None

STOPWORDS = set(
    "the a an of and or in on at to is are was were for this that with have has any does "
    "he she his her what when who which been from as by".split()
)


def _tokens(text):
    return set(
        w for w in re.findall(r"[a-z0-9%.]+", (text or "").lower())
        if w not in STOPWORDS and len(w) > 2
    )


def find_affected(question_text, trials):
    """Which still-unresolved criteria does this answer plausibly bear on? live_server.py
    answers this from an LLM-built gap -> related_criteria map; that map does not exist here
    (traces.json stores questions but not the gaps that produced them), so this does the same
    job with token overlap between the question and each candidate criterion's text -- the
    fallback path live_server.py itself falls back to when a question has no mapped gap."""
    qtok = _tokens(question_text)
    affected = []
    for t_idx, t in enumerate(trials):
        for c_idx, c in enumerate(t.get("criteria", [])):
            if c.get("verdict") not in ("UNKNOWN", "UNCERTAIN"):
                continue
            if qtok & _tokens(c.get("text", "")):
                affected.append({
                    "nct_id": t.get("nct_id"), "trial_idx": t_idx, "crit_idx": c_idx,
                    "text": c.get("text", ""), "type": c.get("type", "inclusion"),
                    "before_verdict": c.get("verdict"),
                })
    if not affected:
        # no token overlap at all: still resolve every open criterion rather than silently
        # dropping the answer on the floor.
        for t_idx, t in enumerate(trials):
            for c_idx, c in enumerate(t.get("criteria", [])):
                if c.get("verdict") in ("UNKNOWN", "UNCERTAIN"):
                    affected.append({
                        "nct_id": t.get("nct_id"), "trial_idx": t_idx, "crit_idx": c_idx,
                        "text": c.get("text", ""), "type": c.get("type", "inclusion"),
                        "before_verdict": c.get("verdict"),
                    })
    return affected[:MAX_AFFECTED]


def handle(body):
    patient_id = str(body.get("patient_id", "")).strip()
    question = str(body.get("question", "")).strip()
    answer = str(body.get("answer", "")).strip()
    trials = body.get("trials")
    extended_record = str(body.get("extended_record", "")).strip()

    if patient_id not in KNOWN_IDS:
        return {"error": "unknown patient_id"}
    if not question or len(question) > MAX_QUESTION_LEN:
        return {"error": "invalid question"}
    if not answer or len(answer) > MAX_ANSWER_LEN:
        return {"error": "answer must be 1-600 characters"}
    if not isinstance(trials, list) or not trials:
        return {"error": "trials array required"}
    trials_error = _validate_trials(patient_id, trials)
    if trials_error:
        return {"error": trials_error}

    # never trust the client for the vignette itself -- only the fixed 10 patients exist here.
    patient = {"patient_id": patient_id, "text": PATIENTS_BY_ID[patient_id]["text"]}

    trials_copy = [dict(t, criteria=[dict(c) for c in t.get("criteria", [])]) for t in trials]
    affected = find_affected(question, trials_copy)
    new_record = (extended_record + f"\n추가 문진 Q: {question} / A: {answer}").strip()

    if not affected:
        return {
            "verdict_changes": [],
            "trials": trials_copy,
            "recommendation": [
                {"nct_id": t.get("nct_id"), "rank": t.get("rank", 99), "eligibility": t.get("eligibility", "UNCERTAIN")}
                for t in trials_copy
            ],
            "extended_record": new_record,
            "note": "이 답변으로 재평가할 미확정 기준이 없습니다.",
        }

    try:
        rematched = rematch_affected_criteria(patient, new_record, affected)
    except Exception as e:
        return {"error": f"재평가 호출 실패: {e}"}

    verdict_changes = []
    for r in rematched:
        crit = trials_copy[r["trial_idx"]]["criteria"][r["crit_idx"]]
        crit["verdict"] = r["after_verdict"]
        crit["effect"] = effect_of(crit["type"], r["after_verdict"])
        # code-derived, same rule as the pipeline; clears stale badges on decided verdicts
        crit["uncertainty_type"], crit["action"] = classify_action(
            r["after_verdict"], r.get("after_uncertainty_type"))
        if r.get("after_evidence"):
            crit["evidence"] = r["after_evidence"]
        crit["reasoning"] = r.get("after_reasoning", crit.get("reasoning", ""))
        if r["after_verdict"] != r["before_verdict"]:
            verdict_changes.append({
                "nct_id": r["nct_id"], "criterion": r["text"],
                "before": r["before_verdict"], "after": r["after_verdict"],
            })

    try:
        recs = recommend(patient, trials_copy)
    except Exception as e:
        return {"error": f"추천 호출 실패: {e}"}

    for t in trials_copy:
        r = recs.get(t.get("nct_id"), {
            "eligibility": t.get("eligibility", "UNCERTAIN"),
            "rank": t.get("rank", 99),
            "rationale": t.get("rationale", ""),
        })
        t["eligibility"] = r["eligibility"]
        t["rank"] = r["rank"]
        t["rationale"] = r["rationale"]
    trials_copy.sort(key=lambda t: t.get("rank", 99))

    return {
        "verdict_changes": verdict_changes,
        "trials": trials_copy,
        "recommendation": [
            {"nct_id": t.get("nct_id"), "rank": t.get("rank"), "eligibility": t.get("eligibility")}
            for t in trials_copy
        ],
        "extended_record": new_record,
    }


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            ip = (self.headers.get("x-forwarded-for", "") or "?").split(",")[0].strip()
            length = int(self.headers.get("Content-Length", 0) or 0)
            if length > MAX_BODY_BYTES:
                result = {"error": "request too large"}
            elif _rate_limited(ip):
                result = {"error": "요청이 너무 잦습니다. 잠시 후 다시 시도해 주세요."}
            else:
                raw = self.rfile.read(length) if length > 0 else b"{}"
                body = json.loads(raw.decode("utf-8"))
                result = handle(body)
        except Exception as e:
            result = {"error": str(e)}
        out = json.dumps(result, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)
