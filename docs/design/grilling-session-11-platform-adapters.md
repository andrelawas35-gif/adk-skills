# Grilling Session 11 — Platform Adapters

**Date:** 2026-07-22
**Model:** Claude Opus 4.6
**Prior session:** Session 10 (Capability Degradation) — see `docs/design/grilling-session-10-capability-degradation.md`
**Deliverable:** `docs/design/platform-adapters-component-plan.md`
**Status:** Complete — 10 decisions accepted (Decisions 82–91)

---

## Session focus

Inspect canonical skill sources, generated Codex/Claude Code/GitHub Copilot adapters, adapter configuration, generator code, and conformance tests. Determine what is portable vs platform-specific. Challenge whether deterministic generation proves semantic equivalence. Main decision: **what should an adapter be allowed to change without changing the meaning of a canonical skill?**

---

## Evidence inspected

| Source | What was checked |
|--------|-----------------|
| `tools/generate-adapters.py` (742 lines) | Full pipeline: `extract_body`, `namespace_skill_references`, `generate_frontmatter`, `generate_adapter_section`, `build_skill_output`, `check_platform` |
| `adapters/codex/overlay.yaml` | Capability mappings, classifications, declared limitations, frontmatter |
| `adapters/claude-code/overlay.yaml` | Same — plus `subagent_isolation: manual-fallback` unique to this platform |
| `adapters/github-copilot/overlay.yaml` | Same — plus `parallel_tool_execution: manual-fallback` |
| `tests/test_generate_adapters.py` (421 lines) | All 20 test methods, especially `test_all_platforms_share_identical_behavior`, `test_core_body_is_preserved_verbatim`, `test_codex_runtime_defers_to_the_project_pin`, `test_drift_is_detected` |
| `tools/verify-conformance.py` (lines 260–298) | Structural + capability table checks |
| `tools/install.sh` (lines 100–129) | `resolve()` function — lock file search for all platforms |
| `skills/core/*/SKILL.md` | All 14 canonical skills — Required capabilities, cross-skill references |
| `references/CAPABILITY-DEGRADATION.md` | Degradation protocol rules compared against generator template |
| `adapters/*/skills/*/SKILL.md` | Spot-checked generated output across all three platforms |
| `docs/design/capability-degradation-component-plan.md` | Session 10's 18 migration steps — sequencing with Session 11 |

---

## Decisions

### Decision 82 — Namespace rewriting is a semantic no-op

Namespace rewriting (`conduct-work-object` → `alawas-conduct-work-object`) is a deterministic bijection. It changes no routing logic, authority boundary, or schema semantic. The test `test_all_platforms_share_identical_behavior` is correct to apply it before comparing.

**Evidence:** `generate-adapters.py:459` (`namespace_skill_references`), `test_generate_adapters.py:37` (test helper applies same rewrite).

### Decision 83 — Capability descriptions may name aspirational behaviors

The word "Parallel" in `pressure-test-decision`'s `subagent_spawn` description is informational, not a gating instruction. The degradation system fires on declared required capabilities, not on prose within descriptions. Restricting descriptions to platform-neutral language would make them less informative on platforms that can parallelize, for no safety gain.

**Evidence:** `skills/core/pressure-test-decision/SKILL.md:83` — "`subagent_spawn` — Parallel Standards and Spec review (optional)." No canonical skill declares `parallel_tool_execution` as a required capability.

### Decision 84 — Every capability classified on any platform must be classified on all platforms

`subagent_isolation` is classified only on Claude Code; `parallel_tool_execution` is classified on Claude Code and GitHub Copilot but not Codex. Neither is required by any canonical skill, so the generator never checks them. Requiring symmetric classification prevents latent cross-platform gaps from hiding until a new skill requires the capability and one platform's generation fails with `ValueError` at line 334.

**Evidence:** `grep -c 'subagent_isolation'` across overlays: codex=0, claude-code=2, github-copilot=0. `grep -c 'parallel_tool_execution'`: codex=0, claude-code=1, github-copilot=1. Zero hits in any `skills/core/*/SKILL.md`.

### Decision 85 — The Codex-only pin-resolution conditional is an untested assumption; document and verify per-platform

The installer (`tools/install.sh:169–177`) writes lock files for all platforms. The generator (line 311) emits the read instruction only for Codex. Whether Claude Code and GitHub Copilot natively resolve duplicate-skill-discovery is unverified. The asymmetry must be verified per-platform, then either the paragraph is emitted where needed or the platform's native precedence is documented as the reason for omission.

