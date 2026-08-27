---
schema_version: 1
id: 2026-08-22-036
title: Add ws list --domain live query flag
type: change
status: active
state: observe
consequence: low
sensitivity: ordinary
domain: [engineering, governance]
created_at: 2026-08-22T20:00:09Z
updated_at: 2026-08-22T20:02:58Z
next_action: Value hypothesis (does the live query flag actually get used vs the generated mirror) is unobserved -- same posture as WO 031/034. No open design questions remain.





---
## Intent

WO 2026-08-22-031 Decision 3 and its closing outcome review both explicitly
deferred a live `ws list --domain <value>` query flag in favor of the
generated-index mirror (`ws domain sync` / `.work-studio/domain/<value>.md`).
The director has now asked for that deferred capability: a direct CLI query
over the corpus by domain, without requiring a regeneration step first.

## Success evidence

<!-- Checklist of observable outcomes that indicate completion. -->
- [x] `ws list --domain <value>` (repeatable) prints every Work Object whose
      `domain:` list includes any of the given values -- id, title, domain
      list, status, state -- reading frontmatter directly, not the generated
      mirror
- [x] `ws list` with no `--domain` filter lists the full corpus with the same
      columns, domain shown as `(none)` when absent
- [x] Verified against a real multi-domain object (WO 2026-08-22-026,
      business+architecture) appearing under both `--domain business` and
      `--domain architecture`
- [x] New unit tests pass; `ws validate` shows no new errors

## Constraints and non-goals

**Constraints:**
- Read-only: query frontmatter directly (same scan pattern as
  `domain.collect_domain_index`), never write to any file.
- Reuse `VALID_DOMAINS`/`parse_domain_field` from `tools/ws/schema.py`; do not
  invent new vocabulary or a second index format.
- Filtering by domain uses the same "list includes any of" semantics as the
  generated mirror, so results match `ws domain sync` output exactly.

**Non-goals:**
- NOT touching `ws domain sync` or the generated `.work-studio/domain/`
  files -- both mechanisms coexist (generated mirror for browsing, `ws list`
  for scripting/quick queries).
- NOT adding command-center domain grouping -- that remains a separate,
  not-yet-opened successor per the outcome review's open items.
- NOT adding filters beyond `--domain` (no `--type`, `--status`, etc.) --
  those are new scope, not part of the deferred item being resolved here.

## Decisions and revisit triggers

<!-- Structured decision records for lifecycle gate enforcement.
     Each major decision gets its own record with the fields below.
     The build, release, close, and observe gates read this section
     structurally — keep field names exactly as shown. -->

### Decision 1 — Skip explore/design: reuse the proven frontmatter-scan mechanism, no new design question

| Field | Value |
|-------|-------|
| **Decision type** | decision |
| **Result** | pass |
| **Scope** | This is a thin, read-only CLI addition. It reuses the exact scan pattern already built and proven in `domain.collect_domain_index` (WO 2026-08-22-031 Decision 3) -- walk `.work-studio/objects/**/*.md`, extract `domain:` via `parse_domain_field`, filter. No new mechanism, no new vocabulary, no new file format. |
| **Authorization** | Director explicitly asked to "add the live query flag" -- one of the three named open items carried forward from WO 2026-08-22-031/034's closing outcome review. |
| **Confidence** | high (basis: [system] the underlying scan/parse code is already unit-tested and demoed against real multi-domain objects in `tests/test_domain_axis.py`; this WO only adds a thin CLI-argument/print layer over it). |
| **Actor** | governance-conduct-work-object |
| **Revisit trigger** | If the director asks for additional filters (`--type`, `--status`) or output formats (JSON), that is new scope requiring its own decision, not silently added here. |
| **Rationale** | Routing straight to build avoids stage theater for a low-consequence, mechanism-proven addition. Recording this explicitly (per the lesson from WO 2026-08-22-034, where the build-gate audit correctly flagged a missing decision record) keeps the gate satisfied by fact. |

## Evidence ledger

<!-- Tagged evidence entries. See references/AGREEMENT-LOOP.md for
     canonical tags: [system], [decision], [inference],
     [gap], [testimony], [memory]. -->

| Tag | Source | Entry |
|-----|--------|-------|
| [system] | python3 -m tools.ws list; python3 -m unittest tests.test_domain_axis tests.test_relation_graph_tracer; python3 -m tools.ws validate | Implemented ws list --domain by adding collect_object_rows/cmd_list to tools/ws/domain.py, wired into __main__.py. Verified against real corpus: WO 2026-08-22-026 (business+architecture) appears under both --domain business and --domain architecture, matching ws domain sync membership. Invalid domain values rejected (exit 1). No-filter list returns all 47 corpus objects sorted by id, unclassified objects shown as (none). 27/27 relevant unit tests pass (22 pre-existing + 5 new ws-list tests). ws validate shows no new errors beyond pre-existing corpus debt (WO 027/035 verify-state gaps, timestamp dupes, baseline-snapshot warnings, evidence-count mismatches on WO 001/006). |
## Open questions

<!-- Unresolved questions that block progress or require a decision. -->

## Next move

<!-- The single next action this Work Object routes to. -->

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-22T20:00:50Z — activate

- **State:** explore
- **Status:** active
- **Actor:** governance-conduct-work-object
- **Rationale:** Activating; director-requested deferred capability, mechanism already proven from WO 031/034
### 2026-08-22T20:00:56Z — skip-design

- **State:** build
- **Status:** active
- **Actor:** governance-conduct-work-object
- **Rationale:** No open design question: Decision 1 records reuse of the already-proven collect_domain_index scan mechanism. Routing to engineering-implement-bounded-change.
### 2026-08-22T20:02:58Z — complete

- **State:** observe
- **Status:** active
- **Actor:** governance-conduct-work-object
- **Rationale:** ws list --domain implemented and verified: multi-domain membership matches ws domain sync exactly, all 4 success-evidence items met, 27/27 regression tests pass, ws validate clean beyond pre-existing corpus debt.
## Relationships

  REL-2026_08_22_036-001:
    type: responds_to
    from: wo:2026-08-22-036
    to: wo:2026-08-22-031
    basis: "Resolves the live query flag explicitly deferred by WO 2026-08-22-031's outcome review"
    created_at: 2026-08-22T20:00:33Z
