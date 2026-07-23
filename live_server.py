#!/usr/bin/env python3
"""
live_server.py -- stdlib-only HTTP server for the LIVE interactive re-eval loop.

A human types answers to the pipeline's clarifying questions; only the criteria
those answers actually affect get re-matched (real Groq calls), then the trial
ranking is recomputed. Two entry paths:
  - known patient (S001-S010): stages loaded instantly from traces.json (demo
    insurance), "precomputed": true.
  - pasted vignette: full pipeline run live (extract -> select candidate trials
    -> parse criteria -> match -> detect gaps -> generate questions).

Reuses pipeline.py's agent functions directly -- no logic duplicated here.
Python 3 stdlib only. Run: python3 live_server.py  (serves http://localhost:8765)
"""
import copy
import json
import os
import re
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pipeline
from pipeline import (
    extract_patient,
    parse_criteria,
    match_trial,
    detect_gaps,
    generate_questions,
    recommend,
    rematch_affected_criteria,
    effect_of,
    TRIALS_PER_PATIENT,
)
from action_policy import enrich_questions

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = 8765

# ---------------------------------------------------------------------------
# static data loaded once at startup
# ---------------------------------------------------------------------------
with open(os.path.join(HERE, "patients.json")) as f:
    PATIENTS = json.load(f)
PATIENTS_BY_ID = {p["patient_id"]: p for p in PATIENTS}

# The 40 stress-test patients (5 base cases x 7 single-defect variants, 지우's set) are
# offered here too -- selecting one runs it through the LIVE pipeline exactly like a pasted
# vignette. They carry no precomputed trace, so they always take the live path; the frozen
# S001-S010 demo traces are untouched. Local only: the deployed API never exposes these.
STRESS_PATIENTS_BY_ID = {}
try:
    with open(os.path.join(HERE, "patients_stress.json")) as f:
        for _p in json.load(f):
            STRESS_PATIENTS_BY_ID[_p["patient_id"]] = _p
except FileNotFoundError:
    pass

# What each variant is SUPPOSED to induce, read straight from the human answer key rather
# than asserted here -- the letters are not a clean 1:1 map (a/b/g carry a single cause,
# c/d/e/f mix several), so hardcoding a meaning per letter would misdescribe the data.
STRESS_EXPECTED_CAUSES = {}
try:
    with open(os.path.join(HERE, "eval_labels_stress.json")) as f:
        for _row in json.load(f):
            if _row.get("uncertainty_type"):
                STRESS_EXPECTED_CAUSES.setdefault(_row["patient_id"], set()).add(
                    _row["uncertainty_type"])
except FileNotFoundError:
    pass

with open(os.path.join(HERE, "traces.json")) as f:
    TRACES = json.load(f)
TRACES_BY_ID = {t["patient_id"]: t for t in TRACES}

# Answer options for the frozen questions live in a sidecar (traces.json must not be
# regenerated -- the blind eval labels join on its criterion text). Attached in memory.
try:
    with open(os.path.join(HERE, "question_options.json"), encoding="utf-8") as f:
        _Q_OPTIONS = json.load(f)
    for _t in TRACES:
        for _q in _t.get("questions", []):
            if not _q.get("options") and _Q_OPTIONS.get(_q.get("question")):
                _q["options"] = _Q_OPTIONS[_q["question"]]
except FileNotFoundError:
    pass

# The stress patients' own trials, fetched from ClinicalTrials.gov. Without these the
# keyword picker had to choose from the S001-S010 pool, which contains no Alzheimer's or
# HFrEF trial at all -- so a 72-year-old dementia patient was scored against a paediatric
# trial and everything came back INELIGIBLE for reasons that had nothing to do with them.
STRESS_TRIALS = {}
STRESS_TRIALS_BY_PATIENT = {}
try:
    with open(os.path.join(HERE, "trials_stress.json"), encoding="utf-8") as f:
        STRESS_TRIALS = json.load(f)
    # which trials belong to which patient comes from the human answer key, not a guess
    with open(os.path.join(HERE, "eval_labels_stress.json"), encoding="utf-8") as f:
        for _row in json.load(f):
            STRESS_TRIALS_BY_PATIENT.setdefault(_row["patient_id"], set()).add(_row["nct_id"])
    # a variant inherits its base case's trials (T001-b is still the T001 bladder-cancer case)
    for _pid in list(STRESS_PATIENTS_BY_ID):
        base = _pid.rsplit("-", 1)[0] if "-" in _pid else _pid
        if not STRESS_TRIALS_BY_PATIENT.get(_pid) and STRESS_TRIALS_BY_PATIENT.get(base):
            STRESS_TRIALS_BY_PATIENT[_pid] = set(STRESS_TRIALS_BY_PATIENT[base])
