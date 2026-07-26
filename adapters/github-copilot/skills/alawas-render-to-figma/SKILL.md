---
name: alawas-render-to-figma
description: "DEFERRED. Use when a verified interface specification needs Figma output; wraps Figwright with authority gates and preservation policy; does not modify approved frames without high-consequence confirmation."
platform: github-copilot
---
# Render to Figma

## Governing principle

Figma output produced by Work Studio represents verified state, not
unverified intent. Every render passes through authority gates, requires
browser evidence (ADR 0027), creates new pages (ADR 0026), and records
full provenance. Figwright provides execution; this skill provides
governance (ADR 0025).

## Boundaries and non-goals

This skill does:

- Invoke Figwright's `figma-build` skill to create Figma output from a
  verified interface specification.
- Enforce the always-new write policy: create new pages/sections named
  `{WO-ID} / {spec-slug} / pass-{N}` (ADR 0026).
- Require `[system:browser-evidence]` before any Figwright invocation
  (ADR 0027).
- Record Figwright inputs, outputs (including node IDs), and success/failure
  in the Evidence Ledger.
- Update the Figma manifest (`design/manifests/figma.yaml`) with new page
  entries.
- Degrade gracefully when Figwright is unavailable — record
  `[system:capability-gap]` and complete the code-side workflow.

This skill does not:

- Modify existing Figma frames without explicit governed update authority.
- Delete any Figma content (prohibited by ADR 0026).
- Create Figma output without browser evidence (no bypass, ADR 0027).
- Implement code changes or modify host-project source files.
- Map components — that is `alawas-connect-design-to-code`.

## Inputs and preconditions

**Required input:** a readable Work Object in the `build` state with:
- A verified interface specification at `design/specs/<slug>.yaml`.
- A `[system:browser-evidence]` Evidence Ledger entry referencing the
  specification being rendered.

**Preconditions:** the specification exists and is verified. Browser evidence
exists. Figwright MCP is configured (or capability degradation applies).

## Required capabilities

- `file_read` — read specifications, token inventory, Figma manifest.
- `file_write` — update Figma manifest in the host project.
- `structured_output` — produce evidence entries.
- `user_confirmation` — confirm before meaningful-consequence actions.
- `browser_automation` — verify specification against running application
  (manual-fallback acceptable; see ADR 0027).

### MCP dependencies (not platform capabilities)

Figwright MCP `figma-build` — create Figma pages from specifications.
Capability degradation applies when Figwright is unavailable.

## Consequence and authority rules

Apply `references/CONSEQUENCE-AUTHORITY.md`.

- Creating a new Figma page (always-new) is **meaningful consequence**.
- Updating a non-approved frame requires: node ID in Evidence Ledger +
  frame not approved + explicit user direction — **meaningful consequence**.
- Updating an approved frame requires explicit named confirmation —
  **high consequence** regardless of the Work Object's consequence level.
- Deleting Figma content is **prohibited**.
- A high-consequence Work Object requires explicit confirmation naming the
  proposed mutation. Do not stage, annotate, change status, append History,
  or make any other mutation before receiving that scoped confirmation;
  reading and recommending remain allowed.

## Grilling entry and stage lens

Follow `references/AGREEMENT-LOOP.md` in full; this skill contributes only
its stage-specific lens below.

Outside an explicit grilling request, nominate a Grilling Candidate only
under the Agreement Loop's three-part threshold. Show its Candidate Card and wait for explicit entry; do not silently start a continuous session.

The render lens asks:

1. Does the browser evidence confirm the specification matches reality?
2. Is the Figma manifest up to date with prior renders?
3. Would this render affect any approved frames?

## Skill Grilling Profile

Apply the `alawas-render-to-figma` profile and continuous Grilling Session in
`references/SKILL-AWARE-GRILLING.md`.

## Stage workflow

### 1. Verify preconditions

Check for: specification file existence, `[system:browser-evidence]` entry
referencing the specification, Figwright MCP availability.

If browser evidence is missing, stop. Do not proceed.
If Figwright is unavailable, record `[system:capability-gap]` and stop with
the code-side workflow complete.

### 2. Prepare Figwright invocation

Assemble the Figwright input: specification content, token mappings from
`[system:token-inventory]`, component mappings from
`design/components/registry.yaml` (if exists).

Determine the page name: `{WO-ID} / {spec-slug} / pass-{N}` where N is
incremented from the Figma manifest's existing entries.

### 3. Authority gate

Check consequence level. For meaningful consequence (new page), confirm
with the user. For high consequence (approved frame update), require explicit
named confirmation.

### 4. Invoke Figwright

Call Figwright's `figma-build` with the prepared input. Record the full
invocation (inputs and parameters) in the Evidence Ledger.

### 5. Record results

Capture Figwright's response: node IDs, page identifiers, success/failure
status. Record as a `[system:figma-render]` Evidence Ledger entry.

Update `design/manifests/figma.yaml` with the new page entry (file key,
page name, node IDs, parity status: unchecked, Work Object ID).

### 6. Capability degradation

When Figwright is unavailable at any step:
- Record `[system:capability-gap]` with the specific operation that was
  deferred.
- Report the gap explicitly — never claim Figma output was produced.
- The code-side workflow (specification, evidence) is complete; Figma
  rendering is deferred.

## Routing and termination

**Route when:**
- Render is complete — return to `alawas-conduct-work-object`.
- Parity verification is needed — route to `verify-design-code-parity`.

**Terminate when:**
- Figma page is created and manifest updated, or
- Capability gap is recorded and code-side workflow is complete.

## Output contract

Evidence entries produced:
- `[system:figma-render]`: Figwright invocation inputs, node IDs returned,
  success/failure status.
- `[system:capability-gap]` (when applicable): specific Figma operation
  deferred.

Durable artifact updated:
- `design/manifests/figma.yaml`: new page entry with file key, page name,
  node IDs, parity status, Work Object ID.

## Final self-check

- [ ] Browser evidence exists and references the rendered specification
- [ ] Figma page name follows `{WO-ID} / {spec-slug} / pass-{N}` convention
- [ ] Authority gate fired before Figwright invocation
- [ ] Figwright inputs and outputs are recorded in Evidence Ledger
- [ ] Figma manifest is updated with the new page entry
- [ ] No existing Figma content was modified without governed update authority
- [ ] No Figma content was deleted
- [ ] Capability degradation is explicit when Figwright unavailable
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
| `browser_automation` | `—` | manual-fallback |

### Capability Degradation

Apply `references/CAPABILITY-DEGRADATION.md`. Per-capability
classifications and notes below.

#### `browser_automation` (manual-fallback)

- **Behavior**: Pause and give one concrete manual instruction.
- **Record**: Append History entry noting the capability gap, the
  manual action taken, and what remains unverified.
- **Note**: GitHub Copilot browser automation requires user interaction for complex workflows. Use manual steps for multi-page flows.
