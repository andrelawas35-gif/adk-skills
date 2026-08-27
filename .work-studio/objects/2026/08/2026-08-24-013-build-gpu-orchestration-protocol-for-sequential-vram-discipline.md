---
schema_version: 1
id: 2026-08-24-013
title: Build GPU orchestration protocol for sequential VRAM discipline
type: change
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [production]
created_at: 2026-08-25T01:56:50Z
updated_at: 2026-08-25T02:49:52Z
next_action: Integration routed to 2026-08-24-014 for Blender GPU claim wiring. Keep 2026-08-24-015 ComfyUI GPU claim wiring as the next downstream integration after Blender.













---
## Intent

Enforce sequential VRAM discipline on the RTX 3080 (10 GB). Only one
GPU-heavy process (Blender, ComfyUI Flux, ComfyUI Hunyuan3D) runs at a time.
Operators claim and release the GPU through this protocol. Prevents the TDR
driver crashes evidenced in WO `2026-08-23-002`.

Parent: WO `2026-08-23-001` §2.4 (GPU time-share). Component: COMP-041.
Deliverable: `2026-08-23-001-production-skill-architecture-implementation-plan.md` §4.2.

## Success evidence

- [x] VRAM state machine documented (idle / blender_loaded / comfyui_flux_loaded / comfyui_hunyuan_loaded)
- [x] Claim/release protocol enforces at-most-one GPU process
- [ ] Tool operators (`2026-08-24-014`, `2026-08-24-015`) can check in/check out
- [x] Concurrent claim attempts are queued or rejected, never silently concurrent


## Constraints and non-goals

**Constraints:**
- Protocol, not scheduler — does not decide what to render or prioritize jobs
- Must handle unclean release (process crash) without permanent lock
- Must be queryable (what is currently loaded?)

**Non-goals:**
- No job scheduling or priority queue
- No multi-GPU support (single RTX 3080)

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Accepted tracer design: file-backed GPU claim registry (2026-08-25T02:40:56Z)

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Smallest tracer for COMP-041: a local file-backed GPU claim registry with one JSON state file, atomic query/claim/release operations, stale-owner recovery, and simulated Blender/ComfyUI claim attempts. Entry state is IDLE; resulting state is either a visible owner transition or a rejected/queued competing claim. No real GPU process launch, no job scheduling, no Windows TDR changes, no multi-GPU support, and no real Blender/ComfyUI integration in this tracer. |
| **Authorization** | User accepted the proposed tracer design in conversation: "accept this tracer design". Local workspace-only implementation authority; no external writes, deployment, registry edits, or real GPU process control implied. |
| **Confidence** | medium-high for proving the protocol invariant locally; lower for real operator integration until 2026-08-24-014 and 2026-08-24-015 call the protocol — basis: the tracer directly tests at-most-one ownership, stale-owner recovery, and queryability, but uses simulated operators rather than live Blender/ComfyUI processes. |
| **Actor** | user, codex |
| **Revisit trigger** | Revisit if tests allow two simultaneous owners, stale-owner recovery can steal a live owner, atomic file operations are unreliable on the local filesystem, or real Blender/ComfyUI integration requires a daemon or scheduler. |
| **Rationale** | The riskiest assumption is that Work Studio can enforce sequential VRAM discipline without building a scheduler. A file-backed claim registry is the smallest reversible path that can prove the invariant, preserve crash recovery, and give operator skills a narrow check-in/check-out contract. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | .work-studio/deliverables/2026-08-23-001-production-skill-architecture-implementation-plan.md §4.2 | COMP-041 is defined as a GPU execution graph/protocol for the VRAM time-share: one state at a time (IDLE, BLENDER_LOADED, COMFYUI_FLUX_LOADED, COMFYUI_HUNYUAN_LOADED), claim/release transitions, and no concurrent claims. |
| [system] | .work-studio/objects/2026/08/2026-08-23-002-define-local-ai-animation-studio-model-architecture.md | The parent local AI animation studio record contains system-log evidence of two VIDEO_TDR_TIMEOUT_DETECTED_FAILURE crashes on 2026-08-24 during or near active local-generation test windows, making sequential GPU discipline a concrete reliability control rather than a preference. |
| [gap] | ws transition audit (build) | No decision record with result: pass found at build transition. An accepted decision record is expected before entering build state. |
| [system] | tools/ws/sections.py parse_decisions_table; WO 2026-08-24-013 Decision 1 | The build-transition audit gap was caused by the decision heading not matching the parser's required '### Decision N' shape. Decision 1 was reformatted to the structured decision heading while preserving the accepted scope and user authorization. |
| [system] | tools/production/gpu_orchestrator/registry.py; tests/test_gpu_orchestrator.py | Implemented bounded tracer for COMP-041 as a local file-backed GPU claim registry with query, claim, release, stale-owner recovery, and at-most-one simulated owner tests. Real Blender/ComfyUI process integration remains outside this tracer. |
| [system] | uv run --python 3.11 python -m pytest tests/test_gpu_orchestrator.py -q; uv run --python 3.11 python -m pytest tests/test_blender_operator_queue.py -q | Focused verification passed: GPU orchestrator tests 7/7 and neighboring Blender operator queue tests 9/9. Tests cover idle query, claim/release, live competing-claim rejection, same-owner refresh, stale-owner recovery, wrong-owner release rejection, and parallel claims granting at most one owner. |
| [gap] | ws transition audit (verify) | Unresolved [gap] entries exist in the Evidence ledger. Residual uncertainty should be reviewed before proceeding. |
| [system] | verification rerun: pytest tests/test_gpu_orchestrator.py; pytest tests/test_blender_operator_queue.py; ad hoc boundary probe | Release-evidence verification for the bounded tracer passed within scope: GPU orchestrator tests 7/7, neighboring Blender queue tests 9/9, invalid owner is rejected, wrong-owner release is blocked with owner_mismatch, and the state file contains only schema/state/owner/owner_id/timing fields. No real GPU process, external system, secret, or production data was accessed. |
| [gap] | verification scope boundary for WO 2026-08-24-013 | Real Blender and ComfyUI operator integration is unverified in this Work Object: 2026-08-24-014 and 2026-08-24-015 have not yet called the GPU claim registry before VRAM operations. This is a downstream integration gap, not a failure of the bounded tracer. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

