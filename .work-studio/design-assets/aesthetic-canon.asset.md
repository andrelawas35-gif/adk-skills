# asset.design.aesthetic-canon Asset Record

**Work Object:** `2026-08-23-001`
**Pipeline:** `references/DESIGN-ASSET-PIPELINE.md`
**Status:** draft
**Asset ID:** `asset.design.aesthetic-canon`
**Asset kind:** creative-canon (novel kind — not a UI token-set or
component-family; see Verification Notes)
**Source of truth:** this asset record
**Projection status:** projections may read this record; they are read-only
and must not be edited as asset truth.

## Asset Summary

An explicit, reusable vocabulary of aesthetic taste for the Director
Console's creative work — composition, camera, light, color, texture,
performance, environment, motion, narrative, and finish — stated as concrete
prefer/avoid criteria per dimension rather than adjectives like "cinematic"
or "moody" that every model and every specialist would interpret
differently.

This is the **Aesthetic Canon** layer adopted in Decision 4 of Work Object
`2026-08-23-001`: the only layer of the submitted three-layer taste system
(canon / evaluator / learned adapters) adopted so far. The Taste Evaluator
(VLM/API-LLM critique, pairwise ranking, an Aesthetic Critic specialist) and
any learned adapter (LoRA, reward model) remain explicitly deferred — see
that Decision's revisit trigger — because they depend on the variant
generation pipeline in `2026-08-23-007` producing reliably distinguishable
outputs, which is not yet demonstrated.

Any specialist skill (Story Editor, Character/Performance Director,
Animation Director, Cinematographer, Art/Asset Director, Sound Director,
Critic/Continuity — per the Director Console implementation plan §4) may
read this record to ground its own judgment. It is a reference document, not
an automated gate: nothing in the current system enforces these criteria
against generated output. That enforcement is exactly what the deferred
Taste Evaluator would add later.

## Dimensions

Each dimension below is a **structural scaffold**, not a filled-in canon.
No `prefer` / `avoid` entry in this record has been confirmed by the
director as `[testimony]`. Populating them is director judgment, not
something this record can supply on its own — filling them in with invented
preferences would misrepresent inference as decided taste.

