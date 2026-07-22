# Capability Degradation Component Plan

**Date:** 2026-07-21
**Source:** Grilling Session 10 (Decisions 71–81)
**Status:** Accepted — not yet executed
**Prior session:** Session 9 (Deterministic CLI) — see `docs/design/deterministic-cli-component-plan.md`
**Evidence trail:** `docs/design/grilling-session-10-capability-degradation.md`
**Sequencing prerequisite:** Session 11 (Platform Adapters, Decisions 82–91) must execute first — see `docs/design/platform-adapters-component-plan.md`. Decision 91 established that Session 11's generator changes (Decisions 86, 87, 88, 90) execute before this migration so that step 11's regeneration produces the correct format in one pass.

---

## 1. Current-State Findings

### Capability model

The current model is entirely static, build-time, per-platform, and prose-enforced:

1. Each core skill declares abstract capabilities in `## Required capabilities`.
2. Each platform overlay (`adapters/*/overlay.yaml`) classifies every capability as `native`, `manual-fallback`, or `unsupported`.
3. `generate-adapters.py` produces per-skill capability tables in generated adapters.
4. At runtime, the agent reads the adapter SKILL.md and follows prose degradation rules.

No runtime detection, no session state, no execution-based discovery, no lazy discovery.

### Static assumptions

The overlay is a platform-level declaration, not a session-level one. It assumes:

- If `web_search: manual-fallback` in the Claude Code overlay, it is always manual-fallback — even when `WebSearch` is available.
- If `browser_automation: manual-fallback`, it is always manual-fallback — even when browser tools are loaded.
- The capability catalog is complete — categories not declared don't exist.

### Missing capabilities

Six capability categories are used by skills in practice but not declared:

| Category | Where it's implicit |
|---|---|
| `deployment` | `deploy-with-recovery` uses `terminal_run` for deployment commands |
| `secret_access` | `deploy-with-recovery` and `diagnose-production-incident` reference credentials |
| `background_processes` | `verify-release-evidence` needs a running server for UI verification |
| `persistent_session_state` | No skill currently needs it |
| `file_uploads` | `deploy-with-recovery` may upload artifacts |
| `artifact_rendering` | `verify-release-evidence` and `govern-scorecards` produce visual output |

---

## 2. Contradictions and Risks

| # | Finding | Evidence |
|---|---------|----------|
| 1 | `web_search: manual-fallback` on Claude Code but `WebSearch` is available in most sessions | `adapters/claude-code/overlay.yaml` vs runtime tool list |
| 2 | `browser_automation: manual-fallback` but `mcp__Claude_Browser__*` tools available | Same — overlay wrong about common case |
| 3 | `deployment` hidden inside `terminal_run` — `terminal_run: native` implicitly permits deployment commands | `deploy-with-recovery` SKILL.md decomposes deployment into `terminal_run` + `web_fetch` |
| 4 | `verify-release-evidence` may need `browser_automation` and `background_processes` but declares neither | Core skill `## Required capabilities` section |
| 5 | `CAPABILITY-DEGRADATION.md:65` says `parallel_tool_execution` is "typically native on Codex, Claude Code" but overlay says `manual-fallback` | Informational column stale vs overlay |
| 6 | No protocol for what happens when a native capability fails | `CAPABILITY-DEGRADATION.md` defines behavior for three tiers but not for execution-time failure |

---

## 3. Accepted Decisions

| # | Decision | Key constraint |
|---|----------|---------------|
| 71 | Manual-fallback capabilities are upgradeable within a session by detection | One-directional: floor can be raised, never lowered |
| 72 | Lazy detection at point of use, no session state | No ephemeral file, no session-start ceremony |
| 73 | Presence-only checking (tool listed = upgradeable) | No probe execution; failure handled like native failure |
| 74 | Detection rule lives in `CAPABILITY-DEGRADATION.md` as universal amendment | Per-capability blocks unchanged — they're the fallback path |
| 75 | Expand catalog to six new capabilities | `deployment`, `secret_access`, `background_processes`, `persistent_session_state`, `file_uploads`, `artifact_rendering` |
| 76 | Declare new capabilities in specific skills | 5 skills gain declarations; `persistent_session_state` undeclared |
| 77 | Per-platform classifications for new capabilities | `background_processes` native on CC/Codex; `artifact_rendering` native on CC; rest manual-fallback |
| 78 | Authority gates and capability degradation are independent pauses | Each records its own History entry with distinct provenance |
| 79 | Lazy detection upgrades are tentative (try-then-degrade) | Failed native execution falls back to manual-fallback protocol |
| 80 | Overlay remains conservative — `native` = guaranteed on every session | No fourth tier; lazy detection handles config-dependent availability |
| 81 | One bounded change in dependency order | Amend protocol → overlays → core skills → regenerate → fixture → tests |

