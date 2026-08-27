---
schema_version: 1
id: 2026-08-22-035
title: Recommend skills to comfortably work with Claude Design, tied to asset management
type: inquiry
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-22T19:58:49Z
updated_at: 2026-08-22T20:03:45Z
next_action: Director selects which recommendation(s), if any, to advance. Smallest first step: the registry schema's external-reference field.



---
## Intent

Recommend additional skills needed to comfortably work with Claude Design
(the connected `DesignSync` MCP tool, confirmed authenticated this session
with 2 writable projects), explicitly tied to the studio's existing design
asset management (`design-manage-assets`, `.work-studio/design-assets/*.asset.md`,
`asset-workbench.html`). Grounded in a structural investigation: only two
skills (`design-apply-design-direction` Path B, `design-verify-design-implementation`)
mention Claude Design at all, and five separate places in the pipeline name
"external design tool sync" as a gated action with no named owner.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] Standalone report deliverable produced under `.work-studio/deliverables/`,
      each recommendation attributed to a verified structural gap
- [x] Recommendations explicitly distinguish "needs a new skill" from "needs
      a schema extension to an existing skill" rather than inflating every
      gap into a new skill
- [x] Recommendations are explicitly tied to asset management (the registry
      schema and `design-manage-assets`' routing table), per the request
- [ ] Director selects which recommendation(s), if any, to advance into their
      own Work Object(s)


## Constraints and non-goals

**Constraints:**
- Report synthesizes structural evidence only; authors no new architecture and
  accepts no recommendation on the director's behalf.

**Non-goals:**
- Building any recommended skill or schema change — each is a pending
  recommendation, not an accepted decision.
- Creating or linking any real Claude Design project to a real asset record
  — no real asset currently has a Claude Design presence to demonstrate
  against (carried as a gap in the deliverable).

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — <summary>

| Field | Value |
|-------|-------|
| **Decision type** | decision / authority / delegation |
| **Result** | pass / fail / pending |
| **Scope** | <!-- what this decision applies to --> |
| **Authorization** | <!-- who or what authorized this --> |
| **Confidence** | <!-- high / medium / low, plus basis. Scope-qualify when the decision's parts differ: 'high for <X>; low for <Y> — basis: <why>' --> |
| **Actor** | <!-- who made the decision --> |
| **Revisit trigger** | <!-- condition that would cause reconsideration --> |
| **Rationale** | <!-- why this decision was made --> |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | design-apply-design-direction/SKILL.md:58,149-169; design-verify-design-implementation/SKILL.md:117 | Only two skills mention Claude Design at all: apply-design-direction (Path B execution) and verify-design-implementation (optional visual comparison, subordinate to browser evidence). |
| [system] | design-build-design-foundation/SKILL.md:35; design-compose-design-system/SKILL.md:166; design-govern-interaction-motion/SKILL.md:223; design-steward-experience-patterns/SKILL.md:166; DESIGN-ASSET-PIPELINE.md:71; design-manage-assets/SKILL.md | Five+ separate places name "external design tool sync" as excluded/gated with no named owner -- design-manage-assets explicitly requires "the owning specialist" for this action but names none in its own 7-entry routing table. |
| [system] | references/DESIGN-ASSET-REGISTRY.md Required Fields; apply-design-direction's [system:design-project-ref] format | The asset registry schema has no field for an external provider reference; a Claude Design project link currently lives only in Work Object evidence, disconnected from the canonical asset record asset-workbench.html and design-manage-assets both treat as authoritative. |
| [system] | DesignSync tool description (this session) | Confirms a required method order (list/read -> finalize_plan -> write/delete) with a mandatory human-review checkpoint at finalize_plan; no skill documents this sequence as its own stage workflow. |
| [system] | .work-studio/deliverables/2026-08-22-035-claude-design-integration-skills.md | Full report deliverable (linked via Artifacts). |
| [gap] | ws transition audit (verify) | No decision record with result: pass and populated scope found. Requirement coverage evidence is expected before verify transition. |
| [decision] | director: 'I want to work with claude design using my skills not in the actual claude design so it could be agent agnostic and globally' | Confirmed constraint, refining Recommendation 2: the local .work-studio/design-assets/*.asset.md record must remain the sole canonical asset truth, readable/actionable by every platform adapter (claude-code, codex, github-copilot) with zero dependency on a live Claude Design connection. Claude Design is always an optional export/import destination via the proposed design-sync-claude-design skill, never a second source of truth -- mirrors the Path A (agent-agnostic default) vs Path B (capability-gated, explicitly-degrading) posture apply-design-direction already uses. Deliverable's Recommendation 2 section updated to state this explicitly rather than leaving it as inference. |
## Open questions

- Which recommendation(s), if any, does the director advance? (Recommendation
  1 -- the registry schema extension -- is the smallest, lowest-risk first
  step; Recommendation 2 -- the new sync skill -- is the larger piece.)
- Should a real Claude Design project (e.g. "Modernist" or "Reclaim Design
  System", both confirmed accessible this session) be used as the first real
  test case if any recommendation advances, closing the "no real asset has a
  Claude Design presence yet" gap?

## Next move

Director selection. No skill or schema change is built from this report;
each recommendation advances only if the director opens a Work Object for
it. The smallest, lowest-risk candidate to advance first is Recommendation
1 (the registry schema's external-reference field).

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T20:01:09Z — Report deliverable produced and linked; awaiting director selection

- **State:** verify
- **Status:** active
- **Actor:** claude-code
- **Rationale:** alawas-research-produce-report produced a report-type deliverable recommending a registry schema extension (external-reference field), a new design-sync-claude-design skill (owning the mechanical DesignSync method sequence and a new external-design-sync frontier), and wiring that frontier into design-manage-assets' routing table. Each is attributed to a verified structural gap (5+ places naming external design tool sync as gated with no owner; the asset registry schema having no external-provider field). Nothing built; recommendations advance only on director selection.
## artifacts

- `.work-studio/deliverables/2026-08-22-035-claude-design-integration-skills.md` (fingerprint: `972ac198f527`, commit: uncommitted at record time) — Report: skills/schema needed to work with Claude Design, tied to asset management
