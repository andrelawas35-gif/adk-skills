# Grilling Session 8 — Authority and Sensitivity

**Date:** 2026-07-21
**Focus:** Where consequence is assigned, who can change it, whether gates are technically enforced, and what actions must become impossible without recorded authority.
**Status:** Converged — shared understanding confirmed
**Prior session:** Session 7 (Evidence Model) — see `docs/design/grilling-session-7-evidence-model.md`

---

## Evidence Ledger

### Observed

- `references/CONSEQUENCE-AUTHORITY.md:7-11` — Three consequence levels defined: low, meaningful, high. Consequence follows effects, not emotional intensity or urgency (line 13).
- `references/CONSEQUENCE-AUTHORITY.md:17-21` — Three sensitivity classes defined: ordinary, private, restricted — independent of consequence.
- `references/CONSEQUENCE-AUTHORITY.md:25-35` — Authority gates table gates by consequence level, with a restricted-sensitivity row added (line 29: "Write restricted-sensitivity body content → Ask first at all levels"). This confirms ADR 0019 Decision 52 **was executed** in the table.
- `.work-studio/objects/` — All 20 real Work Objects have `sensitivity: ordinary`. Zero instances of `private` or `restricted`.
- `.work-studio/objects/` — Consequence values: 2 objects `low`, 18 objects `meaningful`. Zero objects `high`.
- `.gitignore:17-21` — `.work-studio/active.md`, `inbox.md`, `objects/`, `adapter.lock` are Git-excluded. `.work-studio/config.md` is tracked (documented exception).
- `.git/hooks/` — All hooks are `.sample` files only. No active pre-commit, pre-push, or commit-msg hooks exist.
- `tools/` — Contains `install.sh`, `generate-adapters.py`, `verify-conformance.py`, `prompt_payload_tracer.py`. No tool validates authority, sensitivity, or consequence at write time.
- `docs/adr/0019-sensitivity-gates-authority-independently-of-consequence.md:91` — ADR explicitly acknowledges: "The gate is still prose-only — no machine enforcement exists, and none is planned before the CLI session."
- `docs/adr/0019-sensitivity-gates-authority-independently-of-consequence.md:105-107` — "Current enforcement: documented and wired in prose... No machine enforcement exists. Planned enforcement: the future CLI's write path will check sensitivity before allowing body mutation."
- Every skill profile in `SKILL-AWARE-GRILLING.md` specifies gates as prose conditions (e.g., "confirm the requested mutation is attention, ownership, external consequence, or lifecycle commitment") — no profile references executable code.
- `AGREEMENT-LOOP.md:52-53` — `just execute` "never bypasses safety, privacy, destructive-action, or external-commitment gates" — this is a prose instruction to the agent, not a runtime guard.

### Claimed (by the system documentation)

- `CONSEQUENCE-AUTHORITY.md` claims consequence follows actual effects, not emotional intensity or urgency.
- `CONSEQUENCE-AUTHORITY.md` claims restricted data is never stored in Work Objects (pointer-only).
- The conductor skill claims sole authority for persisting session state and checkpointing.
- ADR 0019 claims the restricted-sensitivity row was added to the Authority gates table.

### Inferred

- **Every authority gate in the system is enforced exclusively through prompt instructions.** There is no pre-commit hook, no CLI validator, no schema checker, no file-system permission, and no platform-level gate that prevents any prohibited action.
- An agent that ignores or misreads the Authority gates table can write restricted content, deploy, delete, export, or mutate any Work Object without encountering a technical barrier.
- The `.gitignore` entry for `.work-studio/objects/` is the system's only technical enforcement mechanism — it prevents private-sensitivity data from being committed to Git. But it does not prevent the data from being written in the first place, and `git add -f` bypasses it.
- Consequence assignment is done at Work Object creation by the agent (or user), written into YAML frontmatter, and never validated or re-evaluated. There is no mechanism to detect when a Work Object's actual effects have escalated beyond its declared consequence level.

### Decided (this session)

(None yet — session in progress)

### Open

- Q1: Does consequence accurately track the eight dimensions the user listed (actual effects, reversibility, blast radius, external impact, urgency, emotional intensity, cost, data exposure)?
- Q2: Where should enforcement move from prose to technical?
- Q3: What is the minimum viable set of actions that must be technically gated?

### Contradictions

