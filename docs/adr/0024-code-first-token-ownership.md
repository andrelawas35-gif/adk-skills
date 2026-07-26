# Code-First Token Ownership

- **Status:** Accepted (amended 2026-07-23)
- **Date:** 2026-07-22
- **Amended:** 2026-07-23
- **Component:** Design skill architecture
- **Decision owners:** Human-approved (Grilling Session 12, ephemeral; amended per Grilling Session 13)
- **Related Work Object:** `2026-07-22-006` (original), `2026-07-23-001` (amendment)
- **Related ADRs:**
  - related to: ADR 0025 (Figwright wrapping — deferred per Grilling Session 13)
  - related to: ADR 0028 (design artifacts — amended per Grilling Session 13)
- **Supersedes:** None
- **Superseded by:** None

## Context

Design systems maintain tokens (colors, typography, spacing, shadows, etc.) in
code. When a design review process reads and modifies these tokens, there must
be a clear ownership model. The question: what is canonical, and how do agents
discover and use tokens?

## Decision

Host-project code tokens are canonical. The agent discovers tokens from the
codebase and uses them when implementing design changes. There is no second
token system.

### Specific rules

1. **`build-design-foundation` reads code tokens.** It discovers and audits
   tokens from the host project's codebase (CSS custom properties, theme
   objects, token files). The result is a `[system:token-inventory]` ephemeral
   Evidence Ledger entry.

2. **The agent uses discovered tokens when implementing.** When creating or
   modifying design code in response to NL commands, the agent references the
   token inventory to ensure consistency with existing design decisions.

3. **`verify-design-implementation` flags divergence.** When implemented code
   introduces tokens that diverge from the established inventory, the
   verification report marks the divergence for review.

4. **Token edits are code changes.** Modifying tokens means modifying code,
   which goes through normal code review and git history.

## Scope

This decision applies to:

- All design skills that read or write tokens
- The `build-design-foundation` skill's discovery contract
- The agent's use of discovered tokens during implementation
- The `verify-design-implementation` skill's divergence reporting

This decision does not apply to:

- Host-project build tooling that generates code tokens from a different
  canonical source
- Non-token design properties (layout, component structure)

## Rationale

**Code is already version-controlled.** Tokens in code have full Git history,
code review, branch isolation, and rollback. Making code canonical means token
changes go through the same review process as all other code changes.

**Single source of truth eliminates sync.** With code as the only token
location, there is no sync, no conflicts, no ambiguity. The agent reads tokens
from code and uses them when writing code.

**Design branches provide experimentation.** The review layer's git-branch-based
design alternatives allow token experimentation without polluting the main
branch. Each alternative can try different token values; the accepted branch
merges them.

## Alternatives Considered

### Bidirectional sync with conflict resolution

Both sides are authoritative. Conflicts are detected and resolved through a
merge workflow.

Rejected because: with no external design tool, there is no second side to
sync with. Even if one is added later (revisit trigger), unidirectional
code→tool sync is simpler.

### No token awareness — manual consistency

The agent implements without token discovery. Consistency is checked manually.

Rejected because: manual consistency degrades over time. Token discovery is
cheap and prevents drift from the first change onward.

## Consequences

**Positive:**
- Clear ownership eliminates ambiguity about which token values are correct
- Token changes go through code review
- No sync complexity
- Works with any host project's existing token infrastructure

**Negative:**
- Token discovery depends on `build-design-foundation`'s ability to find tokens
  in diverse codebases

**Neutral:**
- If an external design tool is later adopted, this ADR's principle
  (code is canonical) still holds — the sync direction would be code→tool

## Amendment record

### 2026-07-23 — Grilling Session 13: Remove Figma references

**Authority:** DEC-A2 (workflow is NL → agent → code → browser), Grilling
Session 13 (14 accepted decisions)

**Changes:**
- Removed all references to Figma token sync, Figwright `token_map`, and
  code→Figma sync direction
- Removed `render-to-figma` token mapping rule (skill deferred)
- Renamed `verify-design-code-parity` to `verify-design-implementation`
- Simplified rationale: no second token system exists, so sync is eliminated
  rather than made unidirectional
- Removed "Figma-first token ownership" alternative (no Figma in architecture)
- Removed consequence about Figma-first workflows and Figwright token_map

**Reason:** Figma was never adopted. The design workflow is NL → agent → code →
browser. The review layer replaces Figma as a design surface. The code-first
principle strengthens — it is now the only principle, not one side of a
code→Figma relationship.
