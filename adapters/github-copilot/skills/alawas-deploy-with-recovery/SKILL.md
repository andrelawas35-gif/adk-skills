---
name: alawas-deploy-with-recovery
description: "Use when a verified change has explicit deployment authority; ships the smallest observable increment with rollback and stop gates; never expands without positive evidence."
platform: github-copilot
---
# Deploy With Recovery

## Governing principle

Deployment is a bounded production change, not the conclusion of the work.
Release only the verified path authorized for this Work Object, in recoverable
increments, and let observed production reality determine the next route.

## Boundaries and non-goals

This skill does:

- Deploy a verified Work Object only after its explicit deployment authority,
  platform runbook, and required gates are present.
- Confirm readiness, access, migration, budget, rollback, and incremental
  release boundaries before changing production.
- Execute only the approved incremental deployment, verify each increment, and
  invoke the recorded rollback when verification fails.
- Record sanitized production evidence and route the Work Object to `observe`.

This skill does not:

- It does not claim closure from an incremental deployment or its immediate
  post-deployment checks.
- Infer deployment authority from implementation, verification, or a general
  request to ship.
- Invent a runbook, credentials, readiness signal, migration plan, budget, or
  rollback action.
- Expand a rollout, migrate unrelated data, make a new external commitment, or
  use broader production access than the recorded authority permits.
- Claim closure, sustained success, or a healthy production outcome before the
  observed-outcome specialist has assessed it.

## Inputs and preconditions

**Required input:** a readable Work Object in `release` with verified release
evidence and an explicit deployment authority that names the target, bounded
increment, permitted access, rollback owner or action, and post-deployment
observation window.

**Preconditions:** load the applicable platform runbook before any production
action. The Work Object must also contain the verified scope and artifact,
readiness criteria, access boundary, migration status or an explicit
not-applicable decision, budget or capacity guardrail, rollback trigger and
procedure, and post-deployment reality checks. Missing, stale, ambiguous, or
failed information is a stop condition, not a prompt to fill gaps by inference.

## Required capabilities

The platform adapter classifies capabilities as native, manual-fallback, or
unsupported and follows `references/CAPABILITY-DEGRADATION.md` when needed.

- `file_read`, `directory_list`, and `content_search` — read the Work Object,
  platform runbook, verified evidence, and local deployment artifacts.
- `terminal_run` — execute only the runbook-approved incremental deployment,
  verification, and rollback commands.
- `web_fetch` — retrieve a referenced platform runbook or status page at a
  known location when the authorized route permits it.
- `user_confirmation` — obtain explicit deployment authority or authority for
  a material deviation, rollback mutation, or external commitment.
- `structured_output` — return sanitized deployment evidence, gate status,
  recovery status, and the Observe route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Deployment requires explicit deployment authority for every target and
  increment; prior verification does not authorize production access.
- Read the authority and platform runbook together before acting. If their
  target, increment, access boundary, migration, budget, rollback, or reality
  checks conflict, stop and request one scoped decision.
- For high-consequence Work Objects, explicit confirmation must name the exact
  deployment action and the proposed Work Object mutation. Do not stage,
  annotate, change status, append History, or make any other mutation before
  that confirmation.
- A rollback specified in the accepted authority is a recovery action within
  that authority. A new rollback path, expanded blast radius, or destructive
  recovery requires fresh explicit confirmation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

An explicit grilling request runs the full deployment profile. Otherwise,
nominate a Candidate Card only for a material deployment decision that is not
already recorded. First state the gate, observed evidence, consequence, and
safe route. Recommend one smallest recoverable increment or a hold, then ask
one decision-bearing question naming the exact missing or changed authority.
Do not use this loop to obtain blanket permission for later increments,
unrelated migration, or closure.

## Skill Grilling Profile

Apply the `alawas-deploy-with-recovery` profile and continuous Grilling Session in
`references/SKILL-AWARE-GRILLING.md`. Prove artifact equivalence, challenge
target health and recovery readiness, and make each increment's observation
and stop conditions explicit before external action

## Stage workflow

### 1. Load the release boundary and platform runbook

Read the Work Object, verified evidence, explicit deployment authority, and
platform runbook. Extract the target, artifact identity, authorized increment,
access scope, readiness checks, migration status, budget guardrail, rollback
trigger and procedure, and post-deployment reality checks. Stop if a required
input is unavailable or conflicts with the approved boundary.

### 2. Confirm gates before production change

Confirm, with current evidence, that the authorized actor has the minimum
access; the target is ready; the migration is complete, reversible, or
explicitly not applicable; and the budget or capacity guardrail permits this
increment. Confirm that rollback is executable by the named owner or command.
Do not deploy when any gate is missing, stale, failed, or unverifiable.

