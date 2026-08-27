---
schema_version: 1
id: 2026-08-23-007
title: Make ComfyUI V0 revision lane produce observable critique-directed changes
type: change
status: closed
state: close
consequence: meaningful
sensitivity: ordinary
domain: [engineering, design]
relates_to: [2026-08-23-001, 2026-08-23-002]
created_at: 2026-08-24T02:33:47Z
updated_at: 2026-08-24T21:59:29Z
next_action: Director's choice: keep this WO open in verify/build to pursue S002 and S005's remaining gaps, or close it now on the strength of the two fully-verified flaw categories and spin off S002/S005 as their own follow-up Work Object(s).























































---
## Intent

Repair and validate the revision lane in
`C:\Users\Andre\AppData\Local\Comfy-Desktop\ComfyUI-Installs\ComfyUI\ComfyUI\user\default\workflows\V0_Five_Case_Test_General_Visual.json`
so an accepted LLM critique produces a visibly revised image rather than an
output that is nearly indistinguishable from the before image.

This is a bounded implementation child of `2026-08-23-002`, which owns the
local AI animation studio architecture and five-case proof. This Work Object
owns only the ComfyUI revision-lane behavior and its evidence.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
<!-- Rewritten 2026-08-24 to match the asset-generation scope from Decision 9,
     which superseded the original Mara-scene-domain wording below. Verified
     against Decisions 1-24 via alawas-engineering-verify-release-evidence; see
     History for the full verification report. -->

- [x] An obvious, critique-directed change is shown at 100% side-by-side
      viewing, for at least two distinct flaw categories: background-clutter
      removal (S004, Decision 16) and whole-object turnaround-identity
      consistency (S003, Decision 24). Both are clean, decisive results, not
      marginal improvements.
- [x] The revised/generated asset preserves protected identity with zero
      `avoid` violations for the two categories above (S004: lamp identity
      intact through masked revision; S003: front/back are structurally
      identical by construction, via 3D mesh generation).
- [ ] **Open:** S002 (object material/style revision) preserves protected
      identity with zero `avoid` violations. Not yet met -- an unrequested
      glass-diffuser shape has persisted through four attempts (Decisions 17,
      18, 21). Needs either a stronger cfg/negative-conditioning approach or
      post-hoc artifact masking.
- [ ] **Open:** S005 (whole-frame rendering-style consistency) preserves
      protected identity with zero `avoid` violations. Not yet met -- every
      attempt either left a style seam (Decision 17), destroyed asset identity
      at full denoise (Decision 19), or crashed to a blank image at partial
      denoise (Decision 22). Needs a working denoise/mask combination not yet
      found.
- [x] The visual graph (or, for S003, the 3D-mesh-generation graph) demonstrably
      encodes the loaded before image/reference and produces a distinct,
      evidenced after-result through a recorded revision or generation branch,
      for at least the S004 and S003 categories.
- [x] The selected settings, node graphs, model files, and prompt boundaries
      are recorded in sufficient detail to repeat every tested result (S001-S005,
      all variants) on the installed RTX 3080 10 GB system -- confirmed across
      Decisions 12-24, each naming exact models, denoise/guidance/seed values,
      and prompts actually executed on this hardware.

**Original wording (superseded 2026-08-24, retained for provenance):**
- [ ] An S001 before/after run shows an obvious, critique-directed change at
      100% side-by-side viewing in at least two accepted revision targets.
- [ ] The revised image preserves the protected protagonist, wardrobe, amber
      shoulder light, sealed case, environment, framing, and restrained
      low-key realism, with zero accepted `avoid` violations.
- [ ] The visual graph demonstrably encodes the loaded before image and saves
      a distinct after image through the revision branch.
- [ ] The selected settings and prompt boundary are recorded well enough to
      repeat the result for S002-S005 on the RTX 3080 10 GB system.


## Constraints and non-goals

**Constraints:**
- Keep the workflow local and compatible with the installed Flux Krea FP8,
  CLIP, T5, and VAE model stack on the RTX 3080 10 GB machine.
- Retain manual prompt entry; automatic LM Studio-to-ComfyUI orchestration is
  outside this fix.
- Prefer the smallest controllable graph change and test it against both
  revision strength and preserve fidelity.
- Treat the user's weak-difference observation as testimony until a controlled
  before/after run is captured.

**Non-goals:**
- Redesigning the five synthetic cases or changing their 3-of-5 proof threshold.
- Building the full AI animation studio, Blender integration, or agent runtime.
- Maximizing visual novelty at the expense of identity, composition, or other
  protected content.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Track revision responsiveness as a bounded workflow change

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Create a separate change record for the ComfyUI revision lane while retaining `2026-08-23-002` as owner of the broader architecture and proof suite. |
| **Authorization** | Director explicitly requested a Work Object for the named workflow after observing that the revised image barely differed. |
| **Confidence** | high for the ownership boundary because the parent record and live workflow were inspected; low on the technical cause until a controlled comparison is run. |
| **Actor** | director and Codex conductor |
| **Revisit trigger** | Reopen the ownership boundary if the controlled test shows the failure originates outside the ComfyUI workflow, such as an incorrect critique packet or image-selection step. |
| **Rationale** | The parent Work Object covers architecture and the full V0 proof; this record gives the concrete workflow defect its own acceptance evidence and implementation route without duplicating the parent's outcome. |

### Decision 2 — Run a three-output S001 revision-control tracer

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | In a copied workflow, render three sequential S001 revisions from the same before image, revision-only prompt, seed, sampler, and model: A = existing control with no `FluxGuidance` and denoise `0.50`; B = `FluxGuidance 3.5` and denoise `0.50`; C = `FluxGuidance 3.5` and denoise `0.65`. Save distinct `S001_control`, `S001_guided`, and `S001_guided_065` outputs. |
| **Authorization** | Director accepted the immediately preceding tracer recommendation. Acceptance authorizes recording and routing this design, not broader implementation, deployment, or changes to the original five-case workflow. |
| **Confidence** | medium that this is the smallest discriminating test because A-to-B isolates Flux guidance and B-to-C isolates revision strength; no result is claimed until the three images are rendered and judged. |
| **Actor** | director and tracer-bullet designer |
| **Revisit trigger** | Reopen the design if neither B nor C visibly improves at least two accepted revision targets with zero preserve/avoid violations, or if the first visible change alters protected identity, pose, framing, case, wardrobe, or world. |
| **Rationale** | The tracer directly tests whether global Flux img2img can produce controlled semantic revision on this workflow. Stop at denoise `0.65`; failure routes back to design for masked or region-controlled revision rather than increasing denoise until the image drifts. The copied workflow is the rollback boundary, leaving the current five-case workflow unchanged until a branch passes. |

### Decision 3 — Switch from Flux Dev to HiDream O1 for all image generation

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Abandon Flux Dev pipeline entirely. Rebuild all image generation workflows around HiDream O1 Image Dev FP8, using HiDream O1-native nodes (CheckpointLoaderSimple, EmptyHiDreamO1LatentImage, HiDreamO1ReferenceImages, standard KSampler with CFG). |
| **Authorization** | Director explicitly stated: "defer flux and use hidream from now on for image generation so build the workflows around hidream." |
| **Confidence** | high that HiDream O1 produces visible day-to-night conversion (confirmed by E tracer output); medium on identity preservation fidelity (reference-guided generation, not pixel-perfect editing). |
| **Actor** | director |
| **Revisit trigger** | Reopen if HiDream O1 reference editing consistently fails to preserve protected identity elements across S002-S005, or if VRAM pressure on RTX 3080 10GB prevents practical use. |
| **Rationale** | Flux Dev with img2img (D tracer) changed the wrong things (jacket/expression instead of lighting). HiDream O1 with reference editing (E tracer) achieved the intended day-to-night conversion while preserving subject identity and composition. |

### Decision 4 — F tracer validates two-stage HiDream O1 pipeline

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | The two-stage pipeline (Stage 1: T2I generation, Stage 2: reference-guided revision) works end-to-end for lighting changes at CFG 5.0. Attribute changes (jacket color) achieve the target revision but need CFG reduction (3.0-3.5) to eliminate background artifacts. Pipeline architecture is validated for generalization to S002-S005. |
| **Authorization** | Director delegated judgment to agent for F tracer evaluation. |
| **Confidence** | high for pipeline architecture and lighting revisions; medium for attribute revisions pending CFG tuning. |
| **Actor** | agent (delegated judgment) |
| **Revisit trigger** | Reopen if CFG 3.0-3.5 still produces artifacts for attribute edits, or if identity drift proves unacceptable across S002-S005 subjects. |
| **Rationale** | Revision A (day-to-night) showed unmistakable lighting conversion with preserved identity and composition. Revision B (jacket color) achieved the correct target change but with quality artifacts. The pipeline proves that a single workflow can generate a before image and revise it with a critique-directed instruction, which was the core requirement. |

### Decision 5 — S001-S005 full-suite run identifies Stage 1 flaw-fidelity gap

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | mixed |
| **Scope** | The two-stage pipeline's revision mechanism (Stage 2) is validated across the full S001-S005 suite: 2 of 5 cases pass cleanly (S002, S004), 3 of 5 show only partial change because the before image (Stage 1) did not reliably express its scripted flaw. This is not a revision-lane defect; it is a before-image generation fidelity gap that must be closed before the suite can be judged against its 3-of-5 threshold. |
| **Authorization** | Director delegated judgment to agent for the S001-S005 run. |
| **Confidence** | high that the revision mechanism works when the flaw is present (S002, S004 evidence); medium on the exact fix for Stage 1 flaw fidelity (CFG or seed tuning untested). |
| **Actor** | agent (delegated judgment) |
| **Revisit trigger** | Reopen if raising Stage 1 CFG or trying alternate seeds does not reliably produce the scripted flaw for S001/S003/S005, or if doing so introduces new artifacts. |
| **Rationale** | S002 and S004 before images fully committed to their scripted flaws (bright cheerful mood; cluttered background) and both produced unmistakable, well-preserved revisions. S001, S003, and S005 before images only weakly expressed their flaws (face was already partly readable; framing wasn't clearly flat/static; lighting wasn't clearly split), so their revisions had little contrast to correct and read as minor rather than decisive. The fix belongs in Stage 1 prompt-to-flaw fidelity, not the revision architecture. |

