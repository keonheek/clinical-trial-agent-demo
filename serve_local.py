#!/usr/bin/env python3
"""Run the judge-facing board locally on the Claude subscription instead of the metered key.

Mounts the same Vercel handlers the production site uses (api/patients, api/trace, api/answer,
api/live) under one stdlib server and serves board.html + static files from this directory, so
what you test here is byte-for-byte the production code path with only the LLM backend swapped:

    python3 serve_local.py                 # http://127.0.0.1:8930  (subscription, claude -p)
    LLM_BACKEND=anthropic python3 serve_local.py   # same server on the metered key (not default)

Headless `claude -p` is slower per call than the API (a fresh CLI process each time) but spends
nothing from ANTHROPIC_AI_HEALTHCARE_API_KEY. The rate limits that protect the metered key are
lifted here. No window is opened; paste the URL into your own browser.
"""
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
sys.path.insert(0, HERE)
os.environ.setdefault("LLM_BACKEND", "claude")
os.environ.setdefault("CLAUDE_PIPELINE_MODEL", "claude-sonnet-5")
os.environ.setdefault("LIVE_RATE_LIMIT", "1000")
for _k in ("CLAUDECODE", "CLAUDE_CODE_CHILD_SESSION"):  # let claude -p start from inside a session
    os.environ.pop(_k, None)

from api import patients as _patients, trace as _trace, answer as _answer, live as _live, export as _export  # noqa: E402

_answer.RATE_LIMIT_PER_MIN = 1000
_answer.FOLLOWUP_RATE_LIMIT_PER_MIN = 1000

ROUTES = {
    "/api/patients": _patients.handler,
    "/api/trace": _trace.handler,
    "/api/answer": _answer.handler,
    "/api/live": _live.handler,
    "/api/export": _export.handler,
}
MIME = {".html": "text/html; charset=utf-8", ".js": "application/javascript", ".json": "application/json",
        ".css": "text/css", ".png": "image/png", ".svg": "image/svg+xml", ".pdf": "application/pdf"}
PORT = int(os.environ.get("PORT", "8930"))


class Dispatch(BaseHTTPRequestHandler):
    def _route(self):
        return ROUTES.get(self.path.split("?", 1)[0])

    def do_GET(self):
        h = self._route()
        if h is not None and hasattr(h, "do_GET"):
            return h.do_GET(self)  # the Vercel handler's method, run on this request
        p = self.path.split("?", 1)[0]
        p = "/board.html" if p in ("", "/") else p
        f = os.path.normpath(os.path.join(HERE, p.lstrip("/")))
        if not f.startswith(HERE) or not os.path.isfile(f):
            self.send_response(404); self.end_headers(); return
        data = open(f, "rb").read()
        self.send_response(200)
        self.send_header("Content-Type", MIME.get(os.path.splitext(f)[1], "application/octet-stream"))
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        h = self._route()
        if h is not None and hasattr(h, "do_POST"):
            return h.do_POST(self)
        self.send_response(404); self.end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.command, fmt % args))


if __name__ == "__main__":
    print(f"board on http://127.0.0.1:{PORT}  backend={os.environ['LLM_BACKEND']} "
          f"model={os.environ.get('CLAUDE_PIPELINE_MODEL')}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), Dispatch).serve_forever()
