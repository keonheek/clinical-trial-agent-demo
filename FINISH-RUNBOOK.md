# SDIC demo — finish chain (written 2026-07-08 ~night, session at 90% usage)
Goal: competition-complete. Keonhee is staying up for this.
State when written: pipeline.py v2 RUNNING (10 patients + reeval, Groq free tier, slow by
rate limits); traces.json on disk still 3-patient/no-reeval until it exits and writes.
Watcher biub4sm39 wakes the session on process exit.

Chain (execute in order, verify each on the artifact):
1. Pipeline exited? -> python3 -c "import json;t=json.load(open('traces.json'));print(len(t),sum(1 for x in t if 'reeval' in x))"
   Expect 10/10. Run: python3 assert_traces.py (must pass). If process died early: rerun `python3 pipeline.py --generate` (idempotent).
2. Eval: python3 make_eval_worksheet.py -> dispatch ONE sonnet agent to blind-label eval_labels.json
   (per eval.py docstring), run eval.py, write real eval_results.js (window.EVAL={accuracy,n,confusion}).
3. Verify viewer: demo.html?selftest=1 via Playwright -> expect 11/11 PASS.
4. Fresh adversarial judge agent (SKKU judge persona, no fabrication check, UI reference-pass:
   Linear/Vercel-dashboard school; em dashes already stripped from html, PDF must be REGENERATED from slides.html).
5. Apply fixes -> commit -> push -> redeploy GitHub Pages -> curl the live URL, confirm v2 (stage ⑤ present).
6. Tell Keonhee: final URL + eval accuracy + what changed. He will not sleep until this is done.
Repo: /Users/gunny/Dev/MCP_Agentic_AI/projects/sdic-trial-demo ($0 posture: Groq free tier only, no paid APIs)

## Demo-day answer script (added 2026-07-22, verified live on the deployed URL)

Patient: S002 (Graves'). Paste into the question cards, Enter submits. Verified effect:
summary strip 미해결 31→28, 남은 질문 3→2, TRAb criterion UNKNOWN → MET chip with the typed
labs quoted as evidence.

- Labs: TSH <0.01 mIU/L (suppressed), free T4 3.2 ng/dL (elevated), TRAb positive at 8 IU/L. CBC, liver and renal panels within normal limits.
- Treatment history (rank-mover): Diagnosed with Graves' disease 2 months ago; on methimazole 10 mg daily for 6 weeks; no prior surgery or radioiodine therapy.
- Comorbid: No history of cancer, cardiac disease, hypertension, or neurological conditions.

UI features to narrate: summary strip recomputes per answer; changed criteria carry
before→after chips; rank changes show movement chips; coverage pill per trial (39% one
is the coverage-blindness talking point).

### RANKING CHANGE — re-verify the script before demo day (added 2026-08-16)

The recommendation priority key shipped on 2026-08-16 (`ranking.py`, RANKING_VERSION 2026-08-16;
eligibility class → blocking count → 중재 목적 → Phase 부담 → coverage penalty → unresolved ratio).
The script above is NOT deleted and its criterion-level effects still stand, but the RANK NARRATION
in it predates the new key.

- **S002's rank-1 trial is now `NCT05461820` (PHASE4, therapeutic), not `NCT06963203`.** Under the
  old key the observational Phase-NA trial `NCT06963203` sat at rank 1; it is now rank 2.
  Confirmed against `expected_ranking.json`, which pins the served order for all 10 patients.
- The frozen (pre-key) order per patient rides on the trace as `frozen_rank_order`, but **no UI
  renders it** — it is visible only in the raw `/api/trace?patient_id=…` JSON. To show the
  before/after on demo day, keep that JSON endpoint open in a second tab as the backup.
- **What still needs a live check:** the three answers above were verified live on the deployed URL
  on 2026-07-22 — 미해결 31→28, 남은 질문 3→2, TRAb UNKNOWN → MET. Those criterion-level effects are
  unaffected by ranking. What is NOT re-verified is which trials move rank and by how much AFTER
  those answers land, since the answer round re-ranks through `pipeline.recommend` with the new key.
  Re-run the three answers in one live round before demo day and re-write the rank narration from
  what the screen actually shows.
- **This spends the metered Anthropic key** (a real answer round is a live matcher call), so it is
  Keonhee's call to fire, not an autonomous step. Everything else in this runbook is offline.
