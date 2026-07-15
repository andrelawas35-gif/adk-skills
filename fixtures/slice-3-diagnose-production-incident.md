# Slice 3 Behavioral Fixture — Diagnose Production Incident

This fixture proves the observable incident path: safe intake, containment,
restoration, one-at-a-time diagnosis, affected-path verification, honest
dependency handling, and bounded prevention work. It does not permit a
speculative remediation stack or a closure claim.

## Scenario 1 — Evidence-safe intake establishes a containment boundary

**Given**: An Incident report identifies failed checkout requests and includes a token, customer identifiers, and raw request content; the approved runbook names a reversible traffic-shedding action.
**When**: The skill begins incident intake.
**Then**:

1. It records the affected path, impact, time window, and available authority as sanitized evidence, excluding the token, customer identifiers, and raw request content.
2. It distinguishes the reported symptom from the proposed containment action and from any possible cause.
3. It performs only the authorized reversible containment action or reports the exact authority gap.
4. It records the containment outcome and rollback boundary without calling the incident restored or diagnosed.

**Verification**: The evidence ledger contains minimum-necessary sanitized evidence and a clear containment boundary.

## Scenario 2 — Restoration is verified on the affected path

**Given**: Containment has reduced impact and the runbook permits a bounded restoration action; a generic service health endpoint is green.
**When**: The skill restores service.
**Then**:

1. It records restoration separately from containment.
2. It verifies the original affected checkout path with the runbook's relevant request or integration flow, rather than relying only on the health endpoint.
3. If the affected path fails, it does not report recovery or add another speculative fix without returning to the ranked diagnostic process.
4. If the affected path passes, it routes to `observe` with a bounded observation window and does not claim closure.

**Verification**: Recovery verification names the affected path and its observed result, not a proxy signal.

## Scenario 3 — Ranked hypothesis testing stays one at a time

**Given**: The Incident has two plausible causes: a recent configuration change and a third-party timeout. Each has supporting and contradicting evidence plus a reversible diagnostic test.
**When**: The skill investigates the cause.
**Then**:

1. It records a ranked hypothesis ledger with expected observations and test boundaries.
2. It tests the highest-ranked hypothesis one at a time and records its result before selecting the next test.
3. It does not combine the configuration rollback with a timeout increase or call either hypothesis confirmed without discriminating evidence.
4. It preserves failed or disconfirming tests as evidence.

**Verification**: A reader can reconstruct the ranked hypothesis order and see that changes were not stacked.

## Scenario 4 — A blocked external dependency remains explicit

**Given**: Restoration is incomplete because a payment provider is unavailable and no authorized local workaround exists.
**When**: The skill reaches the dependency boundary.
**Then**:

1. It records the external dependency, affected decision, owner, consequence, and revisit trigger as an unresolved gap.
2. It preserves completed containment and restoration evidence without claiming the affected path is recovered.
3. It sets the Incident to `waiting` only because the external dependency blocks the smallest safe next action.
4. It does not treat the provider outage as proof of root cause or invent an escalation result.

**Verification**: The Work Object's `waiting` status names the external dependency and concrete revisit trigger.

## Scenario 5 — Prevention becomes a linked bounded Change Work Object

**Given**: A verified recovery identifies an accepted prevention action: "add a bounded payment-provider timeout alert with an acceptance check."
**When**: The incident owner authorizes follow-up prevention work.
**Then**:

1. The Incident retains its type and evidence history.
2. The conductor creates a linked follow-up Change Work Object with `responds_to`, one bounded outcome, owner, acceptance evidence, and its own authority boundary.
3. It does not implement or deploy the prevention action as part of diagnosis.
4. It routes the Change Work Object to `implement-bounded-change` only after the new Work Object is accepted.

**Verification**: The prevention action is a linked follow-up Change Work Object, not an unbounded remediation list or a mutation of the Incident.
