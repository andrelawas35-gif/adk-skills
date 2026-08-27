---
schema_version: 1
id: 2026-08-24-022
title: Build environment production pipeline skill with 10-step assembly workflow
type: change
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [production]
created_at: 2026-08-25T01:57:08Z
updated_at: 2026-08-26T07:44:07Z
next_action: verify-release-evidence: independent second run of the steps 1-5 pass (or its recorded fallback) + executor-surface regression + validate baseline











---
## Intent

Assemble and manage reusable environments (sets) from registered assets.
Follows a 10-step workflow: load base scene → place ground/terrain → add
architectural elements → populate props → set lighting rig → configure
atmosphere/fog → place cameras → set render passes → save as environment
template → register in asset registry. Environments are reusable across
multiple shots.

Parent: WO `2026-08-23-001` §5.6. Component: COMP-050.

## Success evidence

- [ ] Can assemble an environment from registered assets via Blender operator
- [ ] Follows the 10-step assembly workflow
- [ ] Saves completed environments as reusable .blend templates
- [ ] Registers environment templates in the asset registry
- [ ] Environment can be loaded and customized per-shot by scene planner


## Constraints and non-goals

**Constraints:**
- Only uses registered assets — cannot fabricate geometry inline
- Must save as template, not as one-off scene
- Lighting rigs are presets, not per-shot custom (per-shot adjustment is scene planner's job)

**Non-goals:**
- No procedural terrain generation (future capability)
- No weather simulation
- No per-shot camera placement (belongs to scene planner)

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Adopt generation-inclusive scope (parent-plan COMP-050), sequenced generation-stages-first

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | COMP-050 boundary: this WO owns the full 10-step environment workflow per deliverable `2026-08-23-001-production-skill-architecture-implementation-plan.md` §545–584 (ComfyUI concepts → director selection → environment-language extraction → Blender blockout → camera test → asset tier division → AI 3D pieces → canonical assembly + procedural duplication → ComfyUI texture/atmosphere over passes → final composite). Implementation order: generation stages (steps 1–7) first, assembly stages (8–10) after. The original Intent's assembly-only 10-step is superseded by this decision; Intent and Success evidence sections are retained as the original capture and must be reconciled during design. |
| **Authorization** | Director instruction "add generation stages first" (2026-08-26), responding to pressure-test recommendation of Branch A |
| **Confidence** | medium — basis: component ledger and parent plan directly define COMP-050 as generation-inclusive; against: three shipped skills (asset-pipeline, visual-critic, shot-pipeline) already own adjacent stages, so consolidation risk is real but accepted by director choice |
| **Actor** | human (director) |
| **Revisit trigger** | If per-asset generation via `production-operate-asset-pipeline` proves sufficient in practice and stage duplication causes maintenance drag, de-scope back to an assembly-only successor. Also revisit if boundary overlap with WO `2026-08-25-008` cannot be reconciled at design time. |
| **Rationale** | Director chose department-level consolidation over separation-of-concerns after seeing both branches. Alternatives considered: Branch A (assembly-only, high confidence, recommended by agent — rejected), Branch C registry-first split (invalidated: asset registration mechanism already exists in `full_pipeline.py` run_registered_stage), Direction D library-link composition (mechanism-level, carried into design as an option, not a scope branch). Edge cases noted at confirmation: step-2 DIRECTOR SELECTS gate means no unattended end-to-end runs (need live approval or pre-approved direction reference); front half assumes ComfyUI workflows can generate environment concepts, not just character/prop lanes `[inference]`; steps 9–10 overlap shot-pipeline territory and need explicit reconciliation in design. |

### Decision 2 — Accepted tracer bullet: one-alley front-half pass (steps 1–5), translation-seam-first

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Smallest end-to-end slice of Decision 1's front half on one alley: hand-author one Flux txt2img workflow JSON → generate 8 alley concepts via `production-operate-comfyui` → director selects one → extract environment language into a structured spec file → minimal `tools/production/environment/blockout.py` compiles the spec into existing blender_operator queue commands → camera-test renders from 2 angles. Tests the riskiest assumption: extracted environment language carries enough structure for a deterministic translator to place blockout geometry that reads as the same environment, without freeform scene code. Primitive-gap resolved at implement stage whichever is cheapest: one new bounded `mesh.add_primitive` op or an imported unit-cube placeholder asset. |
| **Authorization** | Director accepted the proposed tracer bullet verbatim ("accept this tracer bullet", 2026-08-26). Local-only authority; GPU slot claimed/released sequentially (`comfyui_flux`, then `blender`); scratch outputs only; no registry writes, no skill registration, no adapter changes. |
| **Confidence** | medium-high — basis: both operators individually live-proven `[system]`; the cross-operator translation seam itself is untested, which is exactly what this tracer measures |
| **Actor** | human (director) |
| **Revisit trigger** | If blockout renders do not read as the selected concept's environment, return to pressure-test on the spec schema before any further build-out. |
| **Rationale** | Buys evidence on the one unproven seam while reusing proven machinery. Failure behavior: if no checkpoint/workflow runs, skip step 1 with a director-supplied concept image and still test the translation seam, recording why as [system] evidence. Observability: concept PNGs, spec file, queue command log, blockout renders, COMP-041 claim/release entries. Non-goals: steps 6–10, template save/registry, procedural duplication, packaging/adapters, per-shot cameras. Rollback: delete scratch artifacts + blockout.py; zero durable state. Exit criteria: blockout renders read as the same environment to the director's eye beside the selected concept. Trade-off accepted: hand-authored workflow JSON proves submission/output, not workflow-engineering craft. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [decision] | WO Decision 1; director instruction 2026-08-26 | Director adopted generation-inclusive COMP-050 scope (parent plan sections 545-584), sequenced generation-stages-first, superseding assembly-only Intent; Intent/Success-evidence retained as original capture, reconciliation owed at design. |
| [decision] | WO Decision 2; director verbatim acceptance 2026-08-26 | Tracer bullet accepted verbatim: one-alley steps 1-5 front-half pass (Flux concepts via ComfyUI operator -> director selection -> environment-language spec -> blockout.py -> 2-angle camera test); local-only authority; sequential GPU slots comfyui_flux then blender; scratch outputs only; rollback = delete scratch artifacts + blockout.py. |
| [gap] | orchestrate read-only git status + file inspection, 2026-08-26 | tools/production/environment/ existed UNTRACKED on the accepted tracer path (blockout.py 7.8KB self-identifying as this WO Decision 2 + __init__.py + pycache), no History/evidence recording its creation, and required unit_cube.obj placeholder absent from repo. Director disposition: DELETE AND RESTART per Decision 2 rollback definition; primitive-gap choice reverts to open for the fresh implementation pass. All 11 executor ops referenced by the deleted code verified present in executor.py + governance allowlist (read-only check). Also noted: .work-studio/temp-engineering-implement-bounded-change-sketch.md concerns unrelated WO 2026-08-25-003 - out of scope. |
| [system] | implement-bounded-change Decision 2 run, 2026-08-26 | One-alley steps 1-5 tracer PASS (director-qualified). STEP 1: Flux weights located in diffusion_models after CheckpointLoaderSimple enumeration gap (director correction: flux1-krea-dev_fp8_scaled + clip_l + t5xxl_fp16 + ae.safetensors confirmed on disk); 8 alley concepts generated via ComfyUI operator under comfyui_flux GPU claim discipline, 8/8 OK. STEP 2: director selected concept_03 (Mediterranean alley). STEPS 3-4: environment-language spec extracted to scratch spec.json (ground/walls/doors/shutters/steps/pots/bougainvillea masses, materials, cameras); fresh blockout.py compiled spec to EXISTING executor ops only (import_mesh unit-cube placeholder = primitive-gap option b, set_transform, mesh.set_dimensions, material.set/assign, light.set, camera.set, render.final). STEP 5: two camera-test renders. DEFECT TRAIL: (1) OBJ importer bakes 90-deg X rotation - masses initially stood on their faces; fixed by zeroing rotation_deg per mass. (2) material.set is viewport-only - renders gray by design, accepted per director (production flow is 2D -> Hunyuan3D/other image-to-3D -> Blender; gray massing is the read). (3) point-light falloff unreadable; director granted scoped authority for one execute_blender_python sun-lamp one-liner (SUN type, energy 3, fixed rotation), recorded in command params authority{granted_by: director, work_object: 2026-08-24-022}. (4) prior uncheckpointed blockout.py deleted by director authority before this fresh pass. EXIT: blockout renders read as the same environment per director eye judgment (pass for now, qualified). blockout.py promoted to tools/production/environment/. Scratch artifacts in Temp/opencode/ws-env-tracer (concepts, spec, cube asset, renders). |
| [gap] | ws transition audit (verify) | Unresolved [gap] entries exist in the Evidence ledger. Residual uncertainty should be reviewed before proceeding. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

- Which scope does COMP-050 own: this WO's assembly-only intent (registered
  assets in, template out) or the parent plan's generation-inclusive 10-step
  (ComfyUI concepts → blockout → tier division → AI 3D → composite)?
  If the latter, the Intent section needs a successor-level amendment.
