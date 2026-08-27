---
schema_version: 1
id: 2026-08-22-031
title: Add domain axis to Work Object frontmatter
type: inquiry
status: closed
state: close
consequence: meaningful
sensitivity: ordinary
domain: [architecture, governance]
created_at: 2026-08-22T15:17:35Z
updated_at: 2026-08-22T19:52:12Z
next_action: Director's call: (a) backfill domain on the remaining ~33 uncategorized corpus objects as a separate successor Work Object, (b) add a live ws list --domain query flag / command-center grouping as a separate successor, or (c) treat the original intent (tell at a glance what type of work I'm on) as substantially delivered via ws domain sync and close this object. No action is forced.











---
## Intent

Give Work Objects a second classification axis -- domain (business,
architecture, asset, design, governance, engineering, research, ideation,
operations) -- independent of the existing `type` field, so the director
can tell at a glance what discipline a piece of work belongs to. Started
from a scalar design, revised to a list after the real corpus falsified
the single-label assumption on its own recent work (the business-router
cluster, WO 026, WO 023).

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] A `domain:` frontmatter field, list-shaped per Decision 3, with a controlled vocabulary is defined and schema-validated
- [x] `ws create`/`ws start` accept `--domain` (repeatable/list); existing objects can be backfilled
- [x] Tooling can filter/count objects by domain — via `ws domain sync` + reading `.work-studio/domain/<value>.md`, which lists and counts every matching object; NOT via a live `ws list --domain` query flag or command-center grouping, which remain undone if wanted later
- [x] The vocabulary was tested against the corpus and found NOT to cleanly classify as a scalar — resolved by Decision 3 (list-shaped, not scalar)
- [x] A derived, regenerable domain-folder mirror builds from frontmatter as a generated index file (symlinks/junctions ruled out per Decision 3) and never diverges from it — demonstrated live: re-sync after a domain change fully replaces stale entries (test_sync_is_idempotent_and_fully_regenerates)


## Constraints and non-goals

**Constraints:**
- `domain` is a SECOND axis, independent of the existing `type` field ({change,inquiry,project,incident}); it does not replace or repurpose `type`.
- Filenames, the `YYYY/MM` storage path, and the ID resolver stay unchanged — domain lives only in frontmatter.
- Controlled vocabulary, not free text; changes to the vocabulary require a decision.

