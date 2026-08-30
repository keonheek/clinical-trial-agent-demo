#!/usr/bin/env python3
"""Regenerate the clarifying questions of the 10 frozen demo patients with the current
question generator (Korean question text, Korean self-contained options, per-option direction)
into a sidecar -- traces.json stays byte-identical (it is md5-pinned to the blind eval labels).

api/trace.py serves questions_v2.json in place of trace["questions"] when a patient has an entry.

    LLM_BACKEND=claude python3 gen_questions_v2.py          # subscription, ~2 calls per patient
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for _k in ("CLAUDECODE", "CLAUDE_CODE_CHILD_SESSION"):
    os.environ.pop(_k, None)
os.environ.setdefault("LLM_BACKEND", "claude")
os.environ.setdefault("CLAUDE_PIPELINE_MODEL", "claude-sonnet-5")

from pipeline import detect_gaps, generate_questions  # noqa: E402

OUT = os.path.join(HERE, "questions_v2.json")


def main():
    patients = {p["patient_id"]: p for p in json.load(open(os.path.join(HERE, "patients.json"), encoding="utf-8"))}
    traces = json.load(open(os.path.join(HERE, "traces.json"), encoding="utf-8"))
    out = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    for tr in traces:
        pid = tr["patient_id"]
        if pid in out or pid not in patients:
            continue
        flat = [{"nct_id": t["nct_id"], "text": c["text"], "verdict": c["verdict"], "action": c.get("action"),
                 "effect": c.get("effect")} for t in tr["trials"] for c in t["criteria"]]
        gaps = tr.get("gaps") or detect_gaps(patients[pid], flat)
        qs = generate_questions(patients[pid], gaps)
        ok = [q for q in qs if q.get("question_ko") and q.get("option_directions")]
        print(f"{pid}: {len(gaps)} gaps -> {len(qs)} questions ({len(ok)} complete)", flush=True)
        out[pid] = {"gaps": gaps, "questions": qs}
        json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("wrote", OUT, len(out), "patients")


if __name__ == "__main__":
    main()
