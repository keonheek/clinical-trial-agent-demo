#!/usr/bin/env python3
"""
pipeline.py — 6-role multi-agent clinical trial matching pipeline.

SKKU Healthcare Agentic AI Challenge 2026 — Interactive Clinical Trial Recommendation.

Roles (each = one independent Groq LLM call, own system prompt):
  (a) criteria-parser    trial eligibility text  -> structured criteria list
  (b) patient-extractor  patient vignette        -> structured fields w/ verbatim evidence
  (c) matcher             criteria x patient      -> verdict + evidence + reasoning per criterion
  (d) gap-detector        matched criteria        -> missing-info gaps (UNKNOWN due to no data)
  (e) question-generator  gaps                    -> <=3 clarifying questions
  (f) recommender         trial matches            -> ranked trials + overall eligibility

LLM backend is switchable via LLM_BACKEND env var:
    anthropic (default) — paid Anthropic API, Haiku via ANTHROPIC_NEW_KEY (anthropic_client.py);
                       the accepted $0-rule exception for this project
    ollama           — local qwen3.6:35b via Ollama (ollama_client.py); $0, no key, no quota
    groq             — Groq free tier (groq_client.py); daily quota crawls under load
    claude           — headless `claude -p` on the local subscription (claude_client.py)
Every call is cached to disk in cache/ (keyed per backend model), so re-running this
script after the first successful build makes ZERO new LLM calls. Switching backends does
NOT reuse another backend's answers: the model name is part of the cache key.

Run:
    python3 pipeline.py
Writes:
    traces.json   (plain JSON)
    traces.js     (window.TRACES = [...]; consumed by demo.html)
"""
import json
import os
import re
import sys
import time

from action_policy import (
    normalize_uncertainty_type,
    action_for,
    enrich_questions,
    is_question_worthy,
    UNCERTAINTY_TYPES,
)
from evidence import assess_evidence

_BACKEND = os.environ.get("LLM_BACKEND", "anthropic")
if _BACKEND == "ollama":
    from ollama_client import call_llm as _call_backend, stats, DEFAULT_MODEL
elif _BACKEND == "groq":
    from groq_client import call_groq as _call_backend, stats, DEFAULT_MODEL
elif _BACKEND == "anthropic":
    from anthropic_client import call_llm as _call_backend, stats, DEFAULT_MODEL
else:
    from claude_client import call_llm as _call_backend, stats, DEFAULT_MODEL

# Which model the calls actually use. Starts at the backend's default and can be changed
# at runtime (the local UI's model picker) without restarting the process. The cache key
# already includes the model, so switching never returns another model's cached answer.
ACTIVE_MODEL = DEFAULT_MODEL


def set_active_model(model):
    """Point subsequent LLM calls at `model`. Returns the value actually set."""
    global ACTIVE_MODEL
    ACTIVE_MODEL = model or DEFAULT_MODEL
    return ACTIVE_MODEL


def call_groq(role, system_prompt, user_prompt, model=None, **kwargs):
    """Single funnel for every pipeline LLM call, so the active model applies everywhere."""
    return _call_backend(role, system_prompt, user_prompt,
                         model=model or ACTIVE_MODEL, **kwargs)

HERE = os.path.dirname(os.path.abspath(__file__))
TRIALS_PER_PATIENT = 4
MAX_REASONING_WORDS = 25
MAX_RATIONALE_WORDS = 30
MAX_EXTENDED_RECORD_WORDS = 180

VALID_VERDICTS = {"MET", "NOT_MET", "UNCERTAIN", "UNKNOWN"}
VALID_ELIGIBILITY = {"ELIGIBLE", "INELIGIBLE", "UNCERTAIN"}
VALID_EFFECTS = {"PASS", "FAIL", "REVIEW"}

# Two-layer verdict model.
#
# Layer 1 (verdict): is the criterion STATEMENT true of this patient? This is a plain
# reading-comprehension question, identical for inclusion and exclusion criteria, and is what
# the matcher LLM is asked. MET = the statement describes the patient.
#
# Layer 2 (effect): does that make the patient pass or fail this trial? This depends on whether
# the criterion is inclusion or exclusion, and is pure logic -- so it is computed here in code,
# never inferred by a model. An exclusion criterion the patient MEETS excludes them.
#
# Before this split, "MET" silently meant "statement is true" to the human labelers and
# "patient passes" to the matcher, and the recommender prompt used both readings in adjacent
# sentences. Exclusion criteria were therefore scored inverted. See EVAL-NOTES.md.
EFFECT_TABLE = {
    ("inclusion", "MET"): "PASS",
    ("inclusion", "NOT_MET"): "FAIL",
    ("exclusion", "MET"): "FAIL",
    ("exclusion", "NOT_MET"): "PASS",
}


def effect_of(criterion_type, verdict):
    """Map (criterion type, criterion-truth verdict) -> eligibility effect. Pure function."""
    return EFFECT_TABLE.get((criterion_type, verdict), "REVIEW")


def truncate_words(text, n):
    words = text.split()
    if len(words) <= n:
        return text
    return " ".join(words[:n])


_CRITERION_LINE = re.compile(r"^\s*(?:[*\-•]|\d+[.)])\s+\S")


def estimate_raw_criteria_count(raw_text):
    """Deterministic count of criterion-like lines (bullets / numbered items) in a trial's raw
    eligibility text. Zero LLM calls. Used to expose parsing COVERAGE -- how much of the trial's
    protocol the parsed criteria actually represent -- so a trial that merely got read less can't
    silently present as a more certain match (see RECOMMENDATION-DEFINITION.md). Falls back to
    counting non-header lines when the source uses no bullet markup."""
    if not raw_text:
        return None
    lines = raw_text.splitlines()
    bullets = sum(1 for ln in lines if _CRITERION_LINE.match(ln))
    if bullets:
        return bullets
    prose = [ln for ln in lines
             if ln.strip() and not ln.strip().lower().endswith("criteria:")]
    return len(prose) or None


