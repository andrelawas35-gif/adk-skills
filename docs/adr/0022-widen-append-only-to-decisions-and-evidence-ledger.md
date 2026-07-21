# Widen Append-Only Scope to Decisions and Evidence Ledger

- **Status:** Accepted
- **Date:** 2026-07-21
- **Component:** COMP-002 (Work Object conductor)
- **Decision owners:** Human-approved (Grilling Session 7, Decisions 5 and 8; see `docs/design/evidence-model-component-plan.md`)
- **Related Work Object:** `2026-07-21-003` — Produce ADR-0022
- **Related ADRs:**
  - revises: ADR 0017 (widens scope from History-only to History + Decisions + Evidence ledger)
  - complements: ADR 0015 (gates read the Decisions section, which is now append-only protected)
  - complements: ADR 0016 (evidence inline tags are now append-only protected along with the ledger entries that carry them)
- **Supersedes:** None (ADR 0017's decisions remain correct for History; this ADR widens the scope, it does not reverse)
- **Superseded by:** None

## Context

ADR 0017 established that Work Object History entries are append-only — existing entries must not be edited, deleted, reordered, or renumbered. It explicitly exempted the Evidence ledger and Decisions section, stating they "may be edited or corrected."

The evidence-model component plan (Grilling Session 7, `docs/design/evidence-model-component-plan.md`) identified two risks that ADR 0017's narrow scope did not address:

**Risk 1: Gates read an unprotected section.** ADR 0015's five prerequisite gates were specified to check structured field values. The component plan's investigation found that the `## Decisions and revisit triggers` section — not the Evidence ledger — is where those structured fields (`Authorization`, `Confidence`, `Actor`, `Revisit trigger`) actually live in real Work Objects. ADR 0015's gates were clarified to read the Decisions section (Decision 4 of Grilling Session 7). But ADR 0017 exempts the Decisions section from append-only protection. Making Decisions the gate read-target without also protecting it would make a freely-editable section load-bearing for enforcement — a gate could be passed or failed by editing a past decision's fields after the fact.

**Risk 2: Evidence ledger entries can drift under Decision Rationales.** Real Decision Rationale fields embed inline-tagged claims (e.g., `**Rationale**: [system] The fixture passes...`) that summarize fuller Evidence ledger entries. Protecting the Decision text alone leaves the summarized source free to drift underneath it — a Rationale could cite evidence that was later edited to say something different, with no mechanism to detect the divergence.

The component plan accepted Decision 5 (extend append-only to individual Decision entries, formalizing the append-new-entry pattern real practice already follows) and Decision 8 (extend append-only to the full Evidence ledger). Correction in all three sections — History, Decisions, Evidence ledger — happens by appending a new entry, never by editing an existing one.

Additionally, the component plan found that the interim enforcement script ADR 0017 describes — a script that diffs a Work Object's History section against its last-committed version — does not exist anywhere in the repository. ADR 0017 described a planned mechanism, not a built one. The script, when built, must cover all three sections rather than History alone.

## Decision

The append-only rule applies uniformly to three Work Object body sections: **History**, **Decisions and revisit triggers**, and the **Evidence ledger**.

Specifically:

- Existing entries in any of the three sections must not be edited, deleted, reordered, or renumbered.
- New entries may only be appended at the end of their respective section.
- Correction in any section happens by appending a new entry that supersedes or clarifies the prior one, never by editing in place.
- Timestamps within each section must be unique at whole-second precision — three entries sharing an identical second-precision timestamp is a real, observed defect in production Work Object data that prevents unambiguous citation.

The interim enforcement mechanism (the append-only verification script ADR 0017 described but did not build) must, when built, check all three sections — not History alone. For each section, it must diff against the last-committed version and fail if any existing entry's text changed or was removed. New appended entries pass. It must also fail if any two entries within a Work Object share an identical timestamp.

This does not make the three sections structurally identical. History entries use a specific format (timestamp, action, state, actor, platform, rationale). Decision entries use structured fields with inline-tagged Rationales. Evidence ledger entries use the inline-tag convention (`[system]`, `[decision]`, `[inference]`, `[gap]`, `[testimony]`). The append-only rule applies to the entries themselves, not to the internal format of each entry type.

## Scope

This decision applies to:

- The History section of all Work Objects (unchanged from ADR 0017)
- The `## Decisions and revisit triggers` section of all Work Objects (newly covered)
- The Evidence ledger section of all Work Objects (newly covered)

This decision does not apply to:

- Frontmatter fields (may be edited or corrected)
- Body sections other than History, Decisions, and Evidence ledger
- Non-Work-Object structures (Values history, Regulation session records, event store entries)

## Rationale

ADR 0017's original reasoning for append-only — "an audit trail with gaps or altered entries is not an audit trail" — applies with equal force to Decisions and Evidence ledger entries. A decision that was silently edited after it was accepted is not a decision record; an evidence entry that was rewritten after a gate passed is not evidence. The three sections share the same structural property that motivated History's protection: they carry a permanent record whose corruption is unrecoverable.

The differentiation ADR 0017 drew — History is unrecoverable; Evidence and Decisions are "correctable" — collapses under the component plan's findings. The Evidence ledger's timestamp-collision defect shows that entries are already ambiguous without editing; allowing editing on top of ambiguity compounds the problem. The Decisions section's load-bearing role for gates means its past entries are just as consequential as History entries, and just as dangerous to alter after the fact.

The component plan did not make the three sections append-only in a blanket, section-freeze sense. Individual Decision entries are append-to-revise (you can add a new Decision that supersedes an old one), not frozen as a monolithic block. This matches real practice: real Work Objects already append new Decisions rather than editing old ones. The rule formalizes existing behavior; it does not impose a new constraint that practice must grow into.

The timestamp-uniqueness requirement addresses a real, observed defect: one real Work Object has three Evidence ledger bullets sharing an identical second-precision timestamp, making citation-by-timestamp ambiguous. Enforcing uniqueness at the entry level — without introducing a new ID field — fixes the citation problem at its source rather than adding a parallel numbering system.

## Alternatives Considered

### Keep ADR 0017 as-is; protect only History

No change. Evidence and Decisions remain editable. The gate read-target (Decisions) and the evidence base (Evidence ledger) are unprotected.

Rejected because: the component plan's investigation found two concrete risks — gate-gaming through post-hoc Decision edits, and Evidence drift under Decision Rationales — that the status quo does not address. ADR 0017's scope was correct for the state of knowledge at the time of its writing, when Decisions was not a gate read-target and the Evidence ledger's relationship to Decisions was not examined.

### Make the entire Decisions section append-only as a monolithic block

Once a Decision is written, no new Decisions can be added to the same Work Object.

Rejected because: real Work Objects accumulate decisions over their lifetime — a design decision in frame, an implementation decision in build, a verification decision in verify. Freezing the section after the first entry would force each new decision into a new Work Object, creating fragmentation for no gain in protection. Append-to-revise (new entry, not edit-in-place) protects past entries while allowing the section to grow naturally.

### Add an entry-level ID field instead of enforcing timestamp uniqueness

Every Evidence, Decision, and History entry gets a unique identifier (UUID, sequence number, or similar).

Rejected because: timestamps are already the de facto identifier used in prose ("the entry timestamped X"). Adding a parallel ID system requires writer bookkeeping that the inline-tag convention was specifically designed to avoid — the whole point of ADR 0016 was that evidence producers write a tag and prose at capture time, not fill out structured fields. Timestamp uniqueness fixes the actual problem (ambiguous citation) without adding a new field that all 14 skills would need to learn to populate.

## Consequences

### Positive

- The three sections that carry permanent records are uniformly protected under the same append-to-revise rule
- ADR 0015's gates reading the Decisions section now read a section that cannot be silently altered after the fact
- The timestamp-uniqueness requirement fixes a real, observed defect in production Work Object data
- The rule formalizes existing practice — real Work Objects already append-and-revise in all three sections

### Negative

- The interim enforcement script must now cover three sections instead of one (more code, same mechanism)
- ADR 0017's stated scope is now partially inaccurate and must be read alongside this ADR

### New obligations

- The append-only verification script must be built (it does not exist today). It must diff History, Decisions, and Evidence ledger against last-committed versions and enforce timestamp uniqueness
- ADR 0017's scope statement must be read as "History, Decisions, and Evidence ledger" rather than "History only"

### Risks

- The script is still not built. Until it exists, append-only protection for all three sections is prose-compliance only — the same gap that ADR 0017 identified and this ADR widens. Mitigation: the component plan (§6, migration step 6) schedules the script as part of the same implementation batch as the EVIDENCE-MODEL.md rewrite.

## Enforcement

Current enforcement: prose-compliance through the conductor skill and specialist contracts. All three sections are documented as append-only.

Planned enforcement: the append-only verification script (not yet built), which will diff each section against the last-committed version and enforce timestamp uniqueness per entry within a Work Object.

## Validation

- This ADR names ADR 0017 as the predecessor it revises
- This ADR documents the three-section scope (History, Decisions, Evidence ledger)
- This ADR references the evidence-model component plan as the source of accepted decisions
- This ADR does not duplicate the component plan's full contents

## Migration

No immediate migration of existing Work Objects is required — the append-to-revise pattern is already the observed practice. The migration is:

1. This ADR exists and is accepted
2. The append-only verification script is built (separate implementation task, per component plan §6.6)
3. When the script runs against all 15 real Work Objects, it should pass cleanly — no known corruption exists
4. ADR 0017's stated scope is read alongside this ADR when interpreting which sections are protected

## Revisit Triggers

Revisit this ADR when:

- The append-only verification script is built and run against real Work Objects, revealing whether any of the three sections have been silently edited in practice
- A real Work Object demonstrates a legitimate need to edit (not append-to-revise) a Decision or Evidence entry — the append-only rule would be falsified
- The CLI design session determines that append-only should be enforced through a different mechanism (e.g., content-addressable storage)
- The Decisions section's structured field format changes — the append-only rule's interaction with structured fields (vs. inline prose) may need refinement

## Evidence

### Observed

- `docs/adr/0017-...md:13` — ADR 0017 exempts Evidence ledger and Decisions from append-only: "does not apply to ... the Evidence ledger ... which may be edited or corrected"
- `docs/design/evidence-model-component-plan.md` §3.5 and §3.8 — Grilling Session 7 accepted Decisions 5 and 8, extending append-only to Decisions and Evidence ledger
- `docs/design/evidence-model-component-plan.md` §4 — component plan explicitly requires a follow-up ADR to ADR 0017
- `.work-studio/objects/2026/07/2026-07-20-001-...md` — real Evidence ledger with three entries sharing identical second-precision timestamp, confirming the timestamp-collision defect
- Grep across `tools/*.py` and `tests/*.py` — no append-only verification script exists
- Real Work Objects already append new Decisions and Evidence entries rather than editing old ones — the append-to-revise pattern is observed practice

### Decided

- Append-only applies uniformly to History, Decisions, and Evidence ledger (Grilling Session 7, Decisions 5 and 8)
- Correction in all three sections is append-a-new-entry, never edit-in-place
- Timestamps must be unique at whole-second precision within a Work Object
- The interim enforcement script must cover all three sections when built
