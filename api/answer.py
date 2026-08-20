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
import json
import os
import sys
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
MAX_TRIALS = 6                   # traces hold 4 per patient
MAX_CRITERIA_PER_TRIAL = 16      # traces max is 13
MAX_QUESTIONS = 12               # traces hold <= 5 per patient
MAX_BATCH_ANSWERS = 5            # one 반영 click covers at most 5 question cards
MAX_ASKED_QUESTIONS = 50         # dedupe list the client resends; text only, never a prompt
FOLLOWUP_CAP = 3                 # same bound as the base question generator
RATE_LIMIT_PER_MIN = 10          # per client IP, per warm instance (cheap brake, not a wall)
FOLLOWUP_RATE_LIMIT_PER_MIN = 4  # follow-up generation adds 2 LLM calls/round on the metered
                                 # key -- its own tighter per-IP budget, same mechanism

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
from action_policy import _tokens  # noqa: E402


def find_affected(question_text, trials):
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
    qtok = _tokens(question_text)
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
    FOLLOWUP_CAP, stamped followup=True, and enriched with the three priority numbers.
    Returns [] when the existing questions suffice (no gaps, or every candidate is a repeat).
    """
    all_criteria_flat = [
        {"nct_id": t.get("nct_id"), "text": c.get("text", ""), "verdict": c.get("verdict"),
         "action": c.get("action"), "effect": c.get("effect")}
        for t in trials_copy for c in t.get("criteria", [])
    ]
    patient_ext = {"patient_id": patient_id, "text": (vignette + "\n" + new_record).strip()}
    gaps = detect_gaps(patient_ext, all_criteria_flat)
    if not gaps:
        return []
    followups = dedupe_followups(generate_questions(patient_ext, gaps), asked_texts,
                                 cap=FOLLOWUP_CAP)
    for q in followups:
        q["followup"] = True
    return enrich_questions(followups, gaps, trials_copy)


def handle(body, client_ip="?"):
    patient_id = str(body.get("patient_id", "")).strip()
    trials = body.get("trials")
    extended_record = str(body.get("extended_record", "")).strip()

    if patient_id not in KNOWN_IDS:
        return {"error": "unknown patient_id"}
    pairs, pairs_error = _extract_answer_pairs(body)
    if pairs_error:
        return {"error": pairs_error}
    if not isinstance(trials, list) or not trials:
        return {"error": "trials array required"}
    trials_error = _validate_trials(patient_id, trials)
    if trials_error:
        return {"error": trials_error}

    # never trust the client for the vignette itself -- only the fixed 10 patients exist here.
    patient = {"patient_id": patient_id, "text": PATIENTS_BY_ID[patient_id]["text"]}
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
    questions_in = [{"field": str(q.get("field", ""))[:120], "question": str(q.get("question", ""))[:MAX_QUESTION_LEN]}
                    for q in questions_in[:MAX_QUESTIONS] if isinstance(q, dict) and q.get("question")]
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
    affected, sources = union_affected([(q, find_affected(q, trials_copy)) for q, _ in pairs])
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

    try:
        # trust_attached=False: trial_intent/coverage rode in on the client body -- the sort reads
        # only the server-side sidecars (ranking.resolve_intent), so a crafted POST cannot rig it.
        # recommend classifies the need itself from the same server-side text (deterministic, so
        # it always matches the patient_need computed above).
        recs, patient_need = recommend(patient, trials_copy, trust_attached=False)
    except Exception as e:
        return {"error": f"추천 호출 실패: {e}"}

    apply_recommendation(trials_copy, recs)
    # Trial-level action context: once a trial carries a hard FAIL, asking about its remaining
    # undecided criteria is moot -> STOP (same class of rule as effect_of; no model involved).
    for t in trials_copy:
        for c in t.get("criteria", []):
            trial_level_action(c, t)

    # Background follow-up check: after the answers land, does a more accurate judgment need
    # MORE questions? Generated only on a round that actually rematched (this branch), skippable
    # by the client (want_followups=false), and behind its own per-IP budget because it spends
    # 2 extra LLM calls on the metered key. A followup failure must never fail the answer round.
    followup_questions, followup_error = [], None
    if body.get("want_followups") is not False and not _rate_limited(
            client_ip, _followup_calls, FOLLOWUP_RATE_LIMIT_PER_MIN):
        try:
            followup_questions = _generate_followups(
                patient_id, patient["text"], new_record, trials_copy,
                asked_in + [q for q, _ in pairs] + [q["question"] for q in questions_in])
        except Exception:
            followup_questions = []
            followup_error = "추가 질문 생성에 실패했습니다. 이번 반영 결과에는 영향이 없습니다."

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

    if failures:
        print("FAIL:")
        for f in failures:
            print("  -", f)
        raise SystemExit(1)
    print(f"api/answer self-tests passed (batch cap {MAX_BATCH_ANSWERS}, "
          f"union cap {MAX_AFFECTED}, followup cap {FOLLOWUP_CAP}).")


if __name__ == "__main__":
    _selftest()
