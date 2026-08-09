---
name: alawas-engineering-implement-bounded-change
description: "Use when a Work Object contains an accepted tracer bullet; implements and checks only that reversible path while preserving dirty work; stops for any material scope or authority deviation."
default_tier: medium
platform: codex
---
# Implement Bounded Change

## Governing principle

An accepted tracer bullet buys evidence through the smallest reversible change,
not by quietly becoming a broader feature. Implement only the recorded bounded
path, keep unrelated work intact, and make verification and deviations visible.

## Boundaries and non-goals

This skill does:

- Implement an accepted tracer bullet from its recorded design and constraints.
- Inspect the repository before changing it and preserve unrelated working-tree
  changes.
- Run focused verification before and during the change, then record the
  evidence that the bounded path was or was not verified.
- Record a durable deviation only after the required authority is present.
- Route blocked, failed, or degraded paths without claiming success.

This skill does not:

- Invent a tracer bullet, expand its scope, or replace a missing acceptance.
- Make a material product, architecture, data, security, privacy, or authority
  decision on the user's behalf.
- Discard, reset, overwrite, stage, commit, or otherwise alter unrelated
  working-tree changes.
- It does not deploy, release, export, or operate the change unless a
  separately accepted specialist and authority route explicitly authorizes it.

## Inputs and preconditions

**Required input:** an accessible Work Object containing an accepted tracer
bullet design, including its bounded path, authorization, failure behavior,
observability, non-goals, rollback, exit criteria, consequence, sensitivity,
and recorded user acceptance.

**Preconditions:** `alawas-governance-conduct-work-object` has established the Work Object and
the accepted design routes here. The implementation environment and repository
must be readable. If acceptance, scope, authority, or a necessary constraint is
missing, stop and route to the conductor; do not infer consent from the request
to implement.

## Required capabilities

The platform adapter classifies capabilities as native, manual-fallback, or
unsupported and follows `references/CAPABILITY-DEGRADATION.md` when needed.

- `file_read` — read the Work Object, repository instructions, and relevant code.
- `directory_list` — perform scoped repository inspection.
- `content_search` — find the accepted path and focused verification seam.
- `file_write` — apply only the bounded implementation change.
- `terminal_run` — inspect status and run focused verification where safe.
- `background_processes` — start a local server or service when focused
  verification requires it; without it, ask the user to start the service.
- `structured_output` — report scope, verification evidence, and deviations.
- `user_confirmation` — obtain authority for a material deviation when needed.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

**Authority gate:** Writing files outside `.work-studio/` and the accepted
bounded path requires explicit human confirmation. Destructive operations
(delete, reset, force-push) require explicit human confirmation at ALL
consequence levels. Before proceeding: (1) verify the Work Object's
consequence and sensitivity fields, (2) request confirmation naming the
action and scope, (3) record a structured authority History entry per the
authority recording contract in `references/CONSEQUENCE-AUTHORITY.md`.

- Recorded acceptance authorizes only the stated tracer-bullet implementation;
  it does not authorize a deviation, scope expansion, deployment, export, or
  unrelated cleanup.
- Before any write, compare the planned edit with the accepted bounded path.
  Stop for a material new decision or authority boundary.
- A deviation that changes the path, authorization, failure behavior,
  observability, non-goals, rollback, exit criteria, consequence, sensitivity,
  or touched data requires explicit user confirmation naming that deviation.
- For a high-consequence Work Object, explicit confirmation must name the
  proposed deviation-record mutation. Do not stage, annotate, change status,
  append History, or make any other mutation before that confirmation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Do not reopen an accepted implementation boundary merely because a different
solution looks attractive. An explicit grilling request runs the full
implementation profile against the accepted boundary. Otherwise, nominate a
Candidate Card only when a material new decision or authority boundary would
change the tracer bullet. First retrieve discoverable repository facts, then:

1. State the accepted constraint, new evidence, inference, and consequence.
2. Recommend one smallest safe route, including whether to stop, revert, or
   propose a scoped deviation.
3. Ask one decision-bearing question that names the exact deviation and required
   authority.
4. Enter the continuous session only after explicit acceptance; otherwise
   preserve the current boundary and route the unresolved question.

Do not use this loop to obtain blanket permission for nearby cleanup, future
implementation, deployment, or other unaccepted work.

## Skill Grilling Profile

Apply the `alawas-engineering-implement-bounded-change` profile and continuous Grilling Session in
`references/SKILL-AWARE-GRILLING.md`. Reconcile the accepted boundary with the
current repository, establish discriminating checks, protect unrelated dirty
work, and reopen the frontier for any unapproved interface, schema, dependency,
data, deployment, or external-effect expansion

## Stage workflow

### 1. Confirm the accepted boundary

Read the Work Object and extract the accepted tracer bullet verbatim enough to
check its path, constraints, authority, observability, rollback, and exit
criteria. Treat missing or ambiguous detail as a decision gap, not permission
to choose a convenient implementation. State the planned narrow change and
stop if it exceeds the record.

### 2. Inspect without disturbing the repository

Perform scoped repository inspection: read repository instructions, identify
the relevant code and focused test or verification seam, and inspect version
control status when available. Preserve unrelated working-tree changes exactly
as found. Never use destructive recovery commands or include unrelated files in
the implementation. If existing changes overlap the accepted path and their
ownership or intent cannot be determined safely, stop and ask the user how to
proceed.

