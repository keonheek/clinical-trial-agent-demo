#!/usr/bin/env python3
"""
anthropic_client.py — drop-in replacement for groq_client, routed through the Anthropic API.

Why this exists: the Groq free tier's daily quota is exhausted after one full pipeline run,
at which point it returns 429 with 900-second backoffs and a 10-patient run takes hours.
claude_client.py (headless `claude -p`) avoids that but spends the interactive subscription's
rate limit, which degrades the session it is run from. This client spends a metered API key
instead, so a re-run costs a known number of cents and touches nothing else.

Same interface and same on-disk cache scheme as groq_client (keyed on role/model/prompts), so
re-runs are free and existing Groq cache entries stay valid under their own model key.

Model routing (the same split the competition proposal argues for):
  matcher, reeval-matcher  -> reasoning is the accuracy-critical step, so thinking stays on
  everything else          -> structured extraction, thinking off, cheaper and faster

Cost is tracked per call and printed by stats(), because the budget is small and a silent
overrun is worse than a slow run.

Requires ANTHROPIC_API_KEY (repo-root .env or the environment). Standard library only.
"""
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.request

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"

DEFAULT_MODEL = os.environ.get("CLAUDE_PIPELINE_MODEL", "claude-sonnet-5")

# Roles where clinical reasoning quality decides the score. Everything else is extraction.
THINKING_ROLES = {"matcher", "reeval-matcher"}

# USD per million tokens. Sonnet 5 is on introductory pricing through 2026-08-31, which covers
# the whole competition; it reverts to 3/15 on 2026-09-01.
PRICING = {
    "claude-sonnet-5": (2.00, 10.00),
    "claude-haiku-4-5": (1.00, 5.00),
    "claude-opus-4-8": (5.00, 25.00),
}

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")

_stats = {"api_calls": 0, "cache_hits": 0, "in_tokens": 0, "out_tokens": 0, "usd": 0.0}

_FENCE_RE = re.compile(r"```(?:json)?\s*|```", re.IGNORECASE)


# ANTHROPIC_NEW_KEY first: the original ANTHROPIC_API_KEY authenticates but carries a zero
# credit balance, so every call it makes dies with "credit balance is too low" AFTER passing
# auth -- which looks like a working key right up until the request fails. Prefer the funded one.
KEY_NAMES = ("ANTHROPIC_NEW_KEY", "ANTHROPIC_API_KEY")


def _get_api_key():
    for name in KEY_NAMES:
        key = os.environ.get(name)
        if key:
            return key
    here = os.path.dirname(os.path.abspath(__file__))
    for candidate in (
        os.path.join(here, "..", "..", ".env.local"),
        os.path.join(here, "..", "..", ".env"),
    ):
        path = os.path.abspath(candidate)
        if not os.path.exists(path):
            continue
        env = {}
        with open(path) as f:
            for line in f:
                line = line.strip()
                for name in KEY_NAMES:
                    if line.startswith(name + "="):
                        env[name] = line.split("=", 1)[1].strip().strip('"').strip("'")
        for name in KEY_NAMES:
            if env.get(name):
                return env[name]
    raise RuntimeError(
        f"no Anthropic key found. Set one of {KEY_NAMES} in the environment or repo-root .env")


def _cache_key(role, model, system_prompt, user_prompt):
    h = hashlib.sha256()
    for part in (role, model, system_prompt, user_prompt):
        h.update(part.encode("utf-8"))
        h.update(b"\x00")
    return h.hexdigest()


def _cache_path(key):
    return os.path.join(CACHE_DIR, key + ".json")


def _extract_json(text):
    """Prompts demand a bare JSON object. Models sometimes add a fence, or a sentence of
    commentary after the object. Take the FIRST complete object and ignore the rest.

    Naively slicing from the first '{' to the LAST '}' is wrong: if the model emits an object
    followed by any other braced text, the slice spans both and json.loads dies on "Extra data".
    raw_decode stops cleanly at the end of the first value.
    """
    text = _FENCE_RE.sub("", text).strip()
    start = text.find("{")
    if start == -1:
        raise ValueError(f"no JSON object in model output: {text[:120]!r}")
    obj, _end = json.JSONDecoder().raw_decode(text[start:])
    return obj


def call_llm(role, system_prompt, user_prompt, model=DEFAULT_MODEL, json_mode=True,
             max_retries=5):
    """Returns the parsed JSON object. Signature matches groq_client.call_groq."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    key = _cache_key(role, model, system_prompt, user_prompt)
    path = _cache_path(key)
    if os.path.exists(path):
        with open(path) as f:
            _stats["cache_hits"] += 1
            return json.load(f)

    body = {
        "model": model,
        "max_tokens": 8000,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_prompt}],
        "output_config": {"effort": "medium" if role in THINKING_ROLES else "low"},
    }
    if role not in THINKING_ROLES:
        # Structured extraction does not benefit from deliberation; skip it and pay less.
        body["thinking"] = {"type": "disabled"}

    data = json.dumps(body).encode("utf-8")
    headers = {
        "content-type": "application/json",
        "x-api-key": _get_api_key(),
        "anthropic-version": API_VERSION,
    }

    delay = 2.0
    last_err = None
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(API_URL, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=180) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:200]
            last_err = f"HTTP {e.code}: {detail}"
            if e.code in (429, 500, 502, 503, 529) and attempt < max_retries - 1:
                print(f"    [anthropic] {role}: HTTP {e.code}, retrying in {delay:.0f}s "
                      f"(attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError(f"anthropic call failed for {role}: {last_err}") from e
        except (urllib.error.URLError, TimeoutError) as e:
            last_err = str(e)
            if attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError(f"anthropic call failed for {role}: {last_err}") from e
    else:
        raise RuntimeError(f"anthropic call failed for {role}: {last_err}")

    usage = payload.get("usage", {})
    in_tok = usage.get("input_tokens", 0)
    out_tok = usage.get("output_tokens", 0)
    price_in, price_out = PRICING.get(model, (0.0, 0.0))
    _stats["api_calls"] += 1
    _stats["in_tokens"] += in_tok
    _stats["out_tokens"] += out_tok
    _stats["usd"] += (in_tok * price_in + out_tok * price_out) / 1_000_000

    # A safety classifier can decline with HTTP 200; content is then empty. Fail loudly rather
    # than caching an empty object as if it were a real verdict.
    if payload.get("stop_reason") == "refusal":
        raise RuntimeError(f"anthropic refused the {role} request: {payload.get('stop_details')}")

    text = "".join(
        block.get("text", "") for block in payload.get("content", [])
        if block.get("type") == "text"
    ).strip()
    if not text:
        raise RuntimeError(f"anthropic returned no text for {role} "
                           f"(stop_reason={payload.get('stop_reason')})")

    result = _extract_json(text) if json_mode else {"text": text}

    with open(path, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return result


def stats():
    return dict(_stats)
