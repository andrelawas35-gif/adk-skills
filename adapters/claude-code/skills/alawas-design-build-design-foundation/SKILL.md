---
name: alawas-design-build-design-foundation
description: "Use when a target project's design tokens need discovery and audit; inspects codebase for typography, spacing, colors, and themes; does not modify any project files."
default_tier: medium
platform: claude-code
---
# Build Design Foundation

## Governing principle

Design tokens in code are canonical (ADR 0024). Before design work can
reference or map tokens, the target project's token landscape must be
discovered from its codebase — CSS custom properties, theme objects,
token files, utility classes — so that downstream skills work from the
actual token values, not assumptions.

## Boundaries and non-goals

This skill does:

- Discover the target project's design tokens by inspecting the codebase:
  CSS custom properties, theme configurations, token files, utility classes.
- Audit token coverage: identify gaps (missing dark mode tokens, incomplete
  spacing scales, undefined typography variants).
- Produce a `[system:token-inventory]` Evidence Ledger entry containing the
  token snapshot.
- Operate independently of `alawas-design-audit-product-interface` — token discovery may
  run without structural discovery (DEC-6).

This skill does not:

- It does not modify any host-project files, configuration, or tokens.
- Discover routes, components, or layouts (that is `alawas-design-audit-product-interface`).
- Create or recommend new tokens — it reports what exists.
- Sync tokens to external design tools.
- Produce durable artifacts — the token inventory is ephemeral.

## Inputs and preconditions

**Required input:** a readable Work Object in the `explore` state with access
to the target project's codebase.

**Preconditions:** `alawas-governance-conduct-work-object` has discovered the workspace and
established the Work Object. The target project root is identifiable. A prior
`[system:discovery]` entry is helpful but not required (DEC-6: separate audit
and foundation).

## Required capabilities

- `file_read` — read host-project source files (CSS, theme configs, token files).
- `directory_list` — enumerate host-project directories.
- `glob_search` — find token-related files by pattern.
- `content_search` — search for token patterns (CSS custom properties, theme keys).
- `structured_output` — produce the token inventory.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- This skill performs only reads and observations — **low consequence**.
- No host-project files are created, modified, or deleted.
- The token inventory is written to the Work Object's Evidence Ledger
  through the conductor.
- A high-consequence Work Object requires explicit confirmation naming the
  proposed mutation. Do not stage, annotate, change status, append History,
  or make any other mutation before receiving that scoped confirmation;
  reading and recommending remain allowed.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

The foundation lens asks:

1. Are discovered tokens complete for the target project's design needs?
2. Are there inconsistencies (e.g., different spacing scales in different files)?
3. Is the token organization pattern conventional for the framework?

## Skill Grilling Profile

Apply the `alawas-design-build-design-foundation` profile and continuous Grilling Session
in `references/SKILL-AWARE-GRILLING.md`.

## Stage workflow

### 1. Discover token sources

Inspect the target project for token-bearing files: CSS files with custom
properties, theme configuration objects (Tailwind config, MUI theme, Chakra
theme), dedicated token files (JSON, YAML, JS/TS exports), and CSS-in-JS
definitions.

### 2. Extract token values

Parse discovered sources to extract: color palettes, typography scales
(font families, sizes, weights, line heights), spacing scales, border radii,
shadows, breakpoints, z-index scales, and animation/transition tokens.

### 3. Audit coverage

Identify gaps: missing semantic tokens (e.g., colors defined without semantic
aliases), incomplete scales (e.g., spacing jumps from 4 to 16), absent dark
mode variants, undefined responsive breakpoints.

### 4. Produce inventory

Assemble the discovery into a `[system:token-inventory]` Evidence Ledger
entry containing: token sources, extracted values by category, coverage
assessment, and identified gaps.

## Routing and termination

**Route when:**
- Token discovery is complete — return to `alawas-governance-conduct-work-object`.
- A gap requires user input (e.g., which file is the canonical token source).

**Terminate when:**
- The token inventory is recorded in the Evidence Ledger.
- The target project has no discoverable tokens (report as gap).

## Output contract

The `[system:token-inventory]` entry contains:

- `sources`: files and patterns where tokens were found
- `colors`: palette and semantic color tokens with values
- `typography`: font families, size scale, weight scale, line heights
- `spacing`: spacing scale with values
- `other`: borders, shadows, breakpoints, z-indices, animations
- `gaps`: missing or inconsistent tokens

## Final self-check

- [ ] Token inventory is a `[system:token-inventory]` Evidence Ledger entry
- [ ] No host-project files were modified
- [ ] Token extraction is evidence-based, not assumed
- [ ] Gaps reported honestly, not filled with defaults
- [ ] Inventory is structured for downstream consumption
- [ ] Independent of structural discovery (DEC-6)
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
| `file_read` | `Read` | native |
| `directory_list` | `Bash ls` | native |
| `glob_search` | `Glob` | native |
| `content_search` | `Grep` | native |
| `structured_output` | `—` | native |