- `CONSEQUENCE-AUTHORITY.md:13` says consequence follows effects, not urgency — but the high-consequence definition (line 10) includes "safety" and "production" which are urgency-adjacent. The boundary between "effects" and "urgency" is not operationally defined.
- ADR 0019 says "no machine enforcement exists, and none is planned before the CLI session" — but the system documents gates as if they are enforced. The gap between documented authority and actual enforcement is systematic, not incidental.

---

## Decisions Log

### Decision 53 — Authority must be recorded, not just requested

**Date:** 2026-07-21
**Confidence:** High — direct evidence from system inspection.
**Evidence:** Every "ask first" gate in `CONSEQUENCE-AUTHORITY.md:25-35` instructs the agent to request permission, but no mechanism records what was authorized, by whom, or when. Chat history is ephemeral. Work Objects are resumable across sessions (`AGREEMENT-LOOP.md:239`), but a resuming session cannot verify what a prior session authorized. The system's gates are both unenforced and unauditable.
**Decision:** When the system requires "ask first" authority for an action, the authorization and its scope must be recorded in the Work Object's History section (or an equivalent durable location) — not left in ephemeral chat.
**Trade-off:** Adds ceremony to every gated action. Acceptable because unrecorded authority means gates are neither enforceable nor auditable.
**Revisit trigger:** If a future CLI enforces gates at the write path, the recording mechanism should integrate with the CLI's audit log rather than duplicating it in History.
**What would change this:** If Work Studio were strictly single-session-only (no resumption, no handoff), the audit trail would be less critical. The conductor's explicit resumption promise makes it critical.

### Decision 54 — Authority records are structured History entries, not a separate section

**Date:** 2026-07-21
**Confidence:** High — structural reasoning from accepted Decision 53.
**Evidence:** History is the Work Object's sole chronological record (`CONSEQUENCE-AUTHORITY.md:29`, `AGREEMENT-LOOP.md:249`). ADR 0017 established History as append-only. Splitting authority records into a separate section would create two parallel timelines — a resuming session would need to reconcile them to understand what happened and when. A structured entry type inside History keeps the single timeline while adding the specificity that freeform prose lacks.
**Decision:** Authority records are structured entries within the existing `## History` section. A gated-action entry must capture: (1) the gated action name, (2) the scope granted (affected files, systems, or objects), (3) the evidence reviewed before granting, and (4) any constraints the user attached. Non-gated History entries remain freeform prose with a date.
**Trade-off:** Gated-action History entries become heavier than routine entries. Acceptable because these are exactly the actions where "what happened" must be unambiguous to a future session.
**Revisit trigger:** If the History section becomes too noisy to scan (e.g., more than half of entries are structured authority records), consider whether the structured entries should be collapsed or summarized in History with full detail in a linked section.
**What would change this:** If a future CLI provides its own audit log, authority records might live there instead — but the Work Object should still reference them for cross-session resumability.

### Decision 55 — Pre-commit hook as first enforcement layer, not waiting for CLI

**Date:** 2026-07-21
**Confidence:** Medium — the hook addresses the highest-risk bypass paths with existing infrastructure, but it is commit-time enforcement, not runtime enforcement. An agent can still violate gates within a session; the hook catches violations only when artifacts are committed.
**Evidence:** `.git/hooks/` contains only `.sample` files — zero active hooks. `tools/` has no write-time validator. ADR 0019 (`docs/adr/0019:91,105-107`) explicitly states no machine enforcement exists and punts to a future CLI with no timeline. The system has 20 Work Objects and a growing number of accepted decisions about gates (Decisions 52-54) that are enforced only by prose.
**Decision:** Implement a Git pre-commit hook as the first technical enforcement layer. The hook validates:
1. `sensitivity: restricted` Work Objects contain no inline body content (pointer-only rule from `CONSEQUENCE-AUTHORITY.md:21`).
2. `consequence: high` Work Objects have at least one structured authority History entry before status transitions beyond `draft`.
3. `.work-studio/objects/` files are not staged for commit on a tracked branch (defense-in-depth for `.gitignore`).
**Trade-off:** Commit-time enforcement misses runtime violations. Acceptable as a first layer because it turns the most dangerous violations from invisible to visible — a meaningful upgrade from prose-only, without requiring a CLI that has no delivery timeline.
**Revisit trigger:** When the CLI design session begins, decide whether the hook's checks migrate into the CLI write path (making the hook redundant) or remain as defense-in-depth alongside the CLI.
**What would change this:** If the CLI is expected within weeks, the hook may be throwaway work. Current evidence (no CLI code, no CLI design artifact, ADR 0019 says "planned" with no date) suggests indefinite timeline.

### Decision 56 — Runtime enforcement must be platform-agnostic; no platform-specific hooks

