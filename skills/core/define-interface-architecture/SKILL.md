---
name: define-interface-architecture
status: deferred
deferred_date: 2026-07-23
deferred_reason: "All structure emerges from conversation (Grilling Session 13, DEC-A11)"
revisit_trigger: "Project complexity requires upfront architectural planning"
description: "DEFERRED. Use when screen hierarchy, navigation, and information architecture need defining; produces durable architecture documents grounded in discovery; does not implement or modify code."
---

# Define Interface Architecture

## Governing principle

Navigation and screen hierarchy are structural decisions that shape every
downstream interface specification. Define them explicitly — which screens
exist, how they relate, what information each contains, and how users move
between them — before specifying individual screen layouts.

## Boundaries and non-goals

This skill does:

- Define screen hierarchy: which screens exist, their parent-child
  relationships, and their purpose.
- Define navigation structure: how users move between screens (links, tabs,
  modals, drawers, breadcrumbs).
- Define information architecture: what content and data each screen presents,
  at what level of detail.
- Produce durable architecture documents at `design/architecture/<slug>.yaml`
  in the host project (DEC-11, ADR 0028).
- Reference discovery (`[system:discovery]`) and user flows
  (`design/flows/`) to ground architecture in evidence.

This skill does not:

- Define individual screen layouts or component specifications
  (that is `define-interface-specification`).
- Implement navigation or routing changes.
- Create Figma output or design tokens.
- Modify existing host-project code.

## Inputs and preconditions

**Required input:** a readable Work Object in the `decide` state with user
flows defined and a `[system:discovery]` entry available.

**Preconditions:** `model-user-flow` has produced flow definitions. The
discovery snapshot exists. The host project root is identifiable.

## Required capabilities

- `file_read` — read discovery snapshot, user flows, and existing architecture.
- `file_write` — create architecture documents in the host project.
- `structured_output` — produce YAML architecture definitions.
- `user_confirmation` — confirm architecture decisions with the user.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Creating a new architecture document is **meaningful consequence**.
- Reading existing architecture and evidence is low consequence.
- Modifying an existing architecture document is meaningful consequence.
- A high-consequence Work Object requires explicit confirmation naming the
  proposed mutation. Do not stage, annotate, change status, append History,
  or make any other mutation before receiving that scoped confirmation;
  reading and recommending remain allowed.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only
its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only
under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

The architecture lens asks:

1. Does the hierarchy match the user flows' navigation patterns?
2. Are all screens in the flows represented in the architecture?
3. Is the navigation structure feasible given the discovered framework?

## Skill Grilling Profile

Apply the `define-interface-architecture` profile and continuous Grilling
Session in `references/SKILL-AWARE-GRILLING.md`.

## Stage workflow

### 1. Inventory required screens

From user flows and discovery, enumerate all screens the interface needs.
Identify which already exist in the codebase and which are new.

### 2. Define hierarchy

Organize screens into a hierarchy: root screens, section screens, detail
screens, modal/overlay screens. Define parent-child relationships.

### 3. Define navigation

Specify how users move between screens: primary navigation (tabs, sidebar),
secondary navigation (breadcrumbs, back buttons), contextual navigation
(links within content), and modal/overlay triggers.

### 4. Define information architecture

For each screen, specify: what data is presented, at what level of detail,
and how it relates to data on other screens. Identify shared data and
cross-screen references.

### 5. Write architecture document

Create `design/architecture/<slug>.yaml` with the complete architecture
definition. The `design/architecture/` directory is created if it does not
exist (meaningful consequence).

## Routing and termination

**Route when:**
- Architecture is defined — return to `conduct-work-object`.
- Architecture decisions require pressure testing — route to
  `pressure-test-decision`.

**Terminate when:**
- Architecture document is written and confirmed.
- All screens from user flows are accounted for.

## Output contract

Each architecture file at `design/architecture/<slug>.yaml` contains:

- `screens`: list of screens with purpose, hierarchy level, and parent
- `navigation`: navigation patterns with type, source, and target
- `information`: per-screen data inventory with detail level
- `gaps`: screens or navigation patterns not yet in the codebase

## Final self-check

- [ ] Architecture document is a durable file at `design/architecture/`
- [ ] All user-flow screens are represented
- [ ] Navigation patterns are grounded in the discovered framework
- [ ] Information architecture specifies data at appropriate detail levels
- [ ] No host-project code was modified
- [ ] User confirmed architecture before recording
