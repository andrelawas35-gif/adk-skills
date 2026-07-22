# Work Object

The canonical unit of continuity in Andrelawas Work Studio. Chats are
interaction surfaces; Work Objects are continuity surfaces.

## Schema (minimum accepted)

```yaml
---
schema_version: 1
id: <immutable-time-sortable-id>
title: Human-readable title
type: inquiry | project | change | incident
status: active | waiting | paused | closed
state: notice | explore | design | build | verify | release | observe | close
consequence: low | meaningful | high
sensitivity: ordinary | private | restricted
created_at: RFC-3339 timestamp
updated_at: RFC-3339 timestamp
next_action: Concrete next move
---
```

### Required fields

| Field | Constraint |
|-------|------------|
| `id` | Immutable. Time-sortable: `YYYY-MM-DD-NNN` where NNN is a zero-padded sequence number for the day. Example: `2026-07-15-001`. |
| `title` | Human-readable. May change; references use `id`. |
| `type` | Immutable after activation. One of: `inquiry`, `project`, `change`, `incident`. |
| `status` | One of: `active`, `waiting`, `paused`, `closed`. |
| `state` | One lifecycle state. Governed by ADR 0015 (8-state model with 2 terminal prohibitions). Enforced by `ws transition`. |
| `consequence` | One of: `low`, `meaningful`, `high`. Governs required gates. |
| `sensitivity` | One of: `ordinary`, `private`, `restricted`. Governs storage and export rules. |
| `created_at` | RFC-3339 timestamp. Immutable. |
| `updated_at` | RFC-3339 timestamp. Updated on every meaningful transition. |
| `next_action` | Concrete, actionable next move. Must be clear enough that a different agent could continue. |

### Conditional fields

| Field | Required when |
|-------|---------------|
| `revisit_trigger` | `status` is `waiting` or `paused` |

## File naming

```
.work-studio/objects/YYYY/MM/<id>-<slug>.md
```

- `id` is the immutable time-sortable ID (e.g., `2026-07-15-001`)
- `slug` is a URL-safe version of the title, may change on rename
- Directory structure groups by year/month for filesystem navigability

## Identity rules

1. The `id` is immutable. It is assigned at creation and never changes.
2. The `type` is immutable after activation.
3. `title` and filename `slug` may change. References always use `id`.
4. When an Inquiry produces a Project, or an Incident produces a Change, create a linked successor with typed relationships (`resulted_in`, `responds_to`, `supersedes`). Do not mutate the original's type.

## Storage location

By default: `.work-studio/objects/` within the workspace root. Discovery searches upward from the current working directory for `.work-studio/config.md` and stops at the repository or filesystem boundary. Never scan the home directory automatically.

## Write path

All `.work-studio/` file mutations go through the deterministic CLI
(`python3 -m tools.ws`). Agents never write `.work-studio/` files directly.
The CLI enforces:

- Immutable ID allocation with collision detection (`ws create`)
- Lifecycle transition rules per ADR 0015 (`ws transition`, `ws close`)
- Optimistic concurrency via `--expect-updated` on every mutation
- Frontmatter schema validation (`ws validate schema`)
- Section structure validation (`ws validate sections`)
- Append-only invariants (`ws validate append-only`)
- Sensitivity rules (`ws validate sensitivity`)
- Attention register consistency (`ws validate attention`)

Every write command except `ws create` and `ws init` requires
`--expect-updated`. Use `--force` only for recovery with a stderr warning.

## Concurrency

**Work Studio assumes one active session per workspace.** The system does not protect against concurrent sessions.

The `ws` CLI enforces optimistic concurrency on every mutation of existing files via `--expect-updated`: it reads the file's `updated_at`, compares it to the caller-supplied timestamp, and rejects the write with both timestamps if they differ. `--force` bypasses the check with a stderr warning. This protects against intra-session staleness (e.g., when a specialist and conductor both hold references to the same object).

It is not a multi-session concurrency guarantee. If concurrent sessions ever become necessary, the concurrency model must be redesigned from scratch.

## Body sections

After the YAML frontmatter, the Markdown body contains:

| Section | Purpose |
|---------|---------|
| Intent | One sentence: what we're doing and why |
| Success evidence | Observable criteria for completion |
| Constraints and non-goals | Explicit boundaries |
| Evidence ledger | Dated entries with provenance lanes |
| Current hypothesis | Revisable working theory |
| Decisions and revisit triggers | Owned choices with rationale |
| Grilling Session | Compact Context Card, Decision Frontier, coverage, recommendation, and next question; created only when grilling activates |
| Relationships | Typed links to other Work Objects |
| Artifacts | Produced or referenced artifacts |
| Verification and release evidence | What was verified, how, and the result |
| Observed outcome | Post-completion reality vs. hypothesis |
| Open questions | Unresolved questions |
| Next move | Expanded from frontmatter `next_action` |
| Workflow Candidates | Proposed workflow rules with evidence |
| History | Immutable append-only entries |

## History entries

Every meaningful transition appends a History entry. Format:

```markdown
### YYYY-MM-DDTHH:MM:SSZ — <action>

- **State**: <resulting state>
- **Status**: <resulting status>
- **Actor**: human | agent
- **Platform**: codex | claude-code | github-copilot
- **Rationale**: Concise evidence-based reason for the transition
```

Do not store: hidden reasoning chains, full prompts, complete chat transcripts, or internal agent deliberation.

## Grilling Session continuity

Create `## Grilling Session` lazily when the Agreement Loop activates. Store
only the compact state defined in `AGREEMENT-LOOP.md`; keep decisions,
evidence, verification, outcomes, and History in their canonical sections.

On resume, reconstruct the Context Card from the current Work Object and
permitted evidence. Mark missing legacy history as unknown rather than
fabricating it. After every accepted decision, material evidence change, or
specialist route, the conductor checkpoints the session using optimistic
concurrency. A conflicting revision pauses consequential action until accepted
decisions and Decision Frontiers are reconciled.
