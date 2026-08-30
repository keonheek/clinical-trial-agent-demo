"""POST /api/answer -> re-evaluate only the criteria the round's answers affect, re-rank, return.

Serverless functions share no memory, so the browser holds the session state (the current
trials array and the accumulated extended_record) and sends it back on every call. This module
is a pure function of its request body: patient_id + answers + trials + extended_record in,
updated trials + verdict_changes + extended_record (+ follow-up questions) out.

Two request forms, one re-evaluation round either way (Keonhee 08-19: multi-select across ALL
questions gets ONE 반영 click and ONE round, never one loop per question):
  single  {"question": ..., "answer": ...}            -- unchanged, back-compat
  batch   {"answers": [{"question", "answer"}, ...]}  -- max 5; single fields ignored when present
The per-question find_affected results are unioned (deduped by criterion, capped at
MAX_AFFECTED) into ONE rematch_affected_criteria call and ONE recommend call.

Reuses pipeline.py's rematch_affected_criteria/recommend/effect_of directly (same functions
live_server.py uses locally) -- no matching logic duplicated here. find_affected() is a
token-overlap heuristic standing in for live_server.py's gap-detector-based mapping. When no
question's tokens overlap anything open, the union is [] and handle() short-circuits before
any LLM call -- it must never fall back to resolving every open criterion (that silently
re-evaluates the whole trace on the metered key; the exact defect this file's find_affected
used to have, 지우 08-12).

After a round that actually rematched, a background follow-up check (detect_gaps +
generate_questions over the post-answer state) asks whether MORE questions are needed for an
accurate judgment; if the existing questions suffice it returns []. 2 extra LLM calls, so it
sits behind its own per-IP budget and want_followups=false skips it. A followup failure never
fails the answer round.

Never raises past do_POST: any failure comes back as HTTP 200 {"error": "..."}.
Run `python3 api/answer.py` for the offline self-tests (no LLM calls, no server).
"""
import copy
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault("LLM_BACKEND", "anthropic")

import anthropic_client
# Vercel's Python runtime filesystem is read-only except /tmp. anthropic_client's on-disk
# cache is a nice-to-have (repeat calls within one invocation, none across cold starts), not
# a correctness requirement, so point it at the one writable directory instead of editing the
# shared file.
anthropic_client.CACHE_DIR = "/tmp/cache"

from pipeline import (rematch_affected_criteria, recommend, apply_recommendation, effect_of,
                      VALID_VERDICTS, classify_action, apply_evidence_sufficiency,
                      detect_gaps, generate_questions, dedupe_followups)
from action_policy import (trial_level_action, trial_is_blocked, enrich_questions,
                           criterion_id)
from patient_need import classify_patient_need

with open(os.path.join(ROOT, "patients.json"), encoding="utf-8") as f:
    PATIENTS = json.load(f)
try:  # extra demo patients (gen_extra.py) -- answer rounds work on them too
    with open(os.path.join(ROOT, "patients_extra.json"), encoding="utf-8") as f:
        PATIENTS = PATIENTS + json.load(f)
except FileNotFoundError:
    pass
PATIENTS_BY_ID = {p["patient_id"]: p for p in PATIENTS}
KNOWN_IDS = set(PATIENTS_BY_ID)

# The client resends its trials array on every call, but every legitimate criterion for these
# fixed patients originated in traces.json -- so anything not in that whitelist is either a bug
# or an attempt to inject text into a prompt running on the metered key. Whitelist per patient:
# {(nct_id, criterion_text) -> criterion_type}.
with open(os.path.join(ROOT, "traces.json"), encoding="utf-8") as f:
    _TRACES = json.load(f)
try:
    with open(os.path.join(ROOT, "traces_extra.json"), encoding="utf-8") as f:
        _TRACES = _TRACES + json.load(f)
except FileNotFoundError:
    pass
KNOWN_CRITERIA = {}
# Server truth per (patient, trial): title/phase (they enter the ranking key) and the FULL
# criterion-text set. A posted trial must carry exactly that set -- otherwise a client could drop
# a trial's FAIL criteria and have it re-served as ELIGIBLE at rank 1 (adversarial review 08-16).
KNOWN_TRIALS = {}
for _p in _TRACES:
    KNOWN_CRITERIA[_p["patient_id"]] = {
        (t["nct_id"], c["text"]): c["type"]
        for t in _p.get("trials", []) for c in t.get("criteria", [])
    }
    KNOWN_TRIALS[_p["patient_id"]] = {
        t["nct_id"]: {"title": t.get("title", ""), "phase": t.get("phase", "NA"),
                      "criteria_texts": frozenset(c["text"] for c in t.get("criteria", []))}
        for t in _p.get("trials", [])
    }
del _TRACES

# ---------------------------------------------------------------------------
# cost guards -- this endpoint spends a real metered API key
# ---------------------------------------------------------------------------
MAX_ANSWER_LEN = 600
MAX_QUESTION_LEN = 300
MAX_AFFECTED = 12
MAX_BODY_BYTES = 128 * 1024      # real sessions serialize to a few KB
MAX_TRIALS = 6
MAX_LIVE_CRITERIA = 30           # live vignettes: the whitelist cannot apply, so cap hard
MAX_CRITERIA_PER_TRIAL = 16      # traces max is 13
MAX_QUESTIONS = 12               # traces hold <= 5 per patient
MAX_BATCH_ANSWERS = 5            # one 반영 click covers at most 5 question cards
MAX_ASKED_QUESTIONS = 50         # dedupe list the client resends; text only, never a prompt
FOLLOWUP_CAP = 3                 # same bound as the base question generator
RATE_LIMIT_PER_MIN = 10          # per client IP, per warm instance (cheap brake, not a wall)
FOLLOWUP_RATE_LIMIT_PER_MIN = 4  # follow-up generation adds 2 LLM calls/round on the metered
                                 # key -- its own tighter per-IP budget, same mechanism

