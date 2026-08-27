---
schema_version: 1
id: 2026-08-23-002
title: Define local AI animation studio model architecture
type: inquiry
status: active
state: build
consequence: meaningful
sensitivity: ordinary
created_at: 2026-08-23T20:02:28Z
updated_at: 2026-08-24T22:01:04Z
next_action: Director runs the V0 proof: generate the five S001-S005 before images, run each packet through Qwen3.5-9B Q4 in LM Studio Bionic, apply revisions, and record human_judgment verdicts against the 3-of-5 threshold. Continued work on 2026-08-23-001 (Director Console) can now draw on the validated segmentation-masking and Hunyuan3D mesh-generation mechanisms for its Asset Production Department design.
























































---
## Intent

Define the first local AI animation studio model architecture for the user's current PC: Ryzen 5 5600X, 32 GB RAM, RTX 3080 10 GB VRAM. The work exists to choose a testable first loop before expanding into broader studio orchestration.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] A first complete local studio loop is selected.
- [x] The selected loop has a clear test, success signal, and failure signal.
- [x] Model/runtime choices are framed as replaceable workers behind stable schemas.
- [x] GPU/VRAM constraints are explicitly reflected in the workflow.


## Constraints and non-goals

**Constraints:**
- The RTX 3080 has 10 GB dedicated VRAM, so the design should assume sequential GPU time-sharing rather than multiple heavy resident models.
- The first loop should be small enough to test before purchasing a larger Studio Node.
- Local model work should preserve the user's creative authority rather than silently becoming the director.

**Non-goals:**
- Do not implement the Director Studio application in this Work Object.
- Do not purchase or specify a larger hardware build yet.
- Do not commit to one permanent model provider; keep the architecture model-replaceable.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Start with image-to-critique-to-revision

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | First complete studio loop for the local AI animation studio architecture |
| **Authorization** | User accepted the recommended starting point with "yes go ahead" in the active grilling session |
| **Confidence** | medium — basis: current hardware constraints and user-provided architecture note support a small multimodal critique loop, but no local runtime test has been run yet |
| **Actor** | user |
| **Revisit trigger** | Revisit if the chosen local multimodal model cannot reliably critique renders, if VRAM contention makes the loop impractical, or if the user decides speed/workflow automation matters more than creative critique |
| **Rationale** | The image-to-critique-to-revision loop tests the distinctive value of a multimodal local assistant faster than building broad studio orchestration first. |

### Decision 2 — Use image plus small structured shot object

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Input artifact boundary for the first critique loop |
| **Authorization** | User accepted the recommended boundary with "do recommended" in the active grilling session |
| **Confidence** | medium — basis: structured intent is needed to test studio-specific critique, but the exact shot object fields remain open |
| **Actor** | user |
| **Revisit trigger** | Revisit if structured shot metadata slows iteration too much, if image-only critique proves sufficient, or if the local model cannot reliably use the structured fields |
| **Rationale** | Pairing the still image with a small shot object tests whether the assistant can critique against intent, preserve targets, and revision constraints rather than offering generic visual feedback. |

### Decision 3 — Keep the first shot object small

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Minimal field set for the first structured shot object |
| **Authorization** | User accepted the recommended small field set with "yes go ahead" in the active grilling session |
| **Confidence** | medium — basis: a small schema best tests the critique loop quickly, but continuity needs may emerge after cross-shot tests |
| **Actor** | user |
| **Revisit trigger** | Revisit when testing multiple related shots, when continuity errors become the main failure mode, or when asset IDs/scene graph fields become necessary for revision instructions |
| **Rationale** | The first shot object should include only shot_id, intent, subject, camera, mood, preserve, change, and avoid, leaving continuity fields for a later expansion. |

### Decision 4 — Stage Blender MCP as the second loop

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Position of Blender/MCP integration in the local AI animation studio architecture |
| **Authorization** | User accepted the recommendation to record Blender as the second-stage loop with "go ahead" in the active grilling session |
| **Confidence** | medium — basis: current Blender MCP capabilities support scene inspection and Python execution, but local installation/runtime testing has not been performed |
| **Actor** | user |
| **Revisit trigger** | Revisit if Blender MCP setup is unreliable on the user's machine, if still-image critique fails to prove value, or if a Blender-specific task becomes the user's urgent first proof |
| **Rationale** | The architecture should prove V0 with still image plus shot object critique first, then add Blender as a V1 loop for read-only scene state, viewport evidence, and governed operation proposals before allowing write execution. |

