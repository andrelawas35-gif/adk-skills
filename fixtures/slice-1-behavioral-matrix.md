# Work Studio Behavioral Matrix

This matrix maps every implemented Work Studio behavioral requirement to its expected outcome
per platform. It is the canonical reference for the conformance gate — CI
verifies that every scenario is documented, every platform is accounted for,
and no adapter claims behavior it cannot deliver.

## Legend

| Symbol | Meaning |
|--------|---------|
| ✅ | Pass — capability is native and adapter satisfies the requirement |
| ⚠️ | Manual-fallback — requires human step; adapter discloses and records gap |
| ❌ | Unsupported — platform cannot satisfy; adapter stops and records limitation |
| — | Not applicable — scenario does not exercise this platform's capabilities |

---

## Discovery and Workspace

| ID | Scenario | Codex | Claude Code | GitHub Copilot |
|----|----------|-------|-------------|----------------|
| D1 | Search upward for `.work-studio/config.md` | ✅ | ✅ | ✅ |
| D2 | Stop at repository boundary (`.git`) | ✅ | ✅ | ✅ |
| D3 | Never scan home directory automatically | ✅ | ✅ | ✅ |
| D4 | Report workspace name from config | ✅ | ✅ | ✅ |

Source: `fixtures/slice-1-initialize-and-resume.md` Scenarios 1

---

## Work Object Creation

| ID | Scenario | Codex | Claude Code | GitHub Copilot |
|----|----------|-------|-------------|----------------|
| C1 | Classify signal into type (inquiry/project/change/incident) | ✅ | ✅ | ✅ |
| C2 | Generate immutable time-sortable ID | ✅ | ✅ | ✅ |
| C3 | Create file at `.work-studio/objects/YYYY/MM/<id>-<slug>.md` | ✅ | ✅ | ✅ |
| C4 | Valid YAML frontmatter with all required fields | ✅ | ✅ | ✅ |
| C5 | Body contains stub sections | ✅ | ✅ | ✅ |
| C6 | Creation History entry appended | ✅ | ✅ | ✅ |
| C7 | `active.md` updated with Primary role | ✅ | ✅ | ✅ |
| C8 | No hidden reasoning, prompts, or transcripts stored | ✅ | ✅ | ✅ |

Source: `fixtures/slice-1-initialize-and-resume.md` Scenarios 2

---

## Work Object Resumption

| ID | Scenario | Codex | Claude Code | GitHub Copilot |
|----|----------|-------|-------------|----------------|
| R1 | Locate file by ID glob | ✅ | ✅ | ✅ |
| R2 | Read full Work Object | ✅ | ✅ | ✅ |
| R3 | Report title, type, status, state, next_action | ✅ | ✅ | ✅ |
| R4 | Does not depend on chat history | ✅ | ✅ | ✅ |
| R5 | Does not replay full evidence ledger | ✅ | ✅ | ✅ |

Source: `fixtures/slice-1-initialize-and-resume.md` Scenarios 3

---

## Pressure-Testing and Decision

| ID | Scenario | Codex | Claude Code | GitHub Copilot |
|----|----------|-------|-------------|----------------|
| P1 | Sort all claims into provenance lanes | ✅ | ✅ | ✅ |
| P2 | Identify highest-leverage decision | ✅ | ✅ | ✅ |
| P3 | Recommend exactly one branch with confidence | ✅ | ✅ | ✅ |
| P4 | Ask exactly one decision-bearing question | ✅ | ✅ | ✅ |
| P5 | "Do recommended" accepts only preceding recommendation | ✅ | ✅ | ✅ |
| P6 | Surface edge case, assumption, and future friction | ✅ | ✅ | ✅ |
| P7 | Sharpen vague language before recording | ✅ | ✅ | ✅ |

Source: `fixtures/slice-1-pressure-test-and-record.md` Scenarios 1-5

---

## Decision Persistence

| ID | Scenario | Codex | Claude Code | GitHub Copilot |
|----|----------|-------|-------------|----------------|
| S1 | Write to Decisions and revisit triggers section | ✅ | ✅ | ✅ |
| S2 | Record branch chosen, alternatives, rationale, trade-offs | ✅ | ✅ | ✅ |
| S3 | Append History entry with timestamp, actor, platform, rationale | ✅ | ✅ | ✅ |
| S4 | Update frontmatter state and updated_at | ✅ | ✅ | ✅ |
| S5 | Immutable fields (id, type, created_at) unchanged | ✅ | ✅ | ✅ |
| S6 | No hidden reasoning or chat transcripts | ✅ | ✅ | ✅ |
| S7 | ADR created only when all three criteria met | ✅ | ✅ | ✅ |

Source: `fixtures/slice-1-pressure-test-and-record.md` Scenarios 6, 11

---

## Concurrency and Authority

| ID | Scenario | Codex | Claude Code | GitHub Copilot |
|----|----------|-------|-------------|----------------|
| A1 | Re-read before write, check updated_at | ✅ | ✅ | ✅ |
| A2 | Detect conflict when updated_at changed | ✅ | ✅ | ✅ |
| A3 | Report conflict with both timestamps | ✅ | ✅ | ✅ |
| A4 | Do not overwrite on conflict | ✅ | ✅ | ✅ |
| A5 | Offer re-read and retry | ✅ | ✅ | ✅ |

