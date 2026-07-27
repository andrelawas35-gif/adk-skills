---
name: alawas-design-track-components
description: "Use when durable components must be registered, swept, grilled, cascaded, or retired; returns ledger and inbox mutation proposals; never turns findings into Work Objects or commitments automatically."
default_tier: medium
platform: codex
---
# Track Components

## Governing principle

The component ledger is a derived, per-project index of durable capabilities.
It preserves a component's location, lineage, and improvement state while the
component itself remains authoritative in its code, skill, ADR, or schema.
A manual sweep detects and queues improvement signals; it never converts
detection into unapproved commitment.

## Boundaries and non-goals

This skill does:

- Register a durable capability when its shipping Work Object supplies the
  required location, lineage, dependencies, criteria, and authority.
- Maintain the canonical `.work-studio/component-ledger.md` schema and entry
  lifecycle: `active`, `settled`, `needs-regrill`, or `retired`.
- Run a user-invoked sweep that ranks non-retired entries by grilling debt and
  respects a settled cooldown unless a mechanical reopen trigger fires.
- Grill one selected component against its applicable inline dimensions and the
  owning skill's Grilling Profile, then either re-stamp it or queue an inbox
  signal for an actionable finding.
- Cascade a declared contract change to declared dependents and retire, rather
  than delete, a removed component.

This skill does not:

- Copy a component's implementation into the ledger, infer dependency edges,
  invent criteria, or claim a component is settled without a completed pass.
- Schedule or autonomously run sweeps, edit the component under review,
  create a Work Object from a finding, or mass-spawn Work Objects.
- Alter `references/AGREEMENT-LOOP.md`, scorecard rules, another skill's
  Grilling Profile, or the Workspace Documentation Contract without the
  separately required authority.

## Inputs and preconditions

**Required input:** a registration, manual `sweep`, grilling-pass, cascade, or
retirement request, plus the canonical `component-ledger` registry entry in
`WORKSPACE-DOCUMENTATION-CONTRACT.md`.

**For registration:** a shipping Work Object, component name and resolved
location(s), declared dependency edges, applicable dimensions, owning skill
where relevant, and the authority required by the Work Object.

**For a grilling pass:** a non-retired entry, readable pointed-at component and
owning Grilling Profile, current Git SHA where Git is available, and a human
request selecting the pass or manual sweep.

If the contract, pointer, required lineage, authority, or profile is absent,
record the explicit gap per `references/MISSING-ARTIFACT-GAP.md` and route to
`alawas-governance-conduct-work-object`; do not guess it.

## Required capabilities

- `file_read` and `content_search` — read the contract, ledger, pointed-at
  component, Work Object lineage, inbox, and owning profile.
- `file_write` — return a bounded ledger or inbox mutation to
  `alawas-governance-conduct-work-object` for persistence.
- `terminal_run` — obtain the current Git SHA and inspect drift for declared
  locations when Git is available.
- `user_confirmation` — obtain authority for an entry mutation, a changed
  criterion or edge, a contract change, or a material deviation.
- `structured_output` — report debt inputs, pass result, queued signals,
  mutation status, and remaining gaps.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md` and the Workspace Documentation
Contract.

- A shipping Work Object authorizes only the entry mutation within its accepted
  boundary. An unapproved edge, criterion, schema, or contract change remains
  a decision gap.
- A sweep can write only a dated inbox signal and an entry status or
  last-grilled re-stamp when its applicable mutation authority is present; it
  never creates a Work Object.
- A contract-change cascade follows an explicit closeout `yes`; it flags every
  declared dependent `needs-regrill` and leaves the changed component's own
  lineage intact.
- A high-consequence mutation requires confirmation naming the exact ledger or
  inbox mutation before any persistence. Do not stage, annotate, change status,
  append History, or make any other mutation before that confirmation.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its
stage-specific lens below. A manual sweep is not permission for a later
component edit, a future Work Object, or scheduling.

Outside an explicit grilling request, nominate a Grilling Candidate only under
the Agreement Loop's three-part threshold. Show its Candidate Card and wait for
explicit entry; do not silently start a continuous session.

## Skill Grilling Profile

Apply the `alawas-design-track-components` profile and continuous Grilling Session in
`references/SKILL-AWARE-GRILLING.md`

## Ledger schema

The canonical ledger is Markdown with one `## COMP-NNN — <name>` section per
component. Every entry contains:

```markdown
- **status:** active | settled | needs-regrill | retired
- **location(s):** <one or more canonical paths or pointers>
- **built-by Work Object(s):** <immutable IDs, or pre-ledger backfill>
- **depends-on:** <declared component IDs or none>
- **depended-on-by:** <declared component IDs or none>
- **applicable dimensions:** <subset of recovery quality, personal fit, artifact value, novelty yield>
- **owning skill/profile:** <skill or none>
- **last-grilled-SHA:** <Git SHA | not-yet-grilled>
- **best-case anchor:** Option-B-refined: no surviving finding against applicable dimensions and owning profile; reopen on git drift, owning-skill-version change, or contrary govern-scorecards outcome evidence
- **status rationale / findings:** <dated pointer or none>
```

