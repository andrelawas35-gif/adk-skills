---
name: alawas-production-plan-scene
description: "Use when directorial intent must become a structured scene specification; plans bounded Blender commands and never executes tools or fabricates assets."
default_tier: medium
platform: codex
consequence: meaningful
sensitivity: ordinary
domain: [production]
component: COMP-045
parent_wo: 2026-08-23-001
---
# Production Plan Scene

## Governing principle

Translate a director's natural-language shot description into an executable scene specification. This skill performs the six jobs: interpret intent, retrieve registered assets, place everything in spatial context, compose camera from emotional read, light it with mood-appropriate values, and specify render parameters. It produces structured YAML that maps cleanly to bounded Blender operator operations.

## Personal working lens

Scene planning is creative reasoning without execution. The skill reads one natural-language prompt, consults a caller-owned fixture registry for available assets, and emits a deterministic scene spec. It never calls tools, executes Blender/ComfyUI processes, creates assets, or fabricate missing elements — those are Layer 1 responsibilities. The output must be directly consumable by bounded production operators.

## Boundaries and non-goals

**This skill does:**
- Interpret emotional/dramatic intent from directorial prompts using keyword detection for scale/tense markers (tiny, small, isolated, tense, threat, danger)
- Query a fixture asset registry to select only registered assets that match prompt needs
- Report missing scene needs as explicit gaps with fabricated=false; never invent unregistered assets
- Compute camera parameters (lens_mm, location, target) from emotional read
- Compute lighting parameters (energy, color, dramatic_intent) from mood keywords
- Define composition and render passes consistent with the bounded operator surface

**This skill does NOT:**
- Execute Blender or ComfyUI operations — produces command plans for operators to queue
- Call tools or invoke subprocesses — reads registries locally and emits YAML only
- Create assets or modify canonical registries — fixture registry is caller-owned input
- Fabricate missing assets or fill gaps with hallucinated content

## Inputs and preconditions

**Required inputs:**
- `prompt` (str): Director's natural-language shot description, minimum 10 characters recommended
- `registry_path` (Path or str): Local path to a YAML fixture registry containing an "assets" list

**Preconditions:**
- Fixture registry must exist at the provided path and be readable UTF-8
- Registry must contain valid YAML with assets as a list of dicts, each having "asset_id" and "path" fields
- Prompt must not be empty or whitespace-only (raises ValueError)
- Registry asset tags should include keywords matching _NEED_ALIASES for detection (character/person/protagonist/hero, landscape/terrain/environment, prop/object/weapon/vehicle)

## Required capabilities

This skill requires the following abstract capabilities. The platform adapter classifies each as native, manual-fallback, or unsupported and degrades explicitly when one is unavailable.

- `file_read` — Read fixture registry YAML file at provided path
- `structured_output` — Emit valid YAML scene specification with deterministic field ordering

The skill uses internal regex tokenization for prompt analysis — no external text_processing tool required.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

**Default consequence:** meaningful (scene planning affects creative direction but is reversible)

**Authority gates:**
- Writing registry modifications: this skill never writes registries; only reads caller-owned input
- Fabricating missing assets: explicitly forbidden — gaps must be reported with fabricated=false
- Tool execution during planning: forbidden — produce command plans, do not execute them

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

The conductor owns durable checkpoint writes only. During ordinary operation, when evidence selects a different stage lens, it routes:
- An unresolved decision about scene boundary → route to `alawas-thinking-pressure-test-decision`
- A design question about emotional parameter mapping → route to `alawas-design-design-tracer-bullet`

Routine lifecycle actions inside existing authority do not activate grilling.

## Skill Grilling Profile

Apply the `alawas-production-plan-scene` profile and continuous Grilling Session in `references/SKILL-AWARE-GRILLING.md`. Reconstruct one testable outcome, detect overlapping work, ground positive and negative evidence, and make consequence, sensitivity, lifecycle, rationale, and authority explicit before persistence.

For a direct specialist request, discover or establish the Work Object before routing while preserving the same Context Card, Evidence Ledger, Decision Frontier, and accepted decisions. Create `## Grilling Session` lazily. Act as the sole writer of compact continuity state; keep full decisions and evidence in their canonical sections and never store a transcript.

