# Design Artifacts in Creative Coding Studio

- **Status:** Accepted (amended 2026-07-23)
- **Date:** 2026-07-22
- **Amended:** 2026-07-23
- **Component:** Design skill architecture
- **Decision owners:** Human-approved (Grilling Session 12, ephemeral; amended per Grilling Session 13)
- **Related Work Object:** `2026-07-22-006` (original), `2026-07-23-001` (amendment)
- **Related ADRs:**
  - related to: ADR 0024 (code-first token ownership — token inventory is ephemeral evidence)
  - related to: ADR 0027 (browser as canonical design evidence — screenshots are stored artifacts)
- **Supersedes:** None
- **Superseded by:** None

## Context

The design review layer produces artifacts: screenshots, comparison records,
NL command history, design branch metadata, governance events, and extracted
specifications. These artifacts need a home — in the Creative Coding Studio
(where the review layer lives), in the target project, or in the Work Object.

The question: which artifacts belong where?

## Decision

Durable design artifacts live in the Creative Coding Studio under
`design-history/`. Ephemeral observations live in the Work Object's Evidence
Ledger. The target project contains only code and git history — no design
artifacts are written to it.

### Artifact location split

**Durable — Creative Coding Studio `design-history/` directory:**

| Artifact | Path pattern | Producer |
|---|---|---|
| Screenshots | `design-history/<project>/<branch>/screenshots/` | Review layer capture |
| Comparison records | `design-history/<project>/comparisons/` | Review layer compare |
| NL command history | `design-history/<project>/commands/` | Review layer |
| Design branch metadata | `design-history/<project>/branches/` | Review layer |
| Extracted specifications | `design-history/<project>/specs/<slug>.yaml` | Spec extractor |
| Governance events | `design-history/<project>/events/` | Governance emitter |

**Ephemeral — Evidence Ledger entries:**

| Artifact | Tag | Owner skill |
|---|---|---|
| Discovery snapshot | `[system:discovery]` | audit-product-interface |
| Token inventory | `[system:token-inventory]` | build-design-foundation |
| Browser evidence | `[system:browser-evidence]` | Review layer capture |
| Verification report | `[system:verification-report]` | verify-design-implementation |
| Design direction | `[system:design-direction]` | apply-design-direction |

### Storage rules

1. **YAML and PNG format.** Metadata artifacts use YAML for machine
   readability. Screenshots are PNG for lossless visual fidelity.

2. **Git-tracked.** Design history is committed to the Creative Coding Studio
   repository. Changes are version-controlled alongside the review layer code.

3. **Meaningful-consequence creation.** Creating a new project's design history
   directory is a meaningful-consequence action.

4. **Automatic filesystem sync.** The review layer's IndexedDB store syncs to
   `design-history/` automatically. The filesystem is the durable backup; 
   IndexedDB is the fast working store.

5. **Per-project isolation.** Each target project gets its own subdirectory
   under `design-history/`, keyed by project identifier.

### Ephemeral artifact rules

1. **Per-pass scope.** Ephemeral artifacts are observations from a single
   design pass. They inform the current work but are not authoritative for
   future work.

2. **Evidence Ledger format.** Ephemeral artifacts use the standard Evidence
   Ledger entry format with typed tags.

3. **Not regenerated.** If an ephemeral artifact is needed in a new pass, the
   owning skill produces a fresh one by re-running discovery or verification.

## Scope

This decision applies to:

- All active design skills' output contracts
- The review layer's storage system
- The Creative Coding Studio's directory structure for design work

This decision does not apply to:

- Work Studio's own directory structure (`.work-studio/`)
- Target project directories (no design artifacts written there)
- Non-design artifacts in the Creative Coding Studio

## Rationale

**Creative Coding Studio ownership centralizes design history.** As a solo
developer working across multiple projects, design history for all projects
lives in one place — the Creative Coding Studio. This avoids scattering design
artifacts across project repositories and keeps the review layer's storage
co-located with its code.

**Target projects stay clean.** Target projects contain only their own code and
git history. No `design/` directory is created. Design review is an activity
that happens in the Creative Coding Studio, not an artifact that lives in the
target project.

**The ephemeral/durable split matches artifact lifecycle.** A discovery snapshot
is valid for one design pass. A screenshot comparison is a durable record of a
design decision. The split matches how each artifact is actually used.

**Automatic sync provides durability without ceremony.** IndexedDB provides
fast reads/writes during a review session. Filesystem sync ensures everything
is git-tracked and survives browser state loss. The user never manually
exports or saves.

## Alternatives Considered

### Artifacts in target project `design/` directory

Store design artifacts in each target project's repository.

Rejected because: this scatters design history across projects. For a solo
developer with multiple projects reviewed through one Creative Coding Studio,
centralized storage in the studio is simpler and more discoverable. Target
projects should contain only their own code.

### All artifacts in Evidence Ledger

Treat all design output as ephemeral evidence, regenerated each pass.

Rejected because: screenshots, comparison records, and command history are
durable records of design decisions. They should survive across Work Objects
and be browsable outside a specific work context.

### Artifacts in Work Studio `.work-studio/`

Store design history alongside Work Objects.

Rejected because: Work Studio is a governance framework, not a design tool.
Design artifacts belong with the design tool (the review layer in the Creative
Coding Studio), not with the governance system.

## Consequences

**Positive:**
- All design history for all projects in one place
- Target projects stay clean — no design directory clutter
- Git-tracked design history with full version control
- Automatic sync eliminates manual export steps

**Negative:**
- Design history is only accessible from the Creative Coding Studio
- `design-history/` directory grows with screenshots; git LFS may be needed
  (addressed in plan's growth management section)
- If the Creative Coding Studio repository is lost, design history for all
  projects is lost (mitigated by git remote backup)

**Neutral:**
- The per-project subdirectory structure scales naturally to multiple projects
- Extracted specifications are an optional output, generated only when
  a design direction is accepted

## Amendment record

### 2026-07-23 — Grilling Session 13: Move artifacts to Creative Coding Studio

**Authority:** DEC-A1 (design practice lives in Creative Coding Studio),
DEC-A4 (review artifacts live locally in the studio), DEC-A9 (IndexedDB +
automatic filesystem sync), Grilling Session 13 (14 accepted decisions)

**Changes:**
- Title changed from "Design Artifacts in Host Project Repository" to "Design
  Artifacts in Creative Coding Studio"
- Artifact location changed from target project `design/` to Creative Coding
  Studio `design-history/`
- Removed: Figma manifest, component registry for Figma mapping, authored
  specifications (define-interface-specification), authored user flows
  (model-user-flow), authored interface architecture (define-interface-architecture)
- Added: screenshots, comparison records, NL command history, design branch
  metadata, governance events, extracted specifications (lightweight, automatic)
- Added automatic IndexedDB → filesystem sync as the storage mechanism
- Renamed `verify-design-code-parity` to `verify-design-implementation`
- Renamed `[system:parity-report]` to `[system:verification-report]`
- Renamed `[system:revision-manifest]` to `[system:design-direction]`

**Reason:** The design practice lives in the Creative Coding Studio (DEC-A1),
not in each target project. As a solo developer, centralizing design history
in the studio is simpler than scattering it across projects. Figma artifacts
are removed because Figma was never adopted. Authored specification artifacts
are replaced by lightweight extracted specifications that emerge from the
creative workflow.