**Date:** 2026-07-21
**Confidence:** High — explicit user decision, consistent with the adapter system's design intent.
**Evidence:** `tools/generate-adapters.py` generates platform-specific installations for Claude Code, Codex, Copilot, and GitHub from a shared core (`skills/core/`). The adapter overlay system (`adapters/*/overlay.yaml`) maps abstract capabilities to platform tools. The entire architecture is built around platform-agnostic core skills with platform-specific wiring. A Claude Code pre-tool hook would be the first mechanism that exists on only one platform — breaking the invariant.
**Decision:** Runtime enforcement must not be platform-specific. No Claude Code hooks, Codex-specific middleware, or other single-platform enforcement mechanisms for authority gates. Runtime enforcement either lives in the platform-agnostic core (skills, the pre-commit hook, or a future CLI) or waits.
**Trade-off:** This means runtime enforcement before irreversible actions (deploy, export, delete) remains prose-only until a platform-agnostic mechanism exists. The pre-commit hook (Decision 55) catches artifact violations after the fact, but cannot prevent an irreversible action in progress.
**Revisit trigger:** If a platform introduces a hook system that maps cleanly to the adapter overlay pattern (abstract capability → platform-specific tool), reconsider whether per-platform enforcement can be generated from the core, preserving agnosticism.
**What would change this:** If one platform becomes dominant enough that portability is no longer a real constraint, platform-specific enforcement would become acceptable.

### Decision 57 — Inline authority checks at point of action in each skill, not centralized cross-reference

**Date:** 2026-07-21
**Confidence:** High — ADR 0019's own analysis provides the structural argument.
**Evidence:** ADR 0019 (`docs/adr/0019:16,52-56`) diagnosed the exact failure mode: the sensitivity rule lived in a separate table with no cross-reference from the authority-check path, making it structurally unreachable. The fix (Decision 52) was to wire sensitivity into the authority gates table — moving the rule to the point where the agent actually checks. The same structural problem exists for runtime authority checks: the gates are centralized in `CONSEQUENCE-AUTHORITY.md`, skill profiles reference them from `SKILL-AWARE-GRILLING.md`, but the actual action instructions in each `SKILL.md` don't contain the check. An agent executing `deploy-with-recovery/SKILL.md` reads the deployment steps; the authority gate is in a different file.
**Decision:** Each skill's `SKILL.md` must inline the authority check at the exact point where an irreversible or gated action is described. The check must name the specific action, the required authority level, and the recording obligation (per Decisions 53-54). `CONSEQUENCE-AUTHORITY.md` remains the canonical reference for the full gates table; the inlined checks are derived from it, not independent of it.
**Trade-off:** Authority language is duplicated across up to 14 skill files. Acceptable because: (1) ADR 0019 proved that centralization caused the gap it was designed to prevent, (2) the generator (`tools/generate-adapters.py`) already produces skill files from a core + overlay pattern — inlined authority checks can be generated from the canonical reference rather than hand-maintained, and (3) reachability at the point of action is more valuable than single-source maintainability for safety-critical rules.
**Revisit trigger:** If the generator gains the ability to inject authority checks from `CONSEQUENCE-AUTHORITY.md` into skill output automatically, the duplication concern disappears entirely. Also revisit if the number of gated actions grows beyond what's practical to inline.
**What would change this:** If a future CLI enforces gates at the write/execute path before the agent's instructions matter, inlining becomes defense-in-depth rather than primary enforcement — still valuable but less critical.

### Decision 58 — Consequence assignment requires a three-question structural prompt

**Date:** 2026-07-21
**Confidence:** Medium — the evidence of under-assignment is strong (18/20 `meaningful`, 0 `high`, including objects that govern safety mechanisms), but whether the three-question format is the right fix is a design choice that hasn't been tested.
**Evidence:** All 20 Work Objects are `consequence: low` (2) or `consequence: meaningful` (18). Zero are `high`. Work Object `2026-07-21-005` (implements the sensitivity gate system — the mechanism that protects restricted content) is `meaningful`, despite the system's own definition placing "affects safety, privacy" at `high`. The one-line definitions in `CONSEQUENCE-AUTHORITY.md:7-11` do not prompt the author to consider reversibility, blast radius, or downstream effects — they describe the level, not the assessment path.
**Decision:** Before setting `consequence:` in frontmatter, the agent must answer three yes/no questions:
1. Is the action reversible? (If no → at least `meaningful`)
2. Does it affect systems or people beyond this workspace? (If yes → at least `meaningful`)
3. Could a failure here affect safety, privacy, or money? (If yes → `high`)
All three answers must be recorded in the Work Object's first History entry alongside the consequence assignment. This is the assessment path, not a replacement for the level definitions.
**Trade-off:** Adds three questions to every Work Object creation. Acceptable because the current pattern shows consequence being set by habit (`meaningful` as default) rather than assessment — the field has no discriminating power if it's never `high`.
**Revisit trigger:** After 10 Work Objects are created under this rule, check whether `high` consequence has appeared at least once. If it hasn't, either the project genuinely never does high-consequence work (in which case the three-question prompt is unnecessary ceremony) or the questions aren't calibrated correctly.
**What would change this:** If the pre-commit hook (Decision 55) gains the ability to validate consequence assignment against the three questions (e.g., flagging `meaningful` when the History entry records "failure could affect safety = yes"), the structural prompt becomes enforceable rather than advisory.

