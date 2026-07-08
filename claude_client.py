#!/usr/bin/env python3
"""
claude_client.py — drop-in replacement for groq_client that routes pipeline LLM calls
through the local Claude Code CLI (`claude -p`, subscription auth).

- Why: Groq free-tier daily quota was costing ~7-10 min of 429 backoff per call
  (2026-07-08). The subscription has no such crawl.
- Same on-disk cache scheme as groq_client (keyed role/model/system/user), so re-runs
  are free and old Groq cache entries stay valid under their own model key.
- Bulk roles default to Haiku 4.5 (small structured-extraction jobs). Override with
  CLAUDE_PIPELINE_MODEL.
"""
import hashlib
import json
import os
import re
import subprocess
import time

DEFAULT_MODEL = os.environ.get("CLAUDE_PIPELINE_MODEL", "claude-haiku-4-5-20251001")
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")

_stats = {"api_calls": 0, "cache_hits": 0}

_FENCE_RE = re.compile(r"```(?:json)?\s*|```", re.IGNORECASE)


def _cache_key(role, model, system_prompt, user_prompt):
    h = hashlib.sha256()
    for part in (role, model, system_prompt, user_prompt):
        h.update(part.encode("utf-8"))
    return h.hexdigest()


def _strip_fences(raw):
    s = raw.strip()
    if s.startswith("```"):
        s = _FENCE_RE.sub("", s).strip()
    return s


def call_llm(role, system_prompt, user_prompt, model=DEFAULT_MODEL, json_mode=True,
             temperature=0.1, max_retries=4, use_cache=True):
    """Signature-compatible with groq_client.call_groq (temperature accepted, not
    forwarded — claude -p exposes no temperature flag). Returns parsed dict when
    json_mode=True, else raw string."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    key = _cache_key(role, model, system_prompt, user_prompt)
    cache_path = os.path.join(CACHE_DIR, f"{key}.json")

    if use_cache and os.path.exists(cache_path):
        _stats["cache_hits"] += 1
        with open(cache_path) as f:
            cached = json.load(f)
        return cached["parsed"] if json_mode else cached["raw"]

    # System prompt embedded in the input for CLI-version robustness.
    prompt = f"<system>\n{system_prompt}\n</system>\n\n{user_prompt}"
    if json_mode:
        prompt += "\n\nOutput STRICT JSON only — no markdown fences, no prose."

    backoff = 3.0
    last_err = None
    for attempt in range(max_retries):
        try:
            proc = subprocess.run(
                ["claude", "-p", "--model", model, "--output-format", "text",
                 "--strict-mcp-config", "--max-turns", "1"],
                input=prompt, capture_output=True, text=True, timeout=300,
            )
            raw = proc.stdout.strip()
            if proc.returncode != 0 or not raw:
                last_err = RuntimeError(
                    f"claude -p rc={proc.returncode} stderr={proc.stderr.strip()[:300]}")
                print(f"  [claude] {role}: {last_err}, retrying in {backoff}s "
                      f"(attempt {attempt+1}/{max_retries})", flush=True)
                time.sleep(backoff)
                backoff *= 2
                continue
            _stats["api_calls"] += 1
            parsed = None
            if json_mode:
                try:
                    parsed = json.loads(_strip_fences(raw))
                except json.JSONDecodeError as je:
                    last_err = je
                    print(f"  [claude] {role}: malformed JSON (attempt "
                          f"{attempt+1}/{max_retries}), retrying in {backoff}s", flush=True)
                    time.sleep(backoff)
                    backoff *= 2
                    continue
            with open(cache_path, "w") as f:
                json.dump({"role": role, "raw": raw, "parsed": parsed}, f,
                          indent=2, ensure_ascii=False)
            return parsed if json_mode else raw
        except subprocess.TimeoutExpired as e:
            last_err = e
            print(f"  [claude] {role}: timeout 300s (attempt {attempt+1}/{max_retries}), "
                  f"retrying in {backoff}s", flush=True)
            time.sleep(backoff)
            backoff *= 2

    raise RuntimeError(f"claude call failed after {max_retries} attempts for role={role}: {last_err}")


# Back-compat alias so callers can `from claude_client import call_groq` unchanged.
call_groq = call_llm


def stats():
    return dict(_stats)


if __name__ == "__main__":
    out = call_llm(
        "smoke-test",
        "You output strict JSON only, no markdown fences.",
        'Return {"ok": true, "backend": "claude-subscription"}',
        use_cache=False,
    )
    print("Smoke test result:", out)
    print("Stats:", stats())