# Wall-clock budget for the whole serverless round (spec step 2). vercel.json gives this
# function maxDuration=60; rematch alone can already run several seconds, so a round that
# also ran recommend + a 2-call followup chain could brush the ceiling on a slow day and
# 504 in front of judges. Not a hard cutoff mid-call (that would abandon an in-flight LLM
# call with no way to get its result back) -- a START gate: if the budget is already spent
# by the time the followup lane would begin, skip starting it and say so. Env-overridable
# for load testing without a redeploy.
ROUND_BUDGET_S = float(os.environ.get("ROUND_BUDGET_S", "45"))

# A/B switch (2026-08-20 latency work): both the sequential and concurrent lanes for
# recommend()/followups live in this file behind this flag, so the identity assertion in
# _selftest can run the SAME stubbed round both ways and diff the served output byte-for-byte
# -- not just eyeball two separate scripts. Default on; ANSWER_PARALLEL=0 reverts to the
# original sequential order (kept only as a rollback switch, not a maintained second path).
ANSWER_PARALLEL = os.environ.get("ANSWER_PARALLEL", "1") != "0"

_recent_calls = {}               # ip -> [monotonic-ish timestamps]
_followup_calls = {}             # ip -> [timestamps], consumed only when followups would run


def _rate_limited(ip, store=None, limit=RATE_LIMIT_PER_MIN):
    import time
    if store is None:
        store = _recent_calls
    now = time.time()
    window = [t for t in store.get(ip, []) if now - t < 60]
    if len(window) >= limit:
        store[ip] = window
        return True
    window.append(now)
    store[ip] = window
    return False


def _validate_trials(patient_id, trials):
    """Reject anything the frozen traces never produced. Returns an error string or None."""
    if len(trials) > MAX_TRIALS:
        return "too many trials"
    known = KNOWN_CRITERIA.get(patient_id, {})
    known_trials = KNOWN_TRIALS.get(patient_id, {})
    seen_nct = set()
    for t in trials:
        nct = t.get("nct_id")
        if nct not in known_trials or nct in seen_nct:
            return "unknown or duplicate trial for this patient"
        seen_nct.add(nct)
        criteria = t.get("criteria", [])
        if len(criteria) > MAX_CRITERIA_PER_TRIAL:
            return "too many criteria"
        for c in criteria:
            key = (nct, c.get("text"))
            if key not in known:
                return "unknown criterion for this patient"
            if c.get("type") != known[key]:
                return "criterion type mismatch"
            if c.get("verdict") is not None and c.get("verdict") not in VALID_VERDICTS:
                return "invalid verdict value"
        # the whole criterion set, not a subset: dropping a FAIL criterion must not un-exclude
        if frozenset(c.get("text") for c in criteria) != known_trials[nct]["criteria_texts"]:
            return "incomplete criterion set for trial"
    return None


def _restore_server_fields(patient_id, trials):
    if patient_id == "LIVE":
        return trials  # nothing frozen to restore from; live trials came from api/live.py
    """Title and phase come from traces.json, never from the body -- phase is a ranking tier."""
    known_trials = KNOWN_TRIALS.get(patient_id, {})
    for t in trials:
        k = known_trials.get(t.get("nct_id"))
        if k:
            t["title"] = k["title"]
            t["phase"] = k["phase"]
    return trials

# One token set for the whole system: action_policy's list includes the generic clinical words
# ("patient", "history", "evidence", ...) that this local list lacked -- the gap let an
# acute-exacerbation answer flip an unrelated consent criterion via the token "patient"
# (PI-persona catch, 08-20). Same normalization, same stopwords, everywhere.
from action_policy import _tokens, normalize_criterion_text  # noqa: E402


def find_affected(question_text, trials, answer_text=""):
    """Which still-unresolved criteria does this answer plausibly bear on? live_server.py
    answers this from an LLM-built gap -> related_criteria map; that map does not exist here
    (traces.json stores questions but not the gaps that produced them), so this does the same
    job with token overlap between the question and each candidate criterion's text (both run
    through action_policy.normalize_criterion_text first) -- the same fallback live_server.py
    itself falls back to when a question has no mapped gap.

    No overlap at all -> returns [] and the answer resolves nothing. This must NEVER fall back
    to "resolve every open criterion": that silently re-evaluates the whole trace on one
    unrelated answer and spends the metered key on criteria the answer never touched
    (지우's proven bug, same defect class as live_server.find_affected's empty-target case)."""
    # 08-30 stress review: widen with the answer's own tokens so an answer about consent
    # capacity or alcohol use reaches the same criterion on every non-blocked trial, not
    # only the trial whose wording overlapped the question. Still bounded by overlap.
    qtok = _tokens(question_text + " " + (answer_text or ""))
    affected = []
    for t_idx, t in enumerate(trials):
        # trial-level STOP: a trial that already carries a hard FAIL is out; re-evaluating its
        # other criteria cannot change anything and only spends the metered key.
        if trial_is_blocked(t):
            continue
        for c_idx, c in enumerate(t.get("criteria", [])):
            if c.get("verdict") not in ("UNKNOWN", "UNCERTAIN"):
                continue
            if qtok & _tokens(c.get("text", "")):
                affected.append({
                    "nct_id": t.get("nct_id"), "trial_idx": t_idx, "crit_idx": c_idx,
                    "text": c.get("text", ""), "type": c.get("type", "inclusion"),
                    "before_verdict": c.get("verdict"),
                })
    return affected[:MAX_AFFECTED]


