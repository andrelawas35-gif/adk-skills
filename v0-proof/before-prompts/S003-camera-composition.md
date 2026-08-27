# S003 — Turnaround Identity Consistency (before-image prompt)

**Case:** Turnaround Identity Consistency — front and back views of the same asset must match in proportion, material, and detail for image-to-3D generation to succeed.
**Shared subject:** The market lamp prop, front view and back view intended as a matched pair.
**Engine:** Flux.1-Krea (`flux1-krea-dev_fp8_scaled.safetensors`), no LoRA.

## Before-image prompts (paste into your image generator)

**Front view (reference, held constant):**
```
Product reference photo of an oxidized brass market lamp, cracked glass panes, hanging chain, straight-on front view, neutral studio lighting, plain light-grey background, reference-plate framing.
```

**Back view (the flawed generation to critique):**
```
Product reference photo of an oxidized brass lantern, smooth unbroken glass, no visible chain, back view, taller and narrower proportions than a typical market lamp, neutral studio lighting, plain light-grey background, reference-plate framing.
```

## Intended flaw

The back view reads as a different object: the glass is smooth instead of
cracked, the chain is missing, and the proportions have drifted taller and
narrower than the front view. A good critic must name this identity
mismatch and give revision instructions that lock the back view to the
front view's established geometry, material, and scale.
