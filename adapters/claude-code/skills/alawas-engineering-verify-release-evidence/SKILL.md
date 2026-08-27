---
name: alawas-engineering-verify-release-evidence
description: "Use when consequential implementation claims need direct verification; classifies evidence, gaps, blockers, and recovery credibility; does not deploy or promote local results as environment proof."
default_tier: medium
platform: claude-code
---
# Verify Release Evidence

## Governing principle

An implemented bounded change is not release-ready merely because its focused
test passed. Verify the intended user and operational story with evidence that
is proportionate to its consequence, and report what was not verified as
plainly as what was. The evidence report informs the next authority holder; it
never substitutes for release authority.

## Boundaries and non-goals

This skill does:

- Verify the recorded acceptance criteria for an implemented bounded change.
- Exercise relevant failure and recovery behavior, including retries or
  duplicate handling when the bounded path can receive them.
- Check the declared privacy and security boundaries without collecting more
  sensitive data than the check requires.
- Report degraded dependencies, unavailable checks, and other evidence gaps.
- Produce a concise, provenance-labelled evidence record for the conductor.

This skill does not:

- Implement, alter scope, deploy, release, publish, or operate the change.
- Invent passing evidence, infer release approval, or hide an unverified path.
- Expand access to production data, secrets, external systems, or personal
  records just to make a verification claim.

## Inputs and preconditions

**Required input:** a readable Work Object containing the accepted bounded
change, its implementation evidence, acceptance criteria, consequence,
sensitivity, failure and recovery expectations, privacy and security
boundaries, and exit criteria.

**Preconditions:** `alawas-engineering-implement-bounded-change` has completed or honestly routed
its bounded path. The repository and the named verification seam are readable.
If acceptance criteria, implementation identity, consequence, or a necessary
boundary is missing, stop and route to `alawas-governance-conduct-work-object`; do not select a
convenient substitute.

## Required capabilities

The platform adapter classifies capabilities as native, manual-fallback, or
unsupported and follows `references/CAPABILITY-DEGRADATION.md` when needed.

- `file_read` — read the Work Object, implementation evidence, and check setup.
- `directory_list` and `content_search` — locate the declared verification seam.
- `terminal_run` — run focused checks and inspect their completed results.
- `background_processes` — start and manage a local server or service for
  verification; without it, ask the user to start the service.
- `artifact_rendering` — render a visual artifact for human verification of the
  user story; without it, ask the user to open the relevant page.
- `structured_output` — report evidence, gaps, and the next route.
- `user_confirmation` — obtain scoped authority before a check crosses a new
  privacy, security, production, or other material boundary.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

**Authority gate:** Verification steps that access production, secrets, or
external systems require explicit human confirmation at ALL consequence
levels. Before proceeding: (1) verify the Work Object's consequence and
sensitivity fields, (2) request confirmation naming the verification step
and the boundary it crosses, (3) record a structured authority History entry
per the authority recording contract in `references/CONSEQUENCE-AUTHORITY.md`.

- Evidence must be proportionate: low-consequence changes need direct evidence
  for the accepted path and its material failure behavior; meaningful or high-
  consequence changes additionally require the relevant recovery, dependency,
  privacy, and security boundaries to be exercised or named as gaps.
- Existing implementation authority does not authorize production access,
  secrets access, external writes, deployment, or release verification.
- Stop before a verification step that would broaden data sensitivity or
  authority. State the exact missing evidence and route for explicit approval.
- For a high-consequence Work Object, explicit confirmation must name the
  proposed evidence-record mutation. Do not stage, annotate, change status,
  append History, or make any other mutation before that confirmation.
- A failed, unavailable, skipped, or inconclusive check is an evidence gap,
  never a passing or release-ready result.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

An explicit grilling request runs the full verification profile. Otherwise,
nominate a Candidate Card when the recorded evidence plan is insufficient and
the smallest useful check would cross a material authority or boundary change.

1. State the accepted criterion, available evidence, missing evidence, and
   consequence.
2. Recommend one smallest safe verification route or a stop.
3. Ask one decision-bearing question naming the new authority or boundary.
4. Enter the continuous session only after explicit acceptance; otherwise
   report the gap and preserve the current safe boundary.

Do not reopen a bounded implementation merely to improve it while verifying.

## Skill Grilling Profile

Apply the `alawas-engineering-verify-release-evidence` profile and continuous Grilling Session in
`references/SKILL-AWARE-GRILLING.md`. Start with the consequential claim having
the weakest direct evidence, validate checks and negative cases independently,
and expose environment, recovery, privacy, and downstream gaps. On direct
entry, route through `alawas-governance-conduct-work-object` first. Return the compact continuity
record; do not reset context, store a transcript, or mutate the Work Object.

## Stage workflow

### 1. Establish the evidence contract

Read the Work Object and implementation record. List each acceptance criterion,
its intended user or operational observation, consequence, sensitivity,
failure and recovery expectation, dependency assumption, and privacy or
security boundary. Separate executed system evidence from plans and inference.

### 2. Select the smallest proportionate checks

Use the focused verification seam already named by the bounded change when it
can evidence the criterion. Add only checks that cover a material omitted
acceptance, failure/recovery behavior, dependency degradation, or boundary.
For retries or duplicate handling, test only when the accepted path can retry,
receive duplicate delivery, or otherwise repeat side effects; otherwise state
that it is not applicable and why.

### 3. Verify the accepted and operational paths

Run the smallest safe checks. Confirm the success path against its acceptance
criteria, then exercise relevant invalid input, dependency degradation, and
recovery behavior. Record command, observed result, and whether the evidence
was executed. Do not turn a timeout, mocked dependency, or skipped step into a
claim about a live dependency.

