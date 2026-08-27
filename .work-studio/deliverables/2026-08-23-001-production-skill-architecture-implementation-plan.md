# Production Skill Architecture — Implementation Plan

> **Deliverable type:** plan
> **Source Work Object:** `2026-08-23-001` (Director Console)
> **Date:** 2026-08-24
> **Author:** Andre (andrelawas35@gmail.com)
> **Synthesizes:** WO `2026-08-23-001` §2.4 (GPU time-share), §4 (specialist
> profiles), §5 (production departments), §5.4 (asset production), §5.5
> (creative precedent library); investigation results from the production
> skill architecture session (2026-08-24); existing system patterns from
> `BUSINESS-OPERATING-PIPELINE.md`, `ENGINEERING-OPERATING-PIPELINE.md`,
> `component-ledger.md`, domain system (`ws domain sync`), and the validated
> precedent ledger (R-001, R-002).
> **Grounding:** Current Work Studio system (`tools/ws`, 42 skills across
> COMP-001 through COMP-040, design-asset pipeline, domain frontmatter,
> runtime graph projection from WO `2026-08-22-016`).

This plan synthesizes only already-accepted material. It authors nothing new —
every skill boundary, pipeline route, and domain extension traces to the
Director Console implementation plan (WO `2026-08-23-001`) or to system
evidence from the existing Work Studio infrastructure. Where inference is
required to bridge accepted material, it is labeled `[inference]`.

---

## 0. Governing Principle

The production domain translates directorial intent into controllable spatial,
visual, and audio artifacts through governed tool operations. The LLM reasons
about what the scene should communicate. Blender and ComfyUI execute
deterministic operations. The director establishes canon. The production
skills enforce this separation: creative reasoning never bypasses tool
governance, and tool operators never make creative decisions.

The production skill architecture follows the same structural pattern the
studio already uses for business and engineering: a domain tag, a set of
specialist skills, and a routing pipeline — extended with a GPU execution
layer that neither of those domains needs.

---

## 1. What Already Exists (System Evidence)

### 1.1 Domain system

`[system]` Work Objects declare `domain:` in frontmatter (e.g.,
`domain: [business]`, `domain: [engineering, architecture]`). `ws domain sync`
generates index files under `.work-studio/domain/`. Nine domains exist:
`architecture`, `asset`, `business`, `design`, `engineering`, `governance`,
`ideation`, `operations`, `research`. No `production` domain exists yet.

### 1.2 Operating pipeline pattern

`[system]` Two canonical operating pipelines exist:

- `references/BUSINESS-OPERATING-PIPELINE.md` (COMP-036): routes business
  questions through 16 business skills in a default order, with an ownership
  map and handoff rules.
- `references/ENGINEERING-OPERATING-PIPELINE.md`: routes engineering questions
  through 7 engineering/operations skills in a default order.

Both are promoted into the runtime as NetworkX graph projections (WO
`2026-08-22-016`). Both are routing spines — they decide which skill answers
the next question. Neither manages external tool state, GPU resources, or
feedback loops.

### 1.3 Component ledger

`[system]` `.work-studio/component-ledger.md` (ADR 0014) indexes 40
components (COMP-001 through COMP-040). Entry schema: status, component kind,
governance domain, location, built-by WO, declared edges, applicable
dimensions, owning skill, last-grilled-SHA, best-case anchor, findings.
Component kind values: `skill | protocol | runtime | tooling |
artifact-schema | integration`. Governance domain values include the 9
existing domains. New production components will extend this ledger.

### 1.4 Skill system

`[system]` 42 skills exist across 7 governance domains. Each skill has
defined boundaries, required capabilities, authority rules, a grilling
profile, and routes through the conductor. No skill currently calls external
tool APIs (Blender, ComfyUI, TTS) or manages GPU resources. All existing
skills operate on files, evidence, and decisions.

### 1.5 Director Console instruments

`[system]` From WO `2026-08-23-001` §1.7 and §2.4:

- **RTX 3080** (10 GB VRAM): Blender rendering, ComfyUI image generation,
  video generation. Sequential load/unload required.
- **ComfyUI Desktop**: running locally on `:8188`, Flux Dev FP8 installed.
- **Blender**: installed, scriptable via Python API.
- **DeepSeek V4 Flash Vision**: cloud API for visual critique and reasoning
  fallback.
- **API LLM** (Claude): reasoning, routing, tool calls.

### 1.6 Validated recipes

`[system]` Two recipes validated in `precedent-ledger.md`:

- **R-001** (segmentation-masked-regional-revision): regional image revision
  via rembg + VAEEncodeForInpaint + Flux. Validated on RTX 3080.
- **R-002** (single-view-image-to-3d-mesh-turnaround): Hunyuan3D-2 mesh from
  single concept image. Shape-only, fits 10 GB VRAM. Validated on RTX 3080.

### 1.7 Design-asset pipeline

`[system]` `.work-studio/design-assets/` with managed records (`*.asset.md`),
YAML frontmatter, routing pipeline, and a validated registry. This is the
existing precedent for domain-specific structured records with their own
frontmatter schema.

---

## 2. Production Domain Registration

### 2.1 Domain tag

Add `production` to the domain vocabulary. Work Objects for production work
declare `domain: [production]` (or `domain: [production, architecture]` when
cross-cutting) in frontmatter. `ws domain sync` generates
`.work-studio/domain/production.md` automatically.

`[system]` This follows the existing pattern — no code change to `tools/ws`
required. The domain vocabulary is discovered from frontmatter, not from a
hardcoded list.

