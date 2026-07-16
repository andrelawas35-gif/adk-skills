# Slice 4 Behavioral Fixture — Maintain Working Method

This fixture proves the candidate-maintenance contract: an evidence-bearing
proposal can originate from an outcome-review, retain support and challenge,
be tested only within a stated boundary, and become a separate Working Method
only after scoped proof and explicit human confirmation.

## Scenario 1 — Outcome-review creates an attributable candidate

**Given**: An outcome-review of a completed Work Object finds that a short
handoff checklist helped within one product team's weekly review. The review,
its bounded scope, and the supporting evidence are available locally.
**When**: The user asks to retain the learning as a candidate.
**Then**:

1. The skill creates an immutable candidate identity with the proposed rule,
   scope, origin references, timestamps, and append-only lifecycle event.
2. It records the outcome-review as origin and the favorable observation as
   supporting evidence, not universal proof.
3. It records no broader rule application or Working Method.

**Verification**: The candidate is traceable to the outcome-review and its
claim is limited to the stated team and weekly-review context.

## Scenario 2 — Contrary evidence remains a bounded finding

**Given**: A later review finds one team where the checklist added delay, and
the permitted local source review finds no further challenge during the next
two weekly reviews.
**When**: The skill records evidence and performs the contrary-evidence review.
**Then**:

1. It appends the delay as contrary evidence with source, date, and scope.
2. It records the favorable observation separately as supporting evidence.
3. It records `none observed within scope` only for the stated permitted
   sources and two-week review period.
4. It does not say that no contrary evidence exists outside that boundary.

**Verification**: A reader can see both supporting evidence and contrary
evidence, plus the review's bounded limitation.

## Scenario 3 — Bounded tests label the result without overclaiming

**Given**: A completed Work Object predeclared the hypothesis that the
checklist would reduce incomplete handoffs for one team over two weeks, named
its signal, and has attributable results.
**When**: The skill attaches the test to the candidate.
**Then**:

1. It records the Work Object, hypothesis, scope, signal, attribution, and
   result as `supported`, `contradicted`, or `insufficient`.
2. It treats an unavailable signal or attribution as `insufficient`.
3. It states that a `supported` result is confidence within the completed
   boundary, not proof for every team or workflow.

**Verification**: The candidate's test record supports a scoped assessment and
does not manufacture a universal method.

## Scenario 4 — Promotion creates a separate Working Method

**Given**: The candidate has one completed, supported bounded test, a
documented contrary-evidence review, and the user explicitly accepts creating
version 1 of a separate Working Method for the same team and weekly-review
scope.
**When**: The skill reaches the promotion boundary.
**Then**:

1. It routes the exact promotion to the conductor with the candidate link,
   scope, evidence summary, contrary-evidence boundary, and version.
2. The conductor creates a separate Working Method rather than changing the
   candidate in place.
3. The candidate remains evidence-bearing, is marked promoted, and links to
   the new record.
4. The skill does not automatically apply, deploy, export, or broaden the
   Working Method.

**Verification**: Promotion is separate, linked, scoped, versioned, and based
on explicit human confirmation.

## Scenario 5 — Revision and retirement preserve history

**Given**: New attributable evidence shows that the checklist should exclude
handoffs requiring legal review, while a separate candidate is no longer useful.
**When**: The user authorizes the maintenance decision.
**Then**:

1. The material rule change creates a linked successor candidate using
   `supersedes`; the earlier identity and evidence remain intact.
2. The obsolete candidate is retired with a dated rationale and evidence link.
3. Neither record is deleted, rewritten, or silently converted into a Working
   Method.

**Verification**: Revision and retirement preserve an auditable lifecycle.

## Scenario 6 — Evidence Bridge is reference-only and approval-bound

**Given**: A user has supplied an approved Evidence Bridge reference with
provenance and sensitivity for this Work Object, while another candidate has no
such approval.
**When**: The skill records contextual evidence.
**Then**:

1. It records the approved Evidence Bridge reference without reading or
   copying Personal Institution source material.
2. It records the missing bridge as an uncertainty for the other candidate.
3. It continues only with permitted local evidence and does not scan personal
   archives, external systems, or production data.

**Verification**: The Evidence Bridge is minimum-necessary, attributable, and
never a backdoor to personal records.
