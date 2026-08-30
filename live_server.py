#!/usr/bin/env python3
"""
live_server.py -- stdlib-only HTTP server for the LIVE interactive re-eval loop.

A human types answers to the pipeline's clarifying questions; only the criteria
those answers actually affect get re-matched (real Groq calls), then the trial
ranking is recomputed. Two entry paths:
  - known patient (S001-S010): stages loaded instantly from traces.json (demo
    insurance), "precomputed": true.
  - pasted vignette: full pipeline run live (extract -> select candidate trials
    -> parse criteria -> match -> detect gaps -> generate questions).

Reuses pipeline.py's agent functions directly -- no logic duplicated here.
Python 3 stdlib only. Run: python3 live_server.py  (serves http://localhost:8765)
"""
import copy
import hashlib
import json
import os
import re
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pipeline
from pipeline import (
    extract_patient,
    parse_criteria,
    match_trial,
    detect_gaps,
    generate_questions,
    recommend,
    apply_recommendation,
    rematch_affected_criteria,
    effect_of,
    dedupe_followups,
    TRIALS_PER_PATIENT,
)
from action_policy import (
    enrich_questions,
    apply_trial_level_actions,
    trial_is_blocked,
    normalize_criterion_text,
    criterion_id,
)
from build_trial_intent import classify_trial_intent
from patient_need import classify_patient_need
import ranking

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = 8765

# ---------------------------------------------------------------------------
# static data loaded once at startup
# ---------------------------------------------------------------------------
with open(os.path.join(HERE, "patients.json")) as f:
    PATIENTS = json.load(f)
try:  # extra demo patients (gen_extra.py)
    with open(os.path.join(HERE, "patients_extra.json")) as f:
        PATIENTS = PATIENTS + json.load(f)
except FileNotFoundError:
    pass
PATIENTS_BY_ID = {p["patient_id"]: p for p in PATIENTS}

# The 40 stress-test patients (5 base cases x 7 single-defect variants, 지우's set) are
# offered here too -- selecting one runs it through the LIVE pipeline exactly like a pasted
# vignette. They carry no precomputed trace, so they always take the live path; the frozen
# S001-S010 demo traces are untouched. Local only: the deployed API never exposes these.
STRESS_PATIENTS_BY_ID = {}
try:
    with open(os.path.join(HERE, "patients_stress.json")) as f:
        for _p in json.load(f):
            STRESS_PATIENTS_BY_ID[_p["patient_id"]] = _p
except FileNotFoundError:
    pass

# What each variant is SUPPOSED to induce, read straight from the human answer key rather
# than asserted here -- the letters are not a clean 1:1 map (a/b/g carry a single cause,
# c/d/e/f mix several), so hardcoding a meaning per letter would misdescribe the data.
STRESS_EXPECTED_CAUSES = {}
try:
    with open(os.path.join(HERE, "eval_labels_stress.json")) as f:
        for _row in json.load(f):
            if _row.get("uncertainty_type"):
                STRESS_EXPECTED_CAUSES.setdefault(_row["patient_id"], set()).add(
                    _row["uncertainty_type"])
except FileNotFoundError:
    pass

with open(os.path.join(HERE, "traces.json")) as f:
    TRACES = json.load(f)
try:  # extra demo patients (gen_extra.py) -- same shape, merged; enrichments below apply to all
    with open(os.path.join(HERE, "traces_extra.json")) as f:
        TRACES.extend(json.load(f))
except (FileNotFoundError, json.JSONDecodeError):
    pass  # a gen_extra.py run may be mid-write; serve the canonical set rather than crash
TRACES_BY_ID = {t["patient_id"]: t for t in TRACES}

# Answer options for the frozen questions live in a sidecar (traces.json must not be
# regenerated -- the blind eval labels join on its criterion text). Attached in memory.
try:
    with open(os.path.join(HERE, "question_options.json"), encoding="utf-8") as f:
        _Q_OPTIONS = json.load(f)
    for _t in TRACES:
        for _q in _t.get("questions", []):
            if not _q.get("options") and _Q_OPTIONS.get(_q.get("question")):
                _q["options"] = _Q_OPTIONS[_q["question"]]
except FileNotFoundError:
    pass

# Patient-facing design facts (what a joiner receives + what is measured), fetched by
# gen_design.py from ClinicalTrials.gov v2 -- same sidecar pattern, never touches trials_raw.
try:
    with open(os.path.join(HERE, "trial_design.json"), encoding="utf-8") as f:
        _TRIAL_DESIGN = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    _TRIAL_DESIGN = {}

# Trial-intent enrichment for the frozen demo traces, same sidecar pattern (see build_trial_intent.py
# and api/trace.py's identical block): the trace's trial entries carry only nct_id/title/phase, not
# enough to classify from, so the precomputed {intent, confidence} comes from trial_intent.json.
try:
    with open(os.path.join(HERE, "trial_intent.json"), encoding="utf-8") as f:
        _TRIAL_INTENT = json.load(f)
    try:
        with open(os.path.join(HERE, "trial_intent_extra.json"), encoding="utf-8") as f:
            for _k, _v in json.load(f).items():
                _TRIAL_INTENT.setdefault(_k, _v)
    except FileNotFoundError:
        pass
    for _t in TRACES:
        for _tr in _t.get("trials", []):
            _intent = _TRIAL_INTENT.get(_tr["nct_id"])
            if _intent:
                _tr["trial_intent"] = {"intent": _intent["intent"], "confidence": _intent["confidence"]}
            _d = _TRIAL_DESIGN.get(_tr["nct_id"])
            if _d:
                _tr["design"] = _d
except FileNotFoundError:
    pass