### 2.2 Work Object extensions

Production Work Objects use the standard Work Object schema with
domain-specific **body section conventions** enforced by production skills,
not by schema changes to `tools/ws`.

#### Scene Work Object (from §3.2)

A Scene Work Object adds these structured sections to the standard body:

```markdown
## Scene Board

- **Thesis:** <one sentence>
- **Turn:** <what changes>
- **Character state:** <character>: <from> → <to>
- **Audience state:** <from> → <to>
- **Beats:** <numbered list>
- **Directorial rules:** <constraints>

## Screenplay

### Layer A — Story
### Layer B — Drama
### Layer C — Direction
### Layer D — Realization

## Director Layer

| Beat | Screenplay | Director Intent | Performance | Production |
|------|-----------|-----------------|-------------|------------|
```

#### Shot Work Object (from §3.3)

A Shot Work Object adds frontmatter fields and a Shot Specification section:

```yaml
# Extended frontmatter (free-form fields, no tools/ws schema change)
shot_id: SQ01_SC03_SH042
tier: B  # A=generative, B=Blender-guided AI, C=hero controlled
shot_status: blocking  # blocking | animation | render | review | approved
```

```markdown
## Shot Specification

- **Story function:** <what this shot communicates>
- **Intent:** <what the audience should perceive>
- **Camera:** shot_size: <size>, lens: <mm>
- **Performance:** <character behavior>
- **Audio:** dialogue: <>, ambience: <>
- **Continuity:** <prop/position constraints>
- **Protect:** <elements that must not change>
```

#### Direction Object (from §2.2)

Every director input becomes a Direction recorded as `[testimony]` evidence:

```yaml
direction:
  basis: <what this builds on>
  protect: <what must not change>
  change: <what should change>
  desired_effect: <what the audience should perceive/feel>
  authority: approve | propose | explore
```

`[inference]` These extensions use free-form frontmatter fields and body
section conventions. The `tools/ws` CLI stays schema-agnostic. Production
skills enforce the shapes — the same way the Story Editor skill enforces
"beats before dialogue." The design-asset `*.asset.md` pattern is the
precedent for domain-specific structured records.

---

## 3. Three-Layer Skill Architecture

The production skills are organized in three layers. Each layer has a
distinct responsibility and a clear boundary with the others.

### 3.1 Layer 1 — Tool Operators (infrastructure)

Tool operators wrap external tool APIs. They execute structured commands, own
VRAM lifecycle for their tool, and have no creative opinion. They are
deterministic executors, like `tools/ws` is for Work Objects.

#### `production-operate-blender`

- **Component kind:** skill
- **Governance domain:** production
- **Boundary:** Wraps the bounded Blender API from §4.2. Accepts structured
  scene operations: place object, set camera, assign material, render
  preview, import mesh, import reference image, set rig pose, move keyframe.
  Owns the Blender VRAM slot. Rejects arbitrary Python unless the director
  explicitly escalates (high-consequence gate, same authority model as §4.2
  `execute_blender_python()`).
- **Required capabilities:** `terminal_run` (Blender Python subprocess or
  local network protocol), `file_read`/`file_write` (scene files, render
  outputs), `gpu_claim` (VRAM slot via `production-orchestrate-gpu`).
- **Tool surface (from §4.2):**

  ```text
  SCENE / OBJECT
  scene.get_objects          object.get / set_transform / duplicate / delete
  object.set_parent          object.select / deselect
  object.import_mesh(.glb/.obj/.fbx)

  CAMERA / LIGHT
  camera.get / set / lock    light.get / set
  render.preview / final

  RIG / ANIMATION
  rig.get_pose               rig.set_bone_rotation
  animation.get_keyframes    animation.move_keyframe / set_interpolation

  MESH (asset cleanup)
  mesh.get_vertices          mesh.move_vertices
  mesh.extrude               mesh.separate_by_material
  mesh.add_modifier(name, params)
  mesh.set_dimensions        mesh.set_origin
  mesh.decimate(ratio)       mesh.remove_doubles(threshold)

  MATERIAL
  material.get / set / assign
  material.set_texture(slot, image_path)

  IMAGE
  image.import_as_plane      image.set_as_reference
  ```

- **Does NOT:** Make creative decisions. Choose camera angles. Select assets.
  Evaluate composition. Run arbitrary Python without director escalation.
- **Depends-on:** `production-orchestrate-gpu`
- **Implementation pattern:** Blender add-on accepting structured commands
  over local WebSocket/HTTP, same architectural pattern as BCC's
  Controller_Addon (§10, WO `2026-08-23-001`).

#### `production-operate-comfyui`

- **Component kind:** skill
- **Governance domain:** production
- **Boundary:** Wraps the ComfyUI HTTP/WebSocket API on `:8188`. Submits
  workflow JSON, polls queue, retrieves output images/meshes. Owns the
  diffusion-model VRAM slot. Handles model loading/unloading (Flux Dev FP8,
  Hunyuan3D-2) within the VRAM budget.
- **Required capabilities:** `web_fetch` (ComfyUI API on localhost:8188),
  `file_read`/`file_write` (workflow templates, output files),
  `gpu_claim` (VRAM slot via `production-orchestrate-gpu`).
- **Tool surface:**

  ```text
  WORKFLOW
  workflow.submit(workflow_json)    workflow.queue_status()
  workflow.get_output(prompt_id)    workflow.interrupt()

  MODEL
  model.list_checkpoints()         model.list_loras()
  model.get_loaded()

  OUTPUT
  output.get_images(prompt_id)     output.get_mesh(prompt_id)
  output.save_to(path)
  ```

