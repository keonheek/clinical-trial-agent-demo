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
import threading
import time
import urllib.error
import urllib.request

API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"

# Default switched Sonnet 5 -> Opus 5 2026-08-30 (Keonhee's go) for the final submission.
# History: Haiku -> Sonnet 2026-08-19 after the 3-model bake-off on the 51 blind stress labels
# (Sonnet 76.5% vs Haiku 72.6%). Override with CLAUDE_PIPELINE_MODEL or the UI picker
# (Haiku 4.5 / Sonnet 5 / Opus 5 / Fable 5 -- see live_server.MODEL_CHOICES).
DEFAULT_MODEL = os.environ.get("CLAUDE_PIPELINE_MODEL", "claude-opus-5")

# Roles where clinical reasoning quality decides the score. Everything else is extraction.
THINKING_ROLES = {"matcher", "reeval-matcher"}


def _supports_effort(model):
    """output_config.effort and the thinking toggle are frontier-model features. Haiku 4.5
    returns HTTP 400 ("does not support the effort parameter") if either is sent."""
    return not model.startswith("claude-haiku")


def _thinking_always_on(model):
    """Fable 5 and Opus 5 run adaptive thinking by default. Fable rejects
    thinking={"type":"disabled"} with HTTP 400, so it is never sent for these; effort alone
    controls spend there."""
    return model.startswith("claude-fable") or model.startswith("claude-opus-5")


def _price_for(model):
    """Model ids carry a date suffix (claude-haiku-4-5-20251001) but PRICING is keyed on the
    family. Prefix-match, so a dated id never silently costs $0.00 in the running total."""
    for family, price in PRICING.items():
        if model.startswith(family):
            return price
    raise RuntimeError(
        f"No price known for model {model!r}. Add it to PRICING before spending money on it."
    )

# USD per million tokens. Sonnet 5 is on introductory pricing through 2026-08-31, which covers
# the whole competition; it reverts to 3/15 on 2026-09-01.
PRICING = {
    "claude-fable-5": (10.00, 50.00),
    "claude-opus-5": (5.00, 25.00),
    "claude-sonnet-5": (2.00, 10.00),
    "claude-haiku-4-5": (1.00, 5.00),
    "claude-opus-4-8": (5.00, 25.00),
}

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")

_stats = {"api_calls": 0, "cache_hits": 0, "in_tokens": 0, "out_tokens": 0, "usd": 0.0}
# api/answer.py and live_server.py now fire calls from a ThreadPoolExecutor (latency work,
# 2026-08-20) -- plain `_stats[k] += 1` is not atomic across threads under free-threaded
# Python (and is a correctness smell even under the GIL), so every mutation goes through
# this lock. Cheap: it's only ever held for a few dict writes, never around network I/O.
_stats_lock = threading.Lock()

# Anthropic prompt caching (2026-08-20 latency work): mark the system prompt as a cacheable
# block so repeated calls with the SAME role (criteria-parser x4, matcher x4 in one live
# vignette build) can reuse it server-side instead of re-billing full input price. Basic
# `cache_control: {"type": "ephemeral"}` is GA -- no beta header -- verified against the
# claude-api skill's cached docs (2026-06-24), not memory.
#
# IMPORTANT CAVEAT, verified not assumed: Anthropic's documented minimum cacheable prefix is
# ~1024 tokens; every system prompt in this file's caller (pipeline.py) measures 170-434
# tokens (CRITERIA_PARSER_SYS ~216, MATCHER_SYS ~394, QUESTION_GENERATOR_SYS ~434, ...) --
# all comfortably under the floor. A prefix under the floor silently does not cache (no
# error, cache_read_input_tokens stays 0); it is not a win at today's prompt sizes. The flag
# exists so the wiring is correct and ready the day a system prompt crosses ~1024 tokens
# (e.g. MATCHER_SYS growing with more few-shot examples), and so it can be measured directly
# via stats()/response usage rather than assumed. Default ON per spec; set
# ANTHROPIC_PROMPT_CACHE=0 to disable.
PROMPT_CACHE_ENABLED = os.environ.get("ANTHROPIC_PROMPT_CACHE", "1") != "0"

_FENCE_RE = re.compile(r"```(?:json)?\s*|```", re.IGNORECASE)


# ANTHROPIC_NEW_KEY first: the original ANTHROPIC_API_KEY authenticates but carries a zero
# credit balance, so every call it makes dies with "credit balance is too low" AFTER passing
# auth -- which looks like a working key right up until the request fails. Prefer the funded one.
# The challenge's own funded key comes first (2026-08-20, his instruction): this project bills
# to ANTHROPIC_AI_HEALTHCARE_API_KEY, not the general account keys. The others stay as fallbacks
# so a local run still works if the project key is not in the environment.
KEY_NAMES = ("ANTHROPIC_AI_HEALTHCARE_API_KEY", "ANTHROPIC_NEW_KEY", "ANTHROPIC_API_KEY")


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


def _system_field(system_prompt, use_cache):
    """Plain string (unchanged wire shape) when caching is off; a one-block content list with
    cache_control when on. See PROMPT_CACHE_ENABLED's comment for the caveat: below the ~1024
    token floor this silently does not cache -- it does not error, it just does nothing."""
    if not use_cache:
        return system_prompt
    return [{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}]