def classify_action(verdict, raw_uncertainty_type):
    """For an undecided criterion, resolve (uncertainty_type, next action) in code.
    Decided criteria (MET/NOT_MET) carry no uncertainty and no action. UNKNOWN with
    no type defaults to MISSING (its definition: the record is silent); an UNCERTAIN
    with no usable type fails safe to a human via action_for(None) -> ESCALATE."""
    if verdict not in ("UNKNOWN", "UNCERTAIN"):
        return None, None
    utype = normalize_uncertainty_type(raw_uncertainty_type)
    if utype is None and verdict == "UNKNOWN":
        utype = "MISSING"
    return utype, action_for(utype)


def apply_evidence_sufficiency(verdict, evidence_meta):
    """Run the evidence-sufficiency check (evidence.py §6) on a decided verdict.

    Only fires when the matcher actually returned evidence metadata (source_type/
    confirmation_level/directness) for this criterion -- no metadata means nothing to
    check, so a bare MET/NOT_MET passes through unchanged. This is the enforcement
    point for "no blanket caution": a real, evidence-backed MET (e.g. a confirmed,
    direct pathology finding for 'History of ILD') must stay MET, and only the specific
    structured insufficiency rule in evidence.assess_evidence can demote a verdict.

    Returns (verdict, uncertainty_type, action, sufficiency_result|None). uncertainty_type
    and action are None unless the check demotes the verdict, in which case they are
    INSUFFICIENT_EVIDENCE / VERIFY (the same mapping evidence.py itself uses).
    """
    if verdict not in ("MET", "NOT_MET"):
        return verdict, None, None, None
    if not evidence_meta or not evidence_meta.get("confirmation_level"):
        return verdict, None, None, None
    result = assess_evidence(evidence_meta)
    if result["sufficient"]:
        return verdict, None, None, result
    return "UNCERTAIN", "INSUFFICIENT_EVIDENCE", action_for("INSUFFICIENT_EVIDENCE"), result


# ---------------------------------------------------------------------------
# trial-intent classification (건희 priority item 4)
# ---------------------------------------------------------------------------
# Deterministic, keyword/structure-based classification of what KIND of trial this is --
# therapeutic (testing a treatment's effect on disease), supportive (symptom/QoL/psychosocial
# care alongside a diagnosis), or care_delivery (observational/registry/process-of-care work,
# not testing a treatment at all). Computed in code from the trial record itself (title,
# conditions, phase, raw eligibility text); no LLM call needed for this heuristic, so there is
# nothing to default off -- if an LLM-assisted classifier is ever added, it must default off.
TRIAL_INTENT_KEYWORDS = {
    "supportive": [
        "quality of life", "supportive care", "palliative", "symptom management",
        "psychosocial", "caregiver", "nutrition", "coping", "distress",
        "rehabilitation", "exercise intervention", "mindfulness", "counseling",
    ],
    "care_delivery": [
        "registry", "observational", "cohort study", "survey", "screening program",
        "care coordination", "telehealth", "electronic health record", " ehr ",
        "implementation", "quality improvement", "health services", "care pathway",
        "natural history",
    ],
}
INTERVENTIONAL_PHASES = {"1", "2", "3", "4", "1/2", "2/3", "early1", "earlyphase1"}


def _norm_phase(phase):
    return str(phase or "").strip().lower().replace("phase", "").replace(" ", "")


def classify_trial_intent(trial):
    """therapeutic | supportive | care_delivery for one trial record. Pure, deterministic."""
    haystack = " ".join([
        trial.get("title", "") or "",
        " ".join(trial.get("conditions", []) or []),
        trial.get("eligibility_criteria_raw", "") or "",
    ]).lower()

    for kw in TRIAL_INTENT_KEYWORDS["supportive"]:
        if kw in haystack:
            return "supportive"
    for kw in TRIAL_INTENT_KEYWORDS["care_delivery"]:
        if kw in haystack:
            return "care_delivery"

    phase = _norm_phase(trial.get("phase"))
    if phase in INTERVENTIONAL_PHASES:
        return "therapeutic"
    if phase in ("na", "", "n/a"):
        return "care_delivery"
    return "therapeutic"


# ---------------------------------------------------------------------------
# (a) criteria-parser
# ---------------------------------------------------------------------------
CRITERIA_PARSER_SYS = """You are a clinical-trial eligibility criteria parser.
You receive raw eligibility criteria text copied from a ClinicalTrials.gov study record
(it typically has an "Inclusion Criteria" section, an "Exclusion Criteria" section, and
sometimes "Rejection Criteria" / "Termination" sections which you should fold into exclusion).
Split the text into a JSON list of atomic, individually-checkable criteria. Preserve the
original clinical wording as closely as possible -- do not paraphrase medical terms or drop
numeric thresholds. Do not merge two separable conditions into one criterion.
Respond with ONLY a JSON object, no markdown fences, no commentary, in this exact shape:
{"criteria": [{"text": "<verbatim-ish criterion text>", "type": "inclusion"|"exclusion"}]}
Return between 4 and 12 criteria (pick the clinically most decision-relevant ones if there are more)."""


def parse_criteria(trial):
    user = f"""Trial: {trial['title']}
NCT ID: {trial['nct_id']}

Raw eligibility criteria text:
\"\"\"
{trial['eligibility_criteria_raw']}
\"\"\"

Parse this into the JSON schema described in your instructions."""
    result = call_groq("criteria-parser", CRITERIA_PARSER_SYS, user)
    criteria = result.get("criteria", [])
    cleaned = []
    for c in criteria:
        text = str(c.get("text", "")).strip()
        ctype = str(c.get("type", "")).strip().lower()
        if not text or ctype not in ("inclusion", "exclusion"):
            continue
        cleaned.append({"text": text, "type": ctype})
    return cleaned


