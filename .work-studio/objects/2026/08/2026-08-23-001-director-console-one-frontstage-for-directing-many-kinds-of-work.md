---
schema_version: 1
id: 2026-08-23-001
title: Director Console — one frontstage for directing many kinds of work
type: inquiry
status: active
state: verify
consequence: meaningful
sensitivity: ordinary
domain: [ideation, architecture]
created_at: 2026-08-23T19:03:34Z
updated_at: 2026-08-25T00:05:26Z
next_action: V0 verified; V1 continuation opened as 2026-08-24-006 (responds_to 001). 001 itself may transition toward observe/close (outcome review) at the director's call.














































---
## Intent

Explore the "Director Console" product concept the director brought in from a
prior session (full concept pasted as the invoking argument, `[testimony]`):
one **frontstage** where a human directs very different kinds of work
(creative direction, software engineering, research, production) by typing
ordinary natural-language direction, while all structure — work objects,
governance, workflows, skills, capabilities, tools — stays **backstage** and
never leaks into the interface.

Core loop: `you → natural-language direction → system structures/investigates/
executes → artifact comes back changed/explained/compared → you judge and
redirect`. The console is framed as "not primarily an interface for
orchestrating agents; an interface for human judgment over evolving
artifacts." Practice Profiles (creative/software/research/production) swap the
workflow, epistemic rules, verification, and inspector contents while the
three-pane shell (Context / Artifact / Inspector + Director input) stays
stable. Mode (create/investigate/compare/review/implement/verify/incident) is
the current stage within a practice.

This is an **inquiry**: the concept is rich and internally coherent, but which
version of it to actually pursue first — and how it relates to the Work Studio
that already exists — is not yet decided. That is what this Work Object exists
to open up, not to close.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [ ] At least three materially distinct directions for pursuing the Director
      Console concept are generated and recorded
- [ ] The director selects one or more directions (or asks to combine/reframe)
- [ ] Information gaps that discriminate between directions are surfaced


## Constraints and non-goals

**Constraints:**
- File-first: every artifact and variant is a local file; the studio/local
  filesystem remains the source of truth (retained from the earlier
  agent-agnostic rule).
- Model-agnostic: generation sits behind a capability (an "instrument"), not a
  hardcoded tool; any image model behind ComfyUI/Blender satisfies it.
- Local-install dependency is accepted (Blender, ComfyUI) — the one narrowing
  of the earlier "dependency-free" constraint, bounded to a local-install
  requirement, never a hosted/network dependency (Decision 2).

**Non-goals:**
- Building a fresh standalone Next.js/SQLite product (Direction 2, not
  selected).
- Building the multi-practice console up front — only the creative-variant
  practice is in scope first.
- Any hosted/cloud generation dependency.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Pursue combined Direction 1 + 3 (studio-skin frontstage, creative-variant loop as first practice)

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Of four generated directions, the director selected 1 (frontstage skin over the existing Work Studio — no new backend, Work Objects/evidence/decisions as the model, three-pane view generated the way command-center.html and asset-workbench.html already are) and 3 (build only the Creative Direction practice first, and within it the studio's genuinely-missing capability: variants as real artifact branches with visual comparison, selection, and direction lineage). Combined into one path: a studio-backed frontstage whose first built practice is the creative-variant loop. Directions 2 (fresh standalone Next.js/SQLite product) and 4 (schema-only, no visual product) not selected. |
| **Authorization** | Director: "direction 1 and 3" |
| **Confidence** | high for the selection; medium for the combination framing (I proposed merging 1+3 into a single path and stated it explicitly; director selected the two directions but did not separately re-confirm the merge wording — treat the combined framing as provisional until the tracer either validates it or the director corrects it). |
| **Actor** | director |
| **Revisit trigger** | If a tracer bullet shows the studio's markdown/CLI substrate cannot back an interactive three-pane view acceptably (Direction 1's key assumption fails), or if hand-running one creative-variant loop shows the variant/lineage need isn't real (Direction 3's key assumption fails). |
| **Rationale** | Direction 1 preserves the agent-agnostic / local-file-first constraint set earlier this session (no parallel SQLite product; the studio remains sole source of truth). Direction 3 aims the first build at the one capability the studio lacks rather than re-skinning what it already does. Together they minimize new backend while maximizing new capability. |

