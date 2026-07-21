# Work Studio Assumes One Session Per Workspace

- **Status:** Accepted
- **Date:** 2026-07-21
- **Component:** COMP-002 (Work Object conductor)
- **Decision owners:** Human-approved (grilling session, Session 5, Decision 3)
- **Related Work Object:** None — decision reached during ephemeral grilling session (Session 5: Skills & Machine-Readable Contracts)
- **Related ADRs:**
  - constrains: ADR 0015 (lifecycle model — transitions are per-session; no concurrent-transition conflict resolution exists)
  - complements: ADR 0017 (History append-only — a concurrent-write race corrupting History is the exact failure mode this decision accepts as out of scope)
- **Supersedes:** None
- **Superseded by:** None

## Context

`references/WORK-OBJECT.md` documents an optimistic-concurrency rule for Work Object updates: re-read the file immediately before writing and stop if `updated_at` changed since the initial read. The conductor skill encodes this in its Stage 5 update workflow.

What no document in the repository states is whether concurrent sessions — two agents or two terminal windows operating on the same workspace simultaneously — are in scope at all. The optimistic-concurrency rule could be read as a real concurrency guarantee (the system handles multi-session races) or as intra-session hygiene (a single agent checking that its own prior read is still current before a write). The text does not distinguish these interpretations, and the gap has practical consequences:

**Work Object creation has no concurrency protection.** The ID-generation algorithm is scan-then-write: list existing objects for the day, pick the next sequence number, write the file. Two concurrent sessions creating their first Work Object of the day would both see an empty directory, both pick `NNN = 001`, and both write — producing an ID collision. The `updated_at` check guards updates but not creation, because a file that does not exist yet has no `updated_at` to compare.

**No file lock, document lock, or atomic-ID mechanism exists.** `tools/` contains no locking primitive. The `.work-studio/` directory has no lock file. Git is the closest thing to a concurrency arbiter, and it is not used at creation time.

The Skills & Machine-Readable Contracts grilling session (Session 5) inspected this gap and accepted it as a deliberate non-goal: Work Studio does not protect against concurrent sessions because it assumes one session per workspace. Making this assumption explicit closes an unstated ambiguity that every reader of the concurrency section must currently resolve by guess.

## Decision

Work Studio assumes one active session per workspace. The system must not implement multi-session concurrency protection.

Specifically:

- The `updated_at` optimistic-concurrency check on updates is best-effort intra-session hygiene. It protects against a single agent reading stale state — for example, when a specialist writes to a Work Object the conductor also holds open. It is not a multi-session concurrency guarantee.
- ID generation may assume no concurrent creator. The scan-then-write algorithm is correct under the single-session assumption and must not be replaced with an atomic alternative (file lock, central counter, content-addressable ID).
- No document lock, advisory lock, or file lock must be added to `.work-studio/`. The workspace directory is single-writer by assumption.
- The future CLI must not implement multi-session locking, session tokens, or distributed coordination. It may assume it is the only process mutating `.work-studio/` state at any given time.

If concurrent sessions become necessary, the concurrency model must be redesigned from scratch — the existing `updated_at` check and scan-then-write ID generation are not partial implementations of a multi-session model; they are correct under the single-session assumption and incorrect under any other.

## Scope

This decision applies to:

- Work Object creation (ID generation, file placement)
- Work Object updates (the `updated_at` check)
- `active.md`, `inbox.md`, and `component-ledger.md` mutations
- The future CLI's mutation path
- All 14 specialist skills that delegate persistence to the conductor

This decision does not apply to:

- Git operations — Git has its own concurrency model (index locking) that Work Studio does not modify
- Platform adapter generation — `tools/generate-adapters.py` runs as a build step, not a session
- External systems that Work Studio integrates with (databases, APIs, deployment targets)

## Rationale

The single-session assumption is already true in practice. The repository has 15 real Work Objects created across multiple sessions over 6 days, and no ID collision, corrupted History, or concurrent-write artifact has been observed. The assumption held without being stated because real usage never exercised concurrent sessions. Making it explicit converts an unstated guess into a boundary.

Building multi-session concurrency protection would require solving distributed-coordination problems — atomic ID generation, file locking across processes, conflict detection for full-text Markdown files — that have mature solutions in databases and version-control systems but not in a local-markdown-files-plus-agent architecture. The cost of solving these problems is disproportionate to the benefit: a single user operating one session at a time has no need for distributed coordination, and the existing `updated_at` check already catches the only concurrency-like scenario that actually occurs (a specialist and the conductor both holding a reference to the same Work Object within one session).

Stating the assumption also constrains the future CLI. Without this decision, a CLI designer might reasonably read "optimistic concurrency" in `WORK-OBJECT.md` as a requirement and spend design effort on session tokens, lock files, or atomic-ID schemes — all of which would be ceremony without substance under the actual usage pattern.

The alternative of keeping the assumption unstated and letting each reader infer it is what produced the current ambiguity. The `updated_at` check is correct documentation for intra-session hygiene but misleading documentation for a multi-session guarantee it was never designed to provide. Making the scope explicit eliminates the ambiguity without changing any behavior.

## Alternatives Considered

### Build full multi-session concurrency protection

Add atomic ID generation (a central counter file with file locking), advisory locks for all `.work-studio/` writes, and session tokens to detect concurrent writers. The `updated_at` check becomes a real optimistic-concurrency mechanism backed by lock-based creation.