# ---------------------------------------------------------------------------
# (b) patient-extractor
# ---------------------------------------------------------------------------
PATIENT_EXTRACTOR_SYS = """You are a clinical patient-data extractor.
Given a short patient vignette, extract discrete clinical fields: demographics (age, sex),
symptoms, exam findings, lab/imaging findings, and relevant history/risk factors.
For every field, `evidence_quote` MUST be an EXACT verbatim substring copied
character-for-character from the vignette (same spelling, spacing, punctuation) that
supports the value. Never paraphrase the quote -- copy it exactly as it appears.
Respond with ONLY a JSON object, no markdown fences, no commentary, in this exact shape:
{"fields": [{"name": "<field name>", "value": "<extracted value>", "evidence_quote": "<verbatim substring>"}]}
Extract 5 to 10 fields."""


def extract_patient(patient):
    user = f"""Patient vignette (id {patient['patient_id']}):
\"\"\"
{patient['text']}
\"\"\"

Extract fields per your instructions. Remember: evidence_quote must be copied verbatim from the vignette above."""
    result = call_groq("patient-extractor", PATIENT_EXTRACTOR_SYS, user)
    fields = result.get("fields", [])
    verified, dropped = [], []
    for f in fields:
        name = str(f.get("name", "")).strip()
        value = str(f.get("value", "")).strip()
        quote = str(f.get("evidence_quote", "")).strip()
        if not name or not value or not quote:
            dropped.append(f)
            continue
        if quote in patient["text"]:
            verified.append({"name": name, "value": value, "evidence_quote": quote})
        else:
            dropped.append(f)
    return verified, dropped


# ---------------------------------------------------------------------------
# (c) matcher
# ---------------------------------------------------------------------------
MATCHER_SYS = """You are a clinical-trial eligibility matcher.
You receive a patient's extracted clinical fields and a numbered list of trial eligibility
criteria (each labelled inclusion or exclusion).

For EACH criterion, answer ONE question only: is the criterion STATEMENT true of this patient?
Do NOT reason about whether the patient qualifies for the trial. Do NOT invert your answer for
exclusion criteria. Whether a true statement helps or hurts the patient is decided downstream,
not by you. Judge the sentence exactly as written.
  - "MET": the statement is TRUE of this patient (the patient has/does what it describes).
           Example: criterion "Age under 18 years old", patient is 9 -> MET.
           Example: criterion "Age under 18 years old", patient is 54 -> NOT_MET.
           This holds regardless of whether the criterion is inclusion or exclusion.
  - "NOT_MET": the statement is FALSE of this patient (the patient's data contradicts it).
  - "UNCERTAIN": partial/ambiguous patient info that could go either way.
  - "UNKNOWN": the vignette contains NO information addressing this criterion at all (a gap).
Absence of evidence is NOT evidence of absence: if the vignette simply never mentions the
condition, that is UNKNOWN, not NOT_MET. A criterion resting on the investigator's discretion
or opinion is never decidable from the record; return UNKNOWN for it.

When (and ONLY when) your verdict is UNKNOWN or UNCERTAIN, also diagnose WHY it could not be
decided, choosing exactly one `uncertainty_type` from this fixed list (why-it-is-uncertain, not
what-is-missing):
""" + "\n".join(f"  - {k}: {v}" for k, v in UNCERTAINTY_TYPES.items()) + """
Pick the single most specific cause. If the record is simply silent, that is MISSING. If a value
exists but is old, STALE. If a number sits right at the threshold, BOUNDARY. If two findings
disagree, CONFLICTING. If the criterion needs expert interpretation that cannot be automated
(e.g. ECOG 1 vs 2, "clinically stable"), CLINICAL_JUDGMENT. For a MET or NOT_MET verdict, set
uncertainty_type to null.

`evidence` must be a short quote copied from the patient's fields/vignette that supports your
verdict, or null if verdict is UNKNOWN. `reasoning` must be <= 25 words, plain clinical language.

For a MET or NOT_MET verdict, ALSO give `evidence_meta` describing the KIND of evidence that
quote is, so a downstream sufficiency check can catch a finding being over-read (e.g. a
*suspected* imaging finding must never be treated as a *confirmed* diagnosis):
  - source_type: one of symptom, patient_report, lab, imaging, pathology, clinical_judgment
  - confirmation_level: one of suspected, provisional, confirmed (how settled the finding is --
    "CT shows a mass" is suspected; "biopsy-confirmed" or a clinician's documented diagnosis is
    confirmed)
  - directness: direct (the evidence itself states the fact the criterion needs) or indirect
    (you are inferring the fact from something else, e.g. inferring a lab abnormality from a
    symptom cluster)
Set evidence_meta to null when verdict is UNCERTAIN or UNKNOWN.
Respond with ONLY a JSON object, no markdown fences, no commentary, in this exact shape:
{"matches": [{"index": <criterion number as given>, "verdict": "MET"|"NOT_MET"|"UNCERTAIN"|"UNKNOWN", "uncertainty_type": "<one of the list above>"|null, "evidence": "<quote>"|null, "evidence_meta": {"source_type": "<...>", "confirmation_level": "<...>", "directness": "<...>"}|null, "reasoning": "<short reasoning>"}]}
Return exactly one match object per criterion given, in any order, using the given index numbers."""


