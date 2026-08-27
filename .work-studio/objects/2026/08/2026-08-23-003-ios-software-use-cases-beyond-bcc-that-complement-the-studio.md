---
schema_version: 1
id: 2026-08-23-003
title: iOS software use cases beyond BCC that complement the studio
type: inquiry
status: active
state: explore
consequence: meaningful
sensitivity: ordinary
domain: [ideation, research]
created_at: 2026-08-23T22:25:33Z
updated_at: 2026-08-23T22:26:04Z
next_action: Investigate iOS use cases grounded in director's Blender/ComfyUI/studio workflow

---
## Intent

The director already builds BCC (Blender Camera Controller) — an Android app
that turns a phone into a motion-sensor controller for Blender cameras over
UDP. An iOS/PWA implementation plan exists (`Controller_Addon/.work-studio/
deliverables/bcc-ios-pwa-implementation-plan.md`). The question: what other
iOS software use cases — beyond porting BCC — would genuinely help a creative
director who works locally with Blender, ComfyUI, and a governance-backed
studio? The answer informs what to build next alongside the studio.

## Success evidence

- [ ] At least three genuinely distinct iOS use cases identified, each
      grounded in the director's actual workflow (not generic app ideas)
- [ ] Each use case names the specific gap it fills that no existing tool
      covers well
- [ ] Use cases are separated from BCC — not features that belong inside BCC


## Constraints and non-goals

**Constraints:**
- Use cases must connect to the director's real tools: Blender, ComfyUI,
  the Work Studio, local-first file workflow.
- Prefer ideas that leverage what a phone uniquely offers (sensors, camera,
  portability, always-on) rather than things better done on a desktop.
- Stay within the director's technical reach: Swift/SwiftUI, PWA/React,
  Python (Blender add-ons), local networking.

**Non-goals:**
- Not re-listing BCC features or BCC iOS port tasks (already planned).
- Not building a generic "app ideas" list — only things that solve a real
  gap in the director's own workflow.

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


## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-23T22:26:04Z — Activate inquiry

- **State:** explore
- **Status:** active
- **Actor:** system
- **Rationale:** Director asked what iOS use cases beyond BCC would genuinely help. Moving to explore to investigate grounded in the director's actual workflow.
