#!/usr/bin/env python3
"""
make_eval_worksheet.py — dump a VERDICT-FREE worksheet of (patient, trial, criterion) rows
from traces.json so a human can hand-label expected verdicts BLIND to what the pipeline said.

This exists to keep eval_labels.json honest: labels must come from reading the criterion text
+ original vignette alone, never from looking at the matcher's own output (that would make the
eval circular). Labels are always against the PRE-REEVAL verdict (trials[].criteria[], not the
reeval block) per the task's "pre-answer-round ground truth" requirement.

Run:
    python3 make_eval_worksheet.py
Writes:
    eval_worksheet.json   -- [{patient_id, patient_text, nct_id, criterion_text, type}, ...]
    (no verdict field anywhere in this file, by design)
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    with open(os.path.join(HERE, "traces.json")) as f:
        traces = json.load(f)

    rows = []
    for t in traces:
        pid = t["patient_id"]
        ptext = t["patient_text"]
        for trial in t["trials"]:
            for c in trial["criteria"]:
                rows.append({
                    "patient_id": pid,
                    "patient_text": ptext,
                    "nct_id": trial["nct_id"],
                    "criterion_text": c["text"],
                    "type": c["type"],
                })

    with open(os.path.join(HERE, "eval_worksheet.json"), "w") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"Wrote eval_worksheet.json with {len(rows)} verdict-free rows across "
          f"{len(set(r['patient_id'] for r in rows))} patients")


if __name__ == "__main__":
    main()