def match_trial(patient, fields, criteria):
    field_lines = "\n".join(f"- {f['name']}: {f['value']}" for f in fields)
    criteria_lines = "\n".join(
        f"{i+1}. [{c['type']}] {c['text']}" for i, c in enumerate(criteria)
    )
    user = f"""Patient vignette:
\"\"\"
{patient['text']}
\"\"\"

Patient extracted fields:
{field_lines}

Trial eligibility criteria (numbered):
{criteria_lines}

Evaluate each numbered criterion per your instructions."""
    result = call_groq("matcher", MATCHER_SYS, user)
    matches = result.get("matches", [])
    by_index = {}
    for m in matches:
        try:
            idx = int(m.get("index"))
        except (TypeError, ValueError):
            continue
        verdict = str(m.get("verdict", "")).strip().upper()
        if verdict not in VALID_VERDICTS:
            verdict = "UNCERTAIN"
        evidence = m.get("evidence")
        evidence = str(evidence).strip() if evidence else None
        reasoning = truncate_words(str(m.get("reasoning", "")).strip(), MAX_REASONING_WORDS)
        raw_meta = m.get("evidence_meta")
        by_index[idx] = {"verdict": verdict, "evidence": evidence, "reasoning": reasoning,
                         "uncertainty_type": m.get("uncertainty_type"),
                         "evidence_meta": raw_meta if isinstance(raw_meta, dict) else None}

    merged = []
    for i, c in enumerate(criteria):
        m = by_index.get(i + 1, {"verdict": "UNCERTAIN", "evidence": None,
                                  "reasoning": "matcher did not return a verdict for this criterion",
                                  "uncertainty_type": None, "evidence_meta": None})
        verdict = m["verdict"]
        utype, action = classify_action(verdict, m.get("uncertainty_type"))
        verdict, demoted_utype, demoted_action, _suff = apply_evidence_sufficiency(
            verdict, m.get("evidence_meta"))
        if demoted_utype:
            utype, action = demoted_utype, demoted_action
        merged.append({
            "text": c["text"],
            "type": c["type"],
            "verdict": verdict,
            "effect": effect_of(c["type"], verdict),
            "uncertainty_type": utype,
            "action": action,
            "evidence": m["evidence"],
            "reasoning": m["reasoning"],
        })
    return merged


# ---------------------------------------------------------------------------
# (d) gap-detector
# ---------------------------------------------------------------------------
GAP_DETECTOR_SYS = """You are a clinical-trial gap detector.
You receive a patient vignette plus a list of eligibility criteria (across one or more
trials) that were marked UNKNOWN or UNCERTAIN because the vignette did not contain enough
information to evaluate them. Group these into a short list of distinct missing-information
"fields" a clinician would need to ask about (merge duplicates/near-duplicates across trials
into one gap, e.g. multiple criteria about lab values become one "specific lab values" gap).
Respond with ONLY a JSON object, no markdown fences, no commentary, in this exact shape:
{"gaps": [{"field": "<short name of missing info>", "why_needed": "<short reason, <=20 words>", "related_criteria": ["<criterion text>", ...]}]}
Return at most 6 gaps, ordered by how many criteria/trials they affect (most impactful first)."""


def detect_gaps(patient, all_criteria_with_trial):
    unknown_lines = []
    for item in all_criteria_with_trial:
        # Only undecided criteria whose policy action a question could actually advance.
        # IGNORE (not applicable) / STOP (already excluded) are resolved without asking, so
        # the action field gates the question pipeline here -- the differentiator in action.
        if item["verdict"] in ("UNKNOWN", "UNCERTAIN") and is_question_worthy(item.get("action")):
            unknown_lines.append(f"- [{item['nct_id']}] ({item['verdict']}) {item['text']}")
    if not unknown_lines:
        return []
    user = f"""Patient vignette:
\"\"\"
{patient['text']}
\"\"\"

Criteria marked UNKNOWN or UNCERTAIN across this patient's candidate trials:
{chr(10).join(unknown_lines)}

Identify the distinct missing-information gaps per your instructions."""
    result = call_groq("gap-detector", GAP_DETECTOR_SYS, user)
    gaps = result.get("gaps", [])
    cleaned = []
    for g in gaps:
        field = str(g.get("field", "")).strip()
        why = str(g.get("why_needed", "")).strip()
        related = g.get("related_criteria", [])
        if not field:
            continue
        cleaned.append({
            "field": field,
            "why_needed": why,
            "related_criteria": [str(r) for r in related] if isinstance(related, list) else [],
        })
    return cleaned


# ---------------------------------------------------------------------------
# (e) question-generator
# ---------------------------------------------------------------------------
QUESTION_GENERATOR_SYS = """You are a clinical clarifying-question generator.
Given a list of information gaps identified for a patient being matched to clinical trials,
write at most 3 short, specific clarifying questions a clinician or intake coordinator could
ask the patient (or check their chart for) to resolve the MOST IMPORTANT gaps.
Respond with ONLY a JSON object, no markdown fences, no commentary, in this exact shape:
{"questions": [{"field": "<matches a gap field>", "question": "<question text>", "why": "<short reason, <=20 words>"}]}
Return at most 3 questions, prioritizing gaps that affect the most trials."""


def generate_questions(patient, gaps):
    if not gaps:
        return []
    gap_lines = "\n".join(
        f"- {g['field']}: {g['why_needed']} (affects {len(g['related_criteria'])} criteria)"
        for g in gaps
    )
    user = f"""Patient vignette:
\"\"\"
{patient['text']}
\"\"\"

Identified information gaps:
{gap_lines}

Generate at most 3 clarifying questions per your instructions."""
    result = call_groq("question-generator", QUESTION_GENERATOR_SYS, user)
    questions = result.get("questions", [])
    cleaned = []
    for q in questions[:3]:
        field = str(q.get("field", "")).strip()
        question = str(q.get("question", "")).strip()
        why = str(q.get("why", "")).strip()
        if not question:
            continue
        cleaned.append({"field": field, "question": question, "why": why})
    return cleaned


# ---------------------------------------------------------------------------
# (f) recommender
# ---------------------------------------------------------------------------
RECOMMENDER_SYS = """You are a clinical-trial recommendation writer.
You receive a patient vignette and, for each candidate trial, its eligibility status and the
criteria that drove it. The eligibility status and the ranking have ALREADY been decided by a
deterministic rule and are given to you. Do not dispute them, re-derive them, or re-order the
trials -- your only job is to write the human-readable rationale for each.
Write <= 30 words per trial, citing the concrete clinical reason, in plain clinical language
(e.g. "TRAb-positive Graves confirmed by goiter and tachycardia; no exclusion criteria triggered"
or "Excluded: patient is 9 years old and the trial bars anyone under 18").
Respond with ONLY a JSON object, no markdown fences, no commentary, in this exact shape:
{"rationales": [{"nct_id": "<id>", "rationale": "<short rationale>"}]}
Include exactly one entry per trial given."""


