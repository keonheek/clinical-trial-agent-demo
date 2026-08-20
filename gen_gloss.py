"""gen_gloss.py -- one-time bilingual glosses for the LLM-authored text the UI shows.

The Board's chrome is fully bilingual, but the clinical substance (criterion text, trial titles,
rationales, extracted record fields, questions, answer options) is whatever the pipeline produced:
English for the criteria/records, Korean for the answer options. A Korean family cannot read the
first group; an English-reading judge cannot use the second. This script produces a GLOSS sidecar
(source text -> the other language) so the UI can show the original PLUS a labeled gloss, never a
silent machine translation.

  gloss.json:  {sha1(source)[:12]: {"src": "...", "ko": "...", "en": "..."}}

Canonical data is never touched (traces.json md5 stays pinned); this is a serve-time sidecar in
the coverage_map/trial_intent/trial_design family.

Run:  LLM_BACKEND=anthropic python3 gen_gloss.py            # fill in what is missing
      LLM_BACKEND=anthropic python3 gen_gloss.py --rebuild  # redo everything
      python3 gen_gloss.py --report                         # coverage report, no calls
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "gloss.json")
BATCH = 20  # strings per call: big enough to be cheap, small enough to keep the model accurate

SYS_KO = """You translate clinical trial text from English into Korean for a patient's family to read.
Rules:
- Plain Korean a non-medical adult understands; keep the clinical meaning exact.
- Keep standard clinical abbreviations and units as-is (ECOG, HbA1c, mg/dL, NCT ids, DAS28).
- Do not add, soften, or omit anything. No explanations, no hedging language of your own.
- A criterion stays a criterion: "Age >= 18 years" -> "만 18세 이상".
Respond with ONLY a JSON object {"out": ["...", "..."]} with exactly one translation per input,
in the same order. No markdown fences, no commentary."""

SYS_EN = """You translate Korean clinical screening text into English for a clinician reading a
trial-matching tool. Rules:
- Precise clinical English, same meaning, same level of detail. No added interpretation.
- Keep abbreviations, units and lab names as-is (TSH, TRAb, ANC, HbA1c, mg/dL).
- An answer option stays an option: "기록 없음/확인 불가" -> "Not recorded / cannot confirm".
Respond with ONLY a JSON object {"out": ["...", "..."]} with exactly one translation per input,
in the same order. No markdown fences, no commentary."""


def key_of(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def is_korean(text):
    return bool(re.search(r"[가-힣]", text))


def collect_sources():
    """Every distinct user-visible LLM-authored string, from the SERVED payloads."""
    sys.path.insert(0, HERE)
    import importlib.util
    spec = importlib.util.spec_from_file_location("trace_mod", os.path.join(HERE, "api", "trace.py"))
    tm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tm)
    out = set()
    for tr in tm.TRACES:
        for f in tr.get("extraction", []) or []:
            v = f.get("value") or f.get("text") or ""
            if v:
                out.add(str(v))
        for t in tr.get("trials", []):
            out.add(t.get("title", ""))
            if t.get("rationale"):
                out.add(t["rationale"])
            for c in t.get("criteria", []):
                out.add(c.get("text", ""))
                if c.get("reasoning"):
                    out.add(c["reasoning"])
        for t in tr.get("trials", []):
            d = t.get("design") or {}
            for iv in d.get("interventions", []) or []:
                if iv.get("name"):
                    out.add(iv["name"])
                if iv.get("description"):
                    out.add(iv["description"])
            for oc in d.get("primary_outcomes", []) or []:
                if oc.get("measure"):
                    out.add(oc["measure"])
        for q in tr.get("questions", []) or []:
            out.add(q.get("question", ""))
            if q.get("why"):
                out.add(q["why"])
            for o in q.get("options", []) or []:
                out.add(o)
    return sorted(x.strip() for x in out if x and len(x.strip()) > 1)


def translate(batch, to_korean):
    import pipeline
    sys_prompt = SYS_KO if to_korean else SYS_EN
    user = json.dumps({"inputs": batch}, ensure_ascii=False)
    result = pipeline.call_groq("gloss", sys_prompt, user)
    got = result.get("out") or []
    if len(got) != len(batch):  # never silently misalign a translation with its source
        raise ValueError(f"expected {len(batch)} translations, got {len(got)}")
    return [str(x).strip() for x in got]


def main():
    store = {}
    if os.path.exists(OUT) and "--rebuild" not in sys.argv:
        with open(OUT, encoding="utf-8") as f:
            store = json.load(f)
    sources = collect_sources()
    if "--report" in sys.argv:
        have = sum(1 for s in sources if key_of(s) in store)
        print(f"{have}/{len(sources)} strings glossed ({len(store)} entries in {OUT})")
        return
    todo_ko = [s for s in sources if not is_korean(s) and key_of(s) not in store]
    todo_en = [s for s in sources if is_korean(s) and key_of(s) not in store]
    print(f"to gloss: {len(todo_ko)} EN->KO, {len(todo_en)} KO->EN "
          f"({len(sources)} sources, {len(store)} already done)")
    for label, todo, to_ko in (("EN->KO", todo_ko, True), ("KO->EN", todo_en, False)):
        for i in range(0, len(todo), BATCH):
            batch = todo[i:i + BATCH]
            try:
                outs = translate(batch, to_ko)
            except Exception as e:  # noqa: BLE001 -- one bad batch must not lose the rest
                print(f"  {label} batch {i // BATCH + 1}: FAILED ({e}) -- skipped, rerun to retry")
                continue
            for src, tr in zip(batch, outs):
                entry = store.get(key_of(src), {"src": src})
                entry["ko" if to_ko else "en"] = tr
                store[key_of(src)] = entry
            tmp = OUT + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(store, f, ensure_ascii=False, indent=1)
            os.replace(tmp, OUT)  # atomic: a serve-layer reader never sees a torn file
            print(f"  {label} {min(i + BATCH, len(todo))}/{len(todo)}")
    print(f"wrote {OUT}: {len(store)} entries")
    try:
        import anthropic_client
        anthropic_client.stats()
    except Exception:
        pass


if __name__ == "__main__":
    main()
