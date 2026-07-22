# Authority and Sensitivity Component Plan

**Date:** 2026-07-21
**Source:** Grilling Session 8 (Decisions 53–62)
**Status:** Accepted — not yet executed
**Prior session:** Session 7 (Evidence Model) — see `docs/design/evidence-model-component-plan.md`
**Evidence trail:** `docs/design/grilling-session-8-authority-sensitivity.md`

---

## 1. Current-State Findings

### Authority model

Two independent axes govern gates:
- **Consequence** (low / meaningful / high) — determines whether the agent may proceed or must ask first, per `references/CONSEQUENCE-AUTHORITY.md:25-35`.
- **Sensitivity** (ordinary / private / restricted) — determines storage rules. After ADR 0019, restricted-sensitivity body writes are gated with "ask first" at all consequence levels.

Authority is assigned at Work Object creation via YAML frontmatter. The agent or user sets `consequence:` and `sensitivity:`. Neither field is validated, re-evaluated, or checked by any tool.

### Enforcement landscape

- **Every authority gate is enforced exclusively through prompt instructions.** No pre-commit hook, CLI validator, schema checker, file-system permission, or platform-level gate prevents any prohibited action.
- The only technical enforcement is `.gitignore` excluding `.work-studio/objects/` from Git — bypassable with `git add -f`.
- All Git hooks are `.sample` files. Zero active hooks.
- `tools/` contains `install.sh`, `generate-adapters.py`, `verify-conformance.py`, `prompt_payload_tracer.py`. None validate authority, sensitivity, or consequence at write time.
- ADR 0019 (`docs/adr/0019:91,105-107`) explicitly acknowledges: "no machine enforcement exists, and none is planned before the CLI session."

### Real usage

- All 20 Work Objects: `sensitivity: ordinary`. Zero `private`, zero `restricted`.
- Consequence distribution: 2 `low`, 18 `meaningful`, 0 `high`.
- The Work Object implementing the sensitivity gate system itself is `meaningful` despite governing safety mechanisms that the system's own definition places at `high`.
- Authority is never recorded. When an agent "asks first" and gets permission, the authorization lives only in ephemeral chat history.

### Test coverage

- `test_high_consequence_objects_cannot_be_staged_without_confirmation` (`tests/test_generate_adapters.py:180`) verifies authority gate prose is present in all generated adapters across all platforms. This tests prose presence, not runtime enforcement — but establishes the pattern for testing structural reachability.

---

## 2. Contradictions and Risks

| # | Finding | Evidence |
|---|---------|----------|
| 1 | Authority is requested but never recorded — gates are unauditable | `CONSEQUENCE-AUTHORITY.md:25-35` says "ask first" but no mechanism records the answer |
| 2 | Consequence is systematically under-assigned (0/20 objects at `high`) | `.work-studio/objects/` grep; the sensitivity-gates object itself is `meaningful` |
| 3 | The authority model doesn't protect itself — constitutional files are unguarded | `references/CONSEQUENCE-AUTHORITY.md` has no frontmatter, no gate applies to modifying it |
| 4 | `.gitignore` is the sole private-sensitivity enforcement — bypassable, doesn't prevent misplacement | `.gitignore:17-21`; nothing checks that private content is placed in `.work-studio/` |
| 5 | Every runtime gate depends on agent prose-compliance — external-effect actions (deploy, export, delete) are unstoppable | ADR 0019:91; no platform-agnostic runtime prevention mechanism exists |
| 6 | Skill authority checks are cross-referenced, not inlined — structurally unreachable (same pattern ADR 0019 diagnosed) | Skill profiles in `SKILL-AWARE-GRILLING.md` reference `CONSEQUENCE-AUTHORITY.md`; action instructions in `SKILL.md` don't contain the check |

---

## 3. Accepted Decisions

### Decision 53 — Authority must be recorded, not just requested

When the system requires "ask first" authority for an action, the authorization and its scope must be recorded in the Work Object's History section — not left in ephemeral chat.

### Decision 54 — Authority records are structured History entries

A gated-action History entry must capture: (1) the gated action name, (2) the scope granted (affected files, systems, or objects), (3) the evidence reviewed before granting, and (4) any constraints the user attached. Non-gated History entries remain freeform.

### Decision 55 — Pre-commit hook as first enforcement layer

Implement a Git pre-commit hook with five validations (see §5 below). Does not wait for the planned CLI.

### Decision 56 — Runtime enforcement must be platform-agnostic

No Claude Code hooks, Codex-specific middleware, or other single-platform enforcement mechanisms. Runtime enforcement lives in the platform-agnostic core or waits.

### Decision 57 — Inline authority checks at point of action in each skill

Each skill's `SKILL.md` must inline the authority check at the exact point where an irreversible or gated action is described. Checks are derived from the canonical `CONSEQUENCE-AUTHORITY.md` reference, not independent of it. The generator can produce them.

### Decision 58 — Consequence assignment requires a three-question structural prompt

Before setting `consequence:` in frontmatter, the agent must answer:
1. Is the action reversible? (If no → at least `meaningful`)
2. Does it affect systems or people beyond this workspace? (If yes → at least `meaningful`)
3. Could a failure here affect safety, privacy, or money? (If yes → `high`)

