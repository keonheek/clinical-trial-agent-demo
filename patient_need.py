#!/usr/bin/env python3
"""
patient_need.py -- the "need reader" (Q0 of the need-first logic tree, his 08-18 call).

VISION (박호진 email #2 + Keonhee 08-18 step-back): trials exist to help patients who need
help -> recommendation must start from the PATIENT'S NEED, not only trial properties. Before
this module the pipeline only asked "can they join" (decide_eligibility) and "how well
characterized is the trial" (ranking.py); it never asked "does this trial serve what THIS
patient needs". This module answers that middle question.

Pure stdlib, deterministic, NO LLM client imports -- same rule as action_policy.py and ranking.py (bundled into the
serverless api/ handlers, zero-LLM). Rule-based keyword heuristic, same pattern as build_trial_intent.py (that module
classifies the TRIAL's intent; this one classifies the PATIENT's need -- the vocabularies meet in HELP_MATRIX).
Run `python3 patient_need.py` for the self-tests.

classify_patient_need(text) -> one of four needs, from the vignette alone:
  treatment  (치료)     -- needs an intervention to change the course of illness
  diagnosis  (진단 확정) -- needs confirmation before anything else can be decided (a
                           workup/confirmation step is the blocker)
  monitoring (추적관찰) -- needs a known, stable condition tracked over time
  comfort    (증상 완화) -- needs symptom relief / quality of life, not a cure

helps(need, trial_intent) -> does a trial of a given trial_intent (build_trial_intent.py's
therapeutic | supportive | care_delivery | observational) serve that need? 2 = direct match,
1 = partial, 0 = does not (or intent unknown, so nothing is lifted on its account).

RULE PRIORITY (first match wins; sets can overlap, so a hit lower down must never override a hit higher up -- same
reasoning as build_trial_intent.PRIORITY):
  1. COMFORT    -- palliative/hospice/comfort-only language. Checked FIRST, a safety property: goals-of-care-comfort
                   must never be pointed at a disease-modifying trial because some other symptom word also fired.
  2. MONITORING -- chronic-stable/follow-up/surveillance language. A known, stable, tracked condition is not the
                   same need as a new active presentation.
  3. DIAGNOSIS  -- confirmation is the blocker: explicit suspicion language, OR an imaging-detected mass/lesion with
                   no tissue-confirmation language in the text. The tissue-confirmed guard matters: a positive
                   biopsy/lab result means confirmation is already done, so this must not fire on "mass" alone.
  4. TREATMENT (explicit) -- active symptomatic presentation, no language suggesting a treatment is already under
                   way. High confidence.
  5. DEFAULT    -- nothing fired -> treatment, LOW confidence. A patient matching none of our keyword sets is more
                   likely an unanticipated presentation style than one who wants to be watched, not helped.
                   Under-triaging a real treatment need to "just monitoring" silently hides a trial from someone who
                   needed it; the reverse (one extra trial surfaced to a stable patient) is cheap by comparison.
                   LOW confidence flags it for human review either way.

HELP MATRIX: each cell is reasoned out at its definition below. A low-confidence or missing
trial_intent falls to the WORST cell in the need's row -- mirrors ranking.fit_rank's rule
that a hedged guess must never lift a trial above a confirmed fact.

Not touched here: eligibility (pipeline.decide_eligibility), ranking order (ranking.py), the uncertainty/action
taxonomy (action_policy.py) -- this only feeds those layers an input.
"""
import json
import os
import sys

NEED_VERSION = "2026-08-18"
VALID_NEEDS = {"treatment", "diagnosis", "monitoring", "comfort"}
NEED_KO = {"treatment": "치료", "diagnosis": "진단 확정", "monitoring": "추적관찰",
           "comfort": "증상 완화"}
# Rule 1 -- comfort. Checked first (safety property, see module docstring).
COMFORT_KEYWORDS = [
    "palliative", "hospice", "comfort care", "comfort measures", "comfort-focused", "end-of-life", "end of life",
    "terminal diagnosis", "goals of care shifted to comfort", "symptom relief only", "no further disease-directed treatment",
    "focus on comfort", "focus on quality of life", "wish to focus on comfort", "comfort and quality of life",
]

