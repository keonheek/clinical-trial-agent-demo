"""ranking.py -- deterministic, explainable recommendation priority (추천 우선순위).

Pure stdlib. NO LLM client imports (this module is bundled into the serverless api/ handlers,
which must stay zero-LLM -- same rule as action_policy.py). Selftest: `python3 ranking.py`.
Golden order over the frozen demo traces: `python3 ranking.py --golden` (check) /
`--write-golden` (regenerate expected_ranking.json after a deliberate key change).

WHY THIS EXISTS. The organizer (박호진, 07-23 Q&A) said the "가장 적절한" ordering must weigh
not only eligibility but 임상적 적합성 -- Phase, 중재 목적, 환자 부담. The email of 08-16 made the
per-patient priority order the ONE binding deliverable. Until this module, the sort key was
(eligibility class, unresolved count, fail count) only, so within a class the trial whose
protocol was parsed LEAST ranked first (RECOMMENDATION-DEFINITION.md's counter-example, live on
S001) and observational registries out-ranked therapeutic Phase 4 trials (S002).

THE KEY (lexicographic; earlier tiers dominate; every tier is a fact of the trial record or a
code-derived count -- never a model opinion):

  0. eligibility class      ELIGIBLE < UNCERTAIN < INELIGIBLE     (decide_eligibility; a hard
                            FAIL is never out-ranked -- the safety claim on the deck)
  1. blocking criteria      fewer FAIL effects first              (only non-zero for INELIGIBLE)
  2. 중재 목적 (fit)         therapeutic < supportive < care_delivery < observational
                            low-confidence or unclassified intent DEMOTES to the observational
                            tier: a hedged guess never lifts a trial above a confirmed one
  3. Phase 부담 proxy         PHASE4 < PHASE3 < PHASE2 < PHASE1 = EARLY_PHASE1; NA/unknown = mid
                            (later phase = better-characterized intervention, lower burden and
                            uncertainty for the patient; the only burden datum in the record)
  4. coverage penalty       parsed/raw_estimated < 0.5 sinks below fully-read trials
                            (a trial we read less is not a more certain match)
  5. unresolved ratio       REVIEW / parsed, ascending  (normalized, per 지우's option D)
  6. unresolved count       REVIEW count, ascending     (tie-break within equal ratio)
  7. nct_id                 stable, reproducible last resort

Keonhee's call (2026-08-16): 중재 목적 sits ABOVE certainty inside an eligibility class --
"같은 적격성 클래스라면 환자에게 치료 기회가 되는 시험을 먼저 검토한다". Certainty (tiers 4-6) is
mostly an artifact of vignette thinness on the demo set (284/374 criteria UNKNOWN), which is
another reason not to let it outrank a fact of the trial record.

INVARIANTS: eval.py never reads `rank`, and traces.json is never written -- this module re-ranks
IN MEMORY at serve time (api/trace.py, live_server.py) and inside pipeline.recommend() for
generation/answer rounds. The frozen 82.5% n=40 pairing cannot move.
"""
import json
import os
import sys

RANKING_VERSION = "2026-08-16"

ELIGIBILITY_ORDER = {"ELIGIBLE": 0, "UNCERTAIN": 1, "INELIGIBLE": 2}

FIT_ORDER = {"therapeutic": 0, "supportive": 1, "care_delivery": 2, "observational": 3}
FIT_UNKNOWN = 3  # unclassified / low-confidence -> same tier as observational (demote, never lift)

PHASE_BURDEN = {"phase4": 0, "phase3": 1, "phase2": 2, "phase1": 3, "earlyphase1": 3,
                "phase2/phase3": 1, "phase1/phase2": 2}
PHASE_BURDEN_DEFAULT = 2  # NA / unknown: burden not characterized by phase -> middle

LOW_COVERAGE_CUTOFF = 0.5

# One-line statement of the executed rule, for the UI and the deck. Must match rank_key.
RANKING_RULE_KO = ("적격성 클래스(적격>미확정>부적격) → 차단 기준 수 → 중재 목적(치료>지지>관리>관찰; "
                   "확신 낮으면 관찰과 동급) → Phase 부담(4>3>2>1, NA는 중간) → "
                   "원문 커버리지 50% 미만 감점 → 미해결 비율 → 미해결 수 → NCT")

FIT_LABEL_KO = {"therapeutic": "치료 목적", "supportive": "지지·완화", "care_delivery": "의료전달·관리",
                "observational": "관찰 연구"}
