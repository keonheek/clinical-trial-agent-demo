#!/usr/bin/env python3
"""
stress_eval.py — automation harness for the stress-test answer key (건희 item 7).

The team plan: Jiwoo (지우) hand-writes a blind answer key of 5 base patients x 7 broken
variants (T001..T005, suffixes -a..-g, 40 rows total). Jungwon (정원) converts that into
two files this harness consumes:

    patients_stress.json     -- the 40 patient vignettes (base + corrupted variants)
    eval_labels_stress.json  -- the hand-written expected verdict/action per criterion

The moment those two files land, `python3 stress_eval.py` produces the stress score: verdict
accuracy AND action accuracy, matched against `eval_labels_stress.json`.

--- Design note: why this harness does NOT reuse eval.py's join strategy -------------------
eval.py joins hand-written labels against traces.json on exact `criterion_text`, where the
criterion text on both sides was independently produced (labeller typed it once from the raw
trial page; the criteria-parser LLM re-derives its own wording from the same raw text on every
pipeline re-run). That is the known fragility: a 40-label set silently dropped to 20 TWICE
because re-parsing changed the wording (see EVAL-NOTES.md, "21 of the 40 old labels no longer
joined"). This harness structurally cannot reproduce that failure, because there is no LLM
criteria-parsing step in the stress path at all: eval_labels_stress.json's `criterion_text` +
`criterion_type` fields ARE the input fed to the matcher, not a separately-derived echo of it.
The matcher (`pipeline.match_trial`) never rewords a criterion, so the text a label carries in
is byte-identical to the text it is joined back on.

That removes the SOURCE of the historical bug, but the harness still hard-fails loudly instead
of trusting that invariant blindly, because a different failure mode is still possible: a typo
in a label's patient_id (row never reaches any patient), a duplicate (patient_id, nct_id,
criterion_text) triple across two label rows (ambiguous join), or a patient_id present in
eval_labels_stress.json but absent from patients_stress.json. Every one of those is caught
and reported by name -- never silently dropped -- before any accuracy number is computed.
---------------------------------------------------------------------------------------------

Reuses (imports only, never modifies): pipeline.extract_patient, pipeline.match_trial,
pipeline.effect_of. Those already call action_policy.classify_action internally, so `action`
comes out of the same code path production traces use -- no action logic duplicated here.

Caching: per-patient (fields, matched criteria) are cached to cache/stress/<patient_id>.json,
keyed on a hash of (patient text, criteria fed in, LLM backend, model). Reruns after the first
successful build make zero new LLM calls, same guarantee as pipeline.py's own cache/.

$0 rule: this file makes no LLM calls of its own. It calls pipeline.extract_patient /
pipeline.match_trial, which call whatever LLM_BACKEND is configured (see pipeline.py's own
docstring) -- unchanged, not this harness's decision to make or duplicate.

Run:
    python3 stress_eval.py                     # score using default file locations
    python3 stress_eval.py --patients P.json --labels L.json --results OUT.json
    python3 stress_eval.py --no-cache           # force fresh matcher calls, ignore cache/stress/
    python3 stress_eval.py --selftest           # run the self-test suite (mocked matcher, no LLM calls)
"""
import argparse
import hashlib
import json
import os
import sys

import pipeline  # import only -- never edit; see FILE FENCE in the task brief
from action_policy import VALID_ACTIONS  # import only

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATIENTS = os.path.join(HERE, "patients_stress.json")
DEFAULT_LABELS = os.path.join(HERE, "eval_labels_stress.json")
DEFAULT_RESULTS = os.path.join(HERE, "stress_eval_results.json")
CACHE_DIR = os.path.join(HERE, "cache", "stress")

VALID_VERDICTS = {"MET", "NOT_MET", "UNCERTAIN", "UNKNOWN"}


def _row_shape_ok(row):
    """Structural validity of one label row -- independent of whether its patient exists.
    expected_action is legitimately null for a MET/NOT_MET verdict (classify_action only
    assigns an action to UNKNOWN/UNCERTAIN), so null is valid, not missing."""
    pid, nct, text = row.get("patient_id"), row.get("nct_id"), row.get("criterion_text")
    ctype = str(row.get("criterion_type", "")).strip().lower()
    verdict = row.get("expected_verdict")
    action = row.get("expected_action")
    if not pid or not nct or not text or ctype not in ("inclusion", "exclusion"):
        return False
    if verdict not in VALID_VERDICTS:
        return False
    if action is not None and action not in VALID_ACTIONS:
        return False
    return True


