# Platform Adapters Component Plan

**Date:** 2026-07-22
**Source:** Grilling Session 11 (Decisions 82–91)
**Status:** Accepted — not yet executed
**Prior session:** Session 10 (Capability Degradation) — see `docs/design/capability-degradation-component-plan.md`
**Evidence trail:** `docs/design/grilling-session-11-platform-adapters.md`
**Sequencing:** This plan executes BEFORE Session 10's migration (Decision 91).

---

## 1. Current-State Findings

### Adapter pipeline

The generator (`tools/generate-adapters.py`) performs five operations per skill per platform:

1. Extracts the canonical body from `skills/core/<skill>/SKILL.md`.
2. Rewrites cross-skill backtick references with the `alawas-` namespace prefix.
3. Generates platform-specific YAML frontmatter with an independently authored description.
4. Appends a Platform Adapter section with capability mappings, degradation details, and (Codex-only) pin-resolution prose.
5. Copies all 7 shared reference files to every adapter regardless of usage.

### Semantic preservation claim

The test suite's `test_all_platforms_share_identical_behavior` asserts byte-identical core body text across platforms. Its name and docstring claim "identical behavior" — but identical text can produce non-identical runtime behavior when interpreted by different platform runtimes with different tool sets, permission models, and execution semantics.

### Dual-source divergence risks

Two sources of truth exist for:
- **Skill descriptions** — canonical frontmatter vs generator's `descriptions` dict (lines 181–252).
- **Degradation protocol** — generator's inline template (lines 348–358) vs `CAPABILITY-DEGRADATION.md` reference file.

Both pairs say similar things today but are maintained independently and will drift.

### Asymmetric classifications

- `subagent_isolation`: classified only on Claude Code (manual-fallback). Missing from Codex and GitHub Copilot overlays.
- `parallel_tool_execution`: classified on Claude Code and GitHub Copilot (manual-fallback). Missing from Codex overlay.
- Neither is required by any canonical skill, so the gap is invisible to the generator and test suite.

### Pin-resolution asymmetry

The installer writes `.work-studio/adapter.<platform>.lock` for all platforms. The generator emits the runtime read instruction only for Codex. Whether Claude Code and GitHub Copilot need this instruction is unverified.

### Reference file broadcast

All 7 shared reference files are copied to every adapter. `WORKSPACE-DOCUMENTATION-CONTRACT.md` is referenced by 2/14 skills; `SHARED-PROTOCOL.md` by 3/14. Unreferenced files consume context budget and create false signals.

---

## 2. Contradictions and Risks

| # | Finding | Evidence |
|---|---------|----------|
| 1 | Generator descriptions diverge from canonical descriptions in trigger specificity and preconditions | All 14 skills differ — compared canonical vs generated descriptions |
| 2 | Inline degradation template paraphrases canonical reference file — two sources of truth | Generator lines 348–358 vs `CAPABILITY-DEGRADATION.md:13,30–39` |
| 3 | `subagent_isolation` classified on 1/3 platforms; `parallel_tool_execution` on 2/3 | Overlay grep across all three platforms |
| 4 | Pin-resolution paragraph emitted for Codex only; lock files written for all platforms | `generate-adapters.py:311` vs `install.sh:169–177` |
| 5 | Test name `test_all_platforms_share_identical_behavior` overclaims — proves text identity, not behavioral equivalence | Test implementation (line 372) vs Decisions 83, 84, 85 |
| 6 | Unreferenced files copied to adapters — 5/7 references are broadcast to skills that never mention them | Grep of all canonical skills for each reference filename |

---

## 3. Accepted Decisions

| # | Decision | Key constraint |
|---|----------|---------------|
| 82 | Namespace rewriting is a semantic no-op | Deterministic bijection; test is correct to apply it before comparing |
| 83 | Capability descriptions may name aspirational behaviors | Degradation gates on capability declarations, not description prose |
| 84 | Every capability classified on any platform must be classified on all platforms | Prevents latent cross-platform gaps |
| 85 | Codex-only pin-resolution is an untested assumption | Verify per-platform; document native precedence or emit paragraph |
| 86 | Replace inline degradation paraphrase with reference pointer | Match authority-rules pattern; eliminate dual-source risk |
| 87 | Generator must extract canonical description, not maintain a separate one | Single source of truth for trigger semantics |
| 88 | Narrow reference distribution to files the skill actually mentions | Eliminate context waste and false signals |
| 89 | Adapter change boundary: five permitted, four prohibited | Normative answer to the session's main question |
| 90 | Rename test to `test_all_platforms_share_identical_core_text` | Accurately represent what the test proves |
| 91 | Session 11 changes execute before Session 10's migration | One regeneration pass, not two |

---

## 4. Component Design

### 4.1 Extract canonical descriptions (Decision 87)

Remove the `descriptions` dict from `generate_frontmatter()` (lines 181–252). Replace with extraction from the canonical `SKILL.md` frontmatter:

1. Parse the `description:` field from the canonical frontmatter (single-line or multi-line YAML scalar).
2. Compact to a single line.
3. Encode as a JSON string for the generated YAML scalar.