**Evidence:** `install.sh:105` — `lock="$dir/.work-studio/adapter.$PLATFORM.lock"` (all platforms). `generate-adapters.py:311` — `if overlay["platform"] == "codex":` (Codex only). No Claude Code or GitHub Copilot adapter contains "Runtime pin resolution."

### Decision 86 — Replace the inline degradation paraphrase with a reference pointer

The generator (lines 348–358) inlines a paraphrased degradation protocol into each adapter while also shipping `CAPABILITY-DEGRADATION.md` as a reference file. This dual-source diverges silently if either changes. The appendix should say "Apply `references/CAPABILITY-DEGRADATION.md`" and emit only per-capability classification, tool mapping, and platform-specific note — matching the existing authority-rules pattern.

**Evidence:** Generator lines 374–380 (template text). `CAPABILITY-DEGRADATION.md:13,30–39` (canonical rules). Both say the same thing today; no test checks consistency between them.

### Decision 87 — The generator must extract the canonical description, not maintain a separate one

The `descriptions` dict at generator lines 181–252 independently rewrites every skill's description, diverging from the canonical frontmatter in trigger specificity and preconditions. The generator should extract and reformat the canonical description. If the compact trigger-action-boundary format is required, that format belongs in the canonical source.

**Evidence:** Compared all 14 canonical vs generated descriptions — all 14 differ in wording, trigger specificity, or preconditions. Example: canonical `grilling-session` says "Use when the user says 'grill me' or 'grill this'"; generated says "Use when the user explicitly requests continuous grilling or accepts a candidate."

### Decision 88 — Narrow reference distribution to files the skill actually mentions

The generator copies all 7 shared reference files to every adapter. `WORKSPACE-DOCUMENTATION-CONTRACT.md` is referenced by 2/14 skills; `SHARED-PROTOCOL.md` by 3/14. Distribution should be narrowed to files the skill's core body actually mentions.

**Evidence:** grep of all 14 canonical skills for each reference filename — `AGREEMENT-LOOP.md` and `SKILL-AWARE-GRILLING.md` referenced by 14/14; `EVIDENCE-MODEL.md` by 8/14; `CONSEQUENCE-AUTHORITY.md` by 13/14; others by 2–3.

### Decision 89 — Adapter change boundary: five permitted, four prohibited

**An adapter may change:** (1) frontmatter format (not semantic content), (2) appendix capability mapping table, (3) appendix degradation pointer, (4) appendix platform-specific behavioral paragraphs (verified and tested only), (5) reference file set (narrowed to referenced files).

**An adapter must NOT change:** (1) core body text after namespace rewriting, (2) capability declarations (maps and classifies, never adds/removes/reorders), (3) authority gate structure, (4) reference file content.

**Evidence:** Full inspection of generator pipeline, test suite, and all generated adapters across three platforms.

### Decision 90 — Rename the test to reflect what it proves: textual identity, not behavioral equivalence

`test_all_platforms_share_identical_behavior` checks byte-identical core text, not runtime behavioral equivalence. Rename to `test_all_platforms_share_identical_core_text`. Update docstring to: "the core body text is byte-identical across platforms — this guarantees no platform-specific rewriting but does not assert behavioral equivalence under different platform runtimes."

**Evidence:** Test implementation (line 372) compares text only. Decisions 83, 84, 85 show cases where identical text produces non-identical runtime behavior across platforms.

### Decision 91 — Session 11's generator changes execute before Session 10's migration

Decisions 86, 87, 88, 90 modify the generator and test suite. Session 10's step 11 regenerates all adapters. Executing Session 11's changes first means Session 10's regeneration produces the correct format — one pass, not two. Decision 84 (symmetric classification) executes before Session 10's overlay steps 3–5.

**Evidence:** Session 10 migration steps 3–5 (overlays), step 11 (regeneration), step 15 (tests) all touch files modified by Session 11 decisions.

---

## Open items carried forward

- **Decision 85 verification:** Confirm per-platform skill-loader precedence behavior for Claude Code and GitHub Copilot before deciding whether to add or omit the pin-resolution paragraph.
- **Dead classification cleanup:** After Decision 84, add `subagent_isolation` and `parallel_tool_execution` to Codex overlay; add `subagent_isolation` to GitHub Copilot overlay. Verify classifications are correct.
