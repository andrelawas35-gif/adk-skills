# S004 — Reference Plate Clutter (before-image prompt)

**Case:** Reference Plate Clutter — an image-to-3D reference plate must isolate the asset cleanly; background clutter confuses mesh reconstruction.
**Shared subject:** The market lamp prop, intended as a clean isolated reference plate for AI 3D generation.
**Engine:** Flux.1-Krea (`flux1-krea-dev_fp8_scaled.safetensors`), no LoRA.

## Before-image prompt (paste into your image generator)

```
Product reference photo of a market lamp prop, hanging chain, glass panes, straight-on three-quarter angle, but surrounded by a cluttered busy background: overlapping crates, tangled rope, patterned fabric, and other market props all in sharp focus behind and beside it, competing for attention with the lamp itself. Even lighting across the whole cluttered scene.
```

## Intended flaw

The background clutter competes with and partially occludes the asset,
making it unusable as a clean image-to-3D reference plate. A good critic
must name this and give revision instructions that isolate the lamp against
a plain, neutral background without altering the object itself.
