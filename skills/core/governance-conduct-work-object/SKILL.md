---
name: conduct-work-object
default_tier: medium
description: "Use when work must start, resume, transition, or close; maintains the canonical Work Object and routes its next stage; does not perform specialist domain work."
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

Exactly one Primary Work Object receives build or deployment effort at a
time. The Primary slot is a genuine attention primitive — the conductor and
all specialists need to know which object owns the current implementation
pass. Supporting and other tracked-active objects have no numeric cap;
the active.md register is advisory, not a concurrency constraint.

## Boundaries and non-goals

**This skill does:**
- Discover the workspace and any existing Work Objects
- Discover, bootstrap, persist, and reconcile the Workspace Documentation
  Contract as its sole custodian
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

## Required capabilities

This skill requires the following abstract capabilities. The platform adapter
classifies each as native, manual-fallback, or unsupported and degrades
explicitly when one is unavailable (see `references/CAPABILITY-DEGRADATION.md`).

- `file_read` — Read Work Object files, config, active.md
- `file_write` — Create and update Work Object files, append History
- `directory_list` — List `.work-studio/objects/` directory
- `glob_search` — Find Work Objects by ID pattern (`YYYY/MM/<id>-*.md`)
- `content_search` — Search for Work Objects by title or content
- `terminal_run` — Run git commands for workspace discovery
- `git_operations` — Check repository boundaries, commit work
- `structured_output` — Produce valid YAML frontmatter

## Consequence and authority rules

- Creating or updating a Work Object of **low** or **meaningful** consequence:
  proceed, append History.
- Creating or updating a Work Object of **high** consequence: ask first.
- Writing **restricted-sensitivity** content to a Work Object body: ask first,
  regardless of consequence level. The restricted-content pointer-only rule
  (link to protected sources, never store restricted material directly) is
  the substantive prohibition — this gate ensures the agent encounters it
  before writing.
- For a high-consequence Work Object, confirmation must name the specific
  proposed mutation. Generic instructions such as `just execute`, `do
  recommended`, or `perform the next update` are not confirmation. Do not
  stage, annotate, change status, append History, or make any other mutation
  before receiving that scoped confirmation; reading and recommending remain
  allowed.
- Never export, share, deploy, or write outside `.work-studio/` without
  explicit human confirmation.
- `just execute` accepts the current recommendation but never bypasses safety,
  privacy, destructive-action, or external-commitment gates.

## Grilling entry and stage lens

The conductor owns durable checkpoint writes only. During ordinary operation,
when evidence selects a different stage lens, it routes:

- An unresolved decision about work direction → route to `pressure-test-decision`
- An unresolved design question → route to `design-tracer-bullet`
- An ambiguous signal without clear type → route to `turn-signal-into-work`

Routine lifecycle actions inside existing authority do not activate grilling.

## Skill Grilling Profile

Apply the `conduct-work-object` profile and continuous Grilling Session in
`references/SKILL-AWARE-GRILLING.md`. Reconstruct one testable outcome, detect
overlapping work, ground positive and negative evidence, and make consequence,
sensitivity, lifecycle, rationale, and authority explicit before persistence.

For a direct specialist request, discover or establish the Work Object before
routing while preserving the same Context Card, Evidence Ledger, Decision
Frontier, and accepted decisions. Create `## Grilling Session` lazily. Act as
the sole writer of compact continuity state; keep full decisions and evidence
in their canonical sections and never store a transcript.

## Session-boundary rule

This skill includes a session-boundary rule expressed as a bounded trial with
an explicit review condition (per the `maintain-working-method` guardrail-expiry
gate). The rule governs what happens when this skill is invoked at session
start:

| Condition | Default answer |
|-----------|----------------|
| Same repository, same plugin/connector set, same machine | **Stay in session.** Open a branch for the new Work Object; do not restart. Use `breadth-sweep` mode (`references/AGREEMENT-LOOP.md`) — the existing mechanism for holding multiple live Work Object branches in one session. |
| Session context reaches ~150–200k tokens | **Compact the conversation tail; do not restart.** Discarding the cached position-0 prefix costs more than continuing. |
| Position-0 changes (different repository, plugin/connector set, or machine) | **Hand off to a new session.** Position-0 is the session identity. |

**Trial review:** These defaults hold until the earlier of (a) the review date
recorded in the Work Object's `next_action` or (b) observed degradation at high
context — a dropped constraint, a re-read of a file already in context, or a
misremembered decision that survives a compaction. Either triggers a revisit
via `maintain-working-method`.