except FileNotFoundError:
    pass

with open(os.path.join(HERE, "trials_raw.json")) as f:
    TRIALS_RAW = json.load(f)
_all_trials = {}
for _entry in TRIALS_RAW.values():
    for _t in _entry["trials"]:
        _all_trials[_t["nct_id"]] = _t
ALL_TRIALS = list(_all_trials.values())

# Models offerable per backend, for the local UI's picker. IDs are the exact strings the
# provider expects -- Anthropic aliases carry no date suffix. Local only: the deployed
# endpoint stays pinned to its configured model so a visitor can't select a costlier one.
MODEL_CHOICES = {
    "anthropic": [
        {"id": "claude-haiku-4-5", "label": "Haiku 4.5 (기본, 가장 저렴)"},
        {"id": "claude-sonnet-5", "label": "Sonnet 5 (균형)"},
        {"id": "claude-opus-4-8", "label": "Opus 4.8 (최고 성능, 비쌈)"},
    ],
    "claude": [
        {"id": "claude-haiku-4-5", "label": "Haiku 4.5 (기본, 가장 빠름)"},
        {"id": "claude-sonnet-5", "label": "Sonnet 5 (균형)"},
        {"id": "claude-opus-4-8", "label": "Opus 4.8 (최고 성능, 가장 느림)"},
    ],
# Fable is deliberately NOT offered in the UI: it screens inputs for bio content and can
# decline clinical prompts. It stays reachable for offline smoke tests via
# pipeline.set_active_model("claude-fable-5") in a script.
    "groq": [
        {"id": "llama-3.3-70b-versatile", "label": "Llama 3.3 70B (무료)"},
    ],
    "ollama": [
        {"id": "qwen3.6:35b", "label": "Qwen3.6 35B (로컬)"},
    ],
}

SESSIONS = {}
SESSIONS_LOCK = threading.Lock()

# Sessions live in memory, so restarting the server used to strand whoever was mid-demo
# with "session not found" and no way back. Completed sessions are mirrored to disk and
# reloaded at startup: a restart (or a crash) no longer costs a finished run.
SESSION_STORE = os.path.join(HERE, "cache", "sessions")
_SESSION_PERSIST_KEYS = ("id", "mode", "patient", "stage", "error", "extraction",
                         "trials_out", "gaps", "questions", "extended_record",
                         "answer_rounds", "created")


