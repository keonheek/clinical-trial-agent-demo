#!/usr/bin/env python3
"""
action_policy.py -- the uncertainty taxonomy + action-selection layer.

This is the system's stated differentiator (인수인계 v4 §4, 할일.docx corruption key):
it does NOT try to resolve every gap by asking a question. For each criterion it
could not decide from the record, it first diagnoses WHY the uncertainty exists
(the taxonomy), then maps that cause to the single safest next ACTION.

Both tables are pure data + pure functions -- deterministic, unit-testable, and
computed in code, never inferred by a model (same design rule as pipeline.EFFECT_TABLE).
A model may CLASSIFY a criterion's uncertainty type, but the type -> action mapping,
and the question-priority arithmetic, live here where they cannot be gotten backwards.

Grounded verbatim in the two handoff docs:
  - 인수인계_v4.docx §4  (불확실성 유형과 행동 정책, 10 types)
  - 할일.docx           (5 patients x 7 corruptions -> expected action key)

Run `python3 action_policy.py` to execute the self-tests.
"""

# ---------------------------------------------------------------------------
# Uncertainty taxonomy -- WHY a criterion could not be decided from the record.
# Ten mutually-exhaustive causes. UNKNOWN/UNCERTAIN is a symptom; the type is the
# diagnosis. Keys are the stable machine tokens the eval scores against; values are
# the human-readable meaning shown in the trace / UI (Korean, product-facing).
# ---------------------------------------------------------------------------
UNCERTAINTY_TYPES = {
    "MISSING":               "필요한 정보가 기록에 아예 없다",
    "STALE":                 "정보는 있으나 시점이 오래됐다",
    "INSUFFICIENT_EVIDENCE": "근거는 있으나 그 결론까지 지지하지 못한다 (CT 소견 ≠ 조직 확진)",
    "AMBIGUOUS":             "기준이나 기록의 표현이 모호하다",
    "CONFLICTING":           "두 근거가 서로 충돌한다",
    "BOUNDARY":              "수치가 컷오프 바로 부근이다",
    "CLINICAL_JUDGMENT":     "전문가 해석이 필요하다 (자동 판정 금지)",
    "NOT_APPLICABLE":        "이 환자에게 적용되지 않는다",
    "CALCULABLE":            "입력 수치는 있고 계산값만 없다",
    "DEFINITE_EXCLUSION":    "부적격이 확정됐다",
}

# The nine actions the system can take next. "재검(re-test)" is a sub-case of
# REQUEST_LATEST, not its own action (건희 [3]).
VALID_ACTIONS = {
    "ASK",             # 환자/의료진에게 직접 물어본다
    "RETRIEVE",        # 기존 기록을 검색해 찾는다
    "REQUEST_LATEST",  # 최신 검사(또는 재검)를 요청한다
    "CALCULATE",       # 도구로 계산한다 (예: Cockcroft-Gault)
    "VERIFY",          # 근거의 충분성을 확인한다 (예: 조직 확진)
    "PROTOCOL_REVIEW", # 프로토콜 원문을 재확인한다
    "ESCALATE",        # 전문가에게 이관한다
    "IGNORE",          # 이 환자에게 무관하므로 넘긴다
    "STOP",            # 부적격 확정, 추가 분석 중단
}

# uncertainty type -> (primary action, fallback action | None).
# The primary is the labelled ground-truth action (what 지우's answer key encodes);
# the fallback is the safe escalation when the primary cannot resolve it. Taken
# directly from §4's "다음 행동" column and 할일.docx's right-hand "기본 정답" column.
ACTION_TABLE = {
    "MISSING":               ("ASK",             "RETRIEVE"),
    "STALE":                 ("REQUEST_LATEST",  None),
    "INSUFFICIENT_EVIDENCE": ("VERIFY",          None),
    "AMBIGUOUS":             ("PROTOCOL_REVIEW", "ESCALATE"),
    "CONFLICTING":           ("ESCALATE",        None),
    "BOUNDARY":              ("REQUEST_LATEST",  "ESCALATE"),
    "CLINICAL_JUDGMENT":     ("ESCALATE",        None),
    "NOT_APPLICABLE":        ("IGNORE",          None),
    "CALCULABLE":            ("CALCULATE",       None),
    "DEFINITE_EXCLUSION":    ("STOP",            None),
}

VALID_UNCERTAINTY_TYPES = set(UNCERTAINTY_TYPES)


def normalize_uncertainty_type(utype):
    """Coerce a model-returned string to a valid taxonomy token, or None."""
    if not utype:
        return None
    t = str(utype).strip().upper().replace(" ", "_").replace("-", "_")
    return t if t in VALID_UNCERTAINTY_TYPES else None