## Stage workflow

### 1. Discover workspace

First inspect root `WORKSPACE-DOCUMENTATION-CONTRACT.md` when it exists. Use
its registry to locate artifacts; do not search for plausible alternatives. If
it is absent, report a Missing Artifact Gap per `references/MISSING-ARTIFACT-GAP.md`
and recommend bootstrap. Create
only the contract after explicit bootstrap authority, except that an accepted
`component-ledger` registry entry also seeds its empty per-project ledger. For a legacy workspace,
inspect existing files but do not move, rename, import, or canonicalize them
without separately scoped migration authority.

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
   - Current hypothesis (if in Explore or Design)
   - Open questions
4. Do NOT replay full history or evidence — the Work Object is the record.
5. Route to the appropriate specialist based on state and next_action.

### 4. Create Work Object

**Authority gate:** Creating a Work Object at `high` consequence requires
explicit human confirmation. Before proceeding: (1) verify the consequence
and sensitivity fields, (2) request confirmation naming the action and scope,
(3) record a structured authority History entry per the authority recording
contract in `references/CONSEQUENCE-AUTHORITY.md`.

1. Determine or ask for:
   - `type`: inquiry, project, change, or incident
   - `consequence`: low, meaningful, or high
   - `sensitivity`: ordinary, private, or restricted

2. Run the deterministic CLI to create the Work Object:

   ```sh
   python3 -m tools.ws create \
     --title "<human-readable-title>" \
     --type <type> \
     --consequence <consequence> \
     --sensitivity <sensitivity>
   ```

   The CLI handles: immutable ID allocation with collision detection, YAML
   frontmatter generation with validated enums, body template with 7 required
   sections plus structured Decisions template, file write to the correct
   `objects/YYYY/MM/<id>-<slug>.md` path. It prints the created file path and
   allocated ID.

3. Append the creation History entry:

   ```sh
   python3 -m tools.ws append-history <id> \
     --action "Created" \
     --state notice \
     --status active \
     --actor "<platform>" \
     --rationale "<creation rationale>" \
     --expect-updated <updated_at>
   ```

4. Update `active.md` if this is the first active object or the user confirms
   it as Primary:

   ```sh
   python3 -m tools.ws activate <id> \
     --role primary \
     --expect-updated <updated_at>
   ```

### 5. Update Work Object

**Authority gate:** Writing restricted-sensitivity content to a Work Object
body requires explicit human confirmation at ALL consequence levels. Modifying
frontmatter `status` or `state` at `high` consequence requires explicit human
confirmation. Before proceeding: (1) verify the Work Object's consequence and
sensitivity fields, (2) request confirmation naming the action and scope,
(3) record a structured authority History entry per the authority recording
contract in `references/CONSEQUENCE-AUTHORITY.md`.

All `.work-studio/` file mutations go through the deterministic CLI
(`python3 -m tools.ws`). The CLI enforces optimistic concurrency, lifecycle
rules, and schema validation. Every write command except `ws create` and
`ws init` requires `--expect-updated`.

On any meaningful transition:

1. Read the current file to get `updated_at` from the YAML frontmatter.
2. Choose the appropriate CLI command for the change:

   **State/status transitions:**
   ```sh
   python3 -m tools.ws transition <id> \
     --state <target-state> \
     --status <target-status> \
     --expect-updated <current-updated_at> \
     --action "<description>" \
     --actor "<platform>" \
     --rationale "<reason>"
   ```

   **Closing a Work Object:**
   ```sh
   python3 -m tools.ws close <id> \
     --expect-updated <current-updated_at> \
     --rationale "<reason>"
   ```

   **Appending History (without state change):**
   ```sh
   python3 -m tools.ws append-history <id> \
     --action "<description>" \
     --state <current-state> \
     --status <current-status> \
     --actor "<platform>" \
     --rationale "<reason>" \
     --expect-updated <current-updated_at>
   ```

   **Appending Evidence:**
   ```sh
   python3 -m tools.ws append-evidence <id> \
     --tag "[system]|[decision]|[inference]|[gap]|[testimony]|[memory]" \
     --source "<source>" \
     --text "<entry>" \
     --expect-updated <current-updated_at>
   ```