### 3. Release one authorized increment

Execute only the smallest authorized incremental deployment from the platform
runbook. Capture the artifact identity, target, increment, command category,
timestamp, and observed result without recording secrets, tokens, customer
data, raw request bodies, or unrestricted logs. Do not proceed to a later
increment until the current increment's required verification is observed.

### 4. Verify and recover

Run the runbook's post-deployment reality checks for the current increment.
If a required check fails or indicates unsafe behavior, stop further rollout,
execute the recorded rollback when authorized and feasible, then verify the
rollback result. Record failed verification and recovery honestly; a planned,
unavailable, or failed rollback is an explicit gap, never a successful release.

### 5. Sanitize and persist evidence

Label deployment facts and command outcomes as `[system]`, authority as
`[decision]`, and interpretations as `[inference]`. Record only minimum-
necessary sanitized production evidence: artifact identity, target class,
increment, gate outcomes, check results, rollback status, remaining risks, and
the observation window. Redact credentials, secrets, personally identifiable
information, customer content, and security-sensitive implementation detail.

### 6. Route to Observe

Pass the conductor a concise deployment record. On a completed authorized
increment, transition to `observe` with a concrete outcome-review action and
window; do not claim closure. On a missing gate, failed verification, or
incomplete rollback, preserve the evidence and route to the conductor,
investigation, or decision path named by the runbook.

## Evidence rules

- Treat readiness, access, migration, budget, rollback, deployment, and
  post-deployment reality checks as distinct observed facts; do not turn a plan
  into evidence.
- Sanitize all production evidence before it enters the Work Object. Record a
  stable reference or summary instead of sensitive values or raw logs.
- Distinguish a successful increment from a complete rollout, and a rollback
  attempt from a verified rollback result.
- State every missing or unavailable check, including its consequence and the
  smallest safe next action.

## Work Object updates

This skill returns a concise record to `alawas-conduct-work-object`, which validates
and persists it. Include:

- the explicit deployment authority, platform runbook reference, target,
  authorized increment, and artifact identity;
- readiness, access, migration, budget, and rollback gate outcomes;
- sanitized deployment and post-deployment reality-check evidence;
- failed verification, rollback execution and verification, and remaining gaps;
- the observation window, next action, and recommended route.

For a successful authorized increment, the conductor records the release
evidence, transitions the Work Object to `observe`, and sets `next_action` to
the bounded outcome review. It does not close the Work Object. For failure or a
missing gate, the conductor retains the evidence and routes without claiming a
successful deployment.

## Routing and termination

- **Increment verified:** route to `alawas-conduct-work-object` for `observe` with
  the bounded outcome-review window; do not claim closure.
- **Missing readiness, access, migration, budget, or rollback gate:** stop and
  route to the conductor with the exact missing condition.
- **Failed verification:** stop rollout, use the recorded rollback if
  authorized, and route the observed result to investigation or decision.
- **Manual-fallback capability:** pause with one concrete user-run runbook
  instruction and mark the affected deployment evidence unverified.
- **Unsupported capability:** stop the affected deployment path, record the
  limitation, and route to a supported platform or the user.

## Output template

```markdown
## Deployment with recovery

- **Authority and runbook:** <explicit authority, runbook reference, target, increment>
- **Gates:** <readiness, access, migration, budget, rollback outcomes>
- **Increment:** <artifact identity, target class, observed result>
- **Reality checks:** <sanitized post-deployment observations and gaps>
- **Recovery:** <not needed | rollback executed and verified | rollback gap>
- **Evidence:** <sanitized [system], [decision], and [inference] record>
- **Next route:** <observe | conductor | investigation | decision | manual fallback>
```

## Anti-patterns

- Treating verification evidence as deployment authority.
- Deploying before loading a platform runbook or confirming rollback.
- Rolling out beyond the authorized increment because the first increment
  appeared healthy.
- Calling a planned, unavailable, or failed check a successful deployment.
- Storing secrets, customer data, or raw production logs as Work Object evidence.
- Claiming closure from deployment instead of routing to Observe.

## Final self-check

- Is explicit deployment authority present for this target and increment?
- Did I load the platform runbook and confirm readiness, access, migration,
  budget, rollback, and post-deployment reality checks?
- Did I release only one authorized increment and stop on failed verification?
- Is all recorded production evidence sanitized and provenance-labelled?
- Did I route to `observe` without claiming closure or sustained success?
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read_file` | native |
| `directory_list` | `list_dir` | native |
| `content_search` | `grep_search` | native |
| `terminal_run` | `run_in_terminal` | native |
| `web_fetch` | `open_browser_page / mcp tools` | native |
| `user_confirmation` | `conversation turn` | native |
| `structured_output` | `—` | native |
