# Browser as Canonical Design Evidence

- **Status:** Accepted (amended 2026-07-23)
- **Date:** 2026-07-22
- **Amended:** 2026-07-23
- **Component:** Design skill architecture
- **Decision owners:** Human-approved (Grilling Session 12, ephemeral; amended per Grilling Session 13)
- **Related Work Object:** `2026-07-22-006` (original), `2026-07-23-001` (amendment)
- **Related ADRs:**
  - related to: ADR 0024 (code-first token ownership — code produces what the browser renders)
  - related to: ADR 0028 (design artifacts — screenshots are stored design evidence)
- **Supersedes:** None
- **Superseded by:** None

## Context

In a design workflow where code produces the visual output and the browser
renders it, the browser is the canonical visual evidence surface. Design review,
comparison, and verification all depend on what the browser shows. The question:
what role does browser rendering play in the governed design process?

## Decision

The browser IS the design surface. Browser rendering is the canonical visual
evidence for all design work. Screenshots captured from the browser are the
primary comparison and verification artifacts.

### Evidence mechanics

1. **Browser rendering is canonical.** What the browser shows for a given code
   state is the design. There is no separate design representation that needs
   to match the browser — the browser rendering IS the design.

2. **Screenshot capture records evidence.** The review layer captures
   screenshots at specified viewports (mobile, tablet, desktop) as PNG files.
   These screenshots are stored in `design-history/` and serve as comparison
   baselines, review artifacts, and governance evidence.

3. **Verification compares browser states.** `verify-design-implementation`
   compares the current browser rendering against the intended design direction.
   The comparison is browser-to-browser (current vs. baseline screenshots), not
   browser-to-specification.

4. **Capability degradation.** When browser automation is unavailable
   (manual-fallback capability), the skill pauses with one concrete manual
   instruction: "Open [URL] in a browser, verify the interface, and confirm."
   The user's confirmation creates the evidence entry. The skill does not
   claim verification occurred when it did not.

## Scope

This decision applies to:

- The review layer's screenshot capture system
- `verify-design-implementation` (browser comparison)
- `audit-product-interface` (discovers what the browser renders)
- All design skills that reference visual evidence

This decision does not apply to:

- Code-level verification (linting, type checking, tests)
- Token-level verification (handled by `build-design-foundation`)
- Non-visual aspects of design (accessibility semantics, performance)

## Rationale

**The browser is already the user's design surface.** In the NL → agent → code
→ browser workflow, the user sees and evaluates designs in the browser. Making
the browser canonical for governance aligns evidence with reality — what the
user reviews is what gets recorded.

**Screenshots are durable, comparable evidence.** A screenshot is a
point-in-time record of what the browser rendered. Screenshots can be compared
side-by-side across design branches, stored in git, and referenced from
governance events. They are the visual equivalent of a git commit.

**Manual fallback preserves the evidence model.** When browser automation is
unavailable, manual verification is slower but provides the same evidence
quality. The evidence model doesn't depend on automation — it depends on
someone (human or agent) confirming what the browser shows.

## Alternatives Considered

### Specification-based verification

Verify against a written specification rather than browser rendering.

Rejected because: in a code-first workflow, the specification follows the code,
not the other way around. Verifying against a specification that was extracted
from code creates a circular verification. The browser is the ground truth.

### No visual evidence — code review only

Trust that correct code produces correct visual output. Verify through code
review and tests only.

Rejected because: visual correctness is not derivable from code correctness.
CSS interactions, responsive behavior, and visual weight are emergent properties
that only manifest in the browser. Code review catches logic errors; browser
evidence catches visual errors.

## Consequences

**Positive:**
- Visual evidence is grounded in what users actually see
- Screenshots provide durable, comparable records
- The review layer's comparison features work directly with browser output
- Design branches can be visually compared via their screenshots

**Negative:**
- Requires a running dev server for the target project
- Screenshot fidelity depends on viewport configuration and rendering engine
- Large screenshot files may require git LFS (addressed in plan's growth
  management section)

**Neutral:**
- Browser evidence entries accumulate in design-history/ but are managed by
  the review layer's archival system

## Amendment record

### 2026-07-23 — Grilling Session 13: Reframe from gate to evidence

**Authority:** DEC-A2 (workflow is NL → agent → code → browser), DEC-A3
(tool is a governed review/iteration layer), Grilling Session 13 (14 accepted
decisions)

**Changes:**
- Title changed from "Browser Evidence Gates Figma Rendering" to "Browser as
  Canonical Design Evidence"
- Reframed: browser is now the design surface itself, not a verification gate
  before Figma rendering
- Removed all Figma/Figwright references (ADR 0025 deferred)
- Removed `render-to-figma` precondition gate mechanics
- Added screenshot capture as the primary evidence mechanism
- Added design branch comparison via screenshots
- Renamed `verify-design-code-parity` to `verify-design-implementation`
- Removed "no-bypass" rule (the browser is the surface, not a gate to bypass)
- Removed greenfield scope exclusion (the review layer handles existing code,
  and new code is still rendered in the browser)

**Reason:** Figma was never adopted. The browser is not a gate before Figma —
it IS the design surface. The review layer wraps the browser rendering with
governance (screenshots, comparison, history) rather than using it as a
precondition for Figma output.
