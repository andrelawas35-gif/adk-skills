# Slice 2 Behavioral Fixture - Verify Release Evidence

This fixture proves the observable evidence-verification path after an
implemented bounded change. It tests proportionate acceptance and operational
evidence, including gaps and safe recovery behavior; it does not deploy or
release the change.

## Scenario 1 - Successful verification is proportionate

**Given**: A low-consequence accepted bounded change has a focused test seam,
a defined user outcome, and malformed input as its material failure path.
**When**: The skill verifies the change.
**Then**:

1. It maps the acceptance criterion to an executed successful verification at
   the focused seam.
2. It exercises the relevant malformed-input failure and records the safe
   result or recovery observation.
3. It reports commands and outcomes as system evidence, distinct from plans.
4. It routes the evidence without saying the change is deployed or released.

**Verification**: The report distinguishes successful verification from an
unrun plan and assesses only the recorded exit criteria.

## Scenario 2 - Missing evidence remains explicit

**Given**: A meaningful-consequence change has acceptance evidence but no
executed verification of its declared security boundary.
**When**: The skill assembles the evidence report.
**Then**:

1. It records the accepted path as verified only to the extent observed.
2. It labels the unexecuted security check as missing evidence and states its
   consequence.
3. It does not use broader credentials or production data to fill the gap
   without explicit authority.
4. It routes the missing evidence to the conductor or the smallest safe check.

**Verification**: The exit criteria are unverified, not a release claim.

## Scenario 3 - Degraded dependency and recovery are honest

**Given**: The bounded path depends on a service that can time out, while its
accepted behavior is a safe response and a documented recovery route.
**When**: The dependency is degraded during verification.
**Then**:

1. The skill records a degraded dependency rather than a healthy service.
2. It verifies the safe failure response and any executed recovery behavior.
3. It names healthy dependency behavior as unverified unless it was observed.
4. It does not deploy or release from partial dependency evidence.

**Verification**: A reader can tell the difference between graceful degradation,
recovery evidence, and an unavailable dependency check.

## Scenario 4 - Retries, duplicates, privacy, and security stay bounded

**Given**: An accepted path may retry after a timeout and receive a duplicate
request, and it must not expose a secret in its failure response.
**When**: The skill runs its focused verification.
**Then**:

1. It verifies retry or duplicate handling where repeated delivery is relevant,
   or marks it not applicable with a reason.
2. It checks the declared privacy and security boundary using isolated data and
   redacts sensitive values from the report.
3. It stops before a check that would require production secrets or broader
   authority.
4. It reports any unrun boundary check as an evidence gap, never as a supported
   release claim.

**Verification**: The report identifies the repeated-operation outcome, the
privacy or security observation, and every remaining gap.
