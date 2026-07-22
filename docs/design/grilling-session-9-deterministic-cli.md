# Grilling Session 9 — Deterministic Repository CLI

**Date:** 2026-07-21
**Focus:** What is the smallest deterministic command surface that removes integrity-critical mutation from model control?
**Status:** Converged — shared understanding confirmed
**Prior session:** Session 8 (Authority and Sensitivity) — see `docs/design/grilling-session-8-authority-sensitivity.md`

---

## Evidence Ledger

### Observed

- `tools/` — 5 existing tools: `generate-adapters.py` (Python 3, stdlib-only, 680 lines), `verify-conformance.py` (Python 3, stdlib-only), `verify-append-only.py` (Python 3, stdlib-only + git), `install.sh` (POSIX sh, shasum), `prompt_payload_tracer.py` (Python 3, stdlib-only). Zero external dependencies anywhere in the project. No `requirements.txt`, `package.json`, `Cargo.toml`.
- `.work-studio/objects/` — 20+ Work Objects, all mutated by agents reading prose instructions and calling Write/Edit tools directly. No intermediary program for any mutation.
- `references/WORK-OBJECT.md:28` — ID format `YYYY-MM-DD-NNN`, zero-padded sequence number. Allocated by agent scanning directory listing.
- `references/WORK-OBJECT.md:69-71` — Optimistic concurrency via `updated_at` comparison described. No tool implements it.
- `references/WORK-OBJECT.md:68-72` — Single-session assumption (ADR 0020). No lock mechanism. `updated_at` compare is intra-session staleness detection.
- `docs/adr/0015-...md` — 8-state permissive lifecycle model. Any state may transition to any other EXCEPT: `close` is terminal (cannot transition out), `closed` status is terminal. 5 evidence-based prerequisite gates check structural fields in `## Decisions and revisit triggers`.
- `docs/adr/0015-...md:17` — "every 'CLI enforces/validates/prohibits' clause in the lifecycle specification is a target, not a description of current behavior."
- `docs/adr/0019-...md:105-107` — "Planned enforcement: the future CLI's write path will check sensitivity before allowing body mutation."
- `.git/hooks/` — All `.sample` files only. No active hooks.
- `.work-studio/active.md` — Attention register with Primary/Supporting/Paused lists. Updated by agents directly, no consistency check against object frontmatter.
- `.work-studio/objects/2026/07/2026-07-21-008-*.md` — Sample Work Object: Evidence ledger uses table format, History uses table format, Decisions section uses free-text (no structured `type: decision`, `result: pass` fields that ADR 0015 gates expect).
- Session 8 Decision 55 — Five-check pre-commit hook designed but not built.
- Session 8 Decision 56 — Runtime enforcement must be platform-agnostic.
- Session 8 Decision 58 — Consequence assessment requires three-question prompt at creation.
- Session 8 Decision 60 — CLI is highest-priority enforcement deliverable.
- All three target platforms (Codex, Claude Code, GitHub Copilot) provide Python 3 by default. Node.js availability varies. Rust, Go, Deno not installed.
- `generate-adapters.py:72-151` — Hand-rolled minimal YAML parser, stdlib-only. Reusable for frontmatter parsing.

### Claimed

- `WORK-OBJECT.md:34` says state allows "Flexible movement" — predates ADR 0015's two prohibitions. Consistent in intent, imprecise in specification.
- `CONSEQUENCE-AUTHORITY.md:39-44` lists implicit-authority actions (reading, appending History, updating `updated_at`). The CLI must preserve these as agent-callable without extra confirmation.

### Inferred

- ID allocation is the highest-corruption-risk operation: a duplicate ID is unrecoverable, and the current scan-then-write pattern has no collision detection.
- The gap between "described optimistic concurrency" and "no implementation" means every concurrent intra-session write silently overwrites. This has likely already occurred without detection.
- Consequence under-assignment (18/20 `meaningful`, 0/20 `high`) is partially a UX problem — agents default to `meaningful` because nothing forces the three-question assessment.

### Contradictions

- `WORK-OBJECT.md:34` ("Flexible movement") vs ADR 0015 (two terminal prohibitions). The CLI encodes ADR 0015.
- ADR 0015 gates check structured fields in Decisions section, but real Work Objects use free-text Decisions sections with no structured fields. Gates are currently uncheckable.
- ADR 0019 promises CLI-level sensitivity enforcement that does not exist.

