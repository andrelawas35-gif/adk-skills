# Extract Behavioral Rule from Workspace Documentation Contract into a Constitution File

- **Status:** Accepted
- **Date:** 2026-07-21
- **Component:** COMP-002 (Work Object conductor), adapter generator
- **Decision owners:** Human-approved
- **Related Work Object:** None — decision reached during ADR review
- **Related ADRs:**
  - partially supersedes: ADR 0013 (narrows the consequence "adapter generation copies the contract so installed skills use the same rules")
- **Supersedes:** None
- **Superseded by:** None

## Context

ADR-0013 established `WORKSPACE-DOCUMENTATION-CONTRACT.md` as the sole bootstrap artifact and canonical registry. Its stated consequence was: "Adapter generation copies the contract so installed skills use the same rules."

This consequence conflates two things that are now being separated:

- **The behavioral rule**: "An absent registered artifact is a Missing Artifact Gap, never evidence or permission to invent content." This is a universal behavioral guarantee. Every skill, regardless of domain, must not fabricate content when an expected artifact is missing.
- **The contract document**: A registry table with artifact types, exact workspace paths, ownership, stage triggers, provenance rules, and validation pointers. This is a lookup table. Only two skills — `conduct-work-object` (which bootstraps and persists) and `track-components` (which registers components in the ledger) — actually consult it.

The full contract document is already copied into every generated adapter's `references/` directory via `SHARED_REFERENCES` in `tools/generate-adapters.py`. For 12 of 14 skills, it is dead weight — a registry table they never read, carrying paths and ownership fields they never consult.

The recommendation is to extract the behavioral rule into its own constitution file (`MISSING-ARTIFACT-GAP.md`) following the same pattern used for `AGREEMENT-LOOP.md`, `CONSEQUENCE-AUTHORITY.md`, and `EVIDENCE-MODEL.md` — a small, self-standing reference file that carries exactly the behavioral guarantee every skill needs. The full contract document retains its existing role as the authoritative lookup table for the skills that need it.

## Decision

The behavioral rule — "an absent registered artifact is a Missing Artifact Gap, never evidence or permission to invent content" — must be extracted from `WORKSPACE-DOCUMENTATION-CONTRACT.md` into a standalone constitution file (`references/MISSING-ARTIFACT-GAP.md`).

This constitution file must:

- State the Missing Artifact Gap principle directly and self-sufficiently — a reader should not need the full contract to understand the behavioral obligation.
- Be added to `SHARED_REFERENCES` in `tools/generate-adapters.py` so it is copied into every generated adapter's `references/` directory.
- Be referenced by all 14 core skills (either directly in their prose or implicitly via the shared references bundle) so the behavioral guarantee is discoverable regardless of which skill is active.

The full `WORKSPACE-DOCUMENTATION-CONTRACT.md` must remain:

- The authoritative registry of artifact types, paths, ownership, and stage triggers.
- In `SHARED_REFERENCES` (no change to its current distribution).
- The lookup target for `conduct-work-object` (discovery, bootstrap, persistence) and `track-components` (component-ledger registration).

This narrows ADR-0013's consequence: the **rule** is copied universally via the constitution file; the **contract document** is copied as a lookup table for the skills that need it. The original claim — "adapter generation copies the contract so installed skills use the same rules" — was correct about the mechanism but imprecise about which artifact carries the universal behavioral obligation.

## Scope

This decision applies to:

- `references/MISSING-ARTIFACT-GAP.md` (new file)
- `tools/generate-adapters.py` — `SHARED_REFERENCES` list
- All 14 core skills and their generated adapters (which will carry the constitution file)
- ADR-0013 (partially superseded on the specific consequence about rule distribution)

This decision does not apply to:

- The registry table in `WORKSPACE-DOCUMENTATION-CONTRACT.md` — its schema, ownership assignments, and stage triggers are unchanged
- The `owner:` field semantics (content accountability vs. write access) — that clarification is deferred per Session 5
- Any other shared reference file

## Rationale

ADR-0013 was correct that every skill needs the Missing Artifact Gap rule. It was imprecise in claiming that copying the full contract document was the mechanism for distributing that rule. The contract document is 100+ lines of registry YAML; the rule is one sentence in its opening paragraph. Bundling them into one file means 12 skills carry a registry they don't read to get a rule they must follow.

The constitution-file pattern already exists in this repository. `AGREEMENT-LOOP.md` is a small, self-standing reference carrying the grilling protocol. `CONSEQUENCE-AUTHORITY.md` carries the consequence and authority tables. `EVIDENCE-MODEL.md` carries the provenance lane definitions. Each is a focused behavioral contract extracted from what would otherwise be buried in a larger document. `MISSING-ARTIFACT-GAP.md` follows the same pattern: extract one behavioral guarantee into its own file so skills can reference it directly without parsing unrelated machinery.

The separation also makes future maintenance clearer. If the registry schema changes (a new artifact type, a new field), the contract document changes — but the constitution file doesn't, because the behavioral rule ("don't fabricate") is independent of which artifact types exist. If the behavioral rule itself evolves (e.g., a new gap classification), the constitution file changes — and the change is immediately visible as affecting every skill, not buried in a document most skills don't read.

## Alternatives Considered

### Keep the rule embedded in the contract document only

No extraction. Every skill that needs the Missing Artifact Gap rule must reference the full `WORKSPACE-DOCUMENTATION-CONTRACT.md`. The rule travels with the document because the document is already in `SHARED_REFERENCES`.