### 3. Establish continuous verification

Run the narrowest relevant existing check before editing when practical. After
each meaningful edit, run the focused verification that exercises the accepted
path; run broader checks only when the accepted exit criteria require them.
Record command, result, and whether the evidence represents an executed check
or an unrun plan. A failed, unavailable, or inconclusive check is evidence of
an unverified path, never a passing result.

### 4. Implement the smallest path

Make the smallest reversible change that realizes the accepted tracer bullet.
Keep interfaces, dependencies, data access, and side effects within the
recorded authorization. Do not opportunistically refactor, harden for
production, migrate data, add integrations, or implement adjacent features.
Maintain the recorded rollback path as the change evolves.

### 5. Stop and record deviations honestly

When a material new decision or authority boundary appears, stop the affected
path. Describe the evidence, the exact proposed deviation, its consequence,
and the safe next route. After scoped user confirmation, pass a concise
deviation record to `alawas-governance-conduct-work-object` containing the original constraint,
changed constraint, reason, acceptance, verification impact, and revisit
trigger. If recording is unavailable, return that exact record and one concrete
manual instruction; do not claim it was recorded.

### 6. Verify and route

Compare the final change and verification evidence with the accepted exit
criteria. Route a verified bounded result to `alawas-governance-conduct-work-object` for durable
implementation evidence and the next specialist. Route a failed assumption to
the appropriate decision or investigation skill. Route a capability gap using
its declared degradation path. Do not claim deployment or release readiness.

## Evidence rules

- Label repository facts and command results as `[system]`, accepted constraints
  and confirmations as `[decision]`, and implementation reasoning as
  `[inference]`, following `references/EVIDENCE-MODEL.md`.
- Capture only minimum-necessary file names, commands, outcomes, and diffs;
  never copy secrets, restricted material, or full command output into the Work
  Object.
- Distinguish pre-existing working-tree changes from this skill's bounded edits.
- Treat a test result as evidence only when the command completed against the
  relevant change; a skipped or unavailable check remains an explicit gap.

## Work Object updates

This skill does not update a Work Object directly. On completion or an
authorized deviation, pass `alawas-governance-conduct-work-object` a concise record containing:

- accepted tracer-bullet identifier and implemented bounded path;
- repository inspection summary and preservation status for unrelated changes;
- changed files or artifacts, rollback status, and observed failure behavior;
- verification commands, results, gaps, and exit-criteria assessment;
- any authorized deviation, its reason, explicit acceptance, and revisit trigger;
- consequence, sensitivity, and recommended next route.

The conductor owns schema validation, optimistic concurrency, status changes,
and History. If it cannot record, report the exact record and manual step.

## Routing and termination

- **Verified within scope:** route to the conductor with implementation evidence;
  do not imply release or deployment.
- **Failed assumption or failed verification:** preserve the change state,
  report the evidence, and route to investigation or decision.
- **Material new decision or authority boundary:** stop the affected path and
  request scoped confirmation through the conductor.
- **Dirty overlap:** stop before modifying overlapping unrelated changes and ask
  the user for direction.
- **Capability gap:** use manual-fallback when it preserves the boundary, or
  stop as unsupported; state exactly what remains unverified.

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
## Bounded implementation

- **Work Object and accepted boundary:** <id, path, and authority>
- **Repository inspection:** <relevant seam and unrelated-change preservation>
- **Change:** <smallest implemented path and rollback status>
- **Verification:** <executed commands, outcomes, and explicit gaps>
- **Deviation status:** <none | awaiting authority | accepted and recorded>
- **Exit criteria:** <met | failed | unverified, with evidence>
- **Next route:** <conductor | investigation | decision | manual fallback>
```

## Anti-patterns

- Treating an accepted design as blanket authorization to improve nearby code.
- Starting implementation before inspecting repository instructions and status.
- Resetting, staging, committing, or cleaning unrelated working-tree changes.
- Calling unrun, skipped, or failing verification a pass.
- Continuing through a material new decision or authority boundary.
- Recording a deviation as though it were part of the original acceptance.
- Deploying or releasing because a bounded implementation verified locally.

## Final self-check

- Did I implement only the accepted tracer bullet and preserve its non-goals?
- Did repository inspection protect unrelated working-tree changes?
- Did continuous verification produce clear evidence rather than an assertion?
- Did I stop for every material new decision or authority boundary?
- Is each deviation explicitly accepted, durably recordable, and distinguishable
  from the original design?
- Did I avoid claiming deployment, release, or broader success?
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


### Runtime pin resolution

Codex can discover both user and repository skills with the same name.
Before applying this skill, search upward from the current directory for
`.work-studio/adapter.codex.lock`, stopping at the repository or filesystem
boundary. Read its `dest` value and
resolve `<dest>/<this-skill-name>/SKILL.md`. When that path differs from
the currently loaded copy, **load and follow the pinned copy** before
continuing. A matching legacy `adapter.lock` remains valid during migration.
If the pinned file is unavailable, report the broken pin and
stop instead of silently falling back to the global copy.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read_file` | native |
| `directory_list` | `list_dir` | native |
| `content_search` | `grep_search` | native |
| `file_write` | `create_file / replace_string_in_file` | native |
| `terminal_run` | `run_in_terminal` | native |
| `background_processes` | `run_in_terminal (background)` | native |
| `structured_output` | `—` | native |
| `user_confirmation` | `conversation turn` | native |