All three answers recorded in the Work Object's first History entry.

### Decision 59 — Authority records distinguish accepted-recommendation from independent-authorization

The structured authority History entry includes `authority_mode`:
- `accepted-recommendation` — the agent proposed, the user confirmed.
- `independent-authorization` — the user directed the action without an agent recommendation.

### Decision 60 — Accept auditable-but-not-preventable gap for external-effect actions

Five action categories (export, destructive, schema migration, external writes, deployment) are auditable but not preventable until a platform-agnostic CLI exists. The CLI becomes the highest-priority enforcement deliverable.

### Decision 61 — Pre-commit hook rejects misplaced private/restricted files

Staged files outside `.work-studio/` carrying `sensitivity: private` or `sensitivity: restricted` in YAML frontmatter are rejected.

### Decision 62 — Pre-commit hook protects constitutional files

Modifications to files on a declared constitutional-files list require a linked authority record in the commit message or an explicit `CONSTITUTIONAL-OVERRIDE:` bypass tag.

---

## 4. Target Component Boundary

### What this plan changes

| Component | Current state | Target state |
|-----------|--------------|--------------|
| Authority recording | Nonexistent | Structured History entries with action, scope, evidence, constraints, authority mode |
| Pre-commit hook | Zero active hooks | Five-check validation (see §5) |
| Consequence assignment | One-line definitions, set by habit | Three-question structural prompt, answers recorded |
| Skill authority checks | Cross-referenced from `CONSEQUENCE-AUTHORITY.md` | Inlined at point of action in each `SKILL.md` |
| Constitutional file protection | None | Declared list + hook check |
| Recommendation vs. authorization | No distinction | `authority_mode` field in authority History entries |

### What this plan does NOT change

- The three consequence levels (low / meaningful / high) — definitions are refined, not replaced.
- The three sensitivity classes (ordinary / private / restricted) — enforcement is added, definitions unchanged.
- The Authority gates table structure — rows are added (ADR 0019), not reorganized.
- The `AGREEMENT-LOOP.md` engine — no changes to the conversational contract.
- Platform-specific adapter behavior — enforcement is platform-agnostic.

---

## 5. Recommended Architecture

### Pre-commit hook: five checks

The hook is a single executable (shell or Python) installed to `.git/hooks/pre-commit`.

| # | Check | Trigger | Action on failure |
|---|-------|---------|-------------------|
| 1 | Restricted-content pointer-only | Staged Work Object with `sensitivity: restricted` has inline body content | Reject commit; name file |
| 2 | High-consequence authority record | Staged Work Object with `consequence: high` and `state:` beyond `draft` has no structured authority History entry | Reject commit; require authority entry |
| 3 | Private data in Git | Any file under `.work-studio/objects/` is staged | Reject commit; remind to unstage |
| 4 | Misplaced sensitive files | Staged file outside `.work-studio/` has `sensitivity: private` or `restricted` in frontmatter | Reject commit; instruct to move or reclassify |
| 5 | Constitutional file protection | Staged file on the constitutional-files list is modified without a linked authority record or `CONSTITUTIONAL-OVERRIDE:` tag in commit message | Reject commit; name file and requirement |

**Configuration:** The constitutional-files list lives in `.work-studio/constitutional-files.list` (itself on the list).

### Structured authority History entry format

```markdown
### YYYY-MM-DDTHH:MM:SSZ — Authority: <gated action name>

- **Scope:** <affected files, systems, or objects>
- **Evidence reviewed:** <what was checked before granting>
- **Constraints:** <any limits the user attached, or "none">
- **Authority mode:** accepted-recommendation | independent-authorization
- **Granted by:** <user identifier or "conversation">
```

### Consequence assignment prompt

Recorded as the first History entry on Work Object creation:

```markdown
### YYYY-MM-DDTHH:MM:SSZ — Consequence assessment

- **Reversible?** yes | no → <implication>
- **Affects beyond workspace?** yes | no → <implication>
- **Failure affects safety/privacy/money?** yes | no → <implication>
- **Assigned consequence:** low | meaningful | high
```

### Inlined authority checks in skills

Each `SKILL.md` that describes a gated action must contain an authority block at the point of action:

```markdown
**Authority gate:** This action (<name>) requires explicit human confirmation
at <consequence threshold>+ consequence. Before proceeding: (1) verify the
Work Object's consequence and sensitivity fields, (2) request confirmation
naming the action and scope, (3) record a structured authority History entry
per the authority recording contract.
```

The generator (`tools/generate-adapters.py`) can inject these blocks from `CONSEQUENCE-AUTHORITY.md` during adapter generation, keeping the canonical reference as the single source while ensuring reachability.

---

## 6. Migration Steps

All steps are documentation and tooling changes. No Work Objects need modification. No existing behavior changes for `ordinary`-sensitivity, `low`/`meaningful`-consequence objects.

