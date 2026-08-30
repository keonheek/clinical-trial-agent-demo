#!/usr/bin/env python3
"""Fill options_en for every question in questions_v2.json (English mode shows English options,
Korean as the secondary line). Backend-aware (pipeline.call_groq), so it runs on the subscription
with LLM_BACKEND=claude. Skips questions that already carry options_en."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for _k in ("CLAUDECODE", "CLAUDE_CODE_CHILD_SESSION"):
    os.environ.pop(_k, None)
os.environ.setdefault("LLM_BACKEND", "claude")
os.environ.setdefault("CLAUDE_PIPELINE_MODEL", "claude-sonnet-5")
from pipeline import call_groq  # noqa: E402
from gen_option_en import SYSTEM_PROMPT  # noqa: E402

PATH = os.path.join(HERE, "questions_v2.json")


def main():
    data = json.load(open(PATH, encoding="utf-8"))
    todo = [q for v in data.values() for q in v["questions"] if not q.get("options_en")]
    print(f"{len(todo)} questions need options_en")
    for q in todo:
        obj = call_groq("option_en", SYSTEM_PROMPT, json.dumps(q["options"], ensure_ascii=False, indent=1))
        en = obj.get("translations") if isinstance(obj, dict) else None
        if not isinstance(en, list) or len(en) != len(q["options"]):
            print("  mismatch, skipped:", q["question"][:50])
            continue
        q["options_en"] = [str(x).strip() for x in en]
        json.dump(data, open(PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("  ok:", q["question"][:50], flush=True)


if __name__ == "__main__":
    main()