ELIG_LABEL_KO = {"ELIGIBLE": "적격", "UNCERTAIN": "미확정", "INELIGIBLE": "부적격"}

_HERE = os.path.dirname(os.path.abspath(__file__))
_SIDECARS = {}


def normalize_phase(phase):
    """Same compaction as build_trial_intent._is_interventional_phase: 'PHASE 2' == 'PHASE2',
    'EARLY_PHASE1' == 'earlyphase1'. Returns '' for None/NA-like empties."""
    p = str(phase or "").strip().lower().replace(" ", "").replace("_", "")
    return "" if p in {"", "na", "n/a", "none", "null"} else p


def phase_burden(phase):
    return PHASE_BURDEN.get(normalize_phase(phase), PHASE_BURDEN_DEFAULT)


PHASE_LABEL = {"phase1": "Phase 1", "phase2": "Phase 2", "phase3": "Phase 3", "phase4": "Phase 4",
               "earlyphase1": "Early Phase 1", "phase1/phase2": "Phase 1/2", "phase2/phase3": "Phase 2/3"}


def phase_label(phase):
    """Human label for a phase string; mirrored by site.html phaseLabel() -- keep both in sync."""
    p = normalize_phase(phase)
    if not p:
        return "Phase NA"
    return PHASE_LABEL.get(p, "Phase " + str(phase).strip())


def fit_rank(intent):
    """intent = {"intent": str, "confidence": "high"|"low"} or None. Only a HIGH-confidence
    non-observational intent moves a trial up; everything else lands on the observational tier."""
    if not isinstance(intent, dict):
        return FIT_UNKNOWN
    if str(intent.get("confidence", "low")).lower() != "high":
        return FIT_UNKNOWN
    return FIT_ORDER.get(intent.get("intent"), FIT_UNKNOWN)


def coverage_ratio(parsed, raw_estimated):
    if not raw_estimated or raw_estimated <= 0 or parsed is None:
        return None
    return parsed / float(raw_estimated)


def coverage_penalty(parsed, raw_estimated):
    r = coverage_ratio(parsed, raw_estimated)
    return 1 if (r is not None and r < LOW_COVERAGE_CUTOFF) else 0


def _counts(criteria):
    n = len(criteria or [])
    fails = sum(1 for c in (criteria or []) if c.get("effect") == "FAIL")
    reviews = sum(1 for c in (criteria or []) if c.get("effect") == "REVIEW")
    return n, fails, reviews


def _load_sidecars():
    """trial_intent.json + coverage_map.json from the repo root, cached. Missing files -> {}."""
    if _SIDECARS:
        return _SIDECARS
    for name, key in (("trial_intent.json", "intent"), ("coverage_map.json", "coverage")):
        try:
            with open(os.path.join(_HERE, name), encoding="utf-8") as f:
                _SIDECARS[key] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            _SIDECARS[key] = {}
    return _SIDECARS


def resolve_intent(trial, intent_map, trust_attached):
    """Server-side truth first (sidecar by nct_id). The attached trial["trial_intent"] is used
    only when the caller vouches for it (live_server classifies unseen trials itself); a client
    body must never be able to rig the sort (api/answer.py passes trust_attached=False)."""
    side = (intent_map or {}).get(trial.get("nct_id"))
    if isinstance(side, dict) and side.get("intent"):
        return {"intent": side["intent"], "confidence": side.get("confidence", "low")}
    if trust_attached and isinstance(trial.get("trial_intent"), dict):
        return trial["trial_intent"]
    return None


def rank_key(trial, intent=None, raw_estimated=None):
    n, fails, reviews = _counts(trial.get("criteria"))
    ratio = round(reviews / n, 3) if n else 1.0
    return (
        ELIGIBILITY_ORDER.get(trial.get("eligibility"), 1),
        fails,
        fit_rank(intent),
        phase_burden(trial.get("phase")),
        coverage_penalty(n, raw_estimated),
        ratio,
        reviews,
        str(trial.get("nct_id", "")),
    )


