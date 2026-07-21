# Sensitivity Gates Authority Independently of Consequence

- **Status:** Accepted
- **Date:** 2026-07-21
- **Component:** COMP-002 (Work Object conductor)
- **Decision owners:** Human-approved (grilling session, Decision 52)
- **Related Work Object:** None — decision reached during ephemeral grilling session (Sessions 2–3, Decisions 33–55)
- **Related ADRs:**
  - complements: ADR 0001 (Personal Institution separation — restricted sensitivity is the mechanism that protects personal material from entering Work Studio)
  - constrained by: ADR 0015 (lifecycle model — consequence governs lifecycle gates; sensitivity is an independent authority axis)

## Context

The Authority gates table in `references/CONSEQUENCE-AUTHORITY.md` gates every write operation by consequence level only. At `low` or `meaningful` consequence, "Update Work Object body" is "Agent may proceed" with no further check. At `high` consequence, the same operation requires explicit human confirmation.

The restricted-sensitivity pointer-only rule — "Restricted: Never store in Work Objects. Link to protected sources; reference by pointer only" — lives in a separate Sensitivity Classes table in the same file. An agent following the authority-check path reads the Authority gates table, finds "Agent may proceed" for a low-consequence body write, and has no structural reason to consult the Sensitivity Classes table before writing. The restricted-content rule is documented but structurally unreachable from the authority-check path.

This gap was identified during the Work Object Contract grilling session (Session 3). All 15 real Work Objects are `sensitivity: ordinary`, so the gap has not produced an actual breach — it is a designed gap, not an observed failure. But the system's own architecture (separate tables with no cross-reference) guarantees that the first restricted-sensitivity Work Object will be written to without the authority check that should have intercepted it.

The grilling session accepted Decision 52: add an explicit sensitivity row to the Authority gates table so the restricted-content rule is reachable at the point of write.

## Decision

The Authority gates table must include sensitivity as an independent gating axis, alongside consequence.

Writing restricted-sensitivity content to a Work Object body requires explicit human confirmation regardless of consequence level. Specifically:

- At any consequence level, writing content marked `sensitivity: restricted` to a Work Object body is gated — the agent must ask first.
- The gate applies to body writes, not to frontmatter reads or status inquiries.
- The restricted-content pointer-only rule (link to protected sources, never store restricted material directly) remains the substantive prohibition — the authority gate is the mechanism that ensures an agent encounters it before writing, not after.

This does not change the consequence-based gates. A `low`-consequence, `ordinary`-sensitivity body write still proceeds without confirmation. A `high`-consequence body write still requires confirmation regardless of sensitivity. Sensitivity adds a new gating condition; it does not replace or weaken the existing ones.

The decision does not create a sensitivity-consequence matrix (e.g., "medium sensitivity + low consequence = ask first"). The only sensitivity level with a structurally distinct authority gate is `restricted`, because it is the only level whose substantive rule (never store directly) can be violated by a routine body write that the existing consequence-only gate would allow. `private` sensitivity is governed by storage location (`.work-studio/`, Git-excluded), not by write-time authority — the gitignore rule provides defense-in-depth that the restricted level lacks.

## Scope

This decision applies to:

- The Authority gates table in `references/CONSEQUENCE-AUTHORITY.md`
- The conductor skill's authority-check behavior before body writes
- All specialist skills that write to Work Object bodies

This decision does not apply to:

- Frontmatter reads, status inquiries, or History appends (these do not write unrestricted body content)
- The `private` sensitivity class (governed by storage location, not write-time gating)
- Non-Work-Object writes (Personal Institution, PKM, regulation sessions)

## Rationale

The existing design has two tables that an agent must consult in sequence — Authority gates (gated by consequence) then Sensitivity Classes (gated by content type) — with no structural link between them. This is the same failure mode as any unreachable cross-reference: the second table is correct and important, and the first table gives no indication that the second exists.

Adding a sensitivity row to the Authority gates table fixes the structural gap without inventing a new axis. Sensitivity was always intended to govern storage and export rules (`CONSEQUENCE-AUTHORITY.md` already defines sensitivity classes with storage rules). The gap was that the authority-check path — the table an agent actually consults before writing — had no sensitivity dimension.

The fix is minimal: one row in an existing table, wiring an existing rule into an existing check path. It does not create a new enforcement mechanism, a new sensitivity level, or a new gating concept. It makes the existing restricted-content rule discoverable at the point where it matters.

All 15 real Work Objects are `ordinary` sensitivity, so this change has zero impact on current operations. It is a forward-looking guard for the first real `restricted`-sensitivity Work Object, whenever that occurs.

## Alternatives Considered

### Keep sensitivity and consequence fully separate; fix via agent instructions

Add an instruction to the conductor skill: "Before any body write, consult both the Authority gates table AND the Sensitivity Classes table." Rely on the agent reading and following prose.

