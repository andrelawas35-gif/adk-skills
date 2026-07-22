# Grilling Session 10 — Capability Degradation and Negotiation

**Date:** 2026-07-21
**Focus:** How should Work Studio determine what the current coding-agent environment can actually do without overclaiming?
**Status:** Converged — shared understanding confirmed
**Prior session:** Session 9 (Deterministic CLI) — see `docs/design/grilling-session-9-deterministic-cli.md`

---

## Evidence Ledger

### Observed

- `references/CAPABILITY-DEGRADATION.md` — canonical three-tier protocol (native / manual-fallback / unsupported). Five rules: no false verification, stricter safety wins, one instruction at a time, record what remains unverified, unsupported stops the path.
- `adapters/claude-code/overlay.yaml` — 16 abstract capabilities, 11 native, 4 manual-fallback (`browser_automation`, `web_search`, `subagent_isolation`, `parallel_tool_execution`), 0 unsupported.
- `adapters/codex/overlay.yaml` — 14 capabilities, 12 native, 2 manual-fallback (`browser_automation`, `web_search`).
- `adapters/github-copilot/overlay.yaml` — 15 capabilities, 11 native, 3 manual-fallback (`browser_automation`, `parallel_tool_execution`, `web_search`).
- `tools/generate-adapters.py` — extracts `## Required capabilities` from core skills, cross-references overlay classifications, generates per-skill capability tables with degradation sections only when non-native capabilities are required.
- `tests/test_generate_adapters.py:282-379` — tests that every core capability appears in every adapter with a valid classification; tests degradation sections are present only when needed; tests that manual-fallback stays explicit.
- `tools/verify-conformance.py:266-298` — structural checks on capability mappings tables: validates rows match declarations, classifications are valid, degradation sections present for non-native capabilities.
- `fixtures/slice-1-capability-degradation.md` — 11-scenario behavioral fixture covering all three tiers across all platforms.
- All 14 core skills' `## Required capabilities` sections inspected:
  - Only `investigate-live-question` declares `web_search`
  - No core skill declares `browser_automation`
  - `pressure-test-decision` declares `subagent_spawn` (optional)
  - All skills reference `references/CAPABILITY-DEGRADATION.md`
- This session's runtime environment has `WebSearch`, `mcp__Claude_Browser__*`, and parallel tool execution available — all classified `manual-fallback` in the overlay.
- Capability model is entirely static: build-time, per-platform, prose-enforced. No runtime detection, no session state, no execution-based discovery.

### Claimed

- `CAPABILITY-DEGRADATION.md:65` says `parallel_tool_execution` is native on "Codex, Claude Code" — the overlay classifies it as `manual-fallback` on Claude Code. Minor inconsistency in the catalog's "typically native on" column vs the overlay.

### Inferred

- The overlay's static classifications are wrong about this session's actual capabilities in at least three categories (`web_search`, `browser_automation`, `parallel_tool_execution`). The overlay describes the platform's worst case, not the common case.
- `deployment` and `secret_access` are authority-bearing operations hidden inside `terminal_run`. A platform that classifies `terminal_run: native` implicitly permits deployment commands even if the platform's permission model would block them at runtime.
- `verify-release-evidence` may need `browser_automation` and `background_processes` in practice (verifying a rendered web page requires a running server and a browser) but declares neither — the capability gap is invisible.

### Contradictions

- `CAPABILITY-DEGRADATION.md:65` ("typically native on: Codex, Claude Code" for `parallel_tool_execution`) vs `adapters/claude-code/overlay.yaml` (`parallel_tool_execution: manual-fallback`). The catalog's informational column is stale.

---

## Decisions Log

### Decision 71 — Manual-fallback capabilities are upgradeable within a session

Manual-fallback capabilities can be upgraded to native within a session when the agent detects the corresponding tool is available. The overlay classification is the default floor, not the final word. Upgrades are one-directional: detection can raise `manual-fallback` to `native`, never lower `native`.

**Rationale:** The overlay is a platform-level declaration, not a session-level one. A static classification that's wrong about the common case (e.g., `web_search: manual-fallback` when `WebSearch` is available) forces unnecessary manual-fallback pauses.

### Decision 72 — Lazy detection at the point of use, no session state

Capability upgrades are detected lazily when a skill encounters a `manual-fallback` capability, not eagerly at session start. No ephemeral session state file is created. Each skill independently checks tool availability.

**Rationale:** No session-start ceremony, no file to manage, no stale cache. The redundancy cost (multiple skills re-checking) is negligible — the check is "is this tool present?" not "does this tool work end-to-end?"

### Decision 73 — Presence-only checking

Lazy detection uses presence-only checking: if the corresponding platform tool is listed in the current environment's tool list, the capability is upgradeable. No probe execution. If the tool is present but fails during actual use, the skill handles failure the same way as any native capability failure.

**Rationale:** The same failure mode applies to any `native` capability — `terminal_run` doesn't get probed before use. A `manual-fallback` capability upgraded by presence detection is in exactly the same position as any `native` capability.

### Decision 74 — Detection rule lives in CAPABILITY-DEGRADATION.md

The lazy-detection rule is a universal amendment to the `manual-fallback` tier definition in `CAPABILITY-DEGRADATION.md`. Per-capability degradation blocks in generated adapters remain unchanged — they describe the fallback path when the tool is absent.

**Rationale:** Single rule, single location. The detection rule applies to all `manual-fallback` capabilities on all platforms. Per-adapter duplication adds noise without value.

### Decision 75 — Expand the capability catalog to six new categories

Add `deployment`, `secret_access`, `background_processes`, `persistent_session_state`, `file_uploads`, and `artifact_rendering` to the canonical capability catalog in `CAPABILITY-DEGRADATION.md`.