def rank_basis(trial, intent=None, raw_estimated=None):
    """The fired components, in key order, as UI-ready chips + one Korean sentence."""
    n, fails, reviews = _counts(trial.get("criteria"))
    elig = trial.get("eligibility", "UNCERTAIN")
    fr = fit_rank(intent)
    intent_name = intent.get("intent") if isinstance(intent, dict) else None
    conf = intent.get("confidence") if isinstance(intent, dict) else None
    cov = coverage_ratio(n, raw_estimated)
    pen = coverage_penalty(n, raw_estimated)

    basis = [{"key": "eligibility", "label": "적격성", "value": elig, "tier": 0}]
    if fails:
        basis.append({"key": "blocking", "label": "차단 기준", "value": fails, "tier": 1})
    if fr < FIT_UNKNOWN:
        basis.append({"key": "fit", "label": "중재 목적", "value": intent_name,
                      "confidence": conf, "tier": 2})
    else:
        basis.append({"key": "fit", "label": "중재 목적",
                      "value": intent_name or "unclassified",
                      "confidence": conf, "demoted": True, "tier": 2})
    basis.append({"key": "phase", "label": "Phase", "value": (trial.get("phase") or "NA"),
                  "burden": phase_burden(trial.get("phase")), "tier": 3})
    if cov is not None:
        basis.append({"key": "coverage", "label": "원문 커버리지", "value": round(cov, 2),
                      "penalty": bool(pen), "tier": 4})
    basis.append({"key": "open", "label": "미해결", "value": f"{reviews}/{n}", "tier": 5})

    parts = [f"적격성 {ELIG_LABEL_KO.get(elig, elig)}"]
    if fails:
        parts.append(f"차단 기준 {fails}건")
    if fr < FIT_UNKNOWN:
        parts.append(f"{FIT_LABEL_KO.get(intent_name, intent_name)} 시험")
    elif intent_name == "observational":
        parts.append("관찰 연구" + (" (추정)" if conf == "low" else ""))
    else:
        parts.append("중재 목적 미확인 → 관찰과 동급")
    parts.append(phase_label(trial.get("phase")))
    if cov is not None:
        # parsed can exceed the line-count estimate (multi-clause bullets split into atomic
        # criteria) -- never assert more than "전체(추정)", the estimator is an approximation.
        parts.append("원문 커버리지 전체(추정)" if cov >= 1.0
                     else f"원문 커버리지 {int(round(cov * 100))}%" + (" (감점)" if pen else ""))
    parts.append(f"미해결 {reviews}/{n}")
    return basis, " · ".join(parts)


def rank_trials(trials, intent_map=None, coverage_map=None, trust_attached=False):
    """Sort `trials` in place by rank_key and stamp rank / rank_reason / rank_basis /
    ranking_version on each. Returns the same list. Also normalizes trial["trial_intent"] to the
    server-side sidecar value when one exists (display and sort then agree).

    trials: dicts with nct_id, phase, eligibility, criteria[{effect,...}] (+ optional
    trial_intent). intent_map / coverage_map default to the repo-root sidecars."""
    side = _load_sidecars()
    intent_map = side["intent"] if intent_map is None else intent_map
    coverage_map = side["coverage"] if coverage_map is None else coverage_map

    keyed = []
    for t in trials:
        intent = resolve_intent(t, intent_map, trust_attached)
        if intent and (intent_map or {}).get(t.get("nct_id")):
            t["trial_intent"] = {"intent": intent["intent"], "confidence": intent.get("confidence", "low")}
        raw = (coverage_map or {}).get(t.get("nct_id"))
        keyed.append((rank_key(t, intent, raw), t, intent, raw))
    keyed.sort(key=lambda x: x[0])
    trials[:] = [t for _, t, _, _ in keyed]
    for i, (_, t, intent, raw) in enumerate(keyed):
        t["rank"] = i + 1
        basis, reason = rank_basis(t, intent, raw)
        t["rank_basis"] = basis
        t["rank_reason"] = reason
        t["ranking_version"] = RANKING_VERSION
    return trials


def hard_exclusion_holds(trials):
    """Safety property the deck claims: no INELIGIBLE trial ranks above a non-INELIGIBLE one."""
    ranked = sorted(trials, key=lambda t: t.get("rank", 99))
    seen_inel = False
    for t in ranked:
        if t.get("eligibility") == "INELIGIBLE":
            seen_inel = True
        elif seen_inel:
            return False
    return True


# ---------------------------------------------------------------------------
# golden order over the frozen demo traces
# ---------------------------------------------------------------------------
GOLDEN_PATH = os.path.join(_HERE, "expected_ranking.json")


TRACES_PATH = os.path.join(_HERE, "traces.json")


