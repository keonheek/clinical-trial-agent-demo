# SDIC Trial-Match Demo — Interactive Clinical Trial Recommendation

Backend for a demo built for the SKKU "Healthcare Agentic AI Challenge 2026" task: a
multi-agent system that matches patients to clinical trials with evidence, detects missing
information, chooses a next action for each undecided criterion, generates clarifying
questions, and returns a per-patient recommendation with a deterministic priority order.

This is a capability demo, not a validated clinical tool. See disclaimer at the bottom.

## What it does

1. Pulls REAL, currently-recruiting trials from ClinicalTrials.gov for all 10 official sample
   patients (S001-S010 from the challenge's synthetic-patients.json). `TRIALS_PER_PATIENT = 4`,
   so 40 patient-trial pairs are evaluated end to end out of the 52 fetched.
2. Runs a 6-role LLM pipeline plus a re-evaluation loop that parses trial eligibility criteria,
   extracts patient facts with verbatim evidence, matches each criterion, detects gaps in the
   patient's record, and generates clarifying questions. The LLM backend is switchable via the
   `LLM_BACKEND` env var; the default is `anthropic` (`claude-haiku-4-5`, funded by the
   challenge's API credit — this project's sanctioned exception to an otherwise-$0 posture),
   with Groq free tier, local Ollama, and the local Claude Code subscription as alternatives.
   Every call is cached per backend+model, so a re-run costs nothing.
3. Decides eligibility and recommendation priority **in code, never in the model**:
   `pipeline.decide_eligibility` (a hierarchy — one hard FAIL is never averaged away by a pile of
   passes) followed by `ranking.rank_trials` (see [Priority order](#priority-order-추천-우선순위)).
   The sixth role, the recommender, is handed that decision and writes the rationale for it.
4. Serves the result to `site.html`, the judge-facing UI deployed at
   https://sdic-trial-demo.vercel.app — `api/trace.py` for the precomputed traces, `api/answer.py`
   for a live answer round. `live.html` + `live_server.py` are the local development UI.
   `traces.js` (`window.TRACES = [...]`) remains for the static viewer.

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
                | decide_eligibility   |   <- CODE. No LLM call.
                | + ranking.rank_trials|      eligibility class,
                |  hierarchy, then the |      rank, rank_reason,
                |  priority-order key  |      rank_basis
                +----------------------+
                          |
                          v
                +----------------------+
                | (f) recommender      |   <- 1 call per patient
                |  narrates the already|
                |  -decided verdict and|
                |  rank -- decides none |
                +----------------------+
                          |
                          v
                traces.json / traces.js
                (window.TRACES = [...])
                          |
                          v
     site.html (deployed judge UI)  ·  live.html (local dev UI)
```

Each box (a)-(f) is an independent LLM call with its own system prompt — no single
mega-prompt does everything. Total calls per patient with 4 trials: 1 (extractor) + 4
(criteria-parser) + 4 (matcher) + 1 (gap-detector) + 1 (question-generator) + 1
(recommender) = 12. For all 10 official patients: 120 calls on the first run; $0 on every
re-run because every call is cached to disk (`cache/`, keyed on role+model+prompt hash).

## How to re-run

```bash
cd projects/sdic-trial-demo
python3 fetch_trials.py     # re-pulls live trial data (skip if trials_raw.json is fine)
python3 pipeline.py --generate   # runs the 6-role pipeline, writes traces.json + traces.js
python3 assert_traces.py    # verifies traces, actions, and the golden ranking order
python3 ranking.py          # ranking self-tests; --golden checks expected_ranking.json
python3 action_policy.py    # uncertainty/action self-tests
```

The default backend reads `ANTHROPIC_NEW_KEY` (falling back to `ANTHROPIC_API_KEY`) from the
environment or from `.env` / `.env.local` at the repo root; `LLM_BACKEND=groq` reads
`GROQ_API_KEY` instead, and `LLM_BACKEND=ollama` needs no key at all. No dependencies beyond
the Python 3 standard library (`urllib`, `json`, `hashlib`).

Regenerating `traces.json` is a deliberate, gated act: the blind evaluation labels join to
traces on exact criterion text, so a regeneration on a different backend silently unpairs them.
CI pins the file by md5 and re-asserts the canonical accuracy on every push. Ranking is
therefore applied **in memory** at serve time and never written back.

To force a clean re-run with fresh LLM calls: `rm -rf cache/` first (this spends real API
quota again).

## Dependencies

- Python 3 standard library only (no pip installs required: `urllib.request`, `json`,
  `hashlib`, `time`, `os`).
- One LLM backend, selected by `LLM_BACKEND`: `anthropic` (default, `claude-haiku-4-5`),
  `groq` (free tier, `llama-3.3-70b-versatile`), `ollama` (local `qwen3.6`), or `claude`
  (local Claude Code subscription). All are called in JSON mode.
- ClinicalTrials.gov API v2 (`https://clinicaltrials.gov/api/v2/studies`), no key required.
- `ranking.py`, `action_policy.py`, and `evidence.py` import no LLM client at all — they are
  pure modules, which is what makes them safe to bundle into the `api/` serverless handlers.

## Data sources & licenses

- **ClinicalTrials.gov** (U.S. National Library of Medicine / NIH): trial records, titles,
  phases, and eligibility criteria text are public domain (U.S. Government work). See
  https://clinicaltrials.gov/about-site/terms-conditions. All 52 trials in `trials_raw.json`
  are REAL, currently-recruiting studies pulled live via the public API v2 — not
  fabricated. Query used per patient is recorded in `trials_raw.json` under `query_used`.
- **Patient vignettes** (`patients.json`): the competition's own published sample patients
  (S001-S010), copied verbatim from the task brief — not real patient data.
- **LLM inference** is backend-switchable via `LLM_BACKEND`, and the pipeline is not tied to any
  one model. Default is `anthropic` / `claude-haiku-4-5` (funded by the challenge's API credit —
  the sanctioned exception to this project's $0 default); alternatives are Groq free tier
  (`llama-3.3-70b-versatile`), local Ollama (`qwen3.6`, $0), and the local Claude Code
  subscription. Every call is cached per backend+model, so switching backends never reuses
  another's answers. `model_bakeoff_full.json` records the same 51 blind stress labels scored on
  three models — verdict accuracy 80.4% / 76.5% / 72.6% (Opus 4.8 / Sonnet 5 / Haiku 4.5), with
  zero wrongly-passed criteria on all three, because the safety properties live in the code
  layer rather than in the model.

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
  sufficiency (does the quote support the conclusion?). `assess_evidence()` rejects e.g. a
  *suspected* imaging finding standing in for a *confirmed* diagnosis, and routes it to VERIFY.
  The matcher emits `source_type` / `confirmation_level` / `directness` per criterion and
  `pipeline.apply_evidence_sufficiency` gates the verdict on **both** matching passes — the
  initial match and the re-evaluation round — as well as in `api/answer.py`. Two limits are
  documented rather than papered over: the required confirmation level is currently a blanket
  `"confirmed"` instead of per-criterion, and the same model both issues the verdict and grades
  its own evidence, which can defeat the layer (see `EVIDENCE-SELF-GRADING.md`; the obvious
  blanket fix would regress criteria such as ECOG where clinical judgement *is* the standard
  measurement, so it was recorded instead of patched).

A trial-level rule sits on top of the criterion-level table: once a trial carries a hard FAIL, its
remaining undecided criteria are moot, so `apply_trial_level_actions` rewrites their action to
STOP with an `action_scope` of `trial` and a Korean `action_reason`. The criterion's own
`uncertainty_type` is untouched — it still names the cause; only the action changes. Across the 40
frozen patient-trial pairs (374 criteria) this yields ASK 201 / STOP 86 / ESCALATE 11, with 76
criteria already decided.

**Question-priority API (for the frontend cards).** Each clarifying question is served with
`affects_trials`, `affects_criteria`, and `may_change_rank`, computed deterministically from the
trace by `action_policy.enrich_questions`. Both `api/trace.py` (deployed) and `live_server.py`
(local) attach these at serve time and return the questions sorted most-impactful first, so the
frontend consumes served values rather than hardcoded ones. Frozen traces carry no gap-to-question
links, so the enrichment falls back to token overlap there. Run `python3 action_policy.py` and
`python3 evidence.py` for the self-tests.

## Priority order (추천 우선순위)

`ranking.rank_trials` decides the per-patient recommendation order. It is a lexicographic key over
facts of the trial record and counts derived in code — no model opinion enters it — and each trial
is stamped with `rank`, `rank_reason` (a one-line Korean explanation), `rank_basis` (UI chips), and
`ranking_version`.

| Tier | Term | Order |
|---|---|---|
| 0 | eligibility class | `ELIGIBLE` < `UNCERTAIN` < `INELIGIBLE` (`decide_eligibility`) |
| 1 | blocking criteria | fewer `FAIL` effects first |
| 2 | 중재 목적 (intent) | therapeutic < supportive < care_delivery < observational; low-confidence or unclassified is demoted to the observational tier |
| 3 | Phase burden | PHASE4 < PHASE3 < PHASE2 < PHASE1 = EARLY_PHASE1; NA = middle |
| 4 | coverage penalty | parsed / raw_estimated < 0.5 sinks below fully-read trials |
| 5 | unresolved ratio | `REVIEW` / parsed, ascending |
| 6 | unresolved count | `REVIEW` count, ascending |
| 7 | nct_id | stable last resort |

Design intent: within one eligibility class, a trial that could be a treatment opportunity is
reviewed first, and a low-confidence classification never lifts a trial above a confirmed one.
A hard exclusion is never out-ranked at any tier — `hard_exclusion_holds` asserts this and holds
on all 10 patients.

Measured on the frozen demo set when the key shipped (2026-08-16): 24 of 40 ranks move, the rank-1
trial changes for 5 of 10 patients, maximum displacement is 2 positions. `eval.py` never reads
`rank`, so the canonical blind-label accuracy (82.5%, n=40) is unaffected. The resulting order is
pinned in `expected_ranking.json` and checked by `assert_traces.py` Check 7 and by CI, so any
change to the key produces a visible golden diff.

Intent and coverage arrive from sidecars (`trial_intent.json`, `coverage_map.json`) keyed by
`nct_id`, and the server always prefers the sidecar over any `trial_intent` attached to a request
body — `api/answer.py` passes `trust_attached=False` so a client cannot rig the sort.

Known limitation: patient burden is currently proxied by trial phase alone. Visit count, travel
distance, and study duration are not in the record; a `trial_design` sidecar is the intended fix.

## Medical disclaimer

**출력 결과는 의학적 자문이 아닌 참고용입니다.**
(The output of this system is for reference only and does NOT constitute medical advice.
It is a hackathon capability demo and has not been clinically validated. Trial eligibility
must always be confirmed with the trial's own study team and a qualified clinician before
any enrollment decision.)

## Handover / opening the exports (Windows)

Non-technical guide, Korean first: [HANDOVER.md](HANDOVER.md) — which export to use (xlsx vs CSV), how to open each in Excel, the browser view, and how to run the app locally.

## Files

| File | Purpose |
|---|---|
| `fetch_trials.py` | pulls real recruiting trials from ClinicalTrials.gov v2 |
| `patients.json` | 10 official patient vignettes, S001-S010, verbatim from the task brief |
| `trials_raw.json` | raw fetched trial data (52 trials; one query per patient, recorded inline) |
| `pipeline.py` | 6-role multi-agent pipeline; `decide_eligibility` and `recommend` live here |
| `ranking.py` | recommendation priority key — pure module, self-tested, imports no LLM client |
| `expected_ranking.json` | golden per-patient order over the frozen traces; pinned in CI |
| `trial_intent.json` | sidecar: therapeutic / supportive / care_delivery / observational per NCT, with confidence and the signals behind it |
| `coverage_map.json` | sidecar: criterion-like clause count in each raw protocol, denominator of the coverage ratio |
| `action_policy.py` | uncertainty taxonomy, action table, trial-level STOP rule, question-priority scorer (pure, self-tested) |
| `evidence.py` | evidence-sufficiency layer: confirmation/directness rules (pure, self-tested) |
| `anthropic_client.py`, `groq_client.py`, `ollama_client.py`, `claude_client.py` | backend wrappers: on-disk caching + exponential backoff |
| `api/trace.py`, `api/answer.py` | Vercel serverless endpoints behind the deployed UI |
| `site.html` | judge-facing UI, deployed at https://sdic-trial-demo.vercel.app; self-contained, no CDN |
| `live.html`, `live_server.py` | local development UI and its interactive re-eval server |
| `assert_traces.py` | verification: verbatim evidence quotes, structural shape, ranking invariants, golden order |
| `eval.py`, `eval_labels.json`, `eval_results.json` | blind-label scoring of the canonical set (n=40) |
| `stress_eval.py`, `eval_labels_stress.json` | blind-label scoring of the stress set (n=51; 5 conditions × 7 corruptions) |
| `model_bakeoff.py`, `model_bakeoff_full.json` | the same stress labels scored across three models |
| `traces.json`, `traces.js` | frozen pipeline output; never regenerate without relabelling |
| `cache/` | on-disk LLM response cache, keyed on role+model+prompt hash |
| `demo.html`, `index.html` | earlier static trace viewer, kept for reference |
