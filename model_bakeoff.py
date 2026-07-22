#!/usr/bin/env python3
"""Score the same stress patients on several models and compare.

Reuses stress_eval's grouping/execution/scoring so the numbers are produced the same way
the committed stress harness produces them -- only the model varies. Labels are 지우's
human answer key and are never modified here.

    python3 model_bakeoff.py --patients T001-b T001-c T001-d \
        --models claude-haiku-4-5 claude-sonnet-5 claude-opus-4-8
"""
import argparse
import json
import os
import sys

import pipeline
import stress_eval

HERE = os.path.dirname(os.path.abspath(__file__))


def run_one(model, patient_ids, patients_by_id, labels, use_cache=True):
    pipeline.set_active_model(model)
    rows = [r for r in labels if r.get("patient_id") in patient_ids]
    criteria_by_patient, bad = stress_eval.build_criteria_by_patient(rows, patients_by_id)
    if bad:
        raise SystemExit(f"label rows rejected before scoring: {bad}")
    # per-model cache dir keeps runs isolated even if a key scheme changes underneath
    cache_dir = os.path.join(HERE, "cache", "bakeoff", model.replace(":", "_"))
    report, unmatched = stress_eval.score(
        rows, patients_by_id, criteria_by_patient, use_cache=use_cache, cache_dir=cache_dir,
    )
    if unmatched:
        raise SystemExit(f"{len(unmatched)} unmatched labels on {model} -- not scoring")
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--patients", nargs="+", required=True)
    ap.add_argument("--models", nargs="+", required=True)
    ap.add_argument("--out", default=os.path.join(HERE, "model_bakeoff_results.json"))
    ap.add_argument("--no-cache", action="store_true")
    args = ap.parse_args()

    patients = stress_eval.load_json(os.path.join(HERE, "patients_stress.json"))
    labels = stress_eval.load_json(os.path.join(HERE, "eval_labels_stress.json"))
    patients_by_id = stress_eval.index_patients(patients)
    wanted = set(args.patients)
    missing = wanted - set(patients_by_id)
    if missing:
        raise SystemExit(f"unknown patient ids: {sorted(missing)}")

    results = {}
    for model in args.models:
        print(f"\n=== {model} ===", flush=True)
        rep = run_one(model, wanted, patients_by_id, labels, use_cache=not args.no_cache)
        results[model] = rep
        print(f"  labels {rep['n_matched']}  verdict {rep['verdict_accuracy']:.1%}  "
              f"action {rep['action_accuracy']:.1%}  "
              f"utype {rep['uncertainty_type_accuracy'] if rep['uncertainty_type_accuracy'] is None else format(rep['uncertainty_type_accuracy'], '.1%')}  "
              f"wrongly-passed {rep['safety']['n_wrongly_passed']}", flush=True)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"patients": sorted(wanted), "results": results}, f,
                  ensure_ascii=False, indent=2)

    print("\n" + "=" * 78)
    print(f"{'model':<22} {'verdict':>8} {'action':>8} {'utype':>8} {'wrong-pass':>11} {'false-cert':>11}")
    print("-" * 78)
    for model, rep in results.items():
        s = rep["safety"]
        fc = s["false_certainty_rate"]
        print(f"{model:<22} {rep['verdict_accuracy']:>7.1%} {rep['action_accuracy']:>7.1%} "
              f"{('n/a' if rep['uncertainty_type_accuracy'] is None else format(rep['uncertainty_type_accuracy'], '.1%')):>8} "
              f"{s['n_wrongly_passed']:>11} "
              f"{('n/a' if fc is None else format(fc, '.0%')):>11}")
    print(f"\nWrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