- Who owns creating `.work-studio/asset-registry.md`? The registry does not
  exist yet (`[system]` glob, 2026-08-26); `production-operate-asset-pipeline`
  explicitly routes registration elsewhere. Every direction below depends on
  registered assets existing.
- Shared executor gap, independent of direction: `blender_operator` has no
  save/save-as op and no library link/append/collection ops — any direction
  requires new bounded executor surface (`[system]` grep of executor.py,
  2026-08-26).

## Directions

Generated 2026-08-26 by develop-idea. Grounding: parent deliverable
`2026-08-23-001-production-skill-architecture-implementation-plan.md`
§545–584 (COMP-050 pipeline) and §818–840 (asset registry); verified
COMP-042 tool surface; component-ledger COMP-050 depends-on.

### Direction 1: Assembly-only template builder (WO as written)

- **Core idea**: Build the skill exactly per this WO's Intent — a new
  `tools/production/environment` module driving `blender_operator` through
  the fixed 10 assembly steps (base scene → ground → architecture → props →
  lighting preset → atmosphere → cameras → render passes → save template →
  register), consuming only registered assets, emitting reusable `.blend`
  templates plus registry entries.
- **Distinctness claim**: Excludes all ComfyUI/generation stages; treats
  concept selection, blockout, and tier division as upstream inputs from
  other skills; its only outputs are templates + registrations.
