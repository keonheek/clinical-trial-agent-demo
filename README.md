# SDIC Trial-Match Demo — Interactive Clinical Trial Recommendation

Backend for a demo built for the SKKU "Healthcare Agentic AI Challenge 2026" task: a
multi-agent system that matches patients to clinical trials with evidence, detects missing
info, generates clarifying questions, and ranks recommendations.

This is a capability demo, not a validated clinical tool. See disclaimer at the bottom.

## What it does

1. Pulls REAL, currently-recruiting trials from ClinicalTrials.gov for all 10 official sample patients
   (S001-S010 from the challenge's synthetic-patients.json).
2. Runs a 6-role LLM pipeline plus a re-evaluation loop (LLM backend switchable: Groq free tier by default, or local Claude Code subscription via LLM_BACKEND=claude) that parses trial eligibility criteria,
   extracts patient facts with verbatim evidence, matches each criterion, detects gaps in
   the patient's data, generates clarifying questions, and ranks the trials.
3. Writes `traces.js` (`window.TRACES = [...]`) for the frontend (`demo.html`, owned by a
   separate agent) to render directly — no server needed, it's a static JSON blob.

## Agent-role diagram

```
                         ClinicalTrials.gov API v2 (public domain)
                                        |
                                        v
                              +-------------------+
                              |   fetch_trials.py  |
                              +-------------------+
                                        |
                                        v
                                trials_raw.json
                                        |
        patients.json                  |
             |                         |
             v                         v
   +-------------------+     +----------------------+
   | (b) patient-       |     | (a) criteria-parser  |   <- 1 call per trial
   |     extractor      |     |  raw text -> atomic   |
   |  vignette -> fields|     |  {text, type} list    |
   |  + evidence_quote  |     +----------------------+
   | (verified verbatim |                |
   |  substring, server-|                |
   |  side; violations  |                |
   |  dropped)          |                |
   +--------------------+                |
             |                           |
             +------------+--------------+
                          v
                +----------------------+
                | (c) matcher          |   <- 1 call per trial (all its criteria batched)
                |  criteria x patient  |
                |  -> verdict/evidence/|
                |     reasoning each   |
                +----------------------+
                          |
                          v
                +----------------------+
                | (d) gap-detector     |   <- 1 call per patient
                |  UNKNOWN/UNCERTAIN   |
                |  criteria -> distinct|
                |  missing-info gaps   |
                +----------------------+
                          |
                          v
                +----------------------+
                | (e) question-        |   <- 1 call per patient
                |     generator        |
                |  gaps -> <=3         |
                |  clarifying Qs       |
                +----------------------+
                          |
                          v
                +----------------------+
                | (f) recommender      |   <- 1 call per patient
                |  ranks trials,       |
                |  ELIGIBLE/INELIGIBLE/|
                |  UNCERTAIN + why     |
                +----------------------+
                          |
                          v
                traces.json / traces.js
                (window.TRACES = [...])
                          |
                          v
                    demo.html (UI, separate agent)
```

Each box (a)-(f) is an independent Groq LLM call with its own system prompt — no single
mega-prompt does everything. Total calls per patient with 4 trials: 1 (extractor) + 4
(criteria-parser) + 4 (matcher) + 1 (gap-detector) + 1 (question-generator) + 1
(recommender) = 12. For 3 patients: 36 calls total on first run; $0 on every re-run because
every call is cached to disk (`cache/`, keyed on role+model+prompt hash).

## How to re-run

```bash
cd projects/sdic-trial-demo
python3 fetch_trials.py     # re-pulls live trial data (skip if trials_raw.json is fine)
python3 pipeline.py         # runs the 6-role pipeline, writes traces.json + traces.js
python3 assert_traces.py    # verifies every evidence_quote is a verbatim substring
```

Requires `GROQ_API_KEY` in the environment or in `.env` / `.env.local` at the repo root.
No other dependencies beyond the Python 3 standard library (`urllib`, `json`, `hashlib`).

To force a clean re-run with fresh LLM calls: `rm -rf cache/` first (this spends real
Groq free-tier quota again).

## Dependencies

- Python 3 standard library only (no pip installs required: `urllib.request`, `json`,
  `hashlib`, `time`, `os`).
- Groq API (`https://api.groq.com/openai/v1/chat/completions`), free tier, model
  `llama-3.3-70b-versatile`, JSON mode (`response_format: {"type": "json_object"}`).
- ClinicalTrials.gov API v2 (`https://clinicaltrials.gov/api/v2/studies`), no key required.

## Data sources & licenses

- **ClinicalTrials.gov** (U.S. National Library of Medicine / NIH): trial records, titles,
  phases, and eligibility criteria text are public domain (U.S. Government work). See
  https://clinicaltrials.gov/about-site/terms-conditions. All 16 trials in `trials_raw.json`
  are REAL, currently-recruiting studies pulled live via the public API v2 — not
  fabricated. Query used per condition is recorded in `trials_raw.json` under
  `query_used`.
- **Patient vignettes** (`patients.json`): the competition's own published sample patients
  (S001, S002, S008), copied verbatim from the task brief — not real patient data.
- **Groq** (LLM inference, free tier): https://groq.com — used for all 6 agent roles.
  Model: `llama-3.3-70b-versatile`. No paid Anthropic API is used anywhere in this pipeline.

## Uncertainty & action layer (the differentiator)

Overall accuracy hides the point: the system's edge is not "how many criteria it labels
right," it's what it DOES when a criterion cannot be decided from the record. Three code
layers, each a pure table/function (computed in code, never inferred by a model — the same
design rule as the eligibility `effect` table), turn "UNKNOWN" into a diagnosed cause and a
next action:

- **Uncertainty taxonomy** (`action_policy.py`): every undecided criterion is classified into
  one of 10 causes — MISSING, STALE, INSUFFICIENT_EVIDENCE, AMBIGUOUS, CONFLICTING, BOUNDARY,
  CLINICAL_JUDGMENT, NOT_APPLICABLE, CALCULABLE, DEFINITE_EXCLUSION. The matcher LLM proposes
  the type; the type is a fixed vocabulary, not free text.
- **Action-selection table** (`action_policy.py`): each cause maps to exactly one next action —
  ASK / RETRIEVE / REQUEST_LATEST / CALCULATE / VERIFY / PROTOCOL_REVIEW / ESCALATE / IGNORE /
  STOP. Derived in code, so the polarity can't be gotten backwards. An unrecognized cause fails
  safe to ESCALATE — never a silent pass. This is the "질문을 많이 하는 게 아니라 상황에 맞는
  행동을 고른다" claim, made concrete.
- **Evidence sufficiency** (`evidence.py`): traceability (does the quote exist?) is not
  sufficiency (does the quote support the conclusion?). Each evidence item carries source_type /
  confirmation_level / directness; `assess_evidence()` rejects e.g. a *suspected* imaging finding
  standing in for a *confirmed* diagnosis, and routes it to VERIFY.

**Question-priority API (for the frontend cards).** Each clarifying question is served with
`affects_trials`, `affects_criteria`, and `may_change_rank`, computed deterministically from the
trace (`action_policy.enrich_questions`). `live_server.py` attaches these at serve time, so the
frontend consumes real numbers — no hardcoding needed. Questions arrive sorted most-impactful
first. Run `python3 action_policy.py` and `python3 evidence.py` for the self-tests.

## Medical disclaimer

**출력 결과는 의학적 자문이 아닌 참고용입니다.**
(The output of this system is for reference only and does NOT constitute medical advice.
It is a hackathon capability demo and has not been clinically validated. Trial eligibility
must always be confirmed with the trial's own study team and a qualified clinician before
any enrollment decision.)

## Files

| File | Owner | Purpose |
|---|---|---|
| `fetch_trials.py` | this agent | pulls real recruiting trials from ClinicalTrials.gov v2 |
| `patients.json` | this agent | 3 sample patient vignettes (verbatim from task brief) |
| `trials_raw.json` | this agent | raw fetched trial data (16 trials, 3 conditions) |
| `groq_client.py` | this agent | Groq API wrapper: caching + exponential backoff |
| `pipeline.py` | this agent | 6-role multi-agent pipeline orchestration |
| `action_policy.py` | this agent | uncertainty taxonomy + action-selection table + question-priority scorer (pure, self-tested) |
| `evidence.py` | this agent | evidence-sufficiency layer: confirmation/directness rules (pure, self-tested) |
| `live_server.py` | this agent | interactive re-eval HTTP server; serves priority-enriched questions |
| `assert_traces.py` | this agent | verification script: evidence_quote verbatim-substring checks |
| `traces.json` / `traces.js` | this agent | pipeline output consumed by the UI |
| `cache/` | this agent | on-disk LLM response cache (re-runs are free) |
| `demo.html` | **separate agent** | frontend UI — not touched by this agent |
