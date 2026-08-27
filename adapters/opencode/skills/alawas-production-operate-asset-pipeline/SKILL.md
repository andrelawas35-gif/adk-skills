---
name: alawas-production-operate-asset-pipeline
description: "Use when a 3D asset pipeline must progress from concept to canonical .blend; orchestrates operators and never makes creative decisions."
default_tier: medium
platform: opencode
---
# Operate Asset Pipeline (state machine)

## Governing principle

The asset pipeline sequences Layer 1 operators through a state machine that
tracks progress and enables resume-from-failure. Each stage calls the
appropriate operator; state persists in the Asset Work Object so a crash
mid-pipeline leaves a recoverable record.

## Boundaries and non-goals

This skill does:

- Accept an asset description or concept image as input.
- Run assets through a 6-stage state machine: concept → mesh → cleanup → material → rig → registered.
- Call Layer 1 operators (ComfyUI, Blender) for each stage.
- Track asset state in the Asset Work Object frontmatter.
- Resume from the last successful stage on failure.
- Retry individual stages up to 3 times before marking asset as failed.

This skill does not:

- Make creative decisions (asset design, style, composition).
- Call Blender or ComfyUI directly — always uses Layer 1 operators.
- Register assets in the registry — that is a separate step after pipeline completion.
- Manage GPU claims — that flows through operators via COMP-041.

## Inputs and preconditions

**Required inputs:**
- Asset description (text) or concept image (path)
- Target output path for the canonical .blend file

**Preconditions:**
- ComfyUI operator (COMP-043) is available and verified
- Blender operator (COMP-042) is available and verified
- GPU protocol (COMP-041) is available

## State machine

```
concept → mesh → cleanup → material → rig → registered
```

Each state transition:
1. Calls the appropriate Layer 1 operator
2. Updates the Asset Work Object with the new state
3. Records the operator result in the evidence ledger
4. On failure: increments retry count, retries up to 3 times
5. On3 failures: marks asset as failed, stops pipeline

## Tracer bullet scope (WO 2026-08-24-020 Decision 2)

For the tracer bullet, only 3 stages are tested:
- concept → mesh → cleanup

A simulated failure is injected at the mesh stage to test resume capability.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full. Nominate a Candidate when the
pipeline would cross from state-machine orchestration into creative choice,
direct operator execution, registry mutation, or GPU-claim policy.

## Skill Grilling Profile

Apply the `alawas-production-operate-asset-pipeline` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge resume safety, retry limits,
operator-boundary containment, state persistence, and whether canonical asset
registration remains outside the pipeline.

## Required capabilities

- `file_read` — read Asset Work Object state and caller-provided concept image paths.
- `file_write` — persist Asset Work Object state transitions, retry counts, and operator evidence.
- `terminal_run` — run the tracer bullet and invoke Layer 1 operator commands through their bounded entry points.
- `structured_output` — return state-machine status, retry metadata, output paths, and structured errors.

## Routing and termination

- **Pipeline complete:** route to conductor for registry registration
- **Pipeline failed:** route to conductor with failure evidence
- **Capability gap:** stop and report the gap
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Epistemic rules

This skill uses the **essential 3‑tag system** (`references/epistemic/epistemic-rules-essential.md`).

The epistemic tier is resolved from the skill's `default_tier` (medium).
**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the epistemic tier is upgraded to at least `medium` (essential 3‑tag).
When `consequence: high`, the epistemic tier is upgraded to the strongest
available tier (full 6‑tag).
`actual_epistemic_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

For a high-consequence Work Object, confirmation must name the exact
proposed mutation. Do not stage, annotate, change status, append History,
or make any other mutation before receiving that scoped confirmation.

### Model tier

This skill declares `default_tier: medium`.
The platform overlay resolves this to `anthropic/claude-sonnet-4-20250514`.
The prompt budget for this tier is approximately 40000 tokens (advisory).

**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the effective tier is upgraded to at least `medium`. When `consequence: high`,
the effective tier is upgraded to the strongest available model.
`actual_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read` | native |
| `file_write` | `edit / write / apply_patch` | native |
| `terminal_run` | `bash` | native |
| `structured_output` | `—` | native |
