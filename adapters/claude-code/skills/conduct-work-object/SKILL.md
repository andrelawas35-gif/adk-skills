---
name: conduct-work-object
description: >
   Detect, create, activate, resume, update, and close Work Objects — the
  canonical continuity surface of Andrelawas Work Studio. Use when the user asks
  to start or resume work, check what's active, move work forward, record a
  decision, or close something out. This skill owns the Work Object lifecycle
  and routes to specialists for domain-specific work.
platform: claude-code
---
# Conduct Work Object

## Governing principle

A Work Object is the durable record of intent, evidence, decisions, and
outcomes. The chat is for interaction; the Work Object is for continuity.
This skill ensures that every Work Object is discoverable, schema-valid,
immutably identified, and sufficient as a standalone record when chat
history is unavailable.

## Personal working lens

Work Objects are not project management theater. They exist so that work
can be paused, resumed, handed off, reviewed, and learned from without
depending on any one person's memory or any one chat session's context.

One Primary Work Object receives build or deployment effort at a time, with
at most two Supporting Work Objects limited to inquiry, waiting, or
maintenance. This is a provisional rule to be reviewed after five completed
Work Objects.

## Boundaries and non-goals

**This skill does:**
- Discover the workspace and any existing Work Objects
- Create new Work Objects with valid schema and immutable ID
- Resume Work Objects by ID, restoring state, status, next action, and evidence
- Update frontmatter and body sections through routine transitions
- Append attributable History entries
- Route to domain specialists (pressure-test-decision, design-tracer-bullet,
  implement-bounded-change, etc.) for substantive work
- Manage the active.md attention register

**This skill does NOT:**
- Perform domain work itself (design, implementation, investigation,
  deployment) — it routes to specialists
- Export, share, or deploy anything
- Create or modify personal memory entries
- Run the Agreement Loop beyond identifying that a decision is needed
- Modify closed Work Objects except to link successors
- Migrate schemas without explicit human authority

## Inputs and preconditions

**Required inputs:**
- None for discovery and status check
- For creation: a signal, intent, or request from the user
- For resumption: an immutable Work Object ID or a request to "resume" with
  enough disambiguation

**Preconditions:**
- A `.work-studio/config.md` must exist or be creatable at the workspace root
- The workspace root must be identifiable (search upward for `.git`,
  `.work-studio/`, or filesystem boundary)

## Consequence and authority rules

Apply the rules in `references/CONSEQUENCE-AUTHORITY.md`:

- Creating or updating a Work Object of **low** or **meaningful** consequence:
  proceed, append History.
- Creating or updating a Work Object of **high** consequence: ask first.
- Never export, share, deploy, or write outside `.work-studio/` without
  explicit human confirmation.
- `just execute` accepts the current recommendation but never bypasses safety,
  privacy, destructive-action, or external-commitment gates.

## Agreement Loop behavior

This skill identifies decision boundaries but does not run the full Agreement
Loop itself. When it encounters:

- An unresolved decision about work direction → route to `pressure-test-decision`
- An unresolved design question → route to `design-tracer-bullet`
- An ambiguous signal without clear type → route to `turn-signal-into-work`

For routine decisions within this skill's authority (e.g., "should I resume the
last active Work Object?"), apply the loop minimally: recommend, ask one
question, integrate.

## Stage workflow

### 1. Discover workspace