Rejected because: this is the same unreachable-cross-reference failure mode that caused the gap. An instruction to "always consult both tables" is exactly the kind of prose-only guard that the grilling protocol exists to challenge — it depends on an agent remembering to follow a non-local rule with no structural prompt. The authority table is the natural checkpoint; wiring sensitivity into it makes the guard structural rather than memorial.

### Create a full sensitivity-consequence matrix

Define a grid: for every (sensitivity, consequence) pair, specify whether the agent may proceed or must ask.

Rejected because: only `restricted` sensitivity has a rule that a routine body write can violate. `private` sensitivity is governed by storage location (gitignore), and `ordinary` has no additional restriction. A full matrix would have one non-trivial cell (restricted × any consequence) and eight "proceed as normal" cells — ceremony without substance.

### Gate restricted-sensitivity at Work Object creation, not at body writes

Intercept `restricted` sensitivity at the point of Work Object creation rather than at body writes.

Rejected because: the user explicitly chooses sensitivity at creation time — they've already made the judgment that the object will handle restricted material. The risk is not that a restricted object exists (the user created it knowingly), but that an agent writes restricted content into its body without the pointer-only check. The gate belongs at the write, not at the creation.

## Consequences

### Positive

- The restricted-content pointer-only rule becomes reachable from the authority-check path
- An agent following the Authority gates table will encounter the sensitivity gate before writing restricted content
- No new mechanism, axis, or vocabulary — the fix reuses existing concepts in their existing locations

### Negative

- The Authority gates table gains a second dimension, modestly increasing its complexity
- The gate is still prose-only — no machine enforcement exists, and none is planned before the CLI session

### New obligations

- The Authority gates table must be updated with a sensitivity row
- The conductor skill must reflect the updated authority-check path
- Generated adapters must be regenerated after the source update

### Risks

- If an agent reads the Authority gates table but ignores the sensitivity row (same failure mode as ignoring the separate Sensitivity Classes table today), the gate provides no additional protection. Mitigation: the sensitivity row is in the same table the agent is already reading, not a separate file — the structural barrier is lower.

## Enforcement

Current enforcement: documented and wired in prose. The Authority gates table in `CONSEQUENCE-AUTHORITY.md` will include the sensitivity row. The conductor skill's authority-check behavior will reference it. No machine enforcement exists.

Planned enforcement: the future CLI's write path will check sensitivity before allowing body mutation. Until the CLI exists, enforcement depends on agent prose-compliance — same as every other authority rule in the system (Decision 45).

## Validation

- The Authority gates table must include a row gating restricted-sensitivity body writes with "Ask first, regardless of consequence"
- The row must be in the same table as the existing consequence-based gates, not in a separate section
- The conductor skill's authority-check instructions must reference the sensitivity row
- The restricted-content pointer-only rule in the Sensitivity Classes table must remain as the substantive prohibition
- No existing consequence-based gate may be weakened or removed

## Migration

1. Add a sensitivity row to the Authority gates table in `references/CONSEQUENCE-AUTHORITY.md`
2. Update the conductor skill's authority-check section to reference the sensitivity gate
3. Regenerate adapters via `python3 tools/generate-adapters.py`

The migration is a documentation change only — no code to migrate, no Work Objects to modify, no existing behavior to change (all current objects are `ordinary` sensitivity).

## Revisit Triggers

Revisit this ADR when:

- The first real `restricted`-sensitivity Work Object is created and the prose-only gate either works (the agent asks before writing) or fails (restricted content is written without confirmation)
- The CLI design session determines that sensitivity gating should be enforced through a different mechanism (e.g., field-level redaction rather than write-time confirmation)
- A new sensitivity level is added that requires a structurally distinct authority gate beyond what the current two-axis model (consequence + restricted-sensitivity) can express
- An actual restricted-content breach occurs despite the gate — the pointer-only rule is violated and restricted material is stored in a Work Object body

## Evidence

### Observed

- `references/CONSEQUENCE-AUTHORITY.md:23-34` — Authority gates table gates all operations by consequence only; no sensitivity dimension
- `references/CONSEQUENCE-AUTHORITY.md:21` — restricted-sensitivity pointer-only rule lives in the separate Sensitivity Classes table, with no cross-reference from the Authority gates table
- `.work-studio/objects/2026/07/` — all 15 real Work Objects have `sensitivity: ordinary`; no restricted-sensitivity breach has occurred

### Inferred

- An agent following the authority-check path reads the Authority gates table, finds "Agent may proceed" for a low-consequence body write, and has no structural prompt to consult the Sensitivity Classes table — the gap is designed into the table layout, not dependent on agent behavior

### Decided

- Decision 52 (grilling session, 2026-07-21): add an explicit sensitivity row to the Authority gates table — "Write restricted-sensitivity content → Ask first, regardless of consequence"
- The fix must be in the Authority gates table itself, not in a separate instruction to "consult both tables"
