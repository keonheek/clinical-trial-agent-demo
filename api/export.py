"""POST /api/export -> the signed screening record (xlsx) for the patient currently on screen.

The browser sends its own state (trials as displayed, the answer log, the verdict changes from
every applied round). The workbook is the same one export_report.py writes from traces.json --
스크리닝 로그, 적격성 체크리스트, 질의응답 이력, 정정 로그, 근거 원문, 메타 -- built in memory and
returned as a download. No LLM call, no key spend; pure code over the state the reviewer already
sees, so a coordinator can file what the board showed without a terminal.
"""
import datetime
import hashlib
import json
import os
import sys
from http.server import BaseHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import export_report  # noqa: E402

MAX_BODY = 2_000_000


def _trace_from_state(body):
    trials = []
    changes = body.get("verdict_changes") or []
    before_by = {(c.get("nct_id"), c.get("criterion")): c.get("before") for c in changes if c.get("before")}
    for t in body.get("trials") or []:
        crits = []
        for c in t.get("criteria") or []:
            c = dict(c)
            # the board holds the CURRENT verdict; the record needs the initial one underneath
            # so the corrections log can show before -> after. Roll back to the first "before".
            b = before_by.get((t.get("nct_id"), c.get("text")))
            if b:
                c["verdict"] = b
                c["effect"] = export_report.effect_of(c.get("type"), b)
            crits.append(c)
        trials.append({"nct_id": t.get("nct_id"), "title": t.get("title"), "phase": t.get("phase"),
                       "eligibility": t.get("eligibility_initial") or t.get("eligibility"),
                       "rank": t.get("rank"), "rationale": t.get("rationale"),
                       "trial_intent": t.get("trial_intent"), "criteria": crits})
    # keep only the LAST change per criterion (multi-round: initial -> final)
    last = {}
    for c in changes:
        last[(c.get("nct_id"), c.get("criterion"))] = {"nct_id": c.get("nct_id"), "criterion": c.get("criterion"),
                                                       "before": before_by.get((c.get("nct_id"), c.get("criterion")), c.get("before")),
                                                       "after": c.get("after")}
    answers = [{"question": a.get("question", ""), "answer": a.get("answer", ""), "evidence_quote": ""}
               for a in body.get("answers") or [] if a.get("question")]
    return {
        "patient_id": str(body.get("patient_id") or "LIVE")[:32],
        "patient_text": str(body.get("patient_text") or ""),
        "extraction": body.get("extraction") or [],
        "trials": trials,
        "questions": body.get("questions") or [],
        "reeval": {"extended_record": "", "answers": answers,
                   "verdict_changes": list(last.values()), "final_ranking": []},
        "generated_at": datetime.date.today().isoformat(),
    }


def handle(body):
    trace = _trace_from_state(body)
    if not trace["trials"]:
        return None, "trials array required"
    raw = json.dumps(body, ensure_ascii=False, sort_keys=True).encode("utf-8")
    digest = hashlib.sha256(raw).hexdigest()
    traces = export_report.prepare_traces([trace])
    data = export_report.build_workbook_bytes(traces, "board-state.json", digest)
    stamp = datetime.date.today().strftime("%y%m%d")
    name = f"screening_record_{trace['patient_id']}_{stamp}.xlsx"
    return (data, name), None


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0") or "0")
            if length > MAX_BODY:
                return self._json(413, {"error": "payload too large"})
            raw = self.rfile.read(length) if length > 0 else b"{}"
            body = json.loads(raw.decode("utf-8"))
        except Exception:
            return self._json(400, {"error": "invalid JSON body"})
        try:
            result, err = handle(body)
        except Exception as e:  # never a stack trace to the browser
            return self._json(500, {"error": f"export failed: {type(e).__name__}"})
        if err:
            return self._json(400, {"error": err})
        data, name = result
        self.send_response(200)
        self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        self.send_header("Content-Disposition", f"attachment; filename=\"{name}\"")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _json(self, code, obj):
        payload = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, *a):
        pass