If the compact trigger-action-boundary format is desired for adapter descriptions, update the 14 canonical skill frontmatter descriptions to use that format. The generator passes through, never rewrites semantics.

### 4.2 Replace degradation paraphrase with reference pointer (Decision 86)

In `generate_adapter_section()` (lines 348–358), replace the inline degradation protocol paraphrase:

**Before (lines 348–358):**
```
### Capability Degradation
This adapter classifies every required capability...
**Degradation rules**:
- **`manual-fallback`**: Pause with ONE concrete manual instruction...
- **`unsupported`**: Stop the affected path immediately...
- **Stricter safety wins**: When this platform imposes...
```

**After:**
```
### Capability Degradation

Apply `references/CAPABILITY-DEGRADATION.md`. Per-capability classifications and notes below.
```

Keep the per-capability `####` blocks (lines 360–383) — they emit platform-specific classification and notes, not protocol rules.

### 4.3 Narrow reference distribution (Decision 88)

In `build_reference_entries()` (line 507), scan the skill's core body for each reference filename before copying:

```python
body = extract_body(core_skill_dir / "SKILL.md")
for filename in SHARED_REFERENCES:
    if Path(filename).name in body:
        # copy and add to entries
```

Update `test_installed_skills_include_their_declared_references` (line 266) to check only references the skill actually mentions, not the full static list.

### 4.4 Symmetric capability classification (Decision 84)

Add validation to the generator (before generation, alongside `validate_authority_blocks()`):

1. Collect all capability names classified in any overlay.
2. For each capability, verify it exists in all three overlays.
3. Fail with a clear message naming the missing overlay and capability.

Add `subagent_isolation` and `parallel_tool_execution` to the overlays that are missing them:

| Capability | Add to | Classification |
|---|---|---|
| `subagent_isolation` | `codex/overlay.yaml` | native |
| `subagent_isolation` | `github-copilot/overlay.yaml` | manual-fallback |
| `parallel_tool_execution` | `codex/overlay.yaml` | native |

Classifications are initial proposals — verify against actual platform behavior before committing.

### 4.5 Rename test (Decision 90)

In `tests/test_generate_adapters.py`:

- Rename `test_all_platforms_share_identical_behavior` → `test_all_platforms_share_identical_core_text`.
- Update docstring to: "the core body text is byte-identical across platforms — this guarantees no platform-specific rewriting but does not assert behavioral equivalence under different platform runtimes."

### 4.6 Document pin-resolution assumption (Decision 85)

Add a comment in `generate_adapter_section()` at line 311 documenting the assumption:

```python
# Pin-resolution paragraph emitted for Codex only. Assumption: Claude Code
# and GitHub Copilot skill loaders natively prefer project-pinned over global
# without explicit prose instruction. UNVERIFIED — see Decision 85
# (Session 11). Verify per-platform before adding or permanently omitting.
```

Add a test that explicitly asserts the current state (Claude Code and GitHub Copilot do NOT have the paragraph) so the assumption is visible and breakable:

```python
def test_pin_resolution_is_codex_only(self):
    """Pin-resolution paragraph is Codex-only. Decision 85: this is an
    unverified assumption about other platforms' native precedence."""
    for skill in core_skill_names():
        for platform in ["claude-code", "github-copilot"]:
            adapter = adapter_file(platform, skill).read_text()
            self.assertNotIn("### Runtime pin resolution", adapter)
```

### 4.7 Adapter regeneration and verification

After all code changes (4.1–4.6):

1. Run `python3 tools/generate-adapters.py` — regenerate all adapters with the new generator.
2. Run `python3 tools/generate-adapters.py --check` — confirm no drift.
3. Run `python3 -m pytest tests/test_generate_adapters.py` — confirm all tests pass (including renamed test and new tests).
4. Run `python3 tools/verify-conformance.py --structure` — confirm structural conformance.

---

## 5. Dependency Order

```
Extract canonical descriptions (4.1)
        │
        ▼
Replace degradation paraphrase (4.2)
        │
        ▼
Narrow reference distribution (4.3)
        │
        ▼
Symmetric capability classification (4.4)
        │
        ▼
Rename test + document pin assumption (4.5, 4.6)  ← can be parallel
        │
        ▼
Regeneration and verification (4.7)
        │
        ▼
Session 10's migration (steps 1–18)
```

Steps 4.1–4.3 modify the generator and must precede regeneration. Step 4.4 modifies overlays. Steps 4.5–4.6 modify tests and can be parallel with each other. Step 4.7 regenerates and verifies. Session 10's migration follows.

---

## 6. Migration Steps

