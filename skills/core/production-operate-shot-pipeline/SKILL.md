---
name: production-operate-shot-pipeline
default_tier: medium
description: "Use when a shot must be created from screenplay breakdown through final render; orchestrates scene planner, Blender operator, and visual critic through a tiered state machine with retry and resume capability."
---

# Operate Shot Pipeline (tiered state machine)

## Governing principle

The shot pipeline sequences Layer 1/2 operators through a tiered state machine
that tracks progress and enables resume-from-failure. Each tier calls the
appropriate operator; state persists in the Shot Work Object so a crash
mid-pipeline leaves a recoverable record.

## Boundaries and non-goals

This skill does:

- Accept a shot description from screenplay breakdown.
- Run shots through a tiered state machine: breakdown → tier_a → tier_b → tier_c → final.
- Each tier calls the appropriate operator (scene planner, Blender, visual critic).
- Track shot state in the Shot Work Object frontmatter.
- Resume from the last successful tier on failure.
- Retry individual tiers up to 3 times before marking shot as failed.

This skill does not:

- Make editorial decisions about shot selection or sequencing.
- Execute tools directly — always uses Layer 1/2 operators.
- Skip director approval gates for tier escalation.
- Manage GPU claims — that flows through operators via COMP-041.

## Inputs and preconditions

**Required inputs:**
- Shot description (text from screenplay breakdown)
- Target tier (A, B, or C)

**Preconditions:**
- Scene planner (COMP-046) is available
- Blender operator (COMP-042) is available and verified
- Visual critic (COMP-047) is available (for Tier B and C)

## Tiered state machine

```
breakdown → tier_a → tier_b → tier_c → final
```

Each tier:
- **Tier A (fast sketch):** Rough 3D blocking, proxy lighting. Produces quick preview.
- **Tier B (refined):** Full scene assembly, proper materials, draft render.
- **Tier C (final):** Full-quality render, compositing.

Each state transition:
1. Calls the appropriate Layer 1/2 operator
2. Updates the Shot Work Object with the new state
3. Records the operator result in the evidence ledger
4. On failure: increments retry count, retries up to 3 times
5. On 3 failures: marks shot as failed, stops pipeline

## Tracer bullet scope (WO 2026-08-24-021 Decision 2)

For the tracer bullet, only Tier A is tested:
- breakdown → tier_a

A simulated failure is injected at the tier_a stage to test resume capability.

## Required capabilities

- `file_read` — Read shot descriptions and state
- `file_write` — Update shot state and evidence
- `terminal_run` — Run operator commands
- `structured_output` — Produce valid state transitions

## Routing and termination

- **Pipeline complete:** route to conductor for shot registry registration
- **Pipeline failed:** route to conductor with failure evidence
- **Capability gap:** stop and report the gap
