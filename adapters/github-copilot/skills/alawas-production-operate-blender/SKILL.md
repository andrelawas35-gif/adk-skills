---
name: alawas-production-operate-blender
description: "Use when a bounded Blender operation must execute against a local scene; rejects arbitrary Python and never bypasses protect or GPU gates."
default_tier: high
platform: github-copilot
---
# Operate Blender (bounded)

## Governing principle

Blender owns spatial truth. Creative reasoning proposes; the bounded operator
executes deterministic operations; the director establishes canon. The
operator never makes a creative decision, and creative reasoning never bypasses
tool governance. Every command is a durable, inspectable file artifact so a
crash mid-operation leaves a recoverable record instead of an ambiguous one
(WO `2026-08-23-002` TDR evidence).

## Boundaries and non-goals

This skill does:

- Accept structured scene operations through a file-based command queue
  (`CMD-<id>.json` → bounded execute → `result-<id>.json`), crash-durable and
  replay-safe across a Blender restart.
- Execute the bounded §4.2 tool surface: scene/object, camera/light,
  rig/animation, mesh cleanup, material, image, and render preview/final.
- Enforce `protect` fields from Shot/Scene Work Objects before any mutating
  command — a command whose target is protected is rejected before touching
  the scene.
- Claim the GPU slot via the COMP-041 file-backed registry (WO `2026-08-24-013`)
  before VRAM-heavy operations (render, import, texture) and release after,
  preserving sequential-VRAM discipline.
- Report every command result (success data or structured error) as a durable
  result file keyed by the same command ID.

This skill does not:

- Make creative decisions, choose camera angles, select assets, or evaluate
  composition.
- Execute arbitrary Blender Python (`execute_blender_python`) without an
  explicit director authority record (`authority.granted_by: 'director'` +
  `work_object`) — a high-consequence escalation (WO `2026-08-23-001` §4.2).
- Skip the `protect` check, claim the GPU concurrently with another operator,
  schedule or prioritize work, or decide what to render.
- Sculpt, groom hair, simulate cloth, or perform other unlisted operations.
- Operate standalone — it is always called by Layer 2/3 production skills
  through the conductor.

## Inputs and preconditions

**Required input:** a structured command naming a bounded operation and its
parameters, plus (for mutating ops) the `protect` set from the governing
Shot/Scene Work Object and (for VRAM ops) the accepted GPU claim path. For
`execute_blender_python`, an explicit director authority record naming the
approving Work Object.

**Preconditions:** a running Blender session with the add-on registered (or a
headless subprocess), the queue directory readable/writable, and the GPU
registry (COMP-041) available when a VRAM op is requested. Missing authority,
a missing `protect` declaration for a mutation, or an unaccepted GPU claim are
explicit gaps, not permission to proceed.

## Required capabilities

- `terminal_run` — launch/query the headless Blender subprocess and run the
  crash-durability tracer.
- `file_read` and `file_write` — command/result files in the queue directory,
  and the file-backed GPU claim registry.
- `background_processes` — keep the persistent Blender polling session alive
  while commands are processed.
- `user_confirmation` — obtain scoped director authority for the
  `execute_blender_python` escalation and any GPU claim that would preempt a
  live owner.
- `structured_output` — report bounded command results and governance
  rejections.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Executing read-only bounded commands on the local scene is allowed within an
  activated production Work Object.
- Mutating commands, `execute_blender_python`, GPU claims that would preempt a
  live owner, imports, and renders require the owning production skill and any
  scoped authority it carries.
- For a high-consequence Work Object, confirmation must name the exact proposed
  mutation. Do not stage, annotate, change status, append History, or make any
  other mutation before that confirmation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full. Outside explicit grilling,
nominate a Candidate only when a proposed command crosses a material authority
boundary (arbitrary Python, preempting a live GPU owner) or the tool surface
would need an unaccepted expansion.

## Skill Grilling Profile

Apply the `alawas-production-operate-blender` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge bounded-surface containment,
protect-field enforcement, GPU claim discipline, crash-replay behavior, and
whether the executor stays deterministic.

## Stage workflow

1. Receive a structured command through the queue; validate the command ID
   scheme (`CMD-<nonce8>-<seq4>`).
2. Run the governance gates: `execute_blender_python` authority check, then
   `protect` enforcement for mutating ops.
3. For VRAM ops, claim the GPU slot via the COMP-041 registry (`owner:
   'blender'`); if a live owner holds the slot, return `gpu_occupied` rather
   than preempting.
4. Execute the bounded handler; write a durable `result-<id>.json` ack
   (status/data/error) atomically.
5. Release the GPU slot after VRAM work. Report the result to the conductor;
   never claim deployment or canon approval.

## Evidence rules

- Apply `references/EVIDENCE-MODEL.md`; command files, result files, GPU
  registry state, and tracer output are `[system]`.
- Director authority records and accepted protect sets are `[decision]`.
- Boundary/containment judgments are `[inference]` unless recorded.
- Missing protect declarations, unaccepted GPU claims, and rejected authority
  are `[gap]` — reported, never silently bypassed.

## Integration points

- Queue contract and command-ID scheme: `tools/production/blender_operator/queue_schema.md`.
- Queue logic: `tools/production/blender_operator/queue.py`.
- Governance gates: `tools/production/blender_operator/governance.py`.
- Full bounded executor: `tools/production/blender_operator/executor.py`.
- bpy add-on wiring: `tools/production/blender_operator/addon.py`.
- GPU claim registry (COMP-041): `tools/production/gpu_orchestrator/registry.py`.
- Parent spec: `2026-08-23-001-production-skill-architecture-implementation-plan.md` §3.1; WO `2026-08-24-014`; component COMP-042.
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Epistemic rules

This skill uses the **full 6‑tag system** (`references/epistemic/epistemic-rules-full.md`).

The epistemic tier is resolved from the skill's `default_tier` (high).
**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the epistemic tier is upgraded to at least `medium` (essential 3‑tag).
When `consequence: high`, the epistemic tier is upgraded to the strongest
available tier (full 6‑tag).
`actual_epistemic_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

For a high-consequence Work Object, confirmation must name the exact
proposed mutation. Do not stage, annotate, change status, append History,
or make any other mutation before receiving that scoped confirmation.

### Model tier

This skill declares `default_tier: high`.
The platform overlay resolves this to `claude-sonnet-4-20250514`.
The prompt budget for this tier is approximately 80000 tokens (advisory).

**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the effective tier is upgraded to at least `medium`. When `consequence: high`,
the effective tier is upgraded to the strongest available model.
`actual_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `terminal_run` | `run_in_terminal` | native |
| `file_read` | `read_file` | native |
| `file_write` | `create_file / replace_string_in_file / multi_replace_string_in_file` | native |
| `background_processes` | `—` | manual-fallback |
| `user_confirmation` | `conversation turn` | native |
| `structured_output` | `—` | native |

### Capability Degradation

Apply `references/CAPABILITY-DEGRADATION.md`. Per-capability
classifications and notes below.

#### `background_processes` (manual-fallback)

- **Behavior**: Pause and give one concrete manual instruction.
- **Record**: Append History entry noting the capability gap, the
  manual action taken, and what remains unverified.
- **Note**: GitHub Copilot does not support persistent background processes across tool calls. Start services manually or use a separate terminal.
