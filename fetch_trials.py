#!/usr/bin/env python3
"""
fetch_trials.py — Pull real, currently-recruiting trials from ClinicalTrials.gov API v2
for the 3 sample patients in the SKKU Healthcare Agentic AI Challenge 2026 task.

Data source: ClinicalTrials.gov API v2 (https://clinicaltrials.gov/api/v2/studies)
License: U.S. National Library of Medicine — public domain / freely reusable.
         https://clinicaltrials.gov/about-site/terms-conditions (data is US Government work, PD)

No API key required. Run:
    python3 fetch_trials.py
Writes: trials_raw.json
"""
import json
import time
import urllib.request
import urllib.parse

BASE = "https://clinicaltrials.gov/api/v2/studies"

# condition query -> patient id this maps to (for traceability in the output file)
CONDITIONS = [
    {"patient_id": "S002", "query": "Graves disease hyperthyroidism", "n": 5},
    {"patient_id": "S008", "query": "idiopathic pulmonary fibrosis", "n": 5},
    {"patient_id": "S001", "query": "acute pancreatitis", "n": 6},
]

FIELDS = "NCTId,BriefTitle,Phase,EligibilityCriteria,OverallStatus,Condition"


def fetch_condition(query, n):
    params = {
        "query.cond": query,
        "filter.overallStatus": "RECRUITING",
        "pageSize": str(n),
        "fields": FIELDS,
    }
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "sdic-trial-demo/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    return data.get("studies", [])


def normalize(study):
    ps = study.get("protocolSection", {})
    ident = ps.get("identificationModule", {})
    design = ps.get("designModule", {})
    elig = ps.get("eligibilityModule", {})
    status = ps.get("statusModule", {})
    cond_mod = ps.get("conditionsModule", {})
    return {
        "nct_id": ident.get("nctId"),
        "title": ident.get("briefTitle"),
        "phase": (design.get("phases") or ["NA"])[0] if design.get("phases") else "NA",
        "status": status.get("overallStatus"),
        "conditions": cond_mod.get("conditions", []),
        "eligibility_criteria_raw": elig.get("eligibilityCriteria", ""),
    }


def main():
    out = {}
    for c in CONDITIONS:
        print(f"Fetching: {c['query']} (for patient {c['patient_id']}) ...")
        studies = fetch_condition(c["query"], c["n"])
        normalized = [normalize(s) for s in studies]
        # keep only studies that actually have eligibility text
        normalized = [s for s in normalized if s["eligibility_criteria_raw"]]
        out[c["patient_id"]] = {
            "query_used": c["query"],
            "trials": normalized,
        }
        print(f"  -> got {len(normalized)} trials with eligibility text")
        time.sleep(1)  # be polite to the public API

    with open("trials_raw.json", "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("Wrote trials_raw.json")


if __name__ == "__main__":
    main()
