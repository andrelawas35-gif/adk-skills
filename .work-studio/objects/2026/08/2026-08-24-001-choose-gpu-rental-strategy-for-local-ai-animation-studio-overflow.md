---
schema_version: 1
id: 2026-08-24-001
title: Choose GPU rental strategy for local AI animation studio overflow
type: inquiry
status: active
state: design
consequence: meaningful
sensitivity: ordinary
domain: [engineering, business]
relates_to: [2026-08-23-002]
created_at: 2026-08-24T08:10:00Z
updated_at: 2026-08-24T17:43:03Z
next_action: Route to alawas-engineering-implement-bounded-change to provision one RunPod Community Cloud A6000 pod, install both ComfyUI custom nodes, run one existing approved image through TRELLIS.2 and through Hunyuan3D-2.1, verify both GLBs import into Blender, and log actual billed time/cost.

---
## Intent

The director's RTX 3080 10GB proved capable of running HiDream O1 locally this
session (see `2026-08-23-007`), but the planned studio architecture
(`2026-08-23-002`) calls for TRELLIS.2 and Hunyuan3D 2.1 for image-to-3D, which
exceed 10GB VRAM. The director proposed renting a cloud GPU — specifically an
RTX A6000 48GB on RunPod Community Cloud at ~$0.33/hr — as a single default
rental machine for the full pipeline (image gen, 3D gen, Blender, video), with
a stated budget ceiling of $0.40/hr, and asked for critique or improvement on
that recommendation.

This is an **inquiry**: which GPU rental approach (single default machine,
narrower overflow-only rental, serverless per-job billing, or multi-provider
shopping) best fits the studio's actual cost and workflow shape is not yet
decided.

## Success evidence

- [ ] At least three materially distinct GPU rental directions presented,
      each grounded in this session's evidence about what already runs
      locally.
- [ ] Information gaps that would discriminate between directions (live
      pricing, actual VRAM minimums, storage/egress costs, serverless
      endpoint availability) are surfaced for the director to resolve.
- [ ] Director selects a direction or requests further investigation.

## Constraints and non-goals

