# S001 — Asset Silhouette Readability (before-image prompt)

**Case:** Asset Silhouette Readability — a hero prop's form and silhouette must read clearly enough to serve as a 3D-reconstruction reference.
**Shared subject:** A market lamp prop — oxidized brass housing, cracked glass panes, hanging chain — the first hero asset for the Lower Market environment kit.
**Engine:** Flux.1-Krea (`flux1-krea-dev_fp8_scaled.safetensors`), no LoRA.

## Before-image prompt (paste into your image generator)

```
Product reference photo of an oxidized brass market lamp prop, hanging chain, cracked glass panes, straight-on three-quarter angle. The lamp is shot against a near-black background with harsh single-source lighting from one side, throwing most of the object into deep shadow. Its silhouette blends into the dark backdrop, edges barely distinguishable, muddy low-contrast overall. Reference-plate framing, otherwise neutral studio setup.
```

## Intended flaw

The lamp's silhouette and form are unreadable: it merges with the dark
background, contrast is muddy, and there is no clear edge separation. A good
critic must name this and give revision instructions that separate the asset
from its background — enough for the shape to serve as a usable
image-to-3D reference — without inventing new material details.