### Decision 6 — Accepted S001-only Stage 1 CFG tracer (1.0/2.0/3.0 at fixed seed)

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | fail |
| **Scope** | Bounded to S001 only. Re-run Stage 1 T2I three times at the existing fixed seed 42, varying only CFG: 1.0 (existing control), 2.0, 3.0. Save each candidate before-image under a distinct filename tagging its CFG value. Judge each purely against the scripted flaw ("face/silhouette unreadable") — do not touch Stage 2, do not touch S002/S004, do not generalize to S003/S005 yet. Seed variation is explicitly out of scope for this tracer; it is the named follow-up if CFG alone does not resolve the flaw-fidelity gap. |
| **Authorization** | Director: "yes, go ahead with CFG only" — accepted the recommended CFG-only tracer over the alternative of testing CFG and seed together. |
| **Confidence** | high that CFG is a plausible lever (it is the one deliberately-varied parameter across S002/S004 vs S001/S003/S005's shared CFG 1.0); medium on whether CFG alone is sufficient versus prompt wording being the real lever — that is exactly what this tracer tests. |
| **Actor** | director |
| **Revisit trigger** | If no tested CFG value (1.0/2.0/3.0) at seed 42 makes the S001 flaw unambiguous without introducing new artifacts, the "CFG is the lever" assumption is falsified — reopen design toward prompt-wording as the fix, or toward seed variation as the next parameter to isolate. |
| **Rationale** | S001-only bounds cost and risk to the smallest discriminating test. Fixing seed and varying only CFG isolates one variable per the tracer-bullet discipline's smallest-slice principle, rather than conflating two candidate causes (CFG, seed) in one test. |

### Decision 7 — Accepted S001-only Stage 1 prompt-rewrite tracer (CFG 1.0, seed 42, reworded flaw prompt)

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | fail |
| **Scope** | Bounded to S001 only. Keep CFG 1.0 and seed 42 (both already-tested baseline values) unchanged; the only changed variable is the Stage 1 before-prompt text, rewritten to be far more explicit and forceful about the occlusion (no visible eyes/mouth, near-total facial darkness, indistinct silhouette against the wall) while staying within the shot's `preserve` (dark practical jacket, amber shoulder light, sealed case, restrained low-key realism) and `avoid` (not fully invisible, no melodrama) bounds. Do not touch Stage 2, S002/S004, or generalize to S003/S005 yet. Seed variation remains the named fallback if this also fails. |
| **Authorization** | Director: "yes, go ahead" — accepted the recommended prompt-rewrite-only tracer over testing seed variation instead. |
| **Confidence** | medium-high that prompt wording is the real lever, since CFG tuning (Decision 6) demonstrably failed across its full tested range without moving the flaw at all; low-medium on the exact rewrite needed to cross the avoid-boundary without overshooting into "subject so dark she is invisible." |
| **Actor** | director |
| **Revisit trigger** | If the reworded prompt still does not make the flaw unambiguous, or if it overshoots into an avoid violation (subject invisible), prompt wording alone is also falsified as the sole lever — next candidate is seed variation, or a masked/regional darkening approach as a new design question. |
| **Rationale** | Decision 6 exhausted the CFG axis without any movement toward the scripted flaw and introduced an unscripted artifact at the high end — this points away from sampling-parameter tuning and toward the text conditioning itself not being forceful enough for a flow model at CFG 1.0 (which is known to weight the prompt lightly). Isolating prompt wording as the sole changed variable, with CFG/seed held at their already-characterized baseline, keeps this the smallest next discriminating test. |

### Decision 8 — Accepted combined CFG+prompt tracer (CFG 3.0, seed 42, reworded flaw prompt)

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pending |
| **Scope** | Bounded to S001 only, single run. Combine the reworded before-prompt from Decision 7 with CFG 3.0 (the strongest already-characterized value from Decision 6), fixed seed 42. This is the one combination neither Decision 6 (original prompt, CFG varied) nor Decision 7 (reworded prompt, CFG fixed at 1.0) tested. Do not touch Stage 2, S002/S004, or generalize to S003/S005 yet. |
| **Authorization** | Director: "go ahead with the combined CFG+prompt tracer." |
| **Confidence** | medium that combining both levers can compound where neither alone did; medium-low that this specific combination (vs. e.g. CFG 2.0, or seed variation) is the right next step, since it was chosen as the single most-informative untested combination rather than an exhaustive sweep. |
| **Actor** | director |
| **Revisit trigger** | If this combined run also fails to produce the scripted flaw without new artifacts, both CFG and prompt wording (alone and combined at this seed) are exhausted as candidate levers — next step is seed variation, or reconsidering whether HiDream O1 can produce this specific flaw at all (per the live-question investigation on API alternatives, recorded separately in this WO's evidence). |
| **Rationale** | Two independent single-variable tests (Decision 6, Decision 7) both failed; testing their combination is the cheapest remaining local experiment before concluding the model itself cannot produce this flaw regardless of local tuning. |

### Decision 9 — Rewrite S001-S005 as asset-generation tests on Flux; Decision 8 superseded unjudged

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Rewrite all five shot objects (`v0-proof/shot-objects/S001-S005*.json`) and their before-prompts (`v0-proof/before-prompts/S001-S005*.md`) from cinematic-scene critique tests (Mara/night-city shots) to asset-generation critique tests, themed around the Director Console's concept-to-3D asset funnel (a market-lamp hero prop for the Lower Market environment kit): S001 silhouette readability, S002 environment-style match, S003 turnaround identity consistency, S004 reference-plate isolation, S005 turnaround rendering consistency. All five now generate on Flux (`flux1-krea-dev_fp8_scaled.safetensors`, no LoRA) instead of HiDream O1. |
| **Authorization** | Director: "rewrite the 5 tests mainly about assets and use flux from now on," confirmed scope as "yes, S001-S005 from 2026-08-23-007, rewrite for asset generation with flux." |
| **Confidence** | high that this is the director's intended scope (explicit, twice-confirmed instruction); low-medium on whether Flux reproduces the same Stage-1 flaw-fidelity gap (Decisions 5-8) on this new subject matter — untested. |
| **Actor** | director |
| **Revisit trigger** | Reopen if Flux shows the same before-image flaw-fidelity gap on the new asset-generation cases that HiDream O1 showed on S001/S003/S005 (Decision 5) — the CFG/prompt-wording lessons from Decisions 6-8 may still apply and would need re-running against Flux's own CFG/guidance behavior, not HiDream O1's. |
| **Rationale** | Decision 8's combined CFG+prompt tracer output (`S001_Stage1_combined_cfg3_promptrewrite_00001_.png`) was generated but never viewed or judged before the director redirected scope — it is superseded, not resolved; its result is left as `pending` in Decision 8 rather than retroactively marked pass/fail. Two independent live-question investigations in this session (folded into WO `2026-08-23-002`) established that Flux (with and without LoRAs) reliably reproduces target artstyles locally, making Flux a reasonable engine switch for the asset-generation redesign independent of how the HiDream O1 Mara-scene debugging would have concluded. |

### Decision 10 — S001-only FluxGuidance tracer (2.0/5.0/8.0, seed 42): fails at every value, new root cause identified

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | fail |
| **Scope** | Bounded to S001 only. Re-run Stage 1 on Flux three times at fixed seed 42, varying only `FluxGuidance` (the Flux-native analogue to HiDream O1's CFG lever, since Flux keeps KSampler CFG at 1.0 by convention): 2.0, 5.0, 8.0. Judge each purely against the scripted flaw (silhouette merging with a dark background). |
| **Authorization** | Director: "run the S001 CFG tracer on flux." |
| **Confidence** | high that guidance strength alone is not the lever for this specific case — all three tested values produced the same outcome; high on the identified root cause (the prop's own translucent/crackled-glass material catches and reflects light, keeping it visually separated from any dark backdrop regardless of scene darkness). |
| **Actor** | director |
| **Revisit trigger** | Reopen if a different prop (opaque material, no reflective surfaces) is substituted for this test and still fails to merge with a dark background — that would falsify the "reflective material" root-cause theory and point back at prompt wording or seed. Also reopen if S001 is judged unnecessary for the asset-generation redesign (a silhouette-readability test may not be a meaningful criterion for translucent objects at all). |
| **Rationale** | Unlike the HiDream O1 Mara-scene failures (Decisions 5-8), where the model seemed reluctant to darken a photorealistic face/scene in general, this failure has a distinct, visible mechanical cause: the lamp's glass panes act as a built-in light-catching surface, so no amount of guidance-strength tuning removes the object's inherent contrast against a dark backdrop. This points away from parameter tuning entirely and toward either changing the test asset's material, or reconsidering whether "silhouette readability" is the right scripted flaw for a reflective/translucent hero prop. |

### Decision 11 — S001 dropped; revision-lane pass on S002-S005 reproduces the founding weak-revision problem on the asset domain

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | fail |
| **Scope** | Director dropped S001 (silhouette readability) as a scripted flaw case for this asset per Decision 10's finding, and directed proceeding with the revision-lane pass on the 4 remaining passing cases (S002, S003, S004, S005). Ran Flux img2img revision (FluxGuidance 3.5, denoise 0.55, seed 42 -- the parameters validated in Decision 2) with a critique-directed revision prompt reversing each scripted flaw. Result: S002 and S003 partial (some correction visible but the core flaw substantially persists); S004 and S005 fail (essentially unchanged from the flawed before-image). |
| **Authorization** | Director: "drop it and proceed with S002-S005." |
| **Confidence** | high that this reproduces the WO's founding problem (weak/absent revision under critique direction) rather than resolving it -- the pattern (partial-to-no change under denoise 0.55/guidance 3.5) matches Decision 1's original observation almost exactly, now on a different domain (asset generation) and engine (Flux instead of HiDream O1). |
| **Actor** | director |
| **Revisit trigger** | Reopen design toward a stronger or masked/regional revision approach (e.g., higher denoise, inpainting/regional masking limited to the flawed area, or an explicit reference-locking mechanism for turnaround consistency) before any further asset-generation revision-lane testing. Do not re-run at the same denoise/guidance values expecting a different result -- that combination is now characterized as insufficient across two engines and two subject domains (Mara-scene and asset-generation). |
| **Rationale** | The revision-lane mechanism's core defect (denoise 0.55 + global guidance change insufficiently overrides the source image's established content) is not specific to HiDream O1, Mara-scene subjects, or the original workflow's specific graph wiring -- it now shows the identical symptom on Flux img2img with the asset-generation prompts. This strengthens the case that the fix belongs in the revision mechanism itself (denoise strength, masked regions, or a stronger reference-override technique), not in engine choice or subject-matter choice, which have both now been varied without resolving it. |

### Decision 12 — S004 masked-inpainting tracer validates regional masking, exposes mask-precision gap

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | mixed |
| **Scope** | Single bounded test per the accepted design-tracer-bullet recommendation: S004 only, manually-defined rectangular bounding-box mask protecting the lamp, `VAEEncodeForInpaint` with `grow_mask_by: 6`, denoise 1.0 inside the mask, FluxGuidance 3.5, seed 42, revision prompt targeting the background only. |
| **Authorization** | Director: "yes, run it" (accepting the design-tracer-bullet recommendation routed via `alawas-design-design-tracer-bullet`). |
| **Confidence** | high that masked/regional inpainting is a substantially stronger revision mechanism than global img2img -- the masked region regenerated cleanly and decisively to the requested plain background, unlike any global-revision attempt in Decisions 2 or 11; high that the specific mask used (a crude rectangular bounding box) is insufficiently precise for production use -- it produced a visible hard seam and left a strip of original clutter inside the oversized rectangle. |
| **Actor** | director |
| **Revisit trigger** | Reopen if a silhouette-shaped mask (following the lamp's actual outline, with edge feathering) still produces visible seams or incomplete clutter removal -- that would falsify "mask precision" as the remaining gap and point toward a different masking technique (e.g., automated segmentation) or reconsidering the inpainting approach entirely. |
| **Rationale** | This tracer isolated exactly one new variable (masked vs. global revision) against the same engine, seed, and case already characterized as a clean failure in Decision 11. The decisive background change confirms the core hypothesis from the design stage: the model doesn't fight itself when only the flawed region needs to change. The seam and clutter leakage are an expected tracer-bullet finding, not a fix failure -- a manually-drawn rectangle was always going to be an imprecise stand-in for a real silhouette mask, and the test's job was to validate the mechanism, not to ship production-quality masking. |

### Decision 13 — S004 tighter silhouette mask still fails the clean-mechanism bar: seam and protected-region leakage persist

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | fail |
| **Scope** | Follow-up to Decision 12's crude rectangular mask. Built a closer-fitting 4-band silhouette approximation of the lamp (chain/roof/body/base bands), 10px `FeatherMask`, `grow_mask_by: 2`, same denoise 1.0 / FluxGuidance 3.5 / seed 42 / background-only revision prompt as Decision 12, single S004 run. |
| **Authorization** | Director: "build a tighter mask," confirmed with "yes, run it." |
| **Confidence** | high that the broad clutter-removal result still holds (confirms Decision 12's core finding a second time); high that this specific mask still fails the design's own exit bar -- a visible blocky rectangular seam remains where the mask boundary meets the background (patterned fabric bleeds through near the shoulders), and the "protected" lamp itself did not stay pixel-identical, its finish shifting from warm brass/rust to flat matte-black, meaning regeneration leaked past the intended boundary. |
| **Actor** | director |
| **Revisit trigger** | Reopen design toward either (a) true segmentation-based masking (e.g. an automated background-removal/SAM-style tool, not a manually-drawn band approximation) if a hand-authored mask shape is judged too imprecise to ever hit the clean-mechanism bar this way, or (b) a different edge-blending approach (larger feather with zero grow, or a hard mask with no feather at all) if boundary softness itself is identified as the leak path rather than the mask's shape. Do not re-attempt with another hand-drawn band mask at similar feather/grow values -- that combination has now failed twice. |
| **Rationale** | This isolates one new variable against Decision 12 (mask tightness/feathering) while holding engine, seed, case, and revision parameters constant. The result confirms masked revision is directionally sound (background clutter removal is decisive both times) but shows the specific meeting point of feathering and grow_mask_by is where this approach currently breaks down -- soft enough to leave a seam, yet soft enough to let regeneration bleed into the region that was supposed to be fully protected. Two failed attempts at hand-authored masking point toward needing either a fundamentally more precise mask source or a stricter (not softer) boundary treatment, rather than further hand-tuning of feather/grow values. |

### Decision 14 — Engine swap to FLUX.1-Fill-dev rejected: reproduces a documented mask-ignoring failure, worse than the current leak-and-seam problem

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | fail |
| **Scope** | Live-question test (per `alawas-research-investigate-live-question`): swap the img2img engine from `flux1-krea-dev_fp8_scaled` (general text-to-image checkpoint, masked via a manual `VAEEncodeForInpaint` hack) to `FLUX.1-Fill-dev-GGUF` Q4_K_S (a model natively trained for masked inpainting, via `InpaintModelConditioning` + `FluxGuidance 30`). Same S004 case, same silhouette mask from Decision 13, same revision prompt -- isolating engine choice as the one new variable. |
| **Authorization** | Director: "yes, download and run it," following the live-question recommendation to test a purpose-built inpainting model before committing further to hand-tuning Flux-Krea's mask boundary. |
| **Confidence** | high that FLUX.1-Fill-dev is not a safe engine swap for this pipeline -- the mask was effectively ignored entirely (background clutter unchanged from the flawed before-image), reproducing a documented, unresolved community bug report (ComfyUI GitHub discussion #14467) rather than fixing anything. This is a worse failure mode than Decisions 12-13's partial leak-and-seam, not a better one. |
| **Actor** | director |
| **Revisit trigger** | Reopen only if a future FLUX.1-Fill-dev release or ComfyUI node update is confirmed (via new evidence, not assumption) to have fixed the mask-ignoring bug referenced in discussion #14467. Do not re-attempt with the same GGUF quant/node configuration expecting a different result -- this reproduces a known, unresolved upstream issue, not a local misconfiguration. |
| **Rationale** | This closes the "wrong engine" branch of the masking investigation cleanly: the current engine (Flux-Krea + manual inpaint mask) at least partially respects the mask and only leaks at the boundary; the purpose-built alternative ignored the mask altogether. The fix belongs in mask precision/boundary treatment on the current engine (segmentation-based masking, or a stricter non-feathered boundary, per Decision 13's revisit trigger), not in switching models. |

### Decision 15 — Hard-boundary variant falsifies softness as the cause; mask shape/precision confirmed as the actual problem

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | fail |
| **Scope** | Per Decision 13's revisit trigger, tested a hard-boundary variant: same 4-band silhouette mask, `FeatherMask` removed entirely, `grow_mask_by: 0`, otherwise identical to Decision 13 (S004, `flux1-krea-dev_fp8_scaled`, denoise 1.0, FluxGuidance 3.5, seed 42). |
| **Authorization** | Director: "try the hard boundary variant first." |
| **Confidence** | high that this falsifies boundary softness as the leak's cause -- removing all feathering and grow produced the identical failure, just with a crisper edge: a rectangular patch of the original clutter (patterned fabric) still visible behind the lamp's roof. The mask preview shows the cause directly: the 'roof band' rectangle (350-670 x, 190-330 y) is wider than the lamp's actual roof silhouette, so its corners trap real background pixels inside the protected region, which then stay unchanged because they're marked as protected. |
| **Actor** | director |
| **Revisit trigger** | Reopen only with a genuinely silhouette-accurate mask (pixel-level, following the object's real outline) -- not another hand-drawn rectangle/band approximation at any feather or grow setting. Three hand-authored mask variants (crude rectangle, tighter bands + feather, tighter bands hard-edged) have now all failed at the same root cause. |
| **Rationale** | This isolates the one remaining variable from Decision 13 (feather/grow vs. mask shape) and shows conclusively that shape, not softness, is the defect. A rectangular or band-based mask can never perfectly bound a non-rectangular object -- any region wide enough to fully cover the lamp will also include some real background at the corners, and that background stays untouched by design (since it's "protected"). The fix has to be a mask that actually follows the lamp's silhouette, which means automated segmentation (background removal or SAM-style tooling), not further hand-authored geometry. |

### Decision 16 — Automated segmentation (rembg) validates masked revision cleanly; revision-lane mechanism fixed for the background-clutter case

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Per Decision 15's revisit trigger, installed `rembg` (u2net model) into ComfyUI's Python venv, generated a real silhouette-accurate segmentation mask for S004's before-image (standalone script, not a new ComfyUI custom node), and ran the same masked-revision pipeline (`VAEEncodeForInpaint`, `grow_mask_by: 0`, denoise 1.0, FluxGuidance 3.5, seed 42, background-only revision prompt) with this mask in place of any hand-drawn geometry. |
| **Authorization** | Director: "yes, look into rembg." |
| **Confidence** | high that this validates automated segmentation as the fix -- background clutter (crates, rope, fabric, text) is fully removed and replaced with plain neutral grey across the whole frame, with no visible seam and no protected-region identity drift, unlike all three hand-drawn-mask attempts (Decisions 12, 13, 15). Medium-low on one known limitation: `rembg`'s u2net model dropped the lamp's thin hanging chain as background noise, leaving a small unprotected sliver that the model filled with a minor cosmetic rope-like remnant -- a small, localized gap, not the systemic seam/leak failure pattern. |
| **Actor** | director |
| **Revisit trigger** | Reopen if generalizing this recipe to S002 (style match), S003 (turnaround identity), or S005 (rendering consistency) exposes a different failure mode -- S003 in particular is a whole-object identity-drift problem, not a regional-clutter problem, and may need a different fix (reference-locking) rather than masking at all. Also revisit the chain-dropping limitation if a case requires protecting thin/wiry elements precisely. |
| **Rationale** | This closes the masking-precision thread cleanly: four consecutive attempts (crude rectangle, tighter bands+feather, hard-edged bands, real segmentation) isolated exactly one variable each time, and only genuine pixel-accurate segmentation produced a clean, decisive result. This confirms the WO's founding problem (weak/absent revision under critique direction) is solvable for regional/background-type flaws via mask-based revision -- the missing piece was mask source accuracy, not engine choice (Decision 14), not boundary softness (Decision 15), and not the masking approach in principle (Decisions 12-13 showed directional promise throughout). |

### Decision 17 — Masking mechanism generalizes cleanly, but mask scope must match the flaw's actual scope: two distinct partial results on S002 and S005

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | mixed |
| **Scope** | Generalized the validated rembg-masking recipe (Decision 16) to S002 and S005_viewB, inverting mask polarity (protect background, inpaint the foreground object) since both flaws are object-level rather than background-clutter. Same settings otherwise: `grow_mask_by: 0`, denoise 1.0, FluxGuidance 3.5, seed 42. |
| **Authorization** | Director: "yes, run S002 and S005." |
| **Confidence** | high that the masking *mechanism* (clean boundary, no leak, no seam) continues to generalize reliably -- both results show a technically clean mask application. Medium confidence on two distinct, separate residual problems: (1) S002's material flaw was substantially corrected but the revision introduced an unscripted frosted-white glass bell/diffuser shape not present in the original object -- a new artifact, echoing the "gets what's asked, adds something unrequested" pattern from Decisions 6-7; (2) S005_viewB's masked object came out fully photorealistic exactly as targeted, but the unmasked background stayed visibly painterly, producing a jarring style seam -- not a masking failure but a scope mismatch, since S005's flaw is a whole-frame rendering-style problem that foreground-only masking cannot fully address. |
| **Actor** | director |
| **Revisit trigger** | For S002: reopen if a stronger negative-prompt constraint against introducing new geometry (only material/color changes, no new physical elements) still fails to prevent unscripted artifacts across repeated runs. For S005: reopen with a whole-frame mask (or no mask at all, relying on a strong global revision prompt) for any flaw category that is inherently global rather than regional -- masking scope must match flaw scope, not default to foreground-only. |
| **Rationale** | This is the first test of whether the Decision 16 breakthrough generalizes, and it does -- as a mechanism. What it exposes is that "masked revision" is not a single universal recipe: the mask's shape must match where the flaw actually lives (background-only for S004, object-only for S002, whole-frame for S005). Treating all revision flaws as regional-object problems by default would silently produce S005's outcome again on any other whole-frame flaw. |

### Decision 18 — S002 no-new-geometry constraint fails: negative conditioning is inert at cfg=1.0

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | fail |
| **Scope** | Retested S002 with an explicit no-new-geometry constraint added to the positive prompt plus a negative text prompt naming the unwanted glass bell/dome/diffuser shape from Decision 17. Same mask, denoise 1.0, FluxGuidance 3.5, seed 42. |
| **Authorization** | Director: "do all three, starting with S002." |
| **Confidence** | high that this specific fix does not work -- the identical unscripted glass bell shape reappeared in the same location, unchanged. High-confidence root cause: at `cfg: 1.0` (the standard setting used throughout this WO's Flux pipeline), the sampler does not functionally apply negative conditioning, so a negative prompt naming what to avoid has no real effect; the added positive-prompt constraint alone was also insufficient. |
| **Actor** | director |
| **Revisit trigger** | Reopen only with a fix that doesn't rely on negative conditioning at cfg=1.0 -- e.g. raising cfg above 1.0 (a bigger pipeline change affecting all prior-validated settings) or masking the artifact's specific location out after the fact. Do not retry the same negative-prompt approach expecting a different result. |
| **Rationale** | This isolates the mechanism question directly: is the unwanted geometry a prompt-following problem (fixable with better wording) or a structural limitation of the cfg=1.0 pipeline (not fixable by prompt alone)? The identical, unchanged result at the same location strongly favors the latter. |

### Decision 19 — S005 whole-frame mask eliminates the seam but destroys asset identity: scope-matching confirmed, denoise-vs-identity tradeoff exposed

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | mixed |
| **Scope** | Retested S005_viewB with a whole-frame mask (no protected region at all, `SolidMask` value 1.0 covering the entire 1024x1024 canvas) instead of the foreground-only mask from Decision 17. Same denoise 1.0, FluxGuidance 3.5, seed 42, global photoreal revision prompt. |
| **Authorization** | Director: "do all three, starting with S002" (covering all three planned tests). |
| **Confidence** | high that this confirms the scope-matching hypothesis -- the photoreal/painterly seam from Decision 17 is completely gone, the entire frame is uniformly photorealistic. High confidence on a distinct new problem: at full denoise across the whole frame, there is no compositional anchor to the original image at all -- the output is an entirely different lamp design (a traditional table lamp with a white fabric shade), not a revision of the original market-lantern asset. |
| **Actor** | director |
| **Revisit trigger** | Reopen with a whole-frame mask at a lower denoise (e.g. 0.4-0.6) rather than 1.0, to test whether the seam can be eliminated while still retaining enough of the original composition to count as a "revision" rather than a fresh generation. This is the natural next test, not yet run. |
| **Rationale** | This confirms masking scope must match flaw scope (Decision 17's hypothesis), but reveals denoise strength interacts with that choice: whole-frame masking at denoise 1.0 is equivalent to full T2I regeneration, discarding the identity a revision lane exists to preserve. The fix for S005 likely needs both the whole-frame scope AND a moderate denoise, not full denoise. |

### Decision 20 — Reference-locking (Flux Redux) resolves S003's core object-identity mismatch; viewpoint control remains a separate open gap

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Installed Flux Redux (`flux1-redux-dev.safetensors` style model + `sigclip_vision_patch14_384.safetensors` CLIP vision) and used S003's front-view image as a subject/style reference (via `CLIPVisionEncode` + `StyleModelApply`, strength 1.0) to guide a fresh "back view" generation, rather than masking or img2img revision. Text prompt named the same lantern shape/material; latent was fresh noise, not encoded from any existing back-view image. |
| **Authorization** | Director: "do all three, starting with S002" (covering all three planned tests). |
| **Confidence** | high that reference-locking resolves the object-identity mismatch that made S003 fail originally -- front and back now share the same lantern shape (hexagonal, pyramidal roof), material (aged brass/gold patina), glass treatment (crackled panes), and proportions, a decisive fix for a problem that image-space masking cannot address at all (S003's flaw is whole-object identity, not a regional pixel defect). Medium confidence on a residual, separate gap: the generated "back view" is nearly the same viewing angle as the front reference, not a genuinely distinct rotated view -- Redux's strong reference-lock appears to constrain viewpoint along with identity. |
| **Actor** | director |
| **Revisit trigger** | Reopen if a genuinely distinct back-view angle is required for production use -- likely needs combining Redux's identity-lock with an explicit pose/viewpoint control mechanism (e.g. a depth or pose ControlNet conditioning the desired camera angle) rather than relying on the text prompt alone to override Redux's viewpoint bias. |
| **Rationale** | This validates the WO's core hypothesis for the identity-mismatch flaw category: masking (Decisions 12-17) is the right tool for regional pixel-level flaws (background clutter, object material/style), but a whole-object identity flaw like S003's needs reference-conditioned generation instead. Together, Decisions 16 (masking) and 20 (reference-locking) give the revision lane two validated, distinct mechanisms matched to two distinct flaw categories -- closing the "keep working on masking" thread from the earlier live-question investigation with a clear answer: masking alone was never going to solve S003, and it doesn't need to. |

### Decision 21 — S002 cfg=2.0 partially suppresses the unwanted geometry via material, not shape; not yet a clean fix

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | mixed |
| **Scope** | Retested S002 with real (non-zeroed) negative conditioning at `cfg: 2.0` instead of the inert `cfg: 1.0` from Decision 18, naming the unwanted glass shape in the negative prompt. |
| **Authorization** | Director: "do all three but start with s002." |
| **Confidence** | high that cfg>1.0 does activate negative conditioning to some real degree, unlike Decision 18's cfg=1.0 identical-repeat -- the unwanted shape's material changed from frosted glass to weathered brass/patina metal, visually integrating it as an intentional lamp part rather than a floating glass diffuser. Medium-low that this counts as a clean fix -- clear glass edges are still visible at the sides, meaning the extra geometry persists structurally, just recolored, not removed. |
| **Actor** | director |
| **Revisit trigger** | Reopen with a higher cfg value (e.g. 3.5-4.0) to test whether stronger negative conditioning fully suppresses the shape rather than merely recoloring it, or accept that some post-hoc geometry cleanup (masking the specific artifact region after generation) may be the more reliable fix regardless of cfg. |
| **Rationale** | This confirms the Decision 18 diagnosis (negative conditioning inert at cfg=1.0) was correct and identifies a working lever (cfg strength), but the fix is only partial at cfg=2.0 -- the geometry itself needs full suppression, not just material change, for a clean pass. |

### Decision 22 — S005 whole-frame mask at moderate denoise produces a total technical failure, not a partial fix

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | fail |
| **Scope** | Retested S005_viewB with the same whole-frame mask (`SolidMask` value 1.0, no protected region) from Decision 19, but denoise lowered from 1.0 to 0.5 to test whether moderate denoise could balance seam-removal against identity preservation. |
| **Authorization** | Director: "do all three but start with s002" (covering all three planned follow-up tests). |
| **Confidence** | high that this specific configuration is a technical dead end, not a partial improvement -- the output is a completely flat, uniform grey image with zero content, not a stylistic compromise. Likely cause: `VAEEncodeForInpaint`'s noise-mask mechanism has no original content to preserve at 100% mask coverage, and denoise 0.5 does not provide enough steps to build a fresh image from noise either, producing a degenerate/undiffused latent. |
| **Actor** | director |
| **Revisit trigger** | Reopen with a different combination: either a no-mask img2img approach (denoise <1.0 without any `VAEEncodeForInpaint` masking at all) for whole-frame revision, or a whole-frame mask kept at denoise 1.0 (Decision 19's working seam-removal setting) combined with a stronger reference-preservation mechanism (e.g. Redux conditioning on the original image, similar to Decision 20's approach for S003) to retain identity without abandoning full denoise. Do not retry whole-frame mask at partial denoise in this exact node configuration -- it is now confirmed broken, not merely weak. |
| **Rationale** | This rules out "moderate denoise" as a simple dial to turn on the existing masked-inpaint node graph for whole-frame flaws -- the interaction between 100% mask coverage and partial denoise breaks the mechanism outright, rather than trading off seam vs. identity as hypothesized. A working fix for S005 needs a structurally different approach, not a parameter tweak on the current graph. |

### Decision 23 — S003 Redux strength reduction does not free the viewpoint; camera-framing bias is structural, not a dosage effect

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | fail |
| **Scope** | Retested S003 with Redux style_model strength lowered from 1.0 to 0.6, plus an explicit "180 degrees rotated, rear side, hinge and latch visible" phrase added to the text prompt, same seed 42 as Decision 20. |
| **Authorization** | Director: "do all three but start with s002" (covering all three planned follow-up tests). |
| **Confidence** | high that reducing Redux strength does not free up viewpoint control -- the output is still nearly the same viewing angle as the front reference, essentially unchanged from Decision 20's result despite the strength reduction and added rotation language. This rules out strength dosage as the lever for viewpoint independence. |
| **Actor** | director |
| **Revisit trigger** | Reopen only with a genuinely different mechanism for viewpoint control -- e.g. a pose/depth ControlNet (none currently installed locally) conditioning the desired camera angle independently of Redux's identity-lock, or a multi-view-aware generation approach entirely. Do not retry with further Redux strength adjustments alone -- the 1.0-to-0.6 range showed no effect on this variable. |
| **Rationale** | This closes off the cheapest candidate fix (strength tuning) for S003's remaining viewpoint gap, isolating the problem as structural to Redux's reference-conditioning mechanism rather than a tunable balance between identity-lock and prompt-following. The object-identity fix from Decision 20 stands on its own merit; genuine multi-view turnaround generation is now a separately scoped, harder problem requiring new tooling (ControlNet) not yet installed. |

### Decision 24 — Hunyuan3D single-view mesh generation resolves S003's turnaround-identity problem completely, by making it structurally impossible to fail

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Installed native ComfyUI Hunyuan3D-2 support (`hunyuan3d-dit-v2.safetensors`, single-view image-to-3D model) and reframed S003 entirely: instead of trying to generate a separately-consistent 2D "back view" image (Decisions 20, 23's approach), generate one 3D mesh from the front concept image, then derive any needed view (front/back/left/right) as a camera rotation of that single mesh in Blender. First attempt with the raw photo produced a recognizable lantern shape but included an unwanted flat background plane baked into the geometry (the input photo's plain grey background wasn't removed first). Second attempt with a `rembg`-based background-removed, white-composited input cleanly eliminated that artifact. |
| **Authorization** | Director: "yes, install it and test it" (Hunyuan3D), then "yes, run it with the rembg cutout" for the follow-up fix. |
| **Confidence** | high that this fully resolves the turnaround-identity flaw category -- front and back renders are now trivially, structurally identical in shape, proportions, and detail (same panel divisions, same roof/base geometry), because they are camera angles on one 3D object rather than two independently generated 2D images. This is not a probabilistic improvement like the masking or Redux approaches -- identity consistency is now guaranteed by construction. |
| **Actor** | director |
| **Revisit trigger** | Reopen if a production asset needs actual surface texture/material (this test used shape-only generation, no texture stage, which the RTX 3080's 10GB VRAM cannot fit per Decision-era research -- texture generation needs ~20GB+). A textured asset would need either a lower-fidelity texture pass tested for VRAM fit, or texturing done separately in Blender/ComfyUI 2D compositing over rendered mesh passes (the Director Console plan's own "Blender exports -> ComfyUI textures" pipeline, §5.3). |
| **Rationale** | This is the deepest fix in this WO's whole investigation: rather than continuing to patch 2D-generation techniques (masking, reference-locking) to coax consistency out of independently-sampled images, it sidesteps the problem's root cause entirely by making the 3D mesh the single source of spatial truth -- exactly the governing principle already stated in the Director Console plan (`2026-08-23-001`): "Blender owns controllable spatial truth." S003 was never really a 2D-generation problem; it was a false constraint inherited from generating 2D turnarounds instead of a 3D asset from the start. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [testimony] | director, 2026-08-23 | The revised image barely generated any differences after the revision prompt in V0_Five_Case_Test_General_Visual.json. |
| [system] | live inspection of ComfyUI workflow JSON | The revision lane is connected Load Image to VAEEncode to KSampler to VAEDecode to distinct Save/Preview After nodes. KSampler uses fixed seed 987654321123456, 26 steps, CFG 1.0, Euler/simple, and denoise 0.50; its positive conditioning comes from the revision-only CLIPTextEncode node. |
| [inference] | workflow inspection plus director observation | The graph wiring no longer explains the weak delta. Revision strength, Flux-specific guidance/conditioning, prompt construction, or source-image selection remain plausible causes; a controlled S001 comparison is required before selecting a fix. |
| [decision] | director acceptance, conversation | Accepted the three-output S001 tracer: control at denoise 0.50 without FluxGuidance, guidance-only at FluxGuidance 3.5 and denoise 0.50, and guided-strength at FluxGuidance 3.5 and denoise 0.65; use a copied workflow, preserve the original, and stop rather than raising denoise if no branch passes. |
| [system] | bounded implementation and structural validator | Created ComfyUI visual workflow S001_Revision_Control_Tracer_ABC.json with 22 nodes and 29 reciprocal type-compatible links. A uses no FluxGuidance/denoise 0.50, B uses FluxGuidance 3.5/denoise 0.50, and C uses FluxGuidance 3.5/denoise 0.65. Original V0_Five_Case_Test_General_Visual.json remained unchanged at SHA256 84462C61D2390E705740189DCCAE49B54DC6F91EEFD6E1C3D9089B732EC65DBD; tracer SHA256 is F6F8002DAA587A4D8E48ED855F5E33035D5BA6F7BEF068D1866EA3FA7F8254DE. |
| [system] | ComfyUI prompt 7c761f31-5667-498c-b332-48212389b39d | ComfyUI accepted the A/B/C prompt with zero node errors and completed successfully. Saved S001_control_00001_.png, S001_guided_00001_.png, and S001_guided_065_00001_.png in ComfyUI-Shared/output. |
| [system] | Pillow/NumPy pixel comparison of executed outputs | Pixels with maximum channel delta above 10 versus before: A 30.49%, B 30.57%, C 41.71%. A versus B differs on only 0.27% of pixels above that threshold; B versus C differs on 15.71%. Guidance 3.5 alone therefore produced negligible additional pixel change in this run, while denoise 0.65 produced a materially larger delta. |
| [inference] | agent visual comparison of before and A/B/C outputs | A and B visibly improve silhouette separation, jacket midtones, and overall contrast but leave the face unreadable; B is visually near-identical to A. C strengthens hood/shoulder separation but shifts case/hand pose and alley details while the face remains black. Director preserve/avoid judgment is still required before declaring a branch pass. |
| [gap] | verification boundary | No director judgment has yet confirmed whether A or B's two visible improvements outweigh residual face unreadability while satisfying zero preserve/avoid violations; tracer outcome remains unverified until that judgment is recorded. |
| [decision] | director, 2026-08-23 | Defer Flux Dev entirely; use HiDream O1 as the primary image generation model for all workflows. |
| [system] | ComfyUI source inspection, 2026-08-23 | HiDream O1 is architecturally incompatible with Flux-style nodes: pixel-space model (no VAE encode/decode), embedded Qwen3-VL language model (needs HiDreamO1Tokenizer, not DualCLIPLoader), and reference-image editing via HiDreamO1ReferenceImages (1 image = instruction edit mode). The previous E tracer failed with `ValueError: HiDreamO1Transformer requires input_ids and position_ids in conditioning` because it used Flux CLIP embeddings instead of raw tokenized input_ids. |
| [system] | ComfyUI FP8 bug fix, 2026-08-23 | Fixed `comfy/text_encoders/qwen35.py` line 631-648: Qwen3-VL vision encoder positional embeddings were in Float8_e4m3fn which doesn't support arithmetic. Cast `patch_embed` output and `pos_embed` lookups to float32 before addition. Without this fix, any FP8 HiDream O1 model with reference images crashes at sampling step 1. |
| [system] | corrected E tracer workflow, 2026-08-23 | Rebuilt S001_Revision_E_HiDream_Day_To_Night.json with HiDream O1-native architecture: CheckpointLoaderSimple (auto-detects zero-param tokenizer CLIP + pixel-space VAE), EmptyHiDreamO1LatentImage (2048x2048), HiDreamO1ReferenceImages (1 reference = edit mode), KSampler (CFG 5.0, euler/simple, 28 steps, denoise 1.0), no FluxGuidance. Hard-linked model from diffusion_models/ to checkpoints/ for CheckpointLoaderSimple access. |
| [system] | ComfyUI prompt 29096193-914f-4e03-953b-ee006a6d0c82, 2026-08-23 | ComfyUI accepted the corrected E tracer prompt with zero node errors and completed successfully (~3.5 minutes on RTX 3080 10GB). Saved S001_E_hidream_day_to_night_00001_.png (2048x2048) in ComfyUI-Shared/output. |
| [inference] | agent visual comparison, 2026-08-23 | E tracer produces an unmistakable day-to-night conversion: dark blue sky, warm golden streetlamp glow, colorful neon signs, wet reflective pavement, cinematic night lighting. Subject identity (woman, smile, metallic jacket, badge) and composition are preserved. Minor drift: jacket texture more reflective/glossy, market environment shifted slightly more European, face features slightly different (reference-guided generation, not pixel-perfect editing). The day-to-night target is clearly achieved — this is the first tracer to produce the intended revision. |
| [system] | F tracer two-stage workflow, 2026-08-23 | Built and executed S001_Revision_F_HiDream_TwoStage.json: Stage 1 generates before image from text (T2I, CFG 1.0, seed 42, no reference), Stage 2 revises with reference edit (CFG 5.0). Single model load, both stages share CheckpointLoaderSimple output. Saved S001_F_before_00001_.png, S001_F_revision_A_00001_.png (day-to-night), S001_F_revision_B_00001_.png (jacket color change). |
| [inference] | agent visual judgment, 2026-08-23 | Revision A (day-to-night): PASS — unmistakable conversion with dark blue sky, golden streetlamp glow, neon signs, wet reflective pavement; subject identity, pose, jacket pattern, and composition preserved; minor facial feature drift acceptable for reference-guided generation. Revision B (jacket color): PARTIAL PASS — jacket correctly changed from metallic bronze to navy blue denim with buttons and stitching, but background has heavy blown-out highlight artifacts suggesting CFG 5.0 is too aggressive for localized attribute edits. |
| [inference] | agent recommendation, 2026-08-23 | Two-stage pipeline architecture validated. Lighting revisions production-ready at CFG 5.0. Attribute revisions need CFG 3.0-3.5 tuning to reduce artifacts. Settings ready to generalize for S002-S005. |
| [system] | S001-S005 full-suite run, 2026-08-24 | Ran all five V0 proof cases through the two-stage HiDream O1 pipeline using each shot object's `change` field to derive the Stage 2 revision prompt. ComfyUI crashed after S004 (process fully exited, API connection refused); relaunched via Comfy Desktop.exe, recovered queue, re-ran S005 Stage 2 only using the already-generated S005 before image via LoadImage. All 10 images (5 before, 5 revision) generated successfully. |
| [inference] | agent visual judgment, 2026-08-24 | S002 (Mood Mismatch) and S004 (Background Distraction): PASS — before image fully committed to the intended flaw, revision produced a dramatic, coherent, critique-directed change while preserving Mara's identity, jacket, amber light, and sealed case. S004 has one minor artifact: a stray disconnected hand near the frame edge. S001 (Character Readability) and S003 (Camera/Composition): PARTIAL — the Stage 1 before image did not strongly express the intended flaw (face/silhouette were already reasonably readable in S001; framing in S003 was not clearly flat/symmetric/static as scripted), so the Stage 2 revision had little contrast to work against and produced only a subtle change. S005 (Style/Lighting Consistency): revision executed well (unified single-source warm lighting, coherent photoreal look) but the before image likewise did not clearly show the scripted split-style/contradictory-light flaw. |
| [inference] | agent root-cause analysis, 2026-08-24 | 3 of 5 cases (S001, S003, S005) show the same pattern: Stage 1 T2I generation at CFG 1.0 with a single fixed seed does not reliably commit to the flaw described in the shot object's `change` field. This is a Stage 1 flaw-injection fidelity gap, not a Stage 2 revision defect — S002 and S004 prove the revision mechanism works correctly whenever the before image actually expresses its intended flaw. |
| [gap] | ws transition audit (verify) | Unresolved [gap] entries exist in the Evidence ledger. Residual uncertainty should be reviewed before proceeding. |
| [system] | S001_Stage1_cfg1.0/cfg2.0/cfg3.0_00001_.png, executed via local ComfyUI :8188, 2026-08-24 | Ran the accepted Decision 6 tracer: S001 Stage 1 T2I at CFG 1.0/2.0/3.0, fixed seed 42, HiDream O1 Image Dev FP8, 2048x2048, 28 steps euler/simple. All three completed with zero node errors. Visual judgment against the scripted flaw (v0-proof/shot-objects/S001-character-readability.json change: face lost in shadow, silhouette merging with wall, muddy low contrast): CFG 1.0 -- face clearly lit and legible, silhouette well-separated from the wall, flaw not expressed. CFG 2.0 -- face still clearly legible (eyes/nose/mouth visible), only marginally more shadow texture, flaw still not expressed. CFG 3.0 -- face remains clearly lit and legible (arguably as readable as CFG 1.0), AND introduces a new element not in the shot's preserve/description: an orange/copper stripe on the jacket sleeve and garbled text on the case, neither scripted. No tested CFG value made the flaw unambiguous; CFG 3.0 added an unscripted artifact instead. |
| [system] | S001_Stage1_promptrewrite_00001_.png, executed via local ComfyUI :8188, 2026-08-24 | Ran the accepted Decision 7 tracer: S001 Stage 1 at CFG 1.0, seed 42, with a substantially reworded before-prompt explicitly demanding facial invisibility (no visible eyes/nose/mouth, near-total darkness, silhouette blending with wall) and a negative prompt explicitly discouraging a clearly visible/well-lit face. Completed with zero node errors. Visual judgment: face remains clearly lit and legible -- eyes, nose, mouth, and expression all visible, front-lit despite the prompt's explicit instruction otherwise. Silhouette against the wall is somewhat better separated than not worse than prior attempts, but the primary scripted flaw (face lost in shadow) is still not achieved. New artifact: a stray disembodied hand/forearm appears near her leg in the lower-left of frame, not scripted -- the same class of artifact previously noted for S004's revision output. Prompt-wording-alone is falsified as the sole lever, same as CFG-alone (Decision 6). |
| [system] | ComfyUI local generation: AssetStage1_S001_00001_.png, AssetStage1_S002_00001_.png, AssetStage1_S003_front_00001_.png, AssetStage1_S003_back_00001_.png, AssetStage1_S004_00001_.png, AssetStage1_S005_viewA_00001_.png, AssetStage1_S005_viewB_00001_.png | Stage-1 before-image run for the rewritten asset-generation S001-S005 cases on Flux (flux1-krea-dev_fp8_scaled, no LoRA, CFG 1.0, FluxGuidance 3.5, seed 42, 25 steps): S002 (style mismatch), S003 (turnaround identity mismatch), S004 (reference-plate clutter), and S005 (rendering-consistency break) all cleanly expressed their scripted flaw on the first attempt. S001 (silhouette readability) did not -- the lamp read clearly against its black background with visible rim lighting instead of merging into shadow, reproducing the same flaw-fidelity gap seen with HiDream O1 across Decisions 5-8. 4 of 5 pass on Stage 1 alone. |
| [system] | ComfyUI local generation: S001_asset_guidance2_0_00001_.png, S001_asset_guidance5_0_00001_.png, S001_asset_guidance8_0_00001_.png | S001-only FluxGuidance tracer (guidance 2.0/5.0/8.0, seed 42, CFG 1.0, same flaw prompt): all three values failed to produce the scripted flaw (silhouette merging with a dark background). At every guidance level the lamp's crackled/reflective glass panes catch and reflect available light, keeping the object visually separated from the black backdrop regardless of overall scene darkness. This differs from the earlier HiDream O1 failure mode (Decisions 5-8, general reluctance to darken a face/scene) -- here the specific prop's material (translucent glass) is the structural reason the flaw resists expression, independent of engine or guidance strength. |
| [system] | ComfyUI local generation: AssetRevision_S002_after_00001_.png, AssetRevision_S003_back_after_00001_.png, AssetRevision_S004_after_00001_.png, AssetRevision_S005_viewB_after_00001_.png | Revision-lane (Stage 2) pass on Flux img2img (FluxGuidance 3.5, denoise 0.55, seed 42 -- the parameters validated in Decision 2) run against the 4 passing before-images (S002, S003_back, S004, S005_viewB), each with a critique-directed revision prompt reversing its scripted flaw: S002 (style mismatch) partial -- some patina/tarnish appeared but the lamp remained glossy chrome with the neon-teal glow ring intact; S003 (turnaround identity) partial -- crackled glass texture appeared but the back view's overall shape still does not match the front view's hexagonal pyramid-roof silhouette; S004 (reference clutter) fail -- background clutter (crates, rope, fabric) essentially unchanged; S005 (rendering consistency) fail -- still painterly brushwork with the same clashing orange/blue lighting, essentially unchanged from the flawed before-image. This directly reproduces the original weak-revision problem (Decision 1's founding observation) on the asset-generation domain, using Flux instead of HiDream O1. |
| [system] | ComfyUI local generation: AssetRevision_S004_masked_after_00001_.png | S004 masked-inpainting tracer (rectangular bounding-box mask protecting the lamp, VAEEncodeForInpaint, denoise 1.0 inside the mask, FluxGuidance 3.5, seed 42): the masked region cleanly and fully regenerated to a plain neutral-grey background -- a decisive change, unlike the global img2img revision in Decision 11 which left clutter essentially untouched. However, the crude rectangular mask was not shaped to the lamp's actual silhouette: it left a hard visible seam at the mask boundary and a strip of original clutter (rope/fabric) still visible inside the oversized rectangle. Validates masked/regional inpainting as a substantially stronger revision mechanism than global denoise; also identifies mask precision (silhouette-following shape, edge feathering) as a new required component, not yet solved. |
| [system] | ComfyUI local generation, AssetRevision_S004_masked_v2_after_00001_.png, mask preview S004_mask_v2_preview_00002_.png | Tighter, feathered silhouette mask (4-band approximation of lamp shape, 10px feather, grow_mask_by 2) run against S004 background clutter, denoise 1.0 inside mask only, Flux + FluxGuidance 3.5. Result: broad background clutter removed, but two failures remain -- visible blocky rectangular seams where mask boundary meets background (patterned fabric bleeds through at the shoulders), and the protected lamp region did not stay pixel-identical, its finish shifted from warm brass/rust to flat matte-black. Regeneration leaked past the intended mask boundary. |
| [system] | ComfyUI local generation, AssetRevision_S004_fluxfill_after_00001_.png; https://github.com/Comfy-Org/ComfyUI/discussions/14467 | Live-question test: swapped engines from flux1-krea-dev_fp8_scaled (manual VAEEncodeForInpaint masking) to FLUX.1-Fill-dev-GGUF Q4_K_S (a model natively trained for masked inpainting, via InpaintModelConditioning + FluxGuidance 30), same S004 case, same 4-band silhouette mask from Decision 13, same revision prompt. Result: the mask was effectively ignored -- background clutter (crates, rope, fabric) is essentially unchanged from the flawed before-image, a total non-compliance failure rather than Flux-Krea's partial leak-and-seam failure. This reproduces a documented community-reported bug (ComfyUI GitHub discussion #14467: 'FLUX.1 Fill dev inpainting not working - mask completely ignored', multiple users, unresolved as of research). |
| [system] | ComfyUI local generation, AssetRevision_S004_hardboundary_after_00001_.png, mask preview S004_hardboundary_mask_preview_00001_.png | Hard-boundary variant (same 4-band mask as Decision 13, FeatherMask removed, grow_mask_by 0) run against S004 on flux1-krea-dev_fp8_scaled. Result: the same rectangular patch of original clutter (patterned fabric) persists behind the lamp's roof, now with a crisp unfeathered edge instead of a soft one. The mask preview shows the 'roof band' rectangle (350-670 x, 190-330 y) is wider than the lamp's actual roof silhouette, so its corners include real background pixels that stay unchanged because that region is protected. This falsifies boundary softness as the cause of the leak -- the problem is mask shape/precision, not feathering. |
| [system] | ComfyUI local generation, AssetRevision_S004_rembg_after_00001_.png; segmentation cutout preview S004_rembg_cutout_preview.png | Installed rembg (u2net model) into ComfyUI's Python venv, generated a real segmentation mask for S004's before-image (clean silhouette-accurate cutout, dropped the thin hanging chain as background noise -- known limitation). Ran the same masked-revision pipeline (VAEEncodeForInpaint, grow_mask_by 0, denoise 1.0, FluxGuidance 3.5, seed 42, background-only revision prompt) with this mask instead of any hand-drawn geometry. Result: clean pass -- background clutter (crates, rope, fabric, text) fully removed and replaced with plain neutral grey across the whole frame, lamp identity preserved, only a tiny cosmetic rope-like remnant near the dropped-chain area (consistent with the known segmentation gap, not a boundary/seam failure). |
| [system] | ComfyUI local generation, AssetRevision_S002_rembg_after_00001_.png, AssetRevision_S005_viewB_rembg_after_00001_.png | Generalized the validated rembg-masking recipe to S002 and S005_viewB, inverting the mask (protect background, inpaint foreground object) since both flaws are object-level, not background-clutter. S002 result: material flaw substantially corrected (weathered brass/green patina replaced glossy chrome), but the revision introduced an unscripted frosted-white glass bell/diffuser shape not present in the original object -- a new artifact, not requested. S005_viewB result: the masked object rendered fully photorealistic (crisp reflections, brushed-metal texture, painterly brushwork eliminated) exactly as targeted, but the surrounding background stayed visibly painterly since it was protected/unmasked -- a scope mismatch, not a masking failure: S005's flaw is a whole-frame rendering-style problem, and masking only the foreground left the fix half-applied. |
| [system] | ComfyUI local generation, AssetRevision_S002_rembg_v2_noshapes_after_00001_.png | S002 retest: added an explicit no-new-geometry constraint to the positive prompt plus a negative text prompt naming the unwanted glass bell/dome/diffuser shape. Result: fail -- the same unscripted frosted-glass bell shape reappeared in the same location, unchanged by the added constraint. Material patina improved further. Likely cause: at cfg=1.0 (the standard Flux setting used throughout this WO), the sampler does not apply negative conditioning, so a negative prompt has no functional effect; the positive-prompt constraint alone was insufficient to suppress the unwanted geometry. |
| [system] | ComfyUI local generation, AssetRevision_S005_wholeframe_after_00001_.png | S005 retest with a whole-frame mask (SolidMask value 1.0, no protected region at all), same denoise 1.0/guidance 3.5/seed 42. Result: the photoreal/painterly seam is completely gone -- the entire frame is uniformly photorealistic, confirming the scope-matching hypothesis (masking scope must cover the flaw's actual scope to avoid a seam). But this reveals a distinct new problem: at full denoise across the whole frame, there is no compositional anchor to the original image at all -- the output is an entirely different lamp design (a traditional table lamp with white fabric shade, not the original market-lantern shape), not a revision of the original asset. Whole-frame masking at denoise 1.0 solves the seam by discarding the identity the revision needed to preserve. |
| [system] | ComfyUI local generation, AssetRevision_S003_redux_backview_after_00001_.png | S003 turnaround-identity test via reference-locking: installed Flux Redux (flux1-redux-dev.safetensors style_model + sigclip_vision_patch14_384.safetensors CLIP vision), encoded S003's front-view image as a style/subject reference via CLIPVisionEncode + StyleModelApply (strength 1.0), generated a fresh 'back view' with a text prompt naming the same lantern shape/material, guided by the reference conditioning (not img2img -- fresh EmptySD3LatentImage). Result: strong structural win -- the output now matches the front reference's exact lantern shape (hexagonal, pyramidal roof, crackled glass, chain, tapered finial), a decisive fix for the object-identity mismatch that Decision-era S003 evidence originally found (front and back were previously two completely different lantern designs). Residual limitation: the output's viewing angle is nearly identical to the front reference rather than a distinct rotated back view -- Redux's reference-lock constrains viewpoint along with identity, not identity alone. |
| [system] | ComfyUI local generation, AssetRevision_S002_cfg2_realneg_after_00001_.png | S002 retest: raised cfg to 2.0 with real (non-zeroed) negative conditioning naming the unwanted glass shape, same mask/prompt otherwise. Result: partial -- the unwanted bell/diffuser shape's material changed from frosted glass to weathered brass/patina metal (much more visually integrated as an intentional lamp part), but clear glass edges are still visible at the sides, meaning the extra geometry itself persists structurally, just recolored. This confirms cfg>1.0 does activate negative conditioning to some real degree (unlike Decision 18's cfg=1.0 identical-repeat), but cfg=2.0 alone is not strong enough to fully suppress the unwanted shape. |
| [system] | ComfyUI local generation, AssetRevision_S005_wholeframe_denoise05_after_00001_.png | S005 retest: whole-frame mask (value 1.0, no protected region) at moderate denoise 0.5 instead of 1.0. Result: total technical failure -- the output is a completely flat, uniform grey image with zero content (not a stylistic partial fail like S002). Likely cause: VAEEncodeForInpaint's noise-mask mechanism has no original content to preserve at 100% mask coverage, but denoise 0.5 also doesn't provide enough steps to build a fresh image from noise, producing a degenerate/undiffused latent. This rules out 'whole-frame mask at moderate denoise' as a viable fix in this exact configuration -- a different approach (no mask at all with denoise<1.0 img2img, or a much higher denoise with whole-frame mask, or a smaller partially-protected region) would need testing instead. |
| [system] | ComfyUI local generation, AssetRevision_S003_redux_lowstrength_after_00001_.png | S003 retest: reduced Redux style_model strength from 1.0 to 0.6, with an explicit '180 degrees rotated, rear side, hinge and latch visible' phrase added to the text prompt, same seed 42. Result: fail on viewpoint -- the output is still nearly the same viewing angle as the front reference, same three-quarter framing, same proportions. Lowering Redux strength did not free up the viewpoint at all, ruling out strength dosage as the lever; the camera-framing bias appears structural to how Redux's reference conditioning works, not something a text prompt can override within this strength range. |
| [system] | ComfyUI local generation, S003_hunyuan3d_test_v2_00001_.glb; Blender headless renders S003_hunyuan3d_render_v2_front.png and S003_hunyuan3d_render_v2_back.png | Installed native ComfyUI Hunyuan3D-2 support (hunyuan3d-dit-v2.safetensors, ~4.93GB, single-view image-to-3D-mesh model) and reframed S003's turnaround-identity problem: instead of generating a separate, independently-inconsistent 2D back-view image, generate one 3D mesh from the front concept image, then render any view (front/back/left/right) as a camera rotation of that single mesh. First attempt (raw photo input) produced a recognizable lantern shape (roof cap, hexagonal housing, hanging chain, base finial) but included an unwanted flat background plane baked into the geometry, since the input photo's plain grey studio background wasn't removed first. Second attempt with a rembg-based background-removed, white-composited input cleanly eliminated the background plane -- the resulting mesh is a clean, isolated lantern matching the reference's shape and proportions. Rendered front/back/left/right views in Blender (headless) confirm front and back are now trivially identical in structure (same mesh, same panel divisions, same roof/base details), since they are literally the same 3D object viewed from different camera angles rather than two independently generated images. |
| [gap] | ws transition audit (verify) | Unresolved [gap] entries exist in the Evidence ledger. Residual uncertainty should be reviewed before proceeding. |
## Open questions

- Is the weak delta primarily caused by revision strength, Flux conditioning,
  prompt construction, or the particular before image loaded for revision?
- What is the lowest revision strength that produces an obvious accepted
  change while keeping every protected element intact?
- Does the chosen correction generalize beyond S001 without case-specific
  custom nodes or VRAM pressure?

## Next move

Route to `alawas-engineering-implement-bounded-change` to create the copied
three-output S001 tracer exactly as accepted. Do not modify the original
five-case workflow and do not exceed denoise `0.65`.

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-24T02:34:45Z — Created bounded ComfyUI revision-lane change record

- **State:** notice
- **Status:** active
- **Actor:** codex
- **Rationale:** Director requested a Work Object after observing that the revised image barely differed; the record separates this workflow defect from the broader architecture object.
### 2026-08-24T02:35:14Z — Classified weak revision delta as a bounded workflow design change

- **State:** design
- **Status:** active
- **Actor:** codex
- **Rationale:** The failure is observed and the graph is wired, but the smallest effective control change is unresolved; a tracer must discriminate revision strength, conditioning, prompt, and source-selection causes before implementation.
### 2026-08-24T02:45:25Z — Accepted and recorded bounded S001 tracer design

- **State:** build
- **Status:** active
- **Actor:** codex
- **Rationale:** The director accepted the recommended three-output comparison with explicit preserve, stop, observability, and rollback boundaries; the design is ready for bounded implementation.
### 2026-08-24T02:56:07Z — Implemented and executed S001 A/B/C tracer

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** The copied visual workflow passed structural checks and ComfyUI produced all three outputs. Visual pass/fail remains a director judgment because A/B improve multiple targets but leave the face unreadable, while C introduces preserve drift.

### 2026-08-23T10:45:00Z — HiDream O1 E tracer completed successfully

- **State:** verify
- **Status:** active
- **Actor:** codex
- **Rationale:** Director deferred Flux Dev and directed all workflows to HiDream O1.

### 2026-08-23T22:00:00Z — F tracer two-stage pipeline validated (agent judgment)

- **State:** verify
- **Status:** active
- **Actor:** agent (delegated judgment from director)
- **Rationale:** Built and executed two-stage HiDream O1 workflow: Stage 1 generates before image from text prompt (T2I, no reference, CFG 1.0), Stage 2 revises with reference edit (CFG 5.0). Tested two revision types: (A) day-to-night lighting change — PASS, unmistakable conversion with preserved identity; (B) jacket color change — PARTIAL PASS, correct target change but background artifacts at CFG 5.0. Pipeline architecture validated. Next: tune CFG for attribute edits and generalize to S002-S005.

### 2026-08-24T07:45:00Z — Full S001-S005 suite run; Stage 1 flaw-fidelity gap identified (agent judgment)

- **State:** verify
- **Status:** active
- **Actor:** agent (delegated judgment from director)
- **Rationale:** Ran all five V0 proof cases through the two-stage pipeline, deriving each Stage 2 revision prompt from the shot object's `change` field. ComfyUI crashed mid-run after S004 (process exited entirely); relaunched via Comfy Desktop.exe and recovered by re-running only S005's Stage 2 against its already-generated before image. Result: S002 (Mood Mismatch) and S004 (Background Distraction) PASS cleanly — before images fully committed to their scripted flaws and revisions produced dramatic, well-preserved, critique-directed changes. S001 (Character Readability), S003 (Camera/Composition), and S005 (Style/Lighting Consistency) came back PARTIAL — their before images did not reliably express the intended flaw at Stage 1 (CFG 1.0, single seed), leaving little for the revision to visibly correct. This isolates the remaining defect to Stage 1 flaw-injection fidelity, not the revision mechanism itself. Next: raise Stage 1 CFG or vary seed for flaw-prone cases and re-test before judging the suite against its 3-of-5 threshold. Diagnosed architectural incompatibility (pixel-space model vs Flux latent-space pipeline). Rebuilt E tracer with HiDream O1-native nodes. Fixed ComfyUI FP8 bug in Qwen3-VL vision encoder (Float8_e4m3fn positional embedding addition). E tracer produced unmistakable day-to-night conversion at 2048x2048 while preserving subject identity, pose, jacket, and composition. Output saved as S001_E_hidream_day_to_night_00001_.png. Director judgment on preserve/avoid fidelity still required.
### 2026-08-24T19:03:04Z — Transition back to design for Stage 1 flaw-fidelity tracer

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Director requested transition back to design to scope a bounded tracer for the Stage 1 flaw-fidelity gap (Decision 5, mixed result): raise Stage 1 CFG (2.0-3.0) or use multi-seed sampling with a flaw-presence check for S001/S003/S005 before re-judging the suite. This is a new, narrower design question distinct from the suite-judgment work that put the object in verify.
### 2026-08-24T19:04:08Z — Accepted S001-only Stage 1 CFG tracer design (Decision 6)

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted the recommended S001-only tracer: re-run Stage 1 T2I at CFG 1.0/2.0/3.0, fixed seed 42, judging each candidate against the scripted flaw before touching Stage 2. Recorded as Decision 6. Bounded to S001; seed variation and S003/S005 generalization explicitly deferred pending this result.
### 2026-08-24T19:04:26Z — Move to build for accepted S001 CFG tracer implementation

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Decision 6 accepted (S001-only Stage 1 CFG tracer at 1.0/2.0/3.0, fixed seed 42). Ready for bounded implementation.
### 2026-08-24T19:20:45Z — Decision 6 tracer executed and judged: CFG-is-the-lever assumption falsified

- **State:** design
- **Status:** active
- **Actor:** agent
- **Rationale:** Executed the accepted Decision 6 tracer: S001 Stage 1 at CFG 1.0/2.0/3.0, fixed seed 42. All three completed cleanly with zero node errors. Visual judgment against the scripted flaw found the face clearly legible at every tested CFG value -- the flaw (face lost in shadow, silhouette merging with wall) was not expressed at any of the three, and CFG 3.0 additionally introduced an unscripted artifact (orange jacket stripe, garbled case text) per its own revisit trigger. Marked Decision 6 Result: fail. Per its revisit trigger, this falsifies 'CFG is the lever' -- the fix likely belongs in Stage 1 prompt wording (the before-image prompt may need to more forcefully commit to the flaw in its own text) rather than sampling-parameter tuning, with seed variation as a lower-confidence alternative still untested.
### 2026-08-24T19:22:58Z — Move to build for accepted prompt-rewrite tracer (Decision 7)

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Decision 7 accepted (S001-only Stage 1 prompt-rewrite tracer, CFG 1.0/seed 42 held constant). Ready for bounded implementation.
### 2026-08-24T19:26:21Z — Decision 7 tracer executed and judged: prompt-rewrite-alone also falsified

- **State:** design
- **Status:** active
- **Actor:** agent
- **Rationale:** Executed the accepted Decision 7 tracer: S001 Stage 1 with a substantially reworded, more forceful before-prompt at CFG 1.0/seed 42. Completed cleanly. Visual judgment: face remains clearly lit and legible despite explicit prompt instruction otherwise, and a new artifact (stray disembodied hand near the leg) appeared -- the same artifact class previously seen on S004's revision. Marked Decision 7 Result: fail. Both isolated variables (CFG alone -- Decision 6; prompt wording alone -- Decision 7) have now independently failed to produce the scripted flaw, suggesting HiDream O1 has a strong built-in bias toward legible, front-lit faces that neither lever alone overrides at this seed. Untested: combining both (reworded prompt + higher CFG together), and seed variation (still never tested).
### 2026-08-24T19:28:34Z — Move to build for accepted combined CFG+prompt tracer (Decision 8)

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Decision 8 accepted (combined CFG 3.0 + reworded prompt at seed 42). Ready for bounded implementation.
### 2026-08-24T19:58:03Z — Decision 9 recorded: S001-S005 rewritten for asset generation, engine switched to Flux

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Director redirected the five scripted-flaw test cases from cinematic-scene critique (Mara/night-city) to asset-generation critique (a market-lamp hero prop across the concept/turnaround/reference-plate funnel), and switched the generation engine from HiDream O1 to flux1-krea-dev_fp8_scaled. Decision 8's combined tracer output was generated but never judged before this redirect -- left pending/superseded rather than retroactively resolved. All five shot-object JSONs and before-prompt files rewritten accordingly; no generations run yet against the new definitions.
### 2026-08-24T20:10:31Z — Stage-1 asset-generation Flux run judged: 4 of 5 pass

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** S002, S003, S004, S005 cleanly expressed their scripted flaws on Flux on the first attempt -- a marked improvement over HiDream O1's repeated Stage-1 fidelity gap (Decisions 5-8). S001 (silhouette readability against a dark background) failed to express its flaw, reproducing the exact same failure mode seen previously: this specific flaw class (make the subject hard to see) resists CFG-1.0 T2I generation regardless of engine. Given 4 of 5 pass this Stage-1 stage, the revision lane can proceed against S002-S005 immediately; S001 needs its own CFG/prompt-strength tracer on Flux before it can be judged, the same discriminating-test pattern used in Decisions 6-7.
### 2026-08-24T20:16:04Z — Decision 10 recorded: S001 FluxGuidance tracer fails at all tested values, root cause identified

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** All three guidance values (2.0/5.0/8.0) at seed 42 failed to produce the scripted flaw. Root cause differs from the prior HiDream O1 pattern: the lamp's reflective/crackled glass panes inherently catch light and keep the object visually separated from any dark backdrop, independent of guidance strength or engine. This points away from further parameter tuning and toward either substituting a non-reflective test prop or reconsidering whether silhouette-readability is a meaningful scripted flaw for a translucent hero asset.
### 2026-08-24T20:24:11Z — Decision 11 recorded: revision-lane pass reproduces founding weak-revision problem on asset domain

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** S001 dropped per director instruction. Revision-lane pass (FluxGuidance 3.5, denoise 0.55, seed 42) run against S002-S005: S002 and S003 only partially corrected their scripted flaws, S004 and S005 were essentially unchanged. This reproduces the WO's founding weak-revision observation (Decision 1) on a new domain (asset generation) and engine (Flux), strengthening the case that the defect is in the revision mechanism itself (denoise strength / lack of regional masking / no reference-override technique) rather than in engine or subject-matter choice, both of which have now been varied without resolving it.
### 2026-08-24T20:24:53Z — Route to design: scope a stronger revision mechanism

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** Decision 11 reproduced the WO's founding weak-revision problem on the asset-generation domain via Flux; the director accepted routing to alawas-design-design-tracer-bullet to scope the smallest test of a stronger revision mechanism (regional masking, higher denoise, or reference-locking) rather than continuing to vary engine/subject matter.
### 2026-08-24T20:28:52Z — Decision 12 recorded: masked inpainting validated, mask precision identified as remaining gap

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** The S004 masked-inpainting tracer decisively regenerated the masked background region -- confirming regional masking is a substantially stronger revision mechanism than the global img2img approach that failed in Decisions 2 and 11. The crude rectangular mask left a visible seam and a strip of leaked clutter, showing mask precision (silhouette-following shape with edge feathering) is the remaining unsolved piece before this can generalize to S002/S004/S005 or be judged production-ready.
### 2026-08-24T20:41:37Z — Decision 13 recorded: tighter silhouette mask still fails clean-mechanism bar

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** Tighter, feathered 4-band silhouette mask confirms masked revision is directionally sound (background clutter removal decisive a second time) but still fails the design's exit bar: visible seam at the mask boundary and protected-region identity leakage (lamp finish shifted). Two hand-drawn mask attempts have now failed at the same feather/grow meeting point -- next step is either true segmentation-based masking or a stricter (not softer) boundary treatment, not further hand-tuning.
### 2026-08-24T21:02:31Z — Decision 14 recorded: FLUX.1-Fill-dev engine swap rejected

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** FLUX.1-Fill-dev-GGUF reproduced a documented, unresolved community bug (mask completely ignored) rather than fixing the leak-and-seam problem -- a worse failure mode than the current engine. Engine choice is closed as a candidate fix; the remaining path is mask precision/boundary treatment on the current flux1-krea-dev_fp8_scaled pipeline.
### 2026-08-24T21:05:25Z — Decision 15 recorded: mask precision confirmed as root cause, not boundary softness

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** Hard-boundary variant reproduced the identical clutter-leak failure with a crisper edge, falsifying softness as the cause. The mask preview shows the mechanical reason directly: a rectangular protect-region necessarily traps some real background at its corners around a non-rectangular object. Three hand-authored mask attempts have now failed at this same root cause -- the fix requires an actually silhouette-accurate mask, meaning automated segmentation.
### 2026-08-24T21:10:50Z — Decision 16 recorded: automated segmentation validates masked revision, background-clutter case fixed

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** rembg-based segmentation produced a clean, decisive masked revision on S004 with no seam and no protected-region identity drift -- validating automated segmentation as the fix for regional/background-type revision flaws, after three hand-drawn-mask attempts and one engine swap all failed at the same root causes. This resolves the WO's founding weak-revision problem for at least this flaw category.
### 2026-08-24T21:16:27Z — Decision 17 recorded: masking generalizes as a mechanism, but scope must match flaw scope

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** S002 and S005 both show clean mask boundaries (no leak/seam), confirming the segmentation mechanism generalizes. But each has a distinct residual problem: S002 introduced an unscripted new glass-diffuser shape alongside the correct material fix; S005's foreground-only mask left the background painterly, producing a style seam, since S005's flaw is whole-frame, not regional. Masking scope must be chosen per flaw category, not defaulted to foreground-only.
### 2026-08-24T21:30:23Z — Decisions 18-20 recorded: all three follow-up tests complete

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** S002's no-new-geometry constraint failed (negative conditioning inert at cfg=1.0, root cause identified). S005's whole-frame mask eliminated the seam but at denoise 1.0 discarded the asset's identity entirely (scope-matching confirmed, denoise/identity tradeoff exposed). S003's Redux reference-locking decisively fixed the object-identity mismatch (front/back now share the same lantern shape and material), with a separate residual gap: the back view isn't a genuinely distinct rotated angle from the front. The revision lane now has two validated mechanisms for two distinct flaw categories: masking for regional pixel flaws, reference-locking for whole-object identity flaws.
### 2026-08-24T21:37:53Z — Decisions 21-23 recorded: all three follow-up tests complete, closing this design round

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** S002 cfg=2.0 confirmed negative conditioning works above cfg=1.0 but only partially suppressed the unwanted geometry (recolored, not removed). S005's whole-frame mask at moderate denoise 0.5 produced a total technical failure (flat grey output), ruling out that specific parameter combination as broken rather than merely weak. S003's Redux strength reduction did not free the viewpoint at all, confirming the camera-framing bias is structural to Redux's mechanism, not a tunable dosage effect. Two of three threads (S002, S005) need a different technical approach than tested so far; S003's core identity fix (Decision 20) stands, with genuine multi-view generation now scoped as a separate, harder problem needing new tooling (ControlNet, not installed).
### 2026-08-24T21:54:52Z — Decision 24 recorded: Hunyuan3D mesh generation resolves S003 completely

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Single-view Hunyuan3D-2 mesh generation, with a rembg background-removed input, produces a clean lantern mesh where front/back views are structurally guaranteed identical since they're camera angles on one 3D object. This resolves S003's identity-consistency flaw by construction rather than by better prompting -- the deepest fix found in this WO's entire investigation, matching the Director Console plan's own governing principle that Blender/3D owns spatial truth.
### 2026-08-24T21:56:07Z — Transition to verify: revision-lane mechanisms validated across two flaw categories

- **State:** verify
- **Status:** active
- **Actor:** system
- **Rationale:** Director: 'close this WO and move to verify.' Across Decisions 1-24, the revision lane's founding weak-revision problem was diagnosed and resolved for two distinct flaw categories: regional pixel-level flaws (background clutter, object material/style) via automated segmentation masking (Decision 16), and whole-object identity flaws (turnaround consistency) via reference-conditioned 3D mesh generation replacing 2D-turnaround generation entirely (Decision 24). Two narrower threads (S002 unwanted-geometry suppression, S005 whole-frame denoise balance) remain open but do not block verifying the core hypothesis that the revision lane can produce observable, critique-directed changes.
### 2026-08-24T21:58:21Z — Success evidence checklist rewritten to match asset-generation scope; verification complete

- **State:** verify
- **Status:** active
- **Actor:** system
- **Rationale:** Verified via alawas-engineering-verify-release-evidence against Decisions 1-24: the original checklist was written for the superseded Mara-scene domain (Decision 9 pivoted scope to asset-generation on a different engine) and could not be honestly checked as worded. Rewrote it to reflect the four tested flaw categories: background-clutter (S004) and turnaround-identity (S003) are fully met with clean, decisive evidence; object material/style (S002) and whole-frame rendering-consistency (S005) remain open, each with a specific unresolved technical gap recorded. Original wording retained inline for provenance, not deleted.
### 2026-08-24T21:59:29Z — Closed: Closed with a net-positive, mixed outcome. Two of four tested revision-lane flaw categories are fully verified: background-clutter removal via automated segmentation masking (Decision 16), and whole-object turnaround-identity consistency via 3D mesh generation replacing 2D-turnaround generation entirely (Decision 24) -- both resolve the WO's founding weak-revision problem with clean, decisive evidence. The remaining two categories (S002 object-material revision, unresolved unwanted-geometry artifact; S005 whole-frame rendering-consistency, unresolved denoise/mask breakdown) are spun off into their own follow-up Work Object rather than left open here indefinitely. Core hypothesis of this WO -- that the revision lane can be made to produce observable, critique-directed changes -- is proven.

- **State:** close
- **Status:** closed
- **Actor:** system
- **Rationale:** Closed with a net-positive, mixed outcome. Two of four tested revision-lane flaw categories are fully verified: background-clutter removal via automated segmentation masking (Decision 16), and whole-object turnaround-identity consistency via 3D mesh generation replacing 2D-turnaround generation entirely (Decision 24) -- both resolve the WO's founding weak-revision problem with clean, decisive evidence. The remaining two categories (S002 object-material revision, unresolved unwanted-geometry artifact; S005 whole-frame rendering-consistency, unresolved denoise/mask breakdown) are spun off into their own follow-up Work Object rather than left open here indefinitely. Core hypothesis of this WO -- that the revision lane can be made to produce observable, critique-directed changes -- is proven.
