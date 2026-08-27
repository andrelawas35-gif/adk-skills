---
schema_version: 1
id: 2026-08-25-010
title: Live operator integration for asset production pipeline (ComfyUI and Blender)
type: change
status: active
state: design
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-26T02:03:19Z
updated_at: 2026-08-27T20:50:51Z
next_action: Install DINOv2-giant CLIP-vision model into ComfyUI and re-run mesh tracer












---
## Intent

Replace the simulated Layer 1 operator calls in the asset production pipeline
(`skills/core/production-operate-asset-pipeline/`) with real live-operator
integrations on both sides:

1. **ComfyUI side** — real ComfyUI Flux workflows for concept art and real
   Hunyuan3D-2 workflows for 3D mesh generation, dispatched through
   `alawas-production-operate-comfyui` with GPU claim discipline.
2. **Blender side** — real mesh cleanup, material assignment, and rigging
   through the actual Blender file-based command queue (`alawas-production-operate-blender`,
   repository addon.py), replacing `BlenderAdapter`'s simulated API calls.

The state-machine lifecycle proven by predecessor WO `2026-08-24-020`
(concept → mesh → cleanup → material → rig → registered, resume-from-state,
retry up to 3x) carries over unchanged; only the operator implementations
change from simulation to live dispatch.

**Successor of:** WO `2026-08-24-020` (closed) — its closing History entry
pre-declared this work: "Next step (live operator integration) is a separate
Work Object."

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] Concept-art stage dispatches a real ComfyUI Flux workflow and returns a real image
- [ ] Mesh stage dispatches a real Hunyuan3D-2 workflow and returns a real 3D mesh
- [ ] Cleanup/material/rig stages execute through the real Blender command queue (CMD/result files)
- [ ] State machine still resumes correctly from a failed live stage
- [ ] GPU claims flow through operators (COMP-041 registry) for VRAM-heavy stages
- [ ] Completed asset registers in `.work-studio/asset-registry.md` as a canonical .blend

## Constraints and non-goals

**Constraints:**
- Must use Layer 1 operators — never call Blender/ComfyUI directly from the pipeline skill
- All ComfyUI submissions go through `alawas-production-operate-comfyui`; all Blender operations go through the file-based command queue
- GPU claims flow through operators, not this pipeline
- The state-machine architecture from Decision 1 of WO `2026-08-24-020` is retained — this is an operator swap, not a redesign

