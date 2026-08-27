# Asset Recipe / Creative-Precedent Library — Design Critique & Grounded Recommendations

> **Deliverable type:** report
> **Originating Work Object:** `2026-08-23-001` (Director Console) — state `design`
> **Date:** 2026-08-24
> **Author:** Andre (andrelawas35@gmail.com)
> **Prompted by:** Director's design suggestion for a "creative precedent system"
> (recorded here as `[testimony]`), evaluated against the current Work Studio
> and the console implementation plan.

**What this document is and is not.** This is a *report*: it critiques a
proposed architecture and recommends how it would (or would not) fit the
existing system. It does **not** rewrite the canonical console implementation
plan (`2026-08-23-001-director-console-implementation-plan.md`). Section 7
below lists *recommended* plan revisions as proposals; folding any of them into
the canonical plan is a material change that needs a separate director decision
(route: `alawas-thinking-pressure-test-decision`), because the plan document by
rule "synthesizes only already-accepted material and authors nothing new."

---

## 1. The one-line finding

`[inference]` The suggestion is strong and largely correct, but it is framed as
a **greenfield build** when the most important fact is that **the studio already
generates this exact data as a byproduct of governed work and already owns most
of the primitives** — it simply never harvests them. The single closed Work
Object `2026-08-23-007` is, in raw form, a working creative-precedent graph: two
validated recipes, ~six falsified counter-examples, full revision lineage, and
provenance-tagged evidence. The right first move is **harvest, not construct**.

---

## 2. What the suggestion gets right (keep these)

`[testimony]` → `[inference]` assessment of each:

1. **Separate Recipe from Prompt.** Correct and important. A prompt is one
   ingredient; a recipe is method + tool + controls + sequence + applicability.
   `[system]` `2026-08-23-007` proves this directly: "segmentation-masked
   revision" (Decision 16) and "single-view image-to-3D mesh" (Decision 24) are
   recipes whose *prompt* was almost incidental — the method (rembg mask →
   `VAEEncodeForInpaint`; Hunyuan3D → Blender camera rotation) was the reusable
   asset.

2. **Make Revision first-class (bounded transformation with protect/change/
   avoid).** Correct, and it is *already the studio's native shape*. `[system]`
   The Direction object in the console plan §2.2 already has
   `basis/protect/change/desired_effect/authority`. The suggestion's Revision
   object is that same structure applied to an artifact pair. This is a rename
   away from something that already exists.

3. **Three description layers (observable / interpretation / intent-judgment)
   must not collapse.** Correct, and `[system]` this is *already the studio's
   enforced epistemic rule*: observable = `[system]`, interpretation =
   `[inference]`, intent/judgment = `[decision]`/`[testimony]`. The suggestion's
   "never collapse low-saturation into emotionally-restrained" is the existing
   provenance discipline, not a new rule to invent.

4. **Anti-homogenization retrieval rule (2 close + 1 counterexample + 1
   different-but-successful).** This is the single best idea in the proposal and
   has no current equivalent. `[system]` The studio has a *diagnosis* skill
   (`alawas-thinking-diagnose-homogenization`) but nothing that enforces
   diversity at *retrieval* time. Keep this exactly as proposed.

5. **Precedents inform, never dictate; taste must not ossify into policy.**
   Correct, and `[system]` it mirrors the studio's spine rule "LLMs propose;
   the human establishes canon" (plan §0, §1.2). The proposed flow
   `precedents → evidence → interpretation → proposal → director judgment` is
   the Agreement Loop with a retrieval step bolted on the front.

6. **Status maturity states + `known_limits`.** Correct in spirit.

---

## 3. Critiques — where the suggestion needs correcting

### 3.1 It reinvents primitives the studio already has (biggest issue)

`[system]` The proposal introduces ten object types. Mapped against what
already exists:

| Proposed object | Already exists as | Verdict |
|---|---|---|
| Intent | Work Object `## Intent` + Direction object (plan §2.2) | **reuse, don't rebuild** |
| Outcome | `[decision]` records + History | **reuse** |
| Evidence | tagged Evidence ledger (`[system]`/`[inference]`/…) | **reuse** |
| Critique | PRESERVED✓/CHANGED Δ/PROPOSED? pattern (plan §1.3, §6.4) | **reuse** |
| Judgment | `[decision]` with authorization/scope | **reuse** |
| Decision | first-class structured Decision record | **reuse** |
| Artifact | design-asset record (plan §1.5, §5.4) | **reuse (extend)** |
| **Recipe** | — nothing equivalent | **genuinely new** |
| **Revision** (as first-class delta) | partial (Direction object) | **new: promote to a stored artifact-pair** |
| **Taste Principle** | — nothing equivalent | **genuinely new** |

`[inference]` **Recommendation:** build the three genuinely-new objects
(Recipe, Revision-as-stored-delta, Taste Principle) and *reference* the existing
seven rather than cloning them. Cloning them would fork the source of truth —
you would have two "Judgment"-like records that can disagree, which is exactly
the failure the studio's single-Work-Object-of-record model exists to prevent.

