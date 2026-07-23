#!/usr/bin/env python3
"""
assert_traces.py — hard verification of traces.js / traces.json before calling the
demo "done". Never trust a self-report; re-derive the checks from the actual files.

Checks:
  1. traces.js is valid JS in the exact required shape (`window.TRACES = [...];`)
     and its payload round-trips through Node's JS parser (not just Python json.loads,
     since traces.js is JS source, not pure JSON -- Node is the real consumer's runtime).
  2. traces.json parses as plain JSON and is byte-identical in content to traces.js's payload.
  3. HARD ASSERTION (per spec (b) patient-extractor): every extraction[].evidence_quote is a
     verbatim substring of that patient's patient_text. Any violation fails the whole check.
  4. Structural shape check: every trace has the required top-level keys, every trial has
     the required keys, every criterion has the required keys with valid verdict enum,
     every trial has a valid eligibility enum.
  5. Informational (soft) check: how many criteria[].evidence quotes (matcher output, not
     hard-required to be verbatim per spec) are ALSO verbatim substrings of patient_text --
     reported as a quality signal, not a failure condition.

Exit code 0 = all hard checks passed. Exit code 1 = at least one hard check failed.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TRACES_JSON = os.path.join(HERE, "traces.json")
TRACES_JS = os.path.join(HERE, "traces.js")

REQUIRED_TRACE_KEYS = {"patient_id", "patient_text", "extraction", "trials", "questions", "reeval", "generated_at"}
REQUIRED_TRIAL_KEYS = {"nct_id", "title", "phase", "criteria", "eligibility", "rank", "rationale"}
REQUIRED_CRITERION_KEYS = {"text", "type", "verdict", "evidence", "reasoning"}
REQUIRED_REEVAL_KEYS = {"extended_record", "answers", "verdict_changes", "final_ranking"}
REQUIRED_ANSWER_KEYS = {"question", "answer", "evidence_quote"}
REQUIRED_VERDICT_CHANGE_KEYS = {"nct_id", "criterion", "before", "after"}
VALID_VERDICTS = {"MET", "NOT_MET", "UNCERTAIN", "UNKNOWN"}
VALID_ELIGIBILITY = {"ELIGIBLE", "INELIGIBLE", "UNCERTAIN"}

failures = []
warnings = []


def fail(msg):
    failures.append(msg)
    print(f"FAIL: {msg}")


def warn(msg):
    warnings.append(msg)
    print(f"WARN: {msg}")


def ok(msg):
    print(f"OK: {msg}")


def check_js_parses_via_node():
    print("\n--- Check 1: traces.js parses as valid JS via Node ---")
    script = f"""