| # | Step | Files affected | Dependency |
|---|------|---------------|------------|
| 1 | Create the pre-commit hook script with five checks | `.git/hooks/pre-commit` (new) | None |
| 2 | Create the constitutional-files list | `.work-studio/constitutional-files.list` (new) | Step 1 |
| 3 | Add the structured authority History entry format to `CONSEQUENCE-AUTHORITY.md` | `references/CONSEQUENCE-AUTHORITY.md` | None |
| 4 | Add the consequence three-question prompt to `CONSEQUENCE-AUTHORITY.md` | `references/CONSEQUENCE-AUTHORITY.md` | None |
| 5 | Add the `authority_mode` field definition to `CONSEQUENCE-AUTHORITY.md` | `references/CONSEQUENCE-AUTHORITY.md` | Step 3 |
| 6 | Inline authority checks into each core skill's `SKILL.md` at gated action points | `skills/core/*/SKILL.md` (up to 14 files) | Steps 3–5 |
| 7 | Update `tools/generate-adapters.py` to inject authority blocks from the canonical reference | `tools/generate-adapters.py` | Step 6 |
| 8 | Regenerate all adapters | `adapters/*/skills/*/SKILL.md` | Step 7 |
| 9 | Add tests for inlined authority checks (extend pattern from `test_high_consequence_objects_cannot_be_staged_without_confirmation`) | `tests/test_generate_adapters.py` | Step 8 |
| 10 | Add tests for pre-commit hook behavior | `tests/test_pre_commit_hook.py` (new) | Step 1 |
| 11 | Produce ADR documenting Decisions 53–62 | `docs/adr/0023-*.md` (new) | All above |

---

## 7. Tests and Evidence Required

### Pre-commit hook tests

| Test | Validates |
|------|-----------|
| Staged `sensitivity: restricted` Work Object with inline body content → commit rejected | Check 1 |
| Staged `sensitivity: restricted` Work Object with pointer-only body → commit succeeds | Check 1 (negative) |
| Staged `consequence: high` Work Object past `draft` without authority entry → commit rejected | Check 2 |
| Staged `consequence: high` Work Object past `draft` with authority entry → commit succeeds | Check 2 (negative) |
| Staged file under `.work-studio/objects/` → commit rejected | Check 3 |
| Staged file outside `.work-studio/` with `sensitivity: private` frontmatter → commit rejected | Check 4 |
| Staged constitutional file without linked authority or override tag → commit rejected | Check 5 |
| Staged constitutional file with `CONSTITUTIONAL-OVERRIDE:` tag → commit succeeds | Check 5 (bypass) |

### Generator tests

| Test | Validates |
|------|-----------|
| Every skill with a gated action contains the inlined authority block | Decision 57 |
| Authority block text matches the canonical `CONSEQUENCE-AUTHORITY.md` reference | Decision 57 (drift prevention) |
| Consequence three-question prompt is present in conductor skill | Decision 58 |

### Behavioral scenario tests

| Test | Validates |
|------|-----------|
| A `high`-consequence Work Object creation produces a three-question consequence assessment in its first History entry | Decision 58 |
| A gated action on a `high`-consequence object produces a structured authority History entry | Decisions 53–54 |
| `do recommended` on a gated action records `authority_mode: accepted-recommendation` | Decision 59 |
| A user-initiated gated action records `authority_mode: independent-authorization` | Decision 59 |

---

## 8. Deferred Decisions

| # | Topic | Reason deferred | Revisit trigger |
|---|-------|----------------|-----------------|
| 1 | Platform-specific runtime enforcement (Decision 56) | User decision: Work Studio must remain platform-agnostic | A platform hook system maps to the adapter overlay pattern |
| 2 | CLI as primary enforcement path (Decision 60) | No CLI design exists; the five external-effect action categories are the CLI's primary targets | CLI design session begins |
| 3 | `[system]`-entry redaction boundary (from Session 7) | Out of scope for this session | Evidence Model migration (Session 7 component plan) |
| 4 | Consequence three-question calibration (Decision 58) | Untested — may need adjustment | After 10 Work Objects created under the new rule |
| 5 | Authority mode utility (Decision 59) | Untested — may be unnecessary precision | After 5 outcome reviews with recorded authority |
| 6 | Constitutional-files list drift (Decision 62) | List is small today; manual maintenance is adequate | List grows beyond ~10 files |
| 7 | Non-frontmatter sensitivity marking (Decision 61) | Only Work Objects carry frontmatter today | Non-Work-Object files with private content become common |

---

## 9. Smallest Tracer Bullet

**Implement the pre-commit hook (Step 1) with Check 3 only** — reject staged files under `.work-studio/objects/`.

This is the smallest change that produces a technical enforcement mechanism where none existed. It validates the hook infrastructure (installation, execution, error messaging) without requiring any schema parsing or frontmatter reading. All five checks build on the same hook; getting Check 3 working proves the delivery path for Checks 1, 2, 4, and 5.

**Exit evidence:** `git add -f .work-studio/objects/README.md && git commit -m "test"` is rejected by the hook with a clear error message.

**Falsifying result:** The commit succeeds despite `.work-studio/objects/` being staged — the hook is not installed, not executable, or not checking the right paths.
