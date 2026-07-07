#!/usr/bin/env python3
"""
groq_client.py — thin wrapper around the Groq (OpenAI-compatible) chat completions API.

- Free tier ONLY (GROQ_API_KEY). NEVER calls the paid Anthropic API.
- On-disk caching keyed on (role, model, system_prompt, user_prompt): re-running the
  pipeline after the first successful build costs $0 in LLM calls.
- Exponential backoff on 429 / 5xx / transient errors, and on malformed JSON responses.
"""
import hashlib
import json
import os
import time
import urllib.request
import urllib.error

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_MODEL = "llama-3.3-70b-versatile"
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")

_stats = {"api_calls": 0, "cache_hits": 0}


def _get_api_key():
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key.strip().strip('"').strip("'")
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    for fname in (".env.local", ".env"):
        path = os.path.join(repo_root, fname)
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GROQ_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
    raise RuntimeError("GROQ_API_KEY not found in environment or .env/.env.local")


def _cache_key(role, model, system_prompt, user_prompt):
    h = hashlib.sha256()
    for part in (role, model, system_prompt, user_prompt):
        h.update(part.encode("utf-8"))
    return h.hexdigest()


def call_groq(role, system_prompt, user_prompt, model=DEFAULT_MODEL, json_mode=True,
              temperature=0.1, max_retries=5, use_cache=True):
    """Call Groq chat completions for agent `role`. Returns parsed dict (json_mode=True)
    or raw string. Cached to disk so identical calls are free on re-run."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    key = _cache_key(role, model, system_prompt, user_prompt)
    cache_path = os.path.join(CACHE_DIR, f"{key}.json")

    if use_cache and os.path.exists(cache_path):
        _stats["cache_hits"] += 1
        with open(cache_path) as f:
            cached = json.load(f)
        return cached["parsed"] if json_mode else cached["raw"]

    api_key = _get_api_key()
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": temperature,
    }
    if json_mode:
        body["response_format"] = {"type": "json_object"}

    payload = json.dumps(body).encode("utf-8")
    backoff = 2.0
    last_err = None

    for attempt in range(max_retries):
        req = urllib.request.Request(
            GROQ_URL,
            data=payload,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "sdic-trial-demo/1.0 (python-urllib)",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.load(resp)
            raw = data["choices"][0]["message"]["content"]
            _stats["api_calls"] += 1
            parsed = None
            if json_mode:
                try:
                    parsed = json.loads(raw)
                except json.JSONDecodeError as je:
                    last_err = je
                    print(f"  [groq] {role}: malformed JSON (attempt {attempt+1}/{max_retries}), retrying in {backoff}s")
                    time.sleep(backoff)
                    backoff *= 2
                    continue
            with open(cache_path, "w") as f:
                json.dump({"role": role, "raw": raw, "parsed": parsed}, f, indent=2, ensure_ascii=False)
            return parsed if json_mode else raw
        except urllib.error.HTTPError as e:
            last_err = e
            body_txt = e.read().decode(errors="ignore")
            if e.code == 429 or e.code >= 500:
                retry_after = e.headers.get("Retry-After")
                wait = float(retry_after) if retry_after else backoff
                print(f"  [groq] {role}: HTTP {e.code}, retrying in {wait}s (attempt {attempt+1}/{max_retries})")
                time.sleep(wait)
                backoff *= 2
                continue
            raise RuntimeError(f"Groq API error {e.code} for role={role}: {body_txt}") from e
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = e
            print(f"  [groq] {role}: {e}, retrying in {backoff}s (attempt {attempt+1}/{max_retries})")
            time.sleep(backoff)
            backoff *= 2

    raise RuntimeError(f"Groq call failed after {max_retries} attempts for role={role}: {last_err}")


def stats():
    return dict(_stats)


if __name__ == "__main__":
    # smoke test
    out = call_groq(
        "smoke-test",
        "You output strict JSON only, no markdown fences.",
        'Return {"ok": true, "model_check": "respond with the literal string ok"}',
    )
    print("Smoke test result:", out)
    print("Stats:", stats())