### Decision 5 — Keep Blender V1 read-only plus proposals

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | First safe authority boundary for Blender V1 |
| **Authorization** | User accepted the recommended read-only/proposal boundary with "go ahead" in the active grilling session |
| **Confidence** | medium — basis: Blender MCP write/Python execution is powerful and current evidence supports a safety-first staged approach, but local Blender tests are not yet run |
| **Actor** | user |
| **Revisit trigger** | Revisit after read-only scene inspection and proposed operations produce useful results across several test scenes, or if approved execution is needed for a bounded tracer bullet |
| **Rationale** | Blender V1 should let the LLM inspect scene state and viewport evidence and propose governed operations, while write execution and arbitrary Python remain deferred until the operation schema and approval path are proven. |

### Decision 6 — V0 outputs structured revision instructions only

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Output authority boundary for the V0 still-image critique loop |
| **Authorization** | User accepted the recommended boundary with "do recommended" in the active grilling session |
| **Confidence** | medium — basis: structured revision instructions preserve human approval and model replaceability, but usefulness still needs to be tested against real renders |
| **Actor** | user |
| **Revisit trigger** | Revisit if structured instructions are too vague to improve outputs, if manual translation into ComfyUI becomes the bottleneck, or after a safe parameter-change schema is designed |
| **Rationale** | V0 should produce diagnosis, protect lists, revision targets, instructions, reasons, and avoid lists, but should not emit executable ComfyUI parameter changes from day one. |

### Decision 7 — Prove V0 with five before/after render pairs

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Success/failure test for the V0 still-image critique loop |
| **Authorization** | User accepted the recommended proof with "do recommended" in the active grilling session |
| **Confidence** | medium — basis: the test matches the creative problem directly, but judgment of better/worse remains subjective |
| **Actor** | user |
| **Revisit trigger** | Revisit if five pairs are too much friction to run, if subjective judgment is too ambiguous, or if preserve/avoid violations occur despite apparent visual improvement |
| **Rationale** | V0 should be tested with five before/after render pairs. Each initial image plus shot object receives structured revision instructions; the user applies revisions manually; success requires at least 3 of 5 revised images to be clearly better against shot intent, with zero preserve/avoid violations. |

### Decision 8 — Start V0 testing in LM Studio Bionic

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Runtime path for the V0 still-image critique test |
| **Authorization** | User stated they are using LM Studio Bionic in the active grilling session |
| **Confidence** | high for starting runtime — basis: user confirmed the current tool; medium for final backend — basis: API integration is deferred |
| **Actor** | user |
| **Revisit trigger** | Revisit after the five-pair V0 test, when moving from manual evaluation to API-driven Director Studio integration, or if LM Studio Bionic cannot run the chosen multimodal model reliably |
| **Rationale** | LM Studio Bionic is already in use, making it the lowest-friction runtime for V0 manual image critique and schema testing. The architecture remains model- and runtime-replaceable for later Ollama or llama.cpp integration. |

### Decision 9 — Test Qwen3.5-9B Q4 first

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | First multimodal local model for the V0 LM Studio Bionic critique test |
| **Authorization** | User accepted Qwen3.5-9B Q4 as the first model with "yes" in the active grilling session |
| **Confidence** | medium — basis: Qwen3.5-9B Q4 fits the 10 GB VRAM strategy on paper and is aligned with the earlier recommendation, but local Bionic vision behavior still needs to be tested |
| **Actor** | user |
| **Revisit trigger** | Revisit if Qwen3.5-9B Q4 cannot process image input in LM Studio Bionic, fails the five-pair proof, or causes unacceptable VRAM/runtime instability |
| **Rationale** | Qwen3.5-9B Q4 is the first local critic to test. Gemma 3 12B Q4 remains the fallback if Qwen's vision/runtime behavior fails, and cloud models remain escalation only after local options fail. |