- **Does NOT:** Choose styles. Evaluate visual quality. Design workflows.
  Select models. Those are Layer 2 decisions.
- **Depends-on:** `production-orchestrate-gpu`

#### `production-operate-tts`

- **Component kind:** skill
- **Governance domain:** production
- **Boundary:** Calls tiered TTS APIs (local → cheap API → premium API, per
  §5.2). Generates audio takes from structured performance parameters. Returns
  audio files. No performance opinion.
- **Required capabilities:** `web_fetch` (TTS API calls), `file_write`
  (audio output files).
- **Tool surface:**

  ```text
  tts.generate(text, voice_id, performance_params, tier)
  tts.list_voices()
  tts.get_take(take_id)
  ```

- **Does NOT:** Translate intent into performance parameters. Choose voice
  identity. Select takes. Those are Layer 2 decisions.

#### `production-orchestrate-gpu` (protocol)

- **Component kind:** protocol
- **Governance domain:** production
- **Boundary:** Enforces sequential VRAM discipline (§2.4). Only one
  GPU-heavy operator runs at a time. Operators check in (claim slot) and
  check out (release slot) through this protocol. Tracks current VRAM state.
- **State machine:**

  ```text
  VRAM states:
    idle
    blender_loaded
    comfyui_flux_loaded
    comfyui_hunyuan3d_loaded

  Transitions:
    claim(tool) → if idle: load tool, transition to tool_loaded
                → if other_tool_loaded: unload current, load requested
    release(tool) → transition to idle

  Invariant: at most one GPU-heavy process at any time.
  ```

- **Evidence:** `[system]` WO `2026-08-23-002` records two TDR driver crashes
  under sustained GPU load. This protocol prevents concurrent GPU claims that
  cause those crashes.
- **Does NOT:** Decide what to render. Schedule production work. Prioritize
  jobs. It is a lock, not a scheduler.

### 3.2 Layer 2 — Scene Intelligence (creative reasoning)

Scene intelligence skills reason about what should happen in a scene. They
produce structured scene specifications and hand them to Layer 1 operators.
They never call Blender or ComfyUI directly.

#### `production-plan-scene`

- **Component kind:** skill
- **Governance domain:** production
- **Boundary:** Takes a director's natural-language shot description and
  produces a structured scene specification. Interprets directorial intent
  ("make him feel tiny against the landscape") into concrete spatial
  parameters (lens choice, camera distance, horizon placement, negative space
  ratio). Selects assets from the asset registry. Produces the scene
  specification that Layer 1 operators execute.
- **The six jobs** (from the reference analysis):
  1. **Interpret the shot** — derive shot type, camera, character placement,
     environment, lighting, composition from directorial intent.
  2. **Retrieve assets** — query the asset registry for available `.blend`
     files matching the scene needs. Report missing assets as gaps.
  3. **Place everything** — compute positions, rotations, scales for all
     scene elements.
  4. **Compose the camera** — calculate camera position, lens, subject
     distance, horizon, negative space to achieve the intended effect.
  5. **Light it** — establish lighting setup from emotional/atmospheric
     intent, grounded in the director's visual language.
  6. **Specify the render** — define what passes to export (beauty, depth,
     normals, pose, masks) for downstream ComfyUI processing.
- **Output:** Structured scene specification (YAML):

  ```yaml
  scene_spec:
    environment:
      asset: apartment_modern_01
      modifications: []
    characters:
      - asset: character_female_01
        position: [0.5, 0.8, 0]
        pose: standing_neutral
    camera:
      lens_mm: 50
      position: [computed]
      target: character_head
      shot_size: medium_close
      height: eye_level_minus_10cm
    lighting:
      key: hard_sun
      direction: camera_left
      intensity: high
      fill: ambient_low
    composition:
      subject_placement: right_third
      negative_space: moderate
      depth_planes: [foreground_obstruction, subject, background_window]
    render_passes: [beauty, depth, normals, object_masks]
  ```

- **Does NOT:** Execute Blender commands. Run ComfyUI workflows. Evaluate
  rendered output. Those belong to Layer 1 (execution) and Layer 2 (critique).
- **Depends-on:** `production-compose-blocking` (for spatial calculations),
  asset registry (for asset selection)

#### `production-compose-blocking`

- **Component kind:** skill
- **Governance domain:** production
- **Boundary:** Mathematical composition and blocking calculations. Computes
  spatial relationships that achieve dramatic effect. Pure mathematics — no
  tool calls, no file mutations.
- **Calculations:**

  ```text
  CAMERA MATHEMATICS
  focal_length_for_effect(desired_distortion, sensor_size, subject_distance)
  depth_of_field(aperture, focal_length, subject_distance)
  field_of_view(focal_length, sensor_size)
  camera_height_for_authority(subject_height, desired_angle)

  COMPOSITION
  rule_of_thirds_position(frame_width, frame_height, quadrant)
  golden_ratio_position(frame_width, frame_height)
  leading_lines_convergence(vanishing_point, subject_position)
  negative_space_ratio(subject_bounds, frame_bounds)
  visual_weight_balance(element_positions, element_sizes)
  depth_staging(foreground, midground, background, camera_position)

  CHARACTER BLOCKING
  interpersonal_distance(relationship, tension_level)
  eyeline_angle(character_a_position, character_b_position, heights)
  crossing_pattern(characters, waypoints, timing)
  screen_direction(entry_point, exit_point, cut_continuity)
  relative_scale(character_distance, lens, sensor)
  ```

