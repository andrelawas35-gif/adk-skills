# S001 ComfyUI Workflow

Load this file in Comfy Desktop for the visual graph:

`S001_Mara_preserve_lock_img2img_visual.json`

The earlier `S001_Mara_preserve_lock_img2img_api.json` is API-format and may not
render as a node canvas.

The workflow expects this input image to exist in Comfy's shared input folder:

`s001_before_flux_krea_00002.png`

It uses Flux Krea img2img with low denoise (`0.35`) to preserve the original
S001 composition, hood, case, shoulder light, pose, framing, and alley while
improving face and silhouette readability.

## General Five-Case Workflow

Load this file in Comfy Desktop for the reusable visual graph that runs all
S001-S005 tests:

`V0_Five_Case_Test_General_Visual.json`

It has two lanes:

1. **Generate Before Image** — paste the current case's before prompt and
   queue the text-to-image lane.
2. **Revise After LLM Critique** — load the saved before image, paste the
   accepted LLM revision guidance, and queue the low-denoise img2img lane.

Use it one case at a time. Rename the Save Image prefixes if you want outputs
grouped by `S001`, `S002`, etc.