Rejected because: this is the status quo, and it already produces the dead-weight problem — 12 skills carry a registry table they never consult. More importantly, it makes the behavioral rule undiscoverable. A skill author reading `EVIDENCE-MODEL.md` for provenance rules has no reason to open `WORKSPACE-DOCUMENTATION-CONTRACT.md` — and the Missing Artifact Gap rule is in the latter, not the former. The rule's location should match its audience: every skill.

### Remove the contract document from SHARED_REFERENCES entirely

Only the constitution file is copied universally. Skills that need the full registry (`conduct-work-object`, `track-components`) reference it by path within the workspace.

Rejected because: it adds a runtime dependency (the workspace must be discoverable before the registry can be read) to the exact skills that need the registry at bootstrap time. Keeping the contract document in `SHARED_REFERENCES` means the conductor can read the registry even before discovering the workspace root — a property worth preserving.

### Add the Missing Artifact Gap rule to an existing shared reference instead of creating a new file

Add the sentence to `EVIDENCE-MODEL.md` or `CONSEQUENCE-AUTHORITY.md` rather than creating a standalone file.

Rejected because: the rule is not about evidence provenance or consequence gates — it is about artifact discovery. Placing it in an unrelated reference file would bury it under a misleading heading. The constitution-file pattern works because each file is named for its behavioral domain; `MISSING-ARTIFACT-GAP.md` tells a reader exactly what behavioral rule lives inside.

## Consequences

### Positive

- The Missing Artifact Gap rule is discoverable by name, in its own file, in every skill's reference bundle
- The full contract document's role is clarified: it is a lookup table for the conductor and track-components, not the mechanism for distributing behavioral rules
- Future behavioral rules extracted from the contract (or any other document) have a clear pattern to follow
- ADR-0013's consequence is narrowed from an imprecise claim to an accurate one

### Negative

- One more file in every adapter's `references/` directory (approximately 10 lines)
- ADR-0013's original consequence statement is now partially inaccurate and must be read alongside this ADR

### New obligations

- `references/MISSING-ARTIFACT-GAP.md` must be created and added to `SHARED_REFERENCES`
- All adapters must be regenerated
- The two skills that reference the full WDC (`conduct-work-object`, `track-components`) should cross-reference the constitution file where the behavioral rule is the relevant guarantee

### Risks

- The constitution file could drift from the contract document if one is updated without the other. Mitigation: the constitution file explicitly cites the contract document as its authoritative source, establishing a one-way dependency (contract → constitution) that makes drift directionally clear.

## Enforcement

Current enforcement: the constitution file is created and added to `SHARED_REFERENCES`. `python3 tools/generate-adapters.py --check` will verify that it is present in every generated adapter.

Planned enforcement: the `verify-conformance.py` extension (deferred alongside the Session 5 component plan) could assert that every skill's reference bundle contains the constitution file and that its content matches the authoritative sentence in the contract document.

## Validation

- `references/MISSING-ARTIFACT-GAP.md` must exist and contain the Missing Artifact Gap principle
- `tools/generate-adapters.py` must list `MISSING-ARTIFACT-GAP.md` in `SHARED_REFERENCES`
- `python3 tools/generate-adapters.py` must produce the file in every adapter's `references/` directory
- `python3 tools/generate-adapters.py --check` must pass
- The full `WORKSPACE-DOCUMENTATION-CONTRACT.md` must remain unchanged

## Migration

1. Create `references/MISSING-ARTIFACT-GAP.md` with the Missing Artifact Gap principle, citing the contract document as its authoritative source
2. Add `"MISSING-ARTIFACT-GAP.md"` to `SHARED_REFERENCES` in `tools/generate-adapters.py`
3. Regenerate adapters: `python3 tools/generate-adapters.py`
4. Verify: `python3 tools/generate-adapters.py --check`
5. Update `conduct-work-object` and `track-components` core skills to cross-reference the constitution file where behavioral guarantees are the relevant concern

The migration is additive — no existing files are removed or altered beyond the generator's `SHARED_REFERENCES` list.

## Revisit Triggers

Revisit this ADR when:

- A second behavioral rule is extracted from the contract document — the pattern may need generalization beyond a single constitution file
- A skill other than `conduct-work-object` or `track-components` is observed consulting the full contract document at runtime — the "only two skills need the lookup table" assumption would be falsified
- The Missing Artifact Gap principle itself changes — the constitution file and the contract document must be updated together, and the one-way dependency (contract → constitution) must be verified
- The `SHARED_REFERENCES` mechanism changes (e.g., conditional copying by skill rather than universal copying) — the constitution file's distribution model would need revisiting

## Evidence

### Observed

- `tools/generate-adapters.py:37-44` — `SHARED_REFERENCES` copies the full `WORKSPACE-DOCUMENTATION-CONTRACT.md` into every adapter
- `skills/core/conduct-work-object/SKILL.md:146-148` — references the full WDC for discovery; uses the term "Missing Artifact Gap"
- `skills/core/track-components/SKILL.md:49` — references the full WDC for component-ledger registration
- 12 of 14 core skills have no reference to the WDC in their prose — they carry it as dead weight

### Inferred

- The Missing Artifact Gap principle is a universal behavioral rule (every skill must not fabricate content for missing artifacts), but its discoverability depends on a file that 12 skills never read

### Decided

- Extract the behavioral rule into `references/MISSING-ARTIFACT-GAP.md` following the existing constitution-file pattern
- The full contract document retains its role as the authoritative registry
- ADR-0013's consequence is narrowed: the rule travels via the constitution file; the document travels as a lookup table
