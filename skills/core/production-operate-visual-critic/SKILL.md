---
name: production-operate-visual-critic
default_tier: medium
description: "Use when a rendered image needs evaluation against directorial intent; produces structured critique using vision-capable models and feeds adjustments back to scene planner."
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