# Rule 2 -- monitoring. A known, stable, already-characterized condition.
# "stable" is anchored to affirmative phrases ("is stable", "remains stable", "stable on") --
# a bare substring would match "unstable" and flip the most acute patients to monitoring
# (verifier-caught 08-19, same defect class as the bare-"biopsy" fix below). "known history of"
# and bare "follow-up" were dropped: they are routine comorbidity/context lines that shadowed
# acute presentations (e.g. "presents with acute pain. Known history of hypertension").
MONITORING_KEYWORDS = [
    "is stable", "remains stable", "clinically stable", "stable on", "well-controlled", "well controlled",
    "surveillance", "routine monitoring", "asymptomatic", "in remission",
    "routine check-up", "routine checkup", "annual visit", "for monitoring",
    "long-term follow-up", "long-term research", "long-term outcomes", "interested in contributing",
]

# Rule 3 -- diagnosis. Confirmation is the blocking step.
DIAGNOSIS_SUSPECTED_PHRASES = [
    "suspected", "concerning for", "rule out", "presumed", "possible diagnosis of", "query diagnosis",
    "differential includes", "worrisome for",
]
# Requires an imaging VERB next to the finding -- "reveals a mass" is an imaging read;
# "palpable mass" (physical exam) is not, and must not trip this rule.
IMAGING_UNCONFIRMED_PHRASES = [
    "reveals a mass", "shows a mass", "demonstrates a mass", "reveals a lesion", "shows a lesion",
    "reveals a nodule", "shows a nodule", "mass on imaging", "lesion on imaging", "nodule on imaging", "incidental mass",
    "found to have a", "nodule on ultrasound", "nodule on neck ultrasound", "mass on ultrasound",
    "no biopsy has been performed",
]
# Overrides IMAGING_UNCONFIRMED_PHRASES when present. Deliberately NOT a bare "biopsy" token:
# "no prior biopsy" contains the word but means the opposite -- every phrase is anchored to an affirmative result.
TISSUE_CONFIRMED_PHRASES = [
    "biopsy confirms", "biopsy-proven", "biopsy proven", "biopsy revealed", "biopsy showed", "biopsy shows",
    "confirmed by biopsy", "positive biopsy", "pathology confirms", "pathology-confirmed", "histology confirms",
    "histologically confirmed", "tissue diagnosis", "test is positive", "test was positive",
]

# Rule 4 -- treatment (explicit). Active symptomatic presentation, nothing established yet.
ACTIVE_SYMPTOM_PHRASES = [
    "presents with", "presenting with", "sudden onset", "acute onset", "severe pain", "acute ", "new onset", "new-onset",
    "remains symptomatic", "uncontrolled", "poorly controlled", "flare", "worsening", "progressing", "refractory",
    "despite", "history of", "labs show", "urinalysis shows", "emergency visit",
]
ESTABLISHED_TREATMENT_PHRASES = [
    "currently receiving", "currently on", "already started", "post-treatment", "maintenance therapy",
    "history of treatment with", "status post", "s/p ",
]

RULE_KO = ("완화 목적 언급 → 증상 완화 | 안정·추적 관찰 언급 → 추적관찰 | "
           "확진 전 단계(의심 소견/영상 소견만 있고 조직 확진 없음) → 진단 확정 | "
           "급성 증상 호소이고 기존 치료 언급 없음 → 치료 | 아무 규칙도 안 걸리면 → 치료(확신 낮음)")


def _norm(text):
    return (text or "").lower()


def _find_any(haystack, phrases):
    return [p for p in phrases if p in haystack]


