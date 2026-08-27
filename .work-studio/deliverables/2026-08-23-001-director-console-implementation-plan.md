# Director Console — Implementation Plan

> **Deliverable type:** plan
> **Work Object:** `2026-08-23-001`
> **Date:** 2026-08-23
> **Author:** Andre (andrelawas35@gmail.com)
> **Synthesizes:** Decision 1 (combined Direction 1+3), Decision 2 (grilling
> outcome: constraint narrowed, instruments named), Decision 3 (tracer
> validated retroactively by `2026-08-23-007`'s real execution — pass),
> Decision 5 (Creative Precedent Library accepted — adds §5.4 validated
> recipes, §5.5, and edits to §2.4/§4/§6.4), Decision 6 (`ws relation`/
> `ws graph` verified insufficient for the precedent graph; §5.5 storage
> corrected to the Component Ledger pattern), Decision 10 (DeepSeek V4 Flash
> Vision replaces Qwen3.5/Ollama as the reasoning + visual-critique
> instrument; local no-network fallback deliberately given up), `2026-08-24-006`
> Decision 3 (canon registry = lightweight canon record — approved Shot WO +
> Component-Ledger-pattern canon index; §7 V1 canon-registry grounding
> corrected), the
> director's updated system plan `[testimony]`, and the director's 3D asset
> pipeline testimony `[testimony]`.
> **Grounding:** Current Work Studio system (`tools/ws`, skills, governance,
> design assets, command-center/asset-workbench projections) plus the
> `[system]`-verified mechanisms from closed WO `2026-08-23-007`.

This plan synthesizes only already-accepted material. It authors nothing new —
every §5.5 / §5.4-recipe / §2.4 / §4 / §6.4 addition traces to WO
`2026-08-23-001` Decision 5, which accepted them, and to `2026-08-23-007`'s
verified evidence; the §1.7/§2.4/§8/§11 instrument-swap edits trace to
Decision 10.

---

## 0. Governing Principle

Human defines meaning and approves canon. LLMs translate, propose, critique,
and coordinate. Blender owns controllable spatial truth. Generative models
explore appearance and motion. TTS realizes performance. The Console
preserves intent, decisions, versions, and authority.

The Director Console is not an AI that makes the film for you. It is a
governed interface that translates creative intent into controllable writing,
audio, cinematography, animation, image/video generation, and production
workflows — while preserving the director's authority over canon.

---

## 1. What Already Exists (System Evidence)

The Work Studio already provides the backstage the Director Console needs.
The plan builds the frontstage as a new layer over this infrastructure, not
a replacement.

### 1.1 Work Object lifecycle

`python -m tools.ws` — a deterministic CLI that creates, transitions, and
closes Work Objects through an 8-state lifecycle (`notice → explore →
design → build → verify → release → observe → close`). Every mutation
uses optimistic concurrency (`--expect-updated`). History is append-only.
Evidence is tagged (`[system]`, `[testimony]`, `[inference]`, `[decision]`,
`[gap]`, `[memory]`). Decisions are structured records with revisit triggers.

**Console mapping:** The Director Console's Scene Objects, Shot Objects, and
Direction objects are Work Objects or Work Object children. The
`protect/change/propose/approve` pattern maps directly to the existing
`Constraints`, `Decisions`, and `Evidence ledger` sections. The console does
not invent a parallel state system — it uses Work Objects.

### 1.2 Consequence and authority model

Three consequence levels (low/meaningful/high) × three sensitivity classes
(ordinary/private/restricted). High-consequence actions require explicit
human authority. Authority gates enforce that the LLM proposes, the human
approves.

**Console mapping:** The "LLMs propose; you establish canon" rule is the
authority model the studio already enforces. Every canon-establishing act
(selecting a variant, locking a take, approving a shot) is a `[decision]`
recorded with authorization, scope, and revisit trigger.

### 1.3 Evidence model

Tagged evidence with provenance. `[system]` for machine-observed facts,
`[testimony]` for human statements, `[inference]` for derived claims,
`[gap]` for missing evidence. Evidence and History are strictly separated.

**Console mapping:** The "PRESERVED ✓ / CHANGED Δ / PROPOSED ?" reporting
pattern is the evidence model applied to creative work. Every revision
reports what it kept, what it changed, and what it proposes — each tagged
with provenance.

### 1.4 Skills and specialist profiles

45 skills across governance, thinking, research, design, engineering,
operations, and business domains. Each has defined boundaries, required
capabilities, authority rules, and a grilling profile.

**Console mapping:** The 7 specialist profiles (Story Editor, Character
Director, Animation Director, Cinematographer, Art Director, Sound Director,
Critic) are skills in the existing sense — context, rules, evidence, tools,
and permissions, not separate models. They plug into the same conductor
routing that the studio already uses.

### 1.5 Design asset pipeline

`.work-studio/design-assets/` with managed records, a routing pipeline
(`DESIGN-ASSET-PIPELINE.md`), intake/composition/stewardship/application/
verification/component-governance stages, and a validated registry.

**Console mapping:** Visual assets (frames, renders, animatic segments) are
design assets. The existing pipeline handles intake, composition, and
verification without a new system.

### 1.6 Read-only projections

`command-center.html` and `asset-workbench.html` are generated HTML
dashboards — read-only views rendered from `.work-studio/` data. They
never write back. This is the exact pattern the Director Console's
frontstage should follow.

**Console mapping:** The Director Console is the next projection — a richer
HTML interface generated from the same Work Object and design-asset data,
with the addition of artifact rendering, variant comparison, and direction
input. The backstage data model stays exactly what it is.

### 1.7 Hardware and instruments

- **RTX 3080** (10 GB VRAM): Blender rendering, ComfyUI image generation,
  video generation. NOT for running the main LLM during production.
- **ComfyUI Desktop**: running locally on `:8188`, v0.33.3. Currently has
  Flux Dev FP8 (`flux1-krea-dev_fp8_scaled.safetensors`) installed in
  shared `diffusion_models` folder. Fits in 10 GB VRAM.
- **Blender**: installed, scriptable via Python API.
- **API LLM** (Claude, etc.): reasoning, routing, script analysis,
  performance translation, tool calls, structured outputs.
- **DeepSeek V4 Flash Vision** (`deepseek-v4-flash-vision-exp`, cloud API,
  OpenAI-compatible endpoint `https://api.deepseek.com/chat/completions`) —
  visual critique, taste evaluation, and reasoning/routing/classification
  fallback (per WO `2026-08-23-001` Decision 10, replacing the local LLM
  below). Up to 32 MiB inline images, 600 images/request, 384 tokens/image.
  **Note:** this is a cloud dependency, not local — replacing the local LLM
  with it was a deliberate tradeoff giving up the plan's only no-network
  reasoning fallback (Decision 10).
- ~~**Local LLM** (Qwen3.5-9B Q4 via Ollama): offline/fallback worker~~ —
  **removed** (Decision 10). Superseded by DeepSeek V4 Flash Vision above.

---

## 2. Architecture

```text
                         HUMAN
                          YOU
                           │
                meaning / taste / authority
                           │
                           ▼
                   DIRECTOR CONSOLE           ← frontstage (new)
                           │
                           ▼
                      CONDUCTOR               ← backstage (existing)
                           │                     tools/ws + skills
               structured creative intent
                           │
         ┌────────────┬────────────┬────────────┐
         │            │            │            │
         ▼            ▼            ▼            ▼
      WRITING      PERFORMANCE   ASSET        VISUAL
         │            │        PRODUCTION    PRODUCTION
 Screenplay      Voice Bible      │            │
 Beats           TTS Takes    ComfyUI 2D    Blender
 Director Layer  Canon Audio  AI 3D Gen     ComfyUI
         │            │       Blender LLM   Video AI
         │            │       Canon Assets     │
         └────────────┼────────────┼───────────┘
                      ▼            ▼
                        SHOTS
                           │
                           ▼
                       ANIMATIC
                           │
                           ▼
                        DAILIES
                           │
                    specialists critique
                           │
                           ▼
                         YOU
                   approve / revise
                           │
                           ▼
                         CANON
                           │
                           ▼
                     FINAL ARTIFACT
```

### 2.1 Frontstage / backstage split

| Layer | What | Where |
|-------|------|-------|
| **Frontstage** | Director Console UI — artifact view, direction input, variant comparison, scene board, review | New: generated HTML or local web app |
| **Backstage** | Work Objects, evidence, decisions, skills, routing, lifecycle, authority | Existing: `tools/ws`, `.work-studio/`, skills |

The frontstage reads backstage data and writes direction through the
conductor (the existing CLI + skill routing). It never bypasses governance.

### 2.2 Direction object

Every director input becomes a Direction object:

```yaml
direction:
  basis: <what this builds on — current version, variant, scene>
  protect: <what must not change>
  change: <what should change>
  desired_effect: <what the audience should perceive/feel>
  authority: <approve | propose | explore>
```

This is the existing `Constraints` + `Intent` structure from a Work Object,
applied at the granularity of a single creative move. Each Direction is
recorded as `[testimony]` evidence with full provenance.

### 2.3 Intent vs implementation invariant

A system-wide rule enforced by the console:

| Layer | Example | Persists? |
|-------|---------|-----------|
| **Intent** (creative truth) | "Her recognition almost escapes, then she suppresses it." | Yes — canon |
| **Implementation** (hypothesis) | "eyes shift first, breath interruption: 3 frames, head rotation: 3°" | Changes freely |

Intent is stored in Work Object `Intent` sections and Direction objects.
Implementation is stored in Blender scene state, ComfyUI workflows, and
TTS parameters — all editable without losing creative truth.

### 2.4 GPU time-share

10 GB VRAM forces sequential load/unload. Never keep a large image model,
3D generator, and Blender workload resident at once:

```text
API LLM (reasoning) ← runs on cloud, no local GPU
          ↓
DeepSeek V4 Flash Vision (critique/fallback) ← runs on cloud, no local GPU
          ↓
ComfyUI (generation) ← loads diffusion model into VRAM
          ↓ unload
Hunyuan3D (3D gen)   ← loads 3D model into VRAM (~2-4 GB)
          ↓ unload
Blender (render)     ← loads scene into VRAM
          ↓ unload
```

Per Decision 10, there is no longer a local-LLM VRAM step in this cycle — both
reasoning models run on cloud APIs. This simplifies the time-share sequence
(one fewer local load/unload) at the cost of the offline-fallback capability
the Local LLM step previously provided.

**Environment production cycle** (the most demanding workflow):
```text
ComfyUI: concept → unload → Hunyuan3D: assets → unload →
Blender: assemble + render passes → unload →
ComfyUI: texture/style → unload → Blender: final composite
```

The console orchestrates this sequence. Only one GPU-heavy process runs at
a time. The API LLM handles all reasoning without touching the GPU. 32 GB
system RAM assists with offloading between cycles.

**Retrieval-embedding constraint (per Decision 5).** The Creative Precedent
Library's image-similarity retrieval (`find_similar_artifact`, §5.5 v3) needs a
vision-embedding model, which competes for the same contended 10 GB. Two rules:
(1) text/structured retrieval (`find_by_intent`, v1) is GPU-free and ships
first; (2) when image similarity lands, **reuse the `sigclip_vision` model
already installed for Flux Redux** (`2026-08-23-007` Decision 20) rather than
adding a new embedding model — and load/unload it in the same sequential
discipline above. `[system]` evidence from `2026-08-23-002` records two TDR
driver crashes under sustained load, so adding a resident model to this budget
is a real risk, not a theoretical one.

---

## 3. Data Model — Grounded in Work Objects

### 3.1 Project hierarchy

```text
PROJECT (Work Object, type: project)
  ↓
SEQUENCE (Work Object, type: project, relation: child_of)
  ↓
SCENE (Work Object, type: project, relation: child_of)
  ↓
BEAT (section within Scene Work Object)
  ↓
SHOT (Work Object, type: project, relation: child_of)
```

Each level is a real Work Object managed by `tools/ws`. Scenes link to
their sequence via typed relationships (`ws relation`). Shots link to
their scene. The existing `ws graph` command traces the full hierarchy.

### 3.2 Scene Object (extends Work Object)

A Scene Work Object adds these sections to the standard body:

```markdown
## Scene Board

- **Thesis:** Mara tries to hide recognition.
- **Turn:** Leo reveals he may already know.
- **Character state:** Mara: controlled → threatened
- **Audience state:** Leo seems unaware → Leo probably knows
- **Beats:** 01 normal conversation, 02 name mentioned, ...
- **Directorial rules:** restraint, no melodrama, stillness > gesturing

## Screenplay

### Layer A — Story
What happens in this scene.

### Layer B — Drama
Why it happens. What changes. What is withheld.

### Layer C — Direction
What the audience should perceive and feel.

### Layer D — Realization
Camera, performance, sound, timing, lighting, assets.

## Director Layer

| Beat | Screenplay | Director Intent | Performance | Production |
|------|-----------|-----------------|-------------|------------|
| 04 | LEO: "You tell me." / Mara looks down. | Leo tests Mara. Audience realizes he suspects her. | gaze delayed, restrained voice, hand remains still | camera: MC, lens: compressed, audio: market ambience |
```

### 3.3 Shot Object (extends Work Object)

```yaml
# In Work Object frontmatter (extended fields)
shot_id: SQ01_SC03_SH042
tier: B  # A=generative, B=Blender-guided AI, C=hero controlled

# In Work Object body
## Shot Specification

- **Story function:** reveal Leo notices Mara
- **Intent:** audience realizes Leo is testing her
- **Camera:** shot_size: insert, lens: 85
- **Performance:** hand_freezes: subtle
- **Audio:** dialogue: none, ambience: market_v2
- **Continuity:** prop: glass_03, hand: right
- **Protect:** camera, prop, character position
- **Status:** blocking
```

### 3.4 Canon and versioning

Every approved artifact version is recorded as a `[decision]` in the
Work Object's Decisions section:

```markdown
### Decision N — Approve variant C for SC030 beat 04

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Selected variant C (hand stops against the glass) ... |
| **Authorization** | Director: selected C |
| **Rationale** | ... |
```

Asking "Why does this scene look like this?" traces the Decision chain.

---

## 4. Specialist Profiles (Skills)

Each specialist is a skill with context, rules, evidence, tools, and
permissions — not a separate model. They all use the same API LLM.

| Specialist | Skill boundary | Tools |
|------------|---------------|-------|
| **Story Editor** | Scene thesis, beats, dramatic questions, reversals, subtext. Writes beats before dialogue. | File read/write (screenplay files) |
| **Character / Performance Director** | Character objectives, physical behavior, voice performance markup. Translates intent → TTS parameters. | TTS API, voice bible files |
| **Animation Director** | Blender poses, keyframes, timing, motion. Bounded Blender API only. | `scene.get_objects`, `rig.set_bone_rotation`, `animation.move_keyframe`, etc. |
| **Cinematographer** | Camera, lens, framing, lighting reference. Blender camera tools. | `camera.get/set/lock`, `light.get/set`, `render.preview` |
| **Art / Asset Director** | ComfyUI workflows, style, texture, atmosphere. Blender render passes → ComfyUI. **Must capture a Recipe/Revision record at generation time** (intent + recipe + protect/change), per §5.5 — a generation that records nothing does not enter the Creative Precedent Library. | ComfyUI API, Blender pass export, Creative Precedent Library write |
| **Sound Director** | Ambience, music, sound design. Audio file management. | Audio files, mixing tools |
| **Critic / Continuity** | Cross-scene consistency, prop continuity, character state tracking, contradiction detection. | Read-only access to all scene/shot objects |

### 4.1 Productive disagreement

The conductor routes a direction to relevant specialists. Each responds
with their assessment. Contradictions are surfaced, not hidden:

```text
Story Editor: Cut the line.
Character Director: Agree — she'd never say it explicitly.
Cinematographer: The suspicion can be revealed through Leo's eyeline.
→ Director: Cut line. Use eyeline. [decision recorded]
```

### 4.2 Bounded Blender tools

The LLM does not generate arbitrary Python for Blender. It uses a
controlled API:

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

MESH (V3+, for asset cleanup)
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

`execute_blender_python()` remains an escalation path requiring explicit
director authority (high-consequence gate). The mesh tools above are the
bounded surface for LLM-assisted asset cleanup — they cover scale, naming,
separation, retopology, and modifier stacking without exposing arbitrary
Python.

---

## 5. Production Departments

### 5.1 Writing Department

**Workflow:**
```text
IDEA / EMOTIONAL INTENT → SCENE THESIS → CHARACTER OBJECTIVES →
DRAMATIC QUESTION → BEATS → REVERSAL → SUBTEXT → PHYSICAL BEHAVIOR →
DIALOGUE → DIRECTOR PASS → SHOT OBJECTS
```

**Key rule:** Write beats before dialogue. Each beat answers "What changed?"

**Four screenplay layers:**
- **A — Story:** What happens?
- **B — Drama:** Why does it happen? What changes? What is withheld?
- **C — Direction:** What should the audience perceive and feel?
- **D — Realization:** Camera, performance, sound, timing, lighting, assets.

The LLM must not skip layers. Story → Drama → Direction → Realization.

### 5.2 Performance / Audio Department

**Pipeline:**
```text
CHARACTER INTENT → VOICE BIBLE → PERFORMANCE TRANSLATOR (LLM) →
TTS → TAKES A/B/C/D → YOU SELECT → CANONICAL AUDIO → ANIMATION
```

**Voice identity ≠ performance:**
- Voice identity (timbre, accent, age, resonance) = canonical per character
- Performance (pace, stress, breath, pause, volume, pitch, subtext) = varies
  per scene

**Audio tiers:**
| Tier | Use | Cost |
|------|-----|------|
| 1 — Local TTS | Scratch / animatic / exploration | Free (local) |
| 2 — Cheap API TTS | Production dialogue | Low |
| 3 — Best API TTS | Hero emotional performance | Higher |

**Production order:** Script → Voice performance → **Audio lock** → Animatic
→ Blocking → Character animation → Face/lip sync → Polish. Lock audio
before animating to avoid reworking against changing dialogue timing.

### 5.3 Visual Production Department

**Blender owns spatial truth:**
```text
camera, lens, scene geography, character position, blocking,
rig poses, keyframes, timing, lighting reference, depth,
object relationships
```

**ComfyUI owns appearance exploration:**
```text
style, texture, atmosphere, detail, graphic treatment, effects
```

**Blender exports → ComfyUI consumes:**
```text
Blender: beauty, depth, normals, pose, object masks, material IDs, camera metadata
ComfyUI: style, texture, atmosphere, detail, graphic treatment, effects
```

**Shot production tiers:**

| Tier | Lead | Use case |
|------|------|----------|
| **A — Generative** | Video model | Abstract, dream, atmosphere, insert, transition, low continuity |
| **B — Blender-guided AI** | Blender → passes → ComfyUI/video | Majority of shots. Camera + layout + pose → depth/normal/masks → appearance |
| **C — Hero controlled** | Blender full pipeline + AI enhancement | Major emotional or continuity-critical shots |

**Video model as exploration, Blender as truth:**
```text
Video generation: "Show me 6 ways this scene might feel."
YOU: "I like #4."
Blender: reconstruct lens, camera height, blocking, movement, spatial relationship
→ CANONICAL SHOT
```

### 5.4 Asset Production Department

A new department governing 3D asset creation. The governing rule:
**explore generatively before approval; after approval, deterministic tools
take over.** This maps directly to the existing Work Object lifecycle:
`explore` (generate concepts) → `design` (reconstruct as 3D) → `build`
(clean/rig) → `verify` (critic checks) → `canon`.

**Asset creation funnel:**
```text
DIRECTOR INTENT
        ↓
2D EXPLORATION (ComfyUI)
        ↓
YOU APPROVE LOOK
        ↓
REFERENCE SET (front / side / back / 3/4)
        ↓
AI 3D GENERATION (Hunyuan3D / Tripo / local)
        ↓
ROUGH MESH (.glb / .obj)
        ↓
BLENDER (LLM cleanup: scale, separate pieces, materials, naming, retopo)
        ↓
YOU APPROVE
        ↓
CANONICAL 3D ASSET (design asset record)
```

**Grounded in the system:** Each asset gets its own Work Object (type:
project, relation: `child_of` the scene/project it belongs to). The 2D
concept is recorded as `[system]` evidence with `ws append-artifact`. The
director's approval of the look is a `[decision]`. The final canonical 3D
asset is a design asset record in `.work-studio/design-assets/` managed by
the existing pipeline. The Critic/Continuity specialist checks silhouette,
dimensions, and concept similarity before approval.

**Validated recipes (harvested from closed `2026-08-23-007`, WO `2026-08-23-001`
Decision 5).** Two revision/generation methods are `[system]`-verified on the
RTX 3080 10 GB machine and are the Asset Production Department's first entries
in the Creative Precedent Library (§5.5):

1. **Segmentation-masked regional revision** — for changing one region of an
   asset (background clutter, an isolated element) while leaving the rest pixel-
   identical. Method: `rembg` (u2net) generates a silhouette-accurate mask →
   `VAEEncodeForInpaint` (mask, `grow_mask_by: 0`) → Flux
   (`flux1-krea-dev_fp8_scaled`, denoise 1.0, FluxGuidance 3.5) inpaints only
   the masked region. Validated on background-clutter removal (`2026-08-23-007`
   Decision 16). Known limit: thin/wiry elements (e.g. a chain) can be dropped
   by segmentation; and the mask's *scope must match the flaw's scope* — object-
   only masks leave whole-frame flaws half-fixed (`2026-08-23-007` Decisions
   17, 19, now tracked as an open gap in `2026-08-24-003`).
2. **Single-view image-to-3D mesh for turnaround identity** — for any flaw that
   is really "views of this asset must stay consistent." Method: native ComfyUI
   Hunyuan3D-2 (`hunyuan3d-dit-v2.safetensors`, shape-only, ~5 GB, fits 10 GB
   VRAM) generates one 3D mesh from a single background-removed concept image;
   front/back/any view is then a Blender camera rotation of that one mesh, so
   consistency is guaranteed by construction, not by prompt (`2026-08-23-007`
   Decision 24). This is the plan's governing principle ("Blender owns spatial
   truth", §0) applied to turnarounds. Known limit: texture generation needs
   ~20 GB+ VRAM and does not fit — texture separately via Blender-passes →
   ComfyUI (§5.3), not in the mesh stage.

#### Three ComfyUI → Blender paths

| Path | When to use | What happens |
|------|------------|--------------|
| **1. Reference** | Character turnaround refs, costume refs, environment concepts, composition refs, matte plates | ComfyUI PNG → Blender reference image or image plane. Image stays 2D; used to guide 3D construction. |
| **2. AI 3D generation** | Props, vehicles, architectural elements, environment pieces | Approved ComfyUI image(s) → multi-view reference set (2–4 views) → image-to-3D model (Hunyuan3D/Tripo) → .glb/.obj → Blender import → LLM cleanup |
| **3. Direct LLM editing** | Parametric edits, layout, architectural forms, procedural geometry, object assembly, modifiers, scene organization | LLM translates director intent into bounded Blender tool calls — geometry edits, not sculpting |

**What LLM + Blender is good for:**
```text
primitive modeling, layout, architectural forms, procedural geometry,
object assembly, modifiers, parametric edits, scene organization,
asset placement, camera setup, material assignment, simple prop creation
```

**What it is NOT for (use AI 3D generation or purchased assets instead):**
```text
hero character sculpting, organic topology, high-end character anatomy,
hair grooming, subtle clothing folds, hero-quality deformation topology
```

#### Environment production workflow (hardware-aware)

Building an environment on a 10 GB 3080 means generating the pieces that
benefit from generation, not "the environment" in one shot. The workflow
cycles between ComfyUI and Blender, loading/unloading each from VRAM
sequentially:

```text
1. COMFYUI — generate 8–20 environment concepts (2D only)
        ↓ unload
2. YOU SELECT — approved visual direction
        ↓
3. LLM — extract environment language (architecture, materials, lighting,
         landmarks, mood) as structured design rules
        ↓
4. BLENDER BLOCKOUT — simple geometry: scale, walkable space, camera
         angles, geography, sightlines. Intentionally ugly.
        ↓
5. CAMERA TEST — place character proxy, test shot list.
         Discovery: what the camera never sees doesn't need to exist.
        ↓
6. ASSET TIER DIVISION — classify every element (see table below)
        ↓
7. AI 3D — generate individual hero props and modular pieces
        ↓ unload
8. BLENDER — assemble canonical environment + procedural duplication
        ↓ render passes
9. COMFYUI — texture/style/atmosphere/weathering over Blender passes
        ↓ unload
10. BLENDER — final camera + animation + composite
```

**Production rule — camera-proves-existence:** If the camera cannot see it
in any planned shot, don't build it. Film sets work this way. Your Blender
world supports your shots, not a video game.

**Production rule — design cameras before finishing assets:** Place character
proxies and test your shot list against the blockout. The beautiful tower
from the concept that's never visible in any shot? Don't build it.

#### Four asset tiers

More granular than the three environment techniques — these classify every
element in an environment by how much geometry it actually needs:

| Tier | What belongs here | Technique | Examples |
|------|-------------------|-----------|----------|
| **1 — Hero geometry** | Close to camera or touched by characters | Full 3D (modeled or AI-generated) | door, table, weapon, market stall, statue, important architecture |
| **2 — Modular geometry** | Repeated structural components | Model once → Blender duplication (×30) | wall section, window, column, roof module, stairs, arches, railings |
| **3 — 2.5D elements** | Visually rich, minimal physical interaction | ComfyUI images → Blender image planes → depth layers → parallax | distant storefront, far buildings, mountains, city skyline, background crowds |
| **4 — Pure atmosphere** | No geometry at all | ComfyUI / video generation, applied in composite | fog, rain, smoke, clouds, light flicker, crowd impression, distant traffic |

**Key insight for Tier 2:** Don't AI-generate twelve buildings. Create one
modular kit (WINDOW_A, WINDOW_B, COLUMN_A, WALL_A, WALL_B, ROOF_A) and let
the LLM assemble variations through Blender: "Create four storefront
variations using the approved architecture kit. Don't introduce new
materials." Procedural duplication is vastly cheaper than per-building
generation.

**Grounded in the system:** The asset tier classification is a `[decision]`
recorded in the environment's Work Object. The Critic/Continuity specialist
validates that nothing in Tier 3/4 is actually needed at Tier 1 (character
interaction or close camera proximity).

#### Environment language extraction

After the director approves a concept, the LLM extracts structured design
rules that govern all downstream asset creation:

```text
environment: Lower Market

architecture:
  dominant_shape: vertical
  corridors: narrow
  ceiling_height: high

materials: [dark stone, oxidized brass, wet wood]

lighting:
  key_source: hanging warm lamps
  environment: cold blue rain

landmarks: [central stair, ceremonial gate, vendor corridor]

mood: [oppressive, ancient, inhabited]
```

**Grounded in the system:** This is recorded as `[system]` evidence in the
environment's Work Object. The Art Director specialist references it when
generating assets or texture passes — ensuring material and lighting
consistency without the director re-specifying it per asset.

#### Three environment techniques (summary)

| Technique | Use case | Cost |
|-----------|----------|------|
| **A — Full 3D** | Spaces characters interact heavily with: rooms, hallways, streets, vehicles, important props | High |
| **B — 2.5D** | Visually rich environments that don't need full geometry: ComfyUI images → Blender image planes → depth layers → camera parallax | Low |
| **C — Generated video** | Distant atmosphere, clouds, crowds, dreams, abstract motion, background events | Low |

2.5D is especially efficient for a graphic-novel-style production: ComfyUI
generates the environment, you separate it into foreground/midground/
background/sky planes in Blender, and a small camera movement creates
parallax. Blender natively supports image planes and image sequences.

Most environments use all three techniques simultaneously — the four asset
tiers above determine which technique applies to each element.

#### Character pipeline (conservative)

Recurring characters need a more controlled pipeline than props:

```text
CONCEPT (ComfyUI) → TURNAROUND (front/side/back) → 3D BASE
→ BLENDER CLEANUP → CANONICAL TOPOLOGY → RIG → APPROVED CHARACTER
```

Once approved: **stop regenerating the character.** Use the same canonical
model across shots. AI can modify costume, texture, hair variation, lighting,
facial details — but the underlying spatial identity remains stable. This is
how consistency is maintained.

**Grounded in the system:** The canonical character is a design asset record
with `kind: asset`. Its Work Object tracks every approved variation. The
Critic/Continuity specialist checks cross-scene consistency against the
canonical model.

#### Prop pipeline (aggressive generation)

Props are where AI 3D generation gives the biggest productivity gains:

```text
ComfyUI concept → Tripo/Hunyuan → .glb → Blender →
LLM: "remove unnecessary internal geometry, separate handle,
set real-world height to 32cm" → YOU APPROVE → CANON
```

**Automated handoff (V4+):**
```text
YOU: "I approve chair concept C. Turn it into a production prop."
→ CONDUCTOR: recognizes asset-production task
→ ART DIRECTOR: generates multi-view reference set
→ 3D GENERATOR: outputs chair_v01.glb
→ BLENDER TOOL: imports, scales, names, organizes
→ CRITIC: checks silhouette, dimensions, concept similarity
→ YOU: "Make backrest 10% taller." → BLENDER TOOL edits → YOU: "Approve."
→ prop_chair_003, status: CANON
```

#### Anti-pattern: regenerate everything per shot

Do NOT build:
```text
ComfyUI image → random image-to-3D → Blender → random LLM edits →
next shot → regenerate everything
```

Instead:
```text
EXPLORE → SELECT → RECONSTRUCT → CLEAN → APPROVE → CANONIZE → REUSE
```

The generative part happens heavily before approval. After approval,
deterministic tools take over. This is the same `explore → design → build →
verify` lifecycle the studio already enforces for every Work Object.

### 5.5 Creative Precedent Library

*(Added per WO `2026-08-23-001` Decision 5, from the report deliverable
`2026-08-23-001-asset-recipe-library-design-critique.md`. This section is
accepted architecture, not a forecast.)*

The library exists so a specialist can ask not "what prompt should I use?" but
**"what has worked before for this kind of intent, constraint, failure mode,
and desired effect — and what failed?"** It is a *memory of creative cause and
effect*, not a folder of prompts. The prompt is one piece of evidence about how
a decision was realized; the reusable asset is the **recipe** and the **bounded
revision**.

**Harvest first, don't build from empty.** The library's v0 ingestion target is
*closed Work Objects*, not future work. A closed WO's Decision trail already IS
a precedent graph. `2026-08-23-007` alone seeds it with 2 validated recipes
(§5.4) and ~6 falsified counter-examples (global img2img revision, hand-drawn
masks, the FLUX.1-Fill engine swap, negative-prompt-at-cfg-1.0, whole-frame
mask at partial denoise, Redux strength-tuning for viewpoint). Recipes are a
*projection* of decision trails, the same way `command-center.html` projects
Work Object data (§1.6).

**Three genuinely-new object types; everything else is an existing primitive
referenced by ID (never cloned).**

```
NEW:
  Recipe          method + tool + controls + sequence + applicable_when /
                  avoid_when + verification + status + known_limits +
                  provenance(Decision IDs)
  Revision        stored artifact-pair delta: source→result, change/protect/
                  avoid, method = Recipe ID, outcome = Decision ID
  TastePrinciple  a durable, director-authored preference; provenance =
                  Judgment (Decision) IDs

REFERENCED (already exist — link by ID):
  Work Object / Intent section / Direction object   (intent)
  design-asset record                               (artifact)
  Evidence ledger entry (tagged)                    (evidence)
  Decision record                                   (judgment / outcome)
  History entry                                     (chronology)
```

Cloning the seven existing primitives would fork the source of truth (two
"Judgment"-like records that can disagree) — exactly what the single-Work-
Object-of-record model prevents.

**Storage and traversal (corrected per WO `2026-08-23-001` Decision 6 —
`ws relation`/`ws graph` verified insufficient).** Recipe/Revision/
TastePrinciple are stored as Markdown+YAML in `.work-studio/` (§8 house style),
following the **Component Ledger pattern** (`.work-studio/component-ledger.md`,
ADR 0014), not `ws relation`/`ws graph`: `ws relation add` requires both edge
endpoints to be full Work Objects, and its fixed 16-verb vocabulary has no
`protects`/`changes` semantics — confirmed by direct CLI check, not assumed.
The Component Ledger is the studio's own existing, already-working precedent
for "many small named things, each a pointer with declared dependency edges in
prose" — a single derived Markdown index (one Recipe/Revision/TastePrinciple
per entry, hand- or harvester-declared `depends-on`/`realized-by`/`failed-for`
edges, `status` field, findings), the same shape `component-ledger.md` already
uses for COMP-001 through COMP-040. The harvester (v0, below) builds and
maintains this index directly; if genuine graph traversal is later wanted, a
small script reads the index's declared edges into NetworkX independently of
`ws graph` — that traversal layer does not exist for free and must be built.

