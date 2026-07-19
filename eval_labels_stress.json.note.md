# Trial intent scope note

All 5 base trials in this answer key (NCT05879653, NCT07167368, NCT07214727,
NCT06906549, NCT06291935) are `studyType=INTERVENTIONAL` /
`primaryPurpose=TREATMENT` per ClinicalTrials.gov API v2. This was not
deliberate -- it fell out of the trial-selection criteria in the write-up
(favoring trials with numeric cutoffs + free-text ambiguity + multi-criterion
conflicts, which skewed toward active treatment trials).

Consequence: this 40-case set never exercises cross-intent ranking (e.g. a
prevention or care-delivery trial competing against a treatment trial in the
same recommendation list). If the team adds non-TREATMENT trials to the
stress set later, the ranking/ordering behavior those cases test is new
ground this set does not cover.
