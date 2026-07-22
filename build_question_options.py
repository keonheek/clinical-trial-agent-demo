#!/usr/bin/env python3
"""Generate multi-select options for the FROZEN demo questions, into a sidecar file.

traces.json is canonical: regenerating it would drift the criterion text the blind eval
labels join on. Answer options are pure UI affordance and are not part of any scored
artifact, so they are produced once here and stored separately, keyed by question text.
api/trace.py and live_server attach them at serve time.

    python3 build_question_options.py            # fill in anything missing
    python3 build_question_options.py --rebuild  # regenerate all
"""
import argparse
import json
import os
import sys

import pipeline

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "question_options.json")

SYS = """You write answer choices for a clinical trial screening question.
Given the question, why it is being asked, and the eligibility criteria it resolves, produce
3-4 short, MUTUALLY DISTINCT findings a coordinator could tick off a chart (several may be
selected at once), PLUS two closing options in this exact order:
  (a) an explicit clean answer phrased for the question -- "모두 정상 범위" for lab/measurement
      questions, "해당 사항 없음" for history questions;
  (b) "기록 없음/확인 불가".
Ground every finding in the given criteria; never invent a value the criteria do not care
about. Write in Korean, keeping clinical terms and units standard (ANC, HbA1c, mg/dL).
Respond with ONLY {"options": ["...", "..."]} -- no markdown fences, no commentary."""


def options_for(question, why, criteria_texts, model):
    crits = "\n".join(f"- {c}" for c in criteria_texts[:10]) or "- (관련 기준 정보 없음)"
    user = (f"Question: {question}\nWhy it is asked: {why}\n"
            f"Eligibility criteria this question resolves:\n{crits}\n\n"
            "Produce the options per your instructions.")
    result = pipeline.call_groq("question-options", SYS, user, model=model)
    out = []
    for opt in (result.get("options") or []):
        t = str(opt).strip()
        if t and t not in out:
            out.append(t)
    if len(out) > 6:
        out = out[:4] + out[-2:]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=None, help="model id (default: pipeline default)")
    ap.add_argument("--rebuild", action="store_true")
    args = ap.parse_args()
    model = args.model or pipeline.ACTIVE_MODEL

    traces = json.load(open(os.path.join(HERE, "traces.json"), encoding="utf-8"))
    existing = {}
    if os.path.exists(OUT) and not args.rebuild:
        existing = json.load(open(OUT, encoding="utf-8"))

    made = 0
    for tr in traces:
        # criteria text the question plausibly bears on: all undecided criteria for this patient
        crits = [c["text"] for t in tr.get("trials", []) for c in t.get("criteria", [])
                 if c.get("verdict") in ("UNKNOWN", "UNCERTAIN")]
        for q in tr.get("questions", []):
            key = q["question"]
            if key in existing and existing[key]:
                continue
            opts = options_for(key, q.get("why", ""), crits, model)
            if opts:
                existing[key] = opts
                made += 1
                print(f"  + {key[:60]}  -> {len(opts)} options", flush=True)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    print(f"\n{made} new, {len(existing)} total -> {OUT}")

    bad = [k for k, v in existing.items() if len(v) < 3]
    if bad:
        print(f"WARNING: {len(bad)} question(s) got fewer than 3 options")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