def actions_for(utype):
    """(primary, fallback) actions for an uncertainty type. Pure lookup.
    Unknown/None type -> ("ESCALATE", None): if we cannot even name the cause,
    the only safe default is a human, never an automatic pass/fail."""
    t = normalize_uncertainty_type(utype)
    if t is None:
        return ("ESCALATE", None)
    return ACTION_TABLE[t]


def action_for(utype):
    """Primary next action for an uncertainty type. Pure lookup."""
    return actions_for(utype)[0]


# ---------------------------------------------------------------------------
# Question-priority arithmetic (건희 [4], for 정원's question cards).
#
# A clarifying question is worth asking in proportion to how much it moves the
# decision. We do NOT compute a counterfactual (that needs the full re-eval, and
# §15 flags it as intractable in the timeframe); we compute the three observable
# numbers the card shows, from the criteria a question would resolve:
#   affects_criteria  -- how many still-undecided criteria this question bears on
#   affects_trials    -- how many distinct trials those criteria span
#   may_change_rank   -- could resolving them re-order the recommendation?
#
# may_change_rank is true when resolving the question could flip a trial between
# eligibility classes and therefore its rank: i.e. it touches a criterion on a
# trial currently UNCERTAIN (a REVIEW criterion resolving to FAIL/PASS moves that
# trial), OR it touches ≥2 trials (cross-trial resolution can reorder them).
# Deterministic, no LLM.
# ---------------------------------------------------------------------------
_UNDECIDED = ("UNKNOWN", "UNCERTAIN")

# Generic words that co-occur in almost any criterion/question and would make the
# token-overlap fallback match everything. Dropped so the fallback keys on
# distinctive clinical terms. (Only the fallback path uses this; when a trace has
# explicit gap->related_criteria links, those are used and this never fires.)
_STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with", "without",
    "any", "has", "have", "had", "is", "are", "was", "were", "be", "been", "at", "by",
    "as", "if", "it", "its", "this", "that", "these", "those", "no", "not", "than",
    "patient", "patients", "history", "prior", "current", "currently", "known",
    "presence", "evidence", "status", "study", "trial", "criteria", "criterion",
    "what", "when", "does", "do", "did", "their", "they", "she", "he", "you", "your",
}


def _tokens(text):
    import re
    toks = re.findall(r"[a-z0-9%.]+", (text or "").lower())
    return {t for t in toks if t not in _STOPWORDS and (len(t) >= 3 or any(ch.isdigit() for ch in t))}


def _affected_criteria(question, gaps_by_field, trials):
    """Locate the still-undecided criteria a question bears on.

    Prefers the exact gap->related_criteria links (present on freshly-generated
    traces); falls back to token overlap between the question and each gap's
    field/why_needed (the same heuristic live_server.find_affected already uses),
    so this also works on older traces that never stored gaps.
    Returns a list of (trial, criterion) pairs.
    """
    target_texts = set()
    field = question.get("field")
    if field and field in gaps_by_field:
        target_texts.update(gaps_by_field[field].get("related_criteria", []))
    if not target_texts:
        qtok = _tokens(question.get("question", ""))
        for g in gaps_by_field.values():
            gtok = _tokens(g.get("field", "") + " " + g.get("why_needed", ""))
            if qtok & gtok:
                target_texts.update(g.get("related_criteria", []))

    pairs = []
    for t in trials:
        for c in t.get("criteria", []):
            if c.get("verdict") not in _UNDECIDED:
                continue
            # With explicit links, restrict to them; without any links at all,
            # fall back to token overlap directly against the criterion text so a
            # question still surfaces its criteria on gap-less traces.
            if target_texts:
                if c.get("text") not in target_texts:
                    continue
            else:
                if not (_tokens(question.get("question", "")) & _tokens(c.get("text", ""))):
                    continue
            pairs.append((t, c))
    return pairs


def priority_numbers(question, gaps, trials):
    """The three card numbers for one question. Pure function of the trace."""
    gaps_by_field = {g["field"]: g for g in (gaps or [])}
    pairs = _affected_criteria(question, gaps_by_field, trials)

    affected_trials = {t["nct_id"] for t, _ in pairs}
    n_criteria = len(pairs)
    n_trials = len(affected_trials)

    touches_uncertain_trial = any(
        t.get("eligibility") == "UNCERTAIN" for t, _ in pairs
    )
    may_change_rank = bool(pairs) and (touches_uncertain_trial or n_trials >= 2)

    return {
        "affects_criteria": n_criteria,
        "affects_trials": n_trials,
        "may_change_rank": may_change_rank,
    }