- **Does NOT:** Decide what the shot should communicate. Choose assets. Call
  any tool. It computes geometry from parameters that `production-plan-scene`
  provides.

#### `production-critique-visual`

- **Component kind:** skill
- **Governance domain:** production
- **Boundary:** Takes a rendered preview image, the original directorial
  intent, and the scene specification. Uses DeepSeek V4 Flash Vision (§1.7)
  to evaluate whether the composition achieves the intent. Produces a
  structured critique: what's preserved, what's wrong, what adjustment to
  try. Closes the visual feedback loop.
- **Feedback loop:**

  ```text
  Scene Planner → Blender Operator → render preview →
  Visual Critic → structured critique →
    if pass: report PRESERVED ✓ / CHANGED Δ / PROPOSED ?
    if fail: adjustment spec → Scene Planner → re-render
  Loop limit: 3 iterations before escalating to director.
  ```

- **Output:** PRESERVED/CHANGED/PROPOSED report (§6.4), which is also by
  construction a Revision record for the Creative Precedent Library (§5.5).
- **Does NOT:** Execute changes. Approve canon. Override the director. After
  3 failed iterations, it escalates — it never force-converges.
- **Depends-on:** DeepSeek V4 Flash Vision API (cloud dependency, per
  Decision 10)

### 3.3 Layer 3 — Production Pipelines (end-to-end workflows)

Pipeline skills orchestrate Layer 1 and Layer 2 into complete production
workflows. Each pipeline produces one kind of canonical artifact.

#### `production-pipeline-asset`

- **Component kind:** skill
- **Governance domain:** production
- **Boundary:** The asset creation funnel from §5.4. End-to-end from concept
  to canonical 3D asset. Populates the asset registry that every other
  pipeline depends on.
- **Pipeline:**

  ```text
  DIRECTOR INTENT
      ↓
  2D EXPLORATION (ComfyUI operator: generate 8-20 concepts)
      ↓
  DIRECTOR APPROVES LOOK ([decision])
      ↓
  REFERENCE SET (ComfyUI operator: front/side/back/3/4)
      ↓
  AI 3D GENERATION (ComfyUI operator: Hunyuan3D → .glb)
      ↓
  BLENDER IMPORT + CLEANUP (Blender operator: import, scale, separate,
      name, retopologize via bounded mesh tools)
      ↓
  CRITIC CHECK (Visual Critic: silhouette, dimensions, concept similarity)
      ↓
  DIRECTOR APPROVES ([decision])
      ↓
  CANONICAL 3D ASSET (design-asset record + asset registry entry)
  ```

- **GPU sequencing:** ComfyUI (Flux) → unload → ComfyUI (Hunyuan3D) →
  unload → Blender → unload. Each transition goes through
  `production-orchestrate-gpu`.
- **Depends-on:** `production-operate-comfyui`, `production-operate-blender`,
  `production-orchestrate-gpu`, `production-critique-visual`, design-asset
  pipeline (§1.5)

#### `production-pipeline-shot`

- **Component kind:** skill
- **Governance domain:** production
- **Boundary:** End-to-end shot production from shot specification to
  canonical shot artifact. Routes by tier (A/B/C from §5.3).
- **Pipeline:**

  ```text
  SHOT SPECIFICATION (Shot Work Object)
      ↓
  TIER ROUTING
    A (generative): ComfyUI/video → director approval
    B (Blender-guided AI): Scene Planner → Blender layout →
        render passes → ComfyUI appearance → variant comparison
    C (hero controlled): full Blender pipeline + selective AI enhancement
      ↓
  VARIANT COMPARISON (generated HTML, director selects)
      ↓
  VISUAL CRITIQUE LOOP (up to 3 iterations)
      ↓
  DIRECTOR APPROVES ([decision])
      ↓
  CANONICAL SHOT (design-asset record)
  ```

- **Depends-on:** `production-plan-scene`, `production-compose-blocking`,
  `production-operate-blender`, `production-operate-comfyui`,
  `production-critique-visual`, `production-orchestrate-gpu`

#### `production-pipeline-environment`

- **Component kind:** skill
- **Governance domain:** production
- **Boundary:** The 10-step environment workflow from §5.4. Assembles a
  complete environment from concept to final composite.
- **Pipeline (from §5.4):**

  ```text
  1. COMFYUI — generate 8-20 environment concepts
      ↓ unload
  2. DIRECTOR SELECTS — approved visual direction
      ↓
  3. LLM — extract environment language (architecture, materials,
           lighting, landmarks, mood)
      ↓
  4. BLENDER BLOCKOUT — simple geometry: scale, walkable space,
           camera angles, geography, sightlines
      ↓
  5. CAMERA TEST — place character proxy, test shot list.
           "What the camera never sees doesn't need to exist."
      ↓
  6. ASSET TIER DIVISION — classify every element:
       Tier 1 (hero geometry): full 3D
       Tier 2 (modular geometry): model once → duplicate
       Tier 3 (2.5D elements): image planes + parallax
       Tier 4 (pure atmosphere): composite FX
      ↓
  7. AI 3D — generate individual hero props and modular pieces
      ↓ unload
  8. BLENDER — assemble canonical environment + procedural duplication
      ↓ render passes
  9. COMFYUI — texture/style/atmosphere/weathering over Blender passes
      ↓ unload
  10. BLENDER — final camera + animation + composite
  ```