### Decision 59 — Authority records distinguish accepted-recommendation from independent-authorization

**Date:** 2026-07-21
**Confidence:** Medium — the distinction is structurally sound and costs nothing at grant time, but its value is realized only when reviewing outcomes or resuming across sessions. Untested.
**Evidence:** `AGREEMENT-LOOP.md:54` defines `do recommended` as accepting the agent's recommendation within stated scope. `CONSEQUENCE-AUTHORITY.md:53-54` defines `just execute` similarly. Neither distinguishes whether the user evaluated the action independently or deferred to the agent's judgment. In the structured authority History entry (Decision 54), the action and scope are recorded, but the *mode* of authority — did the user direct this, or accept a proposal? — is not. A future session reviewing a deployment outcome cannot tell whether the user made an independent risk judgment or followed an agent suggestion.
**Decision:** The structured authority History entry (Decision 54) must include an `authority_mode` field with two values:
- `accepted-recommendation` — the agent proposed the action and the user confirmed (e.g., `do recommended`, `yes`).
- `independent-authorization` — the user directed the action without an agent recommendation (e.g., "deploy this now", "delete that object").
The mode is recorded at grant time based on the conversational context. It does not change the gate threshold — both modes satisfy "ask first." It is metadata for outcome review and accountability tracing.
**Trade-off:** Introduces a distinction that may feel like unnecessary precision for a single-user system. Acceptable because: (1) it costs nothing — the user already says "yes" or "do recommended," the mode is derived from what they said, not a new question; (2) it matters for outcome review — "I decided to deploy" and "the agent suggested deploying and I went along" have different accountability implications when analyzing failures; (3) it is forward-compatible with multi-user or delegation scenarios if the system ever grows.
**Revisit trigger:** After reviewing 5+ outcomes where authority was recorded, check whether the `authority_mode` distinction actually informed the review. If it never matters, drop it to reduce History entry weight.
**What would change this:** If outcome review consistently shows that the mode doesn't affect accountability analysis (i.e., the user always evaluates independently regardless of who proposed), the field is noise and should be removed.

### Decision 60 — Accept the auditable-but-not-preventable gap for external-effect actions; prioritize CLI as the enforcement path

**Date:** 2026-07-21
**Confidence:** High — this follows directly from Decision 56 (platform-agnostic enforcement) and the observed enforcement landscape.
**Evidence:** Five categories of gated actions — export, destructive, schema migration, external writes, deployment — have effects outside the workspace and leave no artifact the pre-commit hook can validate. These are the highest-risk actions in the system. Platform-agnostic enforcement cannot block them without a CLI that intercepts at the command/write path. Decision 56 rules out platform-specific enforcement. The only remaining options are: (a) accept the gap and make these actions auditable via authority recording + inlined prose, or (b) reverse Decision 56.
**Decision:** Accept the gap. The five external-effect action categories are auditable but not preventable until a platform-agnostic CLI exists. Enforcement for these actions consists of:
- Inlined authority checks at point of action in each skill (Decision 57)
- Structured authority History entries recording action, scope, evidence, constraints, and mode (Decisions 53-54, 59)
- The pre-commit hook validates that authority was recorded *after* the action — it cannot prevent the action itself
This explicitly acknowledges that the system depends on agent prose-compliance for its highest-risk gates. The CLI is the planned resolution; it becomes the highest-priority enforcement deliverable.
**Trade-off:** The five most dangerous actions remain stoppable only by the agent choosing to follow instructions. Acceptable given: (1) the user is the sole operator and accountable owner, (2) authority recording means violations are at least discoverable after the fact, (3) the platform-agnostic constraint is a deliberate architectural choice worth the safety cost.
**Revisit trigger:** When the CLI design session begins, these five action categories are the primary enforcement targets — not the artifact-validatable categories that the pre-commit hook already covers. Also revisit if an actual violation occurs (agent performs an external-effect action without asking), since that would be the first real test of whether auditable-but-not-preventable is sufficient.
**What would change this:** An actual violation where the agent deploys, exports, or deletes without authorization and the after-the-fact audit record is insufficient to remediate. That would force re-evaluating Decision 56.