---

## 4. Component Design

### 4.1 Lazy detection amendment to `CAPABILITY-DEGRADATION.md`

Add to the `manual-fallback` tier definition:

> Before applying manual-fallback degradation, check whether the platform tool
> mapped to this capability is present in the current environment. If present,
> attempt native execution. If native execution succeeds, record the upgrade as
> `[system]` evidence. If native execution fails, apply the manual-fallback
> protocol below and record both the attempted native execution and the fallback.
> If the tool is absent, follow the manual-fallback protocol unchanged.

This is a single paragraph added to the existing `manual-fallback` row in the classification table, or as a subsection immediately after the table.

### 4.2 Six new catalog entries in `CAPABILITY-DEGRADATION.md`

Add to the capability catalog table:

| Capability | Description | Typically native on |
|---|---|---|
| `deployment` | Execute a deployment command that changes a live production environment | None currently |
| `secret_access` | Read secrets, credentials, tokens, or API keys from a vault, env vars, or secure store | None currently |
| `background_processes` | Start and manage a long-running process that outlives a single tool call | Claude Code, Codex |
| `persistent_session_state` | Read and write state that persists across turns within a session | None currently |
| `file_uploads` | Upload a file to an external service or platform | None currently |
| `artifact_rendering` | Render a visual artifact (HTML, diagram, dashboard) for human inspection | Claude Code |

### 4.3 Overlay updates (three files)

Add to each `adapters/*/overlay.yaml`:

**`capability_mappings` additions:**

| Capability | Claude Code | Codex | GitHub Copilot |
|---|---|---|---|
| `deployment` | `—` | `—` | `—` |
| `secret_access` | `—` | `—` | `—` |
| `background_processes` | `Bash (background) / Monitor` | `run_in_terminal (background)` | `—` |
| `persistent_session_state` | `—` | `—` | `—` |
| `file_uploads` | `—` | `—` | `—` |
| `artifact_rendering` | `Artifact` | `—` | `—` |

**`capabilities` additions:**

| Capability | Claude Code | Codex | GitHub Copilot |
|---|---|---|---|
| `deployment` | manual-fallback | manual-fallback | manual-fallback |
| `secret_access` | manual-fallback | manual-fallback | manual-fallback |
| `background_processes` | native | native | manual-fallback |
| `persistent_session_state` | manual-fallback | manual-fallback | manual-fallback |
| `file_uploads` | manual-fallback | manual-fallback | manual-fallback |
| `artifact_rendering` | native | manual-fallback | manual-fallback |

**`declared_limitations` additions** (per platform, for manual-fallback capabilities with notes):

- `deployment` (all platforms): "No platform has first-class deployment tooling. Deployment commands execute through the shell. The skill's authority gate provides the authorization ceremony; the capability layer provides the execution instruction."
- `secret_access` (all platforms): "No platform has first-class vault or secret-store access. Credentials are provided by the user or environment. The skill must not invent, infer, or cache credentials."

### 4.4 Core skill declaration updates (five files)

**`skills/core/deploy-with-recovery/SKILL.md`** — add to `## Required capabilities`:
- `deployment` — execute only the runbook-approved incremental deployment command; without it, give the user the exact command to run.
- `secret_access` — access deployment credentials from the authorized source; without it, ask the user to provide or confirm credentials are available.
- `file_uploads` — upload deployment artifacts to the target platform; without it, give the user the exact upload instruction.

**`skills/core/diagnose-production-incident/SKILL.md`** — add to `## Required capabilities`:
- `secret_access` — access diagnostic credentials from the authorized source; without it, ask the user to provide the needed access.

**`skills/core/verify-release-evidence/SKILL.md`** — add to `## Required capabilities`:
- `background_processes` — start and manage a local server or service for verification; without it, ask the user to start the service.
- `artifact_rendering` — render a visual artifact for human verification of the user story; without it, ask the user to open the relevant page.

**`skills/core/implement-bounded-change/SKILL.md`** — add to `## Required capabilities`:
- `background_processes` — start a local server or service when focused verification requires it; without it, ask the user to start the service.

**`skills/core/govern-scorecards/SKILL.md`** — add to `## Required capabilities`:
- `artifact_rendering` — render scorecard evidence as a visual artifact; without it, present the data in structured text.

### 4.5 Adapter regeneration

Run `python3 tools/generate-adapters.py` after steps 4.1–4.4. The generator will:

1. Pick up new capability declarations from core skills.
2. Cross-reference against updated overlay classifications.
3. Produce updated capability mappings tables in all generated adapters.
4. Emit degradation sections for newly non-native capabilities.

No code changes to the generator are expected — the existing logic handles arbitrary capability names. The generator itself will have been modified by Session 11's migration (Decisions 86, 87, 88) before this step runs (Decision 91).