# ---------------------------------------------------------------------------
# Loading + grouping
# ---------------------------------------------------------------------------
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def index_patients(patients):
    """patient_id -> patient dict. Hard-fails (raises) on a duplicate id -- two patients
    silently sharing an id would make every downstream join ambiguous."""
    by_id = {}
    dupes = []
    for p in patients:
        pid = p["patient_id"]
        if pid in by_id:
            dupes.append(pid)
        by_id[pid] = p
    if dupes:
        raise ValueError(f"patients_stress.json has duplicate patient_id(s): {sorted(set(dupes))}")
    return by_id


def build_criteria_by_patient(labels, patients_by_id):
    """Group label rows into per-patient, per-nct_id ordered criteria lists (the exact
    text+type the matcher will be asked to judge). Returns:
        criteria_by_patient: {patient_id: {nct_id: [{"text":.., "type":..}, ...]}}
        bad_rows: label rows that cannot be placed (unknown patient, missing fields,
                  or a (patient_id, nct_id, criterion_text) triple duplicated with a
                  DIFFERENT criterion_type / expected_verdict / expected_action --
                  an ambiguous label, never silently picked one of the two).
    """
    criteria_by_patient = {}
    seen_keys = {}  # (patient_id, nct_id, criterion_text) -> the first row seen
    bad_rows = []

    for row in labels:
        if not _row_shape_ok(row):
            bad_rows.append({"row": row, "reason": "malformed row (missing/invalid required field)"})
            continue
        pid = row.get("patient_id")
        nct = row.get("nct_id")
        text = row.get("criterion_text")
        ctype = str(row.get("criterion_type", "")).strip().lower()
        expected_verdict = row.get("expected_verdict")
        expected_action = row.get("expected_action")

        if pid not in patients_by_id:
            bad_rows.append({"row": row, "reason": f"patient_id {pid!r} not found in patients_stress.json"})
            continue

        key = (pid, nct, text)
        if key in seen_keys:
            prior = seen_keys[key]
            if (prior.get("criterion_type"), prior.get("expected_verdict"), prior.get("expected_action")) != \
               (ctype, expected_verdict, expected_action):
                bad_rows.append({"row": row, "reason": f"duplicate key {key} with CONFLICTING expected values"})
            continue  # exact duplicate (same everything) -- harmless, keep first
        seen_keys[key] = {"criterion_type": ctype, "expected_verdict": expected_verdict,
                           "expected_action": expected_action}

        criteria_by_patient.setdefault(pid, {}).setdefault(nct, [])
        # de-dupe text within the same trial for the same patient (matcher gets one row each)
        if not any(c["text"] == text for c in criteria_by_patient[pid][nct]):
            criteria_by_patient[pid][nct].append({"text": text, "type": ctype})

    return criteria_by_patient, bad_rows


# ---------------------------------------------------------------------------
# Matcher execution + caching
# ---------------------------------------------------------------------------
def _cache_key(patient, criteria_by_nct):
    backend = os.environ.get("LLM_BACKEND", "anthropic")
    model = getattr(pipeline, "DEFAULT_MODEL", "unknown-model")
    payload = json.dumps(
        {"text": patient["text"], "criteria": criteria_by_nct, "backend": backend, "model": model},
        sort_keys=True, ensure_ascii=False,
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:24]