def call_llm(role, system_prompt, user_prompt, model=DEFAULT_MODEL, json_mode=True,
             max_retries=5, use_cache=None):
    """Returns the parsed JSON object. Signature matches groq_client.call_groq.
    use_cache=None defers to the module-level PROMPT_CACHE_ENABLED flag; pass True/False to
    override per call (tests do this to exercise both wire shapes without touching env)."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    key = _cache_key(role, model, system_prompt, user_prompt)
    path = _cache_path(key)
    if os.path.exists(path):
        with open(path) as f:
            with _stats_lock:
                _stats["cache_hits"] += 1
            return json.load(f)

    use_cache = PROMPT_CACHE_ENABLED if use_cache is None else use_cache
    headers = {
        "content-type": "application/json",
        "x-api-key": _get_api_key(),
        "anthropic-version": API_VERSION,
    }
    # Connection reuse was evaluated and declined: urllib.request.HTTPHandler opens a fresh
    # connection per urlopen() call regardless of whether the caller reuses a build_opener()
    # instance -- reusing an opener does NOT pool TCP/TLS state, so it would be a no-op
    # dressed up as an optimization. Real pooling needs a hand-held http.client.HTTPSConnection,
    # which is not thread-safe and would need threading.local() now that calls run from a
    # ThreadPoolExecutor -- real complexity for one TLS handshake (~50-150ms) against calls
    # that run multi-second. Not worth it; left as one urlopen() per call, as before.

    delay = 2.0
    last_err = None
    result = None
    for attempt in range(max_retries):
        body = {
            "model": model,
            "max_tokens": 8000,
            "system": _system_field(system_prompt, use_cache),
            "messages": [{"role": "user", "content": user_prompt}],
        }
        # output_config.effort and the thinking toggle are only accepted by the frontier models
        # (Sonnet 5, Opus 4.6+). Haiku 4.5 rejects both with HTTP 400, so gate on capability
        # rather than sending them unconditionally.
        if _supports_effort(model):
            body["output_config"] = {"effort": "medium" if role in THINKING_ROLES else "low"}
            if role not in THINKING_ROLES and not _thinking_always_on(model):
                # Structured extraction does not benefit from deliberation; skip it and pay less.
                # Not sent on Fable 5 / Opus 5: Fable returns 400 for it, and Opus 5 with
                # thinking disabled can leak tool-call text -- low effort covers both there.
                body["thinking"] = {"type": "disabled"}
        data = json.dumps(body).encode("utf-8")

        try:
            req = urllib.request.Request(API_URL, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=180) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:200]
            last_err = f"HTTP {e.code}: {detail}"
            # Graceful fallback (spec step 3): if some deployment/model combo ever rejects
            # cache_control, drop it and retry immediately -- never let a caching experiment
            # break a call that would otherwise succeed. Consumes one retry slot, same as any
            # other retry; cheap since it costs no sleep.
            if e.code == 400 and use_cache and "cache_control" in detail.lower():
                use_cache = False
                print(f"    [anthropic] {role}: cache_control rejected (HTTP 400), "
                      f"retrying without it")
                continue
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

        # Account tokens per real API call (a retried attempt genuinely spent tokens too).
        usage = payload.get("usage", {})
        in_tok = usage.get("input_tokens", 0)
        out_tok = usage.get("output_tokens", 0)
        price_in, price_out = _price_for(model)
        with _stats_lock:
            _stats["api_calls"] += 1
            _stats["in_tokens"] += in_tok
            _stats["out_tokens"] += out_tok
            _stats["usd"] += (in_tok * price_in + out_tok * price_out) / 1_000_000

        # A safety classifier can decline with HTTP 200; content is then empty. A refusal is
        # deterministic -- retrying just burns tokens on the same decline -- so fail loudly now.
        if payload.get("stop_reason") == "refusal":
            raise RuntimeError(f"anthropic refused the {role} request: {payload.get('stop_details')}")

        text = "".join(
            block.get("text", "") for block in payload.get("content", [])
            if block.get("type") == "text"
        ).strip()

        # Empty text and malformed JSON are STOCHASTIC (a truncated or fenced generation),
        # unlike a refusal -- a re-roll usually succeeds, so treat both as retryable instead
        # of aborting a whole batch on one bad generation.
        try:
            if not text:
                raise ValueError(f"empty text (stop_reason={payload.get('stop_reason')})")
            result = _extract_json(text) if json_mode else {"text": text}
            break
        except (ValueError, json.JSONDecodeError) as e:
            last_err = f"unparseable output: {e}"
            if attempt < max_retries - 1:
                print(f"    [anthropic] {role}: {last_err}, retrying in {delay:.0f}s "
                      f"(attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
                delay *= 2
                continue
            raise RuntimeError(f"anthropic call failed for {role}: {last_err}") from e
    else:
        raise RuntimeError(f"anthropic call failed for {role}: {last_err}")

    # Write-then-rename, not write-in-place: a truncated write (process killed, or two
    # threads racing the same cache key mid-write under the ThreadPoolExecutor callers added
    # 2026-08-20) must never leave a partial file that a later json.load() on this path
    # explodes on. os.replace is atomic on the same filesystem, so any reader always sees
    # either the old (absent) or the new (complete) file, never a half-written one. The
    # per-thread suffix means two threads computing the SAME key concurrently write to two
    # different temp names and the second os.replace just overwrites with identical content.
    tmp_path = f"{path}.tmp.{os.getpid()}.{threading.get_ident()}"
    with open(tmp_path, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)
    return result


def stats():
    with _stats_lock:  # same discipline as the writers (thread-pool callers since 08-20)
        return dict(_stats)
