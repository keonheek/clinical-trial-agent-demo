#!/usr/bin/env python3
"""
build_trial_intent.py -- deterministic, rule-based trial-intent classifier (지우's ask).

A trial that TREATS the disease should not be presented the same as one that only observes
it, provides supportive care, or studies care logistics. This module classifies every trial
in trials_raw.json + trials_stress.json into exactly one of four tokens:

    therapeutic   -- tests a drug/device/procedure meant to treat the condition
    supportive    -- palliative / quality-of-life / symptom-management, not disease-modifying
    care_delivery -- studies how care is organized/delivered (navigation, telehealth, adherence)
    observational -- registries, cohorts, natural-history, mechanism/outcomes studies with no
                     intervention meant to change the disease course

Pure keyword + phase heuristic, NO LLM call (this repo's hard $0 rule) -- same sidecar +
serve-time-enrichment pattern as coverage_map.json (see api/trace.py): this script produces
`trial_intent.json` ({nct_id: {intent, confidence, signals}}), which api/trace.py and
live_server.py attach to trial payloads in memory. traces.json itself is never touched.

Run: python3 build_trial_intent.py            -- rebuild trial_intent.json + print table
     python3 build_trial_intent.py --selftest  -- synthetic classification checks
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Keyword sets are deliberately disjoint per 지우's own examples (registry -> observational,
# telehealth/navigation -> care_delivery -- NOT the same bucket) so a hit in one list is never
# silently swallowed by another. Matching is substring, case-insensitive, against
# title + conditions + eligibility_criteria_raw.
THERAPEUTIC_KEYWORDS = [
    "pembrolizumab", "chemotherapy", "chemoradiation", "radiation therapy", "radiotherapy",
    "ablation", "immunotherapy", "stem cell transplant", "gene therapy", "vaccine",
    "monoclonal antibody", "antibody-drug conjugate", "surgical resection",
    "fecal microbiota transplant",
]
# Named-intervention words specific enough that a hit is trustworthy even buried in
# eligibility text. Deliberately excludes generic terms like "surgery", "drug", or
# "treatment" -- those fire constantly on EXCLUSION criteria ("no prior surgery", "not on
# any investigational drug") and would misclassify observational studies as therapeutic.
SUPPORTIVE_KEYWORDS = [
    "quality of life", "supportive care", "palliative", "symptom management", "psychosocial",
    "caregiver", "nutrition support", "nutritional support", "pain management", "mindfulness",
    "counseling", "coping", "distress", "rehabilitation", "exercise intervention",
]
CARE_DELIVERY_KEYWORDS = [
    "telehealth", "navigation", "patient navigator", "adherence", "screening program",
    "care model", "care coordination", "implementation", "quality improvement",
    "care pathway", "decision support", "electronic health record", " ehr ",
    "health services",
]
# "improving care" / "access to" are real title patterns (지우's rule 5) but far too generic to
# trust once buried in eligibility text (e.g. "access to email/smartphone" as a logistics
# screening item has nothing to do with care delivery) -- title-scan only, never used in the
# eligibility-text tiebreak (see classify_trial_intent's Rule 4).
CARE_DELIVERY_TITLE_ONLY_KEYWORDS = CARE_DELIVERY_KEYWORDS + ["improving care", "access to"]
OBSERVATIONAL_KEYWORDS = [
    "registry", "observational", "cohort", "natural history", "surveillance",
    "outcomes using", "mechanisms", "epidemiolog", "biomarker study", "imaging study",
    "prospective cohort", "retrospective cohort", "metabolic outcomes",
]
# Weaker observational patterns that only ever raise CONFIDENCE on the phase-NA default
# (never decide intent by themselves, never scanned in Rule 1's title-decisive pass, and
# never reached for an interventional-phase trial -- see classify_trial_intent's Rule 2/3).
# Safe to be generic here (e.g. " after ") specifically because this branch is only ever
# reached once phase has already been ruled non-interventional.
OBSERVATIONAL_TITLE_BOOST_PATTERNS = [
    "biomarkers for", "biomarkers in", "role of", "outcomes after", " after ",
    "natural history of",
]

INTERVENTIONAL_PHASES = {
    "phase1", "phase2", "phase3", "phase4", "phase1/phase2", "phase2/phase3",
    "early_phase1", "earlyphase1", "phase 1", "phase 2", "phase 3", "phase 4",
    "phase 1/phase 2", "phase 2/phase 3",
}

VALID_INTENTS = {"therapeutic", "supportive", "care_delivery", "observational"}


def _is_interventional_phase(phase):
    # Normalize away spaces AND underscores -- ClinicalTrials.gov phase strings show up as
    # both "PHASE 2" and "EARLY_PHASE1" depending on source/era; either must compact the same way.
    p_compact = str(phase or "").strip().lower().replace(" ", "").replace("_", "")
    return p_compact in {
        "phase1", "phase2", "phase3", "phase4", "phase1/phase2", "phase2/phase3",
        "earlyphase1",
    }


def _title_text(trial):
    return " ".join([trial.get("title", "") or "", " ".join(trial.get("conditions", []) or [])]).lower()


def _full_text(trial):
    return " ".join([_title_text(trial), trial.get("eligibility_criteria_raw", "") or ""]).lower()


def _matches(haystack, keywords):
    return [kw for kw in keywords if kw in haystack]


def _title_hits_by_category(title_text):
    """Rule 1's scan -- title is the strong signal, so care_delivery gets its extra
    generic title patterns here (they are NOT safe for the eligibility-text tiebreak)."""
    return {
        "therapeutic": _matches(title_text, THERAPEUTIC_KEYWORDS),
        "supportive": _matches(title_text, SUPPORTIVE_KEYWORDS),
        "care_delivery": _matches(title_text, CARE_DELIVERY_TITLE_ONLY_KEYWORDS),
        "observational": _matches(title_text, OBSERVATIONAL_KEYWORDS),
    }


# Priority when multiple keyword categories fire in the same scan: therapeutic (an actual
# intervention is named) > observational > supportive > care_delivery.
PRIORITY = ["therapeutic", "supportive", "care_delivery", "observational"]


def classify_trial_intent(trial):
    """Returns {"intent": ..., "confidence": "high"|"low", "signals": [...]}. Pure, deterministic.

    Rule order (each rule only fires if the ones above it did not decide):

    1. Title + conditions is the STRONG signal (a trial's title is where its own stated
       purpose lives). A title-level keyword hit is decisive and high-confidence.
    2. If the title is silent, an interventional phase (1-4) is decisive on its own ->
       therapeutic. Eligibility/exclusion-criteria text describes the PATIENT (history,
       exclusions, follow-up schedule), not the trial's own intervention, so it must NEVER
       flip a phased interventional trial away from therapeutic (this was the exact bug a
       "prior surgery" exclusion clause caused for one CGM study, and a "rehabilitation"
       mention caused for a phase-2 drug trial -- both fixed by putting phase ahead of
       eligibility text in priority, not by special-casing either trial).
    3. If the title is silent AND phase is NA/unspecified, the default is observational
       (most NA-phase trials with no stated intervention are registries/cohorts), low
       confidence unless a title pattern typical of observational studies (biomarkers-for,
       role-of, outcomes-after, natural-history-of, "X After Y") raises it to high.
    4. Only within that NA-phase-default branch, eligibility text may weakly tie-break
       between supportive and care_delivery (never toward therapeutic or observational --
       a phase-NA trial whose exclusion criteria happens to mention a drug name is not
       thereby "therapeutic").
    """
    phase = trial.get("phase")
    interventional = _is_interventional_phase(phase)

    title_hits = _title_hits_by_category(_title_text(trial))
    title_categories = [c for c in PRIORITY if title_hits[c]]

    signals = []
    for c in PRIORITY:
        for kw in title_hits[c]:
            signals.append(f"title-keyword:{kw}->{c}")

    if interventional:
        signals.append(f"phase:{phase} (interventional)")
    elif phase not in (None, ""):
        signals.append(f"phase:{phase} (non-interventional, against therapeutic but not decisive)")

    # Rule 1: title decisive.
    if len(title_categories) >= 2:
        intent = next(c for c in PRIORITY if c in title_categories)
        return {"intent": intent, "confidence": "low", "signals": signals}

    if len(title_categories) == 1:
        intent = title_categories[0]
        if intent != "therapeutic" and interventional:
            signals.append(f"conflict: title says {intent} but phase is interventional")
            return {"intent": intent, "confidence": "low", "signals": signals}
        return {"intent": intent, "confidence": "high", "signals": signals}

    # Title silent from here on.
    # Rule 2: interventional phase is decisive by itself. Eligibility text is deliberately
    # NOT consulted in this branch -- it describes the patient, not the trial's intervention.
    if interventional:
        signals.append(
            "no title signal; phase-only default -> therapeutic "
            "(eligibility-text keywords ignored here: they describe patient history/exclusions, "
            "never the trial's own intervention)"
        )
        return {"intent": "therapeutic", "confidence": "high", "signals": signals}

    # Rule 3/4: phase NA (or unspecified) and title silent -> default observational, with
    # eligibility text allowed only a weak supportive/care_delivery tiebreak (never therapeutic,
    # never observational -- that would just be Rule 3's own default restated).
    full_text = _full_text(trial)
    tiebreak_hits = {
        "supportive": _matches(full_text, SUPPORTIVE_KEYWORDS),
        "care_delivery": _matches(full_text, CARE_DELIVERY_KEYWORDS),
    }
    for c in ("supportive", "care_delivery"):
        for kw in tiebreak_hits[c]:
            signals.append(f"eligibility-text-keyword:{kw}->{c} (weak tiebreak, non-interventional only)")
    tiebreak_categories = [c for c in ("supportive", "care_delivery") if tiebreak_hits[c]]

    if tiebreak_categories:
        intent = next(c for c in PRIORITY if c in tiebreak_categories)
        return {"intent": intent, "confidence": "low", "signals": signals}

    if any(p in _title_text(trial) for p in OBSERVATIONAL_TITLE_BOOST_PATTERNS):
        signals.append("observational title pattern (biomarkers/role-of/outcomes-after/etc) "
                        "-> phase-NA default raised to high confidence")
        return {"intent": "observational", "confidence": "high", "signals": signals}

    signals.append("no keyword signal; NA/non-interventional phase-only default -> observational")
    return {"intent": "observational", "confidence": "low", "signals": signals}


def _load_all_trials():
    """Union of trials_raw.json (keyed by patient/query id -> {trials:[...]}) and
    trials_stress.json (flat nct_id -> trial), deduped by nct_id."""
    trials_by_id = {}

    raw_path = os.path.join(HERE, "trials_raw.json")
    if os.path.exists(raw_path):
        with open(raw_path, encoding="utf-8") as f:
            raw = json.load(f)
        for entry in raw.values():
            for t in entry.get("trials", []):
                trials_by_id[t["nct_id"]] = t

    stress_path = os.path.join(HERE, "trials_stress.json")
    if os.path.exists(stress_path):
        with open(stress_path, encoding="utf-8") as f:
            stress = json.load(f)
        for nct_id, t in stress.items():
            trials_by_id.setdefault(nct_id, t)

    return trials_by_id


def build():
    trials_by_id = _load_all_trials()
    result = {}
    for nct_id in sorted(trials_by_id):
        result[nct_id] = classify_trial_intent(trials_by_id[nct_id])

    out_path = os.path.join(HERE, "trial_intent.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write("\n")

    print(f"{len(result)} trials classified -> {out_path}\n")
    print(f"{'nct_id':<14} {'intent':<14} confidence")
    for nct_id in sorted(result):
        r = result[nct_id]
        print(f"{nct_id:<14} {r['intent']:<14} {r['confidence']}")
    return result


def _check(cond, msg, failures):
    if not cond:
        failures.append(msg)


def _selftest():
    failures = []

    supportive_trial = {
        "title": "A Quality of Life and Symptom Management Study for Cancer Patients",
        "phase": "NA", "conditions": ["Cancer"], "eligibility_criteria_raw": "",
    }
    r = classify_trial_intent(supportive_trial)
    _check(r["intent"] == "supportive" and r["confidence"] == "high",
           f"supportive/high expected, got {r}", failures)

    care_delivery_trial = {
        "title": "Telehealth Navigation Program to Improve Screening Adherence",
        "phase": "NA", "conditions": ["Diabetes"], "eligibility_criteria_raw": "",
    }
    r = classify_trial_intent(care_delivery_trial)
    _check(r["intent"] == "care_delivery" and r["confidence"] == "high",
           f"care_delivery/high expected, got {r}", failures)

    observational_trial = {
        "title": "Diabetes RElated to Acute Pancreatitis and Its Mechanisms: Metabolic "
                 "Outcomes Using Novel CGM Metrics",
        "phase": "NA", "conditions": ["Acute Pancreatitis"], "eligibility_criteria_raw": "",
    }
    r = classify_trial_intent(observational_trial)
    _check(r["intent"] == "observational",
           f"observational expected for CGM metrics study, got {r}", failures)

    therapeutic_trial = {
        "title": "Pembrolizumab and EV With Radiation Therapy for MIBC Patients",
        "phase": "PHASE 2", "conditions": ["Bladder Cancer"], "eligibility_criteria_raw": "",
    }
    r = classify_trial_intent(therapeutic_trial)
    _check(r["intent"] == "therapeutic" and r["confidence"] == "high",
           f"therapeutic/high expected, got {r}", failures)

    phase_only_trial = {
        "title": "A Study of Compound XR-19 in Adults With Hypertension",
        "phase": "PHASE 1", "conditions": ["Hypertension"], "eligibility_criteria_raw": "",
    }
    r = classify_trial_intent(phase_only_trial)
    _check(r["intent"] == "therapeutic" and r["confidence"] == "high",
           f"phase-only interventional -> therapeutic/high expected, got {r}", failures)

    na_no_signal_trial = {
        "title": "Long-Term Follow-Up of Graves Disease Patients",
        "phase": "NA", "conditions": ["Graves Disease"], "eligibility_criteria_raw": "",
    }
    r = classify_trial_intent(na_no_signal_trial)
    _check(r["intent"] == "observational" and r["confidence"] == "low",
           f"NA/no-signal -> observational/low expected, got {r}", failures)

    conflict_trial = {
        "title": "Phase 2 Registry-Linked Study of Drug ABC for Lymphoma",
        "phase": "PHASE 2", "conditions": ["Lymphoma"], "eligibility_criteria_raw": "",
    }
    r = classify_trial_intent(conflict_trial)
    _check(r["confidence"] == "low",
           f"conflicting keyword ('registry') + interventional phase -> low confidence expected, got {r}",
           failures)

    # ---- regression cases from 지우's classification audit (synthetic analogues of the 6
    # real trials that misclassified; no NCT ids in the classifier itself, per rule) ----

    # analogue of a biomarker-registry study whose exclusion criteria happens to mention a
    # prior stem-cell transplant -- must not read as therapeutic from eligibility text alone.
    biomarker_trial = {
        "title": "Biomarkers for Refractory Aspergillosis", "phase": "NA",
        "conditions": ["Aspergillosis"],
        "eligibility_criteria_raw": "Exclusion: prior stem cell transplant within 90 days.",
    }
    r = classify_trial_intent(biomarker_trial)
    _check(r["intent"] == "observational" and r["confidence"] == "high",
           f"biomarkers-for title -> observational/high expected, got {r}", failures)

    # analogue of a genetics/mechanism study ("Role of X in Y") whose eligibility text happens
    # to mention radiotherapy in an unrelated exclusion clause.
    role_of_trial = {
        "title": "Role of XYZ1 Variants in Craniofacial Muscle Development", "phase": "NA",
        "conditions": ["Craniofacial Myopathy"],
        "eligibility_criteria_raw": "Exclusion: history of radiotherapy to the head or neck.",
    }
    r = classify_trial_intent(role_of_trial)
    _check(r["intent"] == "observational" and r["confidence"] == "high",
           f"'role of X in Y' title -> observational/high expected, got {r}", failures)

    # analogue of an "X After Y" natural-history/complication study (immunoparalysis-style)
    # whose eligibility text happens to mention chemotherapy as an exclusion.
    after_trial = {
        "title": "Immune Dysfunction After Hepatectomy", "phase": "NA",
        "conditions": ["Post-Hepatectomy Immune Dysfunction"],
        "eligibility_criteria_raw": "Exclusion: chemotherapy within the prior 6 months.",
    }
    r = classify_trial_intent(after_trial)
    _check(r["intent"] == "observational" and r["confidence"] == "high",
           f"'X After Y' title -> observational/high expected, got {r}", failures)

    # analogue of a phased drug trial whose eligibility text happens to mention rehabilitation
    # (e.g. as part of a comorbidity exclusion) -- must stay therapeutic, phase decides first.
    phased_with_supportive_text_trial = {
        "title": "Phase II Study of Compound ZT-04 in Patients With Pulmonary Fibrosis",
        "phase": "PHASE 2", "conditions": ["Idiopathic Pulmonary Fibrosis"],
        "eligibility_criteria_raw": "Exclusion: currently enrolled in a pulmonary rehabilitation program.",
    }
    r = classify_trial_intent(phased_with_supportive_text_trial)
    _check(r["intent"] == "therapeutic" and r["confidence"] == "high",
           f"phased trial must stay therapeutic despite eligibility-text 'rehabilitation', got {r}",
           failures)

    # analogue of a named-intervention title (FMT) whose eligibility text happens to mention
    # nutritional support incidentally -- title keyword must decide, not eligibility text.
    named_intervention_trial = {
        "title": "Fecal Microbiota Transplantation in Patients With Severe Colitis", "phase": "NA",
        "conditions": ["Severe Colitis"],
        "eligibility_criteria_raw": "Inclusion: able to tolerate oral nutritional support if needed.",
    }
    r = classify_trial_intent(named_intervention_trial)
    _check(r["intent"] == "therapeutic" and r["confidence"] == "high",
           f"named-intervention title (FMT) -> therapeutic/high expected, got {r}", failures)

    # analogue of a care-delivery title pattern ("Improving Care for ...").
    care_pattern_trial = {
        "title": "Improving Care for Rural Patients With Chronic Kidney Disease", "phase": "NA",
        "conditions": ["Chronic Kidney Disease"], "eligibility_criteria_raw": "",
    }
    r = classify_trial_intent(care_pattern_trial)
    _check(r["intent"] == "care_delivery" and r["confidence"] == "high",
           f"'Improving Care for...' title -> care_delivery/high expected, got {r}", failures)

    # regression: EARLY_PHASE1 (underscore form, as ClinicalTrials.gov emits it) must be
    # recognized as interventional just like "PHASE 1" -- found via a real CAR-T trial that
    # fell through to the observational default because the underscore wasn't stripped.
    early_phase_trial = {
        "title": "In Vivo CAR-T Cells for Refractory Autoimmune Disease", "phase": "EARLY_PHASE1",
        "conditions": ["Autoimmune Disease"], "eligibility_criteria_raw": "",
    }
    r = classify_trial_intent(early_phase_trial)
    _check(r["intent"] == "therapeutic" and r["confidence"] == "high",
           f"EARLY_PHASE1 must be treated as interventional -> therapeutic/high, got {r}", failures)

    # regression: "access to" is a real title pattern (rule 5) but far too generic for the
    # eligibility-text tiebreak -- a logistics screening item ("access to a smartphone") must
    # not be read as a care-delivery signal for an otherwise-unrelated NA-phase trial.
    access_to_noise_trial = {
        "title": "Remote Symptom Monitoring Feasibility in Migraine", "phase": "NA",
        "conditions": ["Migraine"],
        "eligibility_criteria_raw": "Inclusion: has access to email or a smartphone with internet access.",
    }
    r = classify_trial_intent(access_to_noise_trial)
    _check(r["intent"] == "observational" and r["confidence"] == "low",
           f"'access to' in eligibility text must not force care_delivery, got {r}", failures)

    for intent_r in (r for r in [classify_trial_intent(t) for t in
                                  [supportive_trial, care_delivery_trial, observational_trial,
                                   therapeutic_trial, phase_only_trial, na_no_signal_trial,
                                   conflict_trial, biomarker_trial, role_of_trial, after_trial,
                                   phased_with_supportive_text_trial, named_intervention_trial,
                                   care_pattern_trial, early_phase_trial, access_to_noise_trial]]):
        _check(intent_r["intent"] in VALID_INTENTS, f"intent token must be one of {VALID_INTENTS}", failures)

    if failures:
        print("FAIL:")
        for f in failures:
            print("  -", f)
        raise SystemExit(1)
    print(f"build_trial_intent self-tests passed ({len(failures)} failures).")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    else:
        build()