### Decision 2 — Grilling outcome: constraint narrowed, instruments named, tracer redirected

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Director requested an adversarial grilling of the combined 1+3 plan before any tracer. Four pressure points run serial-depth; outcomes: (1) Dir 1's "no new backend" is **narrowed** — the studio backs the Context + Inspector panes but nothing of the artifact-first Artifact pane, which is a genuinely new layer. (2) The console is confirmed **artifact-first with real images as branchable objects** (director: "Artifact-first — real images as branchable objects"). (3) Images come from **generation-first**, seeded by director intent or an uploaded image (director: "generation first based on my own intent or image i uploaded"). (4) The instruments are **Blender and ComfyUI** (director: "working with blender and comfyui") — both local, file-first, scriptable, so the earlier agent-agnostic constraint is **narrowed, not broken**: file-first truth and model-agnosticism survive; only dependency-freeness gives way, and only to a *local-install* requirement (same shape as needing python/tools.ws), not a hosted/network dependency. Generation sits behind the concept's own **instruments** layer (a requested capability, not a hardcoded tool). |
| **Authorization** | Director across the grilling: "Artifact-first — real images as branchable objects" / "upload and image model generates" / "generation first based on my own intent or image i uploaded" / "working with blender and comfyui" / "record it". |
| **Confidence** | high for the four substantive answers (each a direct director statement); medium for the "instruments are orchestrated external processes = the plan's hard middle" framing (inference, not yet tested — that is exactly what the tracer must probe). |
| **Actor** | director |
| **Revisit trigger** | If the one-loop tracer shows orchestrating a single render-to-lineage cycle through Blender/ComfyUI is disproportionately painful, reopen whether the creative-variant loop is the right first practice (would swing back toward Dir 1's governance panes first). |
| **Rationale** | The original tracer (render a Work Object as three static panes) tested the already-proven easy part and would have produced a false green. Grilling relocated the real risk to the artifact/generation layer and to process orchestration of local instruments, which is where the plan's genuine unknowns live. |

### Decision 3 — Tracer validated retroactively: `2026-08-23-007`'s real execution satisfies the intent-to-lineage loop

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Routed from grilling to the tracer-bullet discipline. Riskiest assumption: orchestrating a local generative instrument for one intent -> image -> lineage cycle is tractable. Tracer originally designed as **three stations**: (1) prose intent -> **local LLM (Qwen3.5-9B Q4 via Ollama/LM Studio) emits a structured Direction object** `{intent, protect, change, avoid}` JSON; (2) ComfyUI consumes it and renders a PNG (LLM makes no pixels, ComfyUI does no reasoning); (3) PNG saved to a local path under the Work Object + one lineage record linking intent->Direction JSON->output. **Resolved 2026-08-24 by director judgment**, not a fresh isolated test run: the child WO `2026-08-23-007` already executed this exact loop shape ~24 times over real asset-generation cases (S001-S005) -- each of its Decisions IS a lineage record (director/critique intent -> revision method -> ComfyUI render -> recorded outcome), on the same local stack (ComfyUI :8188, confirmed running; Ollama with `isotnek/qwen3.5:9B-Unsloth-UD-Q4_K_XL` loaded, confirmed present). This is a materially larger and more rigorous exercise of the core assumption than the original minimal tracer called for. |
| **Authorization** | Director: "yes it's already validated" (accepting that `2026-08-23-007`'s prior execution satisfies this tracer, in lieu of a redundant fresh run). |
| **Confidence** | high that the core assumption (local intent -> generation -> recorded lineage is tractable) is proven -- this is not inference, it is ~24 real executions. Medium-low on one narrower point, noted honestly rather than silently folded in: the specific sub-step "a **separately-invoked local LLM call** structures prose into the `{intent, protect, change, avoid}` JSON" was not isolated as its own tested step in `2026-08-23-007` -- there, the orchestrating agent wrote each revision's structured direction directly, rather than round-tripping through a dedicated Ollama call. Ollama + Qwen3.5 are confirmed present and reachable on this machine (`curl 127.0.0.1:11434/api/tags`), so the capability exists; it just wasn't exercised as an isolated station in the validating evidence. |
| **Actor** | director |
| **Revisit trigger** | Reopen only if the actual V0 build (Direction-input parsing, plan §7 V0 table) shows the local-LLM JSON-structuring step behaves materially differently than the agent-authored structuring `2026-08-23-007` relied on -- e.g. Qwen3.5 fails to reliably emit valid `{intent, protect, change, avoid}` JSON on real director prose. That would be a first real test of the narrower point above, not a reopening of the core loop-tractability finding. |
| **Rationale** | The tracer's purpose was to retire the risk that intent->generation->lineage is unworkable on this hardware/stack before committing to the V0 build. That risk is retired -- decisively, by volume of real evidence, not a single toy run. Re-running an isolated, disconnected three-station test (as first attempted, then stopped) would have tested nothing `2026-08-23-007` hadn't already exercised more thoroughly, and would have ungrounded the test from the actual accepted subject matter (assets), which the director explicitly redirected against. |

### Decision 4 — Split the taste-system suggestion: adopt Aesthetic Canon now, defer Taste Evaluator

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Of the director-submitted three-layer taste system (aesthetic canon / taste evaluator / learned adapters), adopt only the **Aesthetic Canon** layer now: an explicit principles/anti-principles document (composition, light, color, texture, performance, environment, motion, narrative, finish dimensions with prefer/avoid lists), stored as a design asset any specialist skill can reference. Defer the **Taste Evaluator** (VLM/API-LLM critique, pairwise ranking, scorecards), the new **Aesthetic Critic** specialist, and pairwise-preference recording in Decision records until the WO `2026-08-23-007` revision-lane tracer produces a passing result. Defer LoRA training and any reward/ranking model to "V7+, not yet scoped" per the Director Console plan's own explore-before-canonize philosophy (`2026-08-23-001-director-console-implementation-plan.md` §5.4, §9). If and when the Evaluator is later adopted: taste critique routes through the existing API LLM's vision capability, not a new local VLM instrument (the Qwen3-VL embedded in HiDream O1 per `2026-08-23-007` Decision 3 is an internal encoder, not a callable critique tool, and stays out of scope); pairwise judgments are recorded as structured entries inside the existing per-variant Decision record (plan §3.4) rather than a new schema; and Evaluator output is advisory-only, populating the plan's existing `PROPOSED ?` channel (plan §6.4), never auto-filtering candidates before director review. |
| **Authorization** | Director: "yes, do recommended" — accepted the pressure-tested Branch C recommendation. |
| **Confidence** | medium-high. Grounded directly in `2026-08-23-007`'s own Decision 6 (fail), Decision 7 (fail), and Decision 8 (pending) [system]: the revision-lane pipeline the Evaluator would judge is not yet reliably producing distinguishable variants, so building comparison machinery against it now would be judging noise. The canon has no such dependency — it is a document, not infrastructure. |
| **Actor** | director |
| **Revisit trigger** | Reopen Evaluator/Aesthetic-Critic/pairwise-recording scope when `2026-08-23-007`'s Decision 8 (or its successor) passes and the S001-S005 suite clears its 3-of-5 threshold — that is the first evidence variants can be reliably distinguished at all. Reopen the VLM-instrument resolution if the API LLM's vision capability proves insufficient for critique quality once the Evaluator is actually built. |
| **Rationale** | Three branches were tested: adopt the full taste system now, defer everything, or split by dependency. The canon has zero dependency on the revision pipeline and fills a real, independently-identified gap (no cross-project aesthetic vocabulary exists in the plan today). The Evaluator, Critic specialist, and pairwise-ranking machinery all depend on variants existing and being distinguishable, which `2026-08-23-007`'s own evidence shows is not yet true. Splitting avoids both premature infrastructure and discarding the one piece with immediate, dependency-free value. |
| **Edge case noted** | If the canon's prefer/avoid vocabulary itself needs revision once real variants exist to test it against (i.e., abstract principles don't survive contact with actual generated images), that is expected and does not invalidate adopting it now — the canon is meant to evolve via evidence, not be authored once and frozen. |

**Also surfaced, not part of this decision:** the Director Console implementation plan (`2026-08-23-001-director-console-implementation-plan.md` §1.7, §10) still names Flux Dev FP8 as the resolved V4 prerequisite, but `2026-08-23-007` Decision 3 already moved image generation to HiDream O1. This is a supersession candidate independent of the taste-system question and should be corrected the next time that plan document is revised — flagged here as a `[gap]`, not resolved by this decision.

### Decision 5 — Accept the Creative Precedent Library into the plan: harvest-first, three new object types, reuse existing primitives

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Accept the §7 recommended plan revisions from the report deliverable `2026-08-23-001-asset-recipe-library-design-critique.md` and fold them into the canonical implementation plan. Five concrete edits: (1) §5.4 — add the two `[system]`-verified recipes harvested from closed `2026-08-23-007` (segmentation-masked regional revision; single-view image-to-3D mesh for turnaround identity) as the Asset Production Department's first validated entries; (2) new §5.5 Creative Precedent Library — the corrected object model (three genuinely-new object types Recipe/Revision/TastePrinciple, referencing the seven existing primitives by ID rather than cloning them), harvest-first build order, and mandatory anti-homogenization Reference Pack rule; (3) §4 — extend the Art/Asset Director specialist boundary to require capture-at-generation; (4) §6.4 — note the PRESERVED/CHANGED/PROPOSED report IS the Revision capture format; (5) §2.4 — record the retrieval-embedding VRAM constraint and the decision to reuse the already-installed `sigclip_vision` model rather than add another. |
| **Authorization** | Director: "fold the §7 revisions into the plan" (explicit, after reading the full report critique). |
| **Confidence** | high for the acceptance itself (direct, specific director instruction naming §7); medium for the harvest-first build order being the cheapest correct path — grounded in `2026-08-23-007` already containing 2 validated recipes + ~6 counter-examples `[system]`, but the harvesting projection itself is unbuilt and its edge-set expressiveness against `ws relation`/`ws graph` is an open `[gap]` per the report §8. |
| **Actor** | director |
| **Revisit trigger** | Reopen if v0 harvest reveals `ws relation`/`ws graph` cannot express the precedent-graph edge set (`realized_by`, `failed_for`, `protects`, `supports`) — report §8 gap. Reopen the object model if capture-at-generation proves unenforceable at the Art Director skill boundary and tags end up applied retroactively (the make-or-break failure mode, report §3.7). |
| **Rationale** | The extensive adversarial critique in the report deliverable itself served the pressure-testing function for this decision: it endorsed the strong parts, corrected the greenfield framing to harvest-first, prevented the reinvention of seven existing primitives, and assigned the ungoverned status lifecycle to `track-components`. The director accepted after seeing that critique, so a separate formal `pressure-test-decision` pass would add process without adding scrutiny. The plan edit is now backed by this accepted Decision, so the plan continues to "synthesize only accepted material" rather than authoring new architecture unilaterally. |

### Decision 6 — Decision 5's revisit trigger fires: `ws relation`/`ws graph` cannot express the precedent-graph edge set; storage model corrected to the Component Ledger pattern

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | fail (of the original claim) → corrected |
| **Scope** | Direct CLI verification (director: "verify ws relation and ws graph edge-set expressiveness") of the exact revisit condition named in Decision 5. Confirmed: `ws relation add` requires both endpoints to be full Work Object IDs — it cannot link two sub-WO precedent records (Recipe↔Revision, Artifact↔Recipe) unless each becomes its own full Work Object, which is too heavy for small, numerous records. The 16-verb edge vocabulary also has no verb for Revision-specific `protects`/`changes` semantics. This falsifies plan §5.5's claim that Recipe/Revision/TastePrinciple would be "traversed via `ws relation`/`ws graph`" with the NetworkX projection as "the query layer for free." **Correction:** the studio's own existing precedent for this exact shape of problem — many small named things, each with declared dependency edges — is the **Component Ledger** (`.work-studio/component-ledger.md`, ADR 0014), which does not use `ws relation`/`ws graph` either; it is a single derived Markdown index with hand-declared prose edges per entry. Recipe/Revision/TastePrinciple storage and traversal should follow that pattern, not the WO-relation graph. |
| **Authorization** | Director: "verify ws relation and ws graph edge-set expressiveness" (direct instruction to check the named gap). |
| **Confidence** | high — this is a direct CLI check (`ws relation add --help`, `ws graph trace --help`), not inference, and the Component Ledger's actual file content was read to confirm it does not use `ws relation`/`ws graph`. |
| **Actor** | director |
| **Revisit trigger** | Reopen if a future `ws relation`/`ws graph` version adds sub-WO-record edge support, making the original §5.5 claim viable again. Until then, the Component-Ledger-pattern correction stands. |
| **Rationale** | Decision 5 explicitly flagged this as unverified and named the exact revisit condition; verifying it before building v0 (rather than after) avoids building a harvester against a graph mechanism that cannot hold the data. The correction reuses an existing, already-working studio pattern (Component Ledger) instead of inventing new graph infrastructure — consistent with Decision 5's own "reuse, don't rebuild" principle. |

### Decision 7 — Tracer bullet: hand-extracted Recipe R-001 mostly validates harvesting, but exposes a real gap in prompt-string capture

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | mixed (majority pass) |
| **Scope** | Design-tracer-bullet: hand-extract one Recipe entry (R-001, segmentation-masked-regional-revision) from `2026-08-23-007` Decision 16's existing prose into `.work-studio/precedent-ledger.md`, following the Component-Ledger-pattern storage from Decision 6. Tested the riskiest assumption that Decision prose alone carries enough structured signal to populate the Recipe schema without fabrication. |
| **Authorization** | Director: "yes, run it" (accepting the tracer-bullet design recommendation). |
| **Confidence** | high — this is a direct, executed extraction against real source text, not inference. 6 of 9 schema fields (purpose, applicable_when, operations, verification, known_limits, provenance, status) populated cleanly and traceably with zero fabrication. 2 fields (`prompt_template`, `negative_constraints`) could not be honestly populated from Decision 16's own narrative text — the literal prompt string and negative-conditioning approach exist only in the scratchpad script the Decision's evidence references, not in the Decision's prose, and were marked `[gap]` rather than invented or pulled from outside-session memory. |
| **Actor** | director |
| **Revisit trigger** | Reopen the v0 harvester's scope if a second recipe extraction (a different case, e.g. `2026-08-23-007` Decision 24) shows the same two fields gap the same way — that would confirm a systematic pattern (Decision prose narrates method/outcome but not literal prompt text) rather than a one-off, and would mean the harvester either accepts `prompt_template`/`negative_constraints` as routinely `[gap]`, or must also read the linked scratchpad script artifacts to fill them. |
| **Rationale** | The tracer bullet did its job: it demonstrated the assumption holds for the *majority* of the schema (method, parameters, outcome, limits, provenance — genuinely cheap to harvest from existing prose) while surfacing one specific, real limitation (literal prompt text isn't preserved in Decision narrative) rather than a wholesale failure of the harvest-first premise. This is exactly the kind of result a tracer bullet should produce: neither a clean pass that hides a real gap, nor a failure that discards a mostly-working approach. |

### Decision 8 — Second extraction (R-002) refines the tracer finding: the prompt gap is recipe-kind-specific, not universal

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Per Decision 7's revisit trigger, hand-extracted a second Recipe (R-002, single-view-image-to-3d-mesh-turnaround) from `2026-08-23-007` Decision 24 into `.work-studio/precedent-ledger.md`, to test whether R-001's `prompt_template`/`negative_constraints` gap was systematic or a one-off. |
| **Authorization** | Director: "yes, run it." |
| **Confidence** | high — all 9 schema fields populated for R-002, but `prompt_template`/`negative_constraints` are marked **N/A**, not `[gap]`: this recipe's mechanism (image-to-3D mesh via Hunyuan3D-2) has no text-prompt conditioning step at all, so there is nothing to gap. This is a materially different result from R-001, where a prompt genuinely exists in the mechanism but wasn't captured in Decision prose. |
| **Actor** | director |
| **Revisit trigger** | Reopen if a third extraction from a prompt-based recipe (any future 2D-generation Decision) also gaps `prompt_template` — that would confirm the pattern is systematic across all prompt-based recipes specifically (not resolved by this second data point alone, since R-002 is a non-prompt recipe and doesn't actually test the "is R-001's gap systematic among prompt-based recipes" question). |
| **Rationale** | The tracer bullet's second run refined rather than merely repeated the first finding: it revealed that "missing prompt field" has two distinct causes (mechanism has no prompt at all, vs. a prompt exists but wasn't recorded) that a harvester must distinguish, since conflating them would either wrongly flag a complete N/A recipe as incomplete, or wrongly treat a genuinely gapped prompt-based recipe as fully captured. This is a more precise, more useful result for designing the real harvester than either extraction alone. |

### Decision 9 — v0 harvester built as a scaffolding tool, not a Recipe generator

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Implemented `tools/precedent_harvest.py` per the accepted tracer exit criteria (Decisions 7-8): given a Work Object id and Decision number, mechanically extracts the raw Decision record (via the existing `parse_decisions_table` utility) and scaffolds a Recipe entry into `.work-studio/precedent-ledger.md` with judgment-requiring fields explicitly marked `[NEEDS INTERPRETATION]`, never guessed. Standalone script, no `tools/ws/__main__.py` CLI wiring added. |
| **Authorization** | Director: "route to implement-bounded-change." |
| **Confidence** | high — the tool is deliberately scoped below full automation, matching the tracer's own finding (Decisions 7-8) that field population requires judgment a script cannot safely fake; verified by running it against `2026-08-23-007` Decision 12 (deliberately a different, falsified Decision, not R-001/R-002), confirming correct mechanical extraction with zero fabrication, then removing the test entry since Decision 12 is superseded and not a real recipe candidate. |
| **Actor** | director |
| **Revisit trigger** | Reopen if, after using this scaffolding tool for several more recipes, the `[NEEDS INTERPRETATION]` completion step proves reliably mechanical after all (e.g. a consistent sub-pattern in Decision prose that could itself be parsed) — that would justify automating further. Reopen the "no CLI wiring" choice if this tool needs to be invoked from `alawas-governance-conduct-work-object`'s routine operation rather than standalone. |
| **Rationale** | Builds only what the tracer validated: mechanical extraction is reliable, field interpretation is not. Automating the interpretation step would reintroduce exactly the retroactive-tagging risk the plan (§5.5) and report critique (§3.7) warn against. Keeping the tool standalone (not wired into the main CLI) matches the smallest-reversible-change principle -- one new file, no risk to existing `ws` commands. |

### Decision 10 — Replace Qwen3.5/Ollama (local LLM) with DeepSeek V4 Flash Vision as the single reasoning + visual-critique instrument; local no-network fallback is deliberately given up

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Fully replace the "Local LLM (Qwen3.5-9B Q4 via Ollama)" instrument with `deepseek-v4-flash-vision-exp` (DeepSeek's multimodal vision-language API, OpenAI-compatible endpoint `https://api.deepseek.com/chat/completions`, up to 32 MiB inline images, 600 images/request, 384 tokens/image) -- confirmed via direct fetch of `https://api-docs.deepseek.com/guides/vision`, not assumed. DeepSeek V4 Flash Vision now takes over both roles Qwen previously held (offline-fallback reasoning/routing/classification, and the Direction-JSON-structuring station-1 role from Decision 3) **and** fills the plan's previously-generic "API LLM ... visual critique" slot with a concretely named, vision-capable model -- directly satisfying Decision 4's deferred-Taste-Evaluator note that critique should route through "the existing API LLM's vision capability, not a new local VLM instrument." |
| **Authorization** | Director: "use deepseek v4 flash vlm instead of local llm ... add it to the plan," then explicitly confirmed "Full replacement of Qwen3.5" when asked to disambiguate scope (vision-role-only vs. full replacement). |
| **Confidence** | high that this is a real, deliberate tradeoff, not a free upgrade: DeepSeek V4 Flash Vision is a cloud API model, so this **removes the plan's only fully local, no-network-dependency reasoning worker**. The plan's existing constraint "No hosted/cloud generation dependency" (Decision 2, §9) is unaffected -- it governs image/video *generation* (ComfyUI/Blender stay local), not text reasoning, and a separate constraint ("API LLM for reasoning (cloud OK for cognition, not generation)", director testimony, §9) already permitted cloud reasoning in principle. What changes concretely: there is no longer any local fallback if the network is down and only text reasoning/critique is needed -- Qwen previously covered that case; nothing does now. |
| **Actor** | director |
| **Revisit trigger** | Reopen if network unavailability during a production session becomes a real, observed problem (not hypothetical) -- that would be the first genuine test of the offline-fallback capability just given up. Reopen the model choice itself if `deepseek-v4-flash-vision-exp`'s "-exp" (experimental) status changes materially (deprecated, renamed, or reaches general availability) or if its vision-critique quality proves insufficient once the deferred Taste Evaluator (Decision 4) is actually built. |
| **Rationale** | The director made this tradeoff with the offline-fallback cost stated plainly first, not discovered later -- an explicit, informed choice rather than an assumed free win. Consolidating to one API vision-capable model (rather than Claude for reasoning + a separate local Qwen for fallback + an eventually-needed third VLM for critique) is architecturally simpler, and directly resolves Decision 4's deferred Evaluator by naming the "existing API LLM's vision capability" it always intended to use. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [testimony] | Director, grilling turn | Console is artifact-first: real images as branchable objects, not text/markdown records. |
| [testimony] | Director, setup paste | Target hardware: Ryzen 5 5600X, 32 GB RAM, RTX 3080 10 GB VRAM (director-stated, unverified). |
| [testimony] | Director, setup paste | Intended local model: Qwen3.5-9B (stated multimodal) at Q4 via Ollama or LM Studio; Gemma 3 12B Q4 as second-opinion critic; a small 3-4B worker for classification/routing. |
| [testimony] | Director, setup paste | Intended stack: Windows 11 + Blender + ComfyUI + Ollama/LM Studio + Qwen3.5-9B Q4 + Postgres + Director Studio + VS Code. |
| [testimony] | Director, setup paste | LLM role is to translate director prose into structured production instructions (Direction JSON), not to generate imagery; ComfyUI generates. |
| [inference] | Setup synthesis | 10 GB VRAM forces sequential GPU time-share (load LLM -> unload -> load diffusion -> unload -> reload); this load/unload orchestration is the tracer's concrete hard-middle. |
| [gap] | Precondition check | Whether ComfyUI is currently running locally on :8188 with a model is unconfirmed; the tracer cannot be run to pass/fail until it is. |
| [system] | Live probe of :8188 /system_stats (2026-08-23) | ComfyUI 0.33.3 IS running locally; RTX 3080 present, 10.7 GB VRAM total / ~9.5 GB free; ComfyUI Desktop build (deploy_environment local-desktop, show_signin_button, comfy-kitchen/comfy-aimdo cloud-API packages, --enable-manager). |
| [system] | Live probe of /object_info + on-disk models dir | NO local image-generation weights installed: checkpoints/, diffusion_models/, unet/, text_encoders/, clip/, loras/ all empty. Only VAE present is minimax_h3_audio_vae_fp32 (an AUDIO vae). This instance cannot render an image locally without first installing model weights. Model root: C:\Users\Andre\AppData\Local\Comfy-Desktop\ComfyUI-Shared\models. |
| [inference] | Tracer synthesis | ComfyUI-running precondition is met, but the deeper precondition (a LOCAL image model, per the file-first / no-hosted-dependency constraint in Decision 2) is NOT. The Desktop build's default generation path is cloud API nodes, which would contradict Decision 2 if used. |
| [testimony] | Director, grilling turn | Variants are generation-first, seeded by director intent or an uploaded image. |
| [testimony] | Director, grilling turn | Generation instruments are Blender and ComfyUI (local, file-first, scriptable). |
| [inference] | Grilling synthesis | Agent-agnostic constraint narrows to: file-first + model-agnostic retained; dependency-freeness reduced to a local-install requirement, not a network dependency. |
| [inference] | Grilling synthesis | Blender/ComfyUI are orchestrated external processes; process orchestration (launch, hand graph, await render, collect output, record lineage) is the plan's hard middle and the tracer's real target. |
| [testimony] | Director, session 2026-08-23 | Director provided a 20-section updated system plan covering writing departments, performance/audio pipeline, visual production tiers, bounded Blender tools, ComfyUI appearance exploration, specialist profiles, animatic as truth test, and API-model-first architecture. |
| [testimony] | director | Director's 3D asset pipeline testimony: three ComfyUI→Blender paths (reference, AI 3D generation via Hunyuan3D/Tripo, direct LLM editing), three environment techniques (Full 3D, 2.5D parallax, generated video), character pipeline (conservative: concept→turnaround→3D→cleanup→rig→canon, then stop regenerating), prop pipeline (aggressive AI generation), asset creation funnel (explore→select→reconstruct→clean→approve→canonize→reuse), LLM strengths (primitives, layout, parametric) vs limits (hero sculpting, organic topology), anti-pattern (don't regenerate everything per shot). |
| [testimony] | director | Hardware-aware environment production workflow: 9-step hybrid pipeline (concept→select→blockout→camera test→asset tier division→AI 3D selective→assemble→ComfyUI texture→composite), four asset tiers (hero geometry, modular geometry, 2.5D elements, pure atmosphere), production rules (camera-proves-existence, design cameras before finishing assets), modular kit assembly via LLM, environment language extraction as structured design rules, concrete first-environment tracer (one alley + three shots proves the pipeline), sequential GPU load/unload cycle. |
| [system] | filesystem | Flux Dev FP8 diffusion model found installed in ComfyUI: flux1-krea-dev_fp8_scaled.safetensors at ComfyUI-Shared/models/diffusion_models/. Decision 3 image model blocker is resolved. |
| [system] | system | SC030 V0 tracer (WO 2026-08-23-004) validated the Direction-to-evidence pipeline end-to-end and surfaced one defect: ws direction --record embeds multi-line format_direction() output into a single Evidence ledger table row, breaking the markdown table format (validate flags lines 6-8). Direction recording pipeline works; the evidence writer needs newline escaping or single-line serialization. |
| [system] | Direct CLI verification: python3 -m tools.ws relation add --help, ws graph trace --help; .work-studio/component-ledger.md; docs/adr/0014-add-component-ledger-artifact-type.md | Verified ws relation / ws graph directly against the CLI (per Decision 5's revisit trigger). Findings: (1) 'ws relation add' requires both id and --to to be full Work Object IDs (or an external:<locator> string) -- there is no mechanism to link two sub-WO records (e.g. Recipe-to-Revision, Artifact-to-Recipe) unless each is itself a full Work Object. (2) The edge-type vocabulary is a fixed 16-verb list (responds_to, resulted_in, supersedes, depends_on, blocks, implements, verifies, observes, revises, supports, counters, authorized_by, generated_by, used, invalidates, hands_off_to) with no verb for Revision-specific semantics (protects/changes). (3) The studio's own existing precedent for 'many small named things with declared dependency edges' -- the Component Ledger, .work-studio/component-ledger.md, ADR 0014 -- does NOT use ws relation/ws graph at all. It is a single derived Markdown index with hand-declared prose edges per entry (depends-on/depended-on-by), not a machine-traversed graph. This directly falsifies the plan §5.5 claim that Recipe/Revision/TastePrinciple would be 'traversed via ws relation/ws graph' with the NetworkX projection as 'the query layer for free.' |
| [system] | tools/ws/component_ledger.py, docs/adr/0014-add-component-ledger-artifact-type.md | Live-question follow-up on Decision 6: read tools/ws/component_ledger.py (47 lines, regex parser over one Markdown file, depends-on/depended-on-by are unparsed generic key:value bullets) and docs/adr/0014-add-component-ledger-artifact-type.md in full. Confirms zero code path connects the Component Ledger to ws relation/ws graph today, and ws relation was never evaluated as an alternative when the Component Ledger was designed. Neither fact changes Decision 6's conclusion, but closes the historical-precedent gap. |
| [system] | .work-studio/precedent-ledger.md (R-001 entry); source: 2026-08-23-007 Decision 16 | Tracer bullet run: hand-extracted one Recipe entry (R-001, segmentation-masked-regional-revision) from 2026-08-23-007 Decision 16 into .work-studio/precedent-ledger.md, following the Component-Ledger-pattern storage from Decision 6. Result: 6 of 9 schema fields (purpose, applicable_when, operations, verification, known_limits, provenance, status) populated cleanly and traceably from existing Decision prose with zero fabrication. 2 fields (prompt_template, negative_constraints) could NOT be honestly populated from Decision 16's text alone -- the exact prompt string and negative-conditioning approach exist only in the scratchpad Python script the Decision's evidence references, not in the Decision's own narrative text, and were marked [gap] rather than fabricated or pulled from outside-session memory. |
| [system] | .work-studio/precedent-ledger.md (R-002 entry); source: 2026-08-23-007 Decision 24 | Second tracer extraction: hand-extracted R-002 (single-view-image-to-3d-mesh-turnaround) from 2026-08-23-007 Decision 24 into .work-studio/precedent-ledger.md. Result refines, rather than repeats, R-001's finding: all 9 schema fields populated, with prompt_template/negative_constraints marked N/A (not [gap]) because this recipe's mechanism (image-to-3D mesh) has no text-prompt conditioning step at all -- unlike R-001, where a prompt exists but wasn't captured in Decision prose. The gap is specific to prompt-based recipes, not universal. This means a real harvester must distinguish 'no prompt exists' (N/A) from 'a prompt exists but wasn't recorded' ([gap]) rather than treating every recipe's missing prompt field the same way. |
| [system] | tools/precedent_harvest.py; verification run: python3 tools/precedent_harvest.py 2026-08-23-007 12 R-TEST | Built tools/precedent_harvest.py: a scaffolding tool, not a fully-automatic Recipe generator, per the tracer's own finding that field population requires judgment. Given a Work Object id and Decision number, it reuses the existing tools/ws/sections.py parse_decisions_table utility to extract the raw Decision record (result, scope, authorization, confidence, revisit_trigger, rationale) mechanically and reliably, and appends a scaffolded Recipe entry to .work-studio/precedent-ledger.md with judgment-requiring fields (purpose, applicable_when, avoid_when, inputs, operations, prompt_template, negative_constraints, verification, known_limits) explicitly marked [NEEDS INTERPRETATION] rather than guessed. Verified working: ran against 2026-08-23-007 Decision 12 (a falsified attempt, chosen deliberately as a real, different Decision than R-001/R-002 to prove the tool generalizes), confirmed correct mechanical extraction with zero fabrication, then removed the test entry (Decision 12 is a superseded/falsified attempt, not a real recipe candidate) to keep the ledger clean. No CLI subcommand wiring added (kept out of tools/ws/__main__.py) -- standalone script, smallest reversible footprint, one new file. |
| [system] | tools/precedent_harvest.py (read in full); ls on the session scratchpad directory; this session's own scratchpad-directory operating instructions | Live-question: checked whether tools/precedent_harvest.py can/should reference the scratchpad Python script that generated a recipe (to eventually fill R-001's prompt_template/negative_constraints gap). The harvester currently has no such capability -- only wo_id/decision_number. The referenced scripts (rembg_s004_mask.py, s004_masked_inpaint_v2_flux.py, etc.) do currently exist, verified via ls, but live in this session's scratchpad temp directory (C:\Users\Andre\AppData\Local\Temp\claude\...\scratchpad\), which is explicitly session-specific and not part of the governed repo or under git -- not durable. Adding a reference capability today would point at a path likely to vanish. The real fix is capture-at-generation (already required by plan sections 4/5.5): copy the generating script or its literal prompt into a durable, repo-tracked location at the moment a Decision is recorded, then have the harvester reference that durable copy. |
| [system] | This session's verification runs (2026-08-24), WO 2026-08-23-001 resume | V0 foundation verification (plan section 7 V0 table): (1) ws direction parses prose into a structured Direction object — ran on 'Keep the wide framing and silence, but make the recognition less obvious. Avoid melodrama.' → mode command, protect [wide framing, silence], change [less obvious], avoid [melodrama]; (2) ws scene-board rendered SC030 (WO 2026-08-23-004) to .work-studio/scene-board.html — Scenes: 1, all 4 layer tabs (interactive switching confirmed) + 7-beat Director Layer table confirmed in browser; (3) 4-layer screenplay + Director Layer present in SC030; (4) decision-log/versioning via ws append-history + append-artifact in service. V0 exit criteria met. |
| [system] | python -m unittest tests.test_scene_board_direction; git status --short; tools/ws/scene_board.py read | Focused regression test for the scene-board + direction V0 path added (tests/test_scene_board_direction.py): 10/10 pass — direction parsing (mode detection, Protect/Change/Avoid extraction, YAML form, single-line evidence serialization guard for Incident 2026-08-23-005) and scene-board projection (layer tabs, beat table, thesis, non-scene exclusion, empty state). Test exposed a pre-existing defect: _extract_thesis in tools/ws/scene_board.py used '**Key**: value' (colon outside bold) but real Scene WOs (SC030) use '**Key:** value' (colon inside bold), so Scene Thesis never rendered; fixed regex to '**Key:**'/'**Key**:', stripped trailing colon, re-verified — real SC030 scene-board.html now renders its thesis (Mara tries to hide recognition). Broader test_ws_cli.py: 253 tests, 3 pre-existing failures unrelated to this change (CHECK_REGISTRY drift in validate.py from other threads' dirty work; Windows backslash path-separator assertion in evidence-relations test; clock-second race in atomic-write parity test). V0 exit criteria met. |
| [gap] | ws transition audit (verify) | Unresolved [gap] entries exist in the Evidence ledger. Residual uncertainty should be reviewed before proceeding. |
| [system] | verify-release-evidence pass (2026-08-24), executed checks on the V0 foundation | verify-release-evidence (V0 foundation, meaningful/ordinary): claim 1 ws direction structures prose -> Direction object — verified on fresh prose 'Make the scene warmer and less cluttered. Keep the wide shots.' → mode direction, protect [wide shots], change [less cluttered]; claim 2 ws scene-board renders SC030 — verified: 4 layer tabs (UTF-8), 7 beat rows, Scene Thesis present ('Mara tries to hide recognition'), scene id 2026-08-23-004; claim 3 decisions/evidence via ws append-history/append-evidence — verified: SC030 Decision 1 + [testimony] Direction evidence, <br>-joined single-line rows (Incident 2026-08-23-005 fix visible in real ledger); claim 4 regression test — python -m unittest tests.test_scene_board_direction: 10/10 OK, exit 0. Failure/recovery: empty direction input cleanly rejected by argparse (exit 1, no partial write); empty scene-board shows 'No scenes found'; Incident 005 single-line guard regression-tested. Privacy/security: ordinary sensitivity, local-only reads of .work-studio/objects/**.md, no secrets/production/external access crossed. Gaps: station-1 DeepSeek V4 Flash Vision (Decision 10) is cloud/API, not part of the deterministic CLI path (not exercised here); PRESERVED/CHANGED reporting (plan section 7 V0 row) unbuilt, deferred by director's option-2 choice; beat→dialogue Story-Editor boundary is skill governance, not a CLI path. V0 exit criteria MET. No release claim. |
## Open questions

- Is the combined 1+3 framing right, or did the director mean to pursue 1 and
  3 as two parallel threads rather than one merged path? (Confidence: medium —
  see Decision 1.)
- Which practice-agnostic pieces of the shell (Context / Artifact / Inspector)
  are worth building before the creative-variant loop, versus after?
- Does "variant as artifact branch" reuse the existing design-asset record +
  Work Object versioning, or need a new record shape? (Deferred to the tracer.)

## Next move

V0 verified; V1 continuation opened as 2026-08-24-006 (responds_to 001).
001 itself may transition toward observe/close (outcome review) at the
director's call.

## Deliverables

- [Director Console — Implementation Plan](../../../deliverables/2026-08-23-001-director-console-implementation-plan.md) — plan synthesizing Decisions 1-3 + the director's system plan
- [Asset Recipe / Creative-Precedent Library — Design Critique & Recommendations](../../../deliverables/2026-08-23-001-asset-recipe-library-design-critique.md) — report: critique of the director's precedent-library suggestion, grounded in `2026-08-23-007`'s harvested recipes; §7 lists recommended plan revisions that need a decision before being written to canon

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-23T19:04:01Z — Activate as inquiry and enter explore for direction generation

- **State:** explore
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Director brought in a fully-formed Director Console product concept and invoked develop-idea. The concept is coherent but which version to pursue first, and how it relates to the existing Work Studio, is undecided — the divergence question this skill exists for. Captured the concept as testimony in Intent and moved to explore.
### 2026-08-23T19:06:42Z — Director selected combined Direction 1+3; recorded and moved to design for tracer

- **State:** design
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Director selected directions 1 (studio-skin frontstage) and 3 (creative-variant loop first practice). Recorded as Decision 1, combined into one path with the combination framing flagged medium-confidence and provisional. Moving to design so a tracer bullet can reality-test the riskiest assumption before any build.
### 2026-08-23T19:12:35Z — Recorded grilling outcomes (Decision 2): constraint narrowed, Blender/ComfyUI named, tracer redirected

- **State:** design
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Director asked to be grilled on the plan before proceeding. Serial-depth grilling over four pressure points established: artifact-first with real images, generation-first seeded by intent or upload, local instruments Blender+ComfyUI, and a narrowed (not broken) agent-agnostic constraint (file-first + model-agnostic retained; dependency-freeness reduced to a local-install requirement). Original three-pane tracer rejected as a false-green; riskiest assumption relocated to process orchestration of a local generative instrument. Director: 'record it'.
### 2026-08-23T19:16:09Z — Routed to tracer discipline; recorded Decision 3 (three-station render-to-lineage loop, pending on local ComfyUI)

- **State:** design
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Director routed to design-tracer and pasted their intended local stack (RTX 3080 10GB, Qwen3.5-9B Q4, Blender+ComfyUI+Ollama). Redesigned the tracer to three stations (LLM emits Direction JSON, ComfyUI renders, save+lineage), matching the director's LLM-translates/ComfyUI-generates split. Recorded as pending, not run: the paste describes an intended stack, not a confirmed running ComfyUI, so no render is claimed. Noted the 10GB GPU time-share as the concrete orchestration hard-middle.
### 2026-08-23T19:20:33Z — Tracer probe: ComfyUI running but no local image model; loop blocked on model install

- **State:** design
- **Status:** active
- **Actor:** claude-code
- **Rationale:** Probed the live local ComfyUI on :8188. Running (v0.33.3, RTX 3080, ~9.5GB free) but ALL image-model folders empty (checkpoints/diffusion_models/unet/text_encoders/clip/loras); only an audio VAE present. Cannot render locally. Install is cloud-leaning ComfyUI Desktop. Recorded as [system] evidence. Tracer cannot reach pass/fail until a local model exists; surfaced a 3-way fork (install local model / use cloud API nodes and reverse Decision 2 / director installs manually). Did not download anything unprompted.
### 2026-08-23T22:37:56Z — Produced implementation plan deliverable

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** Director requested an implementation plan grounded in the current Work Studio system. Classified as plan-type deliverable synthesizing Decisions 1-3 plus the director's updated 20-section system plan. Build order: V0 (writing+governance) through V6 (agentic dailies), each grounded in existing tools/ws infrastructure.
### 2026-08-23T22:51:01Z — Integrated 3D asset pipeline testimony into implementation plan

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** Director's 3D asset pipeline testimony woven into existing plan: new §5.4 Asset Production Department, expanded bounded Blender tools (mesh ops), expanded V3/V4 build phases, updated provenance.
### 2026-08-23T23:01:00Z — Integrated hardware-aware environment production workflow into implementation plan

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** Director's environment workflow testimony woven into plan: added 9-step environment production workflow with sequential GPU load/unload cycle, four asset tiers (hero/modular/2.5D/atmosphere), production rules (camera-proves-existence, cameras before assets), modular kit assembly, environment language extraction, concrete V4 environment pipeline tracer (one alley + three shots), updated GPU time-share section with Hunyuan3D and environment cycle, updated provenance.
### 2026-08-23T23:16:01Z — Resolved Decision 3 image model blocker

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** Flux Dev FP8 (flux1-krea-dev_fp8_scaled.safetensors) found installed in ComfyUI shared diffusion_models folder. V4 ComfyUI integration is no longer blocked. Updated implementation plan: §1.7 hardware, V4 prerequisite, §10 blockers, provenance.
### 2026-08-23T23:48:17Z — Align next_action to resolved Decision 3 blockers; route back to design

- **State:** design
- **Status:** active
- **Actor:** conductor
- **Rationale:** Director requested routing back to Director Console design. SC030 V0 tracer completed (Direction-to-evidence pipeline validated). Evidence ledger now shows both Decision 3 blockers resolved: ComfyUI 0.33.3 running locally on :8188, and Flux Dev FP8 local diffusion model installed (flux1-krea-dev_fp8_scaled.safetensors). Stale Next-move fork (install model / use cloud / manual install) is obsolete; no local-model decision remains. next_action updated to reconcile the runnable tracer design and run the three-station loop.
### 2026-08-23T23:48:34Z — Sync body Next move to aligned next_action

- **State:** design
- **Status:** active
- **Actor:** conductor
- **Rationale:** Body ## Next move updated to match frontmatter next_action: obsolete no-model fork replaced with reconcile-and-run Decision 3 tracer.
### 2026-08-24T19:45:43Z — Recorded Decision 4: split taste-system suggestion, adopt Aesthetic Canon now, defer Taste Evaluator

- **State:** design
- **Status:** active
- **Actor:** director
- **Rationale:** Pressure-tested via alawas-thinking-pressure-test-decision: WO 2026-08-23-007's revision-lane tracer shows the variant-generation pipeline not yet reliably distinguishing outputs (Decisions 6/7 fail, 8 pending), so Taste Evaluator/Aesthetic Critic/pairwise-ranking machinery is deferred until that passes; the Aesthetic Canon has no such dependency and is adopted now.
### 2026-08-24T22:08:08Z — Produced report deliverable: Asset Recipe / Creative-Precedent Library design critique

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** Director asked for critique of a creative-precedent-library suggestion and a plan revision, grounded on the closed 2026-08-23-007 mechanisms. Produced a report-type deliverable (not plan-type): endorses recipe/prompt separation, first-class Revision, three-layer epistemic description, and the anti-homogenization retrieval rule; critiques the greenfield framing (should harvest closed-WO decision trails, which already contain 2 validated recipes + ~6 counter-examples), the reinvention of 7 existing primitives (reuse, don't clone), the ungoverned status lifecycle (owned by track-components), the success-counter ossification vector, and the unbudgeted image-similarity VRAM cost (reuse installed sigclip_vision). Deliverable §7 lists recommended console-plan revisions as PROPOSALS only -- editing the canonical plan to add this unaccepted architecture needs a separate decision (pressure-test-decision), so the plan was NOT modified.
### 2026-08-24T22:13:54Z — Folded report §7 revisions into canonical console plan (Decision 5)

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** Per Decision 5 (director: 'fold the §7 revisions into the plan'), edited 2026-08-23-001-director-console-implementation-plan.md with five changes: §5.4 gained the two [system]-verified harvested recipes (segmentation-masked regional revision; Hunyuan3D single-view mesh for turnaround identity); new §5.5 Creative Precedent Library (harvest-first, three new object types Recipe/Revision/TastePrinciple referencing existing primitives, mandatory anti-homogenization Reference Pack, staged build order, known-unsolved as first-class status); §4 Art/Asset Director boundary now requires capture-at-generation; §6.4 notes PRESERVED/CHANGED/PROPOSED IS the Revision capture format; §2.4 records the retrieval-embedding VRAM constraint and sigclip_vision reuse. Plan header updated to trace these additions to Decision 5 so the plan still 'authors nothing new'.
### 2026-08-24T22:17:26Z — Decision 6 recorded and plan §5.5 corrected: ws relation/ws graph insufficient, storage model switched to Component Ledger pattern

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** Verified Decision 5's flagged gap directly against the CLI: ws relation add requires both endpoints to be full Work Objects and has no protects/changes edge semantics, falsifying the plan's original claim that the NetworkX projection would traverse Recipe/Revision/TastePrinciple 'for free.' Corrected by pointing at the studio's own existing, working precedent for this exact problem shape -- the Component Ledger (component-ledger.md, ADR 0014) -- which is a hand/harvester-maintained Markdown index with prose-declared edges, not a ws-relation graph. Edited plan §5.5 storage paragraph, the v0 build-order row, and the plan header to trace to Decision 6.
### 2026-08-24T22:20:00Z — Live-question answered: Component Ledger + selective ws relation, not a full-WO-per-recipe alternative

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** Director asked whether to use the Component Ledger alone, hybridize it with ws relation/ws graph, or abandon it for a full-Work-Object-per-Recipe model traversed natively by ws relation/ws graph/NetworkX. Answered: keep the Component Ledger as the unavoidable primary storage for fine-grained Recipe/Revision/TastePrinciple entries (ws relation categorically cannot hold sub-WO edges regardless of volume), and additionally use ws relation at the Work-Object level for provenance links between recipe-originating and recipe-consuming Work Objects, where that granularity is exactly what ws relation is built for. Rejected the full-WO-per-recipe option: it contradicts the capture-at-generation requirement (plan section 4) that Revisions be lightweight and automatic, would force a consequence/sensitivity judgment call and full 7-section schema per recipe, floods active.md/the objects namespace, and still would not fix the missing protects/changes edge vocabulary even if adopted.
### 2026-08-24T22:23:45Z — Decision 7 recorded: tracer bullet R-001 mostly validates harvesting, one real gap found

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** Hand-extracted R-001 from 2026-08-23-007 Decision 16 into .work-studio/precedent-ledger.md. 6/9 schema fields populated cleanly from Decision prose alone; 2 fields (prompt_template, negative_constraints) genuinely gapped -- literal prompt text lives only in scratchpad scripts, not Decision narrative. This is a mixed-but-majority-pass tracer result: harvesting is viable for most of the schema, with one specific, now-named limitation rather than a wholesale failure.
### 2026-08-24T22:26:10Z — Decision 8 recorded: second extraction (R-002) refines the harvester requirement

- **State:** design
- **Status:** active
- **Actor:** system
- **Rationale:** R-002's clean N/A result (vs. R-001's genuine [gap]) shows a harvester must distinguish 'mechanism has no prompt' from 'prompt exists but uncaptured'. The tracer bullet has now produced two informative, distinct results across two recipe kinds (2D image revision, 3D mesh generation) -- enough evidence to design the real harvester's field-population logic, though a genuinely prompt-based third extraction would still be needed to confirm whether R-001's specific gap is systematic across ALL prompt-based recipes, not just this one instance.
### 2026-08-24T22:29:26Z — Route to alawas-engineering-implement-bounded-change per accepted tracer exit criteria (Decisions 7-8)

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Director: 'route to implement-bounded-change.' Tracer bullet exit criteria met: two hand-extractions across two recipe kinds gave enough evidence to design the real v0 harvester's field-population logic (distinguishing N/A from [gap] for prompt fields).
### 2026-08-24T22:30:18Z — Decision 9 recorded: v0 harvester tool built and verified

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** tools/precedent_harvest.py implemented and verified against a real, distinct Decision (2026-08-23-007 Decision 12), then the test entry removed. Bounded implementation matches the accepted design: mechanical extraction only, judgment-requiring fields explicitly flagged, no CLI wiring, one new file.
### 2026-08-24T22:39:21Z — Live-question answered: script-reference capability not yet worth adding; root fix is durable capture-at-generation

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Director asked whether the harvester could reference the generating Python script to fill R-001's prompt gap. Answered: the capability is trivial to add but would point at files in this session's ephemeral scratchpad temp directory, not the governed repo -- not durable. The real prerequisite (already implied by plan sections 4/5.5's capture-at-generation requirement) is committing the generating script or its literal prompt into a durable, repo-tracked location at Decision-recording time; only then does a harvester reference add real value.
### 2026-08-24T22:43:53Z — Decision 3 resolved: pass, retroactively validated by 2026-08-23-007's real execution

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Director corrected an in-progress redundant tracer attempt (a disconnected new prose-intent test) and confirmed the three-station loop is already validated by the ~24 real executions in the closed child WO 2026-08-23-007, run on the same local stack (ComfyUI + Ollama/Qwen3.5, both confirmed present). Decision 3 updated from pending to pass on that basis, with one honest caveat recorded: the specific isolated 'local LLM structures prose into Direction JSON' sub-step wasn't separately tested in 007 (the orchestrating agent wrote structured directions directly there), though the capability is confirmed present.
### 2026-08-24T22:50:39Z — Resumed by ID; synced stale body Next move to frontmatter next_action

- **State:** build
- **Status:** active
- **Actor:** conductor
- **Rationale:** Resume: frontmatter next_action points at the V0 foundation build (plan section 7) but body ## Next move still described the obsolete reconcile-and-run-Decision-3 step. Decision 3 was resolved pass at 2026-08-24T22:43:53Z. Synced body to match; routing to implement-bounded-change for the V0 foundation build.
### 2026-08-24T22:52:31Z — Decision 10 folded into the plan: DeepSeek V4 Flash Vision replaces Qwen3.5/Ollama

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Per Decision 10, edited the plan in five places: section 1.7 hardware/instruments (replaced Local LLM entry with DeepSeek V4 Flash Vision, named model/endpoint/limits, flagged as cloud not local); section 2.4 GPU time-share diagram (removed the local-LLM VRAM-load step, both reasoning models now cloud-only); section 8 Technical Stack table (Local LLM row replaced with a Vision/critique LLM row); section 11 Supersession Notes (recorded that the offline-fallback local LLM is itself now superseded); plan header updated to trace to Decision 10 and to correct Decision 3's stale 'pending' reference to its actual pass result. This is a deliberate, director-confirmed tradeoff: the plan no longer has a fully local, no-network text-reasoning fallback.
### 2026-08-24T23:21:22Z — Director authorized focused regression test for the scene-board + direction V0 path

- **State:** build
- **Status:** active
- **Actor:** director
- **Rationale:** Director selected option 2 from the resume decision frontier: add a focused regression test for the Director Console V0 foundation (scene-board projection + direction parsing), writing to tests/ outside .work-studio/ with explicit go-ahead. V0 verification evidence from this session (direction parsing, scene-board render) recorded in the Evidence ledger.
### 2026-08-24T23:25:49Z — Focused regression test added; pre-existing thesis-extraction defect found and fixed

- **State:** build
- **Status:** active
- **Actor:** system
- **Rationale:** Director authorized (option 2): focused regression test for the scene-board + direction V0 path. Added tests/test_scene_board_direction.py (10 tests, all pass). The test exposed a real pre-existing defect in the V0 scene-board projection: _extract_thesis regex '**Key**: value' never matched the actual data format '**Key:** value' (colon inside bold), so Scene Thesis never rendered — confirmed on real SC030 data, now fixed in tools/ws/scene_board.py and re-verified. Broader test_ws_cli.py has 3 pre-existing failures (CHECK_REGISTRY drift from other threads' dirty work; Windows path-separator expectation; clock-second race in atomic-write test) — all unrelated to this change (validate.py/atomic.py unmodified, scene_board.py not imported by that suite). V0 exit criteria remain met.
### 2026-08-24T23:28:28Z — Director: 'transition to verify'

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** V0 foundation build complete and verified: direction parsing, scene-board projection (regression-guarded, 10/10 tests), 4-layer screenplay in SC030, decision-log/versioning all operational; V0 exit criteria met. Director accepted the recommendation to transition out of build into verify.
### 2026-08-24T23:33:24Z — verify-release-evidence pass: V0 exit criteria met (director: 'route to verify')

- **State:** verify
- **Status:** active
- **Actor:** system
- **Rationale:** Executed verify-release-evidence on the V0 foundation (director routed to verify). All four claims verified with direct evidence: direction parsing, scene-board render (layers/beats/thesis), decisions/evidence via ws append-*, regression test 10/10. Failure behavior exercised (empty input clean rejection, empty-board state, Incident 005 single-line guard). Gaps named, not hidden: station-1 cloud LLM (Decision 10) outside the deterministic CLI path; PRESERVED/CHANGED reporting deferred by director's choice; beat→dialogue boundary is skill governance. V0 exit criteria MET; no release claim made.
### 2026-08-24T23:37:23Z — Director: 'open a next work slice' → opened 2026-08-24-005 (PRESERVED/CHANGED reporting)

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Director chose 'open a next work slice' and selected PRESERVED/CHANGED reporting (the last unbuilt plan section 7 V0 row). Opened successor change Work Object 2026-08-24-005 (responds_to 001, registered supporting in active.md, state design, Decision 1 scopes it to PRESERVED/CHANGED only). 001 remains at verify; the observe/close decision is still open at the director's call.
### 2026-08-25T00:05:26Z — Director: 'create a new work object for V1 production objects' → opened 2026-08-24-006

- **State:** verify
- **Status:** active
- **Actor:** director
- **Rationale:** Director opened the V1 Production Objects slice as the further slice after V0. Created project Work Object 2026-08-24-006 (responds_to 001, registered supporting, state design). Decision 1 scopes it to the plan section 7 V1 table and flags the riskiest assumption: whether existing schema + ws relation/ws transition can represent the Project → Sequence → Scene → Beat → Shot hierarchy and shot-specific states without a material schema change.
## artifacts

- `.work-studio/deliverables/2026-08-23-001-director-console-implementation-plan.md` (fingerprint: `21e5478fa8ab`, commit: uncommitted at record time) — Implementation plan: Director Console grounded on the current Work Studio system, synthesizing Decisions 1-3 and the director's updated 20-section system plan
- `.work-studio/design-assets/aesthetic-canon.asset.md` (fingerprint: `ed4c76182dd5`, commit: uncommitted at record time) — Draft Aesthetic Canon design asset (Decision 4): dimension scaffold with unconfirmed candidate seed values, structural only until director confirms per-dimension prefer/avoid
