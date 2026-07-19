#!/usr/bin/env python3
"""
ollama_client.py — local inference via Ollama. $0, no API key, nothing leaves the machine.

Same interface as groq_client / anthropic_client so pipeline.py can swap backends with
LLM_BACKEND=ollama.

- Default model qwen3.6:35b (MoE, ~79 tok/s on the M5 Pro, fluent Korean).
- think=False: qwen3.6 defaults to thinking-mode ON, which is slow and pollutes JSON output.
- On-disk cache keyed on (role, model, system_prompt, user_prompt), shared with the other
  clients. The model is part of the key, so switching backends never serves a stale answer.
- No API key, no rate limits, no daily quota. Retries only cover a cold/paging model.
"""
import hashlib
import json
import os
import time
import urllib.request
import urllib.error

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434") + "/api/chat"
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3.6:35b")
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")

# First call on a cold model pays the load cost (23 GB read from disk into unified memory).
# Generation itself is fast; it is the load that is slow, so the timeout has to absorb it.
TIMEOUT = float(os.environ.get("OLLAMA_TIMEOUT", "600"))

_stats = {"api_calls": 0, "cache_hits": 0}


def _cache_key(role, model, system_prompt, user_prompt):
    h = hashlib.sha256()
    for part in (role, model, system_prompt, user_prompt):
        h.update(part.encode("utf-8"))
    return h.hexdigest()


def call_llm(role, system_prompt, user_prompt, model=DEFAULT_MODEL, json_mode=True,
             temperature=0.1, max_retries=3, use_cache=True):
    """Call the local Ollama server for agent `role`. Returns parsed dict (json_mode=True)
    or the raw string. Cached to disk so re-runs are instant."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    key = _cache_key(role, model, system_prompt, user_prompt)
    cache_path = os.path.join(CACHE_DIR, f"{key}.json")

    if use_cache and os.path.exists(cache_path):
        _stats["cache_hits"] += 1
        with open(cache_path) as f:
            cached = json.load(f)
        return cached["parsed"] if json_mode else cached["raw"]

    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "stream": False,
        "think": False,
        "options": {"temperature": temperature},
    }
    if json_mode:
        body["format"] = "json"

    payload = json.dumps(body).encode("utf-8")
    backoff = 2.0
    last_err = None

    for attempt in range(max_retries):
        req = urllib.request.Request(
            OLLAMA_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                data = json.load(resp)
            raw = data["message"]["content"]
            _stats["api_calls"] += 1
            parsed = None
            if json_mode:
                try:
                    parsed = json.loads(raw)
                except json.JSONDecodeError as je:
                    last_err = je
                    print(f"  [ollama] {role}: malformed JSON (attempt {attempt+1}/{max_retries}), "
                          f"retrying in {backoff}s", flush=True)
                    time.sleep(backoff)
                    backoff *= 2
                    continue
            with open(cache_path, "w") as f:
                json.dump({"role": role, "raw": raw, "parsed": parsed}, f, indent=2, ensure_ascii=False)
            return parsed if json_mode else raw
        except urllib.error.HTTPError as e:
            body_txt = e.read().decode(errors="ignore")
            raise RuntimeError(f"Ollama error {e.code} for role={role}: {body_txt}") from e
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = e
            print(f"  [ollama] {role}: {e}, retrying in {backoff}s "
                  f"(attempt {attempt+1}/{max_retries}). Is the server up? "
                  f"Start it with: open -a Ollama", flush=True)
            time.sleep(backoff)
            backoff *= 2

    raise RuntimeError(f"Ollama call failed after {max_retries} attempts for role={role}: {last_err}")


def stats():
    return dict(_stats)


if __name__ == "__main__":
    out = call_llm(
        "smoke-test",
        "You output strict JSON only, no markdown fences.",
        'Return {"ok": true, "model_check": "respond with the literal string ok"}',
        use_cache=False,
    )
    print("Smoke test result:", out)
    print("Model:", DEFAULT_MODEL)
    print("Stats:", stats())