### 4. Check privacy and security boundaries

Verify only the boundary declared by the Work Object: for example, that a
failure response does not expose a secret, a test fixture uses isolated data,
or an unauthorized operation remains blocked. Redact sensitive values from the
report. If the check requires broader access, stop before requesting or using
it and report the gap.

### 5. Assess recovery and evidence gaps

For every failed or unavailable check, say whether recovery was exercised,
whether the system remained safe, and what remains unknown. A degraded
dependency may establish graceful handling but cannot establish the dependency's
healthy production behavior. Do not claim release readiness from partial
evidence.

### 6. Report and route

Compare the completed evidence with the exit criteria. Route verified evidence,
failed assumptions, and explicit gaps through `alawas-governance-conduct-work-object`. State
that this skill does not deploy or release; a separate authorized specialist
decides whether any later release action is appropriate.

## Evidence rules

- Apply `capabilities/classify-provenance.md` (reduced 3-tag variant): commands,
  tests, logs, and repository facts as `[system]`; accepted criteria and
  confirmations as `[decision]`; conclusions as `[inference]`.
- Capture minimum-necessary commands, result summaries, affected boundaries,
  and redacted artifacts. Never copy secrets or private records into the
  evidence report.
- Use exact status words: `verified`, `failed`, `unverified`, `not applicable`,
  or `manual-fallback`. Never use `release-ready` as a verification result.
- Distinguish a recovery observation from a plan to recover and a simulated
  degraded dependency from an observed live outage.

## Work Object updates

This skill does not mutate a Work Object directly. Pass `alawas-governance-conduct-work-object`
a concise record containing:

- accepted criteria, consequence, sensitivity, and verification seam;
- executed commands or observations and their results;
- failure, recovery, retry or duplicate-handling, and dependency evidence;
- privacy and security boundaries checked, with sensitive content redacted;
- every evidence gap, its consequence, and the next safe action;
- an exit-criteria assessment that makes no deployment or release claim.

The conductor owns validation, History, and status transitions. If recording is
unavailable, return the same record and one concrete manual instruction.

## Routing and termination

- **Evidence sufficient within scope:** route the evidence report to the
  conductor; do not claim deployment or release.
- **Failed acceptance or recovery:** route to investigation or decision with
  the executed evidence and preserve the bounded implementation boundary.
- **Missing evidence or degraded dependency:** report `unverified` or
  `manual-fallback`, state the exact gap, and route to the smallest safe check.
- **New authority, privacy, or security boundary:** stop and request scoped
  confirmation through the conductor.
- **Unsupported capability:** stop the affected verification path and name the
  platform limitation; do not silently substitute a weaker check.

## Output template

Apply `references/DIRECTOR-LANGUAGE.md` to everything said to the
director. Lead with plain meaning; attach the technical term to the explanation
rather than substituting it. Order anything worth explaining as: what's
happening, why it matters, the technical term, the evidence, the
recommendation, what needs deciding. Short answers stay short, and any part may
be marked absent — "Evidence: none, this is inference" is valid and preferred.
Never fill a part to complete the shape. Never phrase a decision in terms the
director must decode before choosing. Record content is never translated:
field names, state names, record IDs, and file paths stay exact.

```markdown
## Release-evidence verification

- **Work Object and consequence:** <id, accepted path, consequence, sensitivity>
- **Acceptance evidence:** <criterion, executed observation, status>
- **Operational evidence:** <failure, recovery, retries/duplicates, dependency>
- **Privacy and security:** <checked boundary and redacted result>
- **Evidence gaps:** <unverified or not-applicable item and consequence>
- **Exit criteria:** <met | failed | unverified, without release claim>
- **Next route:** <conductor | investigation | decision | manual fallback>
```

## Anti-patterns

- Treating a green unit test as proof of the full user and operational story.
- Exercising production data, secrets, or external writes without authority.
- Calling a mocked or degraded dependency healthy.
- Ignoring recovery, retries, or duplicate handling when repetition is relevant.
- Hiding a missing privacy or security check behind a general success claim.
- Saying a change is deployed, released, or release-ready from this report.

## Final self-check

- Did I verify each accepted criterion with proportionate executed evidence?
- Did I cover relevant failure and recovery, degraded dependencies, and retries
  or duplicates without claiming behavior I did not observe?
- Did I keep privacy and security checks within their declared boundaries?
- Are all missing, unavailable, and simulated checks stated as evidence gaps?
- Did I avoid deployment and release claims and route the evidence honestly?
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Epistemic rules

This skill uses the **essential 3‑tag system** (`references/epistemic/epistemic-rules-essential.md`).

The epistemic tier is resolved from the skill's `default_tier` (medium).
**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the epistemic tier is upgraded to at least `medium` (essential 3‑tag).
When `consequence: high`, the epistemic tier is upgraded to the strongest
available tier (full 6‑tag).
`actual_epistemic_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

For a high-consequence Work Object, confirmation must name the exact
proposed mutation. Do not stage, annotate, change status, append History,
or make any other mutation before receiving that scoped confirmation.

### Model tier

This skill declares `default_tier: medium`.
The platform overlay resolves this to `claude-sonnet-4-20250514`.
The prompt budget for this tier is approximately 40000 tokens (advisory).

**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the effective tier is upgraded to at least `medium`. When `consequence: high`,
the effective tier is upgraded to the strongest available model.
`actual_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `Read` | native |
| `directory_list` | `Bash ls` | native |
| `content_search` | `Grep` | native |
| `terminal_run` | `Bash` | native |
| `background_processes` | `Bash (background) / Monitor` | native |
| `artifact_rendering` | `Artifact` | native |
| `structured_output` | `—` | native |
| `user_confirmation` | `conversation turn` | native |
