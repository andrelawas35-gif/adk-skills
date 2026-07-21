# Attention Register Is Advisory, Not a Cardinality Constraint

- **Status:** Accepted
- **Date:** 2026-07-21
- **Component:** COMP-002 (Work Object conductor)
- **Decision owners:** Human-approved (grilling session, Decision 50)
- **Related Work Object:** None — decision reached during ephemeral grilling session (Sessions 2–3, Decisions 33–55)
- **Related ADRs:**
  - constrains: ADR 0015 (lifecycle model that the attention register tracks)

## Context

The conductor skill (`conduct-work-object`) and `active.md` both encode a cardinality rule: one Primary Work Object receives build or deployment effort at a time, with at most two Supporting Work Objects limited to inquiry, waiting, or maintenance. The rule was explicitly provisional — `active.md`'s own comment states "Review after five completed Work Objects."

Three findings from the Work Object Contract grilling session (Session 3, Decisions 45–55) make this rule untenable as a constraint:

**The review trigger fired and was never acted on.** A count of `status: closed` Work Objects in the repository shows 7 closed objects — the self-declared review threshold of five was passed and the review never occurred. The rule has been operating past its own expiry.

**Real usage already exceeds the cap by 3.5×.** The repository has 15 real Work Objects. During active development periods, 7 or more objects have been concurrently `status: active` against a documented cap of 3. This divergence produced no evidence of harm — no duplicated work, no lost context, no attention thrash attributable to the count rather than the content of active work.

**`active.md` itself is factually inaccurate.** The file omits `2026-07-15-002` (`status: paused`) from the Paused section, making a false claim about the register's own contents. This is not a rule question — it is a maintenance failure that a cardinality constraint did not prevent and an advisory register would still catch.

The grilling session accepted Decision 50: treat the overdue review as the review itself, and loosen the hard numeric cap on Supporting and tracked-active objects while preserving Primary as a real singular concept.

## Decision

`active.md` is an advisory attention register, not a cardinality constraint.

The Primary slot must name exactly one Work Object — the one receiving current build or deployment effort. This is a genuine attention primitive: the conductor and all specialists need to know which object owns the current implementation pass.

The Supporting section and any other tracked-active objects have no hard numeric cap. The register's purpose is discoverability and resumption — an agent resuming work should be able to read `active.md` and understand what is in flight — not enforcement of a concurrency limit that real usage has already demonstrated is artificial.

The conductor must:

- Update `active.md` when a Work Object becomes Primary, closes, pauses, or blocks — same obligation as before, now without a count check.
- Report all active objects on status inquiry, not silently truncate to three.
- Preserve the Primary slot as a singular concept — exactly one object at a time holds it.
- Treat the Supporting section as an accurate list of what else is active, not a capped subset.

The conductor must not:

- Reject activation of a fourth (or tenth) Work Object because a numeric cap is exceeded.
- Silently demote or omit active objects to fit a cap.
- Invent a priority-ordering scheme to compensate for the removed cap — ordering is the user's judgment.

The provisional review clause ("Review after five completed Work Objects") is satisfied by this decision. No new review trigger is set — the register format will be revisited if and when real usage demonstrates a problem with the advisory model.

## Scope

This decision applies to:

- `active.md` in every Work Studio project
- The conductor skill's attention-management behavior
- All specialist skills that consult `active.md` for context

This decision does not apply to:

- The component ledger's status model (`active`, `proposed`, `under-review`, `deprecated`) — a separate grilling target
- The inbox (`inbox.md`), which has its own activation rules
- Non-Work-Studio attention systems (Personal Institution, PKM)

## Rationale

The hard cap was always provisional — "review after five completed Work Objects" — and the review trigger fired without being noticed. A constraint that its own mechanism cannot enforce and its own maintainers cannot remember to review is not a constraint; it is a documented aspiration.

Real usage already ignored the cap without consequences. Seven concurrent active objects during the prompt-payload optimization chain (`2026-07-20-001` through `2026-07-20-005`) produced a coherent, linked set of closed Work Objects with no evidence of attention thrash. The constraint was limiting in documentation only — it never limited actual work.

Preserving Primary as a singular concept keeps the one genuine attention primitive. When the conductor routes to `implement-bounded-change`, the specialist needs to know which Work Object owns the current build. That question has exactly one answer. The Supporting section is context, not capacity management.

The alternative — enforcing the cap — would require the conductor to either reject legitimate work (harmful) or silently omit active objects from the register (misleading). Neither is acceptable.

