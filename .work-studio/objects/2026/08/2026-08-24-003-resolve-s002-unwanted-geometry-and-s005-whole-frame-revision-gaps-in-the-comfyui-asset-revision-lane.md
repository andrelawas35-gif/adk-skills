---
schema_version: 1
id: 2026-08-24-003
title: Resolve S002 unwanted-geometry and S005 whole-frame revision gaps in the ComfyUI asset revision lane
type: change
status: active
state: design
consequence: meaningful
sensitivity: ordinary
domain: [engineering]
created_at: 2026-08-24T21:59:40Z
updated_at: 2026-08-24T22:00:15Z
next_action: Route to alawas-design-design-tracer-bullet: scope the smallest next test for S002 (e.g. higher cfg 3.5-4.0, or post-hoc artifact masking) and/or S005 (e.g. no-mask img2img, or Redux-style identity preservation combined with full denoise).

---
## Intent

Spun off from the closed `2026-08-23-007` (Make ComfyUI V0 revision lane
produce observable critique-directed changes), which resolved 2 of 4 tested
asset-revision flaw categories cleanly (background-clutter via segmentation
masking, turnaround-identity via 3D mesh generation) and closed with those
two categories verified. This Work Object owns the remaining two open gaps:

1. **S002 (object material/style revision)** produces an unrequested
   frosted-glass diffuser/bell shape alongside the correct material fix,
   persisting across four attempts at varying cfg and negative-conditioning
   strength.
2. **S005 (whole-frame rendering-style consistency)** has no working
   denoise/mask combination yet -- attempts either leave a photoreal/painterly
   style seam, destroy the asset's identity at full denoise, or crash to a
   blank image at partial denoise.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [ ] S002: a revision run on the market-lamp asset changes only material/color
      as requested, with no unrequested new geometry (glass shade, dome,
      diffuser, or any other added part) visible in the result.
- [ ] S005: a revision run on the market-lamp asset achieves fully consistent
      photorealistic rendering across the *entire* frame (object and
      background), without destroying the asset's original composition/identity
      and without producing a degenerate/blank output.
- [ ] Both fixes are recorded with exact node graph, model, denoise/guidance/
      seed values, and prompts, repeatable on the installed RTX 3080 10 GB
      system.

## Constraints and non-goals

**Constraints:**
- Continue using the local Flux (`flux1-krea-dev_fp8_scaled.safetensors`)
  pipeline already validated in the parent WO unless a specific test requires
  swapping engines (as `2026-08-23-007` Decision 14 did, and rejected).
- Ground every new attempt in the parent WO's already-falsified approaches
  (Decisions 12-23) -- do not re-test a combination already shown not to work
  without a genuinely new variable.

**Non-goals:**
- Reopening the two already-closed, verified flaw categories (background-
  clutter, turnaround-identity) from `2026-08-23-007`.
- Building a general-purpose fix for every possible revision-lane flaw type --
  scoped strictly to these two named residual gaps.

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
### 2026-08-24T22:00:15Z — Created as spin-off from closed WO 2026-08-23-007; transitioned directly to design (residual problems already characterized, no fresh exploration needed)

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** Director: 'close it now and spin off S002/S005 separately.' Both gaps are already well-characterized with specific falsified approaches (Decisions 17-23 of the parent WO), so this doesn't need fresh signal-classification/exploration -- it can go straight to scoping the next tracer bullet for each.