const fs = require('fs');
const src = fs.readFileSync('{TRACES_JS}', 'utf8');
const sandbox = {{}};
const wrapped = new Function('window', src + '\\nreturn window.TRACES;');
const result = wrapped(sandbox);
if (!Array.isArray(result)) {{
    console.error('TRACES is not an array');
    process.exit(1);
}}
console.log('TRACES_LENGTH=' + result.length);
console.log('PARSE_OK');
"""
    proc = subprocess.run(["node", "-e", script], capture_output=True, text=True)
    if proc.returncode != 0:
        fail(f"traces.js failed to parse in Node: {proc.stderr.strip()}")
        return None
    if "PARSE_OK" not in proc.stdout:
        fail(f"traces.js parsed but did not confirm array shape: {proc.stdout}")
        return None
    ok(f"traces.js parses cleanly in Node ({proc.stdout.strip().splitlines()})")
    return True


def check_json_and_js_payload_match():
    print("\n--- Check 2: traces.json parses + matches traces.js payload ---")
    try:
        with open(TRACES_JSON) as f:
            json_data = json.load(f)
    except json.JSONDecodeError as e:
        fail(f"traces.json failed to parse as JSON: {e}")
        return None
    ok(f"traces.json parses as valid JSON ({len(json_data)} patient traces)")

    with open(TRACES_JS) as f:
        js_src = f.read()
    prefix = "window.TRACES = "
    if not js_src.startswith(prefix):
        fail("traces.js does not start with 'window.TRACES = '")
        return json_data
    payload_str = js_src[len(prefix):].rstrip().rstrip(";").rstrip()
    try:
        js_payload = json.loads(payload_str)
    except json.JSONDecodeError as e:
        fail(f"traces.js payload (after stripping window.TRACES = ... ;) is not valid JSON: {e}")
        return json_data
    if js_payload != json_data:
        fail("traces.js payload does not match traces.json content")
    else:
        ok("traces.js payload is content-identical to traces.json")
    return json_data


def check_evidence_quotes_verbatim(traces):
    print("\n--- Check 3 (HARD): extraction[].evidence_quote verbatim substring of patient_text ---")
    total = 0
    violations = 0
    for trace in traces:
        pid = trace.get("patient_id", "?")
        patient_text = trace.get("patient_text", "")
        for field in trace.get("extraction", []):
            total += 1
            quote = field.get("evidence_quote", "")
            if quote not in patient_text:
                violations += 1
                fail(f"[{pid}] evidence_quote NOT a verbatim substring: "
                     f"field={field.get('name')!r} quote={quote!r}")
    if total == 0:
        fail("no extraction fields found at all across any trace -- cannot verify anything")
    elif violations == 0:
        ok(f"all {total} extraction evidence_quote(s) across {len(traces)} patients are verbatim substrings")
    return total, violations


def check_structural_shape(traces):
    print("\n--- Check 4: structural shape + enum validity ---")
    n_trials = 0
    n_criteria = 0
    for trace in traces:
        pid = trace.get("patient_id", "?")
        missing = REQUIRED_TRACE_KEYS - set(trace.keys())
        if missing:
            fail(f"[{pid}] trace missing top-level keys: {missing}")
        for trial in trace.get("trials", []):
            n_trials += 1
            nct = trial.get("nct_id", "?")
            missing_t = REQUIRED_TRIAL_KEYS - set(trial.keys())
            if missing_t:
                fail(f"[{pid}/{nct}] trial missing keys: {missing_t}")
            if trial.get("eligibility") not in VALID_ELIGIBILITY:
                fail(f"[{pid}/{nct}] invalid eligibility value: {trial.get('eligibility')!r}")
            for c in trial.get("criteria", []):
                n_criteria += 1
                missing_c = REQUIRED_CRITERION_KEYS - set(c.keys())
                if missing_c:
                    fail(f"[{pid}/{nct}] criterion missing keys: {missing_c}")
                if c.get("verdict") not in VALID_VERDICTS:
                    fail(f"[{pid}/{nct}] invalid verdict value: {c.get('verdict')!r}")
        if len(trace.get("questions", [])) > 3:
            fail(f"[{pid}] more than 3 clarifying questions returned: {len(trace['questions'])}")
    if not failures:
        ok(f"structural shape valid across {len(traces)} patients, {n_trials} trials, {n_criteria} criteria")
    return n_trials, n_criteria


def check_reeval_structure_and_grounding(traces):
    print("\n--- Check 6: reeval block structure + HARD grounding (answers <- extended_record) ---")
    total_answers = 0
    ungrounded_answers = 0
    total_changes = 0
    bad_change_refs = 0
    patients_with_reeval_content = 0

    for trace in traces:
        pid = trace.get("patient_id", "?")
        reeval = trace.get("reeval")
        if reeval is None:
            fail(f"[{pid}] missing 'reeval' key entirely")
            continue
        missing = REQUIRED_REEVAL_KEYS - set(reeval.keys())
        if missing:
            fail(f"[{pid}] reeval block missing keys: {missing}")
            continue

        extended_record = reeval.get("extended_record", "")
        answers = reeval.get("answers", [])
        verdict_changes = reeval.get("verdict_changes", [])
        final_ranking = reeval.get("final_ranking", [])

        if extended_record or answers or verdict_changes:
            patients_with_reeval_content += 1

        # HARD: every answer's evidence_quote must be a verbatim substring of extended_record
        for a in answers:
            total_answers += 1
            missing_a = REQUIRED_ANSWER_KEYS - set(a.keys())
            if missing_a:
                fail(f"[{pid}] reeval answer missing keys: {missing_a}")
                ungrounded_answers += 1
                continue
            quote = a.get("evidence_quote", "")
            if not quote or quote not in extended_record:
                ungrounded_answers += 1
                fail(f"[{pid}] reeval answer NOT grounded: evidence_quote={quote!r} "
                     f"not a verbatim substring of this patient's extended_record")

        # HARD: every verdict_changes[].criterion must reference a REAL criterion text that
        # exists under that nct_id in this patient's trials[].criteria[]
        criteria_by_nct = {}
        for trial in trace.get("trials", []):
            criteria_by_nct[trial.get("nct_id")] = {c["text"] for c in trial.get("criteria", [])}
        for vc in verdict_changes:
            total_changes += 1
            missing_vc = REQUIRED_VERDICT_CHANGE_KEYS - set(vc.keys())
            if missing_vc:
                fail(f"[{pid}] verdict_change missing keys: {missing_vc}")
                bad_change_refs += 1
                continue
            nct_id = vc.get("nct_id")
            criterion = vc.get("criterion")
            valid_texts = criteria_by_nct.get(nct_id, set())
            if criterion not in valid_texts:
                bad_change_refs += 1
                fail(f"[{pid}] verdict_change references a criterion NOT found under "
                     f"{nct_id}'s trial criteria: {criterion!r}")
            if vc.get("before") not in VALID_VERDICTS or vc.get("after") not in VALID_VERDICTS:
                fail(f"[{pid}] verdict_change has invalid before/after verdict: "
                     f"{vc.get('before')!r} -> {vc.get('after')!r}")
            if vc.get("before") == vc.get("after"):
                fail(f"[{pid}] verdict_change has identical before/after ({vc.get('before')!r}) "
                     f"-- not a real change")

        # sanity: final_ranking entries must reference real trials for this patient
        real_ncts = set(criteria_by_nct.keys())
        for fr in final_ranking:
            if fr.get("nct_id") not in real_ncts:
                fail(f"[{pid}] final_ranking references unknown nct_id: {fr.get('nct_id')!r}")
            if fr.get("eligibility") not in VALID_ELIGIBILITY:
                fail(f"[{pid}] final_ranking has invalid eligibility: {fr.get('eligibility')!r}")

    if total_answers:
        ok(f"reeval answers grounded: {total_answers - ungrounded_answers}/{total_answers} "
           f"verbatim-in-extended_record across {len(traces)} patients")
    else:
        warn("no reeval answers found across any patient (no gaps needed re-answering?)")
    if total_changes:
        ok(f"verdict_changes reference real criteria: {total_changes - bad_change_refs}/{total_changes} valid")
    print(f"INFO: {patients_with_reeval_content}/{len(traces)} patients produced non-empty reeval content")
    return total_answers, ungrounded_answers, total_changes, bad_change_refs


def check_matcher_evidence_soft(traces):
    print("\n--- Check 5 (soft/informational): criteria[].evidence verbatim in patient_text ---")
    total_with_evidence = 0
    verbatim = 0
    for trace in traces:
        patient_text = trace.get("patient_text", "")
        for trial in trace.get("trials", []):
            for c in trial.get("criteria", []):
                ev = c.get("evidence")
                if ev:
                    total_with_evidence += 1
                    if ev in patient_text:
                        verbatim += 1
    if total_with_evidence:
        pct = 100.0 * verbatim / total_with_evidence
        print(f"INFO: {verbatim}/{total_with_evidence} ({pct:.0f}%) matcher evidence quotes are "
              f"ALSO verbatim substrings of patient_text (not a hard requirement, informational only)")
    else:
        print("INFO: no non-null matcher evidence quotes to check")


def main():
    check_js_parses_via_node()
    traces = check_json_and_js_payload_match()
    if traces is None:
        print("\nCannot continue further checks without parseable traces data.")
        sys.exit(1)

    check_evidence_quotes_verbatim(traces)
    check_structural_shape(traces)
    check_reeval_structure_and_grounding(traces)
    check_matcher_evidence_soft(traces)

    print("\n=== SUMMARY ===")
    print(f"Failures: {len(failures)}")
    print(f"Warnings: {len(warnings)}")
    if failures:
        print("\nRESULT: FAIL")
        sys.exit(1)
    else:
        print("\nRESULT: PASS")
        sys.exit(0)


if __name__ == "__main__":
    main()