def run_patient_stress(patient, criteria_by_nct, use_cache=True, cache_dir=CACHE_DIR):
    """Run pipeline.extract_patient + pipeline.match_trial for one stress patient across
    all its nct_id groups. Returns {(nct_id, criterion_text): {"verdict":.., "action":..}}.
    Cached to cache_dir/<patient_id>.json keyed on a hash of (text, criteria, backend, model)."""
    pid = patient["patient_id"]
    key = _cache_key(patient, criteria_by_nct)
    cache_path = os.path.join(cache_dir, f"{pid}.json")

    if use_cache and os.path.exists(cache_path):
        cached = load_json(cache_path)
        if cached.get("key") == key:
            return {tuple(k.split("\x1f", 1)): v for k, v in cached["results"].items()}

    fields, _dropped = pipeline.extract_patient(patient)

    results = {}
    for nct_id, criteria in criteria_by_nct.items():
        matched = pipeline.match_trial(patient, fields, criteria)
        for c in matched:
            results[(nct_id, c["text"])] = {"verdict": c["verdict"], "action": c.get("action")}

    if use_cache:
        os.makedirs(cache_dir, exist_ok=True)
        serializable = {f"{k[0]}\x1f{k[1]}": v for k, v in results.items()}
        with open(cache_path, "w", encoding="utf-8") as f:
            json.dump({"key": key, "results": serializable}, f, ensure_ascii=False, indent=2)

    return results


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------
def score(labels, patients_by_id, criteria_by_patient, use_cache=True, cache_dir=CACHE_DIR):
    """Returns (report_dict, unmatched_rows). unmatched_rows is non-empty -> hard-fail
    (caller must not treat report_dict['verdict_accuracy'] etc. as trustworthy)."""
    predicted_by_patient = {}
    for pid, by_nct in criteria_by_patient.items():
        predicted_by_patient[pid] = run_patient_stress(
            patients_by_id[pid], by_nct, use_cache=use_cache, cache_dir=cache_dir,
        )

    total = 0
    unmatched = []
    n_verdict_correct = 0
    n_action_correct = 0
    verdict_errors = []
    action_errors = []
    confusion = {}

    for row in labels:
        if not _row_shape_ok(row):
            unmatched.append({**row, "reason": "malformed row"})
            continue
        pid, nct, text = row.get("patient_id"), row.get("nct_id"), row.get("criterion_text")
        expected_verdict = row.get("expected_verdict")
        expected_action = row.get("expected_action")
        preds = predicted_by_patient.get(pid)
        if preds is None:
            unmatched.append({**row, "reason": f"patient_id {pid!r} not in patients_stress.json"})
            continue
        pred = preds.get((nct, text))
        if pred is None:
            unmatched.append({**row, "reason": "no matching (nct_id, criterion_text) in matcher output "
                                                "-- should be impossible by construction; investigate"})
            continue

        total += 1
        confusion.setdefault(expected_verdict, {}).setdefault(pred["verdict"], 0)
        confusion[expected_verdict][pred["verdict"]] += 1

        if pred["verdict"] == expected_verdict:
            n_verdict_correct += 1
        else:
            verdict_errors.append({"patient_id": pid, "nct_id": nct, "criterion_text": text,
                                    "expected": expected_verdict, "predicted": pred["verdict"]})

        if pred["action"] == expected_action:
            n_action_correct += 1
        else:
            action_errors.append({"patient_id": pid, "nct_id": nct, "criterion_text": text,
                                   "expected": expected_action, "predicted": pred["action"]})

    report = {
        "n_total_labels": len(labels),
        "n_matched": total,
        "n_unmatched": len(unmatched),
        "verdict_accuracy": round(n_verdict_correct / total, 4) if total else None,
        "action_accuracy": round(n_action_correct / total, 4) if total else None,
        "confusion": confusion,
        "verdict_errors": verdict_errors,
        "action_errors": action_errors,
        "unmatched": unmatched,
    }
    return report, unmatched


def run(patients_path, labels_path, results_path, use_cache=True, cache_dir=CACHE_DIR):
    patients = load_json(patients_path)
    labels = load_json(labels_path)
    patients_by_id = index_patients(patients)
    criteria_by_patient, bad_rows = build_criteria_by_patient(labels, patients_by_id)

    report, unmatched = score(labels, patients_by_id, criteria_by_patient,
                               use_cache=use_cache, cache_dir=cache_dir)
    all_unmatched = bad_rows + unmatched
    # de-dupe (build_criteria_by_patient and score both flag malformed/unknown-patient rows)
    seen = set()
    deduped_unmatched = []
    for u in all_unmatched:
        fp = json.dumps(u.get("row", u), sort_keys=True, ensure_ascii=False)
        if fp not in seen:
            seen.add(fp)
            deduped_unmatched.append(u)

    hard_fail = len(deduped_unmatched) > 0

    with open(results_path, "w", encoding="utf-8") as f:
        json.dump({**report, "unmatched": deduped_unmatched, "hard_fail": hard_fail}, f,
                   ensure_ascii=False, indent=2)

    matched = report["n_matched"]
    total_labels = report["n_total_labels"]
    print(f"Matched {matched}/{total_labels} labels.")
    if hard_fail:
        print(f"\n*** STRESS EVAL HARD-FAIL: {len(deduped_unmatched)} unmatched label(s). "
              f"NOT reporting a score. ***\n")
        for u in deduped_unmatched:
            row = u.get("row", u)
            print(f"  - {row.get('patient_id')} / {row.get('nct_id')} : "
                  f"{str(row.get('criterion_text'))[:70]!r}  -- {u.get('reason')}")
        print(f"\nWrote {results_path} (partial; hard_fail=true)")
        return 1

    print(f"Verdict accuracy: {report['verdict_accuracy']:.1%}")
    print(f"Action accuracy:  {report['action_accuracy']:.1%}")
    print(f"Wrote {results_path}")
    return 0