**Constraints:**
- Budget ceiling: ~$0.40/hr stated by the director (testimony, not yet
  recorded in `2026-08-23-002`'s evidence ledger).
- Must compose with the sequential GPU time-sharing philosophy already
  decided in `2026-08-23-002` (RTX 3080 10GB assumes sequential model
  loading, not simultaneous residency).
- HiDream O1 image generation is already proven to run locally on the RTX
  3080 this session — any rental direction should account for what does NOT
  need to move to a rented GPU.

**Non-goals:**
- Selecting a specific rental provider account or provisioning a pod.
- Redesigning the studio pipeline architecture (owned by `2026-08-23-002`).
- Comparing GPU purchase vs rental economics beyond what the director already
  raised.

## Decisions and revisit triggers

### Decision 1 — Rent scoped to the 3D-generation stage only, sized for TRELLIS.2 + Hunyuan3D-2.1

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Selected Direction 2 (refined): rent a 48GB GPU (RTX A6000, RunPod Community Cloud, ~$0.33/hr) scoped specifically to the 3D-generation stage of the pipeline — TRELLIS.2-4B and Hunyuan3D-2.1, run sequentially via their ComfyUI custom nodes, unloaded between models. HiDream O1 image generation stays on the local RTX 3080 10GB, which is already proven to run it for free. Blender assembly/viewport work also stays local unless a specific bottleneck emerges. |
| **Authorization** | Director accepted the recommendation with "yes go ahead" after reviewing confirmed pricing, VRAM figures, the two-model division of labor, and confirmed ComfyUI node availability for both models. |
| **Confidence** | high on pricing and VRAM figures (independently verified against RunPod, TRELLIS.2, and Hunyuan3D-2.1 sources); high on ComfyUI node availability (both actively maintained as of 2026); medium on real-world cost and workflow friction, since no rental has actually been provisioned or tested yet. |
| **Actor** | director |
| **Revisit trigger** | Reopen if a rented session reveals load/unload overhead eats a large share of billed time, if Community Cloud preemption interrupts jobs unacceptably, if Hunyuan3D's path-based model loading proves fragile in practice, or if hero-asset volume grows enough that scoping the rental to "3D only" becomes more expensive than a broader default machine. |
| **Rationale** | Both planned 3D models exceed local 10GB VRAM in their production configurations (TRELLIS.2 minimum 24GB; Hunyuan3D shape+texture 29GB, texture-only 21GB), so 3D generation has no local escape hatch regardless of which model is used — this is where rental spend belongs. Image generation does have a local escape hatch (HiDream O1 already proven working on the 3080), so paying cloud rates for it would be waste. Community Cloud pricing was confirmed live and matches the director's original figures exactly; Secure Cloud costs 26-127% more for reduced preemption risk and remains an option if reliability becomes the binding constraint instead of cost. |

### Decision 2 — Accepted tracer-bullet design: one pod, both models, one asset each

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Bounded first rental test: provision exactly one RunPod Community Cloud A6000 pod; install both ComfyUI custom nodes (TRELLIS.2 via ComfyUI Manager, Hunyuan3D-2.1 via manual git-clone with path-based model loading); reuse an existing approved 2D image (no new generation needed) through TRELLIS.2 to produce one GLB, then through Hunyuan3D-2.1 shape+texture to produce a second GLB; verify both import into Blender without manual repair; log wall-clock time split (node install, model download, each generation pass, unload, export) and real billed cost. Terminate the pod when done — no persistent network storage provisioned. |
| **Authorization** | Director accepted the recommended tracer bullet and confirmed the scope should test both models in this first run, not just one, with "run both models in this first test." |
| **Confidence** | high on pricing/VRAM/node-availability evidence (independently verified); medium on real-world friction and cost, since this is the first actual rental — that uncertainty is exactly what the tracer bullet exists to resolve. |
| **Actor** | director |
| **Revisit trigger** | Reopen if either GLB fails to import into Blender without manual repair, if total billed cost exceeds roughly 2x the theoretical $0.33/hr rate, if Hunyuan3D's path-based model loading proves fragile, or if Community Cloud preemption interrupts the test. |
| **Rationale** | Testing both models in one session (rather than just one) directly matches how Decision 1's "sequential unload" workflow is meant to run in production — a single-model test would leave the cross-model handoff (unload TRELLIS.2, load Hunyuan3D-2.1) unverified, which is itself part of the riskiest assumption. |

## Evidence ledger

| Tag | Source | Entry |
|-----|--------|-------|
| [testimony] | director, 2026-08-24 | Proposed RTX A6000 48GB on RunPod Community Cloud (~$0.33/hr) as default rental machine; A40 48GB (~$0.35/hr) as fallback; ruled out RTX 5090 (~$0.69/hr) as exceeding a $0.40/hr budget ceiling. Cited TRELLIS.2's official 24GB VRAM minimum and Hunyuan3D 2.1's ~29GB shape+texture VRAM need as the reason 24GB cards (4090/3090/A5000) are a worse fit. Proposed a sequential load/unload workflow: image model → unload → 3D model → unload → Blender → image model → unload → MiniMax H3 → export → shut down. |
| [system] | this session, 2026-08-23/24 | HiDream O1 Image Dev FP8 (~7.7GB) runs successfully on the director's local RTX 3080 10GB — confirmed by multiple successful two-stage generation runs in `2026-08-23-007`. This means image generation, the first pipeline stage in the director's own proposed workflow, does not require the rented GPU at all. |
| [system] | runpod.io/gpu-models, fetched 2026-08-24 | Confirmed Community Cloud pricing exactly matches director's figures: RTX A6000 48GB $0.33/hr, A40 48GB $0.35/hr, RTX 4090 24GB $0.34/hr, RTX 3090 24GB $0.22/hr, RTX A5000 24GB $0.16/hr, RTX 5090 32GB $0.69/hr (note: 5090 is 32GB, not the higher figure director may have assumed). |
| [system] | runpod.io/pricing, fetched 2026-08-24 | Secure Cloud (non-preemptible, no interruption risk) costs substantially more than Community Cloud: A6000 $0.53/hr (+61%), A40 $0.44/hr (+26%), RTX 4090 $0.74/hr (+118%), RTX 3090 $0.50/hr (+127%). Network storage: $0.07/GB/mo under 1TB, $0.05/GB/mo over 1TB, $0.14/GB/mo for high-performance storage. Serverless GPU tiers run $0.58/hr (16GB) up to $2.72/hr (A100) — RunPod's serverless pricing is per-worker-hour while active, not obviously cheaper than Community Cloud on-demand for a single sequential workflow. |
| [system] | github.com/microsoft/TRELLIS.2, fetched 2026-08-24 | Confirmed: "An NVIDIA GPU with at least 24GB of memory is necessary." Repo has been validated on A100/H100; no stated recommendation between 24GB and those high-end cards. |
| [system] | github.com/Tencent-Hunyuan/Hunyuan3D-2.1, fetched 2026-08-24 | Confirmed and more precise than the director's summary: shape generation alone needs 10GB VRAM; texture generation alone needs 21GB; the two together need 29GB. This means shape-only generation fits comfortably on the local RTX 3080 10GB — only the combined shape+texture pass, or texture generation alone, requires the larger rented card. |
| [system] | vast.ai/pricing/gpu/RTX-A6000 + web search, fetched 2026-08-24 | Vast.ai lists RTX A6000 as low as $0.29/hr on-demand (below RunPod's $0.33/hr), with a median of $0.55/hr across listings — meaning Vast.ai's cheapest listings undercut RunPod but its typical/median price is worse. Vast.ai bills per-second with no rounding, which favors short jobs. A40 pricing on Vast.ai was not returned by search. |

| [testimony] | director, 2026-08-24 | Confirmed both TRELLIS.2-4B and Hunyuan3D-2.1 are planned models, not a choice between them — TRELLIS.2 for fast/general asset generation, Hunyuan3D for hero/PBR-critical assets. Both run sequentially on one rented card per the director's own workflow diagram. |
| [inference] | agent, 2026-08-24 | This resolves the main uncertainty behind Direction 1 vs Direction 2: 3D generation will always exceed local 10GB VRAM regardless of which of the two models is used (TRELLIS.2 minimum 24GB; Hunyuan3D shape-only 10GB fits locally, but hero assets routinely need texture generation too, pushing to 21-29GB). Image generation (HiDream O1) remains proven to run locally and does not need to move to the rental. This favors a refined Direction 2: rent a 48GB card scoped specifically to the 3D-generation stage (both models, sequential, same session), while image generation and possibly Blender viewport work stay local. |
| [system] | web search, fetched 2026-08-24 | Both models have working, actively maintained ComfyUI custom nodes as of 2026: TRELLIS.2 via `PozzettiAndrea/ComfyUI-TRELLIS2` or `visualbruno/ComfyUI-Trellis2` (installable through ComfyUI Manager's Custom Nodes Manager; supports image-to-3D-mesh with PBR materials, GLB export, multi-image texturing). Hunyuan3D-2.1 via `Yuan-ManX/ComfyUI-Hunyuan3D-2.1` or `visualbruno/ComfyUI-Hunyuan3d-2-1` (manual git-clone install into `custom_nodes/`, requires ComfyUI's embedded Python, validated against ComfyUI v0.3.45; models must sit at `models/diffusion_models/hunyuan3d/hunyuan3d-dit-v2-1` — path-based loading, not filename-based). This confirms the 3D-generation stage fits the director's existing ComfyUI-centric workflow style rather than requiring a separate tool. |
| [decision] | director, this session, 2026-08-24 | Director asked whether the GPU on the running tracer-bullet pod could be changed, learned pod GPU type is fixed at creation (only a Network Volume is portable across pods/GPU types, not a pod's local disk), and explicitly chose to set up a Network Volume rather than accept the throwaway-disk approach Decision 2 originally specified ('no persistent network storage provisioned'). This is a deviation from Decision 2's original scope: adds a standing, separately-billed persistent storage resource so the ComfyUI + custom node install survives across pods and GPU-type changes, rather than being reinstalled from scratch each time. |
## Open questions

- Does the full pipeline actually need one GPU rented for everything, or only
  for the stages that exceed local VRAM (3D generation, and possibly video)?
- Is a persistent Community Cloud pod (billed per wall-clock hour including
  model load/unload time) the right billing shape, or would serverless
  per-job billing fit the "one asset at a time" usage pattern better?
- How much does model load/unload time itself cost across a typical session,
  given the proposed sequential workflow unloads and reloads multiple large
  models?
- Is RunPod the only marketplace worth comparing, or should Vast.ai/Lambda
  be priced against it before committing?

## Next move

Route to `alawas-engineering-implement-bounded-change` to execute the
accepted tracer bullet: provision one RunPod Community Cloud A6000 pod,
install both ComfyUI custom nodes, run one existing approved image through
TRELLIS.2 and through Hunyuan3D-2.1 (both models, one asset each), verify
both GLBs import into Blender without manual repair, log actual billed
time/cost, and terminate the pod.

## History

### 2026-08-24T08:10:00Z — Created inquiry for GPU rental strategy

- **State:** explore
- **Status:** active
- **Actor:** agent (develop-idea skill)
- **Rationale:** Director asked for critique/improvement on a specific GPU rental recommendation for the local AI animation studio's cloud overflow needs. This is genuinely undecided — related to but distinct from `2026-08-23-002`'s architecture — so it gets its own inquiry rather than being folded into that Work Object's scope.

### 2026-08-24T08:35:00Z — Confirmed pricing and VRAM figures

- **State:** explore
- **Status:** active
- **Actor:** agent (web_fetch + web_search)
- **Rationale:** Director asked to verify the pricing and VRAM figures behind the four directions before selecting. RunPod Community Cloud pricing matches the director's original figures exactly. Secure Cloud costs 26-127% more depending on card, trading preemption risk for reliability. Hunyuan3D 2.1's VRAM requirement decomposes more favorably than summarized: shape-only generation needs just 10GB (fits the local RTX 3080), texture needs 21GB, combined needs 29GB. TRELLIS.2's 24GB minimum is confirmed as stated. Vast.ai's cheapest A6000 listings ($0.29/hr) undercut RunPod, but its median price ($0.55/hr) is worse — the marketplace has more price variance than a single quoted rate suggests.

### 2026-08-24T09:00:00Z — Confirmed ComfyUI node availability for both 3D models

- **State:** explore
- **Status:** active
- **Actor:** agent (web_search)
- **Rationale:** Director confirmed a two-model division of labor (TRELLIS.2 for fast/general assets, Hunyuan3D-2.1 for hero/PBR assets) and asked whether both fit the existing ComfyUI-centric workflow. Confirmed both have actively maintained ComfyUI custom nodes as of 2026 — TRELLIS.2 installs through ComfyUI Manager directly; Hunyuan3D-2.1 requires manual git-clone install with a path-based (not filename-based) model-loading requirement worth noting for setup. This closed the last open question blocking a direction selection.

### 2026-08-24T09:10:00Z — Selected refined Direction 2; transitioned to design

- **State:** explore → design
- **Status:** active
- **Actor:** director
- **Rationale:** Director accepted the recommendation to rent a 48GB GPU (RTX A6000, RunPod Community Cloud) scoped specifically to the 3D-generation stage, running TRELLIS.2 and Hunyuan3D-2.1 sequentially via ComfyUI nodes, while keeping HiDream O1 image generation on the local RTX 3080 where it already runs for free. Recorded as Decision 1. Routing to design-tracer-bullet for a bounded first rental test before this becomes the standing pattern — no pod has been provisioned yet.

### 2026-08-24T09:25:00Z — Accepted tracer-bullet design covering both models

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** design-tracer-bullet proposed testing one existing approved image through both TRELLIS.2 and Hunyuan3D-2.1 on a single rented A6000 pod, verifying Blender import and logging real billed cost/time, before treating the rental pattern as standing practice. Director confirmed the scope should cover both models (not just one) in this first test, since the cross-model unload/reload handoff is itself part of what needs verifying. Recorded as Decision 2. No pod has been provisioned yet — routing to implement-bounded-change to actually execute it.