Source: `fixtures/slice-1-initialize-and-resume.md` Scenarios 6,
`fixtures/slice-1-pressure-test-and-record.md` Scenarios 7

---

## Authority Gates

| ID | Scenario | Codex | Claude Code | GitHub Copilot |
|----|----------|-------|-------------|----------------|
| G1 | Stop before unrequested implementation | ✅ | ✅ | ✅ |
| G2 | Stop before export or external write | ✅ | ✅ | ✅ |
| G3 | Stop before destructive action or migration | ✅ | ✅ | ✅ |
| G4 | High-consequence decisions require explicit confirmation | ✅ | ✅ | ✅ |
| G5 | Generic acceptance cannot stage or mutate a high-consequence decision | ✅ | ✅ | ✅ |

Source: `fixtures/slice-1-pressure-test-and-record.md` Scenarios 4b, 8-10,
`fixtures/slice-1-initialize-and-resume.md` Scenarios 7-8

---

## Capability Degradation

| ID | Scenario | Codex | Claude Code | GitHub Copilot |
|----|----------|-------|-------------|----------------|
| DG1 | Every capability classified as native/manual-fallback/unsupported | ✅ | ✅ | ✅ |
| DG2 | Native capabilities proceed without degradation message | ✅ | ✅ | ✅ |
| DG3 | Manual-fallback pauses with one concrete instruction | ✅ | ✅ | ✅ |
| DG4 | Manual-fallback records gap in History | ✅ | ✅ | ✅ |
| DG5 | Unsupported stops path and records limitation | ✅ | ✅ | ✅ |
| DG6 | No false verification for unavailable capabilities | ✅ | ✅ | ✅ |
| DG7 | Stricter platform safety constraints take precedence | ✅ | ✅ | ✅ |
| DG8 | Platform limitations declared, not hidden | ✅ | ✅ | ✅ |

Source: `fixtures/slice-1-capability-degradation.md` All scenarios

---

## Signal Capture and Activation

| ID | Scenario | Codex | Claude Code | GitHub Copilot |
|----|----------|-------|-------------|----------------|
| T1 | Preserve a live signal in the user's language | ✅ | ✅ | ✅ |
| T2 | Classify without creating a Work Object | ✅ | ✅ | ✅ |
| T3 | Route explicit activation through the conductor | ✅ | ✅ | ✅ |
| T4 | Require an approved Evidence Bridge for personal context | ✅ | ✅ | ✅ |
| T5 | Disclose manual-fallback or unsupported capability paths | ✅ | ✅ | ✅ |

Source: `fixtures/slice-2-turn-signal-into-work.md` All scenarios

---

## Generated-Artifact Integrity

| ID | Scenario | Codex | Claude Code | GitHub Copilot |
|----|----------|-------|-------------|----------------|
| I1 | Regeneration without source changes produces byte-for-byte identical output | ✅ | ✅ | ✅ |
| I2 | Manifest checksums match generated files | ✅ | ✅ | ✅ |
| I3 | SHA256SUMS match generated files | ✅ | ✅ | ✅ |
| I4 | --check mode detects drift in any artifact | ✅ | ✅ | ✅ |
| I5 | Core body preserved verbatim in all adapters | ✅ | ✅ | ✅ |
| I6 | Adapter only appends Platform Adapter section | ✅ | ✅ | ✅ |

Source: `tests/test_generate_adapters.py`

---

## Summary

| Platform | Total scenarios | ✅ Pass | ⚠️ Manual-fallback | ❌ Unsupported |
|----------|----------------|---------|---------------------|---------------|
| Codex | 56 | 56 | 0 | 0 |
| Claude Code | 56 | 56 | 0 | 0 |
| GitHub Copilot | 56 | 56 | 0 | 0 |

> Note: All documented behavioral scenarios exercise capabilities that are native on
> all three platforms. Manual-fallback and unsupported classifications exist
> in the capability catalog (browser_automation, subagent_isolation,
> parallel_tool_execution, web_search) but are not exercised by the Slice 1
> behavioral scenarios — those capabilities are required by later slices
> (verify-release-evidence, code-review, etc.). Signal capture exercises the
> required degradation behavior in its fixture without claiming a native result.
>
> When a scenario requiring a non-native capability is added in a later slice,
> the matrix will be updated and the capability degradation fixture
> (`slice-1-capability-degradation.md`) will exercise the fallback paths.

## CI Verification

The GitHub Actions workflow at `.github/workflows/slice-1-conformance.yml`
enforces this matrix by:

1. Running `python3 tools/generate-adapters.py --check` (drift detection)
2. Verifying the matrix is complete (all fixtures referenced)
3. Checking adapter structure against behavioral requirements
4. Validating manifest and SHA256SUMS checksums
5. Running the generator contract test suite
6. Confirming Slice 1 is demonstrable from a clean checkout