The rows carry candidate seed values drawn from the original taste-system
suggestion (pasted into this Work Object's grilling, 2026-08-24), tagged
`[inference]` throughout, offered only as a starting point to accept, edit,
or discard — not as anyone's confirmed preference.

| Dimension | Question it answers | Prefer (confirmed) | Avoid (confirmed) | Candidate seed `[inference]` — unconfirmed |
|-----------|---------------------|---------------------|---------------------|---------------------------------------------|
| Composition | Centered or asymmetric? Dense or sparse? Stable or unstable? | *(none yet — `[gap]`)* | *(none yet — `[gap]`)* | prefer: strong negative space, asymmetrical balance, depth through foreground occlusion · avoid: centered hero framing, perfectly resolved compositions |
| Camera | Observational or expressive? Wide or compressed? Eye-level or low? | *(none yet — `[gap]`)* | *(none yet — `[gap]`)* | *(no seed offered — the source material did not give camera-specific examples)* |
| Light | Motivated or stylized? Hard or soft? Practical-heavy? | *(none yet — `[gap]`)* | *(none yet — `[gap]`)* | prefer: motivated practical sources, localized highlights, deep but readable shadows · avoid: global beauty lighting, excessive rim lights, glossy commercial illumination |
| Color | Saturated or restrained? Warm/cool relationship? | *(none yet — `[gap]`)* | *(none yet — `[gap]`)* | *(no seed offered)* |
| Texture | Clean, matte, dirty, painterly, photographic? | *(none yet — `[gap]`)* | *(none yet — `[gap]`)* | *(no seed offered)* |
| Character / Performance | Readable emotion or ambiguous? Posed or observed? | *(none yet — `[gap]`)* | *(none yet — `[gap]`)* | prefer: restrained emotional legibility, eyes doing more than mouth, incomplete gestures · avoid: obvious facial signaling, exaggerated expressions |
| Environment | Pristine or lived-in? Orderly or layered? | *(none yet — `[gap]`)* | *(none yet — `[gap]`)* | *(no seed offered)* |
| Motion | Smooth or irregular? Restrained or energetic? | *(none yet — `[gap]`)* | *(none yet — `[gap]`)* | *(no seed offered)* |
| Narrative | Explicit or suggestive? Heroic or vulnerable? | *(none yet — `[gap]`)* | *(none yet — `[gap]`)* | *(no seed offered)* |
| Finish | Commercial polish or tactile imperfection? | *(none yet — `[gap]`)* | *(none yet — `[gap]`)* | *(no seed offered)* |

## Anti-taste (cross-dimension disqualifiers)

Candidate seed values only, `[inference]`, unconfirmed — offered because the
source material treated these as immediate disqualifiers rather than
per-dimension preferences:

- glossy advertising finish
- overclean skin
- gratuitous orange/teal grade
- centered subject with obvious hierarchy
- fake cinematic bloom
- emotional overstatement
- busy backgrounds with equal contrast everywhere
- unnecessary neon
- excessive rim lighting
- symmetry without narrative reason

None of these are confirmed. They sit here as a candidate list to accept,
edit, or discard in one pass, the same as the per-dimension seeds above.

## Reference library (structure only — empty)

The source suggestion proposed annotating each visual reference with what it
is used for and what should not be copied from it, rather than a plain
mood-board folder:

```text
reference_NNN
Use for: <specific qualities this reference demonstrates>
Do not copy: <specific qualities that should not transfer>
```

No references have been added yet. This structure is recorded so that when
the director does add references, they land in this shape rather than as
undifferentiated mood-board images.

## Provenance

- `[decision]` Decision 4, Work Object `2026-08-23-001`: adopts this Aesthetic
  Canon layer now; defers Taste Evaluator, Aesthetic Critic specialist, and
  pairwise-preference recording until `2026-08-23-007`'s revision-lane
  tracer passes.
- `[testimony]` Director's taste-system suggestion (pasted 2026-08-24,
  grilled and pressure-tested in Work Object `2026-08-23-001`): source of
  the dimension list and the candidate seed values marked `[inference]`
  above. The suggestion itself did not assert these seed values as this
  director's confirmed taste — they were illustrative examples in the
  submitted proposal, which is why they are recorded as unconfirmed
  candidates, not canon.
- `[gap]` No dimension's `prefer` / `avoid` columns are confirmed. This is
  the open item blocking this asset from moving past `draft` status.

## Lifecycle

| Step | Owning skill | Evidence |
|------|--------------|----------|
| Intake and identity | `design-manage-assets` | Asset ID, kind, source of truth, lifecycle status (`draft`), and current frontier (dimension confirmation) recorded here. |
| Confirming candidate seed values, or replacing them with the director's own | `design-manage-assets` routes to whichever skill the director is working in when the confirmation happens — most likely inline in a future Direction or grilling session, not a dedicated skill invocation. |
| Composing this into a governed design-system artifact (if it ever needs tokens/themes rather than prose criteria) | `design-compose-design-system` | Not yet routed — this record is prose criteria, not tokens, and may never need to become one. |

## Verification Notes

- `creative-canon` is not one of the asset kinds seen elsewhere in this
  pipeline (`token-set`, `component-family`) — those govern UI design
  systems, while this governs narrative/cinematic taste for generated
  creative work. Recorded as a novel kind rather than forced into an
  ill-fitting existing one. If `design-manage-assets` classifies this
  differently on its next pass, that classification supersedes this note.
- This record does not enforce anything. No specialist skill or pipeline
  step currently checks generated output against these criteria — that
  enforcement is the deferred Taste Evaluator's job, not this asset's.
- Do not treat the candidate seed values as accepted canon in any
  specialist prompt or Direction object until the director confirms,
  edits, or replaces them per dimension.

## Rollback

Delete this draft asset record if it has not been accepted. If accepted
later (dimensions confirmed), retire or revise it through the governing
Work Object (`2026-08-23-001` or a successor) rather than editing lineage
out of it.
