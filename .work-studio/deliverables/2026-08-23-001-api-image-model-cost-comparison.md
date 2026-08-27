# API Image Models for the Director Console — Cost/Fit Comparison

> **Deliverable type:** report
> **Work Object:** `2026-08-23-001`
> **Date:** 2026-08-24
> **Author:** Andre (andrelawas35@gmail.com)
> **Question:** Given the tests run this session (local ComfyUI/RunPod friction;
> hosted-API precedent found for 3D models — `fal-ai/trellis-2`,
> `fal-ai/hunyuan3d-v21`, `ndreca/hunyuan3d-2.1`), which API-hosted 2D
> image-generation models would fit the Director Console and be cost
> effective?
> **Grounding:** `2026-08-23-001` Decision 2/3 and the implementation plan
> (`.work-studio/deliverables/2026-08-23-001-director-console-implementation-plan.md`).

This is a report: it answers a new falsifiable question with fresh evidence.
It does not synthesize an already-accepted Decision, and it authors no new
decision — the conflict it surfaces in §3 is flagged for the director, not
resolved here.

---

## 1. What already exists (grounding)

- The Director Console's Visual Production Department already runs a **local**
  image model: Flux Dev FP8 (`flux1-krea-dev_fp8_scaled.safetensors`) in
  ComfyUI on the director's RTX 3080 (10 GB VRAM). `[system]`, implementation
  plan §1.7.
- Decision 2 (`2026-08-23-001`) records an active constraint: **"No
  hosted/cloud generation dependency."** The API LLM is explicitly scoped to
  reasoning/cognition only — "cloud OK for cognition, not generation."
  `[decision]`, plan §9.
- The Audio department already has an accepted **tiered** pattern — local TTS
  (free) → cheap API TTS → premium API TTS — but this tiering is scoped to
  audio, not image generation. `[system]`, plan §5.2.
- This session separately found that hosted APIs exist and are cheap for the
  3D-generation side of the pipeline (`fal-ai/trellis-2` ~$0.02/gen,
  `fal-ai/hunyuan3d-v21` ~$0.16-0.48/gen, `ndreca/hunyuan3d-2.1` on Replicate
  ~$0.27/run) — found while diagnosing real friction renting and provisioning
  RunPod GPUs for a different Work Object (`2026-08-24-001`). `[system]`,
  this session.

## 2. API image-generation models found, and their cost

| Model | Provider | Price per image | Notes |
|---|---|---|---|
| FLUX.1 [schnell] | fal.ai | ~$0.003–0.025 | Same model family already running locally (Flux). Fastest, lower quality tier. |
| FLUX.1 [dev] | fal.ai / Replicate | ~$0.03–0.05 | Same family as the local Flux Dev FP8 already in use — most stylistically consistent API option if ever needed. |
| FLUX.2 [pro] | fal.ai | ~$0.03/MP | Higher-end Flux tier. |
| Ideogram 4.0 | Ideogram | $0.03 (Turbo) – $0.10 (Quality) | Strong at text-in-image; different model family from Flux. |
| Stable Diffusion 3.5 | Stability AI | ~$0.04–0.08 | Also self-hostable at no per-image cost if VRAM allows — SD's own claimed advantage. |

`[system]`, WebSearch this session (teamday.ai, pricepertoken.com, costbench.com,
Replicate blog, apiframe.ai, digitalapplied.com — pricing snapshots as
reported by these sources, not independently verified against each
provider's own pricing page).

**Cost-effectiveness read, in isolation:** FLUX.1 [dev] via fal.ai or
Replicate (~$0.03–0.05/image) is the standout choice *if* an API image model
is wanted at all — it is the same model family as what already runs locally,
meaning style/output would be the most consistent with existing local
generations, and its price is near the bottom of the surveyed range.
FLUX.1 [schnell] is cheaper still (~$0.003–0.025/image) but is explicitly
positioned as a faster/lower-quality distillation, better suited to
throwaway exploration than hero-quality frames. `[inference]`.

## 3. The real finding: this conflicts with an already-recorded Decision

This is the load-bearing part of the report, not a footnote.

`2026-08-23-001` Decision 2 already decided, with explicit director
authorization, that image/3D **generation** stays local (Blender + ComfyUI),
narrowing only "dependency-free" to "local-install accepted" — explicitly
**not** loosening to a hosted/network dependency. The Decision's own
rationale: file-first truth and model-agnosticism survive; only
dependency-freeness gives way, and only to a *local-install* requirement.
`[decision]`, plan §9, WO Decision 2.

Adopting an API image model for the Director Console's actual generation
pipeline — as opposed to using one for an unrelated, separate exploration
(like today's 3D-model API research) — would reverse that Decision, not
extend it. That is a genuine authority boundary this report does not cross:
per this skill's own rule, a request that would need a new decision is
routed to `alawas-thinking-pressure-test-decision`, not authored in here. `[inference]`.

**Where an API image model would fit without touching Decision 2 at all:**
anything outside the canon-affecting creative pipeline — for example,
console-UI scratch thumbnails, non-canonical placeholder icons, or
quick-look previews that never become a Scene/Shot artifact. This is not
itself a decision, only a boundary observation: the existing constraint is
scoped to *generation of the creative artifact*, not to every image any
part of the console might ever need. `[inference]`.

## 4. Gaps

- Pricing figures above are drawn from third-party pricing-comparison sites
  current as of this session, not fetched directly from fal.ai's,
  Replicate's, Stability's, or Ideogram's own pricing pages — treat as
  directionally correct, not exact. `[gap]`.
- Whether the director actually wants Decision 2 revisited (to allow API
  image generation as an overflow/fallback tier, mirroring the Audio
  department's tiered pattern) is unasked and unanswered here — this report
  surfaces the question, it does not resolve it. `[gap]`.

## 5. Recommendation (non-binding)

If the director wants an API image-model fallback tier for the Director
Console (mirroring Audio's local→cheap-API→premium-API pattern), FLUX.1
[dev] is the strongest fit on cost and stylistic consistency with the
existing local Flux Dev FP8 pipeline. But that adoption is a Decision-2
reversal, not a plan detail — it belongs in `alawas-thinking-pressure-test-decision`
against `2026-08-23-001`, not silently folded into the existing
implementation plan. `[inference]`.

---

## Provenance

- `[system]` Implementation plan §1.7, §5.2, §9 (existing hardware,
  audio tiering pattern, active constraints)
- `[decision]` `2026-08-23-001` Decision 2 (no hosted/cloud generation
  dependency)
- `[system]` This session's fal.ai/Replicate 3D-model research
  (`fal-ai/trellis-2`, `fal-ai/hunyuan3d-v21`, `ndreca/hunyuan3d-2.1`)
- `[system]` WebSearch results this session: teamday.ai, pricepertoken.com,
  costbench.com, wireflow.ai, replicate.com/blog, apiframe.ai,
  digitalapplied.com
- `[inference]` Cost-effectiveness ranking, Decision-2-conflict framing, and
  the non-canon-image boundary observation are synthesis, not sourced facts