def decide_eligibility(criteria):
    """Deterministic eligibility from criterion effects. No LLM, so polarity cannot be inferred
    wrong. Hierarchy (a hard failure is never averaged away by a pile of passes):
      1. any FAIL   -> INELIGIBLE   (excluded condition present, or required inclusion contradicted)
      2. any REVIEW -> UNCERTAIN    (something undecidable remains)
      3. else       -> ELIGIBLE
    """
    fails = [c for c in criteria if c.get("effect") == "FAIL"]
    reviews = [c for c in criteria if c.get("effect") == "REVIEW"]
    if fails:
        eligibility = "INELIGIBLE"
    elif reviews:
        eligibility = "UNCERTAIN"
    else:
        eligibility = "ELIGIBLE"
    return eligibility, fails, reviews


ELIGIBILITY_ORDER = {"ELIGIBLE": 0, "UNCERTAIN": 1, "INELIGIBLE": 2}


def recommend(patient, trials_with_criteria):
    # Layer 1: decide + rank in code.
    decided = []
    for t in trials_with_criteria:
        eligibility, fails, reviews = decide_eligibility(t["criteria"])
        decided.append({
            "nct_id": t["nct_id"], "title": t["title"], "phase": t["phase"],
            "eligibility": eligibility, "fails": fails, "reviews": reviews,
        })
    # Best match first: eligible before uncertain before ineligible; within a class, the trial
    # with the fewest unresolved criteria wins (a more confidently-established match).
    decided.sort(key=lambda d: (ELIGIBILITY_ORDER[d["eligibility"]], len(d["reviews"]), len(d["fails"])))
    for i, d in enumerate(decided):
        d["rank"] = i + 1

    # Layer 2: the model only narrates the decision it was handed.
    trial_blocks = []
    for d in decided:
        drivers = []
        for c in d["fails"][:3]:
            drivers.append(f"  FAILS [{c['type']}] {c['text']} (patient verdict: {c['verdict']})")
        for c in d["reviews"][:3]:
            drivers.append(f"  UNRESOLVED [{c['type']}] {c['text']} (patient verdict: {c['verdict']})")
        if not drivers:
            drivers.append("  all criteria pass")
        trial_blocks.append(
            f"{d['nct_id']} ({d['title']}, phase {d['phase']}) -> {d['eligibility']}, rank {d['rank']}\n"
            + "\n".join(drivers)
        )
    user = f"""Patient vignette:
\"\"\"
{patient['text']}
\"\"\"

Candidate trials, with their already-decided eligibility and the criteria that drove it:
{chr(10).join(trial_blocks)}

Write one rationale per trial per your instructions."""
    result = call_groq("recommender", RECOMMENDER_SYS, user)
    rationales = {}
    for r in result.get("rationales", []):
        nct_id = str(r.get("nct_id", "")).strip()
        if nct_id:
            rationales[nct_id] = truncate_words(
                str(r.get("rationale", "")).strip(), MAX_RATIONALE_WORDS)

    by_id = {}
    for d in decided:
        by_id[d["nct_id"]] = {
            "eligibility": d["eligibility"],
            "rank": d["rank"],
            "rationale": rationales.get(d["nct_id"], "no rationale returned for this trial"),
        }
    return by_id


# ---------------------------------------------------------------------------
# (g) reeval: record-and-answer generator
# ---------------------------------------------------------------------------
RECORD_ANSWER_SYS = """You are simulating a realistic clinical follow-up encounter.
You are given a patient vignette and a short list of clarifying questions a clinician asked
to resolve missing information gaps for clinical-trial matching. Generate PLAUSIBLE, CLINICALLY
CONSISTENT synthetic follow-up data (labs, exam findings, history, imaging) that a real patient
matching this vignette's diagnosis would plausibly have, and that directly answers each question.
Do not contradict anything already stated in the vignette. Prefer concrete numeric values
(e.g. TSH, fT4, creatinine, dates) over vague statements where clinically appropriate.

Then write ONE combined "extended_record" paragraph (<=180 words) containing all this new
synthetic follow-up information as plain clinical prose (this is the ONLY place this new
information lives -- do not put facts in an answer that are not ALSO in extended_record).

For each question, write a short "answer" and an "evidence_quote" that MUST be an EXACT
verbatim substring copied character-for-character from your own extended_record (same spelling,
spacing, punctuation) that supports the answer. Never paraphrase the quote.

Respond with ONLY a JSON object, no markdown fences, no commentary, in this exact shape:
{"extended_record": "<paragraph, <=180 words, synthetic but clinically plausible>",
 "answers": [{"question": "<question text, copied verbatim from the question given>",
              "answer": "<short answer>",
              "evidence_quote": "<verbatim substring of extended_record>"}]}
Return exactly one answer object per question given."""


def generate_extended_record(patient, questions):
    if not questions:
        return "", []
    q_lines = "\n".join(f"- {q['question']}" for q in questions)
    user = f"""Patient vignette (id {patient['patient_id']}, condition: {patient.get('condition', '')}):
\"\"\"
{patient['text']}
\"\"\"

Clarifying questions asked during follow-up:
{q_lines}

Generate the extended_record and answers per your instructions."""
    result = call_groq("reeval-record-answer", RECORD_ANSWER_SYS, user)
    extended_record = truncate_words(str(result.get("extended_record", "")).strip(), MAX_EXTENDED_RECORD_WORDS)
    answers_raw = result.get("answers", [])
    verified = []
    for a in answers_raw:
        question = str(a.get("question", "")).strip()
        answer = str(a.get("answer", "")).strip()
        quote = str(a.get("evidence_quote", "")).strip()
        if not question or not answer or not quote:
            continue
        if quote in extended_record:
            verified.append({"question": question, "answer": answer, "evidence_quote": quote})
        # else: dropped -- fails the same verbatim-grounding bar as (b) patient-extractor
    return extended_record, verified


