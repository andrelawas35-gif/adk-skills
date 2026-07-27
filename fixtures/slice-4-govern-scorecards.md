# Slice 4 Behavioral Fixture — Govern Scorecards

This fixture proves that a scorecard reviews attributable outcomes without
becoming an activity metric, identity model, or automatic workflow governor.

## Scenario 1 — Conflicting signals remain dimension-level evidence

**Given**: A completed Work Object delivered a useful artifact, but its
recovery record shows a delayed rollback and its decision record shows one
unresolved assumption.
**When**: The user requests a scorecard review.
**Then**:

1. The scorecard records artifact value, recovery quality, and decision quality
   separately with evidence, inference, confidence, exceptions, and revisit
   triggers.
2. It preserves the favorable artifact signal and contrary recovery signal; it
   does not compute a composite score.
3. Unavailable evidence for novelty yield is recorded as `insufficient`.

**Verification**: A reviewer can see the conflict and evidence gap without a
single rating that conceals either condition.

## Scenario 2 — A scorecard proposal remains unconfirmed

**Given**: A bounded scorecard finds repeated routing delay in one support
workflow and cites its outcome evidence, scope, exceptions, and confidence.
**When**: The scorecard recommends a change.
**Then**:

1. It creates or routes an unconfirmed Workflow Candidate with the scorecard
   as origin plus supporting and contrary evidence.
2. It routes to `maintain-working-method` for bounded testing and
   contrary-evidence review.
3. It does not promote, apply, deploy, or directly modify a Working Method,
   skill, adapter, or workflow rule.

**Verification**: The proposal is attributable and useful, but no governance
change occurs without the existing explicit human confirmation gate.

## Scenario 3 — A material revision creates a linked successor

**Given**: Later scorecard evidence shows the proposed routing rule works for
support workflows but should exclude incident response.
**When**: The authorized maintenance path revises the proposed rule.
**Then**:

1. It creates a successor version linked by `supersedes`.
2. It preserves the earlier candidate, original scorecard evidence, scope,
   exceptions, confidence, and version history.
3. It does not edit the predecessor in place or claim the successor governs
   outside its revised scope.

**Verification**: The revision is reviewable and the prior rationale remains
auditable.

## Scenario 4 — Anti-gaming and identity protections hold

**Given**: A review has high message counts, many artifacts, and a user-provided
personal-fit signal for one bounded context.
**When**: The scorecard is produced.
**Then**:

1. It does not use message counts, hours, streaks, or artifact volume as a
   score or optimization target.
2. It records personal fit only as scoped attributable evidence and does not
   infer identity, personality, enduring preference, or capability.
3. It does not read personal-archive content without an approved Evidence
   Bridge reference.
4. It records novelty yield only when a useful option or falsified assumption
   is attributable; it does not reward novelty churn.

**Verification**: The scorecard is outcome-grounded and cannot be improved by
activity inflation or identity claims.
