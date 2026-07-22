---
name: alawas-diagnose-production-incident
description: "Use when production harm is active or suspected; contains harm, separates impact from mechanism, and verifies restoration; does not broaden emergency access or declare a cause without evidence."
platform: claude-code
---
# Diagnose Production Incident

## Governing principle

Protect people and the affected service before explaining the failure. Separate
containment, restoration, diagnosis, and prevention so observed evidence drives
each move; the workflow does not stack speculative fixes or call a plausible
cause confirmed.

## Boundaries and non-goals

This skill does:

- Stabilize an active Incident Work Object with the smallest authorized containment action, then restore the affected path when recovery evidence permits it.
- Preserve minimum-necessary sanitized evidence and keep facts, hypotheses, decisions, and gaps distinct.
- Rank hypotheses by impact, likelihood, reversibility, and available evidence, then test one at a time without changing unrelated variables.
- Verify recovery on the affected path, not merely on a health check or a dashboard aggregate.
- Create a linked, bounded Change Work Object only for a prevention action that needs future implementation authority.

This skill does not:

- Infer authority for production changes, destructive containment, customer contact, external escalation, or an expanded recovery action.
- Apply several changes simultaneously, conceal an unverified recovery, or turn a mitigation into a root-cause claim.
- Store secrets, customer content, tokens, unrestricted logs, or sensitive security detail in the Work Object.
- Implement preventive work, deploy a permanent fix, or close the Incident merely because the immediate symptom is absent.

## Inputs and preconditions

**Required input:** a readable Incident Work Object in `notice`, `frame`, or `observe`, with the reported affected path, consequence and sensitivity, known owner or escalation boundary, and current evidence or an explicit lack of it.

**Preconditions:** establish the current safety boundary before changing a live system: affected users or path, blast-radius limit, available containment and restoration runbook, authority owner, and verification signal. Missing or contradictory information is an explicit gap. Do not invent an incident commander, runbook, credential, dependency status, or recovery signal.

## Required capabilities

The platform adapter classifies capabilities as native, manual-fallback, or unsupported and follows `references/CAPABILITY-DEGRADATION.md` when needed.

- `file_read`, `directory_list`, and `content_search` — read the Incident, runbook, prior evidence, and bounded local diagnostics.
- `terminal_run` — execute only authorized containment, restoration, diagnostic, and affected-path verification commands from the runbook.
- `web_fetch` — retrieve a referenced status page, runbook, or dependency evidence at a known location when the authorized route permits it.
- `user_confirmation` — obtain scoped authority for a material production action, expanded blast radius, destructive recovery, external commitment, or Change Work Object mutation at high consequence.
- `structured_output` — return a sanitized incident record, ranked hypothesis ledger, recovery verification, dependency state, and recommended route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

**Authority gate:** Production changes, destructive containment, customer
contact, and external escalation require explicit human confirmation at ALL
consequence levels. Before proceeding: (1) verify the Incident Work Object's
consequence and sensitivity fields, (2) request confirmation naming the exact
action, target, duration, and blast-radius limit, (3) record a structured
authority History entry per the authority recording contract in
`references/CONSEQUENCE-AUTHORITY.md`.

- Read the Incident, current authority, and runbook together. When they conflict, stop at the safest reversible boundary and ask one scoped question.
- An explicitly authorized emergency containment action may be performed only within its stated target, duration, and blast-radius limit. A new or expanded action requires fresh authority.
- For high-consequence Work Objects, explicit confirmation must name the exact proposed action and Work Object mutation. Do not stage, annotate, change status, append History, or make any other mutation before that confirmation.
- An unavailable external dependency is not a diagnosis. Preserve the blocked condition, set the Incident to `waiting` only when that dependency or authority prevents the next safe action, and name its revisit trigger.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

An explicit grilling request runs the full incident profile without delaying
urgent containment. Otherwise, nominate a Candidate Card for an unrecorded
incident decision: state the observed symptom and evidence gap, consequence and
safe boundary; recommend the smallest reversible containment, recovery, or
diagnostic move; then wait for explicit entry before starting the continuous
session. Urgent, already-authorized containment remains governed by its
runbook, not by the Candidate Card.
Do not ask for blanket permission to make later fixes or declare recovery.

## Skill Grilling Profile

Apply the `alawas-diagnose-production-incident` profile and continuous Grilling
Session in `references/SKILL-AWARE-GRILLING.md`. Prioritize current harm and
reversible containment, maintain separate impact, mechanism, and communication
tracks, and ground causal claims in timeline plus mechanism evidence. On direct
entry, route through `alawas-conduct-work-object` first. Return the compact continuity
record; do not reset context, store a transcript, or mutate the Work Object.

## Stage workflow

### 1. Establish the incident boundary and sanitize intake

Read the Incident and runbook. Record the report as `[lived]`, `[system]`, or `[unresolved]`, including the affected path, time window, impact, consequence, known owners, and current dependency state. Replace secrets, tokens, customer identifiers, raw request bodies, and unrestricted logs with a minimum-necessary sanitized summary or stable reference.

### 2. Contain the immediate risk

Identify the smallest authorized, reversible containment action that reduces harm without hiding the signal needed for recovery. State its target, duration, expected effect, rollback, and verification. Perform it only when authority and the runbook permit it; otherwise stop and route the exact missing decision. Record containment separately from restoration and diagnosis.

### 3. Restore and verify the affected path

