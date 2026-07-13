"""GET /api/patients -> [{id, condition}, ...] for the 10 official patients.

Reads patients.json only. Zero LLM calls.
"""
import json
import os
from http.server import BaseHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

with open(os.path.join(ROOT, "patients.json"), encoding="utf-8") as f:
    PATIENTS = json.load(f)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        out = [
            {"id": p["patient_id"], "condition": p.get("condition", p["patient_id"])}
            for p in PATIENTS
        ]
        body = json.dumps(out, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
