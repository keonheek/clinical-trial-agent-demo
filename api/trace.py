"""GET /api/trace?patient_id=S001 -> the full precomputed trace for that patient.

Reads traces.json only. Zero LLM calls, instant.
"""
import hashlib
import json
import os
import sys
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# action_policy, ranking, patient_need are pure modules (no LLM client imports) -- safe to
# bundle serverless.
from action_policy import action_for, apply_trial_level_actions, enrich_questions, criterion_id
from patient_need import classify_patient_need
import ranking

with open(os.path.join(ROOT, "traces.json"), encoding="utf-8") as f:
    TRACES = json.load(f)

# Extra demo patients (E001-...): generated separately (gen_extra.py) so the canonical
# traces.json stays byte-frozen (md5 pin, blind-label pairing). Same shape, merged at load;
# every enrichment below applies to them identically.
try:
    with open(os.path.join(ROOT, "traces_extra.json"), encoding="utf-8") as f:
        TRACES.extend(json.load(f))
except FileNotFoundError:
    pass
TRACES_BY_ID = {t["patient_id"]: t for t in TRACES}

# Serve-time coverage enrichment: traces.json is a frozen artifact (regenerating it silently
# unpairs the blind eval labels), so parsing coverage is attached here, in memory. The map
# {nct_id -> criterion-like clauses in the raw protocol} is precomputed by
# pipeline.estimate_raw_criteria_count over trials_raw.json (see repo root coverage_map.json)
# so this endpoint stays dependency-free and instant.
try:
    with open(os.path.join(ROOT, "coverage_map.json"), encoding="utf-8") as f:
        _RAW_COUNT = json.load(f)
    try:
        with open(os.path.join(ROOT, "coverage_map_extra.json"), encoding="utf-8") as f:
            for _k, _v in json.load(f).items():
                _RAW_COUNT.setdefault(_k, _v)
    except FileNotFoundError:
        pass
    for _trace in TRACES:
        for _t in _trace.get("trials", []):
            raw_n = _RAW_COUNT.get(_t["nct_id"])
            if raw_n:
                _t["coverage"] = {"parsed": len(_t.get("criteria", [])), "raw_estimated": raw_n}
except FileNotFoundError:
    pass  # coverage is an enrichment, never a reason for the trace endpoint to fail

# Patient-facing design facts (what a joiner receives + what is measured), fetched by
# gen_design.py from ClinicalTrials.gov v2 -- same sidecar pattern, never touches trials_raw.
try:
    with open(os.path.join(ROOT, "trial_design.json"), encoding="utf-8") as f:
        _TRIAL_DESIGN = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    _TRIAL_DESIGN = {}

# Trial-intent enrichment (therapeutic/supportive/care_delivery/observational), same sidecar
# pattern: build_trial_intent.py classifies every trial in trials_raw.json + trials_stress.json
# from its own raw fields (title/phase/conditions/eligibility text) into trial_intent.json
# ({nct_id: {intent, confidence, signals}}), because the frozen trace's trial entries carry
# only nct_id/title/phase/eligibility/rank/rationale -- not enough to classify from directly.
try:
    with open(os.path.join(ROOT, "trial_intent.json"), encoding="utf-8") as f:
        _TRIAL_INTENT = json.load(f)
    try:
        with open(os.path.join(ROOT, "trial_intent_extra.json"), encoding="utf-8") as f:
            for _k, _v in json.load(f).items():
                _TRIAL_INTENT.setdefault(_k, _v)
    except FileNotFoundError:
        pass
    for _trace in TRACES:
        for _t in _trace.get("trials", []):
            intent = _TRIAL_INTENT.get(_t["nct_id"])
            if intent:
                _t["trial_intent"] = {"intent": intent["intent"], "confidence": intent["confidence"]}
                _d = _TRIAL_DESIGN.get(_t["nct_id"])

                if _d:

                    _t["design"] = _d
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

# Regenerated question sets (gen_questions_v2.py): Korean question text, Korean self-contained
# options and per-option direction from the current question generator. Replaces the frozen
# trace's questions (and supplies gaps for the priority numbers) without touching traces.json.
try:
    with open(os.path.join(ROOT, "questions_v2.json"), encoding="utf-8") as f:
        _Q_V2 = json.load(f)
    for _trace in TRACES:
        _v2 = _Q_V2.get(_trace.get("patient_id")) if isinstance(_Q_V2, dict) else None
        if _v2 and _v2.get("questions"):
            _trace["questions"] = _v2["questions"]
            if _v2.get("gaps") and not _trace.get("gaps"):
                _trace["gaps"] = _v2["gaps"]
except (FileNotFoundError, json.JSONDecodeError):
    pass

# Bilingual gloss sidecar (gen_gloss.py), same sidecar pattern as coverage/trial_intent above:
# {sha1(source.strip())[:12]: {"src", "ko"/"en"}}, built once by a separate offline script and
# never touched here. gen_gloss.py may still be mid-write (it writes the whole file on every
# batch) -- a missing file or a torn/partial JSON read must degrade to "no glosses", never crash
# the endpoint. json.JSONDecodeError is the concrete failure mode of reading a file mid-write.
try:
    with open(os.path.join(ROOT, "gloss.json"), encoding="utf-8") as f:
        _GLOSS = json.load(f)
    if not isinstance(_GLOSS, dict):
        _GLOSS = {}