### Decision 61 — Pre-commit hook rejects non-.work-studio files carrying private or restricted sensitivity

**Date:** 2026-07-21
**Confidence:** High — the check is simple, the risk is real, and the mechanism (pre-commit hook) is already accepted (Decision 55).
**Evidence:** `CONSEQUENCE-AUTHORITY.md:19-21` defines private-sensitivity storage rule as `.work-studio/` (Git-excluded) and restricted as "never store in Work Objects, pointer-only." `.gitignore:17-21` excludes `.work-studio/objects/` and related files. But `.gitignore` only protects files *inside* `.work-studio/`. If an agent writes a Work Object with `sensitivity: private` or `sensitivity: restricted` to a path outside `.work-studio/` (e.g., a regular project directory), `.gitignore` provides zero protection — the file would be committed and pushed like any other tracked file.
**Decision:** The pre-commit hook (Decision 55) adds a fourth validation: any staged file outside `.work-studio/` that contains YAML frontmatter with `sensitivity: private` or `sensitivity: restricted` must be rejected. The commit message must name the offending file and instruct the user to move it to `.work-studio/` or reclassify its sensitivity.
**Scope:** This check applies to files with parseable YAML frontmatter only (primarily Work Objects). It does not attempt to classify unlabeled content — that is a classification problem beyond the hook's scope.
**Trade-off:** Does not catch private content in non-frontmatter files (e.g., a plain-text file with sensitive data). Acceptable because Work Objects are the system's primary structured data format and the most likely vector for misplaced sensitive content.
**Revisit trigger:** If non-Work-Object files with private content become common (e.g., evidence attachments, exported reports), extend the check to cover additional file patterns.
**What would change this:** If the system introduces a non-frontmatter mechanism for marking file sensitivity (e.g., `.sensitivity` sidecar files or directory-level classification), the hook should check that mechanism too.

### Decision 62 — Pre-commit hook protects constitutional files via a declared list

**Date:** 2026-07-21
**Confidence:** Medium — the gap is real (the authority model doesn't protect itself), the fix is simple, but the "declared list" mechanism is manual and could drift.
**Evidence:** `references/CONSEQUENCE-AUTHORITY.md`, `references/AGREEMENT-LOOP.md`, and `references/SKILL-AWARE-GRILLING.md` define the authority gates, the conversational engine, and the skill profiles respectively. Changes to any of these alter the behavior of every gate and every skill. None carry `sensitivity:` or `consequence:` frontmatter. None are governed by the authority gates table. An agent can modify the file that defines the gates without any gate applying. The authority model is self-modifiable without authority.
**Decision:** The pre-commit hook (Decision 55) adds a fifth check: modifications to files on a declared constitutional-files list require either (a) a structured authority History entry in the commit message referencing a Work Object that authorized the change, or (b) an explicit bypass tag (e.g., `CONSTITUTIONAL-OVERRIDE:`) in the commit message that makes the unguarded modification visible and auditable. The initial list:
- `references/CONSEQUENCE-AUTHORITY.md`
- `references/AGREEMENT-LOOP.md`
- `references/SKILL-AWARE-GRILLING.md`
- `references/EVIDENCE-MODEL.md`
- `references/SHARED-PROTOCOL.md`
The list is maintained in a hook configuration file (e.g., `.work-studio/constitutional-files.list`) that is itself on the list.
**Trade-off:** Maintaining the list is manual and could drift. Mitigated by: (1) the list is small (5-6 files) and changes rarely, (2) the list file is itself protected by the hook (self-referential guard), and (3) the bypass tag makes unguarded modifications visible rather than silent.
**Revisit trigger:** If the number of constitutional files grows beyond ~10, consider whether a directory-level or naming-convention approach (e.g., all files in `references/`) would be more maintainable than an explicit list.
**What would change this:** If Git branch protection rules are adopted for this repo (e.g., requiring PR review for changes to `references/`), that would provide a stronger and more standard mechanism for protecting constitutional files — the hook check would become defense-in-depth.