def _extract_answer_pairs(body):
    """Both request forms -> a validated list of (question, answer) pairs, or an error.

    Batch form: {"answers": [{"question", "answer"}, ...]} -- max MAX_BATCH_ANSWERS items;
    when "answers" is present the top-level question/answer fields are IGNORED. Single form:
    the existing {"question", "answer"} pair, unchanged semantics and unchanged error strings.
    Every item is held to the same length caps as the single form (each answer line is
    interpolated into the rematch prompt on the metered key). Returns (pairs, error_or_None).
    """
    raw = body.get("answers")
    if raw is not None:
        if not isinstance(raw, list) or not raw:
            return None, "answers must be a non-empty array"
        if len(raw) > MAX_BATCH_ANSWERS:
            return None, f"too many answers (max {MAX_BATCH_ANSWERS})"
        pairs = []
        for it in raw:
            if not isinstance(it, dict):
                return None, "each answers[] item must be an object"
            q = str(it.get("question", "")).strip()
            a = str(it.get("answer", "")).strip()
            if not q or len(q) > MAX_QUESTION_LEN:
                return None, "invalid question in answers[]"
            if not a or len(a) > MAX_ANSWER_LEN:
                return None, f"each answer must be 1-{MAX_ANSWER_LEN} characters"
            pairs.append((q, a))
        return pairs, None
    q = str(body.get("question", "")).strip()
    a = str(body.get("answer", "")).strip()
    if not q or len(q) > MAX_QUESTION_LEN:
        return None, "invalid question"
    if not a or len(a) > MAX_ANSWER_LEN:
        return None, "answer must be 1-600 characters"
    return [(q, a)], None


def union_affected(pairs_affected, cap=MAX_AFFECTED):
    """Union the per-question find_affected results into ONE rematch worklist.

    pairs_affected: [(question_text, affected_list), ...] in the order answered.
    Dedupes by (trial_idx, crit_idx) -- two questions bearing on the same criterion re-evaluate
    it once, on the combined extended record -- and applies `cap` to the UNION, so a batch can
    never spend more of the metered key than a single answer was already allowed to.
    Returns (union, sources): sources maps (trial_idx, crit_idx) -> [question_text, ...] (first-
    seen order, unique), for attributing a verdict change to the question that triggered it.
    Pure function, no LLM.
    """
    union, sources = [], {}
    for question, affected in pairs_affected:
        for af in affected:
            key = (af["trial_idx"], af["crit_idx"])
            if key not in sources:
                sources[key] = []
                union.append(af)
            if question not in sources[key]:
                sources[key].append(question)
    union = union[:cap]
    kept = {(af["trial_idx"], af["crit_idx"]) for af in union}
    return union, {k: v for k, v in sources.items() if k in kept}


def _generate_followups(patient_id, vignette, new_record, trials_copy, asked_texts):
    """The background 'do we need MORE questions?' check: 2 LLM calls over the POST-answer state.

    Runs pipeline.detect_gaps (which honors is_question_worthy + the blocked-trial gate via the
    effect fields on the flat list) then pipeline.generate_questions, with the patient text =
    vignette + the grown extended record -- so a gap the answers just closed no longer surfaces,
    and only still-open UNKNOWN/UNCERTAIN criteria on non-blocked trials can become questions.
    Candidates are deduped against everything already asked (normalized text), capped at
    FOLLOWUP_CAP, stamped followup=True.

    Returns (followups, gaps) UNENRICHED -- the caller attaches the three priority numbers
    (action_policy.enrich_questions) itself, once trials_copy carries the post-recommend()
    eligibility/rank (2026-08-20: this lane can now run concurrently with recommend(), on its
    own trials_copy snapshot that predates apply_recommendation -- enrich_questions'
    may_change_rank reads t.get('eligibility'), so enriching here on a copy that never gets
    that field would silently compute a wrong number; enriching happens after both lanes join
    instead, against the real, fully-decided trials_copy, exactly reproducing the sequential
    order's result). ([], []) when the existing questions suffice (no gaps, or every candidate
    is a repeat) -- enrich_questions on an empty list is a no-op either way.
    """
    all_criteria_flat = [
        {"nct_id": t.get("nct_id"), "text": c.get("text", ""), "verdict": c.get("verdict"),
         "action": c.get("action"), "effect": c.get("effect")}
        for t in trials_copy for c in t.get("criteria", [])
    ]
    patient_ext = {"patient_id": patient_id, "text": (vignette + "\n" + new_record).strip()}
    gaps = detect_gaps(patient_ext, all_criteria_flat)
    if not gaps:
        return [], []
    followups = dedupe_followups(generate_questions(patient_ext, gaps), asked_texts,
                                 cap=FOLLOWUP_CAP)
    for q in followups:
        q["followup"] = True
    return followups, gaps


