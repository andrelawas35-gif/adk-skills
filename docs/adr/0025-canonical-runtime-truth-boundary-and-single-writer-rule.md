# Canonical/Runtime Truth Boundary and the Single-Writer Rule

- **Status:** Accepted
- **Date:** 2026-08-14
- **Component:** None — this ADR governs the boundary between Work Studio and any future runtime plane, not an existing component
- **Decision owners:** Human-approved (director, 2026-08-14; develop-idea → pressure-test-decision)
- **Related Work Object:** `2026-08-14-008` — Local runtime plane Phase 0: accept truth boundary and single-writer rule (narrow ADR)
- **Related ADRs:**
  - depends on: ADR 0020 (one session per workspace — the single-writer rule below extends that assumption to a second process class)
  - complements: ADR 0017, ADR 0022, ADR 0024 (append-only History, Decisions, Evidence ledger, Claims — the properties a runtime must never mutate)
  - constrains: none yet; future runtime ADRs (environment, checkpoint store) are subordinate to this one
- **Supersedes:** None
- **Superseded by:** None

## Context

`references/architecture/langgraph-local-runtime-integrated-build-plan.md` proposes a second execution layer beneath Work Studio: an orchestrator (LangGraph in the plan's recommendation) that runs bounded Work Object passes with checkpoints, interrupts, retries, and event streams, while Markdown, Git, and `python3 -m tools.ws` remain the canonical record.

Its Phase 0 asks for one ADR accepting six things at once: the runtime plane, the truth table, a Python 3.11 environment, the single-writer rule, SQLite's limitation, and a ten-row deferral register.

This ADR deliberately accepts **two** of those six.

The reason is reversibility. The truth boundary — what counts as canonical, who may write it, what recovery means when each store is lost — is expensive to change later, because every downstream contract, test, and recovery procedure encodes it. The environment and storage choices (Python 3.11, `uv`, SQLite, dependency pins, repository layout) are cheap to change and are not yet load-bearing: no runtime code exists, no checkpoint has ever been written, and no dependency has been resolved. Accepting them now would mean deciding on the plan's assertion rather than on evidence, and would mean that a later pin change reopens an ADR whose governance content was never in question.

Work Studio has four in-repo precedents from a single session (2026-08-14) where machinery accepted on inference was later declined for lack of demonstrated need: Work Objects `2026-08-11-014`, `2026-08-11-015`, `2026-08-11-017`, and `2026-08-14-005`. In each, grounding against the live repository showed the motivating problem did not exist. That pattern is the direct argument for keeping this ADR narrow.

This ADR is therefore **not** an adoption of LangGraph. It states the boundary any runtime must respect, whoever builds it and whatever framework it uses.

## Decision

### 1. The truth boundary

Every class of state in a Work Studio deployment belongs to exactly one owner. The owner determines what the state means; other components may read it but must not treat their own copy as authoritative.

| State class | Owner | Storage | Recovery from *incorrectness* | Recovery from *loss* |
|---|---|---|---|---|
| Work Object facts, evidence, decisions, authority, lifecycle, artifacts, outcome reviews | Work Studio | Markdown under `.work-studio/objects/` (Git-**excluded**) | Repair or supersede through existing governance — a new Decision, a superseding Work Object, never an in-place edit of an append-only section | `python3 -m tools.ws backup` / `ws restore <timestamp>` (`tools/ws/backup.py`) — a local, network-free filesystem mirror to `~/.work-studio-backups/<timestamp>/objects/`. Manual invocation only; not scheduled. See WO `2026-08-14-009`. |
| Skill definitions and routing obligations | Work Studio | `skills/core/`, kernel manifest, generated adapters (Git-tracked) | Correct the canonical source in `skills/core/`, regenerate, verify | Restore from Git; regenerate adapters via `tools/generate-adapters.py`; verify with `--check` and `tools/verify-kernel.py` |
| Execution cursor, completed nodes, interrupts, retry state, transient errors | Runtime plane | Local checkpoint store (not yet chosen — see Deferred) | Discard the thread and re-run; a wrong cursor is never repaired in place | Resume, replay, fork, or discard. Loss costs execution progress only and must never require a canonical repair |
| Typed epistemic relationships and loop states | Projection code | In-memory graph; optional generated snapshot | Fix the extraction rule and rebuild | Rebuild deterministically from canonical Markdown. A projection is never a source |
| Runtime diagnostics and event streams | Runtime plane | Append-only local JSONL with retention | Not applicable — diagnostics record what happened, and are not corrected | Rotate or delete freely. Loss must change no canonical truth and block no governance operation |

Two invariants follow, and they are the substance of this decision:

- **A checkpoint, projection edge, event, or runtime inference must never create, alter, or retire a canonical claim.** Canonical claims change only through the `ws` write path with recorded authority.
- **Canonical loss is never recoverable from runtime state.** A runtime may be deleted entirely at any moment without governance consequence. The converse does not hold.

### 2. The single-writer rule

`.work-studio/` has exactly one writer: `python3 -m tools.ws`, invoked by the director's session.

A runtime plane must not write to `.work-studio/` directly — not the object files, not `active.md`, not the component ledger, not the inbox. When a runtime pass produces something that should become canonical, it emits a typed proposal and the write is performed through the CLI at a single serialized persistence point, under the same optimistic-concurrency and validation rules every other mutation obeys.

This extends ADR 0020 rather than replacing it. ADR 0020 assumes one *session* per workspace; this ADR adds that a runtime process is not a second writer that ADR 0020 failed to anticipate — it is a non-writer by construction.

### 3. What this ADR does not decide

Explicitly deferred, each to be decided in its own bounded Work Object at the phase where it first bears load:

| Deferred | Deferred to | Why not now |
|---|---|---|
| Python version, `uv`, dependency pins, repository layout | Phase 2 (runtime skeleton) | No runtime code exists; pins decided now would be resolved against an unbuilt package |
| Checkpoint store (SQLite or otherwise) and its durability profile | Phase 3 (durability) | No checkpoint has been written; SQLite's contention and corruption limits cannot be assessed against zero usage |
| Framework adoption — LangGraph specifically | After tracer evidence | The orchestration *shape* is testable with the standard library; framework choice should follow that evidence |
| The plan's ten-row deferral register | Each promotion trigger, individually | Deferring ten capabilities in one stroke is a list, not a decision; each has its own trigger |

Nothing in this ADR authorizes installing a dependency, creating a runtime storage path, or writing runtime code.

## Scope

This decision applies to:

- Any current or future runtime, orchestrator, scheduler, or agent process operating against this workspace
- The projection layer, whatever graph library backs it
- All runtime diagnostics, event streams, and checkpoint state
- The persistence path by which any automated pass proposes a canonical change

This decision does not apply to:

- Git's own concurrency and storage model
- `tools/generate-adapters.py`, which is a build step over Git-tracked sources
- External systems a Work Object's work may touch (deployment targets, APIs) — those are governed by authority and effect journals, not by this boundary
- Which framework, language, or storage engine a runtime uses, provided it respects the boundary

## Rationale

The boundary is worth deciding before code because it is the one property that cannot be retrofitted. A runtime built without it produces **dual truth**: a checkpoint or projection that a reader eventually trusts as authoritative, at which point the canonical record has silently become one opinion among several. The architecture plan names this risk itself, and names "false assurance" — treating checkpoint durability as canonical durability — alongside it.

Deciding it *narrowly* is worth it because the alternative bundles an irreversible governance claim with reversible tooling. If SQLite is later replaced, an ADR covering only the boundary needs no revision; an ADR covering both needs superseding, and the governance content gets re-litigated as collateral.

The single-writer rule is the mechanical form of the same claim. A boundary that says "runtime state is not canonical" but permits the runtime to write canonical files depends entirely on the runtime's good behavior. Routing every canonical change through one CLI path makes the boundary structural: validation, authority recording, append-only enforcement, and concurrency checking already live there, and a runtime that cannot bypass them cannot violate the boundary by accident.

Writing this now also costs almost nothing to reverse if the tracer proves the runtime idea unattractive — the ADR constrains what a runtime must be, and if no runtime is ever built, it constrains nothing.

## Alternatives Considered

### Accept the whole Phase 0 boundary as the plan specifies

One ADR covering runtime plane, truth table, Python 3.11, single-writer, SQLite, and the deferral register.

Rejected because it fuses a hard-to-reverse governance decision with six easily-reversed tooling choices, none of which currently bear load. Four Work Objects in one session (`2026-08-11-014`, `-015`, `-017`, `2026-08-14-005`) show the failure mode: machinery accepted on a plan's assertion, later declined when grounding showed no live need. Deciding SQLite's risk profile before a checkpoint exists is that same pattern.

### Gate acceptance on a clean validation baseline (debt-first)

Defer this ADR until `ws validate` reports zero errors, on the argument that automating a system with unresolved contradictions makes the contradictions execute faster.

Rejected because the gate is unsatisfiable as stated, and this was tested rather than assumed. A live run on 2026-08-14 reported 37 errors, of which roughly 25 are duplicate-whole-second-timestamp and append-only violations on historical July/August records. ADR 0017, 0022, and 0024 make those sections append-only — repairing them would itself be a violation. A zero-error baseline cannot be reached. The argument's underlying concern is real and is preserved: this ADR authorizes no automated mutation, and Work Object `2026-08-14-007` continues the repairable subset independently.

### Build the read-only tracer first, write the ADR from its evidence

Prove the orchestration shape with a standard-library tracer — load one Work Object, validate an envelope, stream events, interrupt for a director decision, write nothing — then write the boundary ADR from what it demonstrated.

Not rejected, but reordered. Its evidence-gathering step is this ADR's recorded next action. It was not chosen as Phase 0 itself because building a tracer while the truth boundary is unwritten runs the dual-truth risk during the build — precisely when the first checkpoint and first projection come into existence and the temptation to trust them appears. The boundary is cheap to state now and expensive to add later.

## Consequences

### Positive

- The one irreversible decision in the runtime program is recorded before any code
- Tooling choices stay open and can be decided against evidence rather than assertion
- The single-writer rule makes the boundary structural rather than behavioral
- A runtime may be discarded entirely at any point with zero governance consequence
- If the runtime program is abandoned, nothing here needs unwinding

### Negative

- The architecture record becomes several small ADRs instead of one, and the plan's tidy Phase 0 → Phase 8 sequence loosens
- Phase 2 and Phase 3 each carry a decision this ADR could have pre-answered
- A future reader must assemble the full runtime picture from multiple ADRs

### New obligations

- **Work Object loss recovery — resolved.** ~~This gap predates the runtime program and is independent of it, but this ADR is where it became explicit. It warrants its own Work Object.~~ Closed by WO `2026-08-14-009`: `ws backup`/`ws restore` (local filesystem mirror, no git, no network — a git-tracked backup was considered and rejected, since the exclusion is founding privacy design intent, not a stale default). Row 1 above updated accordingly. Scheduling/automation remains out of scope — invocation is manual.
- Before any runtime storage path is created, it must be added to `.gitignore` and reviewed for sensitivity — carried forward from the plan's Phase 0 exit evidence, unsatisfiable until a concrete path is proposed.
- `references/WORK-OBJECT.md` and the conductor skill should reference this boundary once a runtime exists to respect it. Not required while no runtime exists.

### Risks

- A runtime could respect the boundary in code while a *reader* — human or agent — begins trusting a projection or event stream as authoritative. Mitigation: the projection must be rebuildable from canonical sources by construction, so a divergent projection is always the projection's error.
- Deciding the boundary before the tracer means the truth table is grounded in the current repository rather than in runtime experience. Mitigation: the revisit trigger below covers exactly this.

## Enforcement

Current enforcement: none mechanical, and none required — no runtime exists. The decision is a negative constraint on software not yet written.

Planned enforcement, when a runtime is built:

- No runtime module may import or invoke a write path into `.work-studio/` other than by shelling out to `python3 -m tools.ws`
- Checkpoint and event fixtures must be asserted to contain references and bounded summaries only, never private or restricted bodies
- The projection must be rebuildable from canonical sources in a test, proving it is derived rather than authoritative

## Validation

- No runtime code writes to `.work-studio/` except through `python3 -m tools.ws`
- Every truth-table row's owner is singular — no state class appears under two owners
- Deleting all runtime storage leaves `ws validate` output unchanged
- Any future ADR proposing a checkpoint store, environment, or framework cites this ADR and does not restate or contradict its boundary

## Migration

None. No code changes, no behavior changes, no documentation changes are required by this ADR on its own. It constrains software that does not yet exist. The obligations above become actionable only when a runtime is proposed.

## Revisit Triggers

Revisit this ADR when:

- Drafting a future runtime ADR reveals a truth-table row whose owner is genuinely ambiguous in practice, rather than in prospect
- The read-only tracer demonstrates that the orchestration shape requires state this table has no row for
- A runtime needs to write canonically at a rate that makes the single serialized persistence point a measured bottleneck — note that this likely also triggers ADR 0020
- The Work Object loss-recovery gap is closed by a mechanism that changes row 1's storage claim
- Multi-user or multi-host operation is proposed, which changes the single-writer rule's foundation

## Evidence

### Observed

- `references/architecture/langgraph-local-runtime-integrated-build-plan.md` §2, §3, §7, §12 — proposed truth table, Python boundary, SQLite/replay semantics, deferral register
- `.gitignore` — `.work-studio/objects/`, `active.md`, `inbox.md` are Git-excluded; no runtime storage path is listed
- `tools/ws/validate.py:289` — confirms Work Objects live in a Git-excluded directory; `check_append_only_baseline` (`:453`) warns for objects lacking a `.bak-*` snapshot
- `python3 -m tools.ws validate`, 2026-08-14 — 37 errors; roughly 25 are duplicate-timestamp or append-only violations on historical records, immutable under ADR 0017/0022/0024
- System `python3` is 3.8.5; `/Users/andrelawas/.local/bin/python3.11` is 3.11.15 — the environment split the plan describes is real, and is deferred here regardless
- `tools/ws/schema.py:46-65` — `campaign` requires a `docs/design/*.md` path; the architecture plan lives under `references/architecture/`, so it cannot currently be referenced as a campaign anchor

### Inferred

- The truth boundary is the only Phase 0 item that is expensive to reverse; the remainder are cheap and not yet load-bearing. This is the basis for the narrow scope and is an inference from reversibility, not a measured fact.
- Routing all canonical writes through one CLI path makes the boundary structural rather than dependent on runtime good behavior.

### Decided

- Director, 2026-08-14 (Work Object `2026-08-14-008`, Decision 1): Direction 3 selected — narrow ADR covering the truth boundary and single-writer rule only; environment, checkpoint store, framework, and deferral register each deferred to their own bounded decisions; the standard-library read-only tracer recorded as the next move.