Route to `alawas-engineering-verify-release-evidence` for the bounded tracer: confirm the file-backed GPU registry implementation and test evidence, while keeping real Blender/ComfyUI operator integration as an open downstream gap.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-25T02:39:03Z — Activated GPU protocol design

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** User resumed the active Work Object by ID; evidence shows COMP-041 is a defined protocol dependency for Blender/ComfyUI operators and TDR crash evidence makes sequential VRAM discipline necessary before operator integration.
### 2026-08-25T02:41:22Z — Recorded accepted tracer design

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted the proposed file-backed GPU claim registry tracer for COMP-041; decision records the invariant, scope, limits, rollback, and route to bounded implementation.
### 2026-08-25T02:42:26Z — Routed accepted GPU protocol tracer to implementation

- **State:** build
- **Status:** active
- **Actor:** codex
- **Rationale:** User explicitly routed the accepted COMP-041 tracer to implementation; the decision section contains a pass result and scope for the file-backed GPU claim registry.
### 2026-08-25T02:45:27Z — Implemented bounded GPU claim registry tracer

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Implemented the accepted local file-backed GPU claim registry and executed focused tests proving query, claim, release, stale-owner recovery, and at-most-one simulated owner behavior.
### 2026-08-25T02:48:31Z — Verified bounded GPU claim registry tracer evidence

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Executed proportionate verification for the accepted tracer: focused tests and boundary probe passed within local workspace scope; real Blender/ComfyUI operator integration remains explicitly unverified downstream.
### 2026-08-25T02:49:52Z — Accepted bounded GPU protocol tracer evidence and routed integration

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted the verified COMP-041 bounded tracer evidence and directed routing to integration. First integration target is 2026-08-24-014 because its current next_action explicitly awaits GPU claim wiring via 2026-08-24-013.
