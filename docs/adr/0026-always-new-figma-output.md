# Always-New Figma Output

- **Status:** Deferred (2026-07-23)
- **Date:** 2026-07-22
- **Deferred:** 2026-07-23
- **Component:** Design skill architecture
- **Decision owners:** Human-approved (Grilling Session 12, ephemeral; deferred per Grilling Session 13)
- **Related Work Object:** `2026-07-22-006` (original), `2026-07-23-001` (deferral)
- **Related ADRs:**
  - depends on: ADR 0025 (Figwright wrapping — preservation policy enforced through wrapper)
  - related to: ADR 0028 (design artifacts in host project — Figma manifest tracks pages and approved frames)
- **Supersedes:** None
- **Superseded by:** None

## Context

When a design skill renders output to Figma, it must decide whether to create new content or update existing content. Updating existing frames risks overwriting approved designs, losing design history, and creating ambiguity about which version was reviewed and accepted.

The question: what is the default write policy for Figma output, and under what conditions can existing content be modified?

## Decision

`render-to-figma` always creates a new page or section. Existing content is never modified by default. The page/section is named with the Work Object ID, specification slug, and pass number for traceability.

### Write policy tiers

1. **Default: always-new.** Every render creates a new page or section. Named: `{WO-ID} / {spec-slug} / pass-{N}`. No existing content is read, modified, or deleted.

2. **Governed update: non-approved frames only.** Requires all three conditions:
   - The frame's node ID exists in the Evidence Ledger
   - The frame is not marked as approved in the Figma manifest
   - The user provides explicit direction to update

3. **Approved frame update: high consequence.** Requires explicit named confirmation citing the specific frame. This is a high-consequence action regardless of the Work Object's consequence level.

4. **Deletion: prohibited.** No design skill deletes Figma content. Stale pages are the user's responsibility to clean up.

### Naming convention

```
{WO-ID} / {spec-slug} / pass-{N}
```

Example: `2026-07-22-006 / dashboard-overview / pass-1`

The pass number increments per specification per Work Object, providing a full history of renders without overwriting.

## Scope

This decision applies to:

- `render-to-figma` (primary — creates Figma output)
- `apply-design-direction` (produces revision manifests that may target existing frames)
- `connect-design-to-code` (updates component mappings but does not modify canvas content)

This decision does not apply to:

- Figma operations performed directly by the user outside Work Studio
- Figwright's internal canvas operations when invoked outside Work Studio
- Reading Figma content (reads are unrestricted)

## Rationale

**Always-new preserves design history.** Each render is a snapshot tied to a specific Work Object, specification, and pass. Reviewers can compare passes side-by-side. Nothing is lost to overwriting.

**Approved frame protection prevents accidents.** An approved frame represents a reviewed, accepted design. Modifying it should be as deliberate as modifying production code — hence high-consequence authority regardless of the Work Object's consequence level.

**Deletion prohibition is simple and safe.** Figma pages are cheap. The risk of accidentally deleting approved or in-review designs far outweighs the cost of accumulating stale pages. Users who want to clean up can do so directly in Figma with full context about what to keep.

**The naming convention enables traceability.** Given a Figma page name, anyone can find the Work Object, specification, and pass that produced it. Given a Work Object, the Figma manifest lists all pages and their approval status.

## Alternatives Considered

### Update-in-place by default

Each render updates the existing page for that specification, keeping only the latest version.

Rejected because: update-in-place destroys design history. A reviewer cannot compare the current render against a previous pass. If a render introduces a regression, the previous version is gone. Figma's version history provides some mitigation, but it's less granular and harder to navigate than named pages.

### Soft-delete with archive pages

Instead of prohibiting deletion, move stale pages to an archive section within the Figma file.

Rejected because: archive management adds complexity (naming, organization, cleanup of the archive itself) without significant benefit over the simpler prohibition. Users can archive manually if they want to; automated archiving risks moving content the user still needs.

### Pass-limited retention (keep last N passes)

Keep the most recent N passes per specification, deleting older ones automatically.

Rejected because: automated deletion of any kind violates the preservation principle. A pass that looks obsolete today may be the only record of an important design exploration. The cost of keeping extra pages is near zero; the cost of losing a needed page is high.

## Consequences

**Positive:**
- Full render history preserved — every pass is available for comparison
- Approved designs are protected from accidental modification
- Clear traceability from Figma pages back to Work Objects and specifications
- Simple rule — "always new" is easy to understand and implement

**Negative:**
- Figma files accumulate pages over time — users must clean up manually
- If stale page accumulation becomes a significant problem (revisit trigger), a cleanup mechanism may be needed
- The high-consequence gate for approved frame updates may slow iteration when rapid changes to approved designs are needed

**Neutral:**
- The naming convention adds structure to Figma files that may or may not match the user's organizational preferences
- Deletion prohibition applies only to skills — users retain full Figma deletion capability

## Deferral record

### 2026-07-23 — Grilling Session 13: Deferred

**Authority:** DEC-A2 (workflow is NL → agent → code → browser), Grilling
Session 13 (14 accepted decisions)

**Reason:** No Figma output exists or is planned. The always-new write policy
concept is partially preserved in the review layer's branch model — each
design alternative is a separate git branch, not an overwrite of existing
state. The Figma-specific naming convention and write policy tiers are
deferred.

**Revisit trigger:** Figma output becomes a real requirement. At that point,
the always-new principle should be reassessed against the review layer's
branch-based model.

**Full plan:** `docs/design/local-first-design-review-layer-plan.md`
