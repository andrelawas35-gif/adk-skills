# V0 Proof — Local AI Animation Studio (Work Object 2026-08-23-002)

The first complete local studio loop, tested end to end: image-to-critique-to-revision.

- **Runtime:** LM Studio Bionic
- **First model:** Qwen3.5-9B Q4 (fallback: Gemma 3 12B Q4; cloud only after local fails)
- **Success:** 3-of-5 revised images clearly better against shot intent, zero preserve/avoid violations

## Layout

- `packet-template.md` — packet shape, required critic output schema, human-judgment fields
- `before-prompts/S001-...md` — the five deliberately flawed before-image prompts
- `shot-objects/S001-...json` — the five shot objects

## Run procedure

1. **Generate before images.** For each case, paste the prompt from
   `before-prompts/` into your image generator (ComfyUI or your tool of choice)
   and save the result as the case's before image.
2. **Load the packet.** In LM Studio Bionic with Qwen3.5-9B Q4, give the model:
   the before image, the shot object, and the required critic output schema
   (from `packet-template.md`).
3. **Get structured revision instructions.** Ask the critic to return diagnosis,
   protect, revision targets, instructions, reasons, and avoid — exactly per schema.
4. **Apply revisions manually.** Follow the instructions to produce the after image.
5. **Judge.** Fill the `human_judgment` fields for each case.
6. **Score.** Success requires 3-of-5 clearly better against intent with zero
   preserve/avoid violations.

## Notes

- The model is replaceable: this proof validates the schema and loop, not the provider.
- GPU/VRAM: 10 GB RTX 3080 → sequential time-sharing; one resident model at a time.
- Record verdicts and evidence back into the Work Object when the proof is complete.
