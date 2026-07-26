---
name: alawas-connect-design-to-code
description: "DEFERRED. Use when code components need mapping to Figma components; governs Figwright's component_map to maintain a durable component registry; does not modify code or canvas content."
platform: claude-code
---
# Connect Design to Code

## Governing principle

A component registry is the bidirectional bridge between code and Figma.
It maps code components to their Figma counterparts so that rendering,
parity checking, and design iteration can cross the boundary reliably.
The registry is durable — it accumulates mappings over time rather than
being regenerated each pass (DEC-13, ADR 0028).

## Boundaries and non-goals

This skill does:

- Create and maintain `design/components/registry.yaml` in the host project
  (DEC-13, ADR 0028).
- Map code components (from `[system:discovery]`) to Figma components
  (from Figwright's component inventory).
- Govern Figwright's `component_map` — provide the registry as input to
  Figwright calls, record what Figwright returns.
- Update the registry incrementally (append-and-update, not regenerate).

This skill does not:

- Modify host-project code or Figma canvas content.
- Create or delete Figma components.
- Render interfaces (that is `alawas-render-to-figma`).
- Discover components (that is `alawas-audit-product-interface`).

## Inputs and preconditions

**Required input:** a readable Work Object in the `build` state with a
`[system:discovery]` entry containing the component inventory.

**Preconditions:** `alawas-audit-product-interface` has produced a discovery snapshot.
Figwright MCP is configured (or capability degradation applies — the code-side
registry can be created without Figma).

## Required capabilities

- `file_read` — read discovery snapshot, existing registry.
- `file_write` — create or update the component registry.
- `structured_output` — produce YAML registry entries.
- `user_confirmation` — confirm before meaningful-consequence actions.

### MCP dependencies (not platform capabilities)

Figwright MCP component inventory — enumerate available Figma components.
Capability degradation applies when Figwright is unavailable.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Creating the registry file is **meaningful consequence**.
- Adding or updating mappings is **meaningful consequence**.
- The registry is append-and-update — existing mappings are not deleted
  without explicit authority.
- A high-consequence Work Object requires explicit confirmation naming the
  proposed mutation. Do not stage, annotate, change status, append History,
  or make any other mutation before receiving that scoped confirmation;
  reading and recommending remain allowed.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only
its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only
under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

The connection lens asks:

1. Are the code and Figma components actually the same component?
2. Are prop/variant mappings accurate?
3. Are there stale mappings for components that no longer exist in code?

## Skill Grilling Profile

Apply the `alawas-connect-design-to-code` profile and continuous Grilling Session
in `references/SKILL-AWARE-GRILLING.md`.

## Stage workflow

### 1. Load existing registry

Read `design/components/registry.yaml` if it exists. This is the starting
point — new mappings are added to it, not replacing it.

### 2. Identify unmapped components

Compare the discovery snapshot's component inventory against the registry.
Identify code components without Figma mappings and vice versa.

### 3. Query Figma components

If Figwright is available, query its component inventory to find matching
Figma components. Match by name, structure, and prop/variant correspondence.

If Figwright is unavailable, create code-side-only registry entries with
the Figma side marked as unmapped. Record `[system:capability-gap]`.

### 4. Propose mappings

For each unmapped code component with a Figma match, propose a mapping
including: code component path, Figma component key, prop/variant mappings,
and confidence level.

### 5. Update registry

After user confirmation, update `design/components/registry.yaml` with
new and updated mappings. The `design/components/` directory is created
if it does not exist (meaningful consequence).

## Routing and termination

**Route when:**
- Registry is updated — return to `alawas-conduct-work-object`.
- Missing components need creation — route to the appropriate skill.

**Terminate when:**
- Registry is written/updated and confirmed.
- All discoverable mappings are recorded (some may remain unmapped).

## Output contract

Registry file at `design/components/registry.yaml` contains:

- `mappings`: list of component mappings, each with:
  - `code_component`: path, export name, props interface
  - `figma_component`: key, name, variants
  - `prop_mapping`: code prop → Figma variant correspondence
  - `confidence`: high | medium | low
  - `last_verified`: timestamp of last verification
- `unmapped_code`: code components without Figma counterparts
- `unmapped_figma`: Figma components without code counterparts

## Final self-check

- [ ] Registry is a durable file at `design/components/registry.yaml`
- [ ] Existing mappings were preserved (append-and-update, not regenerated)
- [ ] Prop/variant mappings are accurate
- [ ] Unmapped components are explicitly listed
- [ ] No host-project code or Figma canvas was modified
- [ ] Capability degradation is explicit when Figwright unavailable
---

## Platform Adapter

Invocation-relevant wiring only; installation and maintainer guidance live outside this file.

### Required capability mappings

| Abstract capability | Platform tool | Classification |
|---------------------|---------------|----------------|
| `file_read` | `Read` | native |
| `file_write` | `Write / Edit` | native |
| `structured_output` | `—` | native |
| `user_confirmation` | `conversation turn` | native |
