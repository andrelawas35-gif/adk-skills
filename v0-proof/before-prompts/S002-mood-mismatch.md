# S002 — Asset Style Mismatch (before-image prompt)

**Case:** Asset Style Mismatch — the prop must match the Lower Market environment's established material language (dark stone, oxidized brass, wet wood); the current rendering breaks it.
**Shared subject:** The same market lamp prop, now as a concept reference meant to slot into the Lower Market environment kit.
**Engine:** Flux.1-Krea (`flux1-krea-dev_fp8_scaled.safetensors`), no LoRA.

## Before-image prompt (paste into your image generator)

```
Product reference photo of a market lamp prop, hanging chain, glass panes, straight-on three-quarter angle, neutral studio lighting, plain light-grey background. The lamp is rendered in bright glossy chrome with a clean unweathered plastic-like finish, saturated cyan neon accent glow along its edges -- a futuristic sci-fi object, not a weathered market fixture. Crisp, clean, showroom-new appearance.
```

## Intended flaw

The prop's material language is wrong for its environment: glossy sci-fi
chrome and neon accents instead of oxidized brass and weathering. A good
critic must name this mismatch and give revision instructions that ground
the asset in the environment's dark-stone/oxidized-brass/wet-wood language
without changing its silhouette or proportions.
