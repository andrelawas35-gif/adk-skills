# S005 — Turnaround Rendering Consistency (before-image prompt)

**Case:** Turnaround Rendering Consistency — every view in a reference set needs one coherent rendering style and neutral, consistent lighting so image-to-3D generation reads material and form consistently.
**Shared subject:** The market lamp prop, rendered across its reference set.
**Engine:** Flux.1-Krea (`flux1-krea-dev_fp8_scaled.safetensors`), no LoRA.

## Before-image prompts (paste into your image generator)

**View A (reference, held constant):**
```
Product reference photo of an oxidized brass market lamp, cracked glass panes, hanging chain, three-quarter view, flat neutral studio lighting from one consistent overhead source, plain light-grey background, photoreal material rendering.
```

**View B (the flawed generation to critique):**
```
Illustrated painterly rendering of the same market lamp, stylized brushwork, dramatic warm rim lighting clashing with a cool blue fill light with no single consistent source, glass rendered with hand-drawn highlights instead of photoreal reflections, plain light-grey background.
```

## Intended flaw

View B breaks rendering consistency with View A: it switches from photoreal
to illustrative style and introduces contradictory dual-source lighting. A
good critic must name this inconsistency and give revision instructions
that lock View B to View A's photoreal style and single, neutral light
source without altering the object's geometry.
