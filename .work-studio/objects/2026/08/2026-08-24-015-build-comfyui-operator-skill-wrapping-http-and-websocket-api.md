---
schema_version: 1
id: 2026-08-24-015
title: Build ComfyUI operator skill wrapping HTTP and WebSocket API
type: change
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [production]
created_at: 2026-08-25T01:56:52Z
updated_at: 2026-08-25T03:17:02Z
next_action: Select or create a minimal ComfyUI smoke workflow, then run workflow.submit and workflow.await_output against localhost:8188 while observing COMP-041 claim/release from idle to comfyui_flux_loaded or comfyui_hunyuan_loaded and back to idle.









---
## Intent

Wrap the ComfyUI HTTP/WebSocket API (localhost:8188) as a skill. Submits
workflow JSON, polls queue, retrieves output images and meshes. Handles model
loading/unloading (Flux Dev FP8, Hunyuan3D-2) within the 10 GB VRAM budget.

Parent: WO `2026-08-23-001` §5.3, §5.4. Component: COMP-043.

## Success evidence

- [x] Can submit a ComfyUI workflow JSON and poll for completion
- [x] Can retrieve output images and meshes from completed jobs
- [x] Can list available checkpoints and LoRAs
- [x] Claims GPU via `production-orchestrate-gpu` (`2026-08-24-013`) before loading models
- [x] Handles Flux Dev FP8 and Hunyuan3D-2 model loading/unloading


## Constraints and non-goals

**Constraints:**
- Connects to existing ComfyUI on `:8188`, does not manage the server
- Must claim/release GPU through `2026-08-24-013` protocol
- Model-agnostic: any model behind ComfyUI satisfies (Decision 2)