- **Depends-on:** `production-pipeline-asset` (for Tier 1/2 assets),
  `production-plan-scene`, `production-operate-blender`,
  `production-operate-comfyui`, `production-orchestrate-gpu`

#### `production-pipeline-screenplay`

- **Component kind:** skill
- **Governance domain:** production
- **Boundary:** The Writing Department workflow from §5.1. Pure text
  reasoning — no GPU, no external tools.
- **Pipeline:**

  ```text
  IDEA / EMOTIONAL INTENT
      ↓
  SCENE THESIS → CHARACTER OBJECTIVES → DRAMATIC QUESTION →
  BEATS → REVERSAL → SUBTEXT → PHYSICAL BEHAVIOR →
  DIALOGUE → DIRECTOR PASS → SHOT OBJECTS
  ```

- **Key rule:** Write beats before dialogue. Each beat answers "What
  changed?" Four layers enforced: A (Story) → B (Drama) → C (Direction) →
  D (Realization). The LLM must not skip layers.
- **Depends-on:** None (pure text, uses standard Work Object write)

#### `production-pipeline-performance`

- **Component kind:** skill
- **Governance domain:** production
- **Boundary:** The Performance/Audio Department workflow from §5.2. Voice
  identity to canonical audio.
- **Pipeline:**

  ```text
  CHARACTER INTENT → VOICE BIBLE → PERFORMANCE TRANSLATOR (LLM) →
  TTS (tiered) → TAKES A/B/C/D → DIRECTOR SELECTS →
  CANONICAL AUDIO → AUDIO LOCK
  ```

- **Audio lock gate:** Shot cannot advance past audio-lock state without an
  approved take. This gates animation work.
- **Depends-on:** `production-operate-tts`

#### `production-pipeline-animatic`

- **Component kind:** skill
- **Governance domain:** production
- **Boundary:** Shot assembly into a watchable animatic with audio. Editorial
  workflow from §7 V5.
- **Pipeline:**

  ```text
  SHOT TIMELINE (ordered shots with timing from audio lock) →
  RENDERS + AUDIO → ffmpeg ASSEMBLY → REVIEW SURFACE (HTML) →
  DIRECTOR ANNOTATIONS → annotations become [system] evidence
  in shot Work Objects
  ```

- **Depends-on:** `production-pipeline-shot` (for renders),
  `production-pipeline-performance` (for audio)

#### `production-harvest-precedent`

- **Component kind:** skill
- **Governance domain:** production
- **Boundary:** Extracts Recipe/Revision/TastePrinciple records from closed
  Work Objects into the precedent ledger (§5.5 v0). Reads Decision trails,
  emits structured records into the Component-Ledger-pattern index.
- **Already validated:** The manual tracer (R-001, R-002 in
  `precedent-ledger.md`) proved the extraction is viable. This skill
  automates that extraction.
- **Depends-on:** Closed Work Objects with `[decision]` entries

---

## 4. Production Operating Pipeline

### 4.1 Layer A — Creative Routing Spine

A routing spine that decides which production skill owns the current creative
question. Follows the same pattern as `BUSINESS-OPERATING-PIPELINE.md` and
`ENGINEERING-OPERATING-PIPELINE.md`.

**Stored at:** `references/PRODUCTION-OPERATING-PIPELINE.md`

#### Pipeline distinction

| Pipeline | Owns | Does not own |
|----------|------|--------------|
| Work Object lifecycle | Work state: notice → explore → design → build → verify → release → observe → close. | Production-domain judgment by itself. |
| Production operating pipeline | Cross-production routing from screenplay through scene planning, asset creation, shot production, environment assembly, animatic, and review. | Lifecycle state transitions, GPU resource scheduling, or external tool mutation. |
| GPU execution protocol | VRAM slot claims, sequential load/unload discipline, tool operator coordination. | Creative decisions, asset selection, or shot evaluation. |

#### Canonical route

```text
production-pipeline-screenplay
→ production-pipeline-performance
→ production-pipeline-asset
→ production-plan-scene
→ production-compose-blocking
→ production-pipeline-environment
→ production-pipeline-shot
→ production-critique-visual
→ production-pipeline-animatic
→ production-harvest-precedent
→ governance-govern-scorecards
→ governance-review-outcome-and-adapt
→ production-pipeline-screenplay when evidence changes the scene plan
```

Use this order as a default route map, not a mandatory sequence. Enter at
the first skill that owns the current production frontier, then route to the
next skill only when the evidence exposes that downstream question.

#### Ownership map

| Production frontier | Owning skill |
|---------------------|--------------|
| Scene thesis, beats, dramatic questions, reversals, subtext, 4-layer screenplay, beats-before-dialogue | `production-pipeline-screenplay` |
| Character voice identity, performance translation, TTS takes, audio lock | `production-pipeline-performance` |
| Asset concept → 3D canon, asset funnel, asset registry, modular kit design | `production-pipeline-asset` |
| Shot interpretation, asset retrieval, scene specification, camera/lighting from intent | `production-plan-scene` |
| Camera mathematics, composition geometry, character blocking, depth staging, visual weight | `production-compose-blocking` |
| Environment blockout, camera test, tier division, modular assembly, 2.5D layers | `production-pipeline-environment` |
| Shot production by tier (A/B/C), Blender→ComfyUI pass pipeline, variant generation | `production-pipeline-shot` |
| Rendered output evaluation, PRESERVED/CHANGED/PROPOSED reporting, feedback loop | `production-critique-visual` |
| Shot timeline, audio+render assembly, animatic review surface, per-shot annotation | `production-pipeline-animatic` |
| Recipe/Revision extraction, precedent library maintenance, counter-example harvesting | `production-harvest-precedent` |
| Production scorecard, reliability trend, recurring pipeline gap | `governance-govern-scorecards` and `governance-review-outcome-and-adapt` |