### 4.6 Behavioral fixture update

Add scenarios to `fixtures/slice-1-capability-degradation.md`:

**Scenario 12 — Lazy detection upgrades a manual-fallback capability:**
Given Claude Code adapter with `web_search: manual-fallback` and `WebSearch` available in the environment. When `investigate-live-question` needs `web_search`, then: (1) check whether `WebSearch` is present, (2) find it present, (3) use it natively, (4) record upgrade as `[system]` evidence. No manual-fallback pause.

**Scenario 13 — Lazy detection finds no tool, follows manual-fallback:**
Given Claude Code adapter with `deployment: manual-fallback` and no deployment tool in the environment. When `deploy-with-recovery` needs `deployment`, then: follow manual-fallback protocol unchanged.

**Scenario 14 — Tentative upgrade fails, falls back:**
Given Claude Code adapter with `web_search: manual-fallback` and `WebSearch` present but returning errors. When `investigate-live-question` attempts native execution and it fails, then: (1) fall back to manual-fallback protocol, (2) record both the attempted native execution and the fallback, (3) never claim the search succeeded.

**Scenario 15 — Authority gate and capability degradation fire independently:**
Given `deploy-with-recovery` with `deployment: manual-fallback`. When deployment is needed, then: (1) authority gate fires first — records the decision, (2) capability degradation fires second — records the execution method and gap, (3) two independent History entries.

**Scenario 16 — New capability `deployment` classified correctly:**
Given any platform adapter. When checking the capability mappings table for `deploy-with-recovery`, then: `deployment` row exists with classification and mapped tool.

### 4.7 Test updates

Update `tests/test_generate_adapters.py`:

