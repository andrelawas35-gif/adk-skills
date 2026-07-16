---
name: implement-bounded-change
description: "implement-bounded-change — Claude Code adapter"
platform: claude-code
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

**Preconditions:** `conduct-work-object` has established the Work Object and
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
- `structured_output` — report scope, verification evidence, and deviations.
- `user_confirmation` — obtain authority for a material deviation when needed.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

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

## Agreement Loop behavior

Apply the shared conversational inquiry contract in
`references/AGREEMENT-LOOP.md`: give a recommendation before one question,
maintain coverage of material branches, and continue without an arbitrary
question cap until the user and evidence establish the next safe move.

Do not reopen an accepted implementation boundary merely because a different
solution looks attractive. Activate the Agreement Loop only when a material new
decision or authority boundary would change the accepted tracer bullet. First
retrieve discoverable repository facts, then:

1. State the accepted constraint, new evidence, inference, and consequence.
2. Recommend one smallest safe route, including whether to stop, revert, or
   propose a scoped deviation.
3. Ask one decision-bearing question that names the exact deviation and required
   authority.
4. Continue only after the response explicitly accepts that deviation; otherwise
   preserve the current boundary and route the unresolved question.

Do not use this loop to obtain blanket permission for nearby cleanup, future
implementation, deployment, or other unaccepted work.

## Skill-aware grilling lens

Apply the `implement-bounded-change` lens in
`references/SKILL-AWARE-GRILLING.md`. On direct entry, route through
`conduct-work-object` first. Return the standard five-field Grilling handoff
for conductor persistence; do not store a transcript or mutate the Work Object.

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
deviation record to `conduct-work-object` containing the original constraint,
changed constraint, reason, acceptance, verification impact, and revisit
trigger. If recording is unavailable, return that exact record and one concrete
manual instruction; do not claim it was recorded.

### 6. Verify and route

Compare the final change and verification evidence with the accepted exit
criteria. Route a verified bounded result to `conduct-work-object` for durable
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
authorized deviation, pass `conduct-work-object` a concise record containing:

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

This skill is adapted for **Claude Code** from the canonical core.
Core decision logic, authority boundaries, and schema semantics are
preserved unchanged. This section documents only platform-specific
wiring and declared limitations.

### Installation and precedence

Install with the maintainer tool (no Python required at runtime — it
verifies checksums with the platform's `shasum`/`sha256sum`):

```sh
# Global bootstrap (conductor everywhere):
tools/install.sh --platform claude-code --global
# Project pin (takes precedence inside this project):
tools/install.sh --platform claude-code --project .
```

- Global install dir: `~/.claude/skills/`
- Project pin dir: `.claude/skills/`

A **project-pinned** adapter always takes precedence over the global
bootstrap install. The global install supplies conductor and bootstrap
behavior everywhere, then defers to the version a project has pinned.
Precedence is recorded in `.work-studio/adapter.lock` and enforced by
the generated adapter's runtime pin-resolution contract.

### Discovery

- Config path: `.work-studio/config.md`
- Boundary marker: `.git`
- Stop condition: repository root (presence of .git)
- Stop condition: filesystem boundary

### Capability Mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `browser_automation` | `—` | manual-fallback |
| `content_search` | `Grep` | native |
| `directory_list` | `Bash ls` | native |
| `file_read` | `Read` | native |
| `file_write` | `Write / Edit` | native |
| `git_operations` | `Bash (git commands)` | native |
| `glob_search` | `Glob` | native |
| `parallel_tool_execution` | `—` | manual-fallback |
| `structured_output` | `—` | native |
| `subagent_isolation` | `—` | manual-fallback |
| `subagent_spawn` | `Task` | native |
| `terminal_run` | `Bash` | native |
| `user_confirmation` | `conversation turn` | native |
| `web_fetch` | `WebFetch / WebSearch` | native |
| `web_search` | `WebSearch` | manual-fallback |

### Capability Degradation

This adapter classifies every required capability. When a capability
is unavailable, the workflow degrades explicitly — it never pretends
that equivalent verification occurred.

**Degradation rules**:

- **`manual-fallback`**: Pause with ONE concrete manual instruction.
  Record in the Work Object what was done and what remains unverified.
  Never mark verification, export, or deployment as "successful" when
  the required capability was unavailable.
- **`unsupported`**: Stop the affected path immediately. Record the
  platform limitation. Route to a supported platform or ask the user.
- **Stricter safety wins**: When this platform imposes a stricter
  constraint than the core, the platform rule takes precedence.
  Divergences are disclosed below.

#### `browser_automation` (manual-fallback)

- **Behavior**: Pause and give one concrete manual instruction.
- **Record**: Append History entry noting the capability gap, the
  manual action taken, and what remains unverified.
- **Note**: Claude Code browser automation differs from Codex. Complex page interactions may require manual steps.

#### `parallel_tool_execution` (manual-fallback)

- **Behavior**: Pause and give one concrete manual instruction.
- **Record**: Append History entry noting the capability gap, the
  manual action taken, and what remains unverified.

#### `subagent_isolation` (manual-fallback)

- **Behavior**: Pause and give one concrete manual instruction.
- **Record**: Append History entry noting the capability gap, the
  manual action taken, and what remains unverified.
- **Note**: Claude Code sub-agents (Task tool) have different isolation guarantees than Codex subagents. For sensitive multi-agent workflows, verify isolation boundaries manually.

#### `web_search` (manual-fallback)

- **Best-effort tool**: `WebSearch`
- **Behavior**: Pause and give one concrete manual instruction.
- **Record**: Append History entry noting the capability gap, the
  manual action taken, and what remains unverified.

### Declared Limitations

- **subagent_isolation**
  (manual-fallback):
  Claude Code sub-agents (Task tool) have different isolation guarantees than Codex subagents. For sensitive multi-agent workflows, verify isolation boundaries manually.
- **browser_automation**
  (manual-fallback):
  Claude Code browser automation differs from Codex. Complex page interactions may require manual steps.

### Integrity

This file is generated. Do not edit directly — edit the canonical core
at `skills/core/<skill>/SKILL.md` or the overlay at
`adapters/claude-code/overlay.yaml`. Regenerate with
`python3 tools/generate-adapters.py`.
