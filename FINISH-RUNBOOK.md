# SDIC demo — finish chain (written 2026-07-08 ~night, session at 90% usage)
Goal: competition-complete. Keonhee is staying up for this.
State when written: pipeline.py v2 RUNNING (10 patients + reeval, Groq free tier, slow by
rate limits); traces.json on disk still 3-patient/no-reeval until it exits and writes.
Watcher biub4sm39 wakes the session on process exit.

Chain (execute in order, verify each on the artifact):
1. Pipeline exited? -> python3 -c "import json;t=json.load(open('traces.json'));print(len(t),sum(1 for x in t if 'reeval' in x))"
   Expect 10/10. Run: python3 assert_traces.py (must pass). If process died early: rerun `python3 pipeline.py` (idempotent).
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
