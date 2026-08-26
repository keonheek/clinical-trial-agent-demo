"""ranking.py -- deterministic, explainable recommendation priority (추천 우선순위).

Pure stdlib. NO LLM client imports (this module is bundled into the serverless api/ handlers,
which must stay zero-LLM -- same rule as action_policy.py and patient_need.py). Selftest:
`python3 ranking.py`. Golden order over the frozen demo traces: `python3 ranking.py --golden`
(check) / `--write-golden` (regenerate expected_ranking.json after a deliberate key change).

WHY THIS SHAPE. Organizer email #2 made the per-patient priority order the ONE binding
deliverable. Keonhee's 08-18 step-back locked the logic tree: trials exist to help patients who
need help, so the order answers three questions asked IN ORDER, and the sort key is exactly
three groups (lexicographic; earlier groups dominate; every term is a fact of the trial record,
a code-derived count, or the deterministic patient_need classifier -- never a model opinion):

  Q1 참여 (gate)  "Can they join?"
     INELIGIBLE (any hard FAIL) sinks to the bottom and is never out-ranked -- the safety claim
     on the deck. Within the excluded: fewer blocking FAILs first.
  Q2 도움 (help)  "Will it help them?"
     patient_need x trial_intent match via patient_need.HELP_MATRIX (부합 2 > 부분 1 > 무관/
     미확인 0; a low-confidence or unclassified trial intent falls to the row's worst cell -- a
     hedged guess never lifts a trial). Sub-key inside the help group: Phase 부담 (PHASE4 best
     ... PHASE1/EARLY worst, NA mid -- a later phase means a better-characterized intervention,
     lower burden/uncertainty for the patient). When the patient's need was not computed
     (need=None) the help group falls back to intent-only order (치료 < 증상 완화 < 추적관찰 < 관찰,
     low-confidence demoted) and rank_reason flags it: "환자 필요 미산출".
  Q3 확실 (sure)  "How sure are we?"
     ELIGIBLE before UNCERTAIN, then coverage penalty (parsed/raw < 50% sinks below fully-read
     trials), then unresolved ratio (REVIEW/parsed), then unresolved count, then nct_id
     (stable, reproducible last resort).

PRINCIPLE CHANGE (deliberate, Keonhee 08-18): help comes BEFORE eligibility-certainty. A trial
that serves the patient's need but is still UNCERTAIN may out-rank a trial that is ELIGIBLE but
does not serve the need. Hard exclusion stays absolute (Q1). This replaces the 08-16 8-tier key
(eligibility class > FAIL count > 중재 목적 > Phase > coverage > ratio > count > nct), where
certainty sat above usefulness.

INVARIANTS: eval.py never reads `rank`, and traces.json is never written -- this module re-ranks
IN MEMORY at serve time (api/trace.py, live_server.py) and inside pipeline.recommend() for
generation/answer rounds. The frozen 82.5% n=40 pairing cannot move.
"""
import json
import os
import sys

import patient_need as pn

RANKING_VERSION = "2026-08-18"

ELIGIBILITY_ORDER = {"ELIGIBLE": 0, "UNCERTAIN": 1, "INELIGIBLE": 2}

# Intent-only order, used ONLY when the patient's need was not computed (need=None fallback).
FIT_ORDER = {"therapeutic": 0, "supportive": 1, "care_delivery": 2, "observational": 3}
FIT_UNKNOWN = 3  # unclassified / low-confidence -> same tier as observational (demote, never lift)

PHASE_BURDEN = {"phase4": 0, "phase3": 1, "phase2": 2, "phase1": 3, "earlyphase1": 3,
                "phase2/phase3": 1, "phase1/phase2": 2}
PHASE_BURDEN_DEFAULT = 2  # NA / unknown: burden not characterized by phase -> middle

LOW_COVERAGE_CUTOFF = 0.5

# One-line statement of the executed rule, for the UI and the deck. Must match rank_key.
# The three questions, in plain words -- no technical term without a plain-word label.
RANKING_RULE_KO = ("참여할 수 있는가 -- 부적격(탈락) 시험은 항상 맨 아래 · "
                   "도움이 되는가 -- 환자 임상 요구(치료/진단 확정/추적관찰/증상 완화)와 시험 목적이 부합하는 순, "
                   "같으면 검증이 더 된 후기 단계(Phase 4→1) 먼저 · "
                   "얼마나 확실한가 -- 적격 확정이 미확정보다 먼저, 원문을 절반도 못 읽었으면 감점, "
                   "미해결 기준이 적은 순")

