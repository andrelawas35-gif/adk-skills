# Slice 3 Behavioral Fixture — Deploy With Recovery

This fixture proves the observable deployment path after a verified Work
Object. It permits only an explicitly authorized incremental deployment with a
loaded platform runbook, bounded production evidence, recovery, and an Observe
route; it does not claim closure.

## Scenario 1 — Successful incremental deployment moves to Observe

**Given**: A verified release Work Object has explicit deployment authority for
one canary increment, a loaded platform runbook, confirmed readiness and
minimum access, a reversible migration, budget headroom, a tested rollback,
and named post-deployment reality checks.
**When**: The skill performs the authorized increment.
**Then**:

1. It deploys only the stated canary increment and records the artifact and
   target class as sanitized evidence.
2. It confirms the runbook's post-deployment reality checks before any later
   increment is considered.
3. It records the observed check outcomes and observation window with no
   secrets, customer data, or raw production logs.
4. It routes the Work Object to `observe` with a concrete next action and does
   not claim closure.

**Verification**: The record distinguishes a successful incremental deployment
from complete rollout or sustained production success.

## Scenario 2 — Missing readiness stops before production change

**Given**: Deployment authority and a runbook exist, but the required
readiness condition is stale or unavailable.
**When**: The skill evaluates the release gates.
**Then**:

1. It stops before changing production.
2. It records the missing readiness condition, its consequence, and the
   smallest safe next action.
3. It does not substitute a guessed signal, broader access, or a deployment
   claim for the missing evidence.
4. It routes the gap through the conductor or one scoped authority decision.

**Verification**: No deployment is reported and the readiness gap remains
explicit.

## Scenario 3 — Failed verification invokes rollback

**Given**: A first authorized increment is deployed, but a required
post-deployment reality check shows unsafe behavior and the approved runbook
contains a rollback procedure.
**When**: Verification fails.
**Then**:

1. It stops further rollout immediately.
2. It executes the authorized rollback and verifies the rollback result when
   the required capability is available.
3. It records failed verification, rollback evidence, and every remaining gap
   without calling the release successful.
4. It routes the result to investigation or decision rather than `observe`
   when recovery is incomplete.

**Verification**: A reader can distinguish failed verification, a rollback
attempt, and a verified rollback.

## Scenario 4 — Sanitization and platform degradation remain honest

**Given**: The deployment result includes a token and customer identifiers, and
one platform exposes runbook execution only as manual-fallback while another
marks it unsupported.
**When**: The skill prepares evidence or reaches the deployment action.
**Then**:

1. It records only sanitized evidence and redacts the token, customer
   identifiers, raw logs, and sensitive request content.
2. With manual-fallback, it pauses with one concrete user-run runbook command
   and marks deployment verification unverified until an observed result is
   supplied.
3. With unsupported capability, it stops the affected path and routes to a
   supported platform or the user.
4. It does not claim closure, a completed deployment, or healthy production
   behavior from either degraded path.

**Verification**: The Work Object contains bounded sanitized evidence or an
explicit gap, never secret-bearing production output.