| # | Step | Files touched | Verification |
|---|------|---------------|--------------|
| 1 | Update 14 canonical skill descriptions to compact trigger-action-boundary format | `skills/core/*/SKILL.md` (frontmatter only) | Read each frontmatter; confirm `description:` uses "Use when..." format with boundary clause |
| 2 | Remove `descriptions` dict from generator; extract description from canonical frontmatter | `tools/generate-adapters.py` (lines 179–271) | Generator runs without error; descriptions in generated adapters match canonical sources |
| 3 | Replace degradation paraphrase with reference pointer in generator | `tools/generate-adapters.py` (lines 348–358) | Generator runs; generated adapters contain "Apply `references/CAPABILITY-DEGRADATION.md`" instead of inline rules |
| 4 | Add body-scanning to `build_reference_entries()` in generator | `tools/generate-adapters.py` (line 507) | Generator runs; adapters only contain referenced files in their `references/` directory |
| 5 | Update `SHARED_REFERENCES` constant or remove it if scanning replaces it | `tools/generate-adapters.py` (line 37) | No hardcoded broadcast list; reference set is derived from body content |
| 6 | Add `subagent_isolation` to Codex and GitHub Copilot overlays | `adapters/codex/overlay.yaml`, `adapters/github-copilot/overlay.yaml` | grep confirms `subagent_isolation` classified in all three overlays |
| 7 | Add `parallel_tool_execution` to Codex overlay | `adapters/codex/overlay.yaml` | grep confirms `parallel_tool_execution` classified in all three overlays |
| 8 | Add symmetric classification validation to generator | `tools/generate-adapters.py` | Generator fails if a capability is classified in one overlay but not all three |
| 9 | Rename `test_all_platforms_share_identical_behavior` to `test_all_platforms_share_identical_core_text` | `tests/test_generate_adapters.py` (line 372) | Test exists with new name; old name absent |
| 10 | Add `test_pin_resolution_is_codex_only` documenting Decision 85 assumption | `tests/test_generate_adapters.py` | Test passes; documents the assumption |
| 11 | Add comment at generator line 311 documenting pin-resolution assumption | `tools/generate-adapters.py` | Comment present at the conditional |
| 12 | Update `test_installed_skills_include_their_declared_references` to check only referenced files | `tests/test_generate_adapters.py` (line 266) | Test passes with narrowed expectations |
| 13 | Run `python3 tools/generate-adapters.py` | All `adapters/*/skills/*/SKILL.md`, `adapters/*/manifest.json`, `adapters/*/SHA256SUMS` | Generator exits 0 |
| 14 | Run `python3 tools/generate-adapters.py --check` | All generated files | `--check` exits 0 |
| 15 | Run `python3 -m pytest tests/test_generate_adapters.py` | Test file | All tests pass |
| 16 | Run `python3 tools/verify-conformance.py --structure` | All generated files | Structural conformance passes |
| 17 | Run `python3 -m pytest tests/` | All test files | Full suite passes |

---

## 7. Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| Canonical descriptions in legacy multi-line format may lose information when compacted | Review each description during step 1; preserve all semantic content in the compact format |
| Removing `SHARED_REFERENCES` broadcast may break skills that reference files indirectly (via another reference file) | Scan for transitive references; if found, document and include them explicitly |
| Symmetric classification requires choosing correct classifications for `subagent_isolation` (Codex, Copilot) and `parallel_tool_execution` (Codex) | Mark initial classifications as proposals in the overlay comments; verify against platform documentation |
| Narrowing reference distribution changes SHA256SUMS and manifests | Expected — step 13 regenerates all checksums; step 14 verifies |
| Generator description extraction must handle both single-line and multi-line YAML frontmatter | The generator already has a YAML parser (`parse_yaml`); extend it or add a dedicated frontmatter extractor |

---

## 8. Verification Criteria

The change is complete when:

1. `python3 tools/generate-adapters.py --check` exits 0 (generated files match).
2. `python3 tools/verify-conformance.py --structure` exits 0 (structural invariants hold).
3. `python3 -m pytest tests/` passes with no failures.
4. No generated adapter contains the `descriptions` dict's independently authored text — all descriptions match canonical frontmatter.
5. No generated adapter contains the inline degradation paraphrase — all contain the reference pointer.
6. Every adapter's `references/` directory contains only files mentioned in that skill's core body.
7. Every capability classified in any overlay is classified in all three overlays.
8. `test_all_platforms_share_identical_core_text` exists; `test_all_platforms_share_identical_behavior` does not.
9. `test_pin_resolution_is_codex_only` exists and passes.
10. Session 10's migration (steps 1–18) can execute cleanly after this plan completes.

---

## 9. What This Does Not Cover

- **Pin-resolution verification for Claude Code and GitHub Copilot.** Decision 85 flags the assumption but does not resolve it. Verification requires testing each platform's actual skill-loader precedence behavior — a runtime investigation, not a generator change.
- **Behavioral equivalence testing.** Decision 90 renames the test to stop overclaiming, but does not add a test that actually verifies behavioral equivalence across platforms. Such a test would require runtime execution on each platform — outside the generator's scope.
- **Session 10's 18-step migration.** This plan sequences before Session 10 (Decision 91) but does not execute Session 10's steps. Those remain as documented in `docs/design/capability-degradation-component-plan.md`.
- **Dead classification cleanup beyond symmetry.** Decision 84 ensures every capability is classified everywhere, but does not evaluate whether the classifications are correct. Verification against platform documentation is a separate step.
- **Canonical description format enforcement.** Decision 87 makes the generator extract descriptions, but does not add a test enforcing that canonical descriptions use the trigger-action-boundary format. If a canonical description is later written in a different format, the generator will pass it through.