### Decision 10 — Use the V0 test packet shape

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Data packet shape for each of the five V0 before/after render-pair tests |
| **Authorization** | User accepted the proposed packet shape with "yes" in the active grilling session |
| **Confidence** | medium — basis: the shape covers the selected input/output/evaluation boundaries, but it has not yet been used on real render pairs |
| **Actor** | user |
| **Revisit trigger** | Revisit if the packet is too heavy to fill repeatedly, if judging outcomes requires more fields, or if model outputs drift outside the required schema |
| **Rationale** | Each test case should include shot_id, before image, small shot object, required critic output schema, and human judgment fields for better_against_intent, preserve_violations, and avoid_violations. |

### Decision 11 — Use synthetic V0 proof cases

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Source of the five initial render/shot-object pairs for the V0 proof |
| **Authorization** | User selected synthetic cases in the design-stage grilling session |
| **Confidence** | medium — basis: synthetic cases allow controlled failure coverage, but may underrepresent messiness in real creative work |
| **Actor** | user |
| **Revisit trigger** | Revisit if synthetic cases pass but real creative images later fail, or if synthetic cases are too contrived to reveal useful model behavior |
| **Rationale** | The five V0 proof cases should be created specifically to cover known failure modes: character readability, mood mismatch, camera/composition, background distraction, and style/lighting consistency. |

### Decision 12 — Use the five-case synthetic proof suite

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Exact failure-mode coverage for the five synthetic V0 proof cases |
| **Authorization** | User accepted the proposed five-case set with "yes" in the design-stage grilling session |
| **Confidence** | medium — basis: the cases cover distinct critique failure modes, but prompts and images still need to be produced |
| **Actor** | user |
| **Revisit trigger** | Revisit if any case cannot be rendered clearly enough to express its intended failure mode, or if the five cases fail to cover the user's actual studio priorities after the proof |
| **Rationale** | The V0 synthetic proof suite should include S001 Character Readability, S002 Mood Mismatch, S003 Camera/Composition, S004 Background Distraction, and S005 Style/Lighting Consistency. |

### Decision 13 — Use one protagonist/world across all V0 cases

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Subject/world consistency across the five synthetic V0 proof cases |
| **Authorization** | User accepted the recommendation to use the same protagonist/world with "yes" in the design-stage grilling session |
| **Confidence** | medium — basis: consistency helps isolate critique behavior, but reduces subject variety |
| **Actor** | user |
| **Revisit trigger** | Revisit if the suite needs broader genre/subject coverage after the first V0 proof, or if same-subject images create model overfitting to one visual pattern |
| **Rationale** | All five synthetic V0 cases should use the same protagonist, Mara, and a shared world so the suite tests distinct critique failure modes rather than novelty across unrelated scenes. |

### Decision 14 — Use the grounded cinematic sci-fi courier world

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Shared protagonist/world definition for S001-S005 synthetic V0 proof cases |
| **Authorization** | User accepted the proposed Mara/world definition with "yes" in the design-stage grilling session |
| **Confidence** | medium — basis: the world supports the selected visual failure modes, but actual prompt outputs are not yet generated |
| **Actor** | user |
| **Revisit trigger** | Revisit if synthetic renders do not consistently depict Mara or the rain-slick industrial city, or if the world creates style bias that hides critique failures |
| **Rationale** | Mara is a grounded cinematic sci-fi courier moving through a rain-slick industrial city at night. The visual language is restrained, realistic, low-key, and tense. She wears a dark practical jacket with a small amber shoulder light and carries a compact sealed case. The world should feel lived-in, not superheroic or glossy. |

### Decision 15 — Use the five before-image prompts

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Exact before-image prompts for S001-S005 |
| **Authorization** | User accepted the proposed five before-image prompts with "yes" in the design-stage grilling session |
| **Confidence** | medium — basis: prompts intentionally encode the target failure modes, but rendered outputs still need visual inspection |
| **Actor** | user |
| **Revisit trigger** | Revisit if any prompt fails to produce the intended visual failure mode, if the outputs are too incoherent to critique, or if all prompts are solved by the same generic revision advice |
| **Rationale** | The suite should use five deliberately flawed before-image prompts: S001 face/silhouette readability, S002 mood mismatch, S003 weak camera pressure, S004 background distraction, and S005 inconsistent style/lighting. |