- **Key assumption**: A populated asset registry (or at least seed registered
  assets) will exist to draw from when this ships.
- **Smallest test**: Register two trivial assets (ground plane, one prop),
  assemble them into one environment through the Blender queue, save as
  `.blend` template, register it, reload it into a fresh scene.

### Direction 2: Full parent-plan COMP-050 (generation-inclusive)

- **Core idea**: Amend this WO toward the parent plan's complete 10-step —
  ComfyUI concept generation → director selection → environment-language
  extraction → Blender blockout → camera test → asset tier division → AI 3D
  pieces → canonical assembly with procedural duplication → ComfyUI
  texture/atmosphere over passes → final composite.
- **Distinctness claim**: Includes GPU stages and director-in-the-loop gates
  that Direction 1 treats as out of scope; produces finished environments,
  not just reusable templates; heaviest dependency load (COMP-041/043/047).
- **Key assumption**: The studio wants the whole environment department
  workflow in one skill now, accepting director gates at steps 2 and the GPU
  claim/release cycle across three model loads.
- **Smallest test**: Run steps 1–5 on one alley concept: ComfyUI generates
  concepts, director selects one, LLM extracts environment language, a
  blockout is assembled, camera test renders — proving the front half before
  any assembly backend.

### Direction 3: Registry-first split (infrastructure before engine)

- **Core idea**: Treat the true blocker as the missing registry: define the
  environment-template record schema (Component Ledger pattern, extending or
  sitting beside the planned `.work-studio/asset-registry.md`), plus minimal
  save/register/load tooling — and defer full assembly automation to a
  successor once real registered assets exist.
- **Distinctness claim**: Ships the data model and persistence contract
  first, the smallest build surface of the three; unblocks scene planner's
  per-shot customization interface even before rich assembly exists.
- **Key assumption**: The bottleneck is the absent registry/template format,
  not assembly mechanics.
- **Smallest test**: Hand-author one environment-template record for an
  existing `.blend`, load it into a fresh scene via the queue, validate with
  `ws` — round-trip proven with no new assembly code.