def persist_session(session):
    """Mirror a session to disk. Best-effort: a demo must never fail because of this."""
    try:
        os.makedirs(SESSION_STORE, exist_ok=True)
        data = {k: session.get(k) for k in _SESSION_PERSIST_KEYS}
        tmp = os.path.join(SESSION_STORE, f".{session['id']}.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        os.replace(tmp, os.path.join(SESSION_STORE, f"{session['id']}.json"))
    except Exception as e:  # noqa: BLE001 - never let persistence break a live session
        print(f"[live_server] session persist failed ({e})")


def load_persisted_sessions(max_age_hours=12):
    """Restore sessions written by a previous process, so a restart is survivable."""
    if not os.path.isdir(SESSION_STORE):
        return 0
    cutoff = time.time() - max_age_hours * 3600
    restored = 0
    for name in os.listdir(SESSION_STORE):
        if not name.endswith(".json"):
            continue
        path = os.path.join(SESSION_STORE, name)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue
        if not data.get("id") or (data.get("created") or 0) < cutoff:
            continue
        # a restored session is inert: its builder thread is gone, so anything not
        # finished is marked done at whatever stage it reached rather than hanging.
        if data.get("stage") not in ("done", "error"):
            data["stage"] = "done"
        data["lock"] = threading.Lock()
        SESSIONS[data["id"]] = data
        restored += 1
    return restored

# chronological stage order actually executed by the live pipeline
STAGE_ORDER = ["queued", "extract", "parse", "match", "gaps", "questions", "recommend", "done"]


def _tokens(text):
    return set(re.findall(r"[a-z0-9%.]+", (text or "").lower()))


def select_candidate_trials(vignette_text, fields, n=TRIALS_PER_PATIENT):
    """Heuristic keyword/condition overlap over the global trial pool. Uses the
    LLM-extracted field values (not just raw vignette text) so a non-English
    pasted vignette still matches -- the extractor normalizes clinical terms."""
    field_text = " ".join(f"{f['name']} {f['value']}" for f in fields)
    query = _tokens(vignette_text + " " + field_text)
    scored = []
    for t in ALL_TRIALS:
        cond_tok = _tokens(" ".join(t.get("conditions", [])))
        title_tok = _tokens(t.get("title", ""))
        crit_tok = _tokens(t.get("eligibility_criteria_raw", "")[:1000])
        score = 3 * len(query & cond_tok) + 2 * len(query & title_tok) + len(query & crit_tok)
        scored.append((score, t))
    scored.sort(key=lambda pair: -pair[0])
    return [t for _, t in scored[:n]]


def _ranking(trials_out):
    return [{"nct_id": t["nct_id"], "rank": t.get("rank", 99),
              "eligibility": t.get("eligibility", "UNCERTAIN"),
              "rationale": t.get("rationale", "")} for t in trials_out]


# ---------------------------------------------------------------------------
# session builders (run in a background thread per session)
# ---------------------------------------------------------------------------
def build_session_precomputed(session, trace):
    try:
        session["stage"] = "extract"
        session["extraction"] = trace["extraction"]
        time.sleep(0.35)
        session["stage"] = "parse"
        trials_out = [dict(t, criteria=[dict(c) for c in t["criteria"]]) for t in trace["trials"]]
        session["trials_out"] = trials_out
        time.sleep(0.35)
        session["stage"] = "match"
        time.sleep(0.35)
        session["stage"] = "gaps"
        time.sleep(0.35)
        session["stage"] = "questions"
        # enrich with affects_trials/affects_criteria/may_change_rank for the cards.
        # Older frozen traces carry no gaps -> enrich_questions falls back to token overlap.
        session["questions"] = enrich_questions(
            [dict(q) for q in trace["questions"]], trace.get("gaps", []), trials_out)
        time.sleep(0.35)
        session["stage"] = "recommend"
        time.sleep(0.35)
        session["stage"] = "done"
        persist_session(session)
    except Exception as e:
        session["stage"] = "error"
        session["error"] = str(e)
        persist_session(session)


def build_session_live(session):
    try:
        patient = session["patient"]
        session["stage"] = "extract"
        fields, dropped = extract_patient(patient)
        session["extraction"] = fields

        # A stress patient is scored against ITS OWN trials (the ones the human answer key
        # was written against), not whatever the keyword picker finds in the demo pool.
        pinned = STRESS_TRIALS_BY_PATIENT.get(patient.get("patient_id")) or set()
        candidates = [STRESS_TRIALS[n] for n in sorted(pinned) if n in STRESS_TRIALS]
        if not candidates:
            candidates = select_candidate_trials(patient["text"], fields, TRIALS_PER_PATIENT)
        session["trials_total"] = len(candidates)
        session["trials_done"] = 0

        trials_out = []
        all_criteria_flat = []
        session["trials_out"] = trials_out
        for t in candidates:
            session["stage"] = "parse"
            criteria = parse_criteria(t)
            session["stage"] = "match"
            matched = match_trial(patient, fields, criteria)
            for c in matched:
                all_criteria_flat.append({"nct_id": t["nct_id"], "text": c["text"],
                                           "verdict": c["verdict"], "action": c.get("action")})
            trials_out.append({
                "nct_id": t["nct_id"], "title": t["title"], "phase": t.get("phase", "NA"),
                "criteria": matched,
            })
            session["trials_done"] += 1

        session["stage"] = "gaps"
        gaps = detect_gaps(patient, all_criteria_flat)
        session["gaps"] = gaps

        session["stage"] = "questions"
        questions = generate_questions(patient, gaps)
        session["questions"] = questions

        session["stage"] = "recommend"
        recs = recommend(patient, trials_out)
        for t in trials_out:
            r = recs.get(t["nct_id"], {"eligibility": "UNCERTAIN", "rank": 99, "rationale": ""})
            t["eligibility"] = r["eligibility"]
            t["rank"] = r["rank"]
            t["rationale"] = r["rationale"]
        trials_out.sort(key=lambda t: t["rank"])

        # priority numbers now that eligibility/rank are decided
        enrich_questions(questions, gaps, trials_out)

        session["stage"] = "done"
        persist_session(session)
    except Exception as e:
        session["stage"] = "error"
        session["error"] = str(e)
        persist_session(session)


# ---------------------------------------------------------------------------
# answer round: reuse run_reeval's field->criteria mapping logic, but with a
# REAL human answer instead of a simulated one.
# ---------------------------------------------------------------------------
def ensure_gaps(session):
    if session.get("gaps") is None:
        all_criteria_flat = [
            {"nct_id": t["nct_id"], "text": c["text"], "verdict": c["verdict"], "action": c.get("action")}
            for t in session["trials_out"] for c in t["criteria"]
        ]
        session["gaps"] = detect_gaps(session["patient"], all_criteria_flat)
    return session["gaps"]


def find_affected(session, question_text):
    trials_out = session["trials_out"]
    gaps = ensure_gaps(session)
    gaps_by_field = {g["field"]: g for g in gaps}

    field = None
    for q in session.get("questions", []):
        if q["question"] == question_text:
            field = q.get("field")
            break

    target_texts = set()
    if field and field in gaps_by_field:
        target_texts.update(gaps_by_field[field].get("related_criteria", []))
    if not target_texts:
        # fallback: token overlap between the question and any gap's field/why_needed
        qtok = _tokens(question_text)
        for g in gaps:
            gtok = _tokens(g["field"] + " " + g.get("why_needed", ""))
            if qtok & gtok:
                target_texts.update(g.get("related_criteria", []))

    affected = []
    for t_idx, t in enumerate(trials_out):
        for c_idx, c in enumerate(t["criteria"]):
            if c["verdict"] not in ("UNKNOWN", "UNCERTAIN"):
                continue
            if target_texts and c["text"] not in target_texts:
                continue
            affected.append({
                "nct_id": t["nct_id"], "trial_idx": t_idx, "crit_idx": c_idx,
                "text": c["text"], "type": c["type"], "before_verdict": c["verdict"],
            })
    return affected


def eligibility_path(trial):
    """What stands between this patient and enrolment on this trial.

    This is the screening worklist a coordinator actually keeps: what has already been
    satisfied, what is blocking, and what still has to be chased down (with the action the
    policy layer chose). Derived entirely from criteria already computed -- no extra call.
    """
    blocking, to_resolve, satisfied = [], [], []
    for c in trial.get("criteria", []):
        entry = {"text": c.get("text"), "type": c.get("type"), "verdict": c.get("verdict"),
                 "evidence": c.get("evidence"), "action": c.get("action"),
                 "uncertainty_type": c.get("uncertainty_type")}
        eff = c.get("effect")
        if eff == "FAIL":
            blocking.append(entry)
        elif eff == "PASS":
            satisfied.append(entry)
        else:
            to_resolve.append(entry)
    if blocking:
        verdict = "제외 사유 있음"
    elif to_resolve:
        verdict = f"확인 {len(to_resolve)}건 남음"
    else:
        verdict = "선별 통과"
    return {"blocking": blocking, "to_resolve": to_resolve, "satisfied": satisfied,
            "summary": verdict, "n_blocking": len(blocking),
            "n_to_resolve": len(to_resolve), "n_satisfied": len(satisfied)}


def handle_answers_batch(session, items):
    """Apply several answers, then re-evaluate once. One snapshot covers the whole batch,
    so a single revert undoes the batch the way the reviewer entered it."""
    with session["lock"]:
        before = _snapshot(session)
        round_n = len(session.get("answer_rounds", [])) + 1
        applied, affected_all = [], []
        seen = set()
        for it in items:
            q = str(it.get("question", "")).strip()
            a = str(it.get("answer", "")).strip()
            if not q or not a:
                continue
            session["extended_record"] = (
                session.get("extended_record", "") + f"\n추가 문진 Q: {q} / A: {a}"
            ).strip()
            applied.append({"question": q, "answer": a})
            for af in find_affected(session, q):
                key = (af["nct_id"], af["text"])
                if key not in seen:
                    seen.add(key)
                    affected_all.append(af)

        if not applied:
            return {"error": "no usable answers"}

        verdict_changes = []
        if affected_all:
            rematched = rematch_affected_criteria(session["patient"],
                                                   session["extended_record"], affected_all)
            for r in rematched:
                crit = session["trials_out"][r["trial_idx"]]["criteria"][r["crit_idx"]]
                crit["verdict"] = r["after_verdict"]
                crit["effect"] = effect_of(crit["type"], r["after_verdict"])
                if r["after_evidence"]:
                    crit["evidence"] = r["after_evidence"]
                crit["reasoning"] = r["after_reasoning"]
                if r["after_verdict"] != r["before_verdict"]:
                    verdict_changes.append({"nct_id": r["nct_id"], "criterion": r["text"],
                                             "before": r["before_verdict"],
                                             "after": r["after_verdict"]})
            recs = recommend(session["patient"], session["trials_out"])
            for t in session["trials_out"]:
                r = recs.get(t["nct_id"], {"eligibility": t.get("eligibility", "UNCERTAIN"),
                                            "rank": t.get("rank", 99),
                                            "rationale": t.get("rationale", "")})
                t["eligibility"], t["rank"], t["rationale"] = r["eligibility"], r["rank"], r["rationale"]
            session["trials_out"].sort(key=lambda t: t["rank"])

        rank_changes = []
        for t in session["trials_out"]:
            prev = next((b for b in before["trials_out"] if b["nct_id"] == t["nct_id"]), None)
            if prev and (prev.get("rank") != t.get("rank")
                         or prev.get("eligibility") != t.get("eligibility")):
                rank_changes.append({"nct_id": t["nct_id"], "title": t.get("title"),
                                      "rank_before": prev.get("rank"), "rank_after": t.get("rank"),
                                      "eligibility_before": prev.get("eligibility"),
                                      "eligibility_after": t.get("eligibility")})

        session.setdefault("answer_rounds", []).append({
            "round": round_n, "batch": applied,
            "question": " / ".join(i["question"] for i in applied),
            "answer": " / ".join(i["answer"] for i in applied),
            "verdict_changes": verdict_changes, "rank_changes": rank_changes, "_before": before,
        })
        persist_session(session)
        return {
            "round": round_n, "applied": applied,
            "verdict_changes": verdict_changes, "rank_changes": rank_changes,
            "affected": [{"nct_id": a["nct_id"], "text": a["text"]} for a in affected_all],
            "updated_trials": session["trials_out"],
            "recommendation": _ranking(session["trials_out"]),
        }


def _snapshot(session):
    """Deep copy of everything an answer round mutates, so a round can be undone."""
    return {
        "trials_out": copy.deepcopy(session.get("trials_out", [])),
        "extended_record": session.get("extended_record", ""),
        "gaps": copy.deepcopy(session.get("gaps")),
    }


def revert_last_round(session):
    """Undo the most recent answer round. Reviewers try an answer to see what it moves;
    without this they would have to rebuild the whole session to take it back."""
    with session["lock"]:
        rounds = session.get("answer_rounds") or []
        if not rounds:
            return {"error": "되돌릴 답변이 없습니다."}
        last = rounds.pop()
        snap = last.get("_before")
        if not snap:
            rounds.append(last)
            return {"error": "이 답변은 되돌릴 수 없습니다 (이전 상태 미기록)."}
        session["trials_out"] = copy.deepcopy(snap["trials_out"])
        session["extended_record"] = snap["extended_record"]
        session["gaps"] = copy.deepcopy(snap["gaps"])
        persist_session(session)
        return {
            "reverted_round": last.get("round"),
            "reverted_question": last.get("question"),
            "updated_trials": session["trials_out"],
            "recommendation": _ranking(session["trials_out"]),
            "rounds_left": len(rounds),
        }


def handle_answer(session, question_text, answer_text):
    with session["lock"]:
        before = _snapshot(session)
        affected = find_affected(session, question_text)
        round_n = len(session.get("answer_rounds", [])) + 1
        session["extended_record"] = (
            session.get("extended_record", "") + f"\n추가 문진 Q: {question_text} / A: {answer_text}"
        ).strip()

        if not affected:
            session.setdefault("answer_rounds", []).append({
                "round": round_n, "question": question_text, "answer": answer_text,
                "verdict_changes": [], "_before": before,
            })
            return {
                "verdict_changes": [], "affected": [],
                "updated_trials": session["trials_out"],
                "recommendation": _ranking(session["trials_out"]),
                "round": round_n,
                "note": "이 답변으로 재평가할 미확정 기준이 없습니다.",
            }

        rematched = rematch_affected_criteria(session["patient"], session["extended_record"], affected)
        verdict_changes = []
        for r in rematched:
            crit = session["trials_out"][r["trial_idx"]]["criteria"][r["crit_idx"]]
            crit["verdict"] = r["after_verdict"]
            crit["effect"] = effect_of(crit["type"], r["after_verdict"])
            if r["after_evidence"]:
                crit["evidence"] = r["after_evidence"]
            crit["reasoning"] = r["after_reasoning"]
            if r["after_verdict"] != r["before_verdict"]:
                verdict_changes.append({
                    "nct_id": r["nct_id"], "criterion": r["text"],
                    "before": r["before_verdict"], "after": r["after_verdict"],
                })

        recs = recommend(session["patient"], session["trials_out"])
        for t in session["trials_out"]:
            r = recs.get(t["nct_id"], {"eligibility": t.get("eligibility", "UNCERTAIN"),
                                        "rank": t.get("rank", 99), "rationale": t.get("rationale", "")})
            t["eligibility"] = r["eligibility"]
            t["rank"] = r["rank"]
            t["rationale"] = r["rationale"]
        session["trials_out"].sort(key=lambda t: t["rank"])

        rank_changes = []
        for t in session["trials_out"]:
            prev = next((b for b in before["trials_out"] if b["nct_id"] == t["nct_id"]), None)
            if prev and (prev.get("rank") != t.get("rank") or prev.get("eligibility") != t.get("eligibility")):
                rank_changes.append({"nct_id": t["nct_id"], "title": t.get("title"),
                                      "rank_before": prev.get("rank"), "rank_after": t.get("rank"),
                                      "eligibility_before": prev.get("eligibility"),
                                      "eligibility_after": t.get("eligibility")})

        session.setdefault("answer_rounds", []).append({
            "round": round_n, "question": question_text, "answer": answer_text,
            "verdict_changes": verdict_changes, "rank_changes": rank_changes, "_before": before,
        })
        persist_session(session)

        return {
            "verdict_changes": verdict_changes,
            "rank_changes": rank_changes,
            "affected": [{"nct_id": a["nct_id"], "text": a["text"]} for a in affected],
            "updated_trials": session["trials_out"],
            "recommendation": _ranking(session["trials_out"]),
            "round": round_n,
        }


# ---------------------------------------------------------------------------
# HTTP layer
# ---------------------------------------------------------------------------
ROUTE_SESSION = re.compile(r"^/api/session/([a-f0-9]{32})$")
ROUTE_ANSWER = re.compile(r"^/api/session/([a-f0-9]{32})/answer$")
ROUTE_ANSWER_BATCH = re.compile(r"^/api/session/([a-f0-9]{32})/answers$")
ROUTE_REVERT = re.compile(r"^/api/session/([a-f0-9]{32})/revert$")


def session_snapshot(session):
    return {
        "session_id": session["id"],
        "mode": session["mode"],
        "stage": session["stage"],
        "error": session.get("error"),
        "progress": {"trials_done": session.get("trials_done", 0), "trials_total": session.get("trials_total", 0)},
        "result": {
            "patient": {"patient_id": session["patient"]["patient_id"], "text": session["patient"]["text"]},
            "extraction": session.get("extraction", []),
            "trials": session.get("trials_out", []),
            "questions": session.get("questions", []),
            "extended_record": session.get("extended_record", ""),
            # _before holds a deep copy for revert; it is internal and must not be shipped
            "answer_rounds": [{k: v for k, v in r.items() if k != "_before"}
                              for r in session.get("answer_rounds", [])],
            "eligibility_paths": {t["nct_id"]: eligibility_path(t)
                                   for t in session.get("trials_out", [])},
            "can_revert": bool(session.get("answer_rounds")),
        },
    }


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        print(f"[live_server] {self.address_string()} {fmt % args}")

    def _send_json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        try:
            if path == "/":
                with open(os.path.join(HERE, "live.html"), "rb") as f:
                    body = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            if path == "/api/meta":
                # report the backend actually in use -- the badge used to hardcode "Groq"
                # and kept saying so after the default moved to Anthropic/subscription.
                backend = os.environ.get("LLM_BACKEND", "anthropic")
                self._send_json({
                    "backend": backend,
                    "model": getattr(pipeline, "ACTIVE_MODEL", "unknown"),
                    "default_model": getattr(pipeline, "DEFAULT_MODEL", "unknown"),
                    "models": MODEL_CHOICES.get(backend, []),
                })
                return

            if path == "/api/patients":
                out = []
                for pid in sorted(PATIENTS_BY_ID):
                    p = PATIENTS_BY_ID[pid]
                    out.append({"id": pid, "title": p.get("condition", pid), "vignette": p["text"],
                                "group": "demo"})
                for pid in sorted(STRESS_PATIENTS_BY_ID):
                    p = STRESS_PATIENTS_BY_ID[pid]
                    causes = sorted(STRESS_EXPECTED_CAUSES.get(pid, ()))
                    is_variant = "-" in pid
                    if causes:
                        note = "정답지 예상 원인: " + ", ".join(causes)
                    elif is_variant:
                        # a variant with no labeled cause is NOT the original: the corruption
                        # exists, it just still leaves the criterion decidable (expected MET).
                        note = "변형 (판정 가능 — 원인 표기 없음)"
                    else:
                        note = "원본 (손상 없음)"
                    out.append({"id": pid, "title": p.get("condition", pid),
                                "vignette": p["text"], "group": "stress",
                                "expected_causes": causes, "is_variant": is_variant,
                                "note": note})
                self._send_json(out)
                return

            m = ROUTE_SESSION.match(path)
            if m:
                session = SESSIONS.get(m.group(1))
                if not session:
                    self._send_json({"error": "session not found"}, status=404)
                    return
                self._send_json(session_snapshot(session))
                return

            self._send_json({"error": "not found"}, status=404)
        except Exception as e:
            self._send_json({"error": str(e)}, status=200)

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        try:
            if path == "/api/meta":
                # switch the model for subsequent runs; only ids offered for this backend
                body = self._read_json_body()
                backend = os.environ.get("LLM_BACKEND", "anthropic")
                wanted = str(body.get("model", "")).strip()
                allowed = {m["id"] for m in MODEL_CHOICES.get(backend, [])}
                if wanted not in allowed:
                    self._send_json({"error": f"model not available on backend {backend}"},
                                     status=400)
                    return
                self._send_json({"backend": backend, "model": pipeline.set_active_model(wanted)})
                return

            if path == "/api/session":
                body = self._read_json_body()
                patient_id = str(body.get("patient_id", "")).strip()
                vignette = str(body.get("vignette", "")).strip()

                if patient_id and patient_id in PATIENTS_BY_ID:
                    patient = PATIENTS_BY_ID[patient_id]
                    trace = TRACES_BY_ID.get(patient_id)
                    if not trace:
                        self._send_json({"error": f"no precomputed trace for {patient_id}"}, status=200)
                        return
                    sid = uuid.uuid4().hex
                    session = {
                        "id": sid, "mode": "precomputed", "patient": patient, "stage": "queued",
                        "error": None, "extraction": [], "trials_out": [], "gaps": None,
                        "questions": [], "extended_record": "", "answer_rounds": [],
                        "lock": threading.Lock(), "created": time.time(),
                    }
                    with SESSIONS_LOCK:
                        SESSIONS[sid] = session
                    threading.Thread(target=build_session_precomputed, args=(session, trace), daemon=True).start()
                    self._send_json({"session_id": sid, "mode": "precomputed"})
                    return

                # stress patients have no precomputed trace by design -- they take the same
                # live path as a pasted vignette, keeping their own id for the changelog.
                if patient_id and patient_id in STRESS_PATIENTS_BY_ID:
                    sp = STRESS_PATIENTS_BY_ID[patient_id]
                    sid = uuid.uuid4().hex
                    session = {
                        "id": sid, "mode": "live",
                        "patient": {"patient_id": patient_id, "text": sp["text"]},
                        "stage": "queued", "error": None, "extraction": [], "trials_out": [],
                        "gaps": None, "questions": [], "extended_record": "", "answer_rounds": [],
                        "lock": threading.Lock(), "created": time.time(),
                    }
                    with SESSIONS_LOCK:
                        SESSIONS[sid] = session
                    threading.Thread(target=build_session_live, args=(session,), daemon=True).start()
                    self._send_json({"session_id": sid, "mode": "live"})
                    return

                if vignette:
                    sid = uuid.uuid4().hex
                    patient = {"patient_id": f"CUSTOM-{sid[:8]}", "text": vignette}
                    session = {
                        "id": sid, "mode": "live", "patient": patient, "stage": "queued",
                        "error": None, "extraction": [], "trials_out": [], "gaps": None,
                        "questions": [], "extended_record": "", "answer_rounds": [],
                        "lock": threading.Lock(), "created": time.time(),
                    }
                    with SESSIONS_LOCK:
                        SESSIONS[sid] = session
                    threading.Thread(target=build_session_live, args=(session,), daemon=True).start()
                    self._send_json({"session_id": sid, "mode": "live"})
                    return

                self._send_json({"error": "provide patient_id or vignette"}, status=400)
                return

            m = ROUTE_ANSWER_BATCH.match(path)
            if m:
                # Answer several questions, then re-evaluate ONCE. Answering one at a time
                # costs a full re-match + recommend per question; a reviewer filling in a
                # chart wants to enter what they know and see the consequence together.
                session = SESSIONS.get(m.group(1))
                if not session:
                    self._send_json({"error": "session not found"}, status=404)
                    return
                body = self._read_json_body()
                items = body.get("answers")
                if not isinstance(items, list) or not items:
                    self._send_json({"error": "answers[] required"}, status=400)
                    return
                if session["stage"] != "done":
                    self._send_json({"error": f"session not ready (stage={session['stage']})"}, status=200)
                    return
                try:
                    self._send_json(handle_answers_batch(session, items))
                except Exception as e:
                    self._send_json({"error": str(e)}, status=200)
                return

            m = ROUTE_REVERT.match(path)
            if m:
                session = SESSIONS.get(m.group(1))
                if not session:
                    self._send_json({"error": "session not found"}, status=404)
                    return
                self._send_json(revert_last_round(session))
                return

            m = ROUTE_ANSWER.match(path)
            if m:
                session = SESSIONS.get(m.group(1))
                if not session:
                    self._send_json({"error": "session not found"}, status=404)
                    return
                body = self._read_json_body()
                question = str(body.get("question", "")).strip()
                answer = str(body.get("answer", "")).strip()
                if not question or not answer:
                    self._send_json({"error": "question and answer are required"}, status=400)
                    return
                if session["stage"] != "done":
                    self._send_json({"error": f"session not ready (stage={session['stage']})"}, status=200)
                    return
                try:
                    result = handle_answer(session, question, answer)
                    self._send_json(result)
                except Exception as e:
                    self._send_json({"error": str(e)}, status=200)
                return

            self._send_json({"error": "not found"}, status=404)
        except Exception as e:
            self._send_json({"error": str(e)}, status=200)


def main():
    restored = load_persisted_sessions()
    if restored:
        print(f"[live_server] restored {restored} session(s) from a previous run")
    server = ThreadingHTTPServer(("localhost", PORT), Handler)
    print(f"live_server listening on http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