def enrich_questions(questions, gaps, trials):
    """Attach affects_trials / affects_criteria / may_change_rank to each question.
    Questions are returned sorted most-impactful first (the order the cards show).
    Mutates and returns the list."""
    for q in questions or []:
        q.update(priority_numbers(q, gaps, trials))
    (questions or []).sort(
        key=lambda q: (q.get("may_change_rank", False),
                       q.get("affects_trials", 0),
                       q.get("affects_criteria", 0)),
        reverse=True,
    )
    return questions


# ---------------------------------------------------------------------------
# self-tests -- run: python3 action_policy.py
# ---------------------------------------------------------------------------
def _selftest():
    failures = []

    def check(cond, msg):
        if not cond:
            failures.append(msg)

    # every taxonomy type has an action row, and every action it names is valid
    check(set(ACTION_TABLE) == VALID_UNCERTAINTY_TYPES,
          "ACTION_TABLE keys must exactly cover the taxonomy")
    for utype, (primary, fallback) in ACTION_TABLE.items():
        check(primary in VALID_ACTIONS, f"{utype}: primary {primary} not a valid action")
        check(fallback is None or fallback in VALID_ACTIONS,
              f"{utype}: fallback {fallback} not a valid action")

    # the corruption -> action key from 할일.docx must hold exactly
    doc_key = {
        "MISSING": "ASK",
        "STALE": "REQUEST_LATEST",
        "BOUNDARY": "REQUEST_LATEST",
        "AMBIGUOUS": "PROTOCOL_REVIEW",
        "CONFLICTING": "ESCALATE",
        "CLINICAL_JUDGMENT": "ESCALATE",
    }
    for utype, expected in doc_key.items():
        check(action_for(utype) == expected,
              f"{utype}: expected primary {expected}, got {action_for(utype)}")

    # combination-danger case (심부전+CKD+drug) is CONFLICTING/ESCALATE class -> never auto pass
    check(action_for("CLINICAL_JUDGMENT") == "ESCALATE", "clinical judgment must escalate")
    # unknown/None type is fail-safe to a human, never a silent pass
    check(action_for("nonsense") == "ESCALATE", "unknown type must fail safe to ESCALATE")
    check(action_for(None) == "ESCALATE", "None type must fail safe to ESCALATE")
    # normalization tolerates model formatting drift
    check(normalize_uncertainty_type("clinical judgment") == "CLINICAL_JUDGMENT",
          "normalize should map 'clinical judgment' -> CLINICAL_JUDGMENT")
    check(normalize_uncertainty_type("stale ") == "STALE", "normalize should trim/upper")

    # DEFINITE_EXCLUSION halts, NOT_APPLICABLE ignores -- these must not become questions
    check(action_for("DEFINITE_EXCLUSION") == "STOP", "definite exclusion must STOP")
    check(action_for("NOT_APPLICABLE") == "IGNORE", "not-applicable must IGNORE")

    # ---- question-priority arithmetic ----
    trials = [
        {"nct_id": "NCT1", "eligibility": "UNCERTAIN", "criteria": [
            {"text": "Adequate renal function", "verdict": "UNKNOWN"},
            {"text": "ECOG 0-1", "verdict": "MET"},
        ]},
        {"nct_id": "NCT2", "eligibility": "ELIGIBLE", "criteria": [
            {"text": "Adequate renal function", "verdict": "UNKNOWN"},
        ]},
    ]
    gaps = [{"field": "renal", "why_needed": "kidney labs",
             "related_criteria": ["Adequate renal function"]}]
    q = {"field": "renal", "question": "What is the patient's creatinine clearance?"}
    nums = priority_numbers(q, gaps, trials)
    check(nums["affects_criteria"] == 2, f"expected 2 criteria, got {nums['affects_criteria']}")
    check(nums["affects_trials"] == 2, f"expected 2 trials, got {nums['affects_trials']}")
    check(nums["may_change_rank"] is True, "renal gap spans 2 trials -> may_change_rank")

    # a question that resolves nothing undecided scores zero and cannot change rank
    q_none = {"field": "none", "question": "totally unrelated xyzzy"}
    nums0 = priority_numbers(q_none, [], trials)
    check(nums0["affects_criteria"] == 0 and nums0["may_change_rank"] is False,
          "unrelated question must be zero-impact")

    # token-overlap fallback works with no gap links at all
    q_fb = {"question": "adequate renal function labs?"}
    nums_fb = priority_numbers(q_fb, [], trials)
    check(nums_fb["affects_criteria"] >= 1, "fallback overlap should find the renal criterion")

    if failures:
        print("FAIL:")
        for f in failures:
            print("  -", f)
        raise SystemExit(1)
    print(f"action_policy self-tests passed "
          f"({len(UNCERTAINTY_TYPES)} uncertainty types, {len(VALID_ACTIONS)} actions).")


if __name__ == "__main__":
    _selftest()