def handle(body, client_ip="?"):
    # Wall-clock budget starts here, not at the first LLM call -- validation/parsing above is
    # sub-millisecond, but the clock a Vercel invocation is actually judged against starts at
    # the top of the handler, so this is the honest zero point.
    t_start = time.monotonic()
    patient_id = str(body.get("patient_id", "")).strip()
    trials = body.get("trials")
    extended_record = str(body.get("extended_record", "")).strip()

    # LIVE = a vignette the reviewer typed in this session (api/live.py built it). Its criteria
    # were never in the frozen whitelist, so the whitelist cannot be the guard here; the caps
    # below (answer length, trial/criteria counts) and the per-IP rate limit are. The vignette
    # itself is client text in live mode by definition -- that is the feature.
    live_mode = patient_id == "LIVE"
    if not live_mode and patient_id not in KNOWN_IDS:
        return {"error": "unknown patient_id"}
    pairs, pairs_error = _extract_answer_pairs(body)
    if pairs_error:
        return {"error": pairs_error}
    if not isinstance(trials, list) or not trials:
        return {"error": "trials array required"}
    trials_error = None if live_mode else _validate_trials(patient_id, trials)
    if trials_error:
        return {"error": trials_error}
    if live_mode:
        if len(trials) > MAX_TRIALS:
            return {"error": "too many trials"}
        for t in trials:
            if len(t.get("criteria", [])) > MAX_LIVE_CRITERIA:
                return {"error": "too many criteria"}

    # never trust the client for the vignette itself -- only the fixed 10 patients exist here.
    patient = ({"patient_id": "LIVE", "text": str(body.get("patient_text", ""))[:1500]}
               if live_mode else
               {"patient_id": patient_id, "text": PATIENTS_BY_ID[patient_id]["text"]})

    # FOLLOW-UPS AS A SECOND REQUEST (08-20, measured): the core round (rematch + recommend) is
    # ~8s while the follow-up chain (detect_gaps -> generate_questions) adds ~9s of inherently
    # sequential work. Making the reviewer wait through it before seeing their own answer's
    # effect is the wrong trade, so the client now fires the round with want_followups=false
    # and asks for follow-ups here, separately, with the post-answer trials it just received.
    if body.get("followups_only") is True:
        if _rate_limited(client_ip, _followup_calls, FOLLOWUP_RATE_LIMIT_PER_MIN):
            return {"followup_questions": [], "followup_error": "추가 질문 확인 요청이 너무 잦습니다."}
        trials_copy = [dict(t, criteria=[dict(c) for c in t.get("criteria", [])]) for t in trials]
        _restore_server_fields(patient_id, trials_copy)
        for t in trials_copy:
            for c in t.get("criteria", []):
                c["criterion_id"] = criterion_id(t.get("nct_id"), c.get("text", ""))
        _asked = body.get("asked_questions")
        _asked = _asked if isinstance(_asked, list) else []
        asked_texts = [str(x)[:MAX_QUESTION_LEN] for x in _asked[:MAX_ASKED_QUESTIONS]
                       if isinstance(x, str) and x.strip()] + [q for q, _ in pairs]
        try:
            followups, gaps = _generate_followups(
                patient_id, patient["text"], extended_record, trials_copy, asked_texts)
            if followups:
                enrich_questions(followups, gaps, trials_copy)
            return {"followup_questions": followups}
        except Exception as e:  # noqa: BLE001 -- never fail the (already delivered) round
            return {"followup_questions": [], "followup_error": f"추가 질문 생성 실패: {e}"}
    # the patient's need, from the server-side vignette (deterministic rules, no LLM) -- the
    # same classification recommend() applies inside the ranking; attached for the UI.
    patient_need = classify_patient_need(patient["text"])

    trials_copy = [dict(t, criteria=[dict(c) for c in t.get("criteria", [])]) for t in trials]
    _restore_server_fields(patient_id, trials_copy)
    # ids are server truth, never echoed from the body
    for t in trials_copy:
        for c in t.get("criteria", []):
            c["criterion_id"] = criterion_id(t.get("nct_id"), c.get("text", ""))
    # optional: the client's current question list, so the three priority numbers can be
    # recomputed against the post-answer trials (pure arithmetic, no LLM; text is only tokenized)
    questions_in = body.get("questions")
    if not isinstance(questions_in, list):
        questions_in = []
    # Keep the served links and option lists too: affected_detail is the exact criterion set
    # the card promised to re-check, and options/options_en let a Korean answer contribute
    # English tokens. Both are bounded and enter no prompt.
    def _q_in(q):
        det = q.get("affected_detail") if isinstance(q.get("affected_detail"), list) else []
        det = [{"nct_id": str(d.get("nct_id", ""))[:20], "text": str(d.get("text", ""))[:500]}
               for d in det[:MAX_AFFECTED * 2] if isinstance(d, dict)]
        opts = [str(o)[:200] for o in (q.get("options") or [])[:8] if isinstance(o, str)]
        opts_en = [str(o)[:200] for o in (q.get("options_en") or [])[:8] if isinstance(o, str)]
        return {"field": str(q.get("field", ""))[:120], "question": str(q.get("question", ""))[:MAX_QUESTION_LEN],
                "affected_detail": det, "options": opts,
                "options_en": opts_en if len(opts_en) == len(opts) else []}
    questions_in = [_q_in(q) for q in questions_in[:MAX_QUESTIONS] if isinstance(q, dict) and q.get("question")]
    q_by_text = {q["question"]: q for q in questions_in}
    # already-asked question texts, resent by the client so follow-up generation never
    # re-asks something from an earlier round. Text is only ever normalized and compared --
    # it enters no prompt.
    asked_in = body.get("asked_questions")
    if not isinstance(asked_in, list):
        asked_in = []
    asked_in = [str(x)[:MAX_QUESTION_LEN] for x in asked_in[:MAX_ASKED_QUESTIONS]
                if isinstance(x, str) and x.strip()]

    # ONE round for the whole batch: per-question find_affected, then the union (deduped by
    # criterion, capped) feeds a single rematch + a single recommend -- never one loop per
    # question.
    def _affected_for(q, ans):
        qo = q_by_text.get(q) or {}
        # Korean option answers carry no Latin tokens ("악성종양 병력 없음" vs "malignant
        # tumors"); add each selected option's English text to the token source.
        ans_tok_src = ans
        for ko, en in zip(qo.get("options") or [], qo.get("options_en") or []):
            if ko and ko in ans and en:
                ans_tok_src += " " + en
        found = find_affected(q, trials_copy, ans_tok_src)
        # Then the explicit links the card showed (server-side affected_detail): an answer
        # must reach every criterion the question was linked to, not only the ones whose
        # wording happens to overlap -- his 08-30 screenshot: malignancy history stayed
        # UNKNOWN after "해당 사항 없음" because "history"/"patients" are stopwords and
        # "cancer" never matched "malignant tumors".
        seen = {(a["trial_idx"], a["crit_idx"]) for a in found}
        want = {(d["nct_id"], normalize_criterion_text(d["text"])) for d in qo.get("affected_detail") or []}
        if want:
            for t_idx, t in enumerate(trials_copy):
                if trial_is_blocked(t):
                    continue
                for c_idx, c in enumerate(t.get("criteria", [])):
                    if (t_idx, c_idx) in seen or c.get("verdict") not in ("UNKNOWN", "UNCERTAIN"):
                        continue
                    if (t.get("nct_id"), normalize_criterion_text(c.get("text", ""))) in want:
                        found.append({"nct_id": t.get("nct_id"), "trial_idx": t_idx, "crit_idx": c_idx,
                                      "text": c.get("text", ""), "type": c.get("type", "inclusion"),
                                      "before_verdict": c.get("verdict")})
                        seen.add((t_idx, c_idx))
        return found[:MAX_AFFECTED]

    affected, sources = union_affected([(q, _affected_for(q, ans)) for q, ans in pairs])
    new_record = (extended_record
                  + "".join(f"\n추가 문진 Q: {q} / A: {a}" for q, a in pairs)).strip()

    if not affected:
        return {
            "verdict_changes": [],
            "patient_need": patient_need,
            "trials": trials_copy,
            "recommendation": [
                {"nct_id": t.get("nct_id"), "rank": t.get("rank", 99), "eligibility": t.get("eligibility", "UNCERTAIN")}
                for t in trials_copy
            ],
            "questions": enrich_questions(questions_in, [], trials_copy) if questions_in else None,
            # no rematch ran this round -> no follow-up check either (nothing changed that
            # could warrant new questions); same key so the client reads one shape.
            "followup_questions": [],
            "extended_record": new_record,
            # true whether there is nothing left open, OR open criteria exist but none of them
            # relate to any answer in this round (find_affected found no overlap for the whole
            # union) -- same wording in live_server.py's handle_answer for the identical case.
            "note": "이 답변과 연결되는 미확정 기준이 없습니다.",
        }

    try:
        rematched = rematch_affected_criteria(patient, new_record, affected)
    except Exception as e:
        return {"error": f"재평가 호출 실패: {e}"}

    verdict_changes = []
    for r in rematched:
        crit = trials_copy[r["trial_idx"]]["criteria"][r["crit_idx"]]
        after_verdict = r["after_verdict"]
        # code-derived, same rule as the pipeline; clears stale badges on decided verdicts
        utype, action = classify_action(after_verdict, r.get("after_uncertainty_type"))
        # §6 evidence sufficiency, mirroring pipeline.run_reeval: a MET/NOT_MET resting on
        # structurally insufficient evidence (suspected/indirect) is demoted to UNCERTAIN/VERIFY.
        # No-op when the matcher returned no evidence_meta, so nothing changes silently.
        after_verdict, d_ut, d_act, _suff = apply_evidence_sufficiency(after_verdict, r.get("after_evidence_meta"))
        if d_ut:
            utype, action = d_ut, d_act
        crit["verdict"] = after_verdict
        crit["effect"] = effect_of(crit["type"], after_verdict)
        crit["uncertainty_type"], crit["action"] = utype, action
        crit.pop("action_scope", None)   # a decided criterion carries no trial-level STOP
        crit.pop("action_reason", None)  # (re-applied below if the trial is still blocked)
        if r.get("after_evidence"):
            crit["evidence"] = r["after_evidence"]
        crit["reasoning"] = r.get("after_reasoning", crit.get("reasoning", ""))
        if after_verdict != r["before_verdict"]:
            change = {
                "nct_id": r["nct_id"], "criterion": r["text"],
                "before": r["before_verdict"], "after": after_verdict,
            }
            # which answered question triggered this change -- only when exactly one
            # question in the round linked to this criterion (else ambiguous: omitted)
            srcs = sources.get((r["trial_idx"], r["crit_idx"]), [])
            if len(srcs) == 1:
                change["question"] = srcs[0]
            verdict_changes.append(change)

    # Trial-level action context, hoisted here (2026-08-20 latency work; used to run after
    # apply_recommendation below): once a trial carries a hard FAIL, asking about its
    # remaining undecided criteria is moot -> STOP (same class of rule as effect_of; no model
    # involved). Safe to hoist because trial_is_blocked's operative branch here depends only
    # on `effect`, already finalized by the verdict_changes loop above -- decide_eligibility
    # (inside recommend(), below) uses the exact same effect-based rule, so this is
    # output-identical to running it after apply_recommendation for any eligibility the
    # SERVER decides.
    #
    # It must NOT read `t["eligibility"]` here, though: trial_is_blocked also has an
    # eligibility=="INELIGIBLE" branch, and unlike after apply_recommendation runs (the old
    # position), trials_copy's `eligibility` at this point can still be whatever the CLIENT
    # posted -- _validate_trials never checks that field and _restore_server_fields only
    # restores title/phase. Feeding trial_is_blocked a criteria-only view keeps this
    # server-truth-only, closing the same class of gap as the adversarial review that added
    # trial_level_action itself (08-16): a forged eligibility must not be able to STOP a
    # trial's undecided criteria and suppress its follow-up questions.
    #
    # This must run BEFORE the two lanes below (not after recommend(), like the old
    # sequential order): the follow-up lane may now run concurrently with recommend() and
    # needs to see the same STOP-gated `action` fields the sequential code always gave it.
    for t in trials_copy:
        _blocked_view = {"criteria": t.get("criteria", [])}   # never the posted eligibility
        for c in t.get("criteria", []):
            trial_level_action(c, _blocked_view)

    def _run_recommend():
        # trust_attached=False: trial_intent/coverage rode in on the client body -- the sort
        # reads only the server-side sidecars (ranking.resolve_intent), so a crafted POST
        # cannot rig it. recommend classifies the need itself from the same server-side text
        # (deterministic, so it always matches the patient_need computed above). Runs on its
        # OWN deep copy: recommend() only READS trials_copy's criteria (verdict/effect/type)
        # and never mutates trials_copy itself -- the actual mutation is apply_recommendation,
        # called on the real trials_copy below, sequentially, after both lanes have joined --
        # but a deep copy makes that true by construction instead of by reading recommend()'s
        # implementation, so it stays true if recommend() ever changes.
        return recommend(patient, copy.deepcopy(trials_copy), trust_attached=False)

    def _run_followups():
        # Background follow-up check: after the answers land, does a more accurate judgment
        # need MORE questions? Generated only on a round that actually rematched (this
        # branch), skippable by the client (want_followups=false), and behind its own per-IP
        # budget because it spends 2 extra LLM calls on the metered key. A followup failure
        # (or skip) must never fail the answer round -- always returns a (questions, gaps,
        # error) triple, never raises.
        if body.get("want_followups") is False:
            return [], [], None
        if _rate_limited(client_ip, _followup_calls, FOLLOWUP_RATE_LIMIT_PER_MIN):
            return [], [], None
        if time.monotonic() - t_start >= ROUND_BUDGET_S:
            # spec step 2: never let this endpoint quietly run past Vercel's maxDuration.
            # rematch alone can already run several seconds; if the round's budget is spent
            # before this lane would even start, skip it outright instead of risking a 504 in
            # front of judges. Reused key, not a new one: followup_error is the field
            # board.html already renders immediately next to the questions (the `.funote`
            # div) -- verified by reading its fetch handler, not assumed -- so a budget skip
            # is exactly as visible to a judge as a followup failure always was. The
            # empty-affected branch's top-level "note" key is history-tab-only (verified the
            # same way); reusing it here would make a skip silently invisible in the live
            # round, the exact failure mode this budget exists to prevent. Flagged for 정원 in
            # the handoff notes as worth its own UI treatment later.
            return [], [], "시간 제한으로 이번 라운드에서는 추가 질문을 생성하지 않았습니다."
        try:
            followups, gaps = _generate_followups(
                patient_id, patient["text"], new_record, copy.deepcopy(trials_copy),
                asked_in + [q for q, _ in pairs] + [q["question"] for q in questions_in])
            return followups, gaps, None
        except Exception:
            return [], [], "추가 질문 생성에 실패했습니다. 이번 반영 결과에는 영향이 없습니다."

    if ANSWER_PARALLEL:
        # recommend() and the follow-up chain (detect_gaps -> generate_questions) do not
        # depend on each other's output -- each runs on its OWN deepcopy of trials_copy
        # (never a shared mutable trial dict across threads), and neither writes trials_copy
        # itself; the real mutations (apply_recommendation, then enrich_questions against the
        # now-decided state) happen sequentially below, after both lanes have joined.
        with ThreadPoolExecutor(max_workers=2) as ex:
            fut_recommend = ex.submit(_run_recommend)
            fut_followups = ex.submit(_run_followups)
            try:
                recs, patient_need = fut_recommend.result()
            except Exception as e:
                # The follow-up lane already started -- a running thread can't be un-started
                # -- so on a recommend() failure this concurrent version sometimes spends the
                # follow-up lane's 2 LLM calls where the old sequential code spent none (it
                # never reached this line). Accepted cost of genuinely running independent
                # work in parallel; exiting the `with` block below still waits for
                # fut_followups before this function actually returns (same total wall time),
                # its result is simply discarded here rather than fetched.
                return {"error": f"추천 호출 실패: {e}"}
            followup_questions, followup_gaps, followup_error = fut_followups.result()
    else:
        # Rollback path (ANSWER_PARALLEL=0): the original strictly-sequential order, kept only
        # as an escape hatch and for the parallel-vs-sequential identity assertion in
        # _selftest -- not a maintained second implementation.
        try:
            recs, patient_need = _run_recommend()
        except Exception as e:
            return {"error": f"추천 호출 실패: {e}"}
        followup_questions, followup_gaps, followup_error = _run_followups()

    apply_recommendation(trials_copy, recs)
    # Priority numbers for any followup questions, now that trials_copy carries the decided
    # eligibility/rank -- see _generate_followups' docstring for why this can't happen inside
    # the (possibly concurrent) follow-up lane itself.
    if followup_questions:
        # Same soft-degrade rule as the rest of the follow-up lane: a follow-up problem must
        # never discard a round whose real work (rematch + recommend) already succeeded.
        try:
            enrich_questions(followup_questions, followup_gaps, trials_copy)
        except Exception as e:  # noqa: BLE001
            followup_questions = []
            followup_error = f"추가 질문 정리 실패: {e}"

    out = {
        "verdict_changes": verdict_changes,
        "patient_need": patient_need,
        "trials": trials_copy,
        "recommendation": [
            {"nct_id": t.get("nct_id"), "rank": t.get("rank"), "eligibility": t.get("eligibility")}
            for t in trials_copy
        ],
        # priority numbers recomputed against the post-answer state (None when the client sent none)
        "questions": enrich_questions(questions_in, [], trials_copy) if questions_in else None,
        # [] = the existing questions suffice (or followups were skipped/limited)
        "followup_questions": followup_questions,
        "extended_record": new_record,
    }
    if followup_error:
        out["followup_error"] = followup_error
    return out


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            ip = (self.headers.get("x-forwarded-for", "") or "?").split(",")[0].strip()
            length = int(self.headers.get("Content-Length", 0) or 0)
            if length > MAX_BODY_BYTES:
                result = {"error": "request too large"}
            elif _rate_limited(ip):
                result = {"error": "요청이 너무 잦습니다. 잠시 후 다시 시도해 주세요."}
            else:
                raw = self.rfile.read(length) if length > 0 else b"{}"
                body = json.loads(raw.decode("utf-8"))
                result = handle(body, client_ip=ip)
        except Exception as e:
            result = {"error": str(e)}
        out = json.dumps(result, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(out)))
        self.end_headers()
        self.wfile.write(out)