### 3.2 It's framed as build-from-empty; it should be harvest-from-closed-WOs

`[system]` `2026-08-23-007` closed with a decision trail that already contains:
- **2 validated recipes** — segmentation-masked regional revision (Decision 16);
  single-view image-to-3D mesh for turnaround identity (Decision 24).
- **~6 falsified counter-examples** — global img2img revision (Decision 11),
  hand-drawn masks soft/hard (Decisions 12/13/15), FLUX.1-Fill engine swap
  (Decision 14), negative-prompt-at-cfg-1.0 (Decision 18), whole-frame mask at
  partial denoise (Decision 22), Redux strength-tuning for viewpoint
  (Decision 23).
- **Full revision lineage** — each Decision records source → result, what
  changed, what was protected, under what conditions it held or broke.

`[inference]` **Recommendation:** the library's v1 ingestion target is *closed
Work Objects*, not future work. It starts non-empty on day one by importing
`2026-08-23-007`. This also means the capture cost is near-zero for anything
already governed — the recipes are a *projection* of decision trails, the same
way `command-center.html` is a projection of Work Object data (plan §1.6).

### 3.3 The status lifecycle has no owner — but a candidate owner already exists

`[system]` The proposal lists `experimental → candidate → validated → preferred
→ deprecated → superseded` but no governance for the transitions. `[system]`
The studio already has `alawas-design-track-components` ("register, sweep,
grill, cascade, retire … returns ledger and inbox mutation proposals") and
`alawas-governance-maintain-working-method` ("trials, revises, or retires a
bounded working method"). `[inference]` **A Recipe is a durable component.**
Recommendation: do not invent a new governance mechanism; a Recipe's status
transitions are owned by `track-components`, and a Recipe promoted to a general
studio method (not just an asset recipe) escalates to `maintain-working-method`.

### 3.4 `successful_uses: 7 / failed_uses: 2` is an ossification vector

`[inference]` The director already flags the ossification danger and adds the
anti-homogenization rule — good. But a raw success counter is a number that
*looks like authority*, and models (and humans) rank by whatever number is
present. **Recommendation:** store the counter but **never surface it as a
ranking or sort key** in a Reference Pack. Surface `known_limits` and the
counter-examples instead. Tie this to `alawas-thinking-diagnose-homogenization`
as the review that fires if a single recipe starts dominating accepted outputs.

### 3.5 `find_similar_artifact(image)` has a real, unbudgeted hardware cost

`[system]` Image-similarity retrieval needs a vision-embedding model resident or
invoked. `[system]` The 10 GB VRAM is already fully contended — `2026-08-23-002`
records two TDR driver crashes under sustained load, and the plan §2.4 mandates
sequential model load/unload. `[inference]` **Recommendation:** v1 ships
`find_by_intent` only (text/structured query — cheap, no GPU). Defer
`find_similar_artifact`; and when it lands, reuse the **`sigclip_vision`
model already installed for Flux Redux** (`2026-08-23-007` Decision 20) rather
than adding a new embedding model to an already-tight VRAM budget.

### 3.6 Studio vocabulary drifts without an owner

`[inference]` "too resolved / airless / earned / unearned" is a controlled
vocabulary; controlled vocabularies fragment (three phrasings for one idea)
unless owned. **Recommendation:** seed it *small*, and treat each vocabulary
term as a durable component under `track-components` — so "airless" has one
canonical definition, provenance, and retirement path, exactly like a design
token.

### 3.7 The make-or-break is capture discipline, and the proposal is silent on it

`[inference]` Every precedent-graph system that fails, fails at *capture time*:
tags applied retroactively are inconsistent, and inconsistent tags make the
graph queries ("recipes that produced accepted artifacts for restrained grief")
return garbage. **Recommendation:** capture must be enforced at generation time
by the **Art / Asset Director specialist's skill boundary** (plan §4), not left
to later cleanup. A generation that doesn't record intent + recipe + protect/
change at the moment it runs simply doesn't enter the library.

---

## 4. The corrected object model (minimal, grounded)

`[inference]` Three new object types; everything else is an existing primitive
referenced by ID.

```
NEW:
  Recipe          method + tool + controls + sequence + applicable_when/avoid_when
                  + verification + status + known_limits + provenance(Decision IDs)
  Revision        stored artifact-pair delta: source→result, change/protect/avoid,
                  method=Recipe ID, outcome=Decision ID
  TastePrinciple  a durable, director-authored preference, provenance = Judgment IDs

REFERENCED (already exist — link by ID, never clone):
  Work Object / Intent section / Direction object   (intent)
  design-asset record                               (artifact)
  Evidence ledger entry                             (evidence, tagged)
  Decision record                                   (judgment/outcome/decision)
  History entry                                     (chronology)
```

`[inference]` Recipe, Revision, and TastePrinciple are stored as
Markdown+YAML in `.work-studio/` (house style, plan §8), registered in the
component ledger (`track-components`), and traversed via `ws relation` / `ws
graph` (`[system]` existing commands, plan §3.1). The NetworkX projection the
director already has becomes the precedent-graph query layer for free.

---

## 5. Retrieval: the Reference Pack (endorsed, with the diversity rule mandatory)

`[inference]` Endorse the Reference-Pack-not-whole-library approach. The pack is
assembled by a rule that is **not optional**:

```
Reference Pack = 2 close precedents
               + 1 counter-example (a falsified recipe / rejected artifact)
               + 1 different-but-successful approach
               + relevant TastePrinciples (as tension, not instruction)
```

`[inference]` The counter-example slot is why harvesting *failed* Decisions
(§3.2) matters as much as harvesting successes — without a stocked failure
shelf, the diversity rule has nothing to draw the counter-example from.

---

## 6. Staged build order (grounded in current capability)

`[inference]`

- **v0 — Harvest.** Write a projection that reads closed Work Objects' Decision
  trails and emits Recipe + Revision records. Target: ingest `2026-08-23-007`.
  No new runtime, no GPU. Proves the ontology against real data.
- **v1 — `find_by_intent` + Reference Pack.** Structured/text retrieval over the
  harvested records, with the mandatory diversity rule. No GPU.
- **v2 — Capture-at-generation.** The Art/Asset Director skill writes a Recipe/
  Revision record at the moment each generation runs (fixes §3.7).
- **v3 — `find_similar_artifact`.** Reuse the installed `sigclip_vision`
  embeddings; obey the sequential-VRAM discipline.
- **v4 — TastePrinciple governance.** `track-components` owns status lifecycle;
  `diagnose-homogenization` fires on single-recipe dominance.

---

## 7. Recommended console-plan revisions (PROPOSALS — not yet written to canon)

`[inference]` If the director accepts these, they need a decision before the
canonical plan (`2026-08-23-001-director-console-implementation-plan.md`) is
edited:

1. **§5.4 Asset Production Department** — add the two harvested recipes from
   `2026-08-23-007` as the department's first validated entries:
   *segmentation-masked regional revision* (rembg → `VAEEncodeForInpaint`) and
   *single-view image-to-3D mesh for turnaround identity* (Hunyuan3D →
   Blender camera rotation). Both are `[system]`-verified on the 10 GB machine.
2. **New subsection §5.5 (or §3.5) — Creative Precedent Library** — the object
   model from §4 above, explicitly built on existing primitives, with the
   harvest-first build order from §6.
3. **§4 Specialist Profiles** — extend the Art/Asset Director boundary to
   *require* capture-at-generation (§3.7), and assign Recipe/TastePrinciple
   status governance to `track-components` (§3.3).
4. **§6.4 Revision reporting** — note that the PRESERVED/CHANGED/PROPOSED
   report is the capture format for a Revision record (they are the same object
   viewed two ways).
5. **§2.4 GPU time-share** — record the retrieval-embedding VRAM constraint
   (§3.5) and the `sigclip_vision`-reuse decision so v3 doesn't add a model.

---

## 8. Gaps carried into this report (stated, not papered over)

- `[gap]` Whether `ws relation`/`ws graph` can express the full precedent-graph
  edge set (`realized_by`, `failed_for`, `protects`, `supports`) is asserted
  from the plan's `[system]` claims, **not independently verified** against the
  live CLI schema. Verify before committing v0.
- `[gap]` The two open flaw categories from `2026-08-23-007` (S002 unwanted
  geometry, S005 whole-frame revision) are tracked in `2026-08-24-003` and are
  **not yet recipes** — they are open problems. The library must represent
  "known-unsolved" as a first-class status, not omit them.
- `[gap]` No cost/latency measurement exists for assembling a Reference Pack at
  director-interaction time; assumed cheap for text retrieval, unmeasured.

---

## Provenance

- `[testimony]` Director's creative-precedent-system suggestion (2026-08-24)
- `[system]` `2026-08-23-007` (closed): Decisions 11–24, validated recipes 16 & 24,
  falsified counter-examples 14/18/22/23, revision lineage
- `[system]` `2026-08-23-002`: GPU TDR-crash evidence, sequential-VRAM discipline
- `[system]` `2026-08-24-003`: spun-off open gaps S002/S005
- `[system]` Console plan `2026-08-23-001-director-console-implementation-plan.md`
  §0, §1.2–1.6, §2.2, §2.4, §3.1, §4, §5.4, §6.4, §8
- `[system]` Studio skills: `alawas-design-track-components`,
  `alawas-governance-maintain-working-method`,
  `alawas-thinking-diagnose-homogenization`
- `[inference]` All critiques, the corrected object model, staged build order,
  and recommended plan revisions are this report's synthesis — director
  judgment required before any become canon