def golden_from_traces(traces_path=None):
    with open(traces_path or TRACES_PATH, encoding="utf-8") as f:
        traces = json.load(f)
    out = {}
    for tr in traces:
        trials = [dict(t, criteria=[dict(c) for c in t.get("criteria", [])]) for t in tr["trials"]]
        rank_trials(trials)
        assert hard_exclusion_holds(trials), tr["patient_id"]
        out[tr["patient_id"]] = [t["nct_id"] for t in trials]
    return out


def check_golden():
    got = golden_from_traces()
    with open(GOLDEN_PATH, encoding="utf-8") as f:
        want = json.load(f)
    if want.get("ranking_version") != RANKING_VERSION or want.get("order") != got:
        diffs = [pid for pid in got if want.get("order", {}).get(pid) != got[pid]]
        print(f"ranking golden: FAIL (version {want.get('ranking_version')} vs {RANKING_VERSION}; "
              f"patients differing: {diffs})")
        return False
    print(f"ranking golden: PASS ({len(got)} patients, version {RANKING_VERSION})")
    return True


# ---------------------------------------------------------------------------
# self-tests -- run: python3 ranking.py
# ---------------------------------------------------------------------------
def _selftest():
    ok = True

    def check(cond, msg):
        nonlocal ok
        print(("  PASS " if cond else "  FAIL ") + msg)
        ok = ok and cond

    def T(nct, elig, phase, crit_effects, intent=None):
        return {"nct_id": nct, "title": nct, "phase": phase, "eligibility": elig,
                "criteria": [{"effect": e, "text": f"c{i}", "type": "inclusion", "verdict": "UNKNOWN"}
                             for i, e in enumerate(crit_effects)],
                "trial_intent": intent}

    # 1. hard exclusion is never out-ranked, whatever the appropriateness terms say
    trials = [T("NCT1", "INELIGIBLE", "PHASE4", ["FAIL"], {"intent": "therapeutic", "confidence": "high"}),
              T("NCT2", "UNCERTAIN", "NA", ["REVIEW"] * 12, {"intent": "observational", "confidence": "low"})]
    rank_trials(trials, intent_map={}, coverage_map={}, trust_attached=True)
    check(trials[0]["nct_id"] == "NCT2" and hard_exclusion_holds(trials),
          "eligibility class outranks intent/phase (INELIGIBLE therapeutic P4 stays below UNCERTAIN observational)")

    # 2. within a class, confirmed therapeutic beats observational even with more unresolved
    trials = [T("NCTa", "UNCERTAIN", "NA", ["REVIEW"] * 2 + ["PASS"] * 2, {"intent": "observational", "confidence": "high"}),
              T("NCTb", "UNCERTAIN", "PHASE4", ["REVIEW"] * 10 + ["PASS"] * 2, {"intent": "therapeutic", "confidence": "high"})]
    rank_trials(trials, intent_map={}, coverage_map={}, trust_attached=True)
    check(trials[0]["nct_id"] == "NCTb", "중재 목적 above certainty inside a class (his 08-16 call)")

    # 3. low-confidence therapeutic does NOT lift above high-confidence observational with fewer unresolved
    trials = [T("NCTa", "UNCERTAIN", "NA", ["REVIEW"] * 2 + ["PASS"] * 2, {"intent": "observational", "confidence": "high"}),
              T("NCTb", "UNCERTAIN", "NA", ["REVIEW"] * 3 + ["PASS"] * 1, {"intent": "therapeutic", "confidence": "low"})]
    rank_trials(trials, intent_map={}, coverage_map={}, trust_attached=True)
    check(trials[0]["nct_id"] == "NCTa", "low-confidence intent demotes to observational tier (ratio decides)")

    # 4. phase burden inside therapeutic: PHASE4 before PHASE1; spaced + EARLY forms normalize
    check(phase_burden("PHASE 2") == phase_burden("PHASE2") == 2, "phase normalization 'PHASE 2' == 'PHASE2'")
    check(phase_burden("EARLY_PHASE1") == phase_burden("PHASE1") == 3, "EARLY_PHASE1 == PHASE1 burden")
    check(phase_burden("NA") == PHASE_BURDEN_DEFAULT == phase_burden(None), "NA/None -> default mid burden")
    check(phase_label("EARLY_PHASE1") == "Early Phase 1" and phase_label("PHASE 2") == "Phase 2"
          and phase_label("NA") == "Phase NA" and phase_label("PHASE1/PHASE2") == "Phase 1/2",
          "phase_label renders EARLY/spaced/NA/combined forms cleanly")
    trials = [T("NCT1", "UNCERTAIN", "PHASE1", ["REVIEW"] * 2, {"intent": "therapeutic", "confidence": "high"}),
              T("NCT4", "UNCERTAIN", "PHASE4", ["REVIEW"] * 5, {"intent": "therapeutic", "confidence": "high"})]
    rank_trials(trials, intent_map={}, coverage_map={}, trust_attached=True)
    check(trials[0]["nct_id"] == "NCT4", "PHASE4 above PHASE1 within therapeutic despite more unresolved")

    # 5. coverage penalty: a trial read at <50% sinks below a fully-read peer of the same fit/phase
    trials = [T("NCTlow", "UNCERTAIN", "NA", ["REVIEW"] * 2 + ["PASS"] * 2, {"intent": "observational", "confidence": "high"}),
              T("NCTfull", "UNCERTAIN", "NA", ["REVIEW"] * 6 + ["PASS"] * 2, {"intent": "observational", "confidence": "high"})]
    rank_trials(trials, intent_map={}, coverage_map={"NCTlow": 30, "NCTfull": 8}, trust_attached=True)
    check(trials[0]["nct_id"] == "NCTfull", "coverage <50% penalized below a fully-read trial")

    # 6. unresolved RATIO, not count, breaks ties (2/4 beats 4/12? no: 0.5 vs 0.33 -> 4/12 first)
    trials = [T("NCTx", "UNCERTAIN", "NA", ["REVIEW"] * 2 + ["PASS"] * 2, {"intent": "observational", "confidence": "high"}),
              T("NCTy", "UNCERTAIN", "NA", ["REVIEW"] * 4 + ["PASS"] * 8, {"intent": "observational", "confidence": "high"})]
    rank_trials(trials, intent_map={}, coverage_map={}, trust_attached=True)
    check(trials[0]["nct_id"] == "NCTy", "normalized unresolved ratio (4/12 < 2/4) decides, not raw count")

    # 7. client-attached intent is ignored unless trusted; sidecar wins when present
    trials = [T("NCTa", "UNCERTAIN", "NA", ["REVIEW"] * 2, {"intent": "therapeutic", "confidence": "high"}),
              T("NCTb", "UNCERTAIN", "NA", ["REVIEW"] * 1, {"intent": "observational", "confidence": "high"})]
    rank_trials(trials, intent_map={}, coverage_map={}, trust_attached=False)
    check(trials[0]["nct_id"] == "NCTb", "untrusted attached intent cannot rig the sort (both fall to unknown tier)")
    trials = [T("NCTa", "UNCERTAIN", "NA", ["REVIEW"] * 2, {"intent": "observational", "confidence": "high"}),
              T("NCTb", "UNCERTAIN", "NA", ["REVIEW"] * 1, None)]
    rank_trials(trials, intent_map={"NCTa": {"intent": "therapeutic", "confidence": "high"}}, coverage_map={}, trust_attached=True)
    check(trials[0]["nct_id"] == "NCTa" and trials[0]["trial_intent"]["intent"] == "therapeutic",
          "sidecar intent overrides attached and is written back for display")

    # 8. stamps + reason strings present and ranks are 1..n
    check([t["rank"] for t in trials] == [1, 2] and all(t.get("rank_reason") and t.get("rank_basis") for t in trials),
          "rank / rank_reason / rank_basis stamped, ranks are a 1..n permutation")

    # 9. deterministic on the frozen demo traces + safety property on all 10 patients
    if os.path.exists(os.path.join(_HERE, "traces.json")):
        g1 = golden_from_traces()
        g2 = golden_from_traces()
        check(g1 == g2 and len(g1) == 10, "frozen-trace ranking is deterministic across runs (10 patients)")

    print("ranking selftest:", "ALL PASS" if ok else "FAILURES")
    return ok


if __name__ == "__main__":
    if "--write-golden" in sys.argv:
        with open(GOLDEN_PATH, "w", encoding="utf-8") as f:
            json.dump({"ranking_version": RANKING_VERSION, "rule_ko": RANKING_RULE_KO,
                       "order": golden_from_traces()}, f, ensure_ascii=False, indent=1)
        print("wrote", GOLDEN_PATH)
    elif "--golden" in sys.argv:
        sys.exit(0 if check_golden() else 1)
    else:
        sys.exit(0 if _selftest() else 1)