except (FileNotFoundError, json.JSONDecodeError):
    _GLOSS = {}


def _gloss_key(text):
    # Mirrors gen_gloss.key_of exactly: sha1 of the UTF-8 bytes, first 12 hex chars.
    # selftest: _gloss_key("Age >= 18 years") == "b0367dda91e9" (verified against
    # gen_gloss.key_of("Age >= 18 years") at the Python prompt).
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def _trace_gloss_strings(tr):
    """Every distinct LLM-authored string THIS trace shows -- same field list as
    gen_gloss.collect_sources, scoped to one patient so the served payload stays small."""
    out = set()
    for f in tr.get("extraction", []) or []:
        v = f.get("value") or f.get("text") or ""
        if v:
            out.add(str(v))
    for t in tr.get("trials", []) or []:
        if t.get("title"):
            out.add(t["title"])
        if t.get("rationale"):
            out.add(t["rationale"])
        for c in t.get("criteria", []) or []:
            if c.get("text"):
                out.add(c["text"])
            if c.get("reasoning"):
                out.add(c["reasoning"])
    for q in tr.get("questions", []) or []:
        if q.get("question"):
            out.add(q["question"])
        if q.get("why"):
            out.add(q["why"])
        for o in q.get("options", []) or []:
            if o:
                out.add(o)
    return out


def build_trace_gloss(tr):
    """{sha1key: {"ko"/"en": text}} for exactly the strings this trace needs -- not the
    whole GLOSS store, so a patient with 40 criteria never ships another patient's glosses."""
    out = {}
    for s in _trace_gloss_strings(tr):
        s = s.strip()
        if not s or len(s) <= 1:
            continue
        entry = _GLOSS.get(_gloss_key(s))
        if not entry:
            continue
        g = {}
        if entry.get("ko"):
            g["ko"] = entry["ko"]
        if entry.get("en"):
            g["en"] = entry["en"]
        if g:
            out[_gloss_key(s)] = g
    return out


# Stable criterion_id (added for the question-criterion linking fix): sha1(nct_id + normalized
# text)[:10], attached here IN MEMORY only -- traces.json on disk never carries it. Lets a
# client-round-tripped criterion be matched back to the exact one served, independent of any
# text re-typing, once the UI starts using it instead of raw text for cross-checks.
for _trace in TRACES:
    for _t in _trace.get("trials", []):
        for _c in _t.get("criteria", []):
            _c["criterion_id"] = criterion_id(_t["nct_id"], _c.get("text", ""))

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

# Recommendation priority (추천 우선순위), 2026-08-18: the locked three-question tree. The rank
# frozen into traces.json was eligibility-class + raw unresolved count only; the served order is
# re-derived IN MEMORY by ranking.rank_trials -- gate (a hard FAIL is never out-ranked), help
# (the patient's need x the trial's intent, then Phase 부담), sure (적격 before 미확정, coverage,
# unresolved). The patient's need is classified here per trace from the vignette text
# (patient_need.classify_patient_need, deterministic keyword rules, zero LLM) and attached as
# trace["patient_need"] for the UI. Same function the answer round (api/answer.py ->
# pipeline.recommend) uses, so the order cannot flip back after the first answer. traces.json on
# disk is untouched (md5 pin; blind-label pairing). Each trial carries rank_reason / rank_basis
# so the UI can state the executed basis, and the trace carries the rule text + a snapshot of
# the frozen order for transparency.
for _trace in TRACES:
    _trials = _trace.get("trials", [])
    _trace["frozen_rank_order"] = [t["nct_id"] for t in sorted(_trials, key=lambda t: t.get("rank", 99))]
    _need = classify_patient_need(_trace.get("patient_text", ""))
    _trace["patient_need"] = _need
    ranking.rank_trials(_trials, trust_attached=False, patient_need=_need)
    _trace["ranking"] = {"version": ranking.RANKING_VERSION, "rule_ko": ranking.RANKING_RULE_KO,
                         "hard_exclusion_holds": ranking.hard_exclusion_holds(_trials)}
    # Question priority (affects_trials / affects_criteria / may_change_rank): pure arithmetic
    # over the trace (action_policy.enrich_questions); frozen traces carry no gap links, so it
    # uses the token-overlap fallback. Also orders the questions most-impactful first.
    _trace["questions"] = enrich_questions(_trace.get("questions", []), _trace.get("gaps", []), _trials)

# Gloss map, last: built after every field above has taken its final served shape (title,
# rationale, criteria text/reasoning, question text/why/options) so nothing enrichment-added
# is missed. Per-trace and small on purpose -- a family reading S001 never downloads glosses
# for the other nine patients.
for _trace in TRACES:
    _trace["gloss"] = build_trace_gloss(_trace)


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