---

## Decisions Log

### Decision 63 — Tier A/B split for CLI command ownership

**Operations split into two tiers:**

**Tier A (CLI owns end-to-end, agent never touches file directly):** Initialize workspace, allocate immutable ID, create Work Object, apply transition, update `updated_at` (side-effect only), compare `updated_at` (baked into writes), close object, update attention register, validate workspace.

**Tier B (agent supplies content, CLI validates structure and writes):** Append evidence, append history, register component.

**Rationale:** Tier A operations have structural invariants a program can enforce completely. Tier B operations require agent-supplied content the CLI can only validate syntactically.

### Decision 64 — Python 3 stdlib-only package at `tools/ws/`

CLI is a minimal Python package under `tools/ws/` with `__main__.py` entry point. Invoked as `python3 -m tools.ws <command>` or via thin wrapper at `tools/ws`. No `setup.py`, no `pip install`, no virtual environment. Continues the established dependency-free pattern.

**Rationale:** Python 3 is available on all three target platforms by default. Existing tools are all Python 3 stdlib-only. Package structure allows clean module separation for 5+ distinct responsibilities without growing past single-file maintainability limits.

### Decision 65 — Gate enforcement against structured fields, with grandfathering

CLI enforces prerequisite gates against structured fields in Decisions section. `ws create` generates a Decisions section template with the structured format gates expect. Legacy Work Objects (pre-CLI) are grandfathered: missing structured fields produce "gate not yet satisfiable" messages, not failures. Legacy objects are migrated incrementally when an agent next transitions through a gated state.

**Rationale:** Enforcing against free text is theater — gates would parse nothing and always pass. Generating the template at creation means every new Work Object is gate-ready from birth. Grandfathering avoids high-churn bulk migration of 20+ existing objects.

### Decision 66 — Composed validation checks

`ws validate` is composed of named checks: `schema`, `sections`, `append-only`, `attention`, `sensitivity`, `lifecycle`, `structure`. No arguments runs all checks. Named checks can be invoked individually. Pre-commit hook calls specific checks on staged files.

**Rationale:** Pre-commit hook needs `schema`, `append-only`, `sensitivity`, `lifecycle` on staged files — not workspace-wide checks like `attention`. Running the full suite on every commit is slow and noisy.

### Decision 67 — Required `--expect-updated` on mutations

Every write command mutating an existing file requires `--expect-updated <timestamp>`. CLI compares against current `updated_at`, rejects stale writes. `ws create` is exempt (no prior state). `--force` exists for recovery but prints a warning.

**Rationale:** Optional `--expect-updated` becomes opt-in theater. Required means the agent must have read the file before writing — exactly the discipline described in `WORK-OBJECT.md:69-71` but never implemented.

### Decision 68 — Structured argument flags for Tier B content

Tier B commands accept content as separate CLI flags (`--tag`, `--text`, `--source` for evidence; `--action`, `--state`, `--actor`, `--rationale` for history). CLI assembles the Markdown entry. Agent never constructs Markdown format for protected sections. `--text-file <path>` escape hatch for long text values.

**Rationale:** The CLI becomes the single assembler of Markdown format. Eliminates model mistakes in table alignment, column ordering, heading format. Each field can be independently validated (e.g., `--tag` must be allowed value).

### Decision 69 — File-path arguments for targeted validation

`ws validate` accepts optional file paths as positional arguments. With paths: validates only those files. Without paths: validates entire workspace. Workspace-wide checks (`attention`, `structure`) ignore file-path arguments and run only in full-workspace mode.

**Rationale:** Pre-commit hook needs to validate only staged files. Without file-path filtering, the hook either runs the full suite or reimplements validation logic.

### Decision 70 — Minimum required sections in template

`ws create` generates 7 sections: Intent, Success evidence, Constraints and non-goals, Evidence ledger, Open questions, Next move, History. Optional sections added by agents/CLI when needed. Decisions section generated with structured template for gate readiness.

**Rationale:** 14 empty placeholders are noise. Empty `## Grilling Session` and `## Observed outcome` in a fresh object suggest phases that haven't been considered. Every real Work Object uses the minimum set.

---