**Rationale:** These are real capabilities that a coding agent either has or doesn't. The user's session prompt identified them as gaps, and the sweep confirmed that skills implicitly depend on capabilities they don't declare.

### Decision 76 — Declare new capabilities in specific skills

Skill declarations based on sweep evidence:

| Capability | Skills |
|---|---|
| `deployment` | `deploy-with-recovery`, `diagnose-production-incident` |
| `secret_access` | `deploy-with-recovery`, `diagnose-production-incident` |
| `background_processes` | `verify-release-evidence`, `implement-bounded-change` |
| `file_uploads` | `deploy-with-recovery` |
| `artifact_rendering` | `verify-release-evidence`, `govern-scorecards` |
| `persistent_session_state` | None (in catalog, undeclared by any skill) |

**Rationale:** Each declaration is grounded in the skill's prose — `deploy-with-recovery` mentions credentials, `verify-release-evidence` describes exercising the user story, etc. `persistent_session_state` is a forward-compatible slot.

### Decision 77 — Per-platform classifications for new capabilities

| Capability | Claude Code | Codex | GitHub Copilot |
|---|---|---|---|
| `deployment` | manual-fallback | manual-fallback | manual-fallback |
| `secret_access` | manual-fallback | manual-fallback | manual-fallback |
| `background_processes` | native | native | manual-fallback |
| `persistent_session_state` | manual-fallback | manual-fallback | manual-fallback |
| `file_uploads` | manual-fallback | manual-fallback | manual-fallback |
| `artifact_rendering` | native | manual-fallback | manual-fallback |

**Rationale:** `deployment` and `secret_access` are `manual-fallback` everywhere — no platform has first-class deployment or vault tooling. `background_processes` is native on Claude Code (Monitor, background Bash) and Codex (background terminals). `artifact_rendering` is native on Claude Code (Artifact tool). Classifications reflect whether the platform has a dedicated tool, not whether shell commands could accomplish it.

### Decision 78 — Authority gates and capability degradation are independent

Authority gates (skill layer) and capability degradation (capability layer) remain independent pauses, even when both fire on the same action. Each records its own History entry with distinct provenance.

**Rationale:** Authority gates record "should this be done?" (permission). Capability degradation records "who does it?" (ability). These are different facts. Coupling them would require the degradation protocol to understand authority gates.

### Decision 79 — Lazy detection upgrades are tentative

If native execution fails after a lazy-detection upgrade, the skill falls back to the manual-fallback protocol. The upgrade is try-then-degrade, not an irreversible commitment. Both the attempted native execution and the fallback are recorded.

**Rationale:** Without fallback, a presence-detected upgrade that fails leaves the skill stuck — it bypassed manual-fallback and has no recovery path. Tentative upgrades mean the detection opens a fast path; failure drops back to the slow path.

### Decision 80 — Overlay remains conservative

`native` means guaranteed on every session of a platform, regardless of configuration. `manual-fallback` means not guaranteed. No fourth tier. Lazy detection handles the common case where a `manual-fallback` capability is actually available.

**Rationale:** `web_search` on Claude Code depends on configuration — it's not guaranteed the way `file_read` is. A three-tier model stays clean. Lazy detection is the answer to configuration-dependent capabilities, not a new classification tier.

### Decision 81 — One bounded change

Implementation is one bounded change. Order: amend `CAPABILITY-DEGRADATION.md`, update three overlays, update five core skills, regenerate adapters, update fixture, run tests.

**Rationale:** All files are part of the same protocol. The catalog expansion depends on the detection amendment (new `manual-fallback` capabilities rely on lazy detection). Splitting would create an intermediate state where the amendment exists but the capabilities it's designed to upgrade don't.

---

## Coverage Proof

| Branch | Status |
|---|---|
| Upgrade mechanism (lazy, presence, tentative) | Resolved — Decisions 71-74, 79 |
| Rule location | Resolved — Decision 74 |
| Catalog expansion | Resolved — Decisions 75-76 |
| Skill declarations | Resolved — Decision 76 |
| Platform classifications | Resolved — Decision 77 |
| Authority gate interaction | Resolved — Decision 78 |
| Failure fallback | Resolved — Decision 79 |
| Overlay conservatism / tier count | Resolved — Decision 80 |
| Implementation scope | Resolved — Decision 81 |
| `persistent_session_state` | In catalog, undeclared — intentional forward-compatible slot |

No remaining question is likely to change the recommendation.

---

## Session Prompt Requirements Verification

| Requirement | How addressed |
|---|---|
| Statically declared | Yes — overlays declare per-platform floors |
| Detected | Yes — lazy presence detection at point of use (D72-73) |
| Assumed | No — `native` = guaranteed, no assumption without declaration (D80) |
| User-confirmed | Authority gates are independent of capability tier (D78) |
| Tested by execution | Presence-only, no probe; failure triggers fallback (D73, D79) |
| Discovered lazily | Yes (D72) |
| Cached for the session | No caching, re-derived per use (D72) |
| All 14 capability categories | Six new added to catalog (D75-76); existing eight unchanged |
| Three tiers grilled | Tiers unchanged; lazy detection amends manual-fallback (D74) |
| Degradation changes procedure | Yes — manual-fallback changes procedure |
| Degradation changes evidence standard | Yes — evidence tagged as `[human]` not `[system]` |
| Degradation changes allowed claim | Yes — cannot claim "verified" for degraded step |
| Degradation changes route | Yes — unsupported stops the path |
| Degradation changes completion status | Yes — "manual-fallback" not "verified" |
| Degradation changes authority gate | No — independent systems (D78) |
| Degradation changes required human action | Yes — human performs the step |
| Skills unchanged when capability unavailable | Challenged — five skills need new declarations (D76) |
| Ephemeral session state | No (D72) |
