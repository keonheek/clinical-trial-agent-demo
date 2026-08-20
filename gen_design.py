"""gen_design.py -- fetch each trial's patient-facing design facts into trial_design.json.

What a PATIENT gets from joining (interventions: drug/device/procedure/behavioral + what it is)
and what the trial measures about them (primary outcomes + when). Pure network fetch from the
ClinicalTrials.gov v2 API (public domain) -- NO LLM, and trials_raw*.json is never touched
(the criterion-text join the blind eval labels depend on stays safe; this is a NEW sidecar,
same pattern as coverage_map/trial_intent).

Run:  python3 gen_design.py            # fetch all pools (demo + extra), skip already-fetched
      python3 gen_design.py --refetch  # refetch everything
Serve: api/trace.py + live_server.py merge trial_design.json at load.
"""
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "trial_design.json")
BASE = "https://clinicaltrials.gov/api/v2/studies/"
FIELDS = "protocolSection.armsInterventionsModule,protocolSection.outcomesModule,protocolSection.designModule,protocolSection.contactsLocationsModule"


def all_nct_ids():
    ids = []
    for name in ("trials_raw.json", "trials_raw_extra.json"):
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for block in data.values():
            for t in block.get("trials", []):
                if t["nct_id"] not in ids:
                    ids.append(t["nct_id"])
    return ids


def fetch_one(nct):
    url = f"{BASE}{nct}?fields={urllib.request.quote(FIELDS)}"
    with urllib.request.urlopen(url, timeout=30) as r:
        study = json.load(r)
    ps = study.get("protocolSection", {})
    ai = ps.get("armsInterventionsModule", {})
    om = ps.get("outcomesModule", {})
    dm = ps.get("designModule", {})
    interventions = [{
        "type": iv.get("type", ""),
        "name": iv.get("name", ""),
        "description": (iv.get("description", "") or "")[:400],
    } for iv in ai.get("interventions", [])][:6]
    outcomes = [{
        "measure": (oc.get("measure", "") or "")[:200],
        "timeframe": (oc.get("timeFrame", "") or "")[:120],
    } for oc in om.get("primaryOutcomes", [])][:5]
    lm = ps.get("contactsLocationsModule", {})
    countries = []
    for loc in lm.get("locations", []) or []:
        c = loc.get("country", "")
        if c and c not in countries:
            countries.append(c)
    return {
        "study_type": dm.get("studyType", ""),
        "interventions": interventions,
        "primary_outcomes": outcomes,
        "countries": countries[:8],
    }


def main():
    existing = {}
    if os.path.exists(OUT) and "--refetch" not in sys.argv:
        with open(OUT, encoding="utf-8") as f:
            existing = json.load(f)
    out = dict(existing)
    ids = all_nct_ids()
    for i, nct in enumerate(ids):
        if nct in out:
            continue
        try:
            out[nct] = fetch_one(nct)
            print(f"[{i + 1}/{len(ids)}] {nct}: {len(out[nct]['interventions'])} interventions, "
                  f"{len(out[nct]['primary_outcomes'])} outcomes")
        except Exception as e:  # noqa: BLE001 -- a single flaky fetch must not kill the run
            print(f"[{i + 1}/{len(ids)}] {nct}: FAILED ({e}) -- skipped, rerun to retry")
        time.sleep(0.6)
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"wrote {OUT}: {len(out)} trials")


if __name__ == "__main__":
    main()
