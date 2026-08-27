---
schema_version: 1
id: 2026-08-24-016
title: Build tiered TTS operator skill for voice performance generation
type: change
status: active
state: verify
consequence: low
sensitivity: ordinary
domain: [production]
created_at: 2026-08-25T01:56:53Z
updated_at: 2026-08-25T18:21:57Z
next_action: alawas-engineering-verify-release-evidence: independently rerun focused TTS operator checks and live local_piper smoke, confirm generated adapter/install state, and decide whether residual pre-existing ledger/kernel warnings block release.








---
## Intent

Call tiered TTS APIs (Tier 1 local, Tier 2 cheap API, Tier 3 premium API) to
generate voice takes from structured performance parameters. Returns audio
files. No performance opinion.

Parent: WO `2026-08-23-001` §5.2. Component: COMP-044.

## Success evidence

- [x] Can generate audio takes from text + voice_id + performance parameters
- [x] Supports at least Tier 1 (local TTS) at launch
- [x] Returns structured take metadata (duration, file path, tier used)
- [x] Multiple takes (A/B/C/D) generated per request for comparison


## Constraints and non-goals

**Constraints:**
- Tier routing: cheapest tier that meets quality requirements
- No GPU contention (TTS is CPU or cloud API)

**Non-goals:**
- No performance translation (belongs to `2026-08-24-024`)
- No take selection or quality judgment

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Accepted Tier 1 Piper tracer for local TTS operator

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Smallest Tier 1 local TTS tracer for COMP-044: use downloaded Piper 2023.11.14-2 for Windows plus the `en_US-lessac-medium` ONNX voice as the local backend. Build a bounded operator surface with `tts.list_voices` and `tts.generate`; `tts.generate` accepts `text`, `voice_id`, `performance_params`, and `take_count`, writes WAV files, and returns metadata (`duration_seconds`, `file_path`, `tier_used: local_piper`, `voice_id`, `take_id`). A/B/C/D takes may vary Piper synthesis controls such as noise, length, and sentence silence deterministically; no performance translation, take selection, quality judgment, cloud API tier, voice bible, lip-sync, or ffmpeg dependency is included in this slice. |
| **Authorization** | Director accepted the tracer design in chat, then corrected the Tier 1 backend requirement: "download either `piper`, `espeak`, `ffmpeg`, or Python TTS packages not system.speech." |
| **Confidence** | medium-high for local generation with Piper - basis: Piper Windows executable and `en_US-lessac-medium` voice were downloaded outside the repo and a smoke command generated a valid WAV; low for broader voice/performance quality because this tracer deliberately does not judge performance or choose production voices. |
| **Actor** | Director (acceptance/backend correction), alawas-design-design-tracer-bullet (design), codex (dependency download/smoke evidence) |
| **Revisit trigger** | Revisit if Piper cannot support the required performance parameter envelope without hidden quality judgment, if deterministic A/B/C/D variation is not useful enough for downstream director selection, or if a later Tier 1 backend choice makes `local_piper` the wrong stable tier label. |
| **Rationale** | This tests the critical assumption with the smallest real local dependency: Work Studio can generate actual local audio takes and structured metadata before choosing cloud API tiers or building the performance pipeline around the operator. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [decision] | director request, 2026-08-25 | Director explicitly routed this Work Object to alawas-thinking-turn-signal-into-work after conductor activation. Classification result: activate the existing low-consequence production change for COMP-044 rather than discard, remember, or incubate. |
| [system] | local Piper download and smoke run, 2026-08-25 | Tier 1 local TTS dependency installed outside the repo at C:/Users/Andre/Documents/Work_Studio/local_tts: Piper Windows 2023.11.14-2 extracted with piper.exe present, en_US-lessac-medium.onnx and matching .onnx.json downloaded from Hugging Face, and a smoke command generated C:/Users/Andre/Documents/Work_Studio/local_tts/smoke/piper-smoke.wav. WAV verification via Python wave: exists True, 141472 bytes, mono, 22050 Hz, 16-bit samples, duration 3.207 seconds. |
| [system] | implementation, 2026-08-25 | Implemented COMP-044 Tier 1 local_piper tracer: added tools/production/tts_operator with PiperTTSClient supporting tts.list_voices and tts.generate, deterministic A/B/C/D WAV generation from text, voice_id, performance_params, and take_count, structured duration/file/tier/voice/take metadata, validation for invalid voice/take/dependency cases, and no System.Speech, cloud tier, performance translation, take selection, quality judgment, voice bible, lip-sync, ffmpeg, or GPU claim behavior. Registered production-operate-tts in core skill contract, kernel manifest, component governance, component ledger, generated adapters, and project-pinned .agents skills. |
| [system] | verification, 2026-08-25 | Focused implementation verification passed: uv run --python 3.11 python -m unittest tests.test_tts_operator_local_piper -v passed 6 tests; tests.test_component_governance -v passed 4 tests; combined unittest run passed 10 tests. skill-map build generated 48 skills; tools/generate-adapters.py and --check reported no adapter drift; project install wrote .agents/skills/alawas-production-operate-tts/SKILL.md. Live smoke through PiperTTSClient listed en_US-lessac-medium and generated four WAV takes under runtime/tts_takes/smoke-2026-08-25 with durations A 3.049s, B 3.095s, C 3.142s, D 3.153s. tools.ws validate --files for this Work Object passed default checks with only the existing no-baseline warning. tools.ws validate ledger now has only the pre-existing COMP-001 grill-staleness error; no remaining COMP-044 dependency range error. tools/verify-kernel.py still fails on pre-existing undeclared design skills, not production-operate-tts. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-25T18:09:55Z — Resumed and activated as supporting

- **State:** notice
- **Status:** active
- **Actor:** codex
- **Rationale:** Director invoked the conductor on the TTS operator Work Object by path. The object is active but still in notice with no recorded classification evidence, so it was added to active.md as supporting and routed to turn-signal-into-work for classification before design or build work.
### 2026-08-25T18:11:12Z — Classified and activated TTS operator work

- **State:** design
- **Status:** active
- **Actor:** alawas-thinking-turn-signal-into-work
- **Rationale:** The signal is an existing Work Object with explicit director routing, a concrete parent/component reference (WO 2026-08-23-001 section 5.2, COMP-044), clear low consequence, ordinary sensitivity, and bounded non-goals. Classification is activate; next stage is design-tracer-bullet to choose the smallest Tier 1 local TTS operator slice before implementation.
### 2026-08-25T18:15:45Z — Accepted Piper Tier 1 TTS tracer design

- **State:** build
- **Status:** active
- **Actor:** alawas-design-design-tracer-bullet
- **Rationale:** Director accepted the tracer design and corrected the backend away from System.Speech. Piper Windows plus en_US-lessac-medium was downloaded outside the repo and smoke-tested with a valid WAV output, so the next bounded step is implementation of the local_piper TTS operator surface and tests.
### 2026-08-25T18:21:57Z — Implemented local_piper TTS operator tracer

- **State:** verify
- **Status:** active
- **Actor:** alawas-engineering-implement-bounded-change
- **Rationale:** The accepted Tier 1 local_piper implementation is in place, focused tests pass, generated adapters are in sync and installed into the project-pinned Codex adapter directory, and a live PiperTTSClient smoke generated four A/B/C/D WAV takes with structured metadata. Remaining validation caveats are pre-existing ledger/kernel issues outside COMP-044, so the Work Object is ready for independent release-evidence verification rather than more build work.