# Coverage enrichment (parsed vs estimated raw criteria per trial), same sidecar pattern as
# api/trace.py -- was missing here, so the local UI and the deployed UI disagreed on the pill.
try:
    with open(os.path.join(HERE, "coverage_map.json"), encoding="utf-8") as f:
        _RAW_COUNT = json.load(f)
    try:
        with open(os.path.join(HERE, "coverage_map_extra.json"), encoding="utf-8") as f:
            for _k, _v in json.load(f).items():
                _RAW_COUNT.setdefault(_k, _v)
    except FileNotFoundError:
        pass
    for _t in TRACES:
        for _tr in _t.get("trials", []):
            _raw_n = _RAW_COUNT.get(_tr["nct_id"])
            if _raw_n:
                _tr["coverage"] = {"parsed": len(_tr.get("criteria", [])), "raw_estimated": _raw_n}
except FileNotFoundError:
    pass

# Bilingual gloss sidecar (gen_gloss.py), same sidecar pattern as coverage/trial_intent above and
# identical to api/trace.py's block: {sha1(source.strip())[:12]: {"src", "ko"/"en"}}, built once
# by a separate offline script and never touched here. gen_gloss.py may still be mid-write (it
# writes the whole file on every batch) -- a missing file or a torn/partial JSON read must
# degrade to "no glosses", never crash the server. json.JSONDecodeError is the concrete failure
# mode of reading a file mid-write.
try:
    with open(os.path.join(HERE, "gloss.json"), encoding="utf-8") as f:
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
    """{sha1key: {"ko"/"en": text}} for exactly the strings this trace needs -- not the whole
    GLOSS store, so a patient with 40 criteria never ships another patient's glosses."""
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


for _t in TRACES:
    _t["gloss"] = build_trace_gloss(_t)

# Stable criterion_id (added for the question-criterion linking fix): sha1(nct_id + normalized
# text)[:10], attached here IN MEMORY only -- traces.json on disk never carries it. Lets a
# client-round-tripped criterion be matched back to the exact one served, independent of any
# text re-typing, once the UI starts using it instead of raw text for cross-checks.
for _t in TRACES:
    for _tr in _t.get("trials", []):
        for _c in _tr.get("criteria", []):
            _c["criterion_id"] = criterion_id(_tr["nct_id"], _c.get("text", ""))

# Recommendation priority + trial-level STOP for the frozen traces, identical to api/trace.py:
# re-rank IN MEMORY (traces.json untouched) with ranking.rank_trials, and mark undecided criteria
# on already-INELIGIBLE trials STOP instead of ASK.
for _t in TRACES:
    apply_trial_level_actions(_t.get("trials", []))
    _t["frozen_rank_order"] = [x["nct_id"] for x in sorted(_t.get("trials", []), key=lambda x: x.get("rank", 99))]
    # the patient's need (deterministic keyword rules, no LLM) drives the help group of the
    # three-question sort and is attached for the UI -- same block as api/trace.py.
    _need = classify_patient_need(_t.get("patient_text", ""))
    _t["patient_need"] = _need
    ranking.rank_trials(_t.get("trials", []), trust_attached=False, patient_need=_need)
    _t["ranking"] = {"version": ranking.RANKING_VERSION, "rule_ko": ranking.RANKING_RULE_KO,
                     "hard_exclusion_holds": ranking.hard_exclusion_holds(_t.get("trials", []))}

# The stress patients' own trials, fetched from ClinicalTrials.gov. Without these the
# keyword picker had to choose from the S001-S010 pool, which contains no Alzheimer's or
# HFrEF trial at all -- so a 72-year-old dementia patient was scored against a paediatric
# trial and everything came back INELIGIBLE for reasons that had nothing to do with them.
STRESS_TRIALS = {}
STRESS_TRIALS_BY_PATIENT = {}
try:
    with open(os.path.join(HERE, "trials_stress.json"), encoding="utf-8") as f:
        STRESS_TRIALS = json.load(f)
    # which trials belong to which patient comes from the human answer key, not a guess
    with open(os.path.join(HERE, "eval_labels_stress.json"), encoding="utf-8") as f:
        for _row in json.load(f):
            STRESS_TRIALS_BY_PATIENT.setdefault(_row["patient_id"], set()).add(_row["nct_id"])
    # a variant inherits its base case's trials (T001-b is still the T001 bladder-cancer case)
    for _pid in list(STRESS_PATIENTS_BY_ID):
        base = _pid.rsplit("-", 1)[0] if "-" in _pid else _pid
        if not STRESS_TRIALS_BY_PATIENT.get(_pid) and STRESS_TRIALS_BY_PATIENT.get(base):
            STRESS_TRIALS_BY_PATIENT[_pid] = set(STRESS_TRIALS_BY_PATIENT[base])
except FileNotFoundError:
    pass

with open(os.path.join(HERE, "trials_raw.json")) as f:
    TRIALS_RAW = json.load(f)
_all_trials = {}
for _entry in TRIALS_RAW.values():
    for _t in _entry["trials"]:
        _all_trials[_t["nct_id"]] = _t
ALL_TRIALS = list(_all_trials.values())

from model_choices import MODEL_CHOICES  # noqa: E402

SESSIONS = {}
SESSIONS_LOCK = threading.Lock()

# Sessions live in memory, so restarting the server used to strand whoever was mid-demo
# with "session not found" and no way back. Completed sessions are mirrored to disk and
# reloaded at startup: a restart (or a crash) no longer costs a finished run.
SESSION_STORE = os.path.join(HERE, "cache", "sessions")
_SESSION_PERSIST_KEYS = ("id", "mode", "patient", "patient_need", "stage", "error", "extraction",
                         "trials_out", "gaps", "questions", "extended_record",
                         "answer_rounds", "created")