### Decision 16 — Use the S001-S005 shot-object JSON

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Structured shot-object JSON for the five V0 proof cases |
| **Authorization** | User accepted the proposed shot-object JSON with "accept" in the design-stage grilling session |
| **Confidence** | medium — basis: the JSON matches the accepted V0 packet shape and failure modes, but has not yet been run through Qwen3.5-9B Q4 |
| **Actor** | user |
| **Revisit trigger** | Revisit if Qwen ignores the preserve/change/avoid fields, if fields are too verbose for repeated use, or if the human judgment step needs additional evidence fields |
| **Rationale** | S001-S005 should each use a compact shot object containing intent, subject, camera, mood, preserve, change, and avoid fields tailored to its target failure mode. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [testimony] | pasted-text.txt from current Codex attachment | User-provided note frames actual PC as Ryzen 5 5600X, 32 GB RAM, RTX 3080 10 GB VRAM; proposes Qwen3.5-9B Q4 as default local LLM, sequential GPU time-sharing with ComfyUI/Blender, one model with multiple studio profiles, tiny worker models for low-reasoning tasks, and cloud escalation for heavy reasoning. |
| [decision] | current grilling session | User accepted the recommended first studio loop: image-to-critique-to-revision, before broader studio orchestration. |
| [decision] | current grilling session | User accepted the recommended artifact boundary: first critique loop input should be a generated/rendered image plus a small structured shot object, not image-only and not a full production graph. |
| [decision] | current grilling session | User accepted the recommended minimal shot object fields: shot_id, intent, subject, camera, mood, preserve, change, and avoid; continuity fields are deferred from day one. |
| [decision] | current grilling session | User accepted staging Blender MCP as the second loop after V0 still-image critique: V1 should begin with read-only scene/viewport evidence and governed operation proposals before write execution. |
| [decision] | current grilling session | User accepted Blender V1 authority boundary: the LLM may inspect scene state and viewport evidence and propose governed operations, but write execution and arbitrary Blender Python remain deferred. |
| [decision] | current grilling session | User accepted V0 output boundary: the still-image critique loop should produce diagnosis plus structured revision instructions, not executable ComfyUI parameter changes from day one. |
| [decision] | current grilling session | User accepted V0 proof test: five before/after render pairs; success requires at least 3 of 5 revised images to be clearly better against the shot object with zero preserve/avoid violations. |
| [testimony] | current grilling session | User stated they are using LM Studio Bionic. |
| [decision] | current grilling session | V0 testing will start in LM Studio Bionic because the user is already using it; later API backends remain possible after V0 proof. |
| [decision] | current grilling session | User accepted Qwen3.5-9B Q4 as the first multimodal local model to test in LM Studio Bionic; Gemma 3 12B Q4 remains fallback and cloud escalation remains last resort. |
| [decision] | current grilling session | User accepted the exact V0 test packet shape: shot_id, before image, small shot_object, required critic output schema, and human_judgment fields for better_against_intent, preserve_violations, and avoid_violations. |
| [decision] | current design grilling session | User selected synthetic cases as the source for the five V0 before/after proof pairs, rather than real images from current creative work. |
| [decision] | current design grilling session | User accepted the exact five-case synthetic proof suite: S001 Character Readability, S002 Mood Mismatch, S003 Camera/Composition, S004 Background Distraction, and S005 Style/Lighting Consistency. |
| [decision] | current design grilling session | User accepted using the same protagonist/world across all five synthetic V0 cases, with Mara as the recurring subject. |
| [decision] | current design grilling session | User accepted the shared Mara/world definition: grounded cinematic sci-fi courier, rain-slick industrial city at night, restrained realistic low-key tense visual language, dark practical jacket with small amber shoulder light, compact sealed case, lived-in rather than superheroic or glossy. |
| [decision] | current design grilling session | User accepted the five deliberately flawed before-image prompts for S001-S005: character readability, mood mismatch, camera/composition pressure, background distraction, and style/lighting consistency. |
| [decision] | current design grilling session | User accepted the S001-S005 shot-object JSON for the V0 proof suite, with intent, subject, camera, mood, preserve, change, and avoid fields tailored to each failure mode. |
| [testimony] | director, 2026-08-24 | Proposed a two-model 3D generation division of labor: TRELLIS.2-4B as the primary/fast general asset generator (image-to-3D, direct GLB export, PBR-ready materials, handles open/non-manifold topology) for background/modular props (street lamps, stalls, facades); Hunyuan3D-2.1 as the hero-asset/production-PBR finisher (split shape 10GB + texture 21GB pipeline) for close-up assets like Mara's sealed case where material fidelity matters. Explicitly excluded recurring principal characters (e.g. Mara) from generator scope — characters remain hand-authored canonical `.blend` files that AI only modifies (hair, clothing, props) rather than regenerates. Proposed environments be built as separate modular assets (not "generate my whole city") assembled in Blender. Corrected own earlier terminology: these are 3D generative models, not "3D LLMs" — the LLM/VLM remains the director/interpreter, the 3D model is an asset-generation instrument. |
| [system] | v0-proof/ artifacts + local validation run 2026-08-23 | Implemented the V0 tracer-bullet packet suite: 12 files under v0-proof/ (README runbook, packet-template.md, 5 before-image prompts S001-S005 in before-prompts/, 5 shot-object JSON in shot-objects/). All 5 JSON validated: shot_id/intent/subject/camera/mood/preserve/change/avoid present, preserve and avoid lists non-empty. Proof run (image generation + Qwen3.5-9B Q4 critique in LM Studio Bionic) pending and manual. |
| [testimony] | S001 image and LLM critique supplied by user: v0-proof/shot-objects/flux_krea_00002_.png | S001 before image and LLM critique were reviewed in session. The critique identifies face unreadability, silhouette/background merge, and muddy contrast, matching the S001 character-readability failure mode. It preserves the accepted world constraints and proposes structured lighting/contrast revisions. Caveat: the instruction to deepen shadow boundaries and bounce amber shoulder light onto facial planes should be applied carefully so it does not further obscure the face or create unnatural light. |
| [testimony] | S001 after image supplied by user: v0-proof/shot-objects/flux_krea_00003_.png | S001 after image reviewed in session. Human judgment: better_against_intent is mixed. Face/profile readability, silhouette separation, and cinematic lighting improved substantially. Preserve violations: hood/dark practical jacket identity changed materially, compact sealed case missing, amber shoulder light missing or transformed into external wall light, and the alley-pressure composition changed into a side-profile wall-light portrait. Avoid violations: none severe on superhero/glossy styling, though warm wall light is stronger than the subtle shoulder-light constraint. Result should not count as a clean S001 pass because preserve constraints were violated despite improved readability. |
| [system] | Comfy Desktop local install smoke test | Installed custom nodes into Comfy Desktop ComfyUI custom_nodes: comfyui_controlnet_aux, ComfyUI_IPAdapter_plus, and ComfyUI-Advanced-ControlNet. Existing nodes included comfyui-impact-pack, ComfyUI-GGUF, rgthree-comfy, and comfyui-easy-use. Verified actual ComfyUI .venv imports torch 2.12.1+cu130, cv2 5.0.0, onnxruntime 1.29.0, albumentations, fvcore, and yacs. Startup smoke test on port 8199 loaded ComfyUI_IPAdapter_plus, ComfyUI-Advanced-ControlNet, comfyui-impact-pack, and comfyui_controlnet_aux successfully; temporary server stopped after test. DWPose warned that accelerated onnxruntime providers may not be available and may fall back to slower CPU/OpenCV, but this does not block the S001 inpaint/IPAdapter workflow. |
| [system] | Created ComfyUI S001 workflow | Created API-format ComfyUI workflow at user/default/workflows/S001_Mara_preserve_lock_img2img_api.json and copied it to v0-proof/S001_Mara_preserve_lock_img2img_api.json. Copied S001 before image into Comfy shared input as s001_before_flux_krea_00002.png. Workflow uses LoadImage -> VAEEncode -> Flux Krea UNET/CLIP/VAE -> KSampler with denoise 0.35 -> VAEDecode -> SaveImage, with a preserve-lock prompt targeting face/silhouette readability while preserving hood, case, shoulder light, pose, framing, and alley. |
| [system] | Created visual ComfyUI S001 workflow | Created visual/canvas ComfyUI workflow at user/default/workflows/S001_Mara_preserve_lock_img2img_visual.json and copied it to v0-proof/S001_Mara_preserve_lock_img2img_visual.json. Added README-S001-comfy-workflow.md noting that the previous S001_Mara_preserve_lock_img2img_api.json is API-format and the visual file should be loaded for the node graph. |
| [system] | Created general ComfyUI V0 visual workflow | Created reusable visual/canvas ComfyUI workflow at user/default/workflows/V0_Five_Case_Test_General_Visual.json and copied it to v0-proof/V0_Five_Case_Test_General_Visual.json. The graph has two lanes: Generate Before Image using Flux Krea text-to-image, and Revise After LLM Critique using LoadImage -> VAEEncode -> low-denoise Flux img2img. README updated with usage guidance. |
| [system] | system | Fixed V0_Five_Case_Test_General_Visual revision lane in both ComfyUI and project copies. Repaired after-image links so revision KSampler decodes through VAEDecode to Save/Preview After, changed revision prompt guard to revision-only wording, and set revision sampler to distinct fixed seed 987654321123456 with 26 steps and denoise 0.50 so the branch behaves as img2img revision rather than regenerating the before prompt. |
| [system] | ComfyUI local generation, RetroComicFlux_test_00001_.png and RetroComicFlux_test2_original_00001_.png | Local test of Retro Comic Flux LoRA (HuggingFace Muapi/retro-comic-flux, strength 0.85, trigger c0m1c) on flux1-krea-dev_fp8_scaled + clip_l + t5xxl_fp16 + ae.safetensors reproduced the target halftone/pop-art comic style (soft halftone dot gradients, bold black ink linework, duotone color grading, vintage print grain) on two independent prompts: one generic superhero pose (unintentionally reproduced Spider-Man's copyrighted color scheme/emblem, flagged unusable) and one fully original armored-explorer character (clean, no IP conflict). Confirms this artstyle is achievable locally without an API model. |
| [system] | ComfyUI local generation, CyberpunkKrea_test_00001_.png | Local test of base flux1-krea-dev_fp8_scaled (no LoRA) against a cinematic cyberpunk-interior reference (cluttered retro-tech apartment, stacked glowing CRT monitors, magenta/teal neon volumetric lighting, film grain, photoreal concept-art rendering) produced a close match on the first attempt -- correct composition logic, lighting behavior, material realism, and mood, with no LoRA required. Confirms Flux-Krea's base tuning already covers cinematic/photoreal cyberpunk styles, unlike the flat halftone/pop-art comic style which needed a dedicated LoRA. |
| [system] | Get-WinEvent -FilterHashtable @{LogName='System'; Level=1,2} output, 2026-08-24 | Two full system crashes in <24h (2026-08-24 07:12 and 13:35), both Windows bugcheck 0x113 VIDEO_TDR_TIMEOUT_DETECTED_FAILURE with NVIDIA vendor ID (0x10de) in the bugcheck parameters -- confirmed via Get-WinEvent on the System log. Root cause: the NVIDIA driver hung during sustained heavy GPU load (long-running Flux/ComfyUI generation jobs) long enough that Windows' TDR watchdog attempted a driver reset, and the reset itself failed, crashing the whole machine rather than just the app. Both crashes occurred during/near active local-generation test windows in this session. |
| [system] | WO 2026-08-23-007 Decisions 16, 24 (closed); spin-off WO 2026-08-24-003 | Child WO 2026-08-23-007 (ComfyUI revision lane) closed with 2 of 4 asset-revision flaw categories fully verified, directly informing the Director Console's Asset Production Department (WO 2026-08-23-001, section 5.4): (1) Background-clutter/environment-element flaws are resolved via automated segmentation masking -- installed rembg (u2net) locally, generates a pixel-accurate object mask, then masked img2img revision on Flux (flux1-krea-dev_fp8_scaled) cleanly removes/replaces background content while preserving the asset. Directly usable for the plan's Tier 3/4 environment-element and reference-plate workflows. (2) Whole-object turnaround-identity consistency is resolved by replacing 2D-turnaround generation with direct single-view image-to-3D mesh generation -- installed native ComfyUI Hunyuan3D-2 support (hunyuan3d-dit-v2.safetensors, ~5GB, fits comfortably in 10GB VRAM for shape-only generation), which produces one 3D mesh from a single concept image; front/back/any-angle views are then just camera rotations of that mesh in Blender, guaranteeing consistency by construction rather than by prompt engineering. This directly validates and de-risks the plan's asset creation funnel (section 5.4: CONCEPT -> AI 3D GENERATION -> BLENDER) and confirms Blender-owns-spatial-truth as the correct approach for character/prop turnarounds, exactly as the plan's governing principle states. Two flaw categories remain open (object material/style revision without unwanted geometry; whole-frame rendering-style consistency) and are tracked separately in the spun-off WO 2026-08-24-003 -- not yet solved, should not be assumed working when planning V4 ComfyUI Integration or the Asset Production Department build order. |
## Open questions

<!-- None open — the V0 tracer-bullet design was accepted and routed to execution (History 2026-08-23T23:29:52Z). -->

## Next move

Director runs the V0 proof: generate the five S001-S005 before images, run each packet through Qwen3.5-9B Q4 in LM Studio Bionic, apply revisions, and record human_judgment verdicts against the 3-of-5 threshold.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-23T20:02:38Z — Created

- **State:** notice
- **Status:** active
- **Actor:** codex
- **Rationale:** User requested a durable Work Object and continuous grilling session for recommendations around local AI animation studio model architecture.
### 2026-08-23T20:02:56Z — Activated for grilling

- **State:** explore
- **Status:** active
- **Actor:** codex
- **Rationale:** The user explicitly requested a Work Object and grilling session to develop the local AI animation studio model architecture.
### 2026-08-23T20:04:22Z — Recorded first loop decision

- **State:** explore
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted starting the local AI animation studio architecture with an image-to-critique-to-revision loop; next grilling question is the artifact boundary for that loop.
### 2026-08-23T20:05:24Z — Recorded artifact boundary decision

- **State:** explore
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted using an image plus a small structured shot object as the first critique-loop input; next grilling question is the minimal field set for that shot object.
### 2026-08-23T20:06:12Z — Recorded minimal shot object decision

- **State:** explore
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted the small initial shot object field set and deferred continuity fields; next grilling question is the critique-loop output authority boundary.
### 2026-08-23T20:08:34Z — Recorded Blender second-loop decision

- **State:** explore
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted keeping still-image critique as V0 and staging Blender MCP as V1 with read-only scene/viewport evidence and governed operation proposals before write execution.
### 2026-08-23T20:10:15Z — Recorded Blender V1 authority boundary

- **State:** explore
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted keeping Blender V1 read-only plus proposed governed operations, with write execution and arbitrary Python deferred until later proof.
### 2026-08-23T20:11:29Z — Recorded V0 output authority boundary

- **State:** explore
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted that V0 should produce diagnosis plus structured revision instructions rather than executable ComfyUI parameter changes; next grilling question is the success/failure test for V0.
### 2026-08-23T20:29:45Z — Recorded V0 proof test

- **State:** explore
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted the five-pair before/after render test with 3-of-5 improvement and zero preserve/avoid violations as the success threshold; next grilling question is the runtime path for V0 testing.
### 2026-08-23T20:36:23Z — Recorded LM Studio Bionic runtime decision

- **State:** explore
- **Status:** active
- **Actor:** codex
- **Rationale:** User stated they are using LM Studio Bionic, so V0 testing should start there while preserving later migration to API runtimes after proof.
### 2026-08-23T20:37:12Z — Recorded first model decision

- **State:** explore
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted Qwen3.5-9B Q4 as the first model to test in LM Studio Bionic, with Gemma 3 12B Q4 as fallback and cloud escalation only after local options fail.
### 2026-08-23T20:38:06Z — Recorded V0 test packet shape

- **State:** explore
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted the V0 test packet shape; architecture-grilling branch is ready to converge into designing or collecting the five proof cases.
### 2026-08-23T20:38:39Z — Converged architecture grilling branch

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted convergence from architecture exploration into designing the five V0 proof cases; next stage is a tracer-bullet design for the proof run.
### 2026-08-23T20:38:55Z — Set design next action

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** After convergence, the Work Object should resume by designing the five V0 proof cases for the tracer-bullet test.
### 2026-08-23T20:39:45Z — Recorded synthetic test-case source

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** User selected synthetic cases for the V0 proof, so the tracer design should define controlled failure cases rather than collect current creative work.
### 2026-08-23T20:40:44Z — Recorded five-case synthetic proof suite

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted the exact five synthetic failure-mode cases for the V0 proof suite.
### 2026-08-23T20:43:41Z — Recorded shared protagonist/world decision

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted using one protagonist and shared world across S001-S005, with Mara as the recurring subject.
### 2026-08-23T20:44:59Z — Recorded shared Mara/world definition

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted the grounded cinematic sci-fi courier world as the consistency constraint for S001-S005.
### 2026-08-23T20:49:21Z — Recorded V0 before-image prompts

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted the five deliberately flawed before-image prompts for the synthetic V0 proof suite.
### 2026-08-23T20:53:55Z — Recorded V0 shot-object JSON

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** User accepted the S001-S005 shot-object JSON, completing the prompt plus structured intent layer for the synthetic V0 proof suite.
### 2026-08-23T23:29:52Z — Director accepted V0 tracer-bullet design; routed to execution

- **State:** build
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** User confirmed acceptance of the V0 tracer-bullet design ('yes accept'); all 16 design decisions recorded; transitioning design to build to implement the five-pair synthetic proof. GPU/VRAM success evidence and Next move reconciled.
### 2026-08-23T23:34:04Z — Implemented V0 proof packet suite

- **State:** build
- **Status:** active
- **Actor:** github-copilot
- **Rationale:** Created 12 files under v0-proof/: 5 before-image prompts (S001-S005), 5 shot-object JSON, packet template with critic output schema + human-judgment fields, and README run procedure. All 5 JSON validated (required fields present). Manual proof run in LM Studio Bionic pending director.
### 2026-08-24T19:46:47Z — Live-question investigation: answered

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Local Flux.1-Krea + Retro Comic Flux LoRA (strength 0.85, trigger c0m1c) reproduces the target halftone/pop-art comic illustration style closely, verified on two independent generations. First generation unintentionally surfaced Spider-Man's copyrighted color scheme/emblem despite no character-name prompting -- flagged unusable, corrected on the second generation with an original-character, IP-safe prompt pattern that preserved the style cleanly. Conclusion: no API model is needed for this specific artstyle; the existing local pipeline covers it.
### 2026-08-24T19:51:13Z — Live-question investigation: answered

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Question: can the local pipeline produce a cinematic cyberpunk-interior photoreal artstyle (reference: cluttered retro-tech apartment, glowing CRT monitors, magenta/teal neon, film grain), or is an API model needed. Answer: base flux1-krea-dev_fp8_scaled, no LoRA, matched the reference closely on the first generation -- confirms Flux-Krea's own tuning already covers cinematic/photoreal styles natively. Combined with the earlier Retro Comic Flux LoRA finding, the local pipeline now has two confirmed artstyle coverage points (flat halftone/comic via LoRA, cinematic/photoreal natively) with no API model needed for either.
### 2026-08-24T20:42:02Z — Recorded hardware-reliability gap: sustained-load GPU driver crashes

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Two TDR-failure system crashes in <24h during active local-generation test windows are a real constraint on the local-AI-studio hardware plan, not a one-off fluke -- this is a [gap], not yet mitigated. Candidate mitigations identified (raise TdrDelay registry timeout, verify VRAM headroom under Flux's full load, consider NVIDIA Studio driver branch, monitor thermals/power during sustained jobs) but none applied yet -- these are system-level changes outside this skill's write authority and were left for the director to apply directly.
### 2026-08-24T22:01:04Z — Child WO 2026-08-23-007 closed; evidence rolled up for Director Console (2026-08-23-001) continuation

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** The ComfyUI revision-lane WO closed with two validated, reusable mechanisms directly applicable to the Director Console's Asset Production Department: rembg-based segmentation masking for regional/background flaws, and Hunyuan3D single-view mesh generation for turnaround-identity consistency. Both are installed and working on this exact 10GB hardware. Two flaw categories remain unsolved and are tracked in spin-off WO 2026-08-24-003 -- work on the Director Console's V4 ComfyUI Integration or Asset Production Department build order should treat those as open, not assumed working.