`COMP-NNN` identities never change. Removed components are marked `retired`;
their lineage and pointers remain readable but they are excluded from scoring.

## Stage workflow

### 1. Register on ship or backfill

Confirm the durable capability is within the shipping Work Object's accepted
scope, resolve every location, capture declared rather than inferred edges,
and select only applicable inline dimensions. Assign the next immutable
`COMP-NNN` identifier. Backfill uses `pre-ledger backfill` when no building
Work Object is known and starts at `active` with `last-grilled-SHA:
not-yet-grilled`.

### 2. Run a manual sweep

For each non-retired entry, compute and show the qualitative debt inputs:
consequence, staleness, declared blast radius, and Git drift since
`last-grilled-SHA`. A settled entry remains in cooldown until staleness becomes
material or a reopen trigger fires. Reopen immediately when declared locations
drift, the owning skill version changes, or contrary outcome evidence is
recorded; set `needs-regrill`. Rank entries by the resulting debt, explain
ties, and select only the requested or highest-ranked component for a pass.

### 3. Grill one component

Read the pointed-at component and the owning profile. Test every applicable
dimension with file-grounded evidence. A pass with no surviving finding marks
the entry `settled` and re-stamps `last-grilled-SHA`. A concrete actionable
finding marks it `needs-regrill`, preserves the finding pointer, and queues a
dated inbox signal. Do not open a Work Object; the user promotes one signal at
a time under the attention rule.

### 4. Cascade contract changes

At closeout of an accepted component-improvement Work Object, require the
explicit question: "Did this change the component's contract? y/n." On `yes`,
mark every declared dependent `needs-regrill`, identify the source component
and Work Object, and increase its priority on the next manual sweep. On `no`,
leave dependents unchanged. A missing edge is an explicit coverage gap, not
permission to infer one.

### 5. Retire without deletion

When an authorized change removes a capability, set its status to `retired`,
record the removal source and date, and exclude it from future sweeps. Never
reuse its identifier or erase lineage.

## Evidence and Work Object updates

Label local files and command results `[system]`, approval `[decision]`, and
reasoning `[inference]`. Return `alawas-governance-conduct-work-object` a concise record with
the entry ID, requested operation, resolved pointers, lineage, debt inputs,
reopen trigger or cooldown, pass evidence, findings or re-stamp, inbox signal,
cascade or retirement result, authority, and unverified gaps. The conductor
owns durable Work Object History and lifecycle changes.

## Routing and termination

- **Registration or re-stamp within authority:** route the record to
  `alawas-governance-conduct-work-object`.
- **Actionable finding:** queue one inbox signal and route its promotion to the
  user; do not create a Work Object.
- **Missing pointer, edge, criterion, or authority:** stop the mutation and
  route to the conductor or decision owner.
- **Git unavailable:** record drift as unverified; do not assert no drift.
- **Component removed:** retain its entry as `retired` and route the record to
  the conductor.

## Output template

```markdown
## Component tracking

- **Operation and entry:** <register | sweep | grill | cascade | retire; COMP-NNN>
- **Authority and boundary:** <Work Object / owner approval and scope>
- **Pointers and lineage:** <resolved locations, Work Objects, declared edges>
- **Debt / reopen status:** <inputs, cooldown, or mechanical trigger>
- **Pass or finding:** <dimensions, profile, evidence, status>
- **Inbox / cascade:** <signal or dependent entries; none if not applicable>
- **Verification gaps:** <none | exact gap>
- **Next route:** <conductor | decision | user promotion | manual fallback>
```

## Final self-check

- Is every ledger entry a pointer and lineage record rather than duplicated
  component truth?
- Did a sweep remain manual and queue signals instead of creating Work Objects?
- Did settled status require a completed pass with no surviving finding?
- Did mechanical reopen, declared dependency cascade, and retirement preserve
  history without inventing edges or deleting entries?
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Epistemic rules

This skill uses the **essential 3‑tag system** (`references/epistemic/epistemic-rules-essential.md`).

The epistemic tier is resolved from the skill's `default_tier` (medium).
**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the epistemic tier is upgraded to at least `medium` (essential 3‑tag).
When `consequence: high`, the epistemic tier is upgraded to the strongest
available tier (full 6‑tag).
`actual_epistemic_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.


### Runtime pin resolution

Codex can discover both user and repository skills with the same name.
Before applying this skill, search upward from the current directory for
`.work-studio/adapter.codex.lock`, stopping at the repository or filesystem
boundary. Read its `dest` value and
resolve `<dest>/<this-skill-name>/SKILL.md`. When that path differs from
the currently loaded copy, **load and follow the pinned copy** before
continuing. A matching legacy `adapter.lock` remains valid during migration.
If the pinned file is unavailable, report the broken pin and
stop instead of silently falling back to the global copy.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read_file` | native |
| `content_search` | `grep_search` | native |
| `file_write` | `create_file / replace_string_in_file` | native |
| `terminal_run` | `run_in_terminal` | native |
| `user_confirmation` | `conversation turn` | native |
| `structured_output` | `—` | native |
