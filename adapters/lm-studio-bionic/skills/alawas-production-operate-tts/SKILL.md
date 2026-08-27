---
name: alawas-production-operate-tts
description: "Use when structured local TTS generation must produce audio takes and metadata from caller-supplied text, voice_id, and performance parameters; starts with the Tier 1 local_piper tracer and never judges performance or selects takes."
default_tier: high
platform: lm-studio-bionic
---
# Operate TTS

## Governing principle

The TTS operator turns caller-supplied voice-generation parameters into audio
files and structured take metadata. It executes; it does not interpret
performance intent, choose the best take, or decide whether a voice is good.

## Boundaries and non-goals

This skill does:

- Generate local Tier 1 WAV takes through Piper (`local_piper`).
- List the available local Piper voice installed for the tracer.
- Return structured metadata: duration, file path, tier used, voice ID, and
  take ID.
- Generate up to four deterministic A/B/C/D takes for director comparison.

This skill does not:

- Use `System.Speech`.
- Call cloud TTS tiers.
- Translate performance direction into parameters.
- Select, rank, score, or judge generated takes.
- Maintain a voice bible, perform lip-sync, or assemble audio into shots.
- Require GPU claims; TTS is CPU/local-process work in this tracer.

## Inputs and preconditions

**Required input:** a structured TTS operation and parameters. `tts.generate`
requires `text`, `voice_id`, `performance_params`, and `take_count`.

**Preconditions:** Piper 2023.11.14-2 for Windows and the
`en_US-lessac-medium` ONNX voice are installed at the accepted local path:
`C:/Users/Andre/Documents/Work_Studio/local_tts`.

## Required capabilities

- `terminal_run` — run the local Piper executable as a bounded subprocess.
- `file_read` — verify the local Piper executable, voice model, and config.
- `file_write` — write generated WAV takes to caller-owned output paths.
- `structured_output` — return take metadata and structured errors.
- `user_confirmation` — obtain authority before adding cloud tiers, changing
  voice backends, or writing outside caller-owned output paths.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Generating local scratch WAV files in a caller-specified output directory is
  allowed inside the accepted Work Object boundary.
- Changing the backend, adding cloud API calls, downloading additional voices,
  writing to production audio-lock locations, or judging/selecting takes
  requires a separate decision.
- This operator must not treat successful audio generation as director approval
  of a take.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

Nominate a Candidate when a requested operation would cross from bounded
generation into performance interpretation, take selection, cloud API use, or
voice identity governance.

## Skill Grilling Profile

Apply the `alawas-production-operate-tts` profile in
`references/SKILL-AWARE-GRILLING.md`. Challenge whether the operator remains an
executor, whether audio files and metadata are enough evidence, and whether any
request smuggles in performance judgment.

## Stage workflow

1. Receive a structured operation.
2. Validate that the operation is in the bounded surface.
3. For `tts.list_voices`, report installed local Piper voice metadata.
4. For `tts.generate`, validate text, voice ID, take count, and output path.
5. Run Piper once per requested take using deterministic synthesis parameter
   variation.
6. Read each WAV header to compute duration and return metadata.
7. Report errors as generation failures or missing dependency gaps; never claim
   a take exists without a file.

## Evidence rules

- Piper command completion, output files, and WAV metadata are `[system]`.
- Director-selected voice, take, or performance direction is `[decision]`.
- Any statement about take quality is out of scope for this operator unless a
  downstream performance skill records it.

## Implementation

Use `tools/production/tts_operator/client.py` for implementation-level
operations.

## Tool Surface

- `tts.list_voices()`
- `tts.generate(text, voice_id, performance_params, take_count, output_dir)`

## Failure Behavior

If Piper, the voice model, or the voice config is missing, report a missing
dependency gap. If Piper exits non-zero or no WAV is produced, return a
generation failure. If an unknown voice is requested, reject before running
Piper. If more than four takes are requested, reject rather than inventing more
presets.
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Epistemic rules

This skill uses the **full 6‑tag system** (`references/epistemic/epistemic-rules-full.md`).

The epistemic tier is resolved from the skill's `default_tier` (high).
**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the epistemic tier is upgraded to at least `medium` (essential 3‑tag).
When `consequence: high`, the epistemic tier is upgraded to the strongest
available tier (full 6‑tag).
`actual_epistemic_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

For a high-consequence Work Object, confirmation must name the exact
proposed mutation. Do not stage, annotate, change status, append History,
or make any other mutation before receiving that scoped confirmation.

### Model tier

This skill declares `default_tier: high`.
The platform overlay resolves this to `Qwen3.5-9B Q4`.
The prompt budget for this tier is approximately 32000 tokens (advisory).

**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the effective tier is upgraded to at least `medium`. When `consequence: high`,
the effective tier is upgraded to the strongest available model.
`actual_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `terminal_run` | `Shell tool (native, coding projects)` | native |
| `file_read` | `native project file access (Read file)` | native |
| `file_write` | `Edit / write file (native coding tools)` | native |
| `structured_output` | `Structured output (native, per-session schema)` | native |
| `user_confirmation` | `conversation turn` | native |