# ---------------------------------------------------------------------------
# self-tests -- run: python3 api/answer.py. Pure/offline: no LLM call, no server,
# no network. The one handle() round exercised is the empty-union short-circuit,
# which by design returns before any LLM call.
# ---------------------------------------------------------------------------
def _selftest():
    failures = []

    def check(cond, msg):
        if not cond:
            failures.append(msg)

    # ---- _extract_answer_pairs: both request forms ----
    pairs, err = _extract_answer_pairs({"question": "Q1?", "answer": "A1"})
    check(err is None and pairs == [("Q1?", "A1")], "single form must yield one pair")
    _, err = _extract_answer_pairs({"question": "", "answer": "A1"})
    check(err == "invalid question", "single form keeps its exact error strings (question)")
    _, err = _extract_answer_pairs({"question": "Q1?", "answer": ""})
    check(err == "answer must be 1-600 characters", "single form keeps its exact error strings (answer)")

    batch = {"answers": [{"question": "Q1?", "answer": "A1"}, {"question": "Q2?", "answer": "A2"}],
             "question": "IGNORED", "answer": "IGNORED"}
    pairs, err = _extract_answer_pairs(batch)
    check(err is None and pairs == [("Q1?", "A1"), ("Q2?", "A2")],
          "batch form must yield every pair in order and IGNORE the single fields")
    _, err = _extract_answer_pairs({"answers": []})
    check(err is not None, "empty answers[] must be rejected")
    _, err = _extract_answer_pairs({"answers": [{"question": f"Q{i}?", "answer": "A"} for i in range(6)]})
    check(err == f"too many answers (max {MAX_BATCH_ANSWERS})", "answers[] over the cap must be rejected")
    _, err = _extract_answer_pairs({"answers": ["not-a-dict"]})
    check(err is not None, "non-object answers[] item must be rejected")
    _, err = _extract_answer_pairs({"answers": [{"question": "Q?", "answer": "x" * (MAX_ANSWER_LEN + 1)}]})
    check(err is not None, "over-long batch answer must be rejected")
    _, err = _extract_answer_pairs({"answers": [{"question": "q" * (MAX_QUESTION_LEN + 1), "answer": "A"}]})
    check(err is not None, "over-long batch question must be rejected")

    # ---- union_affected: dedupe by criterion, cap on the UNION, source attribution ----
    af = lambda t_idx, c_idx: {"nct_id": f"NCT{t_idx}", "trial_idx": t_idx, "crit_idx": c_idx,  # noqa: E731
                               "text": f"crit {t_idx}.{c_idx}", "type": "inclusion",
                               "before_verdict": "UNKNOWN"}
    a1, a2, a3 = af(0, 0), af(0, 1), af(1, 0)
    union, sources = union_affected([("Q1?", [a1, a2]), ("Q2?", [a2, a3])])
    check([(x["trial_idx"], x["crit_idx"]) for x in union] == [(0, 0), (0, 1), (1, 0)],
          "union must dedupe the shared criterion and keep first-seen order")
    check(sources[(0, 0)] == ["Q1?"] and sources[(1, 0)] == ["Q2?"],
          "a criterion linked to one question attributes to that question")
    check(sources[(0, 1)] == ["Q1?", "Q2?"],
          "a criterion linked to two questions carries both (ambiguous -> no attribution)")
    union_c, sources_c = union_affected([("Q1?", [a1, a2]), ("Q2?", [a2, a3])], cap=2)
    check(len(union_c) == 2 and (1, 0) not in sources_c,
          "cap applies to the UNION and sources are trimmed to the kept criteria")
    union_same, _ = union_affected([("Q1?", [a1]), ("Q2?", [dict(a1)])])
    check(len(union_same) == 1, "the same criterion found via two questions rematches once")

    # ---- followup dedupe normalizer (shared helper; full tests in pipeline._selftest) ----
    kept = dedupe_followups([{"question": "  ECOG 상태는?.  "}], ["ecog 상태는"])
    check(kept == [], "normalized (case/whitespace/punctuation) duplicate must be dropped")

    # ---- handle(): one offline batch round on a real patient, empty union short-circuit ----
    pid = next(p for p in sorted(KNOWN_TRIALS)
               if KNOWN_TRIALS[p] and all(len(t["criteria_texts"]) <= MAX_CRITERIA_PER_TRIAL
                                          for t in KNOWN_TRIALS[p].values()))
    trials = []
    for nct in sorted(KNOWN_TRIALS[pid]):
        texts = sorted(KNOWN_TRIALS[pid][nct]["criteria_texts"])
        trials.append({"nct_id": nct,
                       "criteria": [{"text": tx, "type": KNOWN_CRITERIA[pid][(nct, tx)],
                                     "verdict": "MET"} for tx in texts]})
    body = {"patient_id": pid, "trials": trials, "extended_record": "",
            "answers": [{"question": "완전히 무관한 질문 zzz?", "answer": "예"},
                        {"question": "역시 무관한 질문 yyy?", "answer": "아니오"}]}
    res = handle(body)
    check("error" not in res, f"offline batch round must not error, got {res.get('error')}")
    check(res.get("verdict_changes") == [] and res.get("note"),
          "no open criteria -> no changes + the plain no-link note")
    check(res.get("followup_questions") == [],
          "a round that ran no rematch must return followup_questions: [] (never generate)")
    rec = res.get("extended_record", "")
    check("추가 문진 Q: 완전히 무관한 질문 zzz? / A: 예" in rec
          and "추가 문진 Q: 역시 무관한 질문 yyy? / A: 아니오" in rec
          and rec.index("zzz") < rec.index("yyy"),
          "extended_record must grow by EVERY Q/A pair, in answer order")

    res_single = handle({"patient_id": pid, "trials": trials, "extended_record": "",
                         "question": "완전히 무관한 질문 zzz?", "answer": "예"})
    check("error" not in res_single and res_single.get("followup_questions") == [],
          "single form still works and carries the followup_questions key")

    res_bad = handle(dict(body, answers=[{"question": f"Q{i}?", "answer": "A"} for i in range(6)]))
    check(res_bad.get("error") == f"too many answers (max {MAX_BATCH_ANSWERS})",
          "handle() must reject an over-cap batch before any work")

    # The concurrency claim, actually exercised (verifier 08-20: the comment promised this
    # assertion and it did not exist). Stub the backend so a full rematch+recommend+followup
    # round runs offline, then diff the served JSON parallel vs sequential.
    import copy as _copy
    import json as _json
    import pipeline as _pl
    _real_call = _pl.call_groq
    def _stub(role, sys_prompt, user_prompt, **kw):
        if role == "reeval-matcher":
            return {"matches": [{"index": 1, "verdict": "MET", "uncertainty_type": None,
                                 "evidence": "stub", "reasoning": "stub", "evidence_meta": None}]}
        if role == "recommender":
            return {"rationales": []}
        if role == "gap-detector":
            return {"gaps": [{"field": "stub_field", "why_needed": "stub", "related_criteria": []}]}
        if role == "question-generator":
            return {"questions": [{"field": "stub_field", "question": "Stub follow-up?", "why": "stub"}]}
        return {}
    pid = next(iter(KNOWN_TRIALS))
    body_trials = []
    for nct, meta in list(KNOWN_TRIALS[pid].items()):
        crits = [{"text": txt, "type": KNOWN_CRITERIA[pid][(nct, txt)], "verdict": "UNKNOWN"}
                 for (n2, txt) in KNOWN_CRITERIA[pid] if n2 == nct]
        body_trials.append({"nct_id": nct, "title": meta["title"], "phase": meta["phase"],
                            "eligibility": "UNCERTAIN", "criteria": crits})
    q_text = body_trials[0]["criteria"][0]["text"]
    base_body = {"patient_id": pid, "answers": [{"question": q_text, "answer": "yes, documented"}],
                 "trials": body_trials, "extended_record": "", "questions": [], "asked_questions": []}
    _pl.call_groq = _stub
    globals()["rematch_affected_criteria"] = _pl.rematch_affected_criteria
    outs = {}
    try:
        for mode in (True, False):
            globals()["ANSWER_PARALLEL"] = mode
            _followup_calls.clear()
            outs[mode] = _json.dumps(handle(_copy.deepcopy(base_body), client_ip="selftest"),
                                     sort_keys=True, ensure_ascii=False, default=str)
    finally:
        _pl.call_groq = _real_call
        globals()["ANSWER_PARALLEL"] = os.environ.get("ANSWER_PARALLEL", "1") != "0"
    check(outs[True] == outs[False],
          "parallel and sequential rounds return byte-identical output on a stubbed round")

    if failures:
        print("FAIL:")
        for f in failures:
            print("  -", f)
        raise SystemExit(1)
    print(f"api/answer self-tests passed (batch cap {MAX_BATCH_ANSWERS}, "
          f"union cap {MAX_AFFECTED}, followup cap {FOLLOWUP_CAP}).")


if __name__ == "__main__":
    _selftest()