def classify_patient_need(vignette_text, extraction_fields=None):
    """Deterministic need classification from the vignette text alone (extraction_fields is
    accepted for forward-compat with structured extraction but not yet consulted -- keyword
    text is the only signal today). Returns {need, need_ko, confidence, reasons}; reasons are
    plain-language Korean strings, each naming the literal evidence phrase (quoted from the
    vignette) that fired -- the plain-word label the UI rule requires, paired with the raw
    evidence for auditability."""
    text = _norm(vignette_text)

    hits = _find_any(text, COMFORT_KEYWORDS)
    if hits:
        return {"need": "comfort", "need_ko": NEED_KO["comfort"], "confidence": "high",
                "reasons": [f"완화 목적 기술 있음 → 근치적 치료가 아닌 증상 완화 요구로 분류"
                            f" (근거 문구 '{hits[0]}')"]}

    hits = _find_any(text, MONITORING_KEYWORDS)
    if hits:
        # An acute presentation in the same vignette outranks incidental stable/monitoring
        # context -- the presenting problem defines the need, not the comorbidity line.
        if _find_any(text, ACTIVE_SYMPTOM_PHRASES):
            return {"need": "treatment", "need_ko": NEED_KO["treatment"], "confidence": "low",
                    "reasons": [f"추적관찰 기술과 활동성 증상 동시 존재 → 주호소 우선하여 치료 요구로 분류"
                                f" (확신 낮음, 검토 권장; 근거 문구 '{hits[0]}')"]}
        return {"need": "monitoring", "need_ko": NEED_KO["monitoring"], "confidence": "high",
                "reasons": [f"기지 질환의 경과 관찰 기술 있음 → 신규 개입보다 추적관찰 요구로 분류"
                            f" (근거 문구 '{hits[0]}')"]}

    suspected = _find_any(text, DIAGNOSIS_SUSPECTED_PHRASES)
    imaging = _find_any(text, IMAGING_UNCONFIRMED_PHRASES)
    tissue = _find_any(text, TISSUE_CONFIRMED_PHRASES)
    if suspected or (imaging and not tissue):
        phrase = (suspected or imaging)[0]
        return {"need": "diagnosis", "need_ko": NEED_KO["diagnosis"], "confidence": "high",
                "reasons": [f"조직학적 확진 근거 없이 의심 소견·영상 소견만 존재 → 진단 확정 선행 요구로"
                            f" 분류 (근거 문구 '{phrase}')"]}

    active = _find_any(text, ACTIVE_SYMPTOM_PHRASES)
    established = _find_any(text, ESTABLISHED_TREATMENT_PHRASES)
    if active and not established:
        return {"need": "treatment", "need_ko": NEED_KO["treatment"], "confidence": "high",
                "reasons": [f"활동성 증상 있고 현행 치료 기록 없음 → 치료적 개입 요구로 분류"
                            f" (근거 문구 '{active[0]}')"]}

    return {"need": "treatment", "need_ko": NEED_KO["treatment"], "confidence": "low",
            "reasons": ["증상 완화·추적관찰·진단 확정 중 해당 기술 없음 → 급성 제시 환자는 개입 요구"
                        " 가능성이 높다고 보아 기본값 치료 요구로 분류 (확신 낮음, 검토 권장)"]}


# ---------------------------------------------------------------------------
# HELP MATRIX -- helps(need, trial_intent) -> 2 | 1 | 0. trial_intent vocabulary comes from
# build_trial_intent.py: therapeutic, supportive, care_delivery, observational.
# ---------------------------------------------------------------------------
HELP_MATRIX = {
    # treatment: an intervention meant to change the disease course is the direct match (2).
    # supportive helps symptoms while disease continues -- partial (1). care_delivery /
    # observational change nothing about the disease for this patient (0).
    "treatment": {"therapeutic": 2, "supportive": 1, "care_delivery": 0, "observational": 0},
    # diagnosis: nothing here CHANGES the disease course, so therapeutic is only partial (its
    # own screening/staging can incidentally answer the confirmation question -- 1).
    # observational registries / natural-history / imaging studies are explicitly built to
    # characterize what a finding IS (build_trial_intent's own OBSERVATIONAL_KEYWORDS list
    # includes "imaging study", "biomarker study") -- the direct match here (2), unlike every
    # other row. supportive / care_delivery confirm nothing (0).
    "diagnosis": {"therapeutic": 1, "supportive": 0, "care_delivery": 0, "observational": 2},
    # monitoring: the patient wants a known, stable condition tracked, not changed --
    # observational (registries/surveillance/natural history) is the direct match (2).
    # care_delivery (navigation, adherence, coordination) also serves an already-diagnosed,
    # tracked patient -- partial (1). therapeutic asks a stable patient to accept new-
    # intervention risk for a course that isn't worsening (0). supportive targets symptom
    # burden a monitoring-only patient isn't reporting (0).
    "monitoring": {"therapeutic": 0, "supportive": 0, "care_delivery": 1, "observational": 2},
    # comfort: supportive (palliative/QoL/symptom-management) is the direct, definitional
    # match (2). care_delivery can be palliative-care navigation -- partial, not certain from
    # the label alone (1). therapeutic asks a comfort-focused patient to accept
    # disease-directed risk goals-of-care already moved past (0). observational changes
    # nothing about how the patient feels today (0).
    "comfort": {"therapeutic": 0, "supportive": 2, "care_delivery": 1, "observational": 0},
}