# ---------------------------------------------------------------------------
# Self-tests (mocked matcher -- zero LLM calls)
# ---------------------------------------------------------------------------
def _selftest():
    import tempfile
    import shutil

    tmp_cache = tempfile.mkdtemp(prefix="stress_eval_selftest_cache_")
    failures = []

    def check(name, cond, detail=""):
        status = "PASS" if cond else "FAIL"
        print(f"[{status}] {name}" + (f" -- {detail}" if detail and not cond else ""))
        if not cond:
            failures.append(name)

    patients = [
        {"patient_id": "T001", "text": "A 9-year-old with fever.", "condition": "test"},
        {"patient_id": "T001-a", "text": "A 54-year-old with fever.", "condition": "test"},
    ]
    patients_by_id = index_patients(patients)

    labels_ok = [
        {"patient_id": "T001", "nct_id": "NCT001", "criterion_text": "Age under 18 years old",
         "criterion_type": "inclusion", "expected_verdict": "MET", "expected_action": None},
        {"patient_id": "T001-a", "nct_id": "NCT001", "criterion_text": "Age under 18 years old",
         "criterion_type": "inclusion", "expected_verdict": "NOT_MET", "expected_action": None},
        {"patient_id": "T001", "nct_id": "NCT001", "criterion_text": "History of diabetes",
         "criterion_type": "exclusion", "expected_verdict": "UNKNOWN", "expected_action": "ASK"},
    ]

    # --- test 1: grouping is correct and lossless ---
    criteria_by_patient, bad = build_criteria_by_patient(labels_ok, patients_by_id)
    check("group: no bad rows on clean input", bad == [], detail=str(bad))
    check("group: both patients present", set(criteria_by_patient) == {"T001", "T001-a"})
    check("group: T001 has 2 criteria under NCT001",
          len(criteria_by_patient["T001"]["NCT001"]) == 2,
          detail=str(criteria_by_patient["T001"]))

    # --- test 2: mocked matcher produces a perfect score ---
    def fake_call_groq_perfect(role, sys_prompt, user_prompt, *a, **kw):
        if role == "patient-extractor":
            return {"fields": [{"name": "age", "value": "N/A", "evidence_quote": user_prompt[:0] or "9"}]}
        if role == "matcher":
            # crude: answer MET for "9-year-old" prompts, NOT_MET for "54-year-old", else UNKNOWN
            is_young = "9-year-old" in user_prompt
            matches = []
            if "Age under 18 years old" in user_prompt:
                idx = [i for i, line in enumerate(user_prompt.splitlines()) if "Age under 18" in line]
                matches.append({"index": 1 if "1. " in user_prompt.split("Age under 18")[0][-6:] else 1,
                                 "verdict": "MET" if is_young else "NOT_MET",
                                 "uncertainty_type": None, "evidence": "age", "reasoning": "age check"})
            if "History of diabetes" in user_prompt:
                matches.append({"index": 2, "verdict": "UNKNOWN",
                                 "uncertainty_type": "MISSING", "evidence": None, "reasoning": "not mentioned"})
            return {"matches": matches}
        raise AssertionError(f"unexpected role {role}")

    orig_call_groq = pipeline.call_groq
    pipeline.call_groq = fake_call_groq_perfect
    try:
        report, unmatched = score(labels_ok, patients_by_id, criteria_by_patient,
                                   use_cache=True, cache_dir=tmp_cache)
    finally:
        pipeline.call_groq = orig_call_groq

    check("score: no unmatched on clean run", unmatched == [], detail=str(unmatched))
    check("score: matched == total", report["n_matched"] == len(labels_ok))
    check("score: verdict_accuracy == 1.0", report["verdict_accuracy"] == 1.0,
          detail=str(report["verdict_errors"]))
    check("score: action_accuracy computed (None==None counts as match)",
          report["action_accuracy"] == 1.0, detail=str(report["action_errors"]))

    # --- test 3: caching -- second run must NOT call the (now-exploding) matcher ---
    def explode(*a, **kw):
        raise AssertionError("cache miss: call_groq invoked on a run that should have hit cache")

    pipeline.call_groq = explode
    try:
        report2, unmatched2 = score(labels_ok, patients_by_id, criteria_by_patient,
                                     use_cache=True, cache_dir=tmp_cache)
        check("cache: second run reuses cache (no exception)", True)
        check("cache: second run reproduces same accuracy",
              report2["verdict_accuracy"] == report["verdict_accuracy"])
    except AssertionError as e:
        check("cache: second run reuses cache (no exception)", False, detail=str(e))
    finally:
        pipeline.call_groq = orig_call_groq

    # --- test 4: hard-fail on an unmatched label (unknown patient_id) ---
    labels_bad = labels_ok + [
        {"patient_id": "T999-ghost", "nct_id": "NCT001", "criterion_text": "Some criterion",
         "criterion_type": "inclusion", "expected_verdict": "MET", "expected_action": "ASK"},
    ]
    criteria_by_patient_bad, bad_rows_bad = build_criteria_by_patient(labels_bad, patients_by_id)
    check("hard-fail: unknown patient_id flagged at grouping stage",
          len(bad_rows_bad) == 1 and bad_rows_bad[0]["row"]["patient_id"] == "T999-ghost",
          detail=str(bad_rows_bad))

    pipeline.call_groq = fake_call_groq_perfect
    try:
        report3, unmatched3 = score(labels_bad, patients_by_id, criteria_by_patient_bad,
                                     use_cache=True, cache_dir=tmp_cache)
    finally:
        pipeline.call_groq = orig_call_groq
    check("hard-fail: score() also flags the unmatched row (defense in depth)",
          len(unmatched3) == 1 and unmatched3[0]["patient_id"] == "T999-ghost",
          detail=str(unmatched3))
    check("hard-fail: full run() returns exit code 1 on this input", True)  # exercised below

    # --- test 5: full run() end-to-end via temp files, hard-fail path ---
    tmp_dir = tempfile.mkdtemp(prefix="stress_eval_selftest_files_")
    try:
        p_path = os.path.join(tmp_dir, "patients.json")
        l_path = os.path.join(tmp_dir, "labels.json")
        r_path = os.path.join(tmp_dir, "results.json")
        with open(p_path, "w") as f:
            json.dump(patients, f)
        with open(l_path, "w") as f:
            json.dump(labels_bad, f)
        pipeline.call_groq = fake_call_groq_perfect
        try:
            rc = run(p_path, l_path, r_path, use_cache=True,
                     cache_dir=os.path.join(tmp_dir, "cache"))
        finally:
            pipeline.call_groq = orig_call_groq
        check("run(): exit code 1 on unmatched labels", rc == 1)
        with open(r_path) as f:
            written = json.load(f)
        check("run(): results file marks hard_fail=true", written.get("hard_fail") is True)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    # --- test 6: full run() end-to-end, clean path ---
    tmp_dir2 = tempfile.mkdtemp(prefix="stress_eval_selftest_files_clean_")
    try:
        p_path = os.path.join(tmp_dir2, "patients.json")
        l_path = os.path.join(tmp_dir2, "labels.json")
        r_path = os.path.join(tmp_dir2, "results.json")
        with open(p_path, "w") as f:
            json.dump(patients, f)
        with open(l_path, "w") as f:
            json.dump(labels_ok, f)
        pipeline.call_groq = fake_call_groq_perfect
        try:
            rc = run(p_path, l_path, r_path, use_cache=True,
                     cache_dir=os.path.join(tmp_dir2, "cache"))
        finally:
            pipeline.call_groq = orig_call_groq
        check("run(): exit code 0 on clean labels", rc == 0)
    finally:
        shutil.rmtree(tmp_dir2, ignore_errors=True)

    shutil.rmtree(tmp_cache, ignore_errors=True)

    print(f"\n{len(failures)} failure(s) out of self-test suite." if failures else "\nAll self-tests passed.")
    return 0 if not failures else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--patients", default=DEFAULT_PATIENTS)
    ap.add_argument("--labels", default=DEFAULT_LABELS)
    ap.add_argument("--results", default=DEFAULT_RESULTS)
    ap.add_argument("--no-cache", action="store_true", help="ignore cache/stress/, force fresh matcher calls")
    ap.add_argument("--selftest", action="store_true", help="run the self-test suite (mocked matcher, no LLM calls)")
    args = ap.parse_args()

    if args.selftest:
        sys.exit(_selftest())

    if not os.path.exists(args.patients) or not os.path.exists(args.labels):
        print(f"Waiting on input files -- not yet present:")
        if not os.path.exists(args.patients):
            print(f"  missing: {args.patients}")
        if not os.path.exists(args.labels):
            print(f"  missing: {args.labels}")
        print("See patients_stress.sample.json / eval_labels_stress.sample.json for the schema.")
        sys.exit(2)

    sys.exit(run(args.patients, args.labels, args.results, use_cache=not args.no_cache))


if __name__ == "__main__":
    main()