3. Direct edits are sanctioned, not a workaround, for the sections no append
   command covers: `Intent`, `Success evidence` checkboxes, `Constraints and
   non-goals`, `Decisions and revisit triggers` (including full `### Decision
   N` blocks — there is no `append-decision` command), `Open questions`, and
   `Next move` (WO `2026-08-14-003` Decision 1). `Evidence ledger` rows and
   `History` entries stay CLI-only (`append-evidence`, `append-history`,
   `transition`, `close`) — never edit those directly. `next_action` can be
   set either by `ws transition --next-action` or `ws append-history
   --next-action` without a state change; a direct edit remains available
   when neither applies.

   **Concurrency rule for direct edits:** a direct edit is not guarded by
   `--expect-updated` at write time — it is caught retroactively. Always use
   the correct `--expect-updated` from the CLI on the *next* mutation of that
   object; a stale value there is what surfaces a conflict. This is
   sufficient under the studio's single-session, single-conductor operating
   model (`## Session-boundary rule`, above) but would need revisiting if the
   studio ever supports genuinely concurrent editors on the same Work Object.

4. The CLI handles `updated_at` updates, History appends, and concurrency
   checks automatically. If the CLI rejects with a concurrency error, re-read
   the file to get the new `updated_at` and retry.

### 6. Route to specialist

Based on current state and next_action, route to the appropriate skill:

| State | Typical route |
|-------|---------------|
| notice | turn-signal-into-work |
| explore | develop-idea |
| design | design-tracer-bullet |
| build | implement-bounded-change |
| verify | verify-release-evidence |
| release | deploy-with-recovery |
| observe | review-outcome-and-adapt |
| close | review-outcome-and-adapt (outcome review) |

> `investigate-live-question` is reachable as a **downstream route** from
> `develop-idea` when a specific falsifiable question emerges during
> exploration. The conductor does not route to `investigate-live-question`
> directly from the `explore` state — that path goes through `develop-idea`.

Route by stating: "Routing to [skill] for [specific task]." Include the Work
Object ID and the concrete question or task.

### 7. Manage attention

`active.md` is an advisory attention register, not a cardinality constraint.

**Primary** names exactly one Work Object — the one receiving current build
or deployment effort. This is a genuine attention primitive: every specialist
needs to know which object owns the current implementation pass.

**Supporting** lists all other active objects. There is no numeric cap.
The register exists for discoverability and resumption, not concurrency
enforcement.

Template:

```markdown
# Active Work Objects

## Primary
- `2026-07-15-001` — Build conduct-work-object skill

## Supporting
- `2026-07-15-002` — Research skill packaging formats
```

Update this file when:
- A new Work Object becomes Primary (user confirms)
- A Primary object is closed, paused, or waiting
- Any active object is added or removed from the register

**Do not**:
- Reject activation because a numeric cap is exceeded
- Silently demote or omit active objects to fit a cap
- Invent a priority-ordering scheme — ordering is the user's judgment

Do not change Work Object identity to represent attention shifts.

Use the CLI to manage attention:

```sh
python3 -m tools.ws activate <id> \
  --role primary|supporting|paused \
  --expect-updated <current-updated_at>
```

The CLI cross-checks that the object exists and is not closed before
updating `active.md`.

## Evidence rules

- Distinguish known, inferred, decided, and unresolved material.
- Every factual claim carries a provenance marker.
- Retrieve discoverable facts from the file system rather than asking.
- Record evidence in the Evidence ledger section, not in History entries.
- History entries contain rationale, not raw evidence.

## Adjacent Possibility behavior

During Explore or Design states, this skill may activate the
Adjacent Possibility Pass as described in the planning document. This is
delegated to the routed specialist, not performed by this skill directly.

## Dependency invocation rules

This skill composes with:
- `turn-signal-into-work` — for classifying and activating signals
- `develop-idea` — for divergent exploration in the explore state
- `pressure-test-decision` — for unresolved decisions
- `design-tracer-bullet` — for design work
- `implement-bounded-change` — for implementation
- `verify-release-evidence` — for verification
- `deploy-with-recovery` — for deployment
- `diagnose-production-incident` — for incidents
- `review-outcome-and-adapt` — for closing and review
- `maintain-working-method` — for workflow candidate governance
- `govern-scorecards` — for outcome scorecard review and candidate proposals
- `track-components` — for registering, sweeping, and grilling durable components
- `diagnose-homogenization` — for diagnosing and revising generic or unearned prose

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
- A blocking condition is recorded and the object is set to Waiting

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
