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
    claude (default) — headless `claude -p` on the local subscription (claude_client.py)
    groq             — Groq free tier (groq_client.py); daily quota crawls under load
Every call is cached to disk in cache/ (keyed per backend model), so re-running this
script after the first successful build makes ZERO new LLM calls.

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

if os.environ.get("LLM_BACKEND", "groq") == "groq":
    from groq_client import call_groq, stats, DEFAULT_MODEL
else:
    from claude_client import call_llm as call_groq, stats, DEFAULT_MODEL

HERE = os.path.dirname(os.path.abspath(__file__))
TRIALS_PER_PATIENT = 4
MAX_REASONING_WORDS = 25
MAX_RATIONALE_WORDS = 30
MAX_EXTENDED_RECORD_WORDS = 180

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
Use the same verdict semantics as a standard matcher:
  "MET": patient's data now directly satisfies this criterion (inclusion) or patient clearly
         does NOT have the excluded condition (exclusion).
  "NOT_MET": patient's data now directly contradicts/fails this criterion (inclusion), or the
         patient DOES have the excluded condition (exclusion).
  "UNCERTAIN": partial/ambiguous info that could still go either way.
  "UNKNOWN": still no information addressing this criterion, even after the extended record.
`evidence` must be a short quote from the vignette or extended record, or null if UNKNOWN.
`reasoning` must be <= 25 words.
Respond with ONLY a JSON object, no markdown fences, no commentary, in this exact shape:
{"matches": [{"index": <criterion number as given>, "verdict": "MET"|"NOT_MET"|"UNCERTAIN"|"UNKNOWN", "evidence": "<quote>"|null, "reasoning": "<short reasoning>"}]}
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
        by_index[idx] = {"verdict": verdict, "evidence": evidence, "reasoning": reasoning}

    out = []
    for i, a in enumerate(affected):
        r = by_index.get(i + 1, {"verdict": a["before_verdict"], "evidence": None,
                                  "reasoning": "reeval-matcher did not return a verdict; kept prior verdict"})
        out.append({**a, "after_verdict": r["verdict"], "after_evidence": r["evidence"],
                     "after_reasoning": r["reasoning"]})
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
        crit["verdict"] = r["after_verdict"]
        if r["after_evidence"]:
            crit["evidence"] = r["after_evidence"]
        crit["reasoning"] = r["after_reasoning"]
        if r["after_verdict"] != r["before_verdict"]:
            verdict_changes.append({
                "nct_id": r["nct_id"], "criterion": r["text"],
                "before": r["before_verdict"], "after": r["after_verdict"],
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

    reeval = run_reeval(patient, gaps, questions, trials_out)

    return {
        "patient_id": pid,
        "patient_text": patient["text"],
        "extraction": fields,
        "trials": trials_out,
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


if __name__ == "__main__":
    main()
