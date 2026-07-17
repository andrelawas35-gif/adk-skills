---
name: alawas-govern-scorecards
description: "alawas-govern-scorecards — Claude Code adapter"
platform: claude-code
---
# Govern Scorecards

## Governing principle

A scorecard is a review of attributable outcomes, not a measure of personal
worth or agent activity. It makes evidence, uncertainty, and tensions visible
so a human can decide whether to propose a bounded workflow change.

## Boundaries and non-goals

This skill does:

- Review completion, decision quality, reality contact, loop burden, routing quality,
  recovery quality, personal fit, artifact value, and novelty yield.
- Preserve each dimension's evidence, inference, confidence, exceptions, and
  revisit trigger, including conflicting signals and `insufficient` evidence.
- Propose a scoped Workflow Candidate or a linked successor revision through
  `alawas-maintain-working-method`.
- Preserve prior scorecards, candidates, evidence, and rule versions.

This skill does not:

- Compute a composite score, ranking, or activity proxy from message counts,
  hours, streaks, or artifact volume.
- Infer identity, personality, enduring preference, or capability from a
  scorecard.
- Promote, apply, retire, deploy, export, or directly alter a Working Method,
  skill, adapter, or workflow rule.
- Read or copy Personal Institution content without an approved Evidence Bridge.

## Inputs and preconditions

The input is a completed or reviewed Work Object with durable, attributable
outcome evidence. Each reviewed dimension requires a stated scope, source or
system evidence, inference, confidence, exceptions, and revisit trigger.
Missing material is recorded as `insufficient`; it is never silently converted
into a low score or a negative judgment.

## Required capabilities

The platform adapter classifies each capability as native, manual-fallback, or
unsupported and follows `references/CAPABILITY-DEGRADATION.md` when needed.

- `file_read` and `content_search` — retrieve the Work Object, permitted local
  outcome evidence, decision records, and prior candidate lineage.
- `file_write` — pass a concise scorecard or proposal record to
  `alawas-conduct-work-object` for durable persistence.
- `user_confirmation` — obtain the scoped authority needed for a proposed rule
  or any later candidate-maintenance decision.
- `structured_output` — return dimension-level evidence, conflicts, gaps,
  proposal status, and next route.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- A scorecard may recommend one bounded next move but never changes a workflow
  rule directly.
- A proposed rule remains an unconfirmed Workflow Candidate until the existing
  bounded test, contrary-evidence review, and explicit human confirmation gates
  in `alawas-maintain-working-method` are satisfied.
- A material revision creates a separate successor candidate or Working Method
  linked with `supersedes`; it never overwrites the prior version.
- High-consequence changes require explicit, scoped human confirmation before
  any durable mutation.
- For a high-consequence Work Object, confirmation must name the exact proposed
  mutation. Do not stage, annotate, change status, append History, or make any
  other mutation before that confirmation.

## Agreement Loop behavior

Apply the shared conversational inquiry contract in
`references/AGREEMENT-LOOP.md`: recommend one smallest evidence-supported
next move before one decision-bearing question. Do not use the review to seek
blanket authority for future rule changes, Personal Institution access, or
implementation.

When scorecard evidence conflicts or is insufficient, recommend preserving the
conflict or filling the smallest relevant gap rather than forcing a score,
identity claim, or proposal. Route a material workflow decision to
`alawas-pressure-test-decision` before recording it.

## Skill Grilling Profile

Apply the `alawas-govern-scorecards` profile and continuous Grilling Session in
`references/SKILL-AWARE-GRILLING.md`. Tie every dimension to an attributable,
decision-relevant evidence source; challenge activity proxies, hidden
distributions, aggregation, identity claims, and automatic action. On direct
entry, route through `alawas-conduct-work-object` first. Return the compact continuity
record; do not reset context, store a transcript, or mutate the Work Object.

## Stage workflow

### 1. Establish the review boundary

Read the Work Object's intended outcome, scope, evidence ledger, decision
record, verification evidence, recovery history, and uncertainty. State what
period, context, and sources the scorecard covers. Do not infer a scorecard
dimension from chat activity or unavailable records.

### 2. Review dimensions without collapsing conflicts

For every applicable dimension, retain this minimum record:

- dimension and bounded scope;
- attributable evidence and its provenance;
- a clearly labelled inference;
- confidence, exceptions, and a revisit trigger;
- `supported`, `contradicted`, or `insufficient` assessment where appropriate.