# ---------------------------------------------------------------------------
# (h) reeval: targeted rematcher (only criteria the answers actually affect)
# ---------------------------------------------------------------------------
REEVAL_MATCHER_SYS = """You are a clinical-trial eligibility matcher doing a RE-EVALUATION pass.
The patient's original vignette was insufficient to decide some criteria (UNKNOWN/UNCERTAIN).
Follow-up information has since been obtained (the "extended record"). Re-decide ONLY the
listed criteria using the ORIGINAL vignette PLUS the extended record together.
Answer ONE question per criterion: is the criterion STATEMENT true of this patient? Do not
reason about whether the patient qualifies, and do not invert your answer for exclusion
criteria. Judge the sentence exactly as written; the pass/fail consequence is decided elsewhere.
  "MET": the statement is now TRUE of this patient (e.g. criterion "Age under 18", patient
         is 9 -> MET; patient is 54 -> NOT_MET). Same rule for inclusion and exclusion.
  "NOT_MET": the statement is FALSE of this patient (the record contradicts it).
  "UNCERTAIN": partial/ambiguous info that could still go either way.
  "UNKNOWN": still no information addressing this criterion, even after the extended record.
When (and only when) your verdict is UNKNOWN or UNCERTAIN, also give `uncertainty_type`, the single
best reason it still cannot be decided, from: """ + ", ".join(UNCERTAINTY_TYPES) + """. Otherwise
set uncertainty_type to null.
`evidence` must be a short quote from the vignette or extended record, or null if UNKNOWN.
`reasoning` must be <= 25 words.

For a MET or NOT_MET verdict, ALSO give `evidence_meta` (null for UNCERTAIN/UNKNOWN) describing
the kind of evidence: source_type (symptom, patient_report, lab, imaging, pathology,
clinical_judgment), confirmation_level (suspected, provisional, confirmed), and directness
(direct or indirect) -- same rule as the first matching pass: a suspected/indirect finding must
never be dressed up as a confirmed diagnosis.
Respond with ONLY a JSON object, no markdown fences, no commentary, in this exact shape:
{"matches": [{"index": <criterion number as given>, "verdict": "MET"|"NOT_MET"|"UNCERTAIN"|"UNKNOWN", "uncertainty_type": "<one of the list>"|null, "evidence": "<quote>"|null, "evidence_meta": {"source_type": "<...>", "confirmation_level": "<...>", "directness": "<...>"}|null, "reasoning": "<short reasoning>"}]}
Return exactly one match object per criterion given, using the given index numbers."""


def rematch_affected_criteria(patient, extended_record, affected):
    """affected: list of {nct_id, trial_idx, crit_idx, text, type, before_verdict}"""
    if not affected:
        return []
    lines = "\n".join(
        f"{i+1}. [{a['nct_id']}] [{a['type']}] {a['text']}" for i, a in enumerate(affected)
    )
    user = f"""Original patient vignette:
\"\"\"
{patient['text']}
\"\"\"

Extended record (new follow-up information obtained since the original vignette):
\"\"\"
{extended_record}
\"\"\"

Criteria to re-evaluate (numbered, [trial NCT ID] [inclusion/exclusion]):
{lines}

Re-evaluate each numbered criterion per your instructions."""
    result = call_groq("reeval-matcher", REEVAL_MATCHER_SYS, user)
    matches = result.get("matches", [])
    by_index = {}
    for m in matches:
        try:
            idx = int(m.get("index"))
        except (TypeError, ValueError):
            continue
        verdict = str(m.get("verdict", "")).strip().upper()
        if verdict not in VALID_VERDICTS:
            verdict = "UNCERTAIN"
        evidence = m.get("evidence")
        evidence = str(evidence).strip() if evidence else None
        reasoning = truncate_words(str(m.get("reasoning", "")).strip(), MAX_REASONING_WORDS)
        raw_meta = m.get("evidence_meta")
        by_index[idx] = {"verdict": verdict, "evidence": evidence, "reasoning": reasoning,
                         "uncertainty_type": m.get("uncertainty_type"),
                         "evidence_meta": raw_meta if isinstance(raw_meta, dict) else None}

    out = []
    for i, a in enumerate(affected):
        r = by_index.get(i + 1, {"verdict": a["before_verdict"], "evidence": None,
                                  "reasoning": "reeval-matcher did not return a verdict; kept prior verdict",
                                  "uncertainty_type": None, "evidence_meta": None})
        out.append({**a, "after_verdict": r["verdict"], "after_evidence": r["evidence"],
                     "after_reasoning": r["reasoning"], "after_uncertainty_type": r.get("uncertainty_type"),
                     "after_evidence_meta": r.get("evidence_meta")})
    return out


