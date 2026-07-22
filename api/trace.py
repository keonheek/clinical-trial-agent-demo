"""GET /api/trace?patient_id=S001 -> the full precomputed trace for that patient.

Reads traces.json only. Zero LLM calls, instant.
"""
import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# action_policy is a pure module (no LLM client imports) -- safe to bundle serverless.
from action_policy import action_for

with open(os.path.join(ROOT, "traces.json"), encoding="utf-8") as f:
    TRACES = json.load(f)
TRACES_BY_ID = {t["patient_id"]: t for t in TRACES}

# Serve-time coverage enrichment: traces.json is a frozen artifact (regenerating it silently
# unpairs the blind eval labels), so parsing coverage is attached here, in memory. The map
# {nct_id -> criterion-like clauses in the raw protocol} is precomputed by
# pipeline.estimate_raw_criteria_count over trials_raw.json (see repo root coverage_map.json)
# so this endpoint stays dependency-free and instant.
try:
    with open(os.path.join(ROOT, "coverage_map.json"), encoding="utf-8") as f:
        _RAW_COUNT = json.load(f)
    for _trace in TRACES:
        for _t in _trace.get("trials", []):
            raw_n = _RAW_COUNT.get(_t["nct_id"])
            if raw_n:
                _t["coverage"] = {"parsed": len(_t.get("criteria", [])), "raw_estimated": raw_n}
except FileNotFoundError:
    pass  # coverage is an enrichment, never a reason for the trace endpoint to fail

# Multi-select answer options for the frozen questions, same sidecar pattern as coverage.
try:
    with open(os.path.join(ROOT, "question_options.json"), encoding="utf-8") as f:
        _Q_OPTIONS = json.load(f)
    for _trace in TRACES:
        for _q in _trace.get("questions", []):
            if not _q.get("options") and _Q_OPTIONS.get(_q.get("question")):
                _q["options"] = _Q_OPTIONS[_q["question"]]
except FileNotFoundError:
    pass

# The frozen traces predate the uncertainty/action fields and must never be regenerated
# (relabelling constraint). Derive both at serve time with the SAME policy code the live
# pipeline uses for metadata-less verdicts: UNKNOWN means the record is silent (MISSING ->
# its policy action), UNCERTAIN with no recorded cause fails safe to a human (action_for(None)
# -> ESCALATE). This is the policy's real output for these inputs, not a display guess.
for _trace in TRACES:
    for _t in _trace.get("trials", []):
        for _c in _t.get("criteria", []):
            if _c.get("uncertainty_type") or _c.get("action"):
                continue
            if _c.get("verdict") == "UNKNOWN":
                _c["uncertainty_type"] = "MISSING"
                _c["action"] = action_for("MISSING")
            elif _c.get("verdict") == "UNCERTAIN":
                _c["uncertainty_type"] = None
                _c["action"] = action_for(None)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        qs = parse_qs(urlparse(self.path).query)
        patient_id = (qs.get("patient_id") or [""])[0].strip()
        trace = TRACES_BY_ID.get(patient_id)
        if not trace:
            result = {"error": "unknown patient_id"}
        else:
            result = trace
        body = json.dumps(result, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