**Non-goals:**
- No style selection or workflow design (Layer 2 decisions)
- No ComfyUI server management or installation

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Accepted bounded slice: ComfyUI GPU claim wiring

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Smallest ComfyUI integration slice for COMP-043: create or update the local `production-operate-comfyui` operator wrapper so GPU-heavy ComfyUI workflow/model operations claim the COMP-041 file-backed GPU registry as owner `comfyui_flux` or `comfyui_hunyuan`, reject when another live owner holds the GPU, and release the claim after completion or failure. Verification may use mocked localhost HTTP; no live ComfyUI server or real model load is required for this slice. |
| **Authorization** | Director request in current conversation: "wire ComfyUI's GPU claim (`2026-08-24-015`)." Local workspace implementation only; no external deployment, no ComfyUI server management, no live production render implied. |
| **Confidence** | medium-high — grounded in verified COMP-041 registry behavior and the Blender integration pattern; live ComfyUI API behavior remains a verify/release-evidence gap until exercised against `localhost:8188`. |
| **Actor** | director |
| **Revisit trigger** | Reopen if mocked API wiring passes but live ComfyUI does not preserve claim/release around the actual queued job lifetime, or if Flux/Hunyuan model ownership cannot be inferred or supplied explicitly by the caller. |
| **Rationale** | WO `2026-08-24-015` already requires GPU claim/release through `2026-08-24-013`, and WO `2026-08-24-013` has routed ComfyUI as the next downstream integration after Blender. This slice proves the claim boundary without expanding into workflow design, server management, or real model execution. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | production-operate-comfyui GPU claim implementation | Implemented the bounded production-operate-comfyui GPU claim wiring for COMP-043: tools/production/comfyui_operator/client.py wraps local ComfyUI HTTP operations, workflow.submit claims owner comfyui_flux or comfyui_hunyuan through the COMP-041 registry before POST /prompt, workflow.await_output releases after completion, interrupt/timeout/submission failure release claims, competing live owners fail before any ComfyUI HTTP call, read-only model listing does not claim GPU. Added skills/core/production-operate-comfyui/SKILL.md, registered production-operate-comfyui in component_governance, kernel-manifest, skill-map, component-ledger COMP-043, generated adapters, and installed the Codex project-pinned adapter. |
| [system] | verification commands for ComfyUI GPU claim wiring | Focused verification passed: pytest tests/test_comfyui_operator_gpu_wiring.py tests/test_gpu_orchestrator.py returned 13/13 passing; unittest tests.test_component_governance returned 4/4 passing; tools.ws skill-map build generated 47 skills including production-operate-comfyui; tools/generate-adapters.py --check reported all generated files match and alawas-production-operate-comfyui is present for Codex, Claude Code, and GitHub Copilot. tools.ws validate ledger still reports only pre-existing COMP-001 grill staleness; tools/verify-kernel.py still reports pre-existing undeclared design skill files unrelated to COMP-043. |
| [gap] | verification scope boundary after ComfyUI GPU claim wiring | Live ComfyUI integration remains unverified in this slice: no request was sent to a running localhost:8188 server, no real Flux Dev FP8 or Hunyuan3D-2 workflow was queued, and no real output image/mesh was retrieved. The next verify step should run a small live workflow or explicitly bound the absence of a running server while observing COMP-041 claim/release across the queued job lifetime. |
| [gap] | ws transition audit (verify) | Unresolved [gap] entries exist in the Evidence ledger. Residual uncertainty should be reviewed before proceeding. |
| [system] | ComfyUI bounded tool surface coverage | The implemented ComfyUI client covers the checked success-evidence surface at contract-test level: workflow.submit, workflow.queue_status, workflow.get_output, workflow.await_output, workflow.interrupt, model.list_checkpoints, model.list_loras, model.get_loaded via COMP-041 registry state, output.get_images, and output.get_mesh. output.save_to remains explicitly unimplemented until caller-owned file materialization is specified. |
| [system] | verify-release-evidence (2026-08-25): ComfyUI GPU claim wiring | Verification rerun passed within the bounded slice: pytest tests/test_comfyui_operator_gpu_wiring.py tests/test_gpu_orchestrator.py returned 13/13 passing; unittest tests.test_component_governance returned 4/4 passing; tools/generate-adapters.py --check reported no drift with alawas-production-operate-comfyui present in all adapters. Live local ComfyUI dependency was reachable at http://127.0.0.1:8188: /queue returned HTTP 200 with empty queue, the bounded client listed 2 checkpoints and 1 LoRA through /object_info, and the COMP-041 registry remained idle for read-only model/queue operations. |
| [gap] | verify-release-evidence boundary: live queued workflow | Still unverified: a live queued ComfyUI workflow that holds COMP-041 from workflow.submit through actual completion and releases on workflow.await_output. Existing repo workflow JSONs appear to be real visual workflows, not a designated smoke fixture, so verification did not submit them under this route. Next safe check: choose or create a minimal smoke workflow and run it against localhost:8188 while observing gpu-claim-state.json before submit, during queue, and after completion. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-25T03:09:09Z — Accepted ComfyUI GPU claim wiring slice

- **State:** build
- **Status:** active
- **Actor:** codex
- **Rationale:** Director requested wiring ComfyUI's GPU claim for 2026-08-24-015. Decision 1 records the bounded implementation scope: wrap GPU-heavy ComfyUI workflow/model operations with COMP-041 claim/release using owner comfyui_flux or comfyui_hunyuan, preserve localhost API boundary, and verify with mocked HTTP tests without live server management.
### 2026-08-25T03:13:58Z — Wired ComfyUI GPU claim integration

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Implemented the accepted bounded slice for COMP-043: production-operate-comfyui wraps local ComfyUI workflow/model operations and claims/releases COMP-041 as comfyui_flux or comfyui_hunyuan around GPU-heavy queued work, with mocked HTTP tests proving claim, release, occupied-owner blocking, submit-failure release, read-only model listing, and output metadata paths.
### 2026-08-25T03:17:02Z — Verified ComfyUI GPU claim wiring evidence

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Release-evidence verification reran the focused ComfyUI/GPU tests, component governance tests, adapter drift check, and a live read-only localhost:8188 dependency probe. Local contract evidence passed and ComfyUI was reachable for queue/model-list endpoints; live queued workflow claim/release remains intentionally unverified pending a designated smoke workflow or explicit render authority.