FIT_LABEL_KO = {"therapeutic": "치료 목적", "supportive": "증상 완화", "care_delivery": "의료전달",
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
    non-observational intent moves a trial up; everything else lands on the observational tier.
    Used ONLY for the need=None fallback ordering inside the help group -- when a need exists,
    patient_need.helps() (which applies the same low-confidence demotion) decides instead."""
    if not isinstance(intent, dict):
        return FIT_UNKNOWN
    if str(intent.get("confidence", "low")).lower() != "high":
        return FIT_UNKNOWN
    return FIT_ORDER.get(intent.get("intent"), FIT_UNKNOWN)


def _known_intent(intent):
    """The trial intent name IF it is high-confidence and in the known vocabulary, else None.
    Unlike fit_rank, a confirmed observational intent counts as known -- the help matrix can
    score it as the DIRECT match (diagnosis/monitoring needs)."""
    if not isinstance(intent, dict):
        return None
    if str(intent.get("confidence", "low")).lower() != "high":
        return None
    name = intent.get("intent")
    return name if name in FIT_ORDER else None


def _need_name(need):
    """Accepts classify_patient_need's dict, a bare need string, or None."""
    if isinstance(need, dict):
        return need.get("need")
    if isinstance(need, str):
        return need
    return None


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


def _blocking_detail(criteria):
    """The FAIL criteria as UI-ready rows: the criterion's own text plus a polarity label.

    A count answers "how many", which the 08-23 team review found unusable: a clinician who
    picked criteria 1 and 3 instead of 1 and 2 sees 부적격 and cannot tell which criterion did
    it. The text was never discarded -- every criterion in traces.json carries text/type/
    verdict/effect/evidence/reasoning -- it just never reached the rank surface.

    Polarity is read off `type`, never off `verdict`: the two-layer model means verdict=MET is
    a FAIL on an exclusion and a PASS on an inclusion, so labelling from the verdict is exactly
    the inverted-display bug the two layers exist to prevent.
    """
    out = []
    for c in criteria or []:
        if c.get("effect") != "FAIL":
            continue
        excl = c.get("type") == "exclusion"
        out.append({
            "text": c.get("text") or "",
            "type": c.get("type"),
            "label_ko": "배제 기준 충족" if excl else "포함 기준 미충족",
            "label_en": "exclusion met" if excl else "inclusion not met",
            "reasoning": c.get("reasoning") or "",
            "evidence": c.get("evidence") or "",
        })
    return out


def _resolvable_detail(criteria):
    """The REVIEW criteria -- the ones that are still open and could still settle the verdict.

    Item 2 of the review ("what would make this patient 적격") in its answerable form: the path
    is 'these FAILs would have to not hold, and these REVIEWs need confirming'. The transcript's
    other reading -- enumerate the optimal passing combination -- is combinatorial, and the team
    flagged 변수가 많다 in the same breath, so it is deliberately not attempted here.
    """
    return [{"text": c.get("text") or "", "type": c.get("type"),
             "action": c.get("action"), "action_scope": c.get("action_scope")}
            for c in criteria or [] if c.get("effect") == "REVIEW"]


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
        # extra demo patients (gen_extra.py) ship their trials' sidecar entries separately so
        # the canonical files stay untouched; merged here so every caller sees one map.
        try:
            with open(os.path.join(_HERE, name.replace(".json", "_extra.json")), encoding="utf-8") as f:
                for k, v in json.load(f).items():
                    _SIDECARS[key].setdefault(k, v)  # canonical wins; extra only fills gaps
        except (FileNotFoundError, json.JSONDecodeError):
            pass
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


def rank_key(trial, intent=None, raw_estimated=None, need=None):
    """(gate, help, sure) -- the locked three-question tree as a nested lexicographic key.
    `need` is classify_patient_need's dict (or a bare need string) for THE patient this list
    belongs to: pass the same need for every trial in one sort. None -> the help group falls
    back to intent-only order (its leading discriminator keeps the two modes from ever
    comparing against each other)."""
    n, fails, reviews = _counts(trial.get("criteria"))
    ratio = round(reviews / n, 3) if n else 1.0
    elig = trial.get("eligibility", "UNCERTAIN")

    gate = (1 if elig == "INELIGIBLE" else 0, fails)

    burden = phase_burden(trial.get("phase"))
    nname = _need_name(need)
    if nname in pn.VALID_NEEDS:
        # helps() scores 2 best -> invert so smaller sorts first; low-confidence/unknown
        # trial intent already fell to the row's worst cell inside helps().
        help_group = (0, 2 - pn.helps(nname, intent), burden)
    else:
        help_group = (1, fit_rank(intent), burden)

    sure = (
        ELIGIBILITY_ORDER.get(elig, 1),
        coverage_penalty(n, raw_estimated),
        ratio,
        reviews,
        str(trial.get("nct_id", "")),
    )
    return (gate, help_group, sure)


def _josa(word, with_final, without_final):
    """받침 유무에 따라 조사를 고른다 — "진단 확정를"처럼 틀린 조사가 붙는 걸 막는다.

    네 가지 요구 라벨(치료·진단 확정·추적관찰·증상 완화) 중 "진단 확정"만 받침으로 끝나서, 조사를
    고정으로 박아 두면 그 하나만 어색해진다.
    """
    if not word:
        return with_final
    last = word.strip()[-1]
    if not ("가" <= last <= "힣"):
        return with_final
    return with_final if (ord(last) - 0xAC00) % 28 else without_final


def _help_sentence(nname, need_conf, score, known_intent, phase_txt, guess_intent=None):
    """The 도움 part of rank_reason, plain Korean. Phase NA carries no information for
    non-interventional trials, so an empty phase_txt is simply omitted (08-20 UI review);
    when the intent is only a low-confidence guess, say the guess instead of claiming the
    system has no opinion (the chip next to the sentence shows the guess)."""
    def paren(fit_ko=None):
        # 라벨이 이미 "연구"로 끝나면 "시험"을 덧붙이지 않는다 ("관찰 연구 시험"은 중복).
        parts = [x for x in (fit_ko or None, phase_txt or None) if x]
        return f" ({', '.join(parts)})" if parts else ""
    if nname in pn.VALID_NEEDS:
        need_ko = pn.NEED_KO[nname]
        if known_intent is None:
            if guess_intent in FIT_LABEL_KO:
                txt = (f"{need_ko} 필요, 시험 목적 미확정 "
                       f"(추정: {FIT_LABEL_KO[guess_intent]}{', ' + phase_txt if phase_txt else ''})")
            else:
                txt = f"{need_ko} 필요, 시험 목적 미확인{paren()}"
        else:
            fit_ko = FIT_LABEL_KO[known_intent]
            # 명사만 쌓으면 기계가 뱉은 문장처럼 읽힌다 (08-23 리뷰: "띵 치료라고 하면
            # 당연히 치료해야지"). 필요와 시험 목적의 관계를 문장으로 드러낸다.
            if score == 2:
                txt = f"{need_ko} 필요에 맞음{paren(fit_ko)}"
            elif score == 1:
                txt = f"{need_ko} 필요에 일부 도움{paren(fit_ko)}"
            else:
                txt = f"{need_ko} 필요와 방향 다름{paren(fit_ko)}"
        if need_conf == "low":
            txt += " · 필요 분류 확신 낮음"
        return txt
    if known_intent is None:
        return f"환자 필요·시험 목적 모두 미확인{paren()}"
    return f"환자 필요 미산출 → 시험 목적 순{paren(FIT_LABEL_KO[known_intent])}"


def rank_basis(trial, intent=None, raw_estimated=None, need=None):
    """The fired components of the three groups, as UI-ready chips (each chip carries
    group: join | help | sure) + the rank_reason sentence -- the three questions answered in
    plain Korean, e.g. '참여: 미확정 · 도움: 치료 필요와 부합 (치료 목적 시험, Phase 4) · '
    '확실: 미해결 10/12, 원문 39% (감점)'."""
    n, fails, reviews = _counts(trial.get("criteria"))
    elig = trial.get("eligibility", "UNCERTAIN")
    intent_name = intent.get("intent") if isinstance(intent, dict) else None
    conf = intent.get("confidence") if isinstance(intent, dict) else None
    known_intent = _known_intent(intent)
    nname = _need_name(need)
    need_conf = need.get("confidence") if isinstance(need, dict) else None
    score = pn.helps(nname, intent) if nname in pn.VALID_NEEDS else None
    cov = coverage_ratio(n, raw_estimated)
    pen = coverage_penalty(n, raw_estimated)

    # -- chips, grouped by the three questions (tier kept numeric for stable UI sort order) --
    basis = [{"key": "eligibility", "label": "참여", "value": elig, "group": "join", "tier": 0}]
    if fails:
        basis.append({"key": "blocking", "label": "차단 기준", "value": fails,
                      "texts": _blocking_detail(trial.get("criteria")),
                      "group": "join", "tier": 0})
    if reviews:
        basis.append({"key": "to_resolve", "label": "확인 필요", "value": reviews,
                      "texts": _resolvable_detail(trial.get("criteria")),
                      "group": "join", "tier": 0})
    if nname in pn.VALID_NEEDS:
        basis.append({"key": "need", "label": "환자 필요", "value": pn.NEED_KO[nname], "need": nname,
                      "confidence": need_conf, "group": "help", "tier": 1})
        basis.append({"key": "help", "label": "", "value": pn.help_label_ko(score), "score": score,
                      "group": "help", "tier": 1})
    else:
        basis.append({"key": "need", "label": "환자 필요", "value": "미산출", "need": None,
                      "group": "help", "tier": 1})
    fr = fit_rank(intent)
    if fr < FIT_UNKNOWN:
        basis.append({"key": "fit", "label": "시험 목적", "value": intent_name,
                      "confidence": conf, "group": "help", "tier": 1})
    else:
        basis.append({"key": "fit", "label": "시험 목적",
                      "value": intent_name or "unclassified",
                      "confidence": conf, "demoted": True, "group": "help", "tier": 1})
    basis.append({"key": "phase", "label": "Phase", "value": (trial.get("phase") or "NA"),
                  "burden": phase_burden(trial.get("phase")), "group": "help", "tier": 1})
    if cov is not None:
        basis.append({"key": "coverage", "label": "원문 커버리지", "value": round(cov, 2),
                      "penalty": bool(pen), "group": "sure", "tier": 2})
    basis.append({"key": "open", "label": "미해결", "value": f"{reviews}/{n}", "group": "sure", "tier": 2})

    # -- rank_reason: the three questions in one plain-Korean line --
    join_txt = ELIG_LABEL_KO.get(elig, elig) + (f" (차단 기준 {fails}건)" if fails else "")
    _ph = phase_label(trial.get("phase"))
    _guess = intent.get("intent") if isinstance(intent, dict) and str(intent.get("confidence", "")).lower() == "low" else None
    help_txt = _help_sentence(nname, need_conf, score, known_intent,
                              "" if _ph == "Phase NA" else _ph, guess_intent=_guess)
    sure_txt = f"미해결 {reviews}/{n}"
    if cov is not None:
        # parsed can exceed the line-count estimate (multi-clause bullets split into atomic
        # criteria) -- never assert more than "전체(추정)", the estimator is an approximation.
        sure_txt += (", 원문 전체(추정)" if cov >= 1.0
                     else f", 원문 {int(round(cov * 100))}%" + (" (감점)" if pen else ""))
    reason = " · ".join([f"참여: {join_txt}", f"도움: {help_txt}", f"확실: {sure_txt}"])
    return basis, reason


def rank_trials(trials, intent_map=None, coverage_map=None, trust_attached=False, patient_need=None):
    """Sort `trials` in place by rank_key and stamp rank / rank_reason / rank_basis /
    ranking_version on each. Returns the same list. Also normalizes trial["trial_intent"] to the
    server-side sidecar value when one exists (display and sort then agree).

    trials: dicts with nct_id, phase, eligibility, criteria[{effect,...}] (+ optional
    trial_intent). intent_map / coverage_map default to the repo-root sidecars.
    patient_need: classify_patient_need's dict for the ONE patient this list belongs to, or
    None -> the help group falls back to intent-only order and every rank_reason flags
    "환자 필요 미산출"."""
    side = _load_sidecars()
    intent_map = side["intent"] if intent_map is None else intent_map
    coverage_map = side["coverage"] if coverage_map is None else coverage_map

    keyed = []
    for t in trials:
        intent = resolve_intent(t, intent_map, trust_attached)
        if intent and (intent_map or {}).get(t.get("nct_id")):
            t["trial_intent"] = {"intent": intent["intent"], "confidence": intent.get("confidence", "low")}
        raw = (coverage_map or {}).get(t.get("nct_id"))
        keyed.append((rank_key(t, intent, raw, patient_need), t, intent, raw))
    keyed.sort(key=lambda x: x[0])
    trials[:] = [t for _, t, _, _ in keyed]
    for i, (_, t, intent, raw) in enumerate(keyed):
        t["rank"] = i + 1
        basis, reason = rank_basis(t, intent, raw, patient_need)
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
        need = pn.classify_patient_need(tr.get("patient_text", ""))
        trials = [dict(t, criteria=[dict(c) for c in t.get("criteria", [])]) for t in tr["trials"]]
        rank_trials(trials, patient_need=need)
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

    NEED_TX = {"need": "treatment", "need_ko": "치료", "confidence": "high", "reasons": []}
    NEED_DX = {"need": "diagnosis", "need_ko": "진단 확정", "confidence": "high", "reasons": []}

    # 0. the key is exactly three groups
    k = rank_key(T("NCT0", "UNCERTAIN", "NA", ["REVIEW"]), None, None, NEED_TX)
    check(len(k) == 3 and all(isinstance(g, tuple) for g in k), "rank_key returns (gate, help, sure)")

    # 1. GATE: a hard exclusion is never out-ranked, whatever help/certainty say
    trials = [T("NCT1", "INELIGIBLE", "PHASE4", ["FAIL"], {"intent": "therapeutic", "confidence": "high"}),
              T("NCT2", "UNCERTAIN", "NA", ["REVIEW"] * 12, {"intent": "observational", "confidence": "low"})]
    rank_trials(trials, intent_map={}, coverage_map={}, trust_attached=True, patient_need=NEED_TX)
    check(trials[0]["nct_id"] == "NCT2" and hard_exclusion_holds(trials),
          "gate: INELIGIBLE helps-need P4 trial stays below UNCERTAIN no-help trial")

    # 2. HELP BEFORE CERTAINTY (the 08-18 principle change): a trial that helps the need but is
    # UNCERTAIN out-ranks a trial that is ELIGIBLE but does not help
    trials = [T("NCTa", "ELIGIBLE", "NA", ["PASS"] * 4, {"intent": "observational", "confidence": "high"}),
              T("NCTb", "UNCERTAIN", "PHASE2", ["REVIEW"] * 6 + ["PASS"] * 2, {"intent": "therapeutic", "confidence": "high"})]
    rank_trials(trials, intent_map={}, coverage_map={}, trust_attached=True, patient_need=NEED_TX)
    check(trials[0]["nct_id"] == "NCTb", "help before certainty: helps+UNCERTAIN outranks not-helps+ELIGIBLE")

    # 3. certainty INSIDE equal help: ELIGIBLE before UNCERTAIN
    trials = [T("NCTu", "UNCERTAIN", "PHASE2", ["REVIEW"] * 2 + ["PASS"] * 2, {"intent": "therapeutic", "confidence": "high"}),
              T("NCTe", "ELIGIBLE", "PHASE2", ["PASS"] * 4, {"intent": "therapeutic", "confidence": "high"})]
    rank_trials(trials, intent_map={}, coverage_map={}, trust_attached=True, patient_need=NEED_TX)
    check(trials[0]["nct_id"] == "NCTe", "equal help: ELIGIBLE before UNCERTAIN (sure group)")

    # 4. the help matrix really drives: for a DIAGNOSIS need, an observational registry is the
    # direct match and out-ranks a therapeutic trial (partial credit only)
    trials = [T("NCTther", "UNCERTAIN", "PHASE4", ["REVIEW"] * 2, {"intent": "therapeutic", "confidence": "high"}),
              T("NCTobs", "UNCERTAIN", "NA", ["REVIEW"] * 5, {"intent": "observational", "confidence": "high"})]
    rank_trials(trials, intent_map={}, coverage_map={}, trust_attached=True, patient_need=NEED_DX)
    check(trials[0]["nct_id"] == "NCTobs", "need x intent: observational is the direct match for a diagnosis need")

    # 5. low-confidence intent demotes INSIDE the help matrix (worst cell, never lifted)
    trials = [T("NCTsup", "UNCERTAIN", "NA", ["REVIEW"] * 5, {"intent": "supportive", "confidence": "high"}),
              T("NCTther", "UNCERTAIN", "PHASE4", ["REVIEW"] * 1, {"intent": "therapeutic", "confidence": "low"})]
    rank_trials(trials, intent_map={}, coverage_map={}, trust_attached=True, patient_need=NEED_TX)
    check(trials[0]["nct_id"] == "NCTsup",
          "low-confidence therapeutic falls to worst cell, below confirmed supportive (partial help)")

    # 6. phase burden inside equal help: PHASE4 before PHASE1; normalization forms
    check(phase_burden("PHASE 2") == phase_burden("PHASE2") == 2, "phase normalization 'PHASE 2' == 'PHASE2'")
    check(phase_burden("EARLY_PHASE1") == phase_burden("PHASE1") == 3, "EARLY_PHASE1 == PHASE1 burden")
    check(phase_burden("NA") == PHASE_BURDEN_DEFAULT == phase_burden(None), "NA/None -> default mid burden")
    check(phase_label("EARLY_PHASE1") == "Early Phase 1" and phase_label("PHASE 2") == "Phase 2"
          and phase_label("NA") == "Phase NA" and phase_label("PHASE1/PHASE2") == "Phase 1/2",
          "phase_label renders EARLY/spaced/NA/combined forms cleanly")
    trials = [T("NCT1", "UNCERTAIN", "PHASE1", ["REVIEW"] * 2, {"intent": "therapeutic", "confidence": "high"}),
              T("NCT4", "UNCERTAIN", "PHASE4", ["REVIEW"] * 5, {"intent": "therapeutic", "confidence": "high"})]
    rank_trials(trials, intent_map={}, coverage_map={}, trust_attached=True, patient_need=NEED_TX)
    check(trials[0]["nct_id"] == "NCT4", "PHASE4 above PHASE1 within equal help despite more unresolved")

    # 7. need=None fallback: intent-only order, flagged in the reason
    trials = [T("NCTobs", "UNCERTAIN", "NA", ["REVIEW"] * 1, {"intent": "observational", "confidence": "high"}),
              T("NCTther", "UNCERTAIN", "NA", ["REVIEW"] * 5, {"intent": "therapeutic", "confidence": "high"})]
    rank_trials(trials, intent_map={}, coverage_map={}, trust_attached=True, patient_need=None)
    check(trials[0]["nct_id"] == "NCTther", "need=None: help group falls back to intent-only order")
    check(all("환자 필요 미산출" in t["rank_reason"] for t in trials),
          "need=None: every rank_reason flags 환자 필요 미산출")

    # 8. coverage penalty (sure group): read at <50% sinks below a fully-read peer of equal help
    trials = [T("NCTlow", "UNCERTAIN", "NA", ["REVIEW"] * 2 + ["PASS"] * 2, {"intent": "observational", "confidence": "high"}),
              T("NCTfull", "UNCERTAIN", "NA", ["REVIEW"] * 6 + ["PASS"] * 2, {"intent": "observational", "confidence": "high"})]
    rank_trials(trials, intent_map={}, coverage_map={"NCTlow": 30, "NCTfull": 8}, trust_attached=True,
                patient_need=NEED_TX)
    check(trials[0]["nct_id"] == "NCTfull", "coverage <50% penalized below a fully-read trial")

    # 9. unresolved RATIO, not count, breaks ties (0.5 vs 0.33 -> 4/12 first)
    trials = [T("NCTx", "UNCERTAIN", "NA", ["REVIEW"] * 2 + ["PASS"] * 2, {"intent": "observational", "confidence": "high"}),
              T("NCTy", "UNCERTAIN", "NA", ["REVIEW"] * 4 + ["PASS"] * 8, {"intent": "observational", "confidence": "high"})]
    rank_trials(trials, intent_map={}, coverage_map={}, trust_attached=True, patient_need=NEED_TX)
    check(trials[0]["nct_id"] == "NCTy", "normalized unresolved ratio (4/12 < 2/4) decides, not raw count")

    # 10. client-attached intent is ignored unless trusted; sidecar wins when present
    trials = [T("NCTa", "UNCERTAIN", "NA", ["REVIEW"] * 2, {"intent": "therapeutic", "confidence": "high"}),
              T("NCTb", "UNCERTAIN", "NA", ["REVIEW"] * 1, {"intent": "observational", "confidence": "high"})]
    rank_trials(trials, intent_map={}, coverage_map={}, trust_attached=False, patient_need=NEED_TX)
    check(trials[0]["nct_id"] == "NCTb", "untrusted attached intent cannot rig the sort (both fall to worst cell)")
    trials = [T("NCTa", "UNCERTAIN", "NA", ["REVIEW"] * 2, {"intent": "observational", "confidence": "high"}),
              T("NCTb", "UNCERTAIN", "NA", ["REVIEW"] * 1, None)]
    rank_trials(trials, intent_map={"NCTa": {"intent": "therapeutic", "confidence": "high"}}, coverage_map={},
                trust_attached=True, patient_need=NEED_TX)
    check(trials[0]["nct_id"] == "NCTa" and trials[0]["trial_intent"]["intent"] == "therapeutic",
          "sidecar intent overrides attached and is written back for display")

    # 11. stamps + three-question reason + grouped chips; ranks are 1..n
    check([t["rank"] for t in trials] == [1, 2] and all(t.get("rank_reason") and t.get("rank_basis") for t in trials),
          "rank / rank_reason / rank_basis stamped, ranks are a 1..n permutation")
    r = trials[0]["rank_reason"]
    check(all(m in r for m in ("참여:", "도움:", "확실:")), "rank_reason answers the three questions")
    groups = {b.get("group") for b in trials[0]["rank_basis"]}
    check(groups <= {"join", "help", "sure"} and {"join", "help", "sure"} <= groups,
          "rank_basis chips carry group join/help/sure")

    # 11b. the blocking chip carries the criterion TEXT, polarity-labelled off `type` (the
    # 08-23 review: a count cannot tell a clinician WHICH criterion closed the path).
    ct = [{"effect": "FAIL", "type": "exclusion", "text": "활동성 감염", "reasoning": "r1", "evidence": "e1"},
          {"effect": "FAIL", "type": "inclusion", "text": "ECOG 0-1", "reasoning": "r2", "evidence": "e2"},
          {"effect": "REVIEW", "type": "inclusion", "text": "간기능 수치", "action": "ASK"},
          {"effect": "PASS", "type": "inclusion", "text": "연령 19세 이상"}]
    b, _ = rank_basis({"criteria": ct, "eligibility": "INELIGIBLE", "phase": "PHASE2"})
    blk = next(x for x in b if x["key"] == "blocking")
    check(blk["value"] == 2 and [t["text"] for t in blk["texts"]] == ["활동성 감염", "ECOG 0-1"],
          "blocking chip carries both FAIL criterion texts")
    check([t["label_ko"] for t in blk["texts"]] == ["배제 기준 충족", "포함 기준 미충족"],
          "blocking polarity label is read off type, not verdict")
    res = next(x for x in b if x["key"] == "to_resolve")
    check(res["value"] == 1 and res["texts"][0]["text"] == "간기능 수치",
          "to_resolve chip carries the REVIEW criterion text (the path to 적격)")
    check(all(x["key"] != "blocking" for x in rank_basis({"criteria": ct[2:]})[0]),
          "no blocking chip when nothing FAILs")

    # 12. deterministic on the frozen demo traces + safety property on all 10 patients
    if os.path.exists(os.path.join(_HERE, "traces.json")):
        g1 = golden_from_traces()
        g2 = golden_from_traces()
        check(g1 == g2 and len(g1) == 10, "frozen-trace ranking is deterministic across runs (10 patients)")

    print("ranking selftest:", "ALL PASS" if ok else "FAILURES")
    return ok


if __name__ == "__main__":
    if "--write-golden" in sys.argv:
        with open(TRACES_PATH, encoding="utf-8") as f:
            _needs = {tr["patient_id"]: pn.classify_patient_need(tr.get("patient_text", ""))["need"]
                      for tr in json.load(f)}
        with open(GOLDEN_PATH, "w", encoding="utf-8") as f:
            json.dump({"ranking_version": RANKING_VERSION, "rule_ko": RANKING_RULE_KO,
                       "patient_need": _needs, "order": golden_from_traces()}, f,
                      ensure_ascii=False, indent=1)
        print("wrote", GOLDEN_PATH)
    elif "--golden" in sys.argv:
        sys.exit(0 if check_golden() else 1)
    else:
        sys.exit(0 if _selftest() else 1)
