# Slice 4 Behavioral Fixture — Review Outcome and Adapt

This fixture proves a proportionate outcome-review path. It compares the
recorded hypothesis with lived and system outcomes, keeps shipped output
separate from observed value, and routes a user-chosen next direction without
silently changing the reviewed Work Object.

## Scenario 1 — Confirmed outcome distinguishes delivery from value

**Given**: An `observe` Work Object hypothesizes that a released checklist will
reduce incomplete handoffs. The checklist was shipped, system records show fewer
incomplete handoffs, and a user reports the handoff is easier to complete.
**When**: The skill reviews the outcome.
**Then**:

1. It records the shipped checklist separately from the system and lived
   outcomes.
2. It labels the outcome observations as evidence and the supported conclusion
   as an inference.
3. It assesses the hypothesis as confirmed only within the observed limits.
4. It recommends one bounded next direction before asking the user to choose.

**Verification**: A reader can distinguish the delivered output from observed
value and see the evidence supporting the confirmed assessment.

## Scenario 2 — Contradicted hypothesis remains attributable

**Given**: An `observe` Work Object hypothesizes that a new reminder reduces
missed approvals. The reminder was shipped, but system records show missed
approvals did not decline and lived feedback identifies an approval-boundary
confusion.
**When**: The skill reviews the outcome.
**Then**:

1. It preserves the original hypothesis and the contradictory system and lived
   evidence.
2. It does not call shipping the reminder observed value or silently rewrite
   the hypothesis.
3. It labels the explanation for the contradiction as an inference.
4. It recommends one bounded repair, deeper inquiry, or stop direction before
   asking the user to choose.

**Verification**: Contradictory evidence changes the route, not the history.

## Scenario 3 — Insufficient observation is an explicit result

**Given**: A Work Object has shipped its output, but no outcome observation was
collected and the hypothesis cannot be found in its durable record.
**When**: The skill reaches the review boundary.
**Then**:

1. It assesses the result as `insufficient observation`.
2. It records the missing hypothesis and outcome evidence as unresolved gaps.
3. It names the affected decision and one concrete revisit trigger.
4. It does not claim confirmation, contradiction, observed value, completion,
   or closure.

**Verification**: The outcome review is explicit about what remains unverified.

## Scenario 4 — Successor creation preserves type and authority

**Given**: A user reviews a contradicted outcome, selects `create successor`,
and explicitly authorizes one bounded repair: “clarify the approval boundary in
the reminder flow.”
**When**: The review reaches successor creation.
**Then**:

1. The reviewed Work Object retains its immutable type and evidence history.
2. The conductor creates a separate linked `change` Work Object with one
   bounded outcome, consequence, sensitivity, owner, acceptance evidence, and
   relationship to the reviewed Work Object.
3. The review does not implement the repair or create additional work.
4. The linked Change Work Object routes to `implement-bounded-change` only
   after its own accepted tracer bullet and authority boundary exist.

**Verification**: The successor is correctly typed, linked, bounded, and
independently authorized; the original Work Object is not mutated into Change
work.
