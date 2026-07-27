# Conflict fixture: epistemic tag contract reconciliation

This fixture documents the tag-contract conflict that `2026-07-27-012`
reconciles. It provides testable examples of both valid and invalid tag
usage for conformance testing after reconciliation.

## Conflict record

**Date:** 2026-07-27
**Work Object:** `2026-07-27-012` — Reconcile epistemic tag contract across
skills, validator, and fixtures.
**Normative source:** `references/AGREEMENT-LOOP.md` lines 96–111 — declares
exactly six base provenance tags: `[system]`, `[decision]`, `[inference]`,
`[gap]`, `[testimony]`, `[memory]`.
**Resolution:** Option A — subtypes use governed colon syntax within the base
tag bracket, enumerated in `references/epistemic/taxonomy.yaml`.

## Pre-reconciliation (conflict state)

Before `2026-07-27-012`, the following undeclared tags were in use across
core skills:

| Tag | Used in | Disposition |
|-----|---------|-------------|
| `[source]` | `research-investigate-live-question` output template | Changed to `[system]` |
| `[lived]` | `research-investigate-live-question`, `review-outcome-and-adapt` output templates | Changed to `[testimony]` |
| `[lived]` | `diagnose-production-incident` output template | Changed to `[testimony]` |
| `[unresolved]` | `diagnose-production-incident` output template | Changed to `[gap]` |
| `[unresolved]` | `pressure-test-decision` inline definition block | Changed to `[gap]` |
| `[evidence/lived]` | `pressure-test-decision` inline definition block | Changed to `[testimony]` |
| `[evidence/source]` | `pressure-test-decision` inline definition block | Changed to `[system]` |
| `[evidence/system]` | `pressure-test-decision` inline definition block | Changed to `[system]` |

And the following subtype syntax was in use without governance:

| Token | Used in | Status |
|-------|---------|--------|
| `[system:discovery]` | 3 core skills, 1 Work Object | Registered in taxonomy |
| `[system:predecessor]` | 1 Work Object | Registered in taxonomy |
| `[system:plan]` | 1 Work Object | Registered in taxonomy |

## Valid tag examples (post-reconciliation)

These should all pass `ws epistemic lint`:

```markdown
# Example evidence entries

- 2026-07-27T12:00:00Z — [system] Code inspection revealed ...
- 2026-07-27T12:01:00Z — [decision] Owner confirmed ...
- 2026-07-27T12:02:00Z — [inference] The evidence suggests ...
- 2026-07-27T12:03:00Z — [gap] Could not determine ...
- 2026-07-27T12:04:00Z — [testimony] User reported ...
- 2026-07-27T12:05:00Z — [memory] Workspace preference recorded ...

# Registered subtype examples (valid governed colon syntax)

- 2026-07-27T12:06:00Z — [system:discovery] Found 3 route definitions ...
- 2026-07-27T12:07:00Z — [system:predecessor] Continues from 2026-07-21-008 ...
- 2026-07-27T12:08:00Z — [system:plan] Per docs/design/tracer-bullet.md ...
```

## Invalid tag examples (post-reconciliation)

These should all **fail** `ws epistemic lint`:

```markdown
# Undeclared base tags

- 2026-07-27T12:10:00Z — [source] External reference material ...
- 2026-07-27T12:11:00Z — [lived] Direct observation ...
- 2026-07-27T12:12:00Z — [unresolved] Not yet classified ...

# Unregistered subtype pairs

- 2026-07-27T12:13:00Z — [system:unknown] Not in taxonomy ...
- 2026-07-27T12:14:00Z — [decision:subtype] Not registered ...

# Slash syntax (not valid subtype notation)

- 2026-07-27T12:15:00Z — [evidence/lived] Invalid syntax ...
```

## Test assertions

```python
# Expected lint results for this fixture:
# - Pre-reconciliation table (5 undeclared base tags + 3 slash tokens): 8 issues
# - Invalid examples section (3 undeclared base tags): 3 issues
# - Invalid examples section (2 unregistered subtype pairs): 2 issues
# - Invalid examples section (1 slash token): 1 issue
# Total: 14 issues
#
# Note: the pre-reconciliation table documents the old (invalid) tag state
# and intentionally triggers lint. The valid examples block uses tags that
# pass lint, producing 0 issues.
```