- `test_every_required_core_capability_is_mapped_and_classified` — already works for arbitrary capabilities; verify it picks up the new declarations.
- `test_degradation_details_are_emitted_only_when_required` — add cases for new capabilities: `deployment` degradation present in `deploy-with-recovery` adapters, `artifact_rendering` degradation absent in Claude Code `verify-release-evidence` (it's native there) but present in Codex/Copilot.
- New test: `test_new_capabilities_classified_across_platforms` — verify all six new capabilities appear in each overlay and have valid classifications.

Update `tools/verify-conformance.py`:
- The existing structural checks should work without changes — they validate any capability row in the table. Verify by running `python3 tools/verify-conformance.py --structure`.

---

## 5. Dependency Order

```
Session 11 migration (Decisions 86–88, 90)  ← PREREQUISITE (Decision 91)
        │
        ▼
CAPABILITY-DEGRADATION.md amendment (4.1, 4.2)
        │
        ▼
Three overlay updates (4.3)
        │
        ▼
Five core skill updates (4.4)
        │
        ▼
Adapter regeneration (4.5)
        │
        ▼
Behavioral fixture update (4.6)
        │
        ▼
Test updates and verification (4.7)
```

Session 11's generator changes must complete before this migration begins (Decision 91, Session 11). This ensures step 11's regeneration uses the updated generator and produces correct output in one pass. Within this migration, each step depends on the previous. No parallelism in the implementation order.

---

## 6. Migration Steps

| # | Step | Files touched | Verification |
|---|------|---------------|--------------|
| 1 | Add lazy detection paragraph to `manual-fallback` tier in `CAPABILITY-DEGRADATION.md` | `references/CAPABILITY-DEGRADATION.md` | Read the amended section; confirm it describes presence check → attempt → fallback |
| 2 | Add six new rows to the capability catalog table in `CAPABILITY-DEGRADATION.md` | `references/CAPABILITY-DEGRADATION.md` | Read the table; confirm all six capabilities with descriptions and "typically native on" |
| 3 | Update `adapters/claude-code/overlay.yaml` with six new capability classifications and mappings | `adapters/claude-code/overlay.yaml` | Read overlay; confirm `background_processes: native`, `artifact_rendering: native`, rest `manual-fallback`. Note: Session 11's Decision 84 (symmetric classification) will have already been applied — verify all six new capabilities pass the symmetric check |
| 4 | Update `adapters/codex/overlay.yaml` with six new capability classifications and mappings | `adapters/codex/overlay.yaml` | Read overlay; confirm `background_processes: native`, rest `manual-fallback`. Same symmetric check as step 3 |
| 5 | Update `adapters/github-copilot/overlay.yaml` with six new capability classifications and mappings | `adapters/github-copilot/overlay.yaml` | Read overlay; confirm all six `manual-fallback`. Same symmetric check as step 3 |
| 6 | Add `deployment`, `secret_access`, `file_uploads` to `deploy-with-recovery` Required capabilities | `skills/core/deploy-with-recovery/SKILL.md` | Read section; confirm three new entries with descriptions |
| 7 | Add `secret_access` to `diagnose-production-incident` Required capabilities | `skills/core/diagnose-production-incident/SKILL.md` | Read section; confirm new entry |
| 8 | Add `background_processes`, `artifact_rendering` to `verify-release-evidence` Required capabilities | `skills/core/verify-release-evidence/SKILL.md` | Read section; confirm two new entries |
| 9 | Add `background_processes` to `implement-bounded-change` Required capabilities | `skills/core/implement-bounded-change/SKILL.md` | Read section; confirm new entry |
| 10 | Add `artifact_rendering` to `govern-scorecards` Required capabilities | `skills/core/govern-scorecards/SKILL.md` | Read section; confirm new entry |
| 11 | Run `python3 tools/generate-adapters.py` | All `adapters/*/skills/*/SKILL.md`, `adapters/*/manifest.json`, `adapters/*/SHA256SUMS` | Generator exits 0; `--check` passes |
| 12 | Verify generated adapters contain new capability rows | Generated adapter files | Spot-check: `deploy-with-recovery` Claude Code adapter has `deployment`, `secret_access`, `file_uploads` rows |
| 13 | Verify degradation sections emitted correctly | Generated adapter files | `deploy-with-recovery` Claude Code adapter has degradation sections for `deployment`, `secret_access`, `file_uploads`; `verify-release-evidence` Claude Code adapter has degradation for `background_processes` but NOT `artifact_rendering` (native) |
| 14 | Add scenarios 12–16 to `fixtures/slice-1-capability-degradation.md` | `fixtures/slice-1-capability-degradation.md` | Read fixture; confirm five new scenarios with pass conditions |
| 15 | Add/update tests in `tests/test_generate_adapters.py` | `tests/test_generate_adapters.py` | `python3 -m pytest tests/test_generate_adapters.py` passes |
| 16 | Run full conformance check | All generated files | `python3 tools/verify-conformance.py --structure` passes |
| 17 | Run full test suite | All test files | `python3 -m pytest tests/` passes |
| 18 | Fix stale "typically native on" for `parallel_tool_execution` in catalog | `references/CAPABILITY-DEGRADATION.md` | Column no longer says "Codex, Claude Code" — says "Codex" only |

---

## 7. Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| Generator needs code changes for new capability patterns | Unlikely — generator handles arbitrary capability names. Verify at step 11. |
| Existing tests fail on new capability rows | Tests are parameterized over core skill declarations; new rows should be picked up automatically. Verify at step 15. |
| Lazy detection paragraph is ambiguous about ordering (check → attempt → fallback) | Write the paragraph with explicit numbered steps. Review in step 1. |
| New `deployment` capability creates redundancy with `terminal_run` | Intentional — `deployment` is semantically distinct. The skill declares both. `terminal_run` covers non-deployment shell commands. |
| `persistent_session_state` in catalog but undeclared by any skill adds dead weight | Acceptable — it's a forward-compatible slot. If no skill needs it within two sessions, reconsider. |

---

## 8. Verification Criteria

The change is complete when:

1. `python3 tools/generate-adapters.py --check` exits 0 (generated files match).
2. `python3 tools/verify-conformance.py --structure` exits 0 (structural invariants hold).
3. `python3 -m pytest tests/` passes with no failures.
4. Every core skill that declares a new capability has the corresponding row in every adapter's capability table.
5. Every non-native new capability has a degradation section in the relevant adapters.
6. The behavioral fixture has scenarios covering lazy detection success, lazy detection miss, tentative upgrade failure, authority gate independence, and new capability classification.
7. The `CAPABILITY-DEGRADATION.md` lazy detection paragraph explicitly describes the three-step flow: check presence → attempt native → fall back to manual-fallback on failure.

---

## 9. What This Does Not Cover

- **Implementation of lazy detection in agent behavior.** The amendment is a prose instruction. No runtime code enforces it. Agent compliance is the same enforcement model as the rest of the protocol.
- **Session 9's CLI (`tools/ws/`).** The CLI design is independent — it writes to `.work-studio/`, not to capability state. No conflict with this change.
- **Platform tool development.** No new platform tools are created. The new capabilities are classified based on existing tools.
- **`persistent_session_state` consumers.** No skill declares this capability. It exists in the catalog for future use.
- **Overlay reclassification of existing capabilities.** `web_search`, `browser_automation`, `parallel_tool_execution`, and `subagent_isolation` retain their current classifications. Lazy detection handles session-level variance. Note: Session 11's Decision 84 requires symmetric classification — `subagent_isolation` and `parallel_tool_execution` will be added to missing overlays by Session 11's migration before this plan executes.
- **Session 11's generator changes.** This plan assumes Session 11's migration (Decisions 86–88, 90) has already been executed per Decision 91. See `docs/design/platform-adapters-component-plan.md`.