#### Handoff rules

1. Stay inside the same Work Object when the next production question is part
   of the same bounded creative decision and does not need separate ownership,
   acceptance evidence, or authority.
2. Create a linked Work Object when the next question has a different owner,
   consequence, sensitivity, material acceptance criteria, or production path
   (e.g., a new asset needed for a shot gets its own WO, linked via
   `ws relation`).
3. Route to the conductor for any lifecycle transition, History entry,
   Evidence ledger entry, successor Work Object, authority record, or
   canon-establishing boundary.
4. Treat canon approval, audio lock, asset lock, shot approval, Blender
   arbitrary Python execution, and any write to the asset registry as gated
   actions requiring scoped authority.
5. Do not let a later-stage skill silently settle an earlier-stage creative
   assumption. If downstream evidence (a render that doesn't work, a blocking
   layout that fails camera test) contradicts upstream decisions (the scene
   plan, the screenplay), route back to the owning skill and preserve the
   contradiction.

### 4.2 Layer B — GPU Execution Graph

A resource-aware execution protocol that manages the VRAM time-share. This
is NOT a skill-routing spine. It is an orchestration protocol that the
tool-operator skills use to claim and release the GPU.

`[inference]` This is a genuinely new pattern. Neither the business nor
engineering operating pipeline manages contended hardware resources. The
closest existing precedent is the protocol component kind (like COMP-036,
`BUSINESS-OPERATING-PIPELINE.md`), but the execution graph has state
(current VRAM occupant) that the routing spines do not.

#### State machine

```text
States:
  IDLE                    — no GPU-heavy process loaded
  BLENDER_LOADED          — Blender scene in VRAM
  COMFYUI_FLUX_LOADED     — Flux Dev FP8 in VRAM (~8-10 GB)
  COMFYUI_HUNYUAN_LOADED  — Hunyuan3D-2 in VRAM (~5 GB)

Transitions:
  claim(blender)    — if IDLE: load → BLENDER_LOADED
                    — if other: unload current → load → BLENDER_LOADED
  claim(comfyui_flux) — same pattern
  claim(comfyui_hunyuan) — same pattern
  release(any)      — unload → IDLE

Invariant: exactly one state at any time. No concurrent claims.
```

#### Production cycle sequences

**Asset creation (from §5.4):**
```text
IDLE → claim(comfyui_flux) → generate concepts → release
     → claim(comfyui_flux) → generate reference set → release
     → claim(comfyui_hunyuan) → generate 3D mesh → release
     → claim(blender) → import + cleanup → release
```

**Environment production (from §5.4):**
```text
IDLE → claim(comfyui_flux) → environment concepts → release
     → claim(blender) → blockout + camera test → release
     → claim(comfyui_hunyuan) → hero asset 3D gen → release
     → claim(blender) → assemble + render passes → release
     → claim(comfyui_flux) → texture/style pass → release
     → claim(blender) → final composite → release
```

**Shot production Tier B (from §5.3):**
```text
IDLE → claim(blender) → scene layout + render passes → release
     → claim(comfyui_flux) → appearance variants → release
     → claim(blender) → final render → release
```

#### Runtime graph projection

`[inference]` The GPU execution graph can be projected into the runtime's
NetworkX graph alongside the creative routing spine, using the same code path
as WO `2026-08-22-016`. The GPU states become nodes; the transitions become
edges annotated with the requesting operator and estimated VRAM cost. This
makes GPU state visible to the conductor.

**Open question:** The current runtime graph projection (WO `2026-08-22-016`)
may assume a DAG. The production creative routing spine has a feedback loop
(render → critique → adjust → re-render). Before building the production
graph projection, verify whether the existing NetworkX code handles cycles.
If not, either exclude the feedback loop from the graph (model it as an
internal concern of `production-critique-visual`) or extend the graph code.

---

## 5. Asset Registry

The Scene Planner needs a structured index of available `.blend` files to
select from. This is the "asset vocabulary" that makes LLM scene assembly
practical — the LLM selects from known assets rather than procedurally
modeling everything.

### 5.1 Registry structure

`[inference]` The asset registry follows the Component Ledger pattern
(`.work-studio/component-ledger.md`, ADR 0014): a single derived Markdown
index with one entry per canonical 3D asset.

**Stored at:** `.work-studio/asset-registry.md`

```markdown
## ASSET-001 — apartment_modern_01

- **status:** canonical
- **category:** environment
- **file:** assets/environments/apartment_modern_01.blend
- **dimensions:** 8m × 6m × 3m
- **origin:** WO 2026-XX-XX-XXX Decision N
- **contains:** floor, walls, window, door, ceiling
- **compatible_with:** character_female_01 (scale verified)
- **known_limits:** no kitchen geometry, single room only
```

### 5.2 Population order

The registry starts empty. `production-pipeline-asset` populates it as each
asset is canonized. Early production work must create assets before assembling
scenes — the build order (§6) reflects this dependency.

### 5.3 Asset directory structure