## Alternatives Considered

### Keep the hard cap and fix compliance

Enforce the one-Primary/two-Supporting rule by having the conductor reject activation beyond the cap and require the user to close or pause objects before starting new ones.

Rejected because: the cap was never enforced in practice, real usage already demonstrated it is unnecessary, and rejecting legitimate work to satisfy a provisional rule that already passed its own review trigger is process theater. The conductor exists to enable work, not to ration attention slots.

### Remove Primary as a concept entirely

Make `active.md` a flat list with no distinguished Primary slot.

Rejected because: the Primary slot answers a genuine question — "what am I building right now?" — that every specialist needs to know. Removing it would force every specialist to infer attention from recency or guess, introducing ambiguity where none exists today.

### Keep the cap but raise it to match observed usage

Set the cap to 7 or 10, matching the highest observed concurrent count.

Rejected because: it replaces one arbitrary number with another. If the cap exists to prevent a problem that has never occurred, raising it doesn't make it more useful — it just kicks the same review failure down the road. An advisory register with no cap is simpler and honest about what it can and cannot guarantee.

## Consequences

### Positive

- `active.md` becomes an accurate reflection of real work, not a curated subset
- The conductor no longer faces an impossible choice between rejecting work and misrepresenting state
- The review-trigger debt is cleared — no expired provisional rule lingers in the codebase
- Future agents resuming work see a complete picture of what is in flight

### Negative

- No mechanical backstop against genuine attention fragmentation — the system trusts the user to manage concurrency
- The register may grow large during active periods; `ws status` output will need to handle this gracefully

### New obligations

- The conductor must update `active.md` accurately for all active objects, not just the capped three
- `ws status` (when built) must display all active objects, not silently truncate

### Risks

- An agent or user could activate dozens of Work Objects simultaneously with no mechanical guard. Mitigation: the inbox activation model (signals must be explicitly promoted) already throttles Work Object creation, and the cost of creating and maintaining a Work Object is its own deterrent.

## Enforcement

Current enforcement: prose/agent-compliance through the conductor skill. The conductor's SKILL.md must be updated to reflect the advisory model. `active.md`'s own comment must be updated to remove the provisional cardinality rule and the review trigger.

Planned enforcement: none. Unlike lifecycle state transitions or History immutability, attention registration has no planned machine enforcement. The register is inherently a human judgment about focus, and no schema check can determine whether the user is genuinely attending to seven objects or spread too thin.

## Validation

- `active.md` must list all objects the user considers active, not a capped subset
- The Primary slot must contain exactly one Work Object ID or `None`
- The Supporting section must list objects with their current status
- No object may appear in both Primary and Supporting simultaneously
- The register's comment block must reflect the advisory model and must not claim a numeric cap

## Migration

1. Update `active.md`'s comment block to remove the cardinality rule and the expired review trigger
2. Add `2026-07-15-002` to the Paused section (factual correction, not a rule change)
3. Update the conductor SKILL.md's attention-management section to reflect the advisory model
4. Remove the one-Primary/two-Supporting constraint from the conductor's "Personal working lens" section in both the core skill and all generated adapters
5. Regenerate adapters via `python3 tools/generate-adapters.py`

The migration is a documentation change only — no code to migrate, no CLI to update, no Work Objects to modify.

## Revisit Triggers

Revisit this ADR when:

- A real attention-fragmentation incident occurs — genuine duplicated or conflicting work traceable to having too many active objects rather than too little context per object
- The `ws status` command (when built) reveals that the flat list is unusably long and some form of ordering or filtering becomes necessary
- The user requests a mechanical attention guard after experiencing fragmentation that the advisory model did not prevent

## Evidence

### Observed

- `.work-studio/active.md` — documents the one-Primary/two-Supporting rule with "Review after five completed Work Objects" comment; currently omits `2026-07-15-002` from Paused section
- `.work-studio/objects/2026/07/` — 15 real Work Object files; 7 with `status: closed` (review trigger fired)
- `.work-studio/objects/2026/07/2026-07-20-001` through `2026-07-20-005` — 5 linked Change objects all `status: active` concurrently during the prompt-payload optimization chain, with no evidence of attention thrash in their History entries

### Decided

- Decision 50 (grilling session, 2026-07-21): drop the hard numeric cap, make `active.md` an advisory register, preserve Primary as a singular concept
- The provisional review clause is satisfied by this decision — no new review trigger is set