Use the runbook's authorized restoration action after containment is stable. Verify the actual affected path with its relevant user, request, job, or integration flow. A green generic health check, absence of new alerts, or a planned command is not recovery verification. If verification fails, return to containment or the next ranked hypothesis; do not layer an additional fix onto an unverified change.

### 4. Build and test ranked hypotheses

Create a ledger of plausible causes, each labelled `[inference]` with the supporting and contradicting evidence, expected observable result, lowest-risk test, and rollback. Rank hypotheses by immediate risk reduction, evidence, likelihood, reversibility, and test cost. Test one at a time, observe the specified result, and update the ledger before selecting another hypothesis. Do not stack speculative fixes, alter unrelated variables, or upgrade a hypothesis to a cause without discriminating evidence.

### 5. Handle blocked dependencies honestly

When a dependency, vendor, owner, credential, or required observation is unavailable, record it as `[unresolved]` with the affected decision, consequence, owner, and revisit trigger. Preserve any completed containment or recovery evidence. Set `status: waiting` only when the external dependency blocks the smallest safe next action; otherwise retain active investigation.

### 6. Route prevention as a bounded successor

After recovery is verified or the incident is safely bounded, distinguish confirmed contributing conditions from candidate prevention ideas. For each accepted prevention action that requires implementation, ask for the authority needed to create a separate linked Change Work Object. The successor must name one bounded outcome, owner, acceptance evidence, consequence, and relationship `responds_to` the Incident. Do not silently convert the Incident into Change work or create an unbounded remediation backlog.

## Evidence rules

- Label observations as `[system]` or `[lived]`, recorded authority as `[decision]`, hypotheses as `[inference]`, and unavailable information as `[unresolved]` according to `references/EVIDENCE-MODEL.md`.
- Sanitize evidence before persistence. Keep stable references, timestamps, path classes, metric deltas, command categories, and outcomes—not raw sensitive payloads or credentials.
- Distinguish containment performed, restoration attempted, recovery verified on the affected path, and root cause confirmed; none implies the next.
- Preserve disconfirming results and failed tests. A negative test narrows a hypothesis; it does not prove a different one.

## Work Object updates

This skill returns a concise record to `alawas-conduct-work-object`, which validates and persists it. Include the sanitized intake; authority and runbook reference; containment and restoration actions; affected-path verification; ranked hypothesis ledger and individual test outcomes; external dependency and revisit trigger; remaining risks; and one next action.

The conductor persists the appropriate durable transition:

- **Contained but not restored:** retain the Incident in its active state with containment evidence and the next restoration or authority action.
- **Recovery verified:** transition to `observe`, retain the verification evidence and observation window, and do not close the Incident.
- **Dependency blocked:** retain the current state, set `status` to `waiting`, record the external dependency and revisit trigger, and preserve completed evidence.
- **Prevention accepted:** create and link a separate Change Work Object with `responds_to`; retain the Incident's immutable type and evidence history.

Each update appends attributable History with the evidence summary, selected route, rationale, and next action. For high-consequence Incidents, the conductor requests the already-specified scoped confirmation before mutation.

## Routing and termination

- **Immediate risk uncontained:** stop at the safe boundary and route to the named authority or incident owner with the smallest containment decision.
- **Affected path restored and verified:** route to `alawas-conduct-work-object` for `observe` with a bounded monitoring window; do not claim closure.
- **Ranked diagnosis continues:** keep one active hypothesis test and route the updated ledger through the conductor.
- **External dependency blocked:** record the gap and route to `waiting` with a concrete revisit trigger.
- **Prevention accepted:** route the linked successor to `alawas-implement-bounded-change` only after its own acceptance and authority.
- **Manual-fallback capability:** pause with one concrete user-run runbook instruction and mark the related evidence unverified.
- **Unsupported capability:** stop the affected path, record the limitation, and route to a supported platform or the user.

## Output template

```markdown
## Production incident diagnosis

- **Incident boundary:** <id, affected path, impact, consequence, time window>
- **Evidence:** <sanitized [system], [lived], [decision], [unresolved] record>
- **Containment:** <authorized action, effect, rollback, or gap>
- **Restoration and verification:** <action and affected-path result>
- **Hypothesis ledger:** <ranked one-at-a-time tests and outcomes>
- **Dependency state:** <available | blocked, owner, revisit trigger>
- **Prevention:** <none | bounded linked Change Work Object>
- **Next route:** <contain | investigate | observe | waiting | change>
```

## Anti-patterns

- Applying multiple changes and calling the last one the root cause.
- Treating a generic health signal as verification of the affected path.
- Recording raw logs, secrets, customer content, or security-sensitive detail.
- Calling a blocked dependency evidence of a cause or a resolved incident.
- Turning prevention ideas into unbounded work or silently changing the Incident's type.
- Closing an Incident immediately after containment or one successful check.

## Final self-check

- Did I sanitize intake and state the affected path, authority, and safety boundary without inventing evidence?
- Did I separate containment, restoration, diagnosis, and prevention?
- Did I verify recovery on the affected path rather than a proxy signal?
- Did I rank hypotheses and test one at a time without stacking speculative fixes?
- Did I preserve external dependency gaps and use `waiting` only when blocked?
- Is any prevention work a bounded linked Change Work Object with its own authority, rather than a mutation of the Incident?
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `Read` | native |
| `directory_list` | `Bash ls` | native |
| `content_search` | `Grep` | native |
| `terminal_run` | `Bash` | native |
| `web_fetch` | `WebFetch / WebSearch` | native |
| `user_confirmation` | `conversation turn` | native |
| `structured_output` | `—` | native |