Conflicting signals remain separate. For example, a delivered artifact can
have favorable artifact value evidence and contradictory recovery-quality
evidence; neither is averaged into a composite score.

### 3. Propose, but do not govern automatically

When the review supports a change, propose a Workflow Candidate with a
testable rule, scope, origin scorecard reference, supporting and contrary
evidence, confidence, exceptions, and revisit trigger. Route it to
`alawas-maintain-working-method`; do not apply the proposal or treat one scorecard as
universal proof.

When a proposed or promoted rule changes materially, create a successor linked
by `supersedes`. Preserve the predecessor's identity, evidence, scope, and
version history. If evidence is insufficient or materially contradictory,
recommend a bounded investigation, revision, or retirement decision rather
than a new rule.

### 4. Protect personal fit and novelty yield

Personal fit is a scoped, user-provided outcome signal when attributable; it
is not an identity claim and cannot authorize Personal Institution access.
Novelty yield records whether a bounded review produced a useful new option or
falsified an assumption. It must not reward novelty churn, artifact volume, or
changes made merely to improve a scorecard.

## Evidence rules

- Label source, system, lived, inference, decision, and unresolved material
  according to `references/EVIDENCE-MODEL.md`.
- A missing signal is an evidence gap, not an unfavorable result.
- An approved Evidence Bridge is a minimum-necessary reference only; it does
  not authorize reading the Personal Institution archive.
- State `none observed within scope` only for the sources and period actually
  reviewed.

## Dependency invocation rules

- Route a workflow-rule proposal, revision, contrary-evidence review, bounded
  test, promotion, or retirement to `alawas-maintain-working-method`.
- Route unresolved outcome evidence to `alawas-review-outcome-and-adapt` or
  `alawas-investigate-live-question`.
- Route a material governance decision to `alawas-pressure-test-decision`.
- Report a missing dependency as reduced capability; do not imitate its gates.

## Work Object updates

Return a concise record to `alawas-conduct-work-object` containing the scorecard
scope, each reviewed dimension's evidence and provenance, inference,
confidence, exceptions, revisit trigger, conflicts, evidence gaps, and any
unconfirmed candidate or successor relationship. The conductor owns schema
validation, state/status transitions, History, and durable record placement.

## Routing and termination

- **Evidence supports a proposal:** route the unconfirmed scoped candidate to
  `alawas-maintain-working-method`; do not promote or apply it.
- **Evidence conflicts or is insufficient:** preserve the boundary and route
  the smallest investigation, outcome review, or decision move.
- **Material revision:** route the linked successor through
  `alawas-maintain-working-method` using `supersedes`; do not mutate the predecessor.
- **Manual-fallback capability:** pause with one concrete user-run instruction
  and mark the affected evidence unverified.
- **Unsupported capability:** stop the affected route, record the limitation,
  and route to a supported platform or the user.

## Output template

```markdown
## Scorecard governance review

- **Scope:** <Work Object, period, and evidence boundary>
- **Dimensions:** <evidence, inference, confidence, exceptions, revisit trigger>
- **Conflicts and gaps:** <preserved conflicts and insufficient evidence>
- **Proposal:** <none | unconfirmed Workflow Candidate | linked successor>
- **Protection:** <no aggregate, activity proxy, identity inference, or automatic change>
- **Next route:** <maintain-working-method | investigate | decision | none>
```

## Anti-patterns

- Averaging conflicting evidence into a number that conceals the trade-off.
- Treating message count, hours, streaks, or artifact volume as outcome value.
- Inferring identity or stable personal traits from a bounded review.
- Treating a scorecard proposal as a confirmed or applied workflow rule.
- Rewriting earlier evidence or rule versions to make the newest version look
  inevitable.

## Final self-check

- Does every reviewed dimension preserve attributable evidence, inference,
  confidence, exceptions, and a revisit trigger?
- Are conflicts and `insufficient` evidence visible rather than aggregated?
- Did the review avoid activity proxies and identity inference?
- Is every proposal unconfirmed, scoped, and routed through
  `alawas-maintain-working-method`?
- Does each material revision retain immutable predecessor history with
  `supersedes`?
- Did the review avoid automatic promotion, rule application, Personal
  Institution access, deployment, export, and direct mutation?
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