**Non-goals:**
- No changes to the state machine's states, transitions, retry, or persistence design
- No manual sculpting or detailed mesh editing
- No texture painting
- No asset design decisions (director's authority)
- No modification of closed WO `2026-08-24-020` beyond its successor link

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Tracer bullet: real Flux concept-art dispatch through ComfyUIAdapter's existing interface

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Implement a real dispatch path in the pipeline's `ComfyUIAdapter` for the concept-art stage only: submit one trivial Flux prompt via the local ComfyUI HTTP API (`/prompt`, `/history/<id>` at 127.0.0.1:8188), poll to completion, verify a real image file lands in a scratch output directory. The adapter's public interface (submit_job/poll_status/get_result) and the state machine are unchanged; the other five stages stay simulated. |
| **Authorization** | Director accepted, chat 2026-08-26: "accept." |
| **Confidence** | medium — ComfyUI server confirmed live (/system_stats → 200) and operate-comfyui skill verified elsewhere, but no real workflow has ever flowed through this pipeline's adapter seam. |
| **Actor** | director (accept), alawas-design-design-tracer-bullet (design) |
| **Revisit trigger** | If the live submission fails on API shape, auth, or model availability, the failure evidence routes back to design for revision before any other stage is attempted. If it passes, next decision is the Hunyuan3D mesh stage — not automatic. |
| **Rationale** | Tests the riskiest assumption (live dispatch through the adapter seam) with one cheap GPU job; isolates ComfyUI-side risk from Blender-side and state-machine risk. |

### Decision 2 — Mesh-stage tracer: real image-to-3D through the same adapter interface

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | fail |
| **Scope** | Add live dispatch for the `mesh_generation` job type (opt-in `live_mesh_generation=True`, mirroring Decision 1's flag pattern): upload the real concept image from Decision 1's tracer via `/upload/image`, build the Hunyuan3D-2 graph (CLIPVisionLoader sigclip_vision_patch14_384 → CLIPVisionEncode → Hunyuan3Dv2Conditioning → KSampler ~20 steps cfg 1.0 with hunyuan3d-dit-v2 checkpoint → VAEDecodeHunyuan3D → SaveGLB), poll `/history`, download the GLB via `/view` to scratch, verify `glTF` magic bytes. Adapter interface unchanged; state machine unchanged; Blender side untouched. |
| **Authorization** | Director accepted, chat 2026-08-26: "i accept." |
| **Confidence** | medium — all node schemas verified live against /object_info, but the conditioning→sampler→decode chain has never been executed in this environment; mesh gen is a heavier GPU job than concept art. |
| **Actor** | director (accept), alawas-design-design-tracer-bullet (design) |
| **Revisit trigger** | If the GLB is malformed, empty, or the conditioning path errors, evidence routes back to design before the Blender-side tracer. If it passes, next decision is the Blender-side tracer (real command-queue dispatch) — not automatic. |
| **Rationale** | Tests the full concept→mesh seam with a real generated image as input, proving both ComfyUI stages before crossing to the Blender side; keeps each GPU-heavy risk isolated per stage. |

### Decision 3 — Mesh-stage recovery: install DINOv2-giant clip-vision model

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Download and install DINOv2-giant CLIP-vision model into ComfyUI `models/clip_vision/` to resolve the 1536-dim conditioning mismatch. Re-run mesh tracer after installation. |
| **Authorization** | Director selected Option 1, chat 2026-08-27 |
| **Confidence** | high — adapter seam proven, failure is a single missing model file, not a design flaw |
| **Actor** | director |
| **Revisit trigger** | If model installation fails or the re-run produces a different error, evidence routes back to design |
| **Rationale** | Lowest-risk recovery: the adapter code works correctly, the only gap is a server-side model file. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | skills/core/production-operate-asset-pipeline/tracer_bullet.py, full_pipeline.py, adapters/tracer_bullet.py; WO 2026-08-24-020 evidence ledger | Predecessor pipeline verified against SIMULATED operators only: tracer_bullet.py line 127 'Simulate Blender import and cleanup'; adapters/tracer_bullet.py line 181 '# Simulate Blender API call / In production, this would call the actual Blender file-based command queue'. ComfyUI side likewise simulated. Real operator skills exist and are verified elsewhere: alawas-production-operate-comfyui (WO 2026-08-24-015) and alawas-production-operate-blender (WO 2026-08-24-014). This WO's work is the integration seam between them. |
| [gap] | WO 2026-08-25-006 (closed) and WO 2026-08-25-007 full read, 2026-08-26 | Overlap audit: WO 2026-08-25-006 ('Integrate asset pipeline with live ComfyUI and Blender operators') shares this WO's intent but closed after only a SIMULATED adapter-pattern tracer (ComfyUIAdapter submit/poll/get, no real workflow submission); zero of its six live-dispatch success-evidence items were ever checked; its closing entry declares 'Next step (BlenderAdapter, full pipeline integration) is a separate Work Object.' WO 2026-08-25-007 covered the BlenderAdapter piece (also simulation per source). This WO therefore continues the unfulfilled live-dispatch gap, not duplicating completed work. Relationship: successor-of 2026-08-24-020; continuation-of the unchecked remainder of 2026-08-25-006 and 2026-08-25-007. |
| [system] | live_tracer.py run 2026-08-26 against local ComfyUI 0.33.3 at 127.0.0.1:8188; adapters/tracer_bullet.py | Tracer bullet (Decision 1) PASSED. Real Flux1-Krea-dev submission through ComfyUIAdapter uniform interface: POST /prompt accepted workflow (UNETLoader flux1-krea-dev_fp8_scaled + DualCLIPLoader clip_l/t5xxl type=flux + VAELoader ae.safetensors + FluxGuidance 3.5 + KSampler euler/simple cfg=1.0 4 steps 512x512), prompt_id=7f504f3d-3f70-44d0-8f29-f86d14d5faea. Polled /history to completion (~130s). Image fetched via /view to scratch: C:\Users\Andre\AppData\Local\Temp\ws-pipeline-tracer\concept_00001_.png (142388 bytes, nonzero). Independent visual verification: rendered image matches prompt (gray cube on white background) - blurry as expected at 4 steps, but a genuine Flux render. Regression: simulated tracer_bullet.py main() still passes all checks (simulation path untouched, live path opt-in via live_concept_art=True). Note: director corrected model availability mid-design - flux1-krea-dev is installed under UNETLoader (diffusion_models), not CheckpointLoaderSimple; graph built accordingly. |
| [system] | mesh_tracer.py run 2026-08-26, prompt_id=f1d48b8c-7454-40f6-ac9e-466f8cd973d9, /history error record; ComfyUI install at C:\Users\Andre\AppData\Local\Comfy-Desktop\ComfyUI-Installs | Mesh tracer FAILED at real execution (KSampler, node 7): 'mat1 and mat2 shapes cannot be multiplied (729x1152 and 1536x1024)' inside hunyuan3d model cond_in. Diagnosis: sigclip_vision_patch14_384 emits 1152-dim features (729 patches); hunyuan3d-dit-v2's cond_in expects 1536-dim input - the correct CLIP-vision encoder is DINOv2-giant (1536-dim), which is NOT installed (CLIPVisionLoader offers only the one sigclip file). Adapter seam itself performed correctly end-to-end: image upload (/upload/image ok), graph validation passed after two schema fixes (VoxelToMeshBasic VOXEL-to-MESH conversion; LoadImage string path format), submission accepted, poll detected the honest failure via /history status_str=error. Two prior 400s were validation-time schema errors, fixed before execution: (1) VAEDecodeHunyuan3D outputs VOXEL not MESH; (2) LoadImage image input is a string not a list. Missing piece is server-side model availability, not adapter code. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

Route to `alawas-engineering-implement-bounded-change`: install DINOv2-giant CLIP-vision model into ComfyUI `models/clip_vision/`, then re-run mesh tracer to verify the conditioning path works.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-26T02:03:49Z — Created as successor of WO 2026-08-24-020

- **State:** notice
- **Status:** active
- **Actor:** conductor
- **Rationale:** Director authorized creation after orchestrate routing decision. Predecessor WO 2026-08-24-020 closed with pre-declared follow-on: live operator integration. Scope: replace simulated ComfyUI (Flux concept art, Hunyuan3D-2 mesh) and Blender (cleanup, material, rig via file-based command queue) operator calls with real Layer 1 operator dispatch. State-machine design carries over unchanged.
### 2026-08-26T02:07:36Z — Transition notice -> design

- **State:** design
- **Status:** active
- **Actor:** conductor
- **Rationale:** Director instructed next action. Riskiest assumption already identified from evidence ledger (simulated operators never exercised live dispatch); pilot stage already selected (ComfyUI concept-art, one real submission through alawas-production-operate-comfyui). No divergent exploration needed before design-tracer-bullet, mirroring WO 2026-08-25-001's explore->design precedent.
### 2026-08-26T02:08:49Z — Decision 1 recorded: real Flux concept-art tracer bullet accepted

- **State:** design
- **Status:** active
- **Actor:** alawas-design-design-tracer-bullet
- **Rationale:** Director accepted ('accept'). Riskiest assumption: a real ComfyUI Flux submission can flow through the pipeline adapter interface (submit_job/poll_status/get_result) and return a real image. Smallest slice: one trivial Flux prompt via /prompt + /history at 127.0.0.1:8188, image verified in scratch dir. State machine unchanged; other stages stay simulated. Routing to alawas-engineering-implement-bounded-change.
### 2026-08-26T02:22:15Z — Decision 1 verified PASS: real Flux concept-art dispatch through adapter seam

- **State:** design
- **Status:** active
- **Actor:** alawas-engineering-implement-bounded-change
- **Rationale:** Real Flux1-Krea-dev submission through ComfyUIAdapter (live_concept_art=True) returned a real image: prompt_id=7f504f3d-3f70-44d0-8f29-f86d14d5faea, concept_00001_.png (142388 bytes) in scratch, visually verified matching prompt. Riskiest assumption confirmed: live dispatch flows through submit_job/poll_status/get_result unchanged. Simulation path regression-clean. Director corrected model availability: flux1-krea-dev under UNETLoader, used as recorded in evidence. Next decision per Decision 1 revisit trigger: Hunyuan3D mesh stage - not automatic.
### 2026-08-26T04:03:41Z — Decision 2 recorded: mesh-stage tracer accepted

- **State:** design
- **Status:** active
- **Actor:** alawas-design-design-tracer-bullet
- **Rationale:** Director accepted ('i accept'). Riskiest assumption: the full concept-to-mesh seam works live - a real generated image flows into Hunyuan3D-2 and produces a real GLB through the adapter interface. Node surface verified live (CLIPVisionLoader sigclip_vision_patch14_384, Hunyuan3Dv2Conditioning, hunyuan3d-dit-v2 checkpoint, VAEDecodeHunyuan3D, SaveGLB). Opt-in live_mesh_generation flag; uses Decision 1's cube image as input. Routing to alawas-engineering-implement-bounded-change.
### 2026-08-26T04:10:37Z — Decision 2 execution FAILED at conditioning: dimension mismatch, DINOv2 clip-vision model not installed

- **State:** design
- **Status:** active
- **Actor:** alawas-engineering-implement-bounded-change
- **Rationale:** Real Hunyuan3D dispatch executed: upload, submission, polling, and honest-failure detection all worked through the adapter interface. Execution failed in KSampler: sigclip vision features (1152-dim) incompatible with hunyuan3d-dit-v2 cond_in (expects 1536-dim = DINOv2-giant). The required CLIP-vision model file is not installed on the ComfyUI server; installing it is outside the adapter's and this session's scoped authority. Per Decision 2 revisit trigger, evidence routes back to design. Three options for director: (1) authorize installing dinov2 vitg clip-vision into ComfyUI models/clip_vision (server-side change + download, likely fixes conditioning); (2) pivot mesh stage to Meshy API nodes (external service, needs API key); (3) pause mesh stage, run the Blender-side tracer first (independent of this failure).
### 2026-08-27T20:47:03Z — Conductor routing: Decision 2 failure routes back to design, director decision required

- **State:** design
- **Status:** active
- **Actor:** conductor
- **Rationale:** Decision 2 revisit trigger fired: conditioning path errored (sigclip 1152-dim vs DINOv2-giant 1536-dim). Evidence already in design state. Three recovery options identified: (1) install DINOv2-giant clip-vision model, (2) pivot to Meshy API, (3) pause mesh stage and run Blender tracer first. Director must select before work continues. Route to alawas-thinking-pressure-test-decision after selection.
### 2026-08-27T20:50:51Z — Director selected Option 1: install DINOv2-giant model

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Director chose lowest-risk recovery path. Adapter code works; failure is a missing model file. Decision 3 recorded. Routing to implement-bounded-change.