Rejected because: the implementation cost is high (file locking is platform-specific, atomic counter files are fragile, session tokens require a coordination point), and the benefit is zero for the actual usage pattern. Building distributed-coordination primitives into a local-markdown-files architecture is importing complexity from a different problem domain. If concurrent sessions ever become necessary, solving it then with real usage to test against is better than solving it now against hypothetical races.

### Leave the assumption unstated and let the `updated_at` check imply multi-session support

Keep the current documentation as-is. Readers infer whether "optimistic concurrency" means multi-session or intra-session.

Rejected because: the ambiguity is real — the grilling session itself flagged it as a finding. The `updated_at` check is correct documentation for the intra-session case but actively misleading for the multi-session case it was never designed to handle. A reader who assumes multi-session support will trust a guarantee that does not exist. A reader who assumes single-session will wonder why the check is documented as "concurrency" rather than "staleness." Stating the assumption eliminates both misreadings.

### Use Git as the concurrency arbiter

Require that every Work Object creation or mutation be immediately committed, using Git's index locking as the concurrency primitive. ID collisions are caught by the commit step.

Rejected because: it couples every conductor write to a Git commit, which is a heavyweight operation for what should be a lightweight state transition. It also introduces a new failure mode — what happens when a session is not on a clean branch? — that the current model deliberately avoids (Work Objects live in a Git-excluded directory precisely so work-in-progress commits don't interfere).

## Consequences

### Positive

- The `updated_at` check has a clear, honest scope: intra-session staleness detection, not multi-session concurrency
- The future CLI has one fewer distributed-systems problem to solve
- ID generation remains simple (scan-then-write) with no atomicity requirement
- No new infrastructure (lock files, session tokens, atomic counters) is introduced

### Negative

- If two sessions are ever accidentally run against the same workspace, the system offers no protection — ID collisions and write races are possible
- The boundary relies on human discipline (don't open two sessions) rather than mechanical enforcement

### New obligations

- `references/WORK-OBJECT.md`'s Concurrency section must be updated to state the single-session assumption explicitly
- The conductor skill's update workflow must note that the `updated_at` check is intra-session staleness detection, not a multi-session guarantee

### Risks

- A future platform adapter (e.g., a web-based client) could introduce concurrent-session scenarios that the current desktop-only model never encounters. Mitigation: the revisit trigger below explicitly covers this case — if concurrent sessions become possible, the concurrency model must be redesigned before they become supported.

## Enforcement

Current enforcement: none required. The decision is a negative constraint — it defines what must not be built, not what must be checked. The single-session assumption is enforced by the absence of a second session, not by a mechanism that prevents one.

Planned enforcement: the future CLI's mutation path must not include session tokens, lock files, or atomic-ID primitives. If these appear in a CLI design, this ADR is the authority for removing them.

Documentation enforcement: `references/WORK-OBJECT.md` must state the assumption. The conductor skill must scope its `updated_at` check correctly. These are prose changes deferred to the implementation batch alongside Decisions 46–55 from Sessions 2–3.

## Validation

- `references/WORK-OBJECT.md`'s Concurrency section must state that Work Studio assumes one session per workspace
- The conductor skill's update workflow must describe the `updated_at` check as intra-session staleness detection
- No lock file, session token, or atomic-ID mechanism may be introduced into `tools/` or `.work-studio/` without revisiting this ADR
- The future CLI design must not include multi-session coordination features

## Migration

1. Update `references/WORK-OBJECT.md`'s Concurrency section to state the single-session assumption
2. Update the conductor skill's Stage 5 (update) workflow to scope the `updated_at` check correctly
3. Regenerate adapters via `python3 tools/generate-adapters.py`

The migration is a documentation change only. No code to modify, no behavior to change — the system already operates under the single-session assumption; this ADR only makes it explicit.

## Revisit Triggers

Revisit this ADR when:

- A platform adapter or deployment model introduces the possibility of concurrent sessions (e.g., a web-based client, a shared workspace on a network filesystem, a CI pipeline that mutates Work Objects)
- An actual ID collision or concurrent-write corruption occurs, proving that the single-session assumption was violated in practice
- The future CLI design session determines that a lightweight concurrency primitive (e.g., a PID-based lock file) would add meaningful protection at trivial cost without the full weight of distributed coordination
- Work Studio is deployed in a context where multiple users share a workspace — the single-session assumption is per-workspace, and a shared workspace with multiple users fundamentally changes the concurrency scope

## Evidence

### Observed

- `references/WORK-OBJECT.md:67-69` — Concurrency section documents optimistic concurrency for updates only; no statement about whether concurrent sessions are in scope
- `skills/core/conduct-work-object/SKILL.md` (Stage 5) — update workflow includes re-read-and-check-`updated_at`; Stage 4 (creation) has no concurrency protection — ID generation is scan-then-write
- `.work-studio/objects/2026/07/` — 15 Work Objects across 6 days with zero ID collisions, zero corrupted History entries, zero concurrent-write artifacts
- `tools/` — no lock file, session token, or atomic-ID mechanism exists

### Inferred

- The `updated_at` check has always been intra-session staleness detection, not a multi-session concurrency guarantee. The ambiguity arose because the documentation used the word "concurrency" without stating the scope, and readers could reasonably interpret it either way.

### Decided

- Decision 3 (grilling session, Session 5, 2026-07-21): single-session-per-workspace is an accepted non-goal. Work Studio must not implement multi-session concurrency protection.
