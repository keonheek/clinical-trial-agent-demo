# Eval notes: the verdict-semantics collision (found 2026-07-12)

## What was wrong

The word `MET` meant three different things in three different places, and nobody had written
down which one was correct.

| Where | What `MET` meant on an **exclusion** criterion |
|---|---|
| `MATCHER_SYS` (the model doing the judging) | "the patient does NOT have the excluded condition", i.e. the patient **passes** |
| `RECOMMENDER_SYS` (the model summarising) | its `ELIGIBLE` clause read `MET` as "the patient HAS the condition"; its `INELIGIBLE` clause read it the other way. The same prompt used both readings two sentences apart, and shipped with the literal instruction `re-read verdict semantics carefully` |
| `eval_labels.json` (the human ground truth) | "the criterion statement is TRUE of this patient". Adult patient, criterion `Age under 18 years old` -> labelled `NOT_MET` |

`make_eval_worksheet.py` handed the labeller the criterion text and the vignette and **never
defined the verdict vocabulary at all**, so the labeller picked its own reading. It picked
consistently: across 20 exclusion criteria it labelled `MET` exactly **zero** times.

So on every exclusion criterion, the system and the ground truth were inverted by construction.
The model could reason perfectly and still be scored wrong.

## What it cost us

Re-scoring the existing run, with nothing changed except mapping the two conventions onto each
other before comparing:

| Metric | As originally measured | With the conventions reconciled |
|---|---|---|
| Criterion accuracy (n=40) | 72.5% | **77.5%** |
| NOT_MET recall | 1/5 = **20%** | 3/5 = **60%** |

Two of the eleven errors were purely a definition collision. The frightening "20% NOT_MET
recall" figure, which looked like a model that cannot spot an ineligible patient, was mostly an
artefact of the measurement. Nine errors are real and remain.

This is also why the number could not be trusted in either direction: the same collision that
made the score look worse than it was could just as easily have hidden a genuine safety failure.

## The fix

Split the one overloaded verdict into two layers, and take the polarity logic away from the
model entirely.

**Layer 1, `verdict` (asked of the model).** Is the criterion *statement* true of this patient?
This is plain reading comprehension. It is the same question for inclusion and exclusion
criteria, so there is no polarity for the model to get backwards. `Age under 18 years old` +
a 9-year-old patient is `MET`; the same criterion + a 54-year-old is `NOT_MET`. This matches
what the human labeller was already doing, so the eval set stays valid as-is.

**Layer 2, `effect` (computed in code).** Does that make the patient pass or fail? This depends
on the criterion's type and is pure logic, so it is a lookup table in `pipeline.py`
(`effect_of`), never an inference:

| type | verdict | effect |
|---|---|---|
| inclusion | MET | PASS |
| inclusion | NOT_MET | FAIL |
| exclusion | MET | **FAIL** (patient has the excluded condition) |
| exclusion | NOT_MET | PASS |
| either | UNKNOWN / UNCERTAIN | REVIEW |

**Eligibility is now decided by a hierarchy, not by a model and not by a score** (`decide_eligibility`):

1. any `FAIL` -> `INELIGIBLE`
2. any `REVIEW` -> `UNCERTAIN`
3. otherwise -> `ELIGIBLE`

A single hard exclusion can no longer be averaged away by a pile of satisfied criteria, which is
the failure mode a single fitness score invites. The recommender model no longer decides
eligibility or ranking at all; it is handed the decision and only writes the rationale.

## Why this matters beyond the bug

The competition scores matching accuracy at 30%. An accuracy number computed against a ground
truth that disagrees with the system about what the labels mean is not a measurement, it is
noise with a decimal point. Fixing the schema is what makes every number downstream of it
(accuracy, question value, re-evaluation gain, ranking) mean anything.

Credit: Jiwoo caught the inconsistency from the UI (exclusion criteria the patient clearly did
not have were being displayed as MET, and the recommender then reported "exclusions met" while
marking the trial ineligible). The code and eval-data confirmation above followed from that.