```text
assets/
  environments/
    apartment_modern_01.blend
    city_street_01.blend
  props/
    couch_01.blend
    table_01.blend
    lamp_01.blend
  characters/
    protagonist.blend
  lights/
    sunlight_hard.blend
    window_softbox.blend
  modular_kits/
    architecture_kit_01/
      window_a.blend
      window_b.blend
      column_a.blend
      wall_a.blend
```

---

## 6. Build Order

Each step is a self-contained deliverable. No step depends on capabilities
from a later step. The order respects both the tool dependency chain (nothing
uses Blender without the operator) and the data dependency chain (nothing
assembles scenes without assets).

### Step 1 — Domain registration and protocol

| Component | What | Grounded in |
|-----------|------|-------------|
| `domain: production` | Add to domain vocabulary | Existing `ws domain sync` pattern |
| `PRODUCTION-OPERATING-PIPELINE.md` | Routing spine reference document | `BUSINESS-OPERATING-PIPELINE.md` pattern |
| `production-orchestrate-gpu` | GPU VRAM protocol | §2.4 GPU time-share + TDR crash evidence |
| Scene/Shot/Direction templates | Body section conventions | §3.2, §3.3, §2.2 |

**Exit criteria:** `ws domain sync` generates `production.md`. The pipeline
reference document exists. The GPU protocol is documented.

### Step 2 — Tool operators

| Component | What | Grounded in |
|-----------|------|-------------|
| `production-operate-blender` | Bounded Blender API skill | §4.2 tool surface + BCC pattern |
| `production-operate-comfyui` | ComfyUI API skill | Already running on `:8188` |
| `production-operate-tts` | Tiered TTS API skill | §5.2 audio tiers |

**Exit criteria:** Each operator can execute its tool surface through the
GPU protocol. Blender can import a mesh, set a camera, render a preview.
ComfyUI can submit a workflow and retrieve output. TTS can generate a take.

### Step 3 — Asset pipeline

| Component | What | Grounded in |
|-----------|------|-------------|
| `production-pipeline-asset` | Asset creation funnel | §5.4 + R-001/R-002 validated recipes |
| Asset registry | `.work-studio/asset-registry.md` | Component Ledger pattern |

**Exit criteria:** One prop runs through the full funnel: concept → reference
set → 3D mesh → Blender cleanup → critic check → director approval → canon.
The asset appears in the registry.

### Step 4 — Scene intelligence

| Component | What | Grounded in |
|-----------|------|-------------|
| `production-compose-blocking` | Mathematical composition | §4, reference analysis |
| `production-plan-scene` | Scene specification from intent | §4 six jobs, reference analysis |
| `production-critique-visual` | Visual feedback loop | DeepSeek V4 Flash Vision (§1.7) |

**Exit criteria:** A director's natural-language shot description produces a
structured scene specification. The specification is executed through the
Blender operator. The preview is critiqued. An adjustment is computed and
re-rendered.

### Step 5 — Shot and environment pipelines

| Component | What | Grounded in |
|-----------|------|-------------|
| `production-pipeline-shot` | Tier-routed shot production | §5.3 shot tiers |
| `production-pipeline-environment` | 10-step environment workflow | §5.4 environment production |

**Exit criteria:** One environment (the alley from §7 V4 tracer) and three
shots (SH010 wide, SH020 walk, SH030 close) work end-to-end. The full
ComfyUI→Blender→ComfyUI→composite cycle is proven. GPU sequential load/unload
is tested.

### Step 6 — Writing and performance

| Component | What | Grounded in |
|-----------|------|-------------|
| `production-pipeline-screenplay` | 4-layer screenplay workflow | §5.1 Writing Department |
| `production-pipeline-performance` | Voice → audio lock pipeline | §5.2 Performance Department |

**Exit criteria:** A scene has a 4-layer screenplay. A character has a voice
bible. Multiple takes are generated. Audio lock gates shot advancement.

### Step 7 — Editorial and precedent

| Component | What | Grounded in |
|-----------|------|-------------|
| `production-pipeline-animatic` | Shot assembly + review | §7 V5 |
| `production-harvest-precedent` | Automated recipe extraction | §5.5 v0 + precedent ledger tracer |

**Exit criteria:** An assembled animatic is watchable with per-shot
annotations. The harvester extracts at least one recipe from a closed WO
without human intervention.

### Step 8 — Runtime graph projection

| Component | What | Grounded in |
|-----------|------|-------------|
| Production graph projection | NetworkX projection of routing spine + GPU states | WO `2026-08-22-016` pattern |

**Exit criteria:** The runtime can parse `PRODUCTION-OPERATING-PIPELINE.md`
into a deterministic production route, build a graph, and route a
plain-language production frontier to an owning skill.

---

## 7. Component Ledger Entries

New components to register in `.work-studio/component-ledger.md`. All enter
as `active` with `last-grilled-SHA: not-yet-grilled`.

