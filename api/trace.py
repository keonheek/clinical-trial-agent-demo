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

# action_policy and ranking are pure modules (no LLM client imports) -- safe to bundle serverless.
from action_policy import action_for, apply_trial_level_actions, enrich_questions
import ranking

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

# Trial-intent enrichment (therapeutic/supportive/care_delivery/observational), same sidecar
# pattern: build_trial_intent.py classifies every trial in trials_raw.json + trials_stress.json
# from its own raw fields (title/phase/conditions/eligibility text) into trial_intent.json
# ({nct_id: {intent, confidence, signals}}), because the frozen trace's trial entries carry
# only nct_id/title/phase/eligibility/rank/rationale -- not enough to classify from directly.
try:
    with open(os.path.join(ROOT, "trial_intent.json"), encoding="utf-8") as f:
        _TRIAL_INTENT = json.load(f)
    for _trace in TRACES:
        for _t in _trace.get("trials", []):
            intent = _TRIAL_INTENT.get(_t["nct_id"])
            if intent:
                _t["trial_intent"] = {"intent": intent["intent"], "confidence": intent["confidence"]}
except FileNotFoundError:
    pass  # trial_intent is an enrichment, never a reason for the trace endpoint to fail

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
    # Trial-level context: once a trial is INELIGIBLE (hard FAIL), its remaining undecided
    # criteria are STOP, not ASK -- asking is moot. Deterministic (action_policy), no model.
    apply_trial_level_actions(_trace.get("trials", []))

# Recommendation priority (추천 우선순위), 2026-08-16. The rank frozen into traces.json was
# eligibility-class + raw unresolved count only. The organizer's stated standard weighs 임상적
# 적합성 too (Phase, 중재 목적, 환자 부담), so the served order is re-derived IN MEMORY by
# ranking.rank_trials -- eligibility class first (a hard FAIL is never out-ranked), then blocking
# count, 중재 목적, Phase 부담, coverage penalty, unresolved ratio. Same function the answer round
# (api/answer.py -> pipeline.recommend) uses, so the order cannot flip back after the first
# answer. traces.json on disk is untouched (md5 pin; blind-label pairing). Each trial carries
# rank_reason / rank_basis so the UI can state the executed basis, and the trace carries the
# rule text + a snapshot of the frozen order for transparency.
for _trace in TRACES:
    _trials = _trace.get("trials", [])
    _trace["frozen_rank_order"] = [t["nct_id"] for t in sorted(_trials, key=lambda t: t.get("rank", 99))]
    ranking.rank_trials(_trials, trust_attached=False)
    _trace["ranking"] = {"version": ranking.RANKING_VERSION, "rule_ko": ranking.RANKING_RULE_KO,
                         "hard_exclusion_holds": ranking.hard_exclusion_holds(_trials)}
    # Question priority (affects_trials / affects_criteria / may_change_rank): pure arithmetic
    # over the trace (action_policy.enrich_questions); frozen traces carry no gap links, so it
    # uses the token-overlap fallback. Also orders the questions most-impactful first.
    _trace["questions"] = enrich_questions(_trace.get("questions", []), _trace.get("gaps", []), _trials)


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
