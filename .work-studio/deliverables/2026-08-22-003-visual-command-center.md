# How to build a visual central command center for Work Studio

Report-type deliverable for Work Object `2026-08-22-003`. Produced as
tracer-bullet Decision 2's test run: today's unmodified
`alawas-research-produce-report` decomposition process, no code changes.

## Sub-questions and outcomes

### 1. What structured data does Work Studio already expose?

**Outcome: answered.**

- `[system]` Every Work Object's YAML frontmatter is machine-readable:
  `id`, `title`, `type`, `status`, `state`, `consequence`, `sensitivity`,
  `created_at`, `updated_at`, `next_action`.
- `[system]` The body carries further structured material: `Decisions and
  revisit triggers` (per-decision fields: type, result, scope,
  authorization, confidence, actor, revisit trigger, rationale), the
  `Evidence ledger` (tag/source/entry rows), and append-only `History`
  entries.
- `[system]` `.work-studio/active.md` names the Primary/Supporting
  attention register.
- `[system]` `work-studio/skill-map.yaml` (built by `ws skill-map build`)
  indexes every core skill's responsibility, non-goals, and required
  capabilities — but is not scoped to only this repo's 22 `alawas-*`
  skills; it includes unrelated personal skills (e.g.
  `business-assess-financial-decision`) from a broader shared skill
  library the generator scans.
- `[system]` `ws outcomes` already computes one real cross-cutting view:
  reviewed vs. unreviewed Work Objects (ran it directly: "0 reviewed, 6
  unreviewed" against the current real workspace).

### 2. Does a dashboard-style read layer already exist?

**Outcome: answered, partially.**

- `[system]` `tools/ws/dashboard_signals.py` exists — but its own
  docstring scopes it to "the bounded epistemic-pressure dashboard
  tracer": claims and conflict records specifically, not general Work
  Object state, decisions, or attention.
- `[system]` `ws skill-map` and `ws outcomes` are real, working, read-only
  computed projections — but neither renders anything visual; both are
  CLI text output.
- `[inference]` A command center's data layer would extend this existing
  pattern (a computed reader over `.work-studio/`), not invent one from
  scratch — but no current reader covers Work Object state/attention/
  decisions as a whole.

### 3. What serving/rendering mechanism fits the studio's own rules?

**Outcome: answered, and this is where a new sub-question appeared.**

- `[system]` `references/EVIDENCE-MODEL.md` states directly: "Any view
  over Work Objects — a report, a summary, a graph, a dashboard — is a
  read-only projection. It never becomes a source, and writing to it is
  not a way to change what the record says." This is a hard constraint
  already decided: a command center must be read-only; any interaction it
  offers must route back through the `ws` CLI, never write `.work-studio/`
  directly.
- `[system]` A Work Studio MCP server already exists (`mcp_server/`, Work
  Object `2026-08-21-010`), but it currently exposes exactly one tool —
  `ws_validate` — and its own Work Object is in `verify` state with an
  explicitly open, undecided question: "which further `ws` commands to
  expose and how authority gating should work for a mutating one."
- **New sub-question, not in the original decomposition:** should a
  command center be served *live* by extending this MCP server (a running
  service a viewer queries), or *generated* as a static artifact
  regenerated on demand (no running service, no new authority-gating
  question)? The MCP server's existing minimal/deferred state makes this
  a real fork, not a hypothetical one — extending it inherits an already
  explicitly-open authority question from a separate Work Object.

### 4. What's the smallest real slice buildable today, with no new capability?

**Outcome: answered.**

- `[inference]` Given (a) the read-only-projection rule, (b) the MCP
  server's exposure question being explicitly unresolved elsewhere, and
  (c) this session's own tooling includes a capability to publish a
  self-contained HTML page (an "Artifact") that can read a live data feed
  without needing `.work-studio/` write access — the smallest real slice
  is: a script that reads `.work-studio/objects/**` + `active.md`
  (the same data `ws outcomes`/`skill-map` already parse) and renders one
  static HTML view of current state, status, consequence, and attention
  across all Work Objects. Regenerated on demand, not live-served,
  sidesteps the MCP authority question entirely, and requires zero new
  capability declarations anywhere in the skill system.

## Supersession and dropped material

None. This is a first pass — no prior deliverable or Decision exists on
this question to supersede.

## Gaps carried forward

- **Unresolved, not investigated:** exact visual layout/information
  architecture (which fields matter most at a glance) — a design
  question, not a research one; belongs to a design pass, not this
  report.
- **Explicitly surfaced, needs a decision:** live-MCP-serve vs.
  static-generated-artifact (sub-question 3's finding). Not resolved here
  — this report only surfaces it.
