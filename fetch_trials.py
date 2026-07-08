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
# `fallback_query` + `note` are used ONLY when the primary query's real, currently-recruiting
# trials are not clinically relevant (verified by hand against ClinicalTrials.gov API v2 on
# 2026-07-08 -- see README "Trial sourcing notes" for the manual check that justified each one).
CONDITIONS = [
    {"patient_id": "S001", "query": "acute pancreatitis", "n": 6},
    {"patient_id": "S002", "query": "Graves disease hyperthyroidism", "n": 5},
    {"patient_id": "S003", "query": "nephrotic syndrome", "n": 6,
     "note": "Query returns a mix of adult+pediatric nephrotic-syndrome trials; several are "
             "explicitly pediatric (e.g. Blinatumomab for CNI-resistant SRNS in children, "
             "Telitacicept in pediatric frequently-relapsing/steroid-dependent NS) so used directly, "
             "no substitution needed."},
    {"patient_id": "S004", "query": "bladder cancer", "n": 5},
    {"patient_id": "S005", "query": "migraine", "n": 5},
    {"patient_id": "S006", "query": "mucormycosis", "n": 5,
     "note": "5 recruiting trials directly on mucormycosis exist (biomarkers, imaging prognosis, "
             "antifungal regimens, pediatric PK, facial reconstruction post rhino-orbital-cerebral "
             "disease) -- used directly, diabetes-complication fallback not needed."},
    {"patient_id": "S007", "query": "hypertrophic pyloric stenosis", "n": 8,
     "fallback_query": "infant vomiting", "fallback_query_2": "pediatric gastrointestinal obstruction",
     "fallback_n": 5, "force_fallback": True,
     # excluded: fuzzy-matched noise unrelated to infant pyloric/GI obstruction (chemo-induced
     # vomiting in cancer patients; a B-cell lymphoma drug trial) -- verified by hand 2026-07-08
     "fallback_exclude_nct": ["NCT03118986", "NCT05544019"],
     "note": "VERIFIED FALLBACK: 'hypertrophic pyloric stenosis' / 'infant pyloric stenosis' / "
             "'infantile hypertrophic pyloric stenosis' all return zero or clinically irrelevant "
             "recruiting trials (ClinicalTrials.gov's fuzzy condition matching pulls unrelated "
             "pediatric oncology studies) -- checked by hand 2026-07-08. This makes clinical sense: "
             "pyloric stenosis is cured by a single pyloromyotomy, not an active drug/behavioral "
             "trial target. Nearest available real recruiting trial ('Prevalence and Natural "
             "History of Functional Gastrointestinal Disorders Among At-risk Infants', "
             "NCT06031025) plus other infant-GI trials substituted and flagged honestly here and "
             "in trials_raw.json as `fallback_used: true`."},
    {"patient_id": "S008", "query": "idiopathic pulmonary fibrosis", "n": 5},
    {"patient_id": "S009", "query": "infectious mononucleosis", "n": 5,
     "note": "Dedicated acute-infectious-mononucleosis treatment trials are rare on "
             "ClinicalTrials.gov; the 5 recruiting trials returned study EBV infection more "
             "broadly (one -- 'Occurrence of Antibodies Cross-reacting With Autoantigens in "
             "Primary EBV Infection' -- explicitly enrolls during primary/acute EBV infection). "
             "Used directly, flagged as a broader-EBV substitution rather than mono-specific."},
    {"patient_id": "S010", "query": "retinal detachment", "n": 5},
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


MIN_USABLE = 3  # if primary query yields fewer than this many usable trials, try fallback_query


def main():
    out = {}
    for c in CONDITIONS:
        pid = c["patient_id"]
        query_used = c["query"]
        fallback_used = False
        normalized = []

        if not c.get("force_fallback"):
            print(f"Fetching: {c['query']} (for patient {pid}) ...")
            studies = fetch_condition(c["query"], c["n"])
            normalized = [s for s in (normalize(s) for s in studies) if s["eligibility_criteria_raw"]]
            print(f"  -> got {len(normalized)} trials with eligibility text")
            time.sleep(1)

        if (c.get("force_fallback") or len(normalized) < MIN_USABLE) and c.get("fallback_query"):
            fb_queries = [c["fallback_query"]] + ([c["fallback_query_2"]] if c.get("fallback_query_2") else [])
            seen_nct = set()
            fb_merged = []
            for fbq in fb_queries:
                print(f"Falling back to: {fbq} (for patient {pid}) ...")
                fb_studies = fetch_condition(fbq, c.get("fallback_n", 5))
                fb_normalized = [s for s in (normalize(s) for s in fb_studies) if s["eligibility_criteria_raw"]]
                print(f"  -> got {len(fb_normalized)} fallback trials with eligibility text")
                exclude = set(c.get("fallback_exclude_nct", []))
                for s in fb_normalized:
                    if s["nct_id"] not in seen_nct and s["nct_id"] not in exclude:
                        seen_nct.add(s["nct_id"])
                        fb_merged.append(s)
                time.sleep(1)
            normalized = fb_merged
            query_used = " + ".join(fb_queries)
            fallback_used = True

        out[pid] = {
            "query_used": query_used,
            "primary_query": c["query"],
            "fallback_used": fallback_used,
            "note": c.get("note", ""),
            "trials": normalized[: c.get("fallback_n" if fallback_used else "n", 5)],
        }

    with open("trials_raw.json", "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print("Wrote trials_raw.json")
    for pid, d in out.items():
        print(f"  {pid}: {len(d['trials'])} trials (query={d['query_used']!r}, fallback={d['fallback_used']})")


if __name__ == "__main__":
    main()