### Direction 4: Library-link composition (native Blender linking)

- **Core idea**: Normalize each registered asset as a collection inside a
  library `.blend`; assemble environments by native linked-library append +
  transform overrides + lighting-preset selection rather than per-object
  import/place commands; save the composition as a template.
- **Distinctness claim**: Mechanism-level difference — bets on Blender's
  linking system instead of expanding the per-object executor surface;
  fewer new executor ops but imposes a packaging convention on every
  registered asset.
- **Key assumption**: Registered assets can be normalized to
  collection-per-asset library structure without breaking the existing
  import_mesh-based pipelines.
- **Smallest test**: Package two existing assets as collections in one
  library `.blend`, link both into a fresh scene through the queue, save as
  template.

## Next move

Route to implement-bounded-change: execute the accepted Decision 2 tracer
bullet — one-alley steps 1–5 pass (Flux concepts via ComfyUI operator →
director selection → environment-language spec → blockout.py compiling spec
to existing executor ops → 2-angle camera-test renders), local-only, scratch
artifacts, rollback = delete.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-26T01:49:15Z — activate-for-exploration

- **State:** explore
- **Status:** active
- **Actor:** opencode (ox-alpha)
- **Rationale:** Director routed to conductor after orchestrate classification; WO intent fully specified by parent WO 2026-08-23-001 section 5.4/5.6 and implementation-plan deliverable (production-pipeline-environment, COMP-050). Activating into explore per studio convention for production skill builds; noted scope question for exploration: WO 10-step starts at load-base-scene (assembly-only, registered assets) vs parent plan 10-step starts at COMFYUI concept generation (generation-inclusive).
### 2026-08-26T01:53:16Z — directions-generated

- **State:** explore
- **Status:** active
- **Actor:** opencode (ox-alpha)
- **Rationale:** develop-idea generated 4 directions: (1) assembly-only template builder per WO intent; (2) full parent-plan generation-inclusive COMP-050; (3) registry-first infrastructure split; (4) native Blender library-link composition. Grounded in parent deliverable 545-584/818-840, verified COMP-042 surface, component ledger. Shared findings recorded as Open questions: registry does not exist yet; executor lacks save/link/collection ops for all directions. Awaiting director selection.
### 2026-08-26T01:59:51Z — Decision 1 recorded: generation-inclusive COMP-050 adopted

- **State:** design
- **Status:** active
- **Actor:** opencode (ox-alpha)
- **Rationale:** Director chose Branch B (add generation stages first) over recommended Branch A. Scope now spans parent-plan steps 1-10 sequenced front-half first; assembly-only Intent superseded pending design reconciliation. Routing to design-tracer-bullet.
### 2026-08-26T02:02:50Z — Decision 2 recorded: tracer bullet accepted (one-alley steps 1-5)

- **State:** build
- **Status:** active
- **Actor:** opencode (ox-alpha)
- **Rationale:** Director accepted the proposed tracer bullet. Riskiest assumption: deterministic translation from environment-language spec to blockout geometry reads as same environment. Routing to implement-bounded-change with local-only authority, scratch artifacts, rollback = delete.
### 2026-08-26T06:14:02Z — Authority: AUTH-004 destructive delete of untracked tracer code; ledger seeded; next_action repaired

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director authorized delete-and-restart of untracked tools/production/environment/ per Decision 2 rollback definition (independent-authorization; evidence reviewed: git status, file inspection, executor-surface check). Empty evidence ledger seeded with decision rows; stale next_action from notice state replaced.
### 2026-08-26T07:42:24Z — Tracer implemented + executed: translation seam HOLDS (director-qualified pass)

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Spec-to-blockout seam proven end-to-end on concept_03: ComfyUI Flux concepts -> director selection -> spec -> blockout via existing executor ops -> two camera-test renders read as same environment. Defects found and fixed en route (OBJ rotation, viewport-only materials, sun-lamp authority one-liner). blockout.py promoted to recorded path.
### 2026-08-26T07:44:07Z — Tracer implemented; route to verify-release-evidence

- **State:** verify
- **Status:** active
- **Actor:** system
- **Rationale:** Steps 1-5 pass executed end-to-end with director selection gate honored mid-flow; exit criterion met per director eye (qualified).