**Three description layers, never collapsed** (the studio's existing epistemic
rule applied to a new object): observable = `[system]` ("palette is low
saturation"), interpretation = `[inference]` ("reads as restrained"), intent /
judgment = `[decision]` / `[testimony]` ("director preferred restraint"). A
`[system]` fact must never be laundered into a `[judgment]`.

**Status lifecycle is owned, not invented.** A Recipe is a durable component:
its `experimental → candidate → validated → preferred → deprecated →
superseded` transitions are governed by `alawas-design-track-components`; a
recipe that generalizes into a studio-wide method escalates to
`alawas-governance-maintain-working-method`. Store a success/failure counter but
**never surface it as a ranking or sort key** — surface `known_limits` and the
counter-examples instead, and let `alawas-thinking-diagnose-homogenization`
fire if a single recipe starts dominating accepted output.

**Retrieval returns a Reference Pack, not the whole library, under a mandatory
diversity rule:**

```
Reference Pack = 2 close precedents
               + 1 counter-example (a falsified recipe / rejected artifact)
               + 1 different-but-successful approach
               + relevant TastePrinciples (surfaced as tension, not instruction)
```

The counter-example slot is why harvesting *failed* Decisions matters as much
as harvesting successes. Precedents inform present judgment; they never dictate
it (`precedents → evidence → interpretation → proposal → director judgment`),
so taste does not ossify into policy.

**Capture-at-generation is the make-or-break** and is enforced at the Art /
Asset Director skill boundary (§4), not by later cleanup: a generation that
does not record its intent + recipe + protect/change at the moment it runs does
not enter the library. Retroactive tagging is inconsistent tagging, and
inconsistent tags make every graph query return garbage.

**Staged build order (grounded in current capability):**

| Stage | What | Hardware |
|-------|------|----------|
| **v0 — Harvest** | Projection reads closed WOs' Decision trails → emits Recipe + Revision records into a Component-Ledger-style index (not `ws relation`/`ws graph`, per Decision 6). Target: ingest `2026-08-23-007`. | No GPU |
| **v1 — `find_by_intent` + Reference Pack** | Structured/text retrieval with the mandatory diversity rule. | No GPU |
| **v2 — Capture-at-generation** | Art/Asset Director skill writes a Recipe/Revision record as each generation runs. | — |
| **v3 — `find_similar_artifact`** | Reuse the **already-installed `sigclip_vision`** embeddings (§2.4); obey sequential-VRAM discipline. | GPU |
| **v4 — TastePrinciple governance** | `track-components` owns status; `diagnose-homogenization` guards dominance. | — |

**Known-unsolved is a first-class status.** The open flaw categories from
`2026-08-23-007` (S002 unwanted geometry, S005 whole-frame revision, now in
`2026-08-24-003`) are represented as known-unsolved recipes, not omitted — the
library must record what has *failed* to be honest.

---

## 6. Console UI

### 6.1 Six working areas

```text
┌──────────────────────────────────────────────────────┐
│                    DIRECTOR CONSOLE                  │
├──────────┬───────────┬─────────┬──────────┬──────────┤
│ STORY    │ SCENE     │ SHOT    │ REVIEW   │ CANON    │
│          │ BOARD     │ STAGE   │          │          │
├──────────┴───────────┴─────────┴──────────┴──────────┤
│                                                      │
│                   CURRENT WORK                       │
│                                                      │
│ screenplay / director intent / render / animatic    │
│                                                      │
├───────────────────────────────────┬──────────────────┤
│                                   │                  │
│              ARTIFACT             │   CONVERSATION   │
│                                   │                  │
│ screenplay                        │ Direction input  │
│ Blender preview                   │ + history        │
│ ComfyUI result                    │                  │
│ waveform                          │                  │
│ animatic                          │                  │
│                                   │                  │
├───────────────────────────────────┴──────────────────┤
│ PRESERVE ✓     CHANGE Δ      PROPOSE ?      APPROVE │
└──────────────────────────────────────────────────────┘
```

### 6.2 Progressive disclosure (three depths)

| Depth | What | When |
|-------|------|------|
| **1 — Creative surface** | Artifact + Director input | Default |
| **2 — Interpreted structure** | Intent, target effect, protect, change, avoid, constraints | When helpful |
| **3 — Internals** | Work Object, evidence IDs, skill routing, tool calls, checkpoints | Deliberately opened |

### 6.3 Direction input modes (auto-inferred)

| Mode | Example | System response |
|------|---------|-----------------|
| **Inquiry** | "Why isn't this scene working?" | Investigate → explain. No mutation. |
| **Direction** | "Make this feel less heroic." | Investigate → propose → change → verify |
| **Explicit command** | "Keep B and remove the score from frames 420–610." | Direct execution (specific transformation) |

### 6.4 Revision reporting

Every revision explicitly reports:

```text
PRESERVED ✓   — what was protected and kept
CHANGED Δ     — what was modified and why
PROPOSED ?    — what the system suggests but hasn't done
```

This maps directly to the Evidence ledger's `[system]` / `[decision]` /
`[inference]` tagging.

**The PRESERVED/CHANGED/PROPOSED report *is* the Revision capture format**
(§5.5): PRESERVED = the Revision's `protect` set, CHANGED = its `change` set,
PROPOSED = candidate changes not yet accepted. Recording the report and
recording the Revision object are the same act viewed two ways — so every
revision reported to the director is, by construction, a Revision record
entering the Creative Precedent Library.

---

## 7. Build Order

Each version is a self-contained deliverable. No version depends on
capabilities from a later version.

### V0 — Writing + Governance (foundation)

**What it builds:** The screenplay-as-Work-Object layer and the Direction
input pattern, grounded entirely on the existing `tools/ws` CLI.

| Component | Implementation | Grounded in |
|-----------|---------------|-------------|
| Direction input → structured Direction object | Parse natural language via API LLM → YAML Direction → `ws create` or `ws append-evidence` | Existing Work Object creation + evidence model |
| Scene Board view | Generated HTML (like command-center.html) reading Scene Work Objects | Existing `command_center.py` projection pattern |
| 4-layer screenplay | Sections within Scene Work Object body (Layer A/B/C/D) | Existing Work Object body sections |
| Director Layer | Table section in Scene Work Object beside screenplay | Existing Work Object body sections |
| Beat → dialogue workflow | Skill boundary: Story Editor profile enforces beats-before-dialogue | Existing skill system |
| Decision log | Work Object `Decisions and revisit triggers` section | Existing structured decision records |
| Versioning | `ws append-history` + `ws append-artifact` with fingerprints | Existing artifact tracking |
| PRESERVED / CHANGED reporting | Generated from diff between Work Object versions | Existing `updated_at` + History |

**Tracer for V0:** Create one Scene Work Object for SC030 (Mara/Leo), write
its 4-layer screenplay manually, type one Direction, see the structured
Direction object recorded as evidence, see the Scene Board rendered in HTML.

**Exit criteria:** A director can type a direction, see it structured, see
the scene board, and find decisions recorded — all using `tools/ws` as the
persistence layer.

### V1 — Production Objects

**What it builds:** The full hierarchy (Project → Sequence → Scene → Beat →
Shot) as linked Work Objects, plus the shot state machine.

| Component | Implementation | Grounded in |
|-----------|---------------|-------------|
| Project/Sequence/Scene/Shot hierarchy | Work Objects linked via `ws relation` | Existing typed relationships |
| Shot object with tier classification | Extended Work Object with shot metadata | Existing Work Object schema |
| Shot state machine | `ws transition` through shot-specific states (blocking → animation → render → review → approved) | Existing lifecycle states |
| Canon registry | Lightweight canon record — approved Shot WO (`shot_status: approved`) + `.work-studio/canon-registry.md` Component-Ledger-pattern index | Component-Ledger pattern (WO `2026-08-24-006` Decision 3) |
| Hierarchy graph | `ws graph` traversal | Existing graph command |

**Exit criteria:** A project hierarchy exists as linked Work Objects. A shot
can be transitioned through its production states. Canon is recorded as
design assets.

### V2 — Audio

**What it builds:** The voice performance pipeline using TTS APIs.

| Component | Implementation | Grounded in |
|-----------|---------------|-------------|
| Voice Bible | Design asset record per character (voice identity) | Existing design asset pipeline |
| Performance Translator | Skill: Character/Performance Director. Translates intent → TTS parameters via API LLM. | Existing skill system |
| TTS generation (tiered) | Tier 1: local TTS (free). Tier 2: cheap API. Tier 3: premium API. | Capability-gated instruments (Decision 2 pattern) |
| Take comparison | Generated HTML showing waveforms + playback for A/B/C/D takes | Existing projection pattern |
| Audio approval → canon | Director selects take → `[decision]` in Work Object | Existing decision records |
| Audio lock gate | Shot cannot advance past audio-lock state without approved take | Lifecycle gate enforcement |

**Exit criteria:** A character has a voice bible. The system generates
multiple takes from a performance direction. The director selects one. Audio
lock prevents premature animation.

### V3 — Blender Integration

**What it builds:** Bounded Blender tools accessible through the console,
with governance protecting locked elements.

| Component | Implementation | Grounded in |
|-----------|---------------|-------------|
| Blender MCP server | Python add-on exposing bounded tool API (camera.get/set, rig.get_pose, etc.) over local connection | BCC pattern (local network protocol to Blender) |
| Scene inspection | Read Blender scene state → `[system]` evidence | Existing evidence model |
| Camera/layout/pose tools | Bounded API, no arbitrary Python | Authority model (escalation for raw Python) |
| Mesh tools | `mesh.get_vertices`, `mesh.move_vertices`, `mesh.extrude`, `mesh.separate_by_material`, `mesh.add_modifier`, `mesh.decimate`, `mesh.remove_doubles` | Asset cleanup for imported 3D models |
| Image import | `image.import_as_plane`, `image.set_as_reference` | Reference images and 2.5D environment planes |
| Object import | `object.import_mesh(.glb/.obj/.fbx)` for AI-generated 3D assets | Path 2 of ComfyUI→Blender pipeline |
| Governance integration | Check `protect` fields before executing changes | Existing constraint enforcement |
| Preview render | Blender render → local file → asset record | Existing artifact tracking |

**Technical note:** This follows the same architectural pattern as BCC
(Controller_Addon) — a Blender add-on that accepts structured commands over
a local network protocol. The difference: BCC sends motion-sensor data over
UDP; the Director Console sends structured tool calls over WebSocket/HTTP.
The mesh tools enable LLM-assisted asset cleanup: scaling imported meshes to
real-world dimensions, separating parts by material, removing internal
geometry, and applying modifiers — all without arbitrary Python.

**Exit criteria:** The console can read Blender scene state, execute bounded
camera/pose/mesh changes with governance checks, import .glb/.obj assets,
import reference images as planes, and render a preview.

### V4 — ComfyUI Integration

**What it builds:** Blender render passes fed into ComfyUI for appearance
exploration.

| Component | Implementation | Grounded in |
|-----------|---------------|-------------|
| Blender pass export | Automated export of depth, normals, pose, masks, material IDs | V3 Blender integration |
| ComfyUI workflow templates | Pre-built workflows consuming Blender passes | ComfyUI API (already running on :8188) |
| Variant generation | Generate A/B/C appearance variants from same Blender layout | Decision 2: generation-first via ComfyUI |
| Variant comparison view | Generated HTML for side-by-side comparison | Existing projection pattern |
| Variant approval → canon | Director selects variant → `[decision]` + design asset | Existing decision + asset pipeline |
| Multi-view reference generation | ComfyUI generates front/side/back/¾ views from approved concept | Asset creation funnel (§5.4) |
| AI 3D generation | Hunyuan3D/Tripo workflows in ComfyUI: approved image(s) → .glb mesh | §5.4 Path 2 |
| Asset import pipeline | Generated .glb → V3 `object.import_mesh` → LLM cleanup → director approval → canonical design asset | Asset creation funnel → design asset pipeline |
| 2.5D environment assembly | ComfyUI environment image → Blender image planes → depth layers → camera parallax | §5.4 environment technique B |

**Prerequisite (resolved):** Flux Dev FP8 is installed in ComfyUI
(`flux1-krea-dev_fp8_scaled.safetensors`). Fits in 10 GB VRAM. AI 3D
generation (Hunyuan3D) adds ~2-4 GB model weight — must load/unload
sequentially with the diffusion model.

**Exit criteria:** Blender exports passes, ComfyUI generates appearance
variants AND 3D assets from approved concepts, director compares and selects,
selection recorded as canon. The asset creation funnel
(explore→select→reconstruct→clean→approve→canonize→reuse) is end-to-end
functional for at least one prop.

**Concrete environment pipeline tracer (V4):** Build one alley, not a city.

```text
ENVIRONMENT 001 — MARKET ALLEY

FULL 3D (Tier 1):  ground, two walls, door, stairs
AI 3D (Tier 1-2):  lamp, stall, statue, sign
MODULAR (Tier 2):  windows, arches, pipes
2.5D (Tier 3):     distant marketplace, city beyond alley
FX (Tier 4):       rain, fog, steam
```

Then build three shots (SH010 wide establishing, SH020 character walks,
SH030 close dialogue). If those three shots work with the full
ComfyUI→Blender→ComfyUI→composite cycle, the entire environment pipeline
is proven. The GPU sequential load/unload cycle is tested end-to-end.

This also tests the Direction-to-environment loop:
```text
YOU: "Make this alley feel more oppressive without changing the camera
      or character blocking."
→ PROTECT: camera, character positions, architecture footprint
→ PROPOSE: narrow negative space, increase foreground obstruction,
           reduce distant illumination, increase vertical density
→ Blender/ComfyUI changes → preview → YOU approve
```

### V5 — Animatic / Editorial

**What it builds:** Shot assembly into a watchable animatic with audio.

| Component | Implementation | Grounded in |
|-----------|---------------|-------------|
| Shot timeline | Ordered shot sequence with timing from audio lock | V1 production objects + V2 audio |
| Animatic assembly | Renders + audio → video timeline | Local ffmpeg or similar |
| Review surface | Playable animatic with per-shot annotations | Existing projection pattern (HTML) |
| Write → visualize → watch → judge → rewrite loop | The animatic as truth test for writing decisions | Evidence model: animatic review → `[system]` evidence |

**Exit criteria:** An assembled animatic is watchable. The director can
annotate per-shot and the annotations become evidence in shot Work Objects.

### V6 — Agentic Dailies

**What it builds:** Specialist profiles that critique work and surface
productive disagreements.

| Component | Implementation | Grounded in |
|-----------|---------------|-------------|
| Specialist critique skills | Story Editor, Character Director, Cinematographer, etc. as skills with API LLM | Existing skill system |
| Dailies session | Specialists review recent work, surface disagreements | Agreement Loop / grilling mechanism |
| Proposed changes with evidence | Each specialist proposes changes with `[inference]` evidence | Existing evidence tagging |
| Director approval workflow | Director reviews proposals, approves/rejects each | Existing decision records |

**Exit criteria:** Specialists independently critique a scene. Disagreements
are surfaced. The director resolves them. Decisions are recorded.

---

## 8. Technical Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Persistence** | `tools/ws` CLI + `.work-studio/` markdown files | Already built. File-first. Git-versionable. |
| **API LLM** | Claude API (or equivalent) | Reasoning, routing, script analysis, tool calls. Keeps GPU free. |
| **Vision/critique LLM** | DeepSeek V4 Flash Vision (`deepseek-v4-flash-vision-exp`) | Visual critique, taste evaluation, reasoning/classification fallback (Decision 10, replaces Qwen3.5/Ollama). Cloud API — no local no-network fallback remains. |
| **Frontstage UI** | Generated HTML (V0-V2) → local web app (V3+) | Follows command-center.html projection pattern initially. |
| **Blender integration** | Python add-on with bounded tool API | Same pattern as BCC's Blender add-on. |
| **ComfyUI integration** | HTTP API + websocket on :8188 | Already running locally. |
| **TTS** | Tiered: local → cheap API → premium API | Cost control. |
| **Rendering** | Blender (spatial) + ComfyUI (appearance) + ffmpeg (assembly) | GPU time-shared. |
| **Networking** | Local network (WebSocket/HTTP) | Same LAN pattern as BCC. |

---

## 9. Constraints (from accepted Decisions)

| Constraint | Source | Status |
|------------|--------|--------|
| File-first: every artifact is a local file | Decision 2 | Active |
| Model-agnostic: any model behind ComfyUI satisfies | Decision 2 | Active |
| Local-install dependency accepted (Blender, ComfyUI) | Decision 2 | Active |
| No hosted/cloud generation dependency | Decision 2 | Active |
| API LLM for reasoning (cloud OK for cognition, not generation) | Director testimony | Active |
| Blender owns spatial truth, not video models | Director testimony | Active |
| Intent and implementation remain separate | Director testimony | Active |
| LLMs propose; human establishes canon | Director testimony | Active |

---

## 10. Current Blockers

| Blocker | Impact | Resolution path |
|---------|--------|-----------------|
| ~~No local image model in ComfyUI~~ | ~~V4 blocked~~ | **Resolved:** Flux Dev FP8 installed (`flux1-krea-dev_fp8_scaled.safetensors`) |
| Blender MCP bounded tool API does not exist yet | V3 (Blender integration) requires building it | Build as a Blender add-on, same pattern as BCC |
| GPU time-share orchestration untested | Sequential load/unload may be painful | V4 environment pipeline tracer tests exactly this |

---

## 11. Supersession Notes

The following earlier material is superseded by the director's updated plan:

- **Original Direction 1 ("no new backend")** was narrowed in Decision 2:
  the studio backs Context + Inspector panes but the Artifact pane is a
  genuinely new layer, not just a projection of existing data.
- **Original tracer (render a Work Object as three static panes)** was
  rejected in Decision 2 as a false green — it tested the already-proven
  easy part. Replaced by the three-station render-to-lineage tracer.
- **"Dependency-free" constraint** was narrowed in Decision 2 to
  "local-install dependency accepted" — Blender and ComfyUI are accepted
  local dependencies, not hosted services.
- **Local LLM as primary intelligence** was superseded by the director's
  updated plan: API models handle reasoning/routing/critique; local LLM
  (Qwen) is offline fallback only; GPU stays free for generation.
- **Local LLM (Qwen3.5/Ollama) as offline fallback** is itself now superseded
  (WO `2026-08-23-001` Decision 10): fully replaced by DeepSeek V4 Flash
  Vision (`deepseek-v4-flash-vision-exp`), a cloud API model, taking over both
  the fallback-reasoning role and the visual-critique/taste-evaluation role.
  This is a deliberate, director-confirmed tradeoff — the plan no longer has
  any fully local, no-network text-reasoning option.

---

## Provenance

- `[decision]` Decision 1 (WO 2026-08-23-001): combined Direction 1+3
- `[decision]` Decision 2 (WO 2026-08-23-001): constraint narrowed, instruments named
- `[decision]` Decision 3 (WO 2026-08-23-001): tracer designed, image model blocker resolved (Flux Dev FP8 installed)
- `[testimony]` Director's updated system plan (pasted 2026-08-23): 20-section concept document
- `[system]` Work Studio infrastructure: `tools/ws` CLI, 45 skills, design asset pipeline, command center projection, evidence model, authority gates
- `[system]` BCC implementation plan (Controller_Addon): Blender add-on integration pattern
- `[system]` ComfyUI probe (2026-08-23): running on :8188, Flux Dev FP8 installed (`flux1-krea-dev_fp8_scaled.safetensors`)
- `[system]` Hardware: RTX 3080 10 GB, Ryzen 5 5600X, 32 GB RAM
- `[testimony]` Director's 3D asset pipeline testimony (pasted 2026-08-23): ComfyUI→Blender paths, AI 3D generation (Hunyuan3D/Tripo), environment techniques, character/prop pipelines, asset creation funnel, bounded LLM editing strengths/limits
- `[inference]` Build order, component mapping, and technical stack choices are synthesis of the above, not new decisions
- `[testimony]` Director's hardware-aware environment workflow testimony (pasted 2026-08-23): 9-step hybrid environment pipeline, four asset tiers (hero/modular/2.5D/atmosphere), camera-proves-existence rule, modular kit assembly, environment language extraction, concrete first-environment tracer (one alley + three shots), sequential GPU load/unload cycle for environment production
- `[inference]` §5.4 Asset Production Department structure, bounded mesh tools expansion, V3/V4 asset pipeline components are synthesis of the 3D asset and environment workflow testimonies grounded in existing studio infrastructure