def run_reeval(patient, gaps, questions, trials_out):
    """Stage 5 (재평가): simulate the answer round, re-match only affected criteria, re-rank."""
    empty = {
        "extended_record": "", "answers": [], "verdict_changes": [],
        "final_ranking": [{"nct_id": t["nct_id"], "rank": t["rank"],
                            "eligibility": t["eligibility"], "rationale": t["rationale"]}
                           for t in trials_out],
    }
    if not questions or not gaps:
        return empty

    print(f"  [reeval] simulating extended patient record + answer round...")
    extended_record, answers = generate_extended_record(patient, questions)
    if not extended_record or not answers:
        print(f"    -> record/answer generation failed grounding check, skipping reeval")
        return empty

    gaps_by_field = {g["field"]: g for g in gaps}
    answered_fields = {q["field"] for q in questions
                        if any(a["question"] == q["question"] for a in answers)}
    target_criteria_texts = set()
    for field in answered_fields:
        g = gaps_by_field.get(field)
        if g:
            target_criteria_texts.update(g.get("related_criteria", []))

    affected = []
    for t_idx, t in enumerate(trials_out):
        for c_idx, c in enumerate(t["criteria"]):
            if c["text"] in target_criteria_texts and c["verdict"] in ("UNKNOWN", "UNCERTAIN"):
                affected.append({
                    "nct_id": t["nct_id"], "trial_idx": t_idx, "crit_idx": c_idx,
                    "text": c["text"], "type": c["type"], "before_verdict": c["verdict"],
                })

    if not affected:
        print(f"    -> no criteria matched to answered gaps, skipping rematch")
        return {**empty, "extended_record": extended_record, "answers": answers}

    print(f"  [reeval] re-matching {len(affected)} affected criteria...")
    rematched = rematch_affected_criteria(patient, extended_record, affected)

    verdict_changes = []
    updated_trials = [dict(t, criteria=[dict(c) for c in t["criteria"]]) for t in trials_out]
    for r in rematched:
        crit = updated_trials[r["trial_idx"]]["criteria"][r["crit_idx"]]
        after_verdict = r["after_verdict"]
        utype, action = classify_action(after_verdict, r.get("after_uncertainty_type"))
        after_verdict, demoted_utype, demoted_action, _suff = apply_evidence_sufficiency(
            after_verdict, r.get("after_evidence_meta"))
        if demoted_utype:
            utype, action = demoted_utype, demoted_action
        crit["verdict"] = after_verdict
        crit["effect"] = effect_of(crit["type"], after_verdict)
        crit["uncertainty_type"], crit["action"] = utype, action
        if r["after_evidence"]:
            crit["evidence"] = r["after_evidence"]
        crit["reasoning"] = r["after_reasoning"]
        if after_verdict != r["before_verdict"]:
            verdict_changes.append({
                "nct_id": r["nct_id"], "criterion": r["text"],
                "before": r["before_verdict"], "after": after_verdict,
            })

    print(f"    -> {len(verdict_changes)} verdict change(s)")
    print(f"  [reeval] re-ranking with updated criteria...")
    recs = recommend(patient, updated_trials)
    final_ranking = []
    for t in updated_trials:
        r = recs.get(t["nct_id"], {"eligibility": t["eligibility"], "rank": t["rank"], "rationale": t["rationale"]})
        final_ranking.append({"nct_id": t["nct_id"], "rank": r["rank"],
                               "eligibility": r["eligibility"], "rationale": r["rationale"]})
    final_ranking.sort(key=lambda r: r["rank"])

    return {
        "extended_record": extended_record,
        "answers": answers,
        "verdict_changes": verdict_changes,
        "final_ranking": final_ranking,
    }


# ---------------------------------------------------------------------------
# main orchestration
# ---------------------------------------------------------------------------
def run_patient(patient, trials_raw_for_patient):
    pid = patient["patient_id"]
    print(f"\n=== Patient {pid} ===")
    trials = trials_raw_for_patient["trials"][:TRIALS_PER_PATIENT]

    print(f"  [patient-extractor] extracting fields from vignette...")
    fields, dropped_fields = extract_patient(patient)
    if dropped_fields:
        print(f"    dropped {len(dropped_fields)} field(s) failing verbatim-substring check")

    trials_out = []
    all_criteria_flat = []  # for gap-detector: [{nct_id, text, verdict}]

    for t in trials:
        print(f"  [criteria-parser] {t['nct_id']} ({t['title'][:50]}...)")
        criteria = parse_criteria(t)
        print(f"    -> {len(criteria)} criteria parsed")

        print(f"  [matcher] {t['nct_id']} vs patient fields...")
        matched = match_trial(patient, fields, criteria)

        for c in matched:
            all_criteria_flat.append({"nct_id": t["nct_id"], "text": c["text"],
                                       "verdict": c["verdict"], "action": c.get("action")})

        trials_out.append({
            "nct_id": t["nct_id"],
            "title": t["title"],
            "phase": t["phase"],
            "trial_intent": classify_trial_intent(t),
            "criteria": matched,
        })

    print(f"  [gap-detector] aggregating UNKNOWN/UNCERTAIN gaps...")
    gaps = detect_gaps(patient, all_criteria_flat)
    print(f"    -> {len(gaps)} gap(s) identified")

    print(f"  [question-generator] generating clarifying questions...")
    questions = generate_questions(patient, gaps)
    print(f"    -> {len(questions)} question(s) generated")

    print(f"  [recommender] ranking {len(trials_out)} trials...")
    recs = recommend(patient, trials_out)

    for t in trials_out:
        r = recs.get(t["nct_id"], {"eligibility": "UNCERTAIN", "rank": 99, "rationale": ""})
        t["eligibility"] = r["eligibility"]
        t["rank"] = r["rank"]
        t["rationale"] = r["rationale"]

    trials_out.sort(key=lambda t: t["rank"])

    # attach the question-priority numbers 정원's cards show (pure, no LLM), now that
    # eligibility/rank are decided; also sorts questions most-impactful first.
    enrich_questions(questions, gaps, trials_out)

    reeval = run_reeval(patient, gaps, questions, trials_out)

    return {
        "patient_id": pid,
        "patient_text": patient["text"],
        "extraction": fields,
        "trials": trials_out,
        "gaps": gaps,
        "questions": questions,
        "reeval": reeval,
        "generated_at": "2026-07-08",
    }


def main():
    t0 = time.time()
    with open(os.path.join(HERE, "patients.json")) as f:
        patients = json.load(f)
    with open(os.path.join(HERE, "trials_raw.json")) as f:
        trials_raw = json.load(f)

    traces = []
    for patient in patients:
        pid = patient["patient_id"]
        if pid not in trials_raw:
            print(f"WARNING: no trials fetched for {pid}, skipping", file=sys.stderr)
            continue
        trace = run_patient(patient, trials_raw[pid])
        traces.append(trace)

    with open(os.path.join(HERE, "traces.json"), "w") as f:
        json.dump(traces, f, indent=2, ensure_ascii=False)

    js_content = "window.TRACES = " + json.dumps(traces, indent=2, ensure_ascii=False) + ";\n"
    with open(os.path.join(HERE, "traces.js"), "w") as f:
        f.write(js_content)

    elapsed = time.time() - t0
    s = stats()
    print(f"\n=== DONE in {elapsed:.1f}s ===")
    print(f"Groq API calls made: {s['api_calls']}  |  cache hits: {s['cache_hits']}")
    print("Wrote traces.json and traces.js")


