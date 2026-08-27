---
schema_version: 1
id: 2026-08-24-017
title: Build scene planner skill for directorial intent to structured scene specification
type: change
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [production]
created_at: 2026-08-25T01:56:58Z
updated_at: 2026-08-25T18:39:01Z
next_action: alawas-governance-conduct-work-object: record the live executor evidence and preserve verify/active; route queue diagnosis and canonical .blend registry creation as separate scoped work.













---
## Intent

Take a director's natural-language shot description and produce a structured
scene specification: environment, characters, camera, lighting, composition,
render passes. Performs the six jobs: interpret shot, retrieve assets from
registry, place everything, compose camera, light it, specify render. This is
the creative reasoning layer that translates "make him feel tiny against the
landscape" into concrete spatial parameters.

Parent: WO `2026-08-23-001` §4. Component: COMP-045.

## Success evidence

- [x] Accepts natural-language directorial intent and produces structured YAML scene spec
- [ ] Queries asset registry for available .blend files matching scene needs
- [x] Reports missing assets as gaps (not fabricated placements)
- [x] Computes camera, lighting, and composition from emotional/dramatic intent
- [ ] Output is directly executable by Blender operator (`2026-08-24-014`)


## Constraints and non-goals

**Constraints:**
- Never calls Blender or ComfyUI directly — produces specs for operators
- Must use asset registry — cannot invent assets that don't exist
- Uses `production-compose-blocking` (`2026-08-24-018`) for spatial math

**Non-goals:**
- No tool execution (Layer 1 responsibility)
- No visual evaluation (belongs to `2026-08-24-019`)
- No asset creation (belongs to `2026-08-24-020`)

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Accepted dry-run fixture-registry scene-planner tracer

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Smallest COMP-045 Scene Planner tracer: implement a dry-run local planner that accepts one natural-language directorial prompt, queries a fixture asset registry with one or more known assets plus at least one deliberately missing need, emits structured YAML scene spec fields (`intent`, `asset_matches`, `asset_gaps`, `camera`, `lighting`, `composition`, `render_passes`, and a Blender-command plan), and maps only to bounded Blender operator operations. The tracer must not call Blender, ComfyUI, cloud APIs, or asset-generation tools; it must not create canonical assets or fabricate missing assets. |
| **Authorization** | Director accepted the immediately preceding design-tracer recommendation in chat: "i accept". |
| **Confidence** | medium-high for proving the planner boundary because the repo already has a verified bounded Blender operator surface and the production plan defines the Scene Planner responsibility; medium for real production usefulness because the canonical `.work-studio/asset-registry.md` does not exist yet and no production `.blend/.glb/.obj/.fbx` assets were found in the repo search. |
| **Actor** | Director (acceptance), alawas-design-design-tracer-bullet (design), codex (context retrieval) |
| **Revisit trigger** | Revisit if a canonical production asset registry is created before implementation and changes the fixture-registry interface, if the planner cannot express emotional/dramatic intent without fabricating unregistered assets, or if the emitted command plan does not map cleanly to `production-operate-blender` bounded operations. |
| **Rationale** | The riskiest assumption is that Scene Planner can translate directorial intent into an executable scene spec while selecting only known assets and reporting missing needs as gaps. A dry-run fixture-registry tracer tests that assumption without prematurely building asset production, calling Blender, or hardening a full production registry. Exit criteria: one focused test/demo shows known assets selected, missing assets reported as gaps, and generated YAML mapped to bounded Blender operations. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [decision] | director route request, 2026-08-25 | Director asked to route the existing Scene Planner Work Object. Classification result: activate the existing meaningful-consequence production change for COMP-045 rather than discard, remember, or incubate. Basis: the object already has a concrete parent reference (WO 2026-08-23-001 section 4), component reference (COMP-045), production domain, explicit success evidence, and bounded non-goals. Next stage is design-tracer-bullet to choose the smallest scene-planner tracer before implementation. |
| [decision] | director acceptance, 2026-08-25 | Director accepted the design-tracer recommendation: build the smallest dry-run Scene Planner tracer using a fixture asset registry, one directorial prompt, known asset selection, missing asset gaps, structured YAML scene spec, and a Blender-command plan constrained to bounded production-operate-blender operations. No Blender/ComfyUI/tool execution, no asset creation, no canonical registry creation, and no fabricated assets are authorized in this slice. |
| [system] | COMP-045 tracer implementation, 2026-08-25 | Added tools/production/scene_planner/planner.py and fixture registry fixtures/production/scene_planner/asset_registry.yaml. Focused command: uv run --python 3.11 python -m unittest tests.test_scene_planner_tracer -v. Result: 3 tests passed. Evidence covers registered protagonist selection, missing landscape gap with fabricated=false, structured YAML fields, bounded Blender operation names, and no subprocess tool execution. No Blender, ComfyUI, cloud API, asset generation, or canonical registry write was performed. |
| [system] | COMP-045 verification, 2026-08-25 | Executed uv run --python 3.11 python -m unittest tests.test_scene_planner_tracer -v: 3/3 passed. Independent local verification also passed for exact scene-spec field set, YAML emission, known protagonist selection, missing landscape gap, bounded Blender op containment, and empty-prompt rejection. No external systems, production data, secrets, Blender, ComfyUI, or tool execution were used. |
| [gap] | COMP-045 verification boundary, 2026-08-25 | The fixture planner verified only a dry-run command descriptor. The canonical .work-studio/asset-registry.md and production .blend assets are absent from the inspected repository, the fixture uses a descriptor path for a .glb asset, and no live Blender session was started. Therefore .blend registry querying and direct end-to-end execution by production-operate-blender remain unverified; no release or deployment claim is made. Next safe action is a separately scoped canonical asset-registry/live-Blender verification slice. |
| [system] | COMP-045 live Blender verification, 2026-08-25 | Canonical registry check: .work-studio/asset-registry.md is absent and no .blend assets were found in the scoped .work-studio, runtime, or fixtures paths. Live Blender check: Blender 5.2.0 executed the bounded executor operation scene.get_info in a factory-startup background session and returned ok=True with scene=Scene, object_count=3, blender_version=5.2.0 LTS. No production data or external system was accessed. |
| [gap] | COMP-045 live verification boundary, 2026-08-25 | The planner's accepted full path remains unverified: no canonical .blend registry exists to query, the fixture registry points to a descriptor-only .glb path, and the queued addon one-shot command did not produce a result acknowledgement within 30 seconds and was stopped as the verification-launched process. Direct bounded executor execution is verified; queue-mediated planner execution and real asset import are not. Next safe action is a separately scoped queue/addon diagnosis plus canonical asset-registry decision. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-25T18:24:46Z — Resumed and activated as supporting

