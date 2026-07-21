"""GET /api/trace?patient_id=S001 -> the full precomputed trace for that patient.

Reads traces.json only. Zero LLM calls, instant.
"""
import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

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
