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
