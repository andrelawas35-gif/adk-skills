---
schema_version: 1
id: 2026-08-22-031
title: Add domain axis to Work Object frontmatter
type: inquiry
status: active
state: design
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-22T15:17:35Z
updated_at: 2026-08-22T15:18:17Z
next_action: design-tracer-bullet: test whether a fixed domain vocabulary cleanly labels the current corpus -- classify objects 026-029 (and spot-check the 018-022 business-router cluster and 026's business+architecture ambiguity) by hand before deciding scalar-vs-list and schema enforcement.


---
## Intent

<!-- Describe what this Work Object accomplishes and why it exists. -->

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [ ] A `domain:` frontmatter field with a controlled vocabulary is defined and schema-validated
- [ ] `ws create`/`ws start` accept `--domain`; existing objects can be backfilled
- [ ] Tooling can filter/count objects by domain (e.g. `ws list --domain business` or command-center grouping)
- [ ] The vocabulary cleanly classifies the current 41 objects, or a documented rule handles genuinely multi-domain cases


## Constraints and non-goals

**Constraints:**
- `domain` is a SECOND axis, independent of the existing `type` field ({change,inquiry,project,incident}); it does not replace or repurpose `type`.
- Filenames, the `YYYY/MM` storage path, and the ID resolver stay unchanged — domain lives only in frontmatter.
- Controlled vocabulary, not free text; changes to the vocabulary require a decision.

**Non-goals:**
- NOT domain-in-filename (Direction 2), domain folders (Direction 3), campaign reuse (Direction 4), or a derived-view-only projection (Direction 5).
- No retro-migration of storage layout; backfilling the `domain` field on existing objects is metadata-only.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Selected Direction 1: domain as a controlled-vocabulary frontmatter field

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Add a `domain:` frontmatter field (controlled vocabulary: business, architecture, asset, design, governance, engineering, research, ideation, operations — mirroring skill families) as a second classification axis alongside `type`. Metadata-only; filenames/paths/resolver unchanged. |
| **Authorization** | Director selected develop-idea Direction 1 and confirmed domain is a second axis (not a repurposing of `type`). |
| **Confidence** | high for the choice of axis and placement (basis: [system] no domain signal exists anywhere structural today; frontmatter is the only queryable, tool-enforceable home that doesn't touch the ID resolver); medium for the exact vocabulary (basis: [inference] — mirrors skill families but not yet tested against all 41 objects). |
| **Actor** | thinking-develop-idea (director-accepted) |
| **Revisit trigger** | If a real Work Object cannot be cleanly classified by a single domain value (e.g. genuinely business+architecture), revisit whether domain should allow a small ordered list rather than a scalar. |
| **Rationale** | Domain-as-metadata gives a queryable, schema-enforceable discipline axis without touching filenames, the YYYY/MM path, or the ID resolver/graph scans that assume that layout. Rejected alternatives: filename prefix (unenforced drift), domain folders (breaks the path/resolver contract — ADR-level), campaign reuse (conflates effort with discipline), derived-view-only (doesn't give a stored, authoritative label). |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [decision] | develop-idea selection, director-confirmed | develop-idea selection (director-confirmed): domain is a SECOND axis alongside the existing type field {change,inquiry,project,incident}, which describes work shape not discipline. Selected Direction 1: add a controlled-vocabulary domain: frontmatter field (business|architecture|asset|design|governance|engineering|research|ideation|operations, mirroring skill families). Filenames and YYYY/MM storage unchanged; tooling can filter by domain. Directions 2 (filename prefix), 3 (domain folders), 4 (campaign reuse), 5 (derived-view projection) not selected. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T15:17:35Z — Started via ws start (created + evidence + explore + activate supporting)

- **State:** explore
- **Status:** active
- **Actor:** thinking-develop-idea
- **Rationale:** Director chose domain-as-metadata: queryable and tool-enforceable without touching filenames, paths, or the ID resolver (which globs objects/YYYY/MM).
### 2026-08-22T15:18:17Z — Director selected develop-idea Direction 1 (domain as a controlled-vocabulary frontmatter field, second axis alongside type). Recorded as Decision 1. Routing to design-tracer-bullet.

- **State:** design
- **Status:** active
- **Actor:** thinking-develop-idea
- **Rationale:** Single direction selected; transition explore->design per develop-idea. The key assumption (a fixed vocabulary cleanly classifies every WO) needs a reality test before schema enforcement.