Search upward from the current working directory for `.work-studio/config.md`.
Stop at:
- The repository root (presence of `.git`)
- The filesystem boundary (can't go higher)
- An explicit boundary marker (`.work-studio/BOUNDARY`)

Never scan the home directory automatically. If no workspace is found, offer
to create one at the current project root.

Read `active.md` if it exists to identify current Primary and Supporting
objects.

### 2. Detect or create

**If the user provides a Work Object ID** → resume (go to step 3).

**If the user provides a signal or intent without an ID**:
1. Check `active.md` for a matching Primary or Supporting object.
2. Check recent Work Objects by scanning `.work-studio/objects/` for title or
   intent matches.
3. If a match is found, confirm resumption with the user.
4. If no match, create a new Work Object (go to step 4).

**If the user asks "what's active" or "status"**:
1. Read `active.md`.
2. Read frontmatter of active objects.
3. Report: ID, title, type, status, state, next_action.

### 3. Resume by ID

1. Locate `.work-studio/objects/YYYY/MM/<id>-*.md` by glob for the ID.
2. Read the full Work Object.
3. Restore and report:
   - Title, type, status, state
   - `next_action`
   - Most recent History entries (last 3)
   - Current hypothesis (if in Explore, Decide, or Design)
   - Open questions
4. Do NOT replay full history or evidence — the Work Object is the record.
5. Route to the appropriate specialist based on state and next_action.

### 4. Create Work Object

1. Determine or ask for:
   - `type`: inquiry, project, change, or incident
   - `consequence`: low, meaningful, or high
   - `sensitivity`: ordinary, private, or restricted
2. Generate the immutable ID: `YYYY-MM-DD-NNN` where NNN is the next
   zero-padded sequence number for the day. Scan existing objects to avoid
   collisions.
3. Create the file at `.work-studio/objects/YYYY/MM/<id>-<slug>.md`.
4. Populate frontmatter with all required fields. Set:
   - `state`: `notice` (initial state)
   - `status`: `active` (unless explicitly waiting)
   - `created_at` and `updated_at`: now (RFC-3339)
5. Populate body with stub sections for Intent, Success evidence, Constraints
   and non-goals, Evidence ledger, Open questions, Next move, History.
6. Append the creation History entry.
7. Update `active.md` if this is the first active object or the user confirms
   it as Primary.

### 5. Update Work Object

On any meaningful transition:

1. Read the current file to get `updated_at`.
2. Prepare changes.
3. Re-read the file. If `updated_at` changed since step 1, report the conflict
   and stop.
4. Write the changes.
5. Update `updated_at` to now.
6. Append a History entry with timestamp, action, resulting state, actor type,
   platform, and rationale.

### 6. Route to specialist

Based on current state and next_action, route to the appropriate skill:

| State | Typical route |
|-------|---------------|
| notice, frame | turn-signal-into-work |
| explore | investigate-live-question |
| decide | pressure-test-decision |
| design | design-tracer-bullet |
| build | implement-bounded-change |
| verify | verify-release-evidence |
| release | deploy-with-recovery |
| observe | review-outcome-and-adapt |
| close | review-outcome-and-adapt (outcome review) |

Route by stating: "Routing to [skill] for [specific task]." Include the Work
Object ID and the concrete question or task.

### 7. Manage attention

`active.md` tracks the current Primary and Supporting objects:

```markdown
# Active Work Objects

## Primary
- `2026-07-15-001` — Build conduct-work-object skill

## Supporting
- `2026-07-15-002` — Research skill packaging formats
```

Update this file when:
- A new Work Object becomes Primary (user confirms)
- A Primary object is closed, paused, or blocked
- Supporting objects are added or removed

Do not change Work Object identity to represent attention shifts.

## Evidence rules

- Distinguish known, inferred, decided, and unresolved material.
- Every factual claim carries a provenance marker.
- Retrieve discoverable facts from the file system rather than asking.
- Record evidence in the Evidence ledger section, not in History entries.
- History entries contain rationale, not raw evidence.

## Adjacent Possibility behavior

During Explore, Decide, or Design states, this skill may activate the
Adjacent Possibility Pass as described in the planning document. This is
delegated to the routed specialist, not performed by this skill directly.

## Dependency invocation rules

This skill composes with:
- `turn-signal-into-work` — for classifying and activating signals
- `pressure-test-decision` — for unresolved decisions
- `design-tracer-bullet` — for design work
- `implement-bounded-change` — for implementation
- `verify-release-evidence` — for verification
- `deploy-with-recovery` — for deployment
- `diagnose-production-incident` — for incidents
- `review-outcome-and-adapt` — for closing and review
- `maintain-working-method` — for workflow candidate governance

Missing dependencies must be reported as reduced capability rather than
silently imitated.

## Work Object updates

After every interaction with a Work Object:
- `updated_at` is current
- A History entry is appended for any state or status change
- `next_action` reflects the concrete next move
- The Work Object is sufficient to resume work without chat context

## Routing and termination

**Route when:**
- Domain work is needed (design, implement, investigate, etc.)
- A decision requires the full Agreement Loop
- Action is more useful than deliberation

**Terminate when:**
- The Work Object is closed with a recorded outcome
- The user explicitly ends the session
- A blocking condition is recorded and the object is set to Blocked

## Output template

After each interaction, report:

```markdown
**Work Object**: `{id}` — {title}
**State**: {state} → {new_state} (if changed)
**Status**: {status}
**Next action**: {next_action}
**History appended**: {action} at {timestamp}
**Route**: {next_skill or "none — awaiting user input"}
```

## Failure and degradation behavior

| Failure | Behavior |
|---------|----------|
| No `.work-studio/config.md` found | Offer to create at project root. If declined, report inability to proceed. |
| Work Object file not found by ID | Report the ID, suggest checking active.md, list recent objects. |
| `updated_at` conflict on write | Report the conflict with both timestamps. Do not overwrite. Offer to re-read and retry. |
| Invalid frontmatter | Report the specific validation error. Offer to repair if the fix is unambiguous. |
| Missing specialist skill | Report reduced capability. Offer manual alternatives. |
| Home directory scan attempted | Stop immediately. Report the boundary. Suggest explicit configuration. |

## Anti-patterns

1. **Stage theater**: Moving through lifecycle states just to check boxes.
   States describe reality, not progress rituals.

2. **Context obesity**: Copying chat transcripts into the Work Object.
   Extract decisions and evidence, not conversation.

3. **Artifact sprawl**: Creating Work Objects for everything. An idea is
   provisional until activated. Use `inbox.md` for unactivated signals.

4. **Stale state**: Leaving `next_action` vague or outdated. The next
   action must be concrete enough that a different agent could continue.

5. **Authority drift**: Making high-consequence decisions without asking.
   When in doubt, confirm.

6. **Silent mutation**: Changing `type`, deleting History, or editing past
   entries. History is append-only. Types change via successor objects.

7. **Identity confusion**: Changing the Work Object ID or type in place
   rather than creating a linked successor.

8. **Memory overreach**: Writing to personal memory during routine work.
   Memory is read-only during ordinary work sessions.

## Final self-check

Before reporting completion:

- [ ] Work Object `id` is immutable, time-sortable, and collision-free
- [ ] Frontmatter passes schema validation (all required fields present and valid)
- [ ] `updated_at` is current
- [ ] History entry appended for any transition
- [ ] `next_action` is concrete and actionable
- [ ] Evidence carries provenance markers
- [ ] No hidden reasoning, full prompts, or chat transcripts stored
- [ ] Private storage is in `.work-studio/` (Git-excluded)
- [ ] Home directory was not scanned
- [ ] The Work Object is sufficient to resume without chat context
---

## Platform Adapter

This skill is adapted for **Claude Code** from the canonical core.
Core decision logic, authority boundaries, and schema semantics are
preserved unchanged. This section documents only platform-specific
wiring and declared limitations.

**Installation**: Copy this skill to `~/.claude/skills/`.

### Discovery

- Config path: `.work-studio/config.md`
- Boundary marker: `.git`
- Stop condition: repository root (presence of .git)
- Stop condition: filesystem boundary

### Capability Mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `content_search` | `Grep` | native |
| `directory_list` | `Bash ls` | native |
| `file_read` | `Read` | native |
| `file_write` | `Write / Edit` | native |
| `git_operations` | `Bash (git commands)` | native |
| `glob_search` | `Glob` | native |
| `structured_output` | `—` | native |
| `subagent_spawn` | `Task` | native |
| `terminal_run` | `Bash` | native |
| `web_fetch` | `WebFetch / WebSearch` | native |

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