def persist_session(session):
    """Mirror a session to disk. Best-effort: a demo must never fail because of this."""
    try:
        os.makedirs(SESSION_STORE, exist_ok=True)
        data = {k: session.get(k) for k in _SESSION_PERSIST_KEYS}
        # Each answer round carries a `_before` deep copy of the whole trial state for revert.
        # Persisting it would bloat the file by a full copy per round (and revert doesn't
        # survive a restart anyway -- a restored session is inert). Strip it, matching the
        # API output, so disk holds only the reviewable history.
        if isinstance(data.get("answer_rounds"), list):
            data["answer_rounds"] = [{k: v for k, v in r.items() if k != "_before"}
                                     for r in data["answer_rounds"]]
        tmp = os.path.join(SESSION_STORE, f".{session['id']}.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        os.replace(tmp, os.path.join(SESSION_STORE, f"{session['id']}.json"))
    except Exception as e:  # noqa: BLE001 - never let persistence break a live session
        print(f"[live_server] session persist failed ({e})")


def load_persisted_sessions(max_age_hours=12):
    """Restore sessions written by a previous process, so a restart is survivable."""
    if not os.path.isdir(SESSION_STORE):
        return 0
    cutoff = time.time() - max_age_hours * 3600
    restored = 0
    for name in os.listdir(SESSION_STORE):
        if not name.endswith(".json"):
            continue
        path = os.path.join(SESSION_STORE, name)
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            continue
        if not data.get("id") or (data.get("created") or 0) < cutoff:
            # too old to restore -- also delete it so the store doesn't grow across restarts
            try:
                os.remove(path)
            except OSError:
                pass
            continue
        # a restored session is inert: its builder thread is gone, so anything not
        # finished is marked done at whatever stage it reached rather than hanging.
        if data.get("stage") not in ("done", "error"):
            data["stage"] = "done"
        data["lock"] = threading.Lock()
        SESSIONS[data["id"]] = data
        restored += 1
    return restored

# chronological stage order actually executed by the live pipeline
STAGE_ORDER = ["queued", "extract", "parse", "match", "gaps", "questions", "recommend", "done"]


def _tokens(text):
    return set(re.findall(r"[a-z0-9%.]+", (text or "").lower()))


def select_candidate_trials(vignette_text, fields, n=TRIALS_PER_PATIENT):
    """Heuristic keyword/condition overlap over the global trial pool. Uses the
    LLM-extracted field values (not just raw vignette text) so a non-English
    pasted vignette still matches -- the extractor normalizes clinical terms."""
    field_text = " ".join(f"{f['name']} {f['value']}" for f in fields)
    query = _tokens(vignette_text + " " + field_text)
    scored = []
    for t in ALL_TRIALS:
        cond_tok = _tokens(" ".join(t.get("conditions", [])))
        title_tok = _tokens(t.get("title", ""))
        crit_tok = _tokens(t.get("eligibility_criteria_raw", "")[:1000])
        score = 3 * len(query & cond_tok) + 2 * len(query & title_tok) + len(query & crit_tok)
        scored.append((score, t))
    scored.sort(key=lambda pair: -pair[0])
    return [t for _, t in scored[:n]]


def _ranking(trials_out):
    return [{"nct_id": t["nct_id"], "rank": t.get("rank", 99),
              "eligibility": t.get("eligibility", "UNCERTAIN"),
              "rationale": t.get("rationale", "")} for t in trials_out]


# ---------------------------------------------------------------------------
# session builders (run in a background thread per session)
# ---------------------------------------------------------------------------
def build_session_precomputed(session, trace):
    try:
        # need was classified at load time and attached to the trace (same value the module-
        # level re-rank used); recompute only if a trace somehow predates that block.
        session["patient_need"] = trace.get("patient_need") or classify_patient_need(
            trace.get("patient_text", ""))
        # precomputed at module load (build_trace_gloss), from this same trace's own strings.
        session["gloss"] = trace.get("gloss") or {}
        session["stage"] = "extract"
        session["extraction"] = trace["extraction"]
        time.sleep(0.35)
        session["stage"] = "parse"
        trials_out = [dict(t, criteria=[dict(c) for c in t["criteria"]]) for t in trace["trials"]]
        session["trials_out"] = trials_out
        time.sleep(0.35)
        session["stage"] = "match"
        time.sleep(0.35)
        session["stage"] = "gaps"
        time.sleep(0.35)
        session["stage"] = "questions"
        # enrich with affects_trials/affects_criteria/may_change_rank for the cards.
        # Older frozen traces carry no gaps -> enrich_questions falls back to token overlap.
        session["questions"] = enrich_questions(
            [dict(q) for q in trace["questions"]], trace.get("gaps", []), trials_out)
        time.sleep(0.35)
        session["stage"] = "recommend"
        time.sleep(0.35)
        session["stage"] = "done"
        persist_session(session)
    except Exception as e:
        session["stage"] = "error"
        session["error"] = str(e)
        persist_session(session)


def _build_one_trial_live(patient, fields, t):
    """One candidate trial's parse -> match -> intent-classify, run inside a ThreadPoolExecutor
    worker by build_session_live. Pure function of its args: `patient`/`fields` are read-only
    (shared across every worker, never written), and everything returned is freshly built here
    -- no shared mutable trial dict crosses threads. Returns (trial_out_dict, flat_criteria_list)
    so the caller assembles trials_out/all_criteria_flat itself, in candidate order."""
    criteria = parse_criteria(t)
    matched = match_trial(patient, fields, criteria, nct_id=t["nct_id"])
    flat = [{"nct_id": t["nct_id"], "text": c["text"], "verdict": c["verdict"],
             "action": c.get("action"), "effect": c.get("effect")} for c in matched]
    _intent = classify_trial_intent(t)
    trial_out = {
        "nct_id": t["nct_id"], "title": t["title"], "phase": t.get("phase", "NA"),
        "criteria": matched,
        # recency: how fresh the eligibility criteria are. Trial criteria on
        # ClinicalTrials.gov change over time; a coordinator needs to know the
        # screening was run against criteria fetched on this date, not "current".
        "criteria_fetched_at": t.get("fetched_at"),
        "criteria_source": t.get("source"),
        # therapeutic/supportive/care_delivery/observational -- classified live since
        # `t` here is the raw trial record (title/phase/conditions/eligibility text
        # all present), same rule-based classifier the sidecar uses for frozen traces.
        "trial_intent": {"intent": _intent["intent"], "confidence": _intent["confidence"]},
    }
    return trial_out, flat


def build_session_live(session):
    try:
        patient = session["patient"]
        session["stage"] = "extract"
        fields, dropped = extract_patient(patient)
        session["extraction"] = fields
        # Need card immediately (deterministic, no LLM): on the live path the UI otherwise
        # waits ~8 LLM calls before the anchor of the whole screen appears. recommend() will
        # recompute the same value later (same pure function) -- no divergence possible.
        session["patient_need"] = classify_patient_need(patient["text"])
        # live-generated text (pasted vignette / stress patient) isn't in gen_gloss.py's source
        # set (it only scans the frozen TRACES) -- no glosses to offer, ever, not just "not yet".
        session["gloss"] = {}
        persist_session(session)

        # A stress patient is scored against ITS OWN trials (the ones the human answer key
        # was written against), not whatever the keyword picker finds in the demo pool.
        pinned = STRESS_TRIALS_BY_PATIENT.get(patient.get("patient_id")) or set()
        candidates = [STRESS_TRIALS[n] for n in sorted(pinned) if n in STRESS_TRIALS]
        if not candidates:
            candidates = select_candidate_trials(patient["text"], fields, TRIALS_PER_PATIENT)
        session["trials_total"] = len(candidates)
        session["trials_done"] = 0

        # Per-trial parse+match run concurrently (2026-08-20 latency work): each candidate's
        # criteria-parser + matcher calls are independent of every other trial's -- 4 trials
        # sequential (8 LLM calls back to back) becomes 4 trials in parallel, bounded by
        # max_workers. `patient`/`fields` are read-only across every worker; each worker
        # returns its own new dicts (never mutates a shared trial dict), so there is nothing
        # to race on.
        #
        # trials_out is assigned ONCE, fully populated and in CANDIDATE order (not completion
        # order) -- not progressively appended as each trial lands, unlike the old sequential
        # loop. A partial list with placeholder entries would break session_snapshot's
        # eligibility_path() call over every trial on any poll landing mid-build; verified no
        # shipped page needs the old progressive reveal (grepped every *.html/*.js in the repo
        # for this server's port/session routes -- none call it, the live-vignette path has no
        # wired frontend yet). trials_done still climbs in real time under session["lock"], so
        # a future poller's progress bar (X/4 loaded) stays truthful throughout the build even
        # though trials_out itself only reveals once everything is ready.
        session["stage"] = "match"  # parse+match now run fused inside one worker per trial;
        # "match" stands in for the whole concurrent span -- nothing reads the finer-grained
        # "parse" vs "match" distinction today (same grep as above).
        lock = session["lock"]
        results = [None] * len(candidates)
        with ThreadPoolExecutor(max_workers=4) as ex:
            futures = {ex.submit(_build_one_trial_live, patient, fields, t): i
                       for i, t in enumerate(candidates)}
            for fut in as_completed(futures):
                i = futures[fut]
                # a worker's exception re-raises here, propagates past the executor's
                # __exit__ (which first waits out the remaining in-flight workers -- same
                # total wall time as letting them finish, no behavior change) and lands in
                # this function's own try/except below, same as the old sequential loop.
                results[i] = fut.result()
                with lock:
                    session["trials_done"] += 1

        trials_out = [r[0] for r in results]
        all_criteria_flat = [item for r in results for item in r[1]]
        session["trials_out"] = trials_out

        session["stage"] = "gaps"
        gaps = detect_gaps(patient, all_criteria_flat)
        session["gaps"] = gaps

        session["stage"] = "questions"
        questions = generate_questions(patient, gaps)
        session["questions"] = questions

        session["stage"] = "recommend"
        # trust_attached=True: the trial_intent on these dicts was classified server-side above
        # (classify_trial_intent), so ranking may use it for trials outside the sidecar.
        recs, need = recommend(patient, trials_out, trust_attached=True)
        session["patient_need"] = need
        apply_recommendation(trials_out, recs)
        apply_trial_level_actions(trials_out)

        # priority numbers now that eligibility/rank are decided
        enrich_questions(questions, gaps, trials_out)

        session["stage"] = "done"
        persist_session(session)
    except Exception as e:
        session["stage"] = "error"
        session["error"] = str(e)
        persist_session(session)


# ---------------------------------------------------------------------------
# answer round: reuse run_reeval's field->criteria mapping logic, but with a
# REAL human answer instead of a simulated one.
# ---------------------------------------------------------------------------
def ensure_gaps(session):
    if session.get("gaps") is None:
        all_criteria_flat = [
            {"nct_id": t["nct_id"], "text": c["text"], "verdict": c["verdict"], "action": c.get("action"),
             "effect": c.get("effect")}
            for t in session["trials_out"] for c in t["criteria"]
        ]
        session["gaps"] = detect_gaps(session["patient"], all_criteria_flat)
    return session["gaps"]


def find_affected(session, question_text):
    """Which still-undecided criteria does this answer bear on? Two link rungs, in order:
    (1) the question's own field -> that gap's related_criteria; (2) no field match ->
    token overlap between the question and any gap's field/why_needed -> that gap's
    related_criteria. Comparison is normalized (action_policy.normalize_criterion_text) so a
    stray whitespace/punctuation difference between a gap's related_criteria (LLM-retyped)
    and the real criterion text can no longer break the link (지우's DAS28 case).

    If NEITHER rung finds a link, target_texts stays empty and this returns [] -- it must
    NOT fall through to "every open criterion" (the bug this replaces: an empty target set
    used to compare falsy, so nothing was ever filtered and every undecided criterion on
    every trial came back "affected", silently re-evaluating the whole trace and spending
    the metered key on a single answer)."""
    trials_out = session["trials_out"]
    gaps = ensure_gaps(session)
    gaps_by_field = {g["field"]: g for g in gaps}

    field = None
    for q in session.get("questions", []):
        if q["question"] == question_text:
            field = q.get("field")
            break

    target_texts = set()
    if field and field in gaps_by_field:
        target_texts.update(gaps_by_field[field].get("related_criteria", []))
    if not target_texts:
        # fallback: token overlap between the question and any gap's field/why_needed
        qtok = _tokens(question_text)
        for g in gaps:
            gtok = _tokens(g["field"] + " " + g.get("why_needed", ""))
            if qtok & gtok:
                target_texts.update(g.get("related_criteria", []))
    target_norm = {normalize_criterion_text(x) for x in target_texts}
    if not target_norm:
        # no link at all on either rung: correctly resolve to NOTHING, not everything
        return []

    affected = []
    for t_idx, t in enumerate(trials_out):
        # trial-level STOP: a trial that already carries a hard FAIL is out; re-evaluating
        # its other criteria cannot change anything and only spends the metered key (same
        # gating action_policy._affected_criteria and api/answer.find_affected already do).
        if trial_is_blocked(t):
            continue
        for c_idx, c in enumerate(t["criteria"]):
            if c["verdict"] not in ("UNKNOWN", "UNCERTAIN"):
                continue
            if normalize_criterion_text(c["text"]) not in target_norm:
                continue
            affected.append({
                "nct_id": t["nct_id"], "trial_idx": t_idx, "crit_idx": c_idx,
                "text": c["text"], "type": c["type"], "before_verdict": c["verdict"],
            })
    return affected


def eligibility_path(trial):
    """What stands between this patient and enrolment on this trial.

    This is the screening worklist a coordinator actually keeps: what has already been
    satisfied, what is blocking, and what still has to be chased down (with the action the
    policy layer chose). Derived entirely from criteria already computed -- no extra call.
    """
    blocking, to_resolve, satisfied = [], [], []
    for c in trial.get("criteria", []):
        entry = {"text": c.get("text"), "type": c.get("type"), "verdict": c.get("verdict"),
                 "evidence": c.get("evidence"), "action": c.get("action"),
                 "uncertainty_type": c.get("uncertainty_type")}
        eff = c.get("effect")
        if eff == "FAIL":
            blocking.append(entry)
        elif eff == "PASS":
            satisfied.append(entry)
        else:
            to_resolve.append(entry)
    if blocking:
        verdict = "제외 사유 있음"
    elif to_resolve:
        verdict = f"확인 {len(to_resolve)}건 남음"
    else:
        verdict = "선별 통과"
    return {"blocking": blocking, "to_resolve": to_resolve, "satisfied": satisfied,
            "summary": verdict, "n_blocking": len(blocking),
            "n_to_resolve": len(to_resolve), "n_satisfied": len(satisfied)}


def handle_answers_batch(session, items, want_followups=True):
    """Apply several answers, then re-evaluate once. One snapshot covers the whole batch,
    so a single revert undoes the batch the way the reviewer entered it. After a round that
    actually rematched, a background follow-up check (detect_gaps + generate_questions over
    the post-answer state) asks whether MORE questions are needed -- same behavior as the
    deployed api/answer.py; want_followups=False skips it."""
    with session["lock"]:
        before = _snapshot(session)
        round_n = len(session.get("answer_rounds", [])) + 1
        applied, affected_all = [], []
        seen = set()
        for it in items:
            q = str(it.get("question", "")).strip()
            a = str(it.get("answer", "")).strip()
            if not q or not a:
                continue
            session["extended_record"] = (
                session.get("extended_record", "") + f"\n추가 문진 Q: {q} / A: {a}"
            ).strip()
            applied.append({"question": q, "answer": a})
            for af in find_affected(session, q):
                key = (af["nct_id"], af["text"])
                if key not in seen:
                    seen.add(key)
                    affected_all.append(af)
        # cost-guard parity with api/answer.py: one round never rematches more than
        # MAX_AFFECTED_PER_ROUND criteria on the metered backend
        affected_all = affected_all[:MAX_AFFECTED_PER_ROUND]

        if not applied:
            return {"error": "no usable answers"}

        verdict_changes = []
        if affected_all:
            rematched = rematch_affected_criteria(session["patient"],
                                                   session["extended_record"], affected_all)
            for r in rematched:
                crit = session["trials_out"][r["trial_idx"]]["criteria"][r["crit_idx"]]
                crit["verdict"] = r["after_verdict"]
                crit["effect"] = effect_of(crit["type"], r["after_verdict"])
                if r["after_evidence"]:
                    crit["evidence"] = r["after_evidence"]
                crit["reasoning"] = r["after_reasoning"]
                if r["after_verdict"] != r["before_verdict"]:
                    verdict_changes.append({"nct_id": r["nct_id"], "criterion": r["text"],
                                             "before": r["before_verdict"],
                                             "after": r["after_verdict"]})
            recs, session["patient_need"] = recommend(session["patient"], session["trials_out"],
                                                      trust_attached=True)
            apply_recommendation(session["trials_out"], recs)
            apply_trial_level_actions(session["trials_out"])
            # affects_trials/affects_criteria/may_change_rank are a pure function of the
            # current trial state (action_policy.priority_numbers); refresh them here so the
            # cards' numbers and sort order reflect what THIS batch just resolved, not what
            # was true before it -- same recompute api/answer.py does per (stateless) request.
            enrich_questions(session.get("questions", []), session.get("gaps") or [],
                             session["trials_out"])

        # Follow-up check, only on a round that actually rematched: with the answers now in
        # the record, are MORE questions needed for an accurate judgment? Same generation as
        # api/answer.py: detect_gaps honors the blocked-trial gate via the effect fields and
        # is_question_worthy via the action fields; the patient text is the vignette plus the
        # grown extended record, so just-closed gaps do not resurface. Deduped (normalized
        # text) against every question this session has shown AND this round's answers.
        # 2 extra LLM calls; a failure here must never fail the answer round.
        followup_questions, followup_error = [], None
        if affected_all and want_followups:
            try:
                asked = ([q.get("question", "") for q in session.get("questions", [])]
                         + [i["question"] for i in applied])
                all_criteria_flat = [
                    {"nct_id": t.get("nct_id"), "text": c.get("text", ""),
                     "verdict": c.get("verdict"), "action": c.get("action"),
                     "effect": c.get("effect")}
                    for t in session["trials_out"] for c in t.get("criteria", [])
                ]
                patient_ext = {"patient_id": session["patient"]["patient_id"],
                               "text": (session["patient"]["text"] + "\n"
                                        + session.get("extended_record", "")).strip()}
                fgaps = detect_gaps(patient_ext, all_criteria_flat)
                if fgaps:
                    followup_questions = dedupe_followups(
                        generate_questions(patient_ext, fgaps), asked, cap=3)
                    for q in followup_questions:
                        q["followup"] = True
                    enrich_questions(followup_questions, fgaps, session["trials_out"])
                if followup_questions:
                    # onto the session's question dock, flagged, so later answers to them run
                    # through the same find_affected/answer flow as the original questions...
                    session.setdefault("questions", []).extend(followup_questions)
                    # ...and merge their fresh gap links so find_affected's field rung can
                    # locate the criteria a follow-up answer resolves (append-only: existing
                    # fields keep the links the original questions were built against).
                    if isinstance(session.get("gaps"), list):
                        have = {g.get("field") for g in session["gaps"]}
                        session["gaps"].extend(
                            g for g in fgaps if g.get("field") not in have)
            except Exception as e:  # noqa: BLE001 - followups are best-effort by contract
                print(f"[live_server] followup generation failed ({e})")
                followup_questions = []
                followup_error = "추가 질문 생성에 실패했습니다. 이번 반영 결과에는 영향이 없습니다."

        rank_changes = []
        for t in session["trials_out"]:
            prev = next((b for b in before["trials_out"] if b["nct_id"] == t["nct_id"]), None)
            if prev and (prev.get("rank") != t.get("rank")
                         or prev.get("eligibility") != t.get("eligibility")):
                rank_changes.append({"nct_id": t["nct_id"], "title": t.get("title"),
                                      "rank_before": prev.get("rank"), "rank_after": t.get("rank"),
                                      "eligibility_before": prev.get("eligibility"),
                                      "eligibility_after": t.get("eligibility")})

        session.setdefault("answer_rounds", []).append({
            "round": round_n, "batch": applied,
            "question": " / ".join(i["question"] for i in applied),
            "answer": " / ".join(i["answer"] for i in applied),
            "verdict_changes": verdict_changes, "rank_changes": rank_changes, "_before": before,
        })
        persist_session(session)
        out = {
            "round": round_n, "applied": applied,
            "verdict_changes": verdict_changes, "rank_changes": rank_changes,
            "affected": [{"nct_id": a["nct_id"], "text": a["text"]} for a in affected_all],
            "updated_trials": session["trials_out"],
            "recommendation": _ranking(session["trials_out"]),
            # refreshed priority numbers (stale until affected_all ran the recompute above,
            # unchanged and still correct when nothing was affected) -- lets the client render
            # the current dock straight from this response instead of a second round trip.
            # Includes any just-generated follow-ups (flagged followup=true).
            "questions": session.get("questions", []),
            # [] = the existing questions suffice (or no rematch ran / followups skipped)
            "followup_questions": followup_questions,
        }
        if followup_error:
            out["followup_error"] = followup_error
        if not affected_all:  # same plain note the single-answer path returns
            out["note"] = "이 답변과 연결되는 미확정 기준이 없습니다."
        return out


def _snapshot(session):
    """Deep copy of everything an answer round mutates, so a round can be undone."""
    return {
        "trials_out": copy.deepcopy(session.get("trials_out", [])),
        "extended_record": session.get("extended_record", ""),
        "gaps": copy.deepcopy(session.get("gaps")),
    }


def revert_last_round(session):
    """Undo the most recent answer round. Reviewers try an answer to see what it moves;
    without this they would have to rebuild the whole session to take it back."""
    with session["lock"]:
        rounds = session.get("answer_rounds") or []
        if not rounds:
            return {"error": "되돌릴 답변이 없습니다."}
        last = rounds.pop()
        snap = last.get("_before")
        if not snap:
            rounds.append(last)
            return {"error": "이 답변은 되돌릴 수 없습니다 (이전 상태 미기록)."}
        session["trials_out"] = copy.deepcopy(snap["trials_out"])
        session["extended_record"] = snap["extended_record"]
        session["gaps"] = copy.deepcopy(snap["gaps"])
        # the round being undone last refreshed the priority numbers for its own (post-round)
        # state; now that trials_out/gaps are rolled back, those numbers must roll back too --
        # otherwise a reverted answer's card would show numbers from a round that no longer
        # happened.
        enrich_questions(session.get("questions", []), session.get("gaps") or [],
                         session["trials_out"])
        persist_session(session)
        # the exact questions this round answered, so the client un-greys ONLY these cards
        # rather than re-opening every prior committed round (review #3).
        reverted_qs = ([b.get("question") for b in (last.get("batch") or [])]
                       or [last.get("question")])
        return {
            "reverted_round": last.get("round"),
            "reverted_question": last.get("question"),
            "reverted_questions": [q for q in reverted_qs if q],
            "updated_trials": session["trials_out"],
            "recommendation": _ranking(session["trials_out"]),
            "rounds_left": len(rounds),
            "questions": session.get("questions", []),
        }


def handle_answer(session, question_text, answer_text):
    """Single answer = a batch of one. One code path (verifier finding 08-19: the two paths
    had drifted -- the single path never ran the follow-up check). The response keeps the
    single-path shape the client reads (note when nothing linked)."""
    out = handle_answers_batch(session, [{"question": question_text, "answer": answer_text}])
    if not out.get("affected"):
        out.setdefault("note", "이 답변과 연결되는 미확정 기준이 없습니다.")
    return out


ROUTE_SESSION = re.compile(r"^/api/session/([a-f0-9]{32})$")
ROUTE_ANSWER = re.compile(r"^/api/session/([a-f0-9]{32})/answer$")
ROUTE_ANSWER_BATCH = re.compile(r"^/api/session/([a-f0-9]{32})/answers$")
ROUTE_REVERT = re.compile(r"^/api/session/([a-f0-9]{32})/revert$")



MAX_ANSWERS_PER_BATCH = 5   # parity with api/answer.py
MAX_AFFECTED_PER_ROUND = 12  # parity with api/answer.py MAX_AFFECTED
MAX_ANSWER_CHARS = 600
MAX_QUESTION_CHARS = 400


def session_snapshot(session):
    # trials_out is sorted in place under session["lock"] by every answer round; a poll
    # landing mid-sort could serialize a torn/empty list. Read under the same lock (review #4).
    lock = session.get("lock")
    if lock is not None:
        with lock:
            return _session_snapshot_locked(session)
    return _session_snapshot_locked(session)


def _session_snapshot_locked(session):
    return {
        "session_id": session["id"],
        "mode": session["mode"],
        "stage": session["stage"],
        "error": session.get("error"),
        "progress": {"trials_done": session.get("trials_done", 0), "trials_total": session.get("trials_total", 0)},
        "result": {
            "patient": {"patient_id": session["patient"]["patient_id"], "text": session["patient"]["text"]},
            "patient_need": session.get("patient_need"),
            "extraction": session.get("extraction", []),
            "trials": session.get("trials_out", []),
            "questions": session.get("questions", []),
            "gloss": session.get("gloss", {}),
            "extended_record": session.get("extended_record", ""),
            # _before holds a deep copy for revert; it is internal and must not be shipped
            "answer_rounds": [{k: v for k, v in r.items() if k != "_before"}
                              for r in session.get("answer_rounds", [])],
            "eligibility_paths": {t["nct_id"]: eligibility_path(t)
                                   for t in session.get("trials_out", [])},
            "can_revert": bool(session.get("answer_rounds")),
        },
    }


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        print(f"[live_server] {self.address_string()} {fmt % args}")

    def _send_json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _read_json_body(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        if length <= 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw.decode("utf-8"))

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        try:
            if path == "/":
                with open(os.path.join(HERE, "live.html"), "rb") as f:
                    body = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return

            if path == "/api/meta":
                # report the backend actually in use -- the badge used to hardcode "Groq"
                # and kept saying so after the default moved to Anthropic/subscription.
                backend = os.environ.get("LLM_BACKEND", "anthropic")
                self._send_json({
                    "backend": backend,
                    "model": getattr(pipeline, "ACTIVE_MODEL", "unknown"),
                    "default_model": getattr(pipeline, "DEFAULT_MODEL", "unknown"),
                    "models": MODEL_CHOICES.get(backend, []),
                })
                return

            if path == "/api/patients":
                out = []
                for pid in sorted(PATIENTS_BY_ID):
                    p = PATIENTS_BY_ID[pid]
                    out.append({"id": pid, "title": p.get("condition", pid), "vignette": p["text"],
                                "group": "demo"})
                for pid in sorted(STRESS_PATIENTS_BY_ID):
                    p = STRESS_PATIENTS_BY_ID[pid]
                    causes = sorted(STRESS_EXPECTED_CAUSES.get(pid, ()))
                    is_variant = "-" in pid
                    if causes:
                        note = "정답지 예상 원인: " + ", ".join(causes)
                    elif is_variant:
                        # a variant with no labeled cause is NOT the original: the corruption
                        # exists, it just still leaves the criterion decidable (expected MET).
                        note = "변형 (판정 가능 — 원인 표기 없음)"
                    else:
                        note = "원본 (손상 없음)"
                    out.append({"id": pid, "title": p.get("condition", pid),
                                "vignette": p["text"], "group": "stress",
                                "expected_causes": causes, "is_variant": is_variant,
                                "note": note})
                self._send_json(out)
                return

            m = ROUTE_SESSION.match(path)
            if m:
                session = SESSIONS.get(m.group(1))
                if not session:
                    self._send_json({"error": "session not found"}, status=404)
                    return
                self._send_json(session_snapshot(session))
                return

            self._send_json({"error": "not found"}, status=404)
        except Exception as e:
            self._send_json({"error": str(e)}, status=200)

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        try:
            if path == "/api/meta":
                # switch the model for subsequent runs; only ids offered for this backend
                body = self._read_json_body()
                backend = os.environ.get("LLM_BACKEND", "anthropic")
                wanted = str(body.get("model", "")).strip()
                allowed = {m["id"] for m in MODEL_CHOICES.get(backend, [])}
                if wanted not in allowed:
                    self._send_json({"error": f"model not available on backend {backend}"},
                                     status=400)
                    return
                self._send_json({"backend": backend, "model": pipeline.set_active_model(wanted)})
                return

            if path == "/api/session":
                body = self._read_json_body()
                patient_id = str(body.get("patient_id", "")).strip()
                vignette = str(body.get("vignette", "")).strip()

                if patient_id and patient_id in PATIENTS_BY_ID:
                    patient = PATIENTS_BY_ID[patient_id]
                    trace = TRACES_BY_ID.get(patient_id)
                    if not trace:
                        self._send_json({"error": f"no precomputed trace for {patient_id}"}, status=200)
                        return
                    sid = uuid.uuid4().hex
                    session = {
                        "id": sid, "mode": "precomputed", "patient": patient, "stage": "queued",
                        "error": None, "extraction": [], "trials_out": [], "gaps": None,
                        "questions": [], "extended_record": "", "answer_rounds": [],
                        "lock": threading.Lock(), "created": time.time(),
                    }
                    with SESSIONS_LOCK:
                        SESSIONS[sid] = session
                    threading.Thread(target=build_session_precomputed, args=(session, trace), daemon=True).start()
                    self._send_json({"session_id": sid, "mode": "precomputed"})
                    return

                # stress patients have no precomputed trace by design -- they take the same
                # live path as a pasted vignette, keeping their own id for the changelog.
                if patient_id and patient_id in STRESS_PATIENTS_BY_ID:
                    sp = STRESS_PATIENTS_BY_ID[patient_id]
                    sid = uuid.uuid4().hex
                    session = {
                        "id": sid, "mode": "live",
                        "patient": {"patient_id": patient_id, "text": sp["text"]},
                        "stage": "queued", "error": None, "extraction": [], "trials_out": [],
                        "gaps": None, "questions": [], "extended_record": "", "answer_rounds": [],
                        "lock": threading.Lock(), "created": time.time(),
                    }
                    with SESSIONS_LOCK:
                        SESSIONS[sid] = session
                    threading.Thread(target=build_session_live, args=(session,), daemon=True).start()
                    self._send_json({"session_id": sid, "mode": "live"})
                    return

                if vignette:
                    sid = uuid.uuid4().hex
                    patient = {"patient_id": f"CUSTOM-{sid[:8]}", "text": vignette}
                    session = {
                        "id": sid, "mode": "live", "patient": patient, "stage": "queued",
                        "error": None, "extraction": [], "trials_out": [], "gaps": None,
                        "questions": [], "extended_record": "", "answer_rounds": [],
                        "lock": threading.Lock(), "created": time.time(),
                    }
                    with SESSIONS_LOCK:
                        SESSIONS[sid] = session
                    threading.Thread(target=build_session_live, args=(session,), daemon=True).start()
                    self._send_json({"session_id": sid, "mode": "live"})
                    return

                self._send_json({"error": "provide patient_id or vignette"}, status=400)
                return

            m = ROUTE_ANSWER_BATCH.match(path)
            if m:
                # Answer several questions, then re-evaluate ONCE. Answering one at a time
                # costs a full re-match + recommend per question; a reviewer filling in a
                # chart wants to enter what they know and see the consequence together.
                session = SESSIONS.get(m.group(1))
                if not session:
                    self._send_json({"error": "session not found"}, status=404)
                    return
                body = self._read_json_body()
                items = body.get("answers")
                if not isinstance(items, list) or not items:
                    self._send_json({"error": "answers[] required"}, status=400)
                    return
                if len(items) > MAX_ANSWERS_PER_BATCH:
                    self._send_json({"error": f"too many answers (max {MAX_ANSWERS_PER_BATCH})"}, status=400)
                    return
                for _it in items:
                    if len(str(_it.get("answer", ""))) > MAX_ANSWER_CHARS or \
                       len(str(_it.get("question", ""))) > MAX_QUESTION_CHARS:
                        self._send_json({"error": "answer or question too long"}, status=400)
                        return
                if session["stage"] != "done":
                    self._send_json({"error": f"session not ready (stage={session['stage']})"}, status=200)
                    return
                try:
                    self._send_json(handle_answers_batch(
                        session, items,
                        want_followups=body.get("want_followups") is not False))
                except Exception as e:
                    self._send_json({"error": str(e)}, status=200)
                return

            m = ROUTE_REVERT.match(path)
            if m:
                session = SESSIONS.get(m.group(1))
                if not session:
                    self._send_json({"error": "session not found"}, status=404)
                    return
                self._send_json(revert_last_round(session))
                return

            m = ROUTE_ANSWER.match(path)
            if m:
                session = SESSIONS.get(m.group(1))
                if not session:
                    self._send_json({"error": "session not found"}, status=404)
                    return
                body = self._read_json_body()
                question = str(body.get("question", "")).strip()
                answer = str(body.get("answer", "")).strip()
                if not question or not answer:
                    self._send_json({"error": "question and answer are required"}, status=400)
                    return
                if session["stage"] != "done":
                    self._send_json({"error": f"session not ready (stage={session['stage']})"}, status=200)
                    return
                try:
                    result = handle_answer(session, question, answer)
                    self._send_json(result)
                except Exception as e:
                    self._send_json({"error": str(e)}, status=200)
                return

            self._send_json({"error": "not found"}, status=404)
        except Exception as e:
            self._send_json({"error": str(e)}, status=200)


def main():
    restored = load_persisted_sessions()
    if restored:
        print(f"[live_server] restored {restored} session(s) from a previous run")
    server = ThreadingHTTPServer(("localhost", PORT), Handler)
    print(f"live_server listening on http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
