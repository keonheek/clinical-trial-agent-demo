"""gen_extra.py -- generate the EXTRA demo patients (E001-...) end to end.

Writes ONLY the *_extra artifacts; the frozen canonical set (traces.json, coverage_map.json,
trial_intent.json) is never touched, so the md5 pin and the blind-label pairing stay intact.

  patients_extra.json      (input, hand-authored vignettes -- clearly synthetic)
  trials_raw_extra.json    real recruiting trials from ClinicalTrials.gov per patient
  traces_extra.json        full pipeline output per patient (same shape as traces.json)
  trial_intent_extra.json  intent sidecar for the new trials (build_trial_intent rules)
  coverage_map_extra.json  raw-criteria-count sidecar for the new trials

Run:  LLM_BACKEND=anthropic python3 gen_extra.py            (spends the challenge credit)
      python3 gen_extra.py --fetch-only                     (network but no LLM: trials only)

Serve-time merge: api/trace.py and live_server.py load *_extra.json next to the canonical
files when present.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def fetch_extra():
    import fetch_trials as ft
    with open(os.path.join(HERE, "patients_extra.json"), encoding="utf-8") as f:
        patients = json.load(f)
    # Query lists are need-shaped (2nd fetch round, 08-19): the first round's single generic
    # queries returned pools where the patient's designed need-match never fired (e.g. E004's
    # comfort patient got zero supportive-intent trials). Multi-query merge, dedupe, cap 4.
    queries = {
        "E001": ["severe eosinophilic asthma"],
        "E002": ["thyroid nodule fine needle aspiration", "thyroid nodule diagnosis", "thyroid nodule"],
        "E003": ["type 2 diabetes registry", "type 2 diabetes observational", "type 2 diabetes"],
        "E004": ["cancer palliative care", "cancer symptom management", "pancreatic cancer supportive care"],
        "E005": ["ulcerative colitis induction", "ulcerative colitis biologic", "ulcerative colitis"],
    }
    only = None
    for a in sys.argv:
        if a.startswith("--only="):
            only = set(a.split("=", 1)[1].split(","))
    prev = {}
    if os.path.exists(os.path.join(HERE, "trials_raw_extra.json")):
        with open(os.path.join(HERE, "trials_raw_extra.json"), encoding="utf-8") as f:
            prev = json.load(f)
    out = {}
    for p in patients:
        pid = p["patient_id"]
        if only and pid not in only and pid in prev:
            out[pid] = prev[pid]
            print(f"Keeping existing pool for {pid}")
            continue
        merged, seen = [], set()
        for q in queries[pid]:
            if len(merged) >= 4:
                break
            print(f"Fetching: {q} (for {pid}) ...")
            studies = ft.fetch_condition(q, 6)
            for t in (ft.normalize(s) for s in studies):
                if t["eligibility_criteria_raw"] and t["nct_id"] not in seen:
                    seen.add(t["nct_id"])
                    merged.append(t)
            print(f"  -> pool now {len(merged)}")
            time.sleep(1)
        out[pid] = {"query_used": " + ".join(queries[pid]), "primary_query": queries[pid][0],
                    "fallback_used": False, "note": "", "trials": merged[:4]}
    with open(os.path.join(HERE, "trials_raw_extra.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("wrote trials_raw_extra.json")
    return out


def sidecars(trials_raw_extra):
    import build_trial_intent as bti
    import pipeline
    intent, coverage = {}, {}
    for _pid, block in trials_raw_extra.items():
        for t in block["trials"]:
            intent[t["nct_id"]] = bti.classify_trial_intent(t)
            coverage[t["nct_id"]] = pipeline.estimate_raw_criteria_count(t["eligibility_criteria_raw"])
    with open(os.path.join(HERE, "trial_intent_extra.json"), "w", encoding="utf-8") as f:
        json.dump(intent, f, ensure_ascii=False, indent=1)
    with open(os.path.join(HERE, "coverage_map_extra.json"), "w", encoding="utf-8") as f:
        json.dump(coverage, f, ensure_ascii=False, indent=1)
    print(f"wrote sidecars: {len(intent)} trials")


def generate(trials_raw_extra):
    import pipeline
    with open(os.path.join(HERE, "patients_extra.json"), encoding="utf-8") as f:
        patients = json.load(f)
    only = None
    for a in sys.argv:
        if a.startswith("--only="):
            only = set(a.split("=", 1)[1].split(","))
    prev = {}
    if os.path.exists(os.path.join(HERE, "traces_extra.json")):
        with open(os.path.join(HERE, "traces_extra.json"), encoding="utf-8") as f:
            prev = {t["patient_id"]: t for t in json.load(f)}
    traces = []
    for p in patients:
        pid = p["patient_id"]
        if only and pid not in only and pid in prev:
            traces.append(prev[pid])
            print(f"=== {pid}: keeping existing trace ===")
            continue
        print(f"\n=== {pid}: {p['condition']} ===")
        trace = pipeline.run_patient(p, trials_raw_extra[pid])
        traces.append(trace)
        # incremental save so a mid-run failure loses nothing
        with open(os.path.join(HERE, "traces_extra.json"), "w", encoding="utf-8") as f:
            json.dump(traces, f, ensure_ascii=False, indent=1)
        print(f"  saved ({len(traces)} so far)")
    print("\nwrote traces_extra.json")
    try:
        import anthropic_client
        anthropic_client.stats()
    except Exception:
        pass


if __name__ == "__main__":
    if os.path.exists(os.path.join(HERE, "trials_raw_extra.json")) and "--refetch" not in sys.argv and not any(a.startswith("--only=") for a in sys.argv):
        with open(os.path.join(HERE, "trials_raw_extra.json"), encoding="utf-8") as f:
            raw = json.load(f)
        print("using existing trials_raw_extra.json (pass --refetch to refresh)")
    else:
        raw = fetch_extra()
    sidecars(raw)
    if "--fetch-only" not in sys.argv:
        generate(raw)
