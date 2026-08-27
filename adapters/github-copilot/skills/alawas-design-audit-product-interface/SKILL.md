---
name: alawas-design-audit-product-interface
description: "Use when a target project's interface structure needs discovery; inspects codebase for routes, components, layouts, and framework conventions; does not modify any project files."
default_tier: medium
platform: github-copilot
---
# Audit Product Interface

## Governing principle

Design skills operate on what exists, not what is assumed. Before any design
work begins, the target project's interface structure must be discovered from
its codebase — routes, components, layouts, framework conventions — so that
downstream skills work from observed facts, not guesses.

## Boundaries and non-goals

This skill does:

- Discover the target project's framework, routing structure, component tree,
  and layout conventions by inspecting the codebase.
- Produce a `[system:discovery]` Evidence Ledger entry containing the
  structural snapshot.
- Run once per design pass; downstream skills read the result rather than
  re-scanning (DEC-3).
- Detect and report ambiguity (multiple frameworks, unconventional structure)
  as gaps rather than guesses.

This skill does not:

- It does not modify any host-project files, configuration, or code.
- Discover design tokens (that is `alawas-design-build-design-foundation`'s domain).
- Produce durable artifacts — the discovery snapshot is ephemeral.
- Require any host-project manifest or configuration (DEC-2: zero onboarding).
- Implement, design, or render anything.

## Inputs and preconditions

**Required input:** a readable Work Object in the `explore` state with access
to the target project's codebase.

**Preconditions:** `alawas-governance-conduct-work-object` has discovered the workspace and
established the Work Object. The target project root is identifiable. No prior
discovery is required — this skill produces the first discovery snapshot.

## Required capabilities

- `file_read` — read host-project source files (configs, routes, components).
- `directory_list` — enumerate host-project directories.
- `glob_search` — find files by pattern (e.g., `*.tsx`, `routes.*`).
- `content_search` — search for framework-specific patterns.
- `structured_output` — produce the discovery snapshot.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- This skill performs only reads and observations — **low consequence**.
- No host-project files are created, modified, or deleted.
- The discovery snapshot is written to the Work Object's Evidence Ledger
  through the conductor.
- A high-consequence Work Object requires explicit confirmation naming the
  proposed mutation. Do not stage, annotate, change status, append History,
  or make any other mutation before receiving that scoped confirmation;
  reading and recommending remain allowed.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

The discovery lens asks:

1. Is the discovered structure consistent with the framework's conventions?
2. Are there components or routes that the discovery missed?
3. Does the snapshot contain enough detail for downstream skills?

## Skill Grilling Profile

Apply the `alawas-design-audit-product-interface` profile and continuous Grilling Session
in `references/SKILL-AWARE-GRILLING.md`.

## Stage workflow

### 1. Identify framework

Inspect the target project for framework indicators: `package.json`
dependencies, configuration files (`next.config.*`, `vite.config.*`,
`angular.json`, etc.), directory conventions (`app/`, `pages/`, `src/`).

Report the detected framework and version. If ambiguous, report the ambiguity
as a `[gap]` entry.

### 2. Discover routes

Find the routing structure: file-based routes (Next.js, Remix, SvelteKit),
configuration-based routes (React Router, Angular), or other patterns. Produce
a route tree with path patterns, associated components, and layout wrappers.

### 3. Discover components

Enumerate UI components: their locations, export patterns, prop interfaces,
and composition relationships. Distinguish page-level components from
reusable/shared components.

### 4. Discover layouts

Identify layout patterns: root layouts, nested layouts, error boundaries,
loading states, and shared wrappers.

### 5. Produce snapshot

Assemble the discovery into a `[system:discovery]` Evidence Ledger entry
containing: framework, route tree, component inventory, layout structure,
and any gaps or ambiguities.

## Routing and termination

**Route when:**
- Discovery is complete — return to `alawas-governance-conduct-work-object` with the snapshot.
- An ambiguity requires user input — pause and ask.

**Terminate when:**
- The discovery snapshot is recorded in the Evidence Ledger.
- The target project has no discoverable interface structure (report as gap).

## Output contract

The `[system:discovery]` entry contains:

- `framework`: detected framework name and version
- `routes`: route tree with paths, components, and layouts
- `components`: inventory with locations, exports, and relationships
- `layouts`: layout hierarchy and composition
- `gaps`: ambiguities, missing information, unconventional patterns

## Final self-check

- [ ] Discovery snapshot is a `[system:discovery]` Evidence Ledger entry
- [ ] No host-project files were modified
- [ ] Framework detection is evidence-based, not assumed
- [ ] Ambiguities reported as gaps, not resolved by guessing
- [ ] Snapshot contains enough detail for downstream skills
- [ ] Discovery ran once — not re-triggered within the same pass
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

For a high-consequence Work Object, confirmation must name the exact
proposed mutation. Do not stage, annotate, change status, append History,
or make any other mutation before receiving that scoped confirmation.

### Model tier

This skill declares `default_tier: medium`.
The platform overlay resolves this to `claude-sonnet-4-20250514`.
The prompt budget for this tier is approximately 40000 tokens (advisory).

**Consequence-based escalation:** When a Work Object has `consequence: meaningful`,
the effective tier is upgraded to at least `medium`. When `consequence: high`,
the effective tier is upgraded to the strongest available model.
`actual_tier = max(skill.default_tier, consequence_escalation(wo.consequence))`.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read_file` | native |
| `directory_list` | `list_dir` | native |
| `glob_search` | `file_search` | native |
| `content_search` | `grep_search` | native |
| `structured_output` | `—` | native |
