---
schema_version: 1
id: 2026-08-27-001
title: Design Animation and Visual Development agents for Work Studio
type: project
status: active
state: notice
consequence: meaningful
sensitivity: ordinary
domain: [production, design]
created_at: 2026-08-27T20:53:04Z
updated_at: 2026-08-27T20:54:57Z
next_action: Route to alawas-thinking-turn-signal-into-work to activate and classify the Animation and Visual Development branches; recommend Animation Agent as the first design branch.




---
## Intent

Define two missing agent-level owners in Work Studio's production architecture:
an **Animation Agent** for character motion, performance timing, and editable
animation takes, and a **Visual Development Agent** for governed look
exploration and translation of approved style direction into production-ready
assets or scene changes. Produce accepted contracts and bounded tracer routes
without rebuilding the existing Layout, Critic, Blender Operator, Research,
ComfyUI, TTS, or asset-pipeline capabilities.

## Success evidence

- [ ] Current agent-to-skill/component map is reconciled against live Work Objects and canonical skills
- [ ] Animation Agent ownership, inputs, outputs, authority, dependencies, and non-goals are accepted
- [ ] Visual Development Agent ownership, inputs, outputs, authority, dependencies, and non-goals are accepted
- [ ] Both agents use typed, file-backed artifacts and preserve Work Studio as canonical state
- [ ] Token-budget and compaction expectations are defined for each agent
- [ ] Each agent has one smallest viable tracer with explicit verification evidence
- [ ] Implementation is routed through bounded successor Work Objects rather than widening this design project


## Constraints and non-goals

**Constraints:**
- Treat the accepted decision in WO `2026-08-25-002` as the architectural
  baseline: agent-shaped execution consumes existing skills and operators; it
  does not replace them.
- Reuse `production-plan-scene` (COMP-045), Blocking Composition (COMP-046),
  `production-operate-visual-critic` (COMP-047),
  `production-operate-blender` (COMP-042), the ComfyUI and TTS operators, the
  asset pipeline, and the research skill through typed handoffs.
- Preserve file-first canonical state, immutable provenance, explicit
  authority envelopes, GPU-claim discipline, and human approval gates.
- Keep Animation and Visual Development as separate ownership boundaries even
  while this Work Object governs their shared architecture.
- Fail closed when an operator, model, rig map, asset license, or production
  capability has not been live-verified.

**Non-goals:**
- No implementation, model download, software installation, deployment, or
  production-scene mutation in this Work Object.
- No redesign of existing Layout, Critic, Blender Operator, or Research agents.
- No generic multi-agent runtime rewrite or replacement of `runtime/agents.py`.
- No claim that generative video, research text-to-motion, automatic
  retargeting, or visual-continuity scoring is production-ready.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Create one design project for the two missing production agents

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Create a separate umbrella Work Object for Animation Agent and Visual Development Agent design while preserving existing production agents as dependencies. |
| **Authorization** | Director explicitly requested: "create a separate work object for the agents." |
| **Confidence** | High that both are current ownership gaps; medium that one umbrella design project is sufficient through implementation, because their tracer and tool dependencies differ. |
| **Actor** | Director (authorization), alawas-governance-conduct-work-object (persistence) |
| **Revisit trigger** | Split into separate successor Work Objects when either agent reaches an accepted tracer design, or earlier if their authority, evidence, or dependency boundaries conflict. |
| **Rationale** | [decision] WO `2026-08-25-002` established that Layout, Critic, Blender Operator, and Research already map to existing capabilities while Animation and Visual Development remain genuine gaps. A shared design project preserves their relationship to the same Director Console and shot pipeline, while bounded successors prevent coupled implementation. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [decision] | Director request, 2026-08-27 | Director explicitly requested a separate Work Object for the agents after review of the existing-agent map and the Animation/Visual Development gaps. |
| [system] | Current Work Objects and canonical skills, inspected 2026-08-27 | Scene Planner COMP-045 is verify/active; Blocking Composition COMP-046 is design/active; Blender Operator COMP-042 is verify/active; Visual Critic COMP-047 is closed and its downstream shot-pipeline integration Work Objects are closed; research-investigate-live-question exists as a canonical core skill. |
| [gap] | Canonical skills and production tooling search, 2026-08-27 | No canonical Animation Agent or Visual Development Agent owner was found. Existing TTS, Blender, ComfyUI, asset, scene-planning, design-direction, and critic capabilities provide dependencies or partial functions but do not own editable character performance or governed look development end to end. |
## Open questions

- Where does Animation Agent ownership stop relative to Scene Planner timing,
  TTS/viseme generation, Blender execution, and director performance approval?
- Where does Visual Development Agent ownership stop relative to design
  direction, ComfyUI execution, asset promotion, materials, lighting, and
  compositing?
- Which typed artifacts form each agent's stable input/output contract?
- What evidence is required before each agent is exposed in Director Console?

## Next move

Route to `alawas-thinking-turn-signal-into-work` to activate and classify the
two agent branches, preserve one shared architectural boundary, and select the
first branch for design. Recommended first branch: Animation Agent, because
the current character-animation implementation plan supplies a concrete
voice-to-face and one-rig motion tracer boundary.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-27T20:54:22Z — Created separate agent-design Work Object with consequence assessment

- **State:** notice
- **Status:** active
- **Actor:** codex
- **Rationale:** Reversible: yes, design records and future successors can be revised. Affects beyond workspace: no current external effect; later implementation may affect durable production architecture. Failure affects safety/privacy/money: no direct effect at this stage. Assigned consequence: meaningful because accepted agent contracts can direct substantial implementation effort. Scope is limited to Animation Agent and Visual Development Agent; existing agents remain dependencies.