**Non-goals:**
- NOT domain-in-filename (Direction 2) or campaign reuse (Direction 4).
- NOT authoritative domain folders (Direction 3's original form): the canonical `objects/YYYY/MM/` layout, filenames, and ID resolver stay unchanged. The domain folder tree is a DERIVED, rebuildable mirror only (see Decision 2), never a source of truth, and objects are not moved.
- NOT dual-authoritative storage (folder AND frontmatter both authoritative) — director-rejected as guaranteed drift.
- No retro-migration of storage layout; backfilling the `domain` field on existing objects is metadata-only.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Selected Direction 1: domain as a controlled-vocabulary frontmatter field

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Add a `domain:` frontmatter field (controlled vocabulary: business, architecture, asset, design, governance, engineering, research, ideation, operations — mirroring skill families) as a second classification axis alongside `type`. Metadata-only; filenames/paths/resolver unchanged. |
| **Authorization** | Director selected develop-idea Direction 1 and confirmed domain is a second axis (not a repurposing of `type`). |
| **Confidence** | high for the choice of axis and placement (basis: [system] no domain signal exists anywhere structural today; frontmatter is the only queryable, tool-enforceable home that doesn't touch the ID resolver); medium for the exact vocabulary (basis: [inference] — mirrors skill families but not yet tested against all 41 objects). |
| **Actor** | thinking-develop-idea (director-accepted) |
| **Revisit trigger** | If a real Work Object cannot be cleanly classified by a single domain value (e.g. genuinely business+architecture), revisit whether domain should allow a small ordered list rather than a scalar. |
| **Rationale** | Domain-as-metadata gives a queryable, schema-enforceable discipline axis without touching filenames, the YYYY/MM path, or the ID resolver/graph scans that assume that layout. Rejected alternatives: filename prefix (unenforced drift), domain folders (breaks the path/resolver contract — ADR-level), campaign reuse (conflates effort with discipline), derived-view-only (doesn't give a stored, authoritative label). |

### Decision 2 — Add Direction 3 as a DERIVED domain-folder mirror (frontmatter authoritative)

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | A read-only, regenerable domain folder tree (e.g. `ws domain sync` builds `domain/<value>/` links or a projection) that mirrors the authoritative `domain:` frontmatter from Decision 1. Objects are not moved; the canonical store stays `objects/YYYY/MM/`. |
| **Authorization** | Director requested "also add domain-partitioned directories," then chose "folders mirror the frontmatter" when the conflict with Decision 1 was surfaced. |
| **Confidence** | high for the reconciliation (basis: [decision] director-selected; a derived mirror matches the architecture's "derived view, not new source of truth" rule and leaves the resolver/graph scans intact); medium for the mirror mechanism (basis: [inference] — symlinks vs a generated index vs a projection file not yet chosen; Windows symlink support is a known constraint). |
| **Actor** | thinking-develop-idea (director-accepted) |
| **Revisit trigger** | If maintaining the mirror in sync with frontmatter proves unreliable, or if the director later wants the folder tree to be authoritative (which would reopen the ADR-level path/resolver decision explicitly rejected here). |
| **Rationale** | Gives the "browse the tree by domain" experience the director wanted without the ADR-level risk of moving the canonical store. Frontmatter stays the single source of truth; the folder view is rebuildable and disposable, so folder-vs-frontmatter drift is impossible by construction (the folder is always regenerated from frontmatter, never edited directly). |

### Decision 3 — Revise domain to a short ordered LIST; mirror mechanism is a generated index file (symlinks/junctions ruled out)

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | Fires Decision 1's own revisit trigger. `domain:` becomes a short ordered list (primary domain first), not a scalar. The Decision 2 mirror mechanism is fixed as a generated index file (`domain/<value>.md` listing member paths); OS symlinks and junctions are ruled out entirely, not merely deprioritized. |
| **Authorization** | design-tracer-bullet directly tested both Decision 1 and Decision 2's mechanism assumptions before recommending further work; director accepted the revised tracer. |
| **Confidence** | high (basis: [system] direct tests, not inference — native Windows symlink creation fails without admin ("Administrator privilege required for this operation"); Git Bash `ln -s` silently falls back to a plain copy, confirmed via `os.path.islink() == False`; junctions are directory-only, structurally inapplicable to per-file mirroring; corpus spot-check found the majority of recent objects — the entire 018-022 cluster, plus 026, 017, 023 — are genuinely multi-domain, not edge cases). |
| **Actor** | design-tracer-bullet (director-accepted) |
| **Revisit trigger** | If a short ordered list still can't cleanly cover a real object (needs 4+ domains, or domains that don't have a sensible primary/secondary order), revisit toward uncontrolled free-form tags instead of a controlled list. |
| **Rationale** | The scalar assumption in Decision 1 was evidence, not just theory: tested directly against the real corpus and failed on the majority of the sample, not an isolated case. The symlink assumption in Decision 2 was similarly evidence-tested and failed for two independent reasons (privilege gate; MSYS silent-copy fallback that would have shipped a hidden second source of truth). Both revisions are now grounded in direct measurement rather than the original inference-labeled placeholders. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [decision] | develop-idea selection, director-confirmed | develop-idea selection (director-confirmed): domain is a SECOND axis alongside the existing type field {change,inquiry,project,incident}, which describes work shape not discipline. Selected Direction 1: add a controlled-vocabulary domain: frontmatter field (business|architecture|asset|design|governance|engineering|research|ideation|operations, mirroring skill families). Filenames and YYYY/MM storage unchanged; tooling can filter by domain. Directions 2 (filename prefix), 3 (domain folders), 4 (campaign reuse), 5 (derived-view projection) not selected. |
| [decision] | director request 'also add domain-partitioned directories' + reconciliation choice 'folders mirror the frontmatter' | Supersedes the earlier 'Direction 3 not selected' note in the prior ledger row: director subsequently added Direction 3, reconciled as Decision 2 (a DERIVED domain-folder mirror with frontmatter as single source of truth, objects not moved). The selection is now Direction 1 + Direction 3-as-derived-mirror, not Direction 1 alone. |
| [system] | python3 -m unittest tests.test_domain_axis -v | Decision 3 fully implemented: schema.py gained VALID_DOMAINS, validate_domain, format_domain_field, parse_domain_field (dedicated parser -- the shared parse_frontmatter is scalar-only per its own docstring and would have silently mis-parsed a bracketed list), generate_frontmatter(domain=...). --domain (repeatable) wired into ws create/ws start. New tools/ws/domain.py builds ws domain sync: read-only corpus scan generating one clearly-marked file per domain value at .work-studio/domain/<value>.md. 11 new unit tests in tests/test_domain_axis.py, all pass. |
| [system] | ws domain sync; cat .work-studio/domain/business.md .work-studio/domain/architecture.md .work-studio/domain/engineering.md .work-studio/domain/design.md | Live demo executed (not just tested): classified the real 8-object hard-case set via sanctioned direct-edit (018-022 as [business,engineering], 017 as [design,asset], 023 as [design,engineering,architecture], 026 as [business,architecture]). Ran ws domain sync for real; read the generated files directly. CONFIRMED: 2026-08-22-026 appears in BOTH .work-studio/domain/business.md and architecture.md; 2026-08-22-023 appears in all three of design.md, engineering.md, architecture.md. This is the exact multi-domain case that falsified Decision 1's scalar assumption, now correctly represented. |
| [system] | ws validate; git status --short; git diff --stat tools/ws/schema.py tools/ws/__main__.py | ws validate shows one pre-existing error on WO 2026-08-22-027, unrelated dirty work not touched by this implementation -- not a regression. Repository inspection preserved a large volume of unrelated concurrent dirty work untouched (SKILL-AWARE-GRILLING.md changes across three adapters, a new design-govern-interaction-motion skill scaffold). |
| [system] | review-outcome-and-adapt outcome review; director accepted stop | Outcome review (review-outcome-and-adapt): mechanism hypothesis CONFIRMED with direct evidence (WO 026 in both business.md and architecture.md; WO 023 in three files; no new validate errors). Value hypothesis (director tells work apart at a glance in real use) is INSUFFICIENT OBSERVATION -- shipped and demoed this session, not yet used in real work. Not blocking closure since the recorded Success Evidence was mechanism-level. Director accepted stop. Open items carried forward as revisit triggers, not blockers: WO 2026-08-22-027 still needs classification (tied to its own unrelated pre-existing error); live ws list --domain query tooling remains a deferred, un-opened successor; the 9-value vocabulary has not had independent second-reviewer verification. |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T15:17:35Z — Started via ws start (created + evidence + explore + activate supporting)

- **State:** explore
- **Status:** active
- **Actor:** thinking-develop-idea
- **Rationale:** Director chose domain-as-metadata: queryable and tool-enforceable without touching filenames, paths, or the ID resolver (which globs objects/YYYY/MM).
### 2026-08-22T15:18:17Z — Director selected develop-idea Direction 1 (domain as a controlled-vocabulary frontmatter field, second axis alongside type). Recorded as Decision 1. Routing to design-tracer-bullet.

- **State:** design
- **Status:** active
- **Actor:** thinking-develop-idea
- **Rationale:** Single direction selected; transition explore->design per develop-idea. The key assumption (a fixed vocabulary cleanly classifies every WO) needs a reality test before schema enforcement.
### 2026-08-22T15:20:18Z — Director added Direction 3 (domain-partitioned directories) alongside Direction 1. Conflict surfaced (Direction 3 contradicted Decision 1's paths-unchanged constraint and risked dual-source-of-truth drift); director chose reconciliation 'folders mirror the frontmatter'. Recorded as Decision 2: a derived, regenerable domain-folder mirror with frontmatter as the single source of truth. Objects are not moved; resolver and graph scans stay intact.

- **State:** design
- **Status:** active
- **Actor:** thinking-develop-idea
- **Rationale:** Reconciled the two directions into one coherent design rather than stacking a contradicting decision: frontmatter authoritative (Decision 1) + derived folder mirror (Decision 2). Drift is impossible by construction because the folder tree is always regenerated from frontmatter.
### 2026-08-22T15:23:40Z — Accepted Decision 3: domain is a short ordered LIST (not scalar), mirror mechanism is a generated index file (symlinks/junctions ruled out by direct test -- native symlink needs admin, Git Bash ln -s silently falls back to a copy, junctions are directory-only). Both revisions grounded in direct measurement against the real corpus and this environment, not inference. Routing to engineering-implement-bounded-change.

- **State:** build
- **Status:** active
- **Actor:** design-tracer-bullet
- **Rationale:** The originally-scoped tracer (scalar vocabulary + symlink mirror) failed both assumption tests before any code was written -- corrected the design rather than building on a disproven premise, matching the discipline from the first tracer in this session (WO 2026-08-22-026).
### 2026-08-22T15:30:00Z — Decision 3 fully implemented and demonstrated: schema field, CLI flags, ws domain sync, 11 passing tests, real 8-object corpus classification proving the multi-domain case (026 in both business.md+architecture.md; 023 in three files). All 5 success-evidence items met. No further build work is scoped -- moving to observe rather than continuing to expand.

- **State:** observe
- **Status:** active
- **Actor:** governance-conduct-work-object
- **Rationale:** This is a completed, demonstrated tracer bullet, not an open implementation. Backfilling the remaining ~33 corpus objects and adding a live ws list --domain query flag are both separate, larger scopes explicitly deferred (Decision 1 non-goals: no retro-migration required) -- observing whether the shipped mechanism holds up in real use is the honest next state, not silently expanding scope.
### 2026-08-22T19:52:12Z — Closed: Mechanism hypothesis confirmed with direct evidence; value hypothesis (does this actually help orient at a glance) is unobserved but not blocking since recorded Success Evidence was mechanism-level, not usage-level. Director accepted stop after outcome review. Open items (WO 027 classification, deferred query tooling, unverified vocabulary) recorded as revisit triggers, not reopened as blockers.

- **State:** close
- **Status:** closed
- **Actor:** governance-review-outcome-and-adapt
- **Rationale:** Mechanism hypothesis confirmed with direct evidence; value hypothesis (does this actually help orient at a glance) is unobserved but not blocking since recorded Success Evidence was mechanism-level, not usage-level. Director accepted stop after outcome review. Open items (WO 027 classification, deferred query tooling, unverified vocabulary) recorded as revisit triggers, not reopened as blockers.