## Stage workflow

### 1. Validate inputs

1. Check prompt is non-empty string with length ≥ 10
2. Check registry path exists and is readable
3. Attempt to load YAML registry; if parse error or missing "assets" list, raise descriptive ValueError
4. Log validation failures in History entries (append-history)

### 2. Interpret intent

1. Tokenize prompt using regex `[a-z0-9]+` for lowercase word extraction
2. Detect scale keywords: tiny/small/isolated/alone/vast → set `tiny=True` else False
3. Detect tense keywords: tense/threat/danger/urgent → set `tense=True` else False
4. Requested needs = intersection of prompt tokens with _NEED_ALIASES values; default to ["character", "landscape"] if none detected

### 3. Query registry for asset matches

1. Load registry YAML and extract assets list
2. For each asset, check if any of its tags intersect with requested need aliases
3. Build `asset_matches` list containing: asset_id, path, needs (sorted), match_reason="registered_tag_match"
4. Track matched_needs set for gap detection

### 4. Detect gaps and report missing elements

1. Compare requested_needs against matched_needs
2. For each unmet need, create gap entry with:
   - `need`: the specific capability (e.g., "landscape")
   - `reason`: "no_registered_asset_match"
   - `fabricated`: False (explicitly forbidden to fabricate)
3. Include gaps in scene spec output

### 5. Compute emotional parameters

1. Call `_emotional_parameters(prompt)` which returns:
   - **camera**: name, lens_mm (35 if tiny else 50), location array, target array, dramatic_intent ("scale_and_isolation" vs "direct_subject_attention")
   - **lighting**: name, energy (900 if tense else 650), color RGB [1.0, 0.78, 0.58] if tense else neutral white, dramatic_intent ("urgent_contrast" vs "neutral_readability")
   - **composition**: subject_scale ("small_in_frame" vs "medium_in_frame"), horizon_emphasis ("wide_landscape" vs "subject_first"), emotional_read ("vulnerable_against_scale" vs "clear_subject_presence")

### 6. Generate blender command plan

1. For each matched asset, emit:
   ```python
   {"op": "object.import_mesh", "params": {"path": ..., "asset_id": ...}, "source_asset_id": ...}
   ```
2. Append camera setup op with lens_mm from emotional read
3. Append lighting op with energy and color from emotional read
4. Append render.preview op (width: 1280, height: 720) as default

### 7. Validate bounded operations

1. Compare all command_plan ops against BOUNDED_OPS frozenset:
   - object.import_mesh
   - camera.set
   - light.set
   - render.preview
2. Raise AssertionError if any op falls outside the set (violates operator contract)

### 8. Emit structured scene spec

1. Call `plan_scene_yaml(prompt, registry_path)` which returns YAML string with:
   ```yaml
   intent:
     prompt: "directorial description"
     requested_needs: ["character", "landscape"]
   asset_matches: [{asset_id, path, needs, match_reason}]
   asset_gaps: [{need, reason, fabricated}]
   camera: {name, lens_mm, location, target, dramatic_intent}
   lighting: {name, energy, color, dramatic_intent}
   composition: {subject_scale, horizon_emphasis, emotional_read}
   render_passes: [{name, format, resolution}]
   blender_command_plan: [{op, params, source_asset_id}]
   ```

### 9. Append History entry

1. Record completion timestamp and prompt processed
2. If gaps detected, note count in History rationale
3. Include scene spec summary (field names only, not values) for audit trail

## Routing and termination

**Route when:**
- Director provides a new natural-language shot description requiring scene planning
- Gap detection reveals missing registry assets that need production work → route to `alawas-business-direct-project-delivery` or create separate WO for asset creation
- Emotional parameter tuning requires semantic expansion beyond current keywords → route to `alawas-design-design-tracer-bullet`

**Terminate when:**
- Scene spec successfully generated with zero tool calls executed
- Gaps are reported explicitly with fabricated=false
- Output is valid YAML containing all required fields per schema
- Command plan contains only bounded operations from BOUNDED_OPS set

## Output template

After each interaction, report:

```markdown
**Scene Planner**: `production-plan-scene` (COMP-045)
**State**: design → verify
**Status**: active
**Prompt processed**: "{truncated prompt}"
**Asset matches found**: {count} registered assets selected
**Gaps reported**: {count} missing needs (all fabricated=false)
**Bounded ops used**: object.import_mesh, camera.set, light.set, render.preview
**Route**: none — awaiting user input OR route to next skill if gaps need production work
```

## Failure and degradation behavior

| Failure | Behavior |
|---------|----------|
| Empty/short prompt (<10 chars) | Raise ValueError: "directorial prompt must be at least 10 characters" |
| Registry path not found or unreadable | Raise FileNotFoundError with exact path |
| Invalid YAML syntax in registry | Raise yaml.YAMLError with parse details |
| Missing "assets" list key in registry | Raise ValueError: "fixture registry 'assets' must be a list" |
| Asset dict missing required keys | Raise ValueError describing which field is absent |
| Planner emits unsupported op | Raise AssertionError listing the unexpected operation |
| Registry has duplicate asset_ids | Warning logged; processing continues with last value |

## Anti-patterns

1. **Tool execution during planning**: This skill must never invoke Blender, ComfyUI, or cloud APIs — it produces command plans for operators to queue and execute.

2. **Asset fabrication**: Missing needs must always be reported as gaps with fabricated=false. Never invent unregistered assets or fill gaps with hallucinated content.

3. **Hardcoded emotional parameters**: The current implementation only detects "tiny/small/isolated" and "tense/threat/danger". Future expansion requires semantic analysis beyond regex token matching — route to design-tracer for boundary refinement.

4. **Registry mutation**: This skill reads registries; it never writes, appends, or modifies canonical asset lists. Those are separate production-work responsibilities.

5. **Context obesity**: Do not embed full prompts, registry contents, or chat transcripts in Work Objects — extract decisions and evidence only.

## Final self-check

Before reporting completion:

- [ ] Prompt validated (non-empty, ≥10 chars)
- [ ] Registry loaded successfully (valid YAML with assets list)
- [ ] Asset matches computed from tag intersection logic
- [ ] Gaps reported explicitly with fabricated=false for missing needs
- [ ] Emotional parameters derived from prompt keywords
- [ ] Camera, lighting, composition dicts complete and consistent
- [ ] Blender command plan contains only bounded ops
- [ ] No tool calls or subprocess invocations occurred
- [ ] Output is valid YAML with all required fields
- [ ] History entry appended for state transition

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Epistemic rules

This skill uses the **essential 3‑tag system** (`references/epistemic/epistemic-rules-essential.md`).

The epistemic tier is resolved from the skill's `default_tier` (medium).
**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the epistemic tier is upgraded to at least `medium` (essential 3‑tag).
When `consequence: high`, the effective tier is upgraded to the strongest available tier.
`actual_epistemic_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Model tier

This skill declares `default_tier: medium`.
The platform overlay resolves this to `claude-sonnet-4-20250514`.
The prompt budget for this tier is approximately 15000 tokens (advisory).

**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the effective tier is upgraded to at least `medium`. When `consequence: high`,
the effective tier is upgraded to the strongest available model.
`actual_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `Read file` | native |
| `structured_output` | Internal (YAML formatting) | native |
| `user_confirmation` | Conversation turn | native |

### Component governance

This skill implements **COMP-045** as defined in production plan. It is governed by:

- **Parent Work Object**: WO 2026-08-23-001 (Production Skill Architecture)
- **Governed surface**: tools/production/scene_planner/planner.py
- **Fixture registry**: fixtures/production/scene_planner/asset_registry.yaml
- **Tests**: tests/test_scene_planner_tracer.py (3 focused tests passing)

### Dependency invocation rules

This skill composes with:
- `alawas-governance-conduct-work-object` — for lifecycle management and state transitions
- `alawas-engineering-implement-bounded-change` — if registry or code mutations are needed
- `alawas-production-operate-blender` — receives command plans from this skill for execution

Missing dependencies must be reported as reduced capability rather than silently imitated.

### Adjacent Possibility behavior

During design state, this skill may activate the Adjacent Possibility Pass as described in 2026-08-24-017's planning document. This is delegated to `alawas-design-design-tracer-bullet` for boundary exploration and emotional parameter expansion.
