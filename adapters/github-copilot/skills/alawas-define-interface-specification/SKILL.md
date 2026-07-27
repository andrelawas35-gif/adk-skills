---
name: alawas-define-interface-specification
description: "Use when a screen needs a machine-readable specification connecting natural language, code, and Figma; produces durable YAML specs; does not implement the specified interface."
platform: github-copilot
---
# Define Interface Specification

## Governing principle

A specification is the contract between creative intent and implementation.
It must be precise enough for a skill to implement from, reviewable enough
for a human to validate, and machine-readable enough for parity checking.
Specifications live in the host project as durable, version-controlled YAML
files (DEC-11, ADR 0028).

## Boundaries and non-goals

This skill does:

- Translate architecture and design direction into machine-readable interface
  specifications.
- Produce durable specification files at `design/specs/<slug>.yaml` in the
  host project.
- Reference discovery, token inventory, architecture, and user flows to
  ground specifications in evidence.
- Define layout structure, component usage, token references, responsive
  behavior, and interaction patterns for each screen.

This skill does not:

- Implement the specified interface.
- Create Figma output (that is `alawas-render-to-figma`).
- Define navigation or screen hierarchy (that is `alawas-define-interface-architecture`).
- Modify existing host-project code.
- Invent tokens — specifications reference existing tokens from the inventory.

## Inputs and preconditions

**Required input:** a readable Work Object in the `design` state with
architecture documents and token inventory available.

**Preconditions:** `alawas-define-interface-architecture` has produced architecture
documents. `alawas-build-design-foundation` has produced a `[system:token-inventory]`
entry. The `[system:discovery]` entry exists.

## Required capabilities

- `file_read` — read architecture, tokens, discovery, and existing specs.
- `file_write` — create specification files in the host project.
- `structured_output` — produce YAML specifications.
- `user_confirmation` — confirm specification accuracy with the user.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Creating a new specification file is **meaningful consequence**.
- Reading existing specifications and evidence is low consequence.
- Modifying an existing specification file is meaningful consequence.
- A high-consequence Work Object requires explicit confirmation naming the
  proposed mutation. Do not stage, annotate, change status, append History,
  or make any other mutation before receiving that scoped confirmation;
  reading and recommending remain allowed.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only
its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only
under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

The specification lens asks:

1. Does the specification reference actual tokens from the inventory?
2. Is the layout structure feasible for the discovered framework?
3. Are responsive breakpoints and behavior explicitly defined?

## Skill Grilling Profile

Apply the `alawas-define-interface-specification` profile and continuous Grilling
Session in `references/SKILL-AWARE-GRILLING.md`.

## Stage workflow

### 1. Select screen

From the architecture document, select the screen to specify. Confirm with
the user if multiple screens are candidates.

### 2. Define layout structure

Specify the screen's layout: grid/flex structure, content areas, component
placement, and spatial relationships. Reference tokens for spacing and
sizing.

### 3. Specify components

For each component in the layout: its type (from the discovery's component
inventory or new), its props/configuration, its content, and its token
references (colors, typography, spacing).

### 4. Define responsive behavior

Specify how the layout adapts across breakpoints: which components reflow,
hide, or change size. Reference breakpoint tokens from the inventory.

### 5. Define interaction patterns

Specify user interactions: hover states, focus states, click/tap behavior,
form validation, loading states, error states. Reference the user flow for
context.

### 6. Write specification

Create `design/specs/<slug>.yaml` with the complete specification. The
`design/specs/` directory is created if it does not exist (meaningful
consequence).

## Routing and termination

**Route when:**
- Specification is written — return to `alawas-conduct-work-object`.
- Specification reveals missing tokens or components — route back to
  `alawas-build-design-foundation` or `alawas-audit-product-interface`.

**Terminate when:**
- Specification file is written and confirmed.
- All layout, component, responsive, and interaction details are specified.

## Output contract

Each specification file at `design/specs/<slug>.yaml` contains:

- `screen`: screen identifier matching the architecture document
- `layout`: grid/flex structure with spatial relationships
- `components`: list with type, props, content, and token references
- `responsive`: per-breakpoint adaptations
- `interactions`: hover, focus, click, validation, loading, error states
- `tokens`: all referenced token keys with their source

## Final self-check

- [ ] Specification is a durable file at `design/specs/`
- [ ] All token references point to tokens in the inventory
- [ ] Layout structure is feasible for the discovered framework
- [ ] Responsive behavior covers the token inventory's breakpoints
- [ ] Interaction patterns reference the user flow
- [ ] No host-project code was modified
- [ ] User confirmed specification before recording
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `read_file` | native |
| `file_write` | `create_file / replace_string_in_file / multi_replace_string_in_file` | native |
| `structured_output` | `—` | native |
| `user_confirmation` | `conversation turn` | native |