- **State:** notice
- **Status:** active
- **Actor:** codex
- **Rationale:** Director invoked the conductor on the Scene Planner Work Object by path. The object is active but still in notice with no recorded classification evidence, so it was added to active.md as supporting and routed to turn-signal-into-work for activation/classification before design or build work.
### 2026-08-25T18:25:40Z — Classified and activated Scene Planner work

- **State:** design
- **Status:** active
- **Actor:** alawas-thinking-turn-signal-into-work
- **Rationale:** The routed signal is an existing active Work Object with clear parent/component references, meaningful consequence, ordinary sensitivity, production domain, success evidence, and bounded non-goals. It should not be discarded, remembered, or incubated; it is ready for design because the smallest executable scene-planner tracer boundary still needs to be chosen before implementation.
### 2026-08-25T18:28:25Z — Accepted dry-run Scene Planner tracer design

- **State:** build
- **Status:** active
- **Actor:** alawas-design-design-tracer-bullet
- **Rationale:** Director accepted the smallest dry-run fixture-registry tracer. The riskiest assumption is now bounded: Scene Planner must translate directorial intent into a structured YAML scene spec, select only known registered fixture assets, report missing needs as gaps, and emit a Blender-command plan compatible with the bounded Blender operator without calling tools or creating assets.
### 2026-08-25T18:32:28Z — Implemented accepted COMP-045 dry-run tracer

- **State:** verify
- **Status:** active
- **Actor:** alawas-engineering-implement-bounded-change
- **Rationale:** [system] Focused tracer tests passed 3/3. [inference] The accepted dry-run boundary is implemented: local fixture-registry selection, explicit missing-asset gaps, structured YAML, and bounded Blender command descriptors without tool execution. Live Blender execution remains unverified because the fixture path is a descriptor and the canonical production asset registry/assets are out of scope.
### 2026-08-25T18:34:06Z — Verified bounded COMP-045 tracer evidence

- **State:** verify
- **Status:** active
- **Actor:** alawas-engineering-verify-release-evidence
- **Rationale:** [system] Focused and independent local checks passed. [inference] Dry-run acceptance criteria are verified; canonical .blend registry querying and live Blender execution remain unverified gaps and are not release evidence.
### 2026-08-25T18:39:01Z — Verified direct live Blender executor; preserved registry and queue gaps

- **State:** verify
- **Status:** active
- **Actor:** alawas-engineering-verify-release-evidence
- **Rationale:** [system] Blender 5.2.0 returned structured success for bounded scene.get_info. [gap] Canonical .blend registry is absent, no .blend assets exist in scoped paths, and queue-mediated one-shot execution timed out without an acknowledgement. [inference] Direct executor behavior is verified, but the full planner-to-queue-to-asset-import story is unverified.