# ---------------------------------------------------------------------------
# self-tests -- run: python3 pipeline.py --selftest (no LLM calls, no file I/O)
# ---------------------------------------------------------------------------
def _selftest():
    failures = []

    def check(cond, msg):
        if not cond:
            failures.append(msg)

    # ---- evidence-sufficiency wiring (apply_evidence_sufficiency) ----

    # no metadata at all -> pass through unchanged (no blanket caution)
    v, ut, act, r = apply_evidence_sufficiency("MET", None)
    check(v == "MET" and ut is None and act is None and r is None,
          "MET with no evidence_meta must pass through unchanged")

    # THE non-regression case: an evidence-backed "History of ILD" MET must stay MET.
    ild_meta = {"source_type": "patient_report", "confirmation_level": "confirmed", "directness": "direct"}
    v, ut, act, r = apply_evidence_sufficiency("MET", ild_meta)
    check(v == "MET", "confirmed direct evidence must NOT demote a real MET (ILD non-regression)")
    check(ut is None and act is None, "sufficient evidence must not attach an uncertainty_type/action")

    # THE §6 demotion case: a suspected/indirect imaging finding must demote MET -> UNCERTAIN.
    ct_meta = {"source_type": "imaging", "confirmation_level": "suspected", "directness": "indirect"}
    v, ut, act, r = apply_evidence_sufficiency("MET", ct_meta)
    check(v == "UNCERTAIN", "suspected/indirect imaging evidence must demote MET to UNCERTAIN")
    check(ut == "INSUFFICIENT_EVIDENCE", "demotion must carry uncertainty_type INSUFFICIENT_EVIDENCE")
    check(act == "VERIFY", "demotion must route to action VERIFY")
    check(r is not None and r["sufficient"] is False, "sufficiency result must be attached and insufficient")

    # UNCERTAIN/UNKNOWN verdicts are untouched regardless of metadata -- only MET/NOT_MET qualify
    v, ut, act, r = apply_evidence_sufficiency("UNCERTAIN", ct_meta)
    check(v == "UNCERTAIN" and ut is None and act is None,
          "apply_evidence_sufficiency must not touch UNCERTAIN/UNKNOWN verdicts")

    # NOT_MET can be demoted the same way as MET
    v, ut, act, r = apply_evidence_sufficiency("NOT_MET", ct_meta)
    check(v == "UNCERTAIN" and ut == "INSUFFICIENT_EVIDENCE",
          "NOT_MET must be demotable the same as MET")

    # effect_of composes correctly with a demoted verdict: REVIEW either way
    check(effect_of("exclusion", "UNCERTAIN") == "REVIEW", "demoted exclusion verdict -> REVIEW effect")
    check(effect_of("inclusion", "UNCERTAIN") == "REVIEW", "demoted inclusion verdict -> REVIEW effect")

    # end-to-end through match_trial's merge shape: a MET verdict with confirmed/direct evidence_meta
    # returned by the (mocked) matcher must still merge to MET/PASS, matching the real matcher's
    # by_index contract without making any network call.
    m_sufficient = {"verdict": "MET", "evidence": "biopsy shows...", "reasoning": "confirmed",
                    "uncertainty_type": None, "evidence_meta": ild_meta}
    utype, action = classify_action(m_sufficient["verdict"], m_sufficient.get("uncertainty_type"))
    verdict, d_ut, d_act, _ = apply_evidence_sufficiency(m_sufficient["verdict"], m_sufficient.get("evidence_meta"))
    if d_ut:
        utype, action = d_ut, d_act
    check(verdict == "MET" and effect_of("inclusion", verdict) == "PASS",
          "merge-shape simulation: sufficient evidence keeps MET -> PASS")

    m_insufficient = {"verdict": "MET", "evidence": "CT shows a bladder wall mass", "reasoning": "imaging",
                       "uncertainty_type": None, "evidence_meta": ct_meta}
    utype, action = classify_action(m_insufficient["verdict"], m_insufficient.get("uncertainty_type"))
    verdict, d_ut, d_act, _ = apply_evidence_sufficiency(m_insufficient["verdict"], m_insufficient.get("evidence_meta"))
    if d_ut:
        utype, action = d_ut, d_act
    check(verdict == "UNCERTAIN" and utype == "INSUFFICIENT_EVIDENCE" and action == "VERIFY"
          and effect_of("exclusion", verdict) == "REVIEW",
          "merge-shape simulation: §6 worked example demotes MET -> UNCERTAIN/VERIFY/REVIEW")

    # ---- trial-intent classification ----
    supportive_trial = {"title": "A Quality of Life and Symptom Management Study", "phase": "NA",
                         "conditions": ["Cancer"], "eligibility_criteria_raw": ""}
    check(classify_trial_intent(supportive_trial) == "supportive",
          "QoL/symptom-management title must classify as supportive")

    registry_trial = {"title": "A Prospective Observational Registry of Diabetes Outcomes",
                       "phase": "NA", "conditions": ["Diabetes"], "eligibility_criteria_raw": ""}
    check(classify_trial_intent(registry_trial) == "care_delivery",
          "observational registry title must classify as care_delivery")

    drug_trial = {"title": "A Phase 2 Study of Drug X for Advanced NSCLC", "phase": "2",
                  "conditions": ["NSCLC"], "eligibility_criteria_raw": "Histologically confirmed NSCLC"}
    check(classify_trial_intent(drug_trial) == "therapeutic",
          "phase 2 drug study must classify as therapeutic")

    na_no_signal_trial = {"title": "Long-Term Follow-Up of Graves Disease Patients", "phase": "NA",
                           "conditions": ["Graves Disease"], "eligibility_criteria_raw": ""}
    check(classify_trial_intent(na_no_signal_trial) == "care_delivery",
          "NA phase with no keyword signal must default to care_delivery")

    unphased_interventional = {"title": "Efficacy of a New Antibody Treatment", "phase": "1/2",
                                "conditions": ["Lymphoma"], "eligibility_criteria_raw": ""}
    check(classify_trial_intent(unphased_interventional) == "therapeutic",
          "phase 1/2 study must classify as therapeutic")

    if failures:
        print("FAIL:")
        for f in failures:
            print("  -", f)
        raise SystemExit(1)
    print(f"pipeline self-tests passed ({len(failures)} failures).")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    else:
        main()
