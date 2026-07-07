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

LLM = Groq free tier only (see groq_client.py). Every call is cached to disk in cache/ so
re-running this script after the first successful build makes ZERO new API calls.

Run:
    python3 pipeline.py
Writes:
    traces.json   (plain JSON)
    traces.js     (window.TRACES = [...]; consumed by demo.html)
"""
import json
import os
import sys
import time

from groq_client import call_groq, stats, DEFAULT_MODEL

HERE = os.path.dirname(os.path.abspath(__file__))
TRIALS_PER_PATIENT = 4
MAX_REASONING_WORDS = 25
MAX_RATIONALE_WORDS = 30

VALID_VERDICTS = {"MET", "NOT_MET", "UNCERTAIN", "UNKNOWN"}
VALID_ELIGIBILITY = {"ELIGIBLE", "INELIGIBLE", "UNCERTAIN"}


def truncate_words(text, n):
    words = text.split()
    if len(words) <= n:
        return text
    return " ".join(words[:n])


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
criteria (each labelled inclusion or exclusion). For EACH criterion, decide:
  - "MET": the patient's data directly satisfies this criterion (for inclusion) or the
           patient clearly does NOT have the excluded condition (for exclusion).
  - "NOT_MET": the patient's data directly contradicts/fails this criterion (for inclusion),
           or the patient DOES have the excluded condition (for exclusion).
  - "UNCERTAIN": there is partial/ambiguous patient info that could go either way.
  - "UNKNOWN": the vignette contains NO information addressing this criterion at all (a gap).
`evidence` must be a short quote copied from the patient's fields/vignette that supports your
verdict, or null if verdict is UNKNOWN. `reasoning` must be <= 25 words, plain clinical language.
Respond with ONLY a JSON object, no markdown fences, no commentary, in this exact shape:
{"matches": [{"index": <criterion number as given>, "verdict": "MET"|"NOT_MET"|"UNCERTAIN"|"UNKNOWN", "evidence": "<quote>"|null, "reasoning": "<short reasoning>"}]}
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
        by_index[idx] = {"verdict": verdict, "evidence": evidence, "reasoning": reasoning}

    merged = []
    for i, c in enumerate(criteria):
        m = by_index.get(i + 1, {"verdict": "UNCERTAIN", "evidence": None,
                                  "reasoning": "matcher did not return a verdict for this criterion"})
        merged.append({
            "text": c["text"],
            "type": c["type"],
            "verdict": m["verdict"],
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
        if item["verdict"] in ("UNKNOWN", "UNCERTAIN"):
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
RECOMMENDER_SYS = """You are a clinical-trial recommendation ranker.
You receive a patient vignette and, for each candidate trial, its criteria with verdicts
(MET/NOT_MET/UNCERTAIN/UNKNOWN per criterion). Decide an overall eligibility label per trial:
  - "ELIGIBLE": no exclusion criteria are MET (i.e. patient doesn't have excluded condition)
    and all/most inclusion criteria are MET, with no NOT_MET inclusion criteria.
  - "INELIGIBLE": at least one exclusion criterion verdict indicates the patient HAS the
    excluded condition (NOT_MET on an exclusion item means patient fails it -- re-read verdict
    semantics carefully), or a required inclusion criterion is clearly NOT_MET.
  - "UNCERTAIN": mixed picture, or too many UNKNOWN/UNCERTAIN criteria to decide confidently.
Then RANK the trials for this patient (1 = best match), favoring ELIGIBLE trials and trials
with fewer UNKNOWN/UNCERTAIN gaps. Give a rationale <= 30 words per trial citing the concrete
clinical reason (e.g. "TRAb-positive Graves confirmed by goiter+tachycardia; no exclusions met").
Respond with ONLY a JSON object, no markdown fences, no commentary, in this exact shape:
{"recommendations": [{"nct_id": "<id>", "rank": <int>, "eligibility": "ELIGIBLE"|"INELIGIBLE"|"UNCERTAIN", "rationale": "<short rationale>"}]}
Include exactly one entry per trial given."""


def recommend(patient, trials_with_criteria):
    trial_blocks = []
    for t in trials_with_criteria:
        lines = "\n".join(
            f"  - [{c['type']}] {c['text']} -> {c['verdict']}" for c in t["criteria"]
        )
        trial_blocks.append(f"{t['nct_id']} ({t['title']}, phase {t['phase']}):\n{lines}")
    user = f"""Patient vignette:
\"\"\"
{patient['text']}
\"\"\"

Candidate trials with per-criterion verdicts:
{chr(10).join(trial_blocks)}

Rank these trials and assign eligibility per your instructions."""
    result = call_groq("recommender", RECOMMENDER_SYS, user)
    recs = result.get("recommendations", [])
    by_id = {}
    for r in recs:
        nct_id = str(r.get("nct_id", "")).strip()
        if not nct_id:
            continue
        elig = str(r.get("eligibility", "")).strip().upper()
        if elig not in VALID_ELIGIBILITY:
            elig = "UNCERTAIN"
        try:
            rank = int(r.get("rank"))
        except (TypeError, ValueError):
            rank = 99
        rationale = truncate_words(str(r.get("rationale", "")).strip(), MAX_RATIONALE_WORDS)
        by_id[nct_id] = {"eligibility": elig, "rank": rank, "rationale": rationale}

    # fallback for any trial the model forgot
    for i, t in enumerate(trials_with_criteria):
        if t["nct_id"] not in by_id:
            by_id[t["nct_id"]] = {"eligibility": "UNCERTAIN", "rank": 99 + i,
                                   "rationale": "recommender did not return a rationale for this trial"}
    return by_id


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
            all_criteria_flat.append({"nct_id": t["nct_id"], "text": c["text"], "verdict": c["verdict"]})

        trials_out.append({
            "nct_id": t["nct_id"],
            "title": t["title"],
            "phase": t["phase"],
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

    return {
        "patient_id": pid,
        "patient_text": patient["text"],
        "extraction": fields,
        "trials": trials_out,
        "questions": questions,
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


if __name__ == "__main__":
    main()
