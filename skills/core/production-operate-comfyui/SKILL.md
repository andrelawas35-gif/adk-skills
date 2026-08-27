---
name: production-operate-comfyui
description: Use when bounded ComfyUI workflow or model operations must run through the local API; claims GPU work and never designs workflows or manages the server.
default_tier: high
---
# Operate ComfyUI

## Governing Principle

ComfyUI is a bounded production tool operator. It executes caller-supplied
workflow/model commands against the local ComfyUI API and owns the diffusion
GPU slot only while that work is active. It does not choose styles, evaluate
visual quality, design workflows, install models, or manage the ComfyUI server.

## Boundaries and non-goals

This skill does:

- Submit caller-provided workflow JSON to the existing local ComfyUI API.
- Poll queue/history and return output metadata for caller-provided prompt IDs.
- List available checkpoints and LoRAs through ComfyUI's read-only object-info
  endpoint.
- Claim the GPU slot via the COMP-041 file-backed registry before GPU-heavy
  Flux/Hunyuan workflow work and release it after completion, timeout,
  interrupt, or submission failure.

This skill does not:

- Choose styles, evaluate visual quality, select models, or design workflows.
- Start, stop, install, update, or repair the ComfyUI server.
- Download, move, delete, or install model files.
- Save outputs to an unspecified destination or silently mutate caller-owned
  production artifacts.

## Inputs and preconditions

**Required input:** a structured ComfyUI operation and parameters. GPU-heavy
workflow submission requires caller-provided workflow JSON and an explicit
model owner: `comfyui_flux` for Flux-family work or `comfyui_hunyuan` for
Hunyuan3D-family work.

**Preconditions:** ComfyUI is already running on `localhost:8188` or an
equivalent caller-specified base URL, the workflow JSON is already designed by
an upstream production skill, and the COMP-041 GPU registry is available.

## Required capabilities

- `web_fetch` — call the local ComfyUI HTTP API on `localhost:8188`.
- `file_read` and `file_write` — read workflow inputs or output metadata as
  directed by the caller and access the file-backed GPU claim registry.
- `gpu_claim` — claim/release the COMP-041 registry for `comfyui_flux` or
  `comfyui_hunyuan`.
- `structured_output` — return prompt IDs, queue status, output metadata, and
  structured errors.
- `user_confirmation` — obtain authority for any operation outside the bounded
  local API surface, such as server management or model installation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when the
operation would cross from bounded local API execution into workflow design,
model installation, server management, output ownership, or GPU-claim policy.

## Skill Grilling Profile

Apply the `production-operate-comfyui` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge workflow ownership, GPU-claim
lifetime, timeout release behavior, model-selection authority, and whether
output materialization remains inside the caller-specified Work Object.

## Implementation

Use `tools/production/comfyui_operator/client.py` for implementation-level
operations. The operator talks to the existing ComfyUI instance at
`localhost:8188` by default.

## Tool Surface

- `workflow.submit(workflow_json, model_owner)`
- `workflow.queue_status()`
- `workflow.get_output(prompt_id)`
- `workflow.await_output(prompt_id)`
- `workflow.interrupt()`
- `model.list_checkpoints()`
- `model.list_loras()`
- `model.get_loaded()`
- `output.get_images(prompt_id)`
- `output.get_mesh(prompt_id)`
- `output.save_to(path)` is intentionally not implemented until output
  materialization ownership is specified by a caller Work Object.

## GPU Claim Discipline

Before GPU-heavy work, claim COMP-041 through
`tools/production/gpu_orchestrator/registry.py`.

- Flux-family work uses owner `comfyui_flux`.
- Hunyuan3D-family work uses owner `comfyui_hunyuan`.
- If another live owner holds the registry, fail with `gpu_occupied` before
  submitting to ComfyUI.
- `workflow.submit` keeps the claim while the queued job runs.
- `workflow.await_output`, completion-aware `workflow.get_output`, timeout,
  submit failure, or `workflow.interrupt` releases the claim.

## Authority

Allowed without additional authority:

- Submit a caller-provided workflow JSON to the local ComfyUI API.
- Poll queue/history for a caller-provided prompt ID.
- List available checkpoints and LoRAs.
- Report output metadata returned by ComfyUI.

Requires a separate Work Object decision:

- Start, stop, install, or modify the ComfyUI server.
- Download, move, delete, or install models.
- Design or materially alter workflow JSON.
- Save outputs into a caller-owned destination not specified by the current
  Work Object.

## Failure Behavior

If GPU claim is denied, do not call ComfyUI. If ComfyUI submission fails after
claim, release the claim before returning the error. If a queued job times out
while awaiting output, release the claim and return the timeout as a verification
gap, not as a successful render.
