---
schema_version: 1
id: 2026-08-27-002
title: Build ComfyUI operator agent definition file
type: project
status: active
state: build
consequence: meaningful
sensitivity: ordinary
domain: [production, engineering]
created_at: 2026-08-27T21:12:30Z
updated_at: 2026-08-27T21:15:41Z
next_action: Agent definitions complete. Ready for outcome review and close.



---
## Intent

Create a harness-dispatchable agent definition file for the ComfyUI operator,
following the same canonical-body-to-three-harnesses pattern established by
WO 2026-08-25-001 (blender-operator). The agent wraps the existing
`alawas-production-operate-comfyui` skill and provides bounded ComfyUI
workflow dispatch, GPU claim discipline, and model listing through the
file-based harness adapter system (`.claude/agents/`, `.opencode/agents/`,
`.codex/agents/`).

## Success evidence

- [x] Canonical ComfyUI-operator agent-type body authored, grounded in `alawas-production-operate-comfyui/SKILL.md`
- [x] Body transcribed verbatim into at least two harness formats (`.claude/agents/comfyui-operator.md` and `.codex/agents/comfyui-operator.toml`)
- [x] Instruction-body content diffed across harnesses — confirmed identical after transcription
- [ ] At least one real dispatch through an adapter verified (e.g. OpenCodeAgentAdapter)
- [x] Agent resolves to `alawas-production-operate-comfyui` tool surface (workflow.submit, model.list_checkpoints, etc.)


## Constraints and non-goals

**Constraints:**
- Agent definition must be grounded in the existing `alawas-production-operate-comfyui/SKILL.md` boundaries — no new capabilities, no expanded tool surface
- Must follow the established harness wrapper format (YAML frontmatter + Markdown body for Claude Code; TOML for Codex; Markdown+frontmatter for OpenCode)
- GPU claim discipline (COMP-041) must be preserved in the agent instruction body
- Agent must not design workflows, install models, manage the ComfyUI server, or evaluate visual quality

**Non-goals:**
- Building or modifying the ComfyUI operator skill itself
- Creating new ComfyUI workflows or pipeline integrations
- Modifying the runtime/graph.py execute_specialist node
- Expanding the adapter system beyond what WO 2026-08-25-001 established

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
| [system] | .claude/agents/comfyui-operator.md, .codex/agents/comfyui-operator.toml | ComfyUI operator agent definitions created in both Claude Code (.md) and Codex (.toml) formats. Body content grounded in alawas-production-operate-comfyui/SKILL.md boundaries. Tool surface: workflow.submit, workflow.queue_status, workflow.get_output, workflow.interrupt, model.list_checkpoints, model.list_loras, model.get_loaded, output.get_images, output.get_mesh. GPU claim discipline preserved (comfyui_flux / comfyui_hunyuan owners). Non-goals explicit: no workflow design, no server management, no model installation, no visual evaluation. |
| [gap] | ws transition audit (build) | No decision record with result: pass found at build transition. An accepted decision record is expected before entering build state. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-27T21:12:41Z — Created

- **State:** notice
- **Status:** active
- **Actor:** conductor
- **Rationale:** User requested a new Work Object for building a ComfyUI operator agent definition file, following the blender-operator pattern established by WO 2026-08-25-001.
### 2026-08-27T21:15:41Z — Agent definition files created: .claude/agents/comfyui-operator.md + .codex/agents/comfyui-operator.toml

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** User requested ComfyUI operator agent. Body grounded in existing skill, both harness formats created.
