---
name: alawas-production-operate-visual-critic
description: "Use when a rendered image needs evaluation against directorial intent; produces structured critique using vision-capable models and feeds adjustments back to scene planner."
default_tier: medium
platform: claude-code
---
# Operate Visual Critic (vision feedback loop)

## Governing principle

The visual critic evaluates rendered images against directorial intent using
vision-capable models. It produces structured, actionable critique — not
subjective commentary — that the scene planner can consume to adjust the scene.

## Boundaries and non-goals

This skill does:

- Accept a rendered image path and original directorial intent text
- Evaluate the image using a vision-capable model (DeepSeek V4 Flash Vision or equivalent)
- Produce structured critique: composition errors, lighting issues, staging problems
- Output concrete adjustment instructions consumable by scene planner
- Enforce a maximum 3-iteration cap before escalating to director

This skill does not:

- Modify scenes (belongs to scene planner)
- Render images (belongs to Blender/ComfyUI operators)
- Make final quality approval decisions (director's authority)
- Call tools or mutate files

## Inputs and preconditions

**Required inputs:**
- Image path (rendered image to evaluate)
- Directorial intent text (what the shot should look like)

**Preconditions:**
- Vision-capable model is available (DeepSeek V4 Flash Vision or equivalent)
- Scene planner (COMP-046) is available to consume critique output

## Tracer bullet scope (WO 2026-08-24-019 Decision 1)

For the tracer bullet, only the single-function tracer is implemented:
- `visual_critique_for_image(image_path, intent_text) -> dict[str, Any]`
- Returns 5 bounded fields: composition_score, lighting_issues, staging_recommendations, subject_scale_feedback, escalation_needed
- Proves vision→structured output path before full feedback loop implementation

## Required capabilities

- `file_read` — Read image paths and intent text
- `terminal_run` — Run vision model commands
- `structured_output` — Produce valid critique output

## Routing and termination

- **Critique complete:** route to scene planner for adjustments
- **Max iterations reached:** escalate to director for judgment
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
The platform overlay resolves this to `claude-sonnet-4-20250514`.
The prompt budget for this tier is approximately 40000 tokens (advisory).

**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the effective tier is upgraded to at least `medium`. When `consequence: high`,
the effective tier is upgraded to the strongest available model.
`actual_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `Read` | native |
| `terminal_run` | `Bash` | native |
| `structured_output` | `—` | native |
