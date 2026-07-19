#!/usr/bin/env python3
"""
evidence.py -- the evidence-sufficiency layer (건희 우선순위 1, 인수인계_v4 §6).

Traceability (does a quoted phrase exist in the record?) is not the same as
sufficiency (does that phrase actually support the conclusion drawn from it?).
The failure §6 names: "CT에서 bladder wall mass" was taken as a bladder-cancer
diagnosis AND a cystectomy indication -- but an imaging finding is neither a
histological confirmation, a muscle-invasion finding, nor a surgical indication.

So every piece of evidence carries metadata, and a pure function decides whether
that evidence is strong enough for what a criterion actually requires. Like
EFFECT_TABLE and ACTION_TABLE, the sufficiency judgment is computed in code, not
inferred by a model -- a model may fill in the metadata, but "imaging/suspected
does not equal confirmed diagnosis" is a rule, not an opinion.

The action for an insufficient piece of evidence is the same one action_policy
assigns to the INSUFFICIENT_EVIDENCE uncertainty type (VERIFY), imported here so
the two layers never disagree.

Run `python3 evidence.py` for the self-tests.
"""

from action_policy import action_for, VALID_ACTIONS

# What KIND of thing the evidence is. Ordered loosely weakest->strongest as proof
# of a definitive clinical fact, but the real strength test is confirmation level.
SOURCE_TYPES = {
    "symptom":           "환자가 호소하는 증상",
    "patient_report":    "환자 본인 진술",
    "lab":               "검사 수치",
    "imaging":           "영상 소견",
    "pathology":         "병리 결과",
    "clinical_judgment": "임상의의 판단",
}

# How settled the finding is. STRICTLY ORDERED: a criterion that needs 확진
# is not met by a 의심 finding, no matter how many of them there are.
CONFIRMATION_LEVELS = ["suspected", "provisional", "confirmed"]  # 의심 · 잠정 · 확진
_CONF_RANK = {lvl: i for i, lvl in enumerate(CONFIRMATION_LEVELS)}

DIRECTNESS = {"direct", "indirect"}  # 기준을 직접 증명 vs 간접 추론


def _norm(value, allowed, default=None):
    if value is None:
        return default
    v = str(value).strip().lower().replace(" ", "_").replace("-", "_")
    return v if v in allowed else default


def confirmation_rank(level):
    """Numeric rank of a confirmation level, or -1 if unknown. Pure."""
    return _CONF_RANK.get(_norm(level, _CONF_RANK), -1)


def assess_evidence(evidence, required_confirmation="confirmed", requires_direct=True):
    """Decide whether one piece of evidence is SUFFICIENT for what a criterion needs.

    evidence: dict with keys source_type, confirmation_level, directness, supports,
              does_not_support (any may be missing; missing -> treated as weakest).
    required_confirmation: the confirmation level the criterion demands (default the
              strictest, 'confirmed' -- most eligibility criteria mean a settled fact).
    requires_direct: whether the criterion needs the evidence to prove it directly
              rather than by indirect inference.

    Returns {sufficient: bool, reason: str, suggested_action: str|None}. When
    insufficient, suggested_action is VERIFY (establish the missing confirmation),
    matching action_policy's INSUFFICIENT_EVIDENCE mapping. Pure function.
    """
    have = confirmation_rank(evidence.get("confirmation_level"))
    need = confirmation_rank(required_confirmation)
    if need < 0:
        need = _CONF_RANK["confirmed"]

    directness = _norm(evidence.get("directness"), DIRECTNESS, default="indirect")

    reasons = []
    sufficient = True
    if have < need:
        sufficient = False
        have_lbl = CONFIRMATION_LEVELS[have] if have >= 0 else "unknown"
        reasons.append(
            f"confirmation {have_lbl} < required {CONFIRMATION_LEVELS[need]}"
        )
    if requires_direct and directness == "indirect":
        sufficient = False
        reasons.append("evidence is indirect but criterion needs direct proof")

    if sufficient:
        return {"sufficient": True, "reason": "meets required confirmation and directness",
                "suggested_action": None}

    action = action_for("INSUFFICIENT_EVIDENCE")  # -> VERIFY, single source of truth
    assert action in VALID_ACTIONS
    return {"sufficient": False, "reason": "; ".join(reasons), "suggested_action": action}


def _selftest():
    failures = []

    def check(cond, msg):
        if not cond:
            failures.append(msg)

    # ordering is strict and total
    check(confirmation_rank("suspected") < confirmation_rank("provisional") < confirmation_rank("confirmed"),
          "confirmation levels must be strictly ordered")
    check(confirmation_rank("garbage") == -1, "unknown level -> -1")
    check(confirmation_rank("CONFIRMED") == 2, "normalization should be case-insensitive")

    # THE §6 worked example: bladder wall mass on CT must NOT satisfy a
    # confirmed-cancer / cystectomy-indication criterion.
    ct_mass = {
        "source_type": "imaging", "confirmation_level": "suspected",
        "directness": "indirect",
        "supports": "possible bladder pathology",
        "does_not_support": "histologic cancer confirmation, muscle invasion, cystectomy indication",
    }
    r = assess_evidence(ct_mass, required_confirmation="confirmed", requires_direct=True)
    check(r["sufficient"] is False, "CT suspected mass must be INSUFFICIENT for confirmed dx")
    check(r["suggested_action"] == "VERIFY", "insufficient evidence must route to VERIFY")

    # a real pathology confirmation IS sufficient
    biopsy = {"source_type": "pathology", "confirmation_level": "confirmed", "directness": "direct",
              "supports": "urothelial carcinoma confirmed"}
    r2 = assess_evidence(biopsy, required_confirmation="confirmed", requires_direct=True)
    check(r2["sufficient"] is True, "confirmed direct pathology must be sufficient")
    check(r2["suggested_action"] is None, "sufficient evidence needs no action")

    # a lab value that directly meets a lab-threshold criterion (needs only provisional)
    lab = {"source_type": "lab", "confirmation_level": "provisional", "directness": "direct"}
    r3 = assess_evidence(lab, required_confirmation="provisional", requires_direct=True)
    check(r3["sufficient"] is True, "provisional direct lab meeting a provisional bar is sufficient")

    # indirect evidence fails a direct-proof criterion even at high confirmation
    indirect = {"source_type": "imaging", "confirmation_level": "confirmed", "directness": "indirect"}
    r4 = assess_evidence(indirect, required_confirmation="confirmed", requires_direct=True)
    check(r4["sufficient"] is False, "indirect evidence must fail a direct-proof requirement")

    # missing metadata is treated as weakest, never silently sufficient
    r5 = assess_evidence({}, required_confirmation="confirmed")
    check(r5["sufficient"] is False, "empty evidence must never be sufficient for a confirmed bar")

    if failures:
        print("FAIL:")
        for f in failures:
            print("  -", f)
        raise SystemExit(1)
    print(f"evidence self-tests passed "
          f"({len(SOURCE_TYPES)} source types, {len(CONFIRMATION_LEVELS)} confirmation levels).")


if __name__ == "__main__":
    _selftest()