| ID | Name | Kind | Domain | Depends-on |
|----|------|------|--------|------------|
| COMP-041 | GPU orchestration protocol | protocol | production | COMP-001, COMP-002 |
| COMP-042 | Blender operator | skill | production | COMP-001, COMP-002, COMP-041 |
| COMP-043 | ComfyUI operator | skill | production | COMP-001, COMP-002, COMP-041 |
| COMP-044 | TTS operator | skill | production | COMP-001, COMP-002 |
| COMP-045 | Scene planner | skill | production | COMP-001, COMP-002, COMP-046 |
| COMP-046 | Blocking composition | skill | production | COMP-001, COMP-002 |
| COMP-047 | Visual critic | skill | production | COMP-001, COMP-002 |
| COMP-048 | Asset pipeline | skill | production | COMP-001, COMP-002, COMP-042, COMP-043, COMP-041, COMP-047 |
| COMP-049 | Shot pipeline | skill | production | COMP-001, COMP-002, COMP-045, COMP-042, COMP-043, COMP-047 |
| COMP-050 | Environment pipeline | skill | production | COMP-001, COMP-002, COMP-048, COMP-045, COMP-042, COMP-043 |
| COMP-051 | Screenplay pipeline | skill | production | COMP-001, COMP-002 |
| COMP-052 | Performance pipeline | skill | production | COMP-001, COMP-002, COMP-044 |
| COMP-053 | Animatic pipeline | skill | production | COMP-001, COMP-002, COMP-049, COMP-052 |
| COMP-054 | Precedent harvester | skill | production | COMP-001, COMP-002 |
| COMP-055 | Production operating pipeline | protocol | production | COMP-001, COMP-002, COMP-041 through COMP-054 |

---

## 8. Constraints

| Constraint | Source | Status |
|------------|--------|--------|
| File-first: every artifact is a local file | WO `2026-08-23-001` Decision 2 | Active |
| Blender owns spatial truth | WO `2026-08-23-001` §0 | Active |
| LLMs propose; human establishes canon | WO `2026-08-23-001` §0 | Active |
| Intent and implementation remain separate | WO `2026-08-23-001` §2.3 | Active |
| Sequential VRAM: one GPU-heavy process at a time | WO `2026-08-23-001` §2.4 + TDR evidence | Active |
| Bounded Blender API: no arbitrary Python without director escalation | WO `2026-08-23-001` §4.2 | Active |
| Capture-at-generation for precedent library | WO `2026-08-23-001` §5.5 | Active |
| Camera-proves-existence: don't build what the camera can't see | WO `2026-08-23-001` §5.4 | Active |
| No hosted/cloud generation dependency | WO `2026-08-23-001` Decision 2 | Active |
| DeepSeek V4 Flash Vision is a cloud dependency (no local fallback) | WO `2026-08-23-001` Decision 10 | Active |

---

## 9. Current Blockers

| Blocker | Impact | Resolution path |
|---------|--------|-----------------|
| Blender MCP bounded tool API does not exist yet | Step 2 (tool operators) blocked | Build as Blender add-on, BCC pattern |
| Asset registry is empty | Step 4+ (scene assembly) produces nothing useful | Step 3 (asset pipeline) populates it first |
| Runtime graph cycle support unverified | Step 8 (graph projection) may need code changes | Check existing NetworkX projection code |
| TTS API choice not yet made | Step 2 `production-operate-tts` partially blocked | Can build with local TTS first (Tier 1) |

---

## 10. Automation Potential Summary

From the reference analysis, grounded in the Director Console's instrument
set. This table guides which skills invest in full automation vs. which stay
as director-assisted tools.

| Task | Automation | Owning skill |
|------|-----------|--------------|
| Asset selection from registry | Very high | `production-plan-scene` |
| Scene organization | Very high | `production-plan-scene` |
| Object placement | Very high | `production-plan-scene` + Blender operator |
| Camera creation and setup | Very high | `production-compose-blocking` + Blender operator |
| Camera blocking | High | `production-compose-blocking` |
| Lighting setup from intent | High | `production-plan-scene` |
| Background/2.5D cards | Very high | `production-pipeline-environment` |
| Material assignment | High | Blender operator |
| Character placement | Very high | `production-plan-scene` |
| Rough posing | Medium-high | `production-plan-scene` + Blender operator |
| Animation blocking | Medium-high | `production-plan-scene` |
| Procedural environment assembly | High | `production-pipeline-environment` |
| Complex organic modeling | Medium | Asset pipeline (AI 3D generation) |
| Hero character sculpting | Low | Manual + asset pipeline for base mesh only |
| Artistic final polish | Low-medium | Director-driven, ComfyUI assists |

---

## Provenance

- `[system]` WO `2026-08-23-001` §0, §1.7, §2.2-2.4, §3.1-3.4, §4, §4.2,
  §5.1-5.5, §6.4, §7 V0-V6, §8, §9, §10: Director Console implementation
  plan (accepted architecture, not forecast)
- `[system]` `references/BUSINESS-OPERATING-PIPELINE.md` (COMP-036): routing
  spine pattern
- `[system]` `references/ENGINEERING-OPERATING-PIPELINE.md`: routing spine
  pattern
- `[system]` `.work-studio/component-ledger.md`: component registration
  pattern (ADR 0014)
- `[system]` `.work-studio/precedent-ledger.md` R-001, R-002: validated
  recipes on RTX 3080
- `[system]` WO `2026-08-22-016`: runtime graph projection pattern
- `[system]` WO `2026-08-23-002`: TDR crash evidence under GPU load
- `[system]` Domain system: `ws domain sync`, 9 existing domains
- `[system]` Design-asset pipeline: `*.asset.md` structured records
- `[testimony]` Reference analysis (2026-08-24): LLM-driven Blender scene
  assembly, six-job Scene Planner, visual feedback loop, asset vocabulary,
  automation potential by task type
- `[inference]` Three-layer architecture (operators / intelligence /
  pipelines), GPU execution graph as new pattern, asset registry as
  Component Ledger extension, build order, COMP-041 through COMP-055
  registration — all synthesis of the above sources