HELP_LABEL_KO = {2: "도움 됨", 1: "부분적", 0: "참고용"}


def helps(need, trial_intent):
    """need: one of VALID_NEEDS. trial_intent: {"intent": str, "confidence": "high"|"low"}, a
    bare intent string, or None/anything else. A missing or low-confidence intent falls to the
    WORST cell in the need's row -- matches ranking.fit_rank's rule that a hedged guess must
    never lift a trial (every row's worst cell happens to be 0, so no need needs special-
    casing, but the lookup is written generically rather than hardcoding that)."""
    row = HELP_MATRIX.get(need)
    if row is None:
        return 0
    intent_name = None
    if isinstance(trial_intent, dict):
        if str(trial_intent.get("confidence", "low")).lower() == "high":
            intent_name = trial_intent.get("intent")
    elif isinstance(trial_intent, str):
        intent_name = trial_intent
    if intent_name not in row:
        return min(row.values())
    return row[intent_name]


def help_label_ko(score):
    return HELP_LABEL_KO.get(score, HELP_LABEL_KO[0])


# ---------------------------------------------------------------------------
# self-tests -- run: python3 patient_need.py
# ---------------------------------------------------------------------------
def _selftest():
    ok = True

    def check(cond, msg):
        nonlocal ok
        print(("  PASS " if cond else "  FAIL ") + msg)
        ok = ok and cond

    # one synthetic vignette per rule branch, in priority order
    cases = [
        ("Patient with metastatic cancer, goals of care shifted to comfort, family requests "
         "hospice.", "comfort", "high", "comfort: hospice language"),
        ("A 60-year-old woman with well-controlled hypertension presents for routine "
         "follow-up; asymptomatic, stable on current regimen.", "monitoring", "high",
         "monitoring: stable/follow-up language"),
        ("A 50-year-old man with a lung nodule, suspected malignancy, referred for further "
         "workup.", "diagnosis", "high", "diagnosis: explicit 'suspected' language"),
        ("CT urography reveals a mass in the bladder wall; no prior biopsy.", "diagnosis",
         "high", "diagnosis: imaging mass with no tissue confirmation"),
        ("A 54-year-old man presents with severe epigastric pain radiating to the back, "
         "nausea, and vomiting. Labs reveal markedly elevated lipase.", "treatment", "high",
         "treatment: active symptomatic presentation, nothing established"),
        ("A patient was seen in clinic today.", "treatment", "low",
         "default: no rule fires -> treatment, LOW confidence"),
    ]
    for text, want_need, want_conf, msg in cases:
        r = classify_patient_need(text)
        check(r["need"] == want_need and r["confidence"] == want_conf and r["reasons"], msg)

    # guards: phrases that must NOT trip a rule despite a surface keyword match
    for text, want, msg in [
        ("Imaging reveals a mass; biopsy confirms adenocarcinoma.",
         lambda r: r["need"] != "diagnosis", "named biopsy confirmation blocks the imaging rule"),
        ("A 3-month-old infant presents with projectile vomiting and a palpable "
         "olive-shaped mass in the epigastrium.", lambda r: r["need"] == "treatment",
         "'palpable mass' (exam, not imaging) does not trip the diagnosis rule"),
        ("Patient presents with fatigue; currently receiving chemotherapy for known diagnosis.",
         lambda r: r["need"] != "treatment" or r["confidence"] == "low",
         "'currently receiving' blocks the high-confidence treatment rule"),
    ]:
        check(want(classify_patient_need(text)), f"guard: {msg}")

    check(all(NEED_KO[n] for n in VALID_NEEDS), "every need has a non-empty Korean label")

    # HELP_MATRIX sanity: only 0/1/2, every row covers all four intents, has >=1 direct match
    intent_tokens = {"therapeutic", "supportive", "care_delivery", "observational"}
    for need, row in HELP_MATRIX.items():
        check(set(row.values()) <= {0, 1, 2} and 2 in row.values() and set(row.keys()) == intent_tokens,
              f"HELP_MATRIX[{need}] scores only 0/1/2, has a direct match, covers all four intents")
    check(set(HELP_MATRIX.keys()) == VALID_NEEDS, "HELP_MATRIX has exactly the four needs")

    hi = lambda i: {"intent": i, "confidence": "high"}  # noqa: E731
    for need, intent, want, msg in [
        ("treatment", hi("therapeutic"), 2, "high-confidence therapeutic for treatment scores 2"),
        ("treatment", {"intent": "therapeutic", "confidence": "low"}, 0,
         "low-confidence intent falls to worst cell"),
        ("treatment", None, 0, "missing intent falls to worst cell"),
        ("treatment", "therapeutic", 2, "bare high-trust intent string works"),
        ("diagnosis", hi("observational"), 2, "observational is the direct match for diagnosis"),
        ("comfort", hi("supportive"), 2, "supportive is the direct match for comfort"),
        ("monitoring", hi("observational"), 2, "observational is the direct match for monitoring"),
        ("not_a_need", hi("therapeutic"), 0, "unknown need scores 0 rather than raising"),
    ]:
        check(helps(need, intent) == want, f"helps(): {msg}")
    check(help_label_ko(2) == "도움 됨" and help_label_ko(1) == "부분적" and help_label_ko(0) == "참고용",
          "help_label_ko renders all three scores")

    # deterministic + valid on the frozen demo traces (read-only; no hardcoded expected needs)
    traces_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "traces.json")
    if os.path.exists(traces_path):
        with open(traces_path, encoding="utf-8") as f:
            traces = json.load(f)
        r1 = [classify_patient_need(t["patient_text"])["need"] for t in traces]
        r2 = [classify_patient_need(t["patient_text"])["need"] for t in traces]
        check(r1 == r2 and len(r1) == 10 and all(n in VALID_NEEDS for n in r1),
              "deterministic + valid need on all 10 frozen demo patients")

    # verifier-caught regressions (08-19): substring negation, acute-shadowing, matrix-comment parity
    r = classify_patient_need("presents with crushing chest pain; ECG shows changes consistent with unstable angina")
    check(r["need"] == "treatment", f"'unstable' must never fire monitoring (got {r['need']})")
    r = classify_patient_need("Routine surveillance visit was planned; patient presents today with new-onset severe headache")
    check(r["need"] == "treatment", f"acute presentation outranks incidental monitoring context (got {r['need']})")
    r = classify_patient_need("He is clinically stable on metformin and attends routine monitoring visits.")
    check(r["need"] == "monitoring", f"anchored stable phrase still fires monitoring (got {r['need']})")
    r = classify_patient_need("He and his family wish to focus on comfort and quality of life.")
    check(r["need"] == "comfort", f"goals-of-care comfort wording fires comfort (got {r['need']})")
    r = classify_patient_need("She is found to have a 2 cm thyroid nodule on neck ultrasound. No biopsy has been performed yet.")
    check(r["need"] == "diagnosis", f"imaging finding without tissue confirmation fires diagnosis (got {r['need']})")
    check(HELP_MATRIX["monitoring"]["supportive"] == 0, "monitoring x supportive matches its documented reasoning (0)")

    print("patient_need selftest:", "ALL PASS" if ok else "FAILURES")
    return ok


if __name__ == "__main__":
    sys.exit(0 if _selftest() else 1)
