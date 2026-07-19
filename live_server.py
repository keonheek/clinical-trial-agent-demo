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
import json
import os
import re
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

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

with open(os.path.join(HERE, "traces.json")) as f:
    TRACES = json.load(f)
TRACES_BY_ID = {t["patient_id"]: t for t in TRACES}

with open(os.path.join(HERE, "trials_raw.json")) as f:
    TRIALS_RAW = json.load(f)
_all_trials = {}
for _entry in TRIALS_RAW.values():
    for _t in _entry["trials"]:
        _all_trials[_t["nct_id"]] = _t
ALL_TRIALS = list(_all_trials.values())

SESSIONS = {}
SESSIONS_LOCK = threading.Lock()

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
    except Exception as e:
        session["stage"] = "error"
        session["error"] = str(e)


def build_session_live(session):
    try:
        patient = session["patient"]
        session["stage"] = "extract"
        fields, dropped = extract_patient(patient)
        session["extraction"] = fields

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
    except Exception as e:
        session["stage"] = "error"
        session["error"] = str(e)


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


def handle_answer(session, question_text, answer_text):
    with session["lock"]:
        affected = find_affected(session, question_text)
        round_n = len(session.get("answer_rounds", [])) + 1
        session["extended_record"] = (
            session.get("extended_record", "") + f"\n추가 문진 Q: {question_text} / A: {answer_text}"
        ).strip()

        if not affected:
            session.setdefault("answer_rounds", []).append({
                "round": round_n, "question": question_text, "answer": answer_text, "verdict_changes": [],
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

        session.setdefault("answer_rounds", []).append({
            "round": round_n, "question": question_text, "answer": answer_text, "verdict_changes": verdict_changes,
        })

        return {
            "verdict_changes": verdict_changes,
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
            "answer_rounds": session.get("answer_rounds", []),
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

            if path == "/api/patients":
                out = []
                for pid in sorted(PATIENTS_BY_ID):
                    p = PATIENTS_BY_ID[pid]
                    out.append({"id": pid, "title": p.get("condition", pid), "vignette": p["text"]})
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
    server = ThreadingHTTPServer(("localhost", PORT), Handler)
    print(f"live_server listening on http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
