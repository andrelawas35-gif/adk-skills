# Slice 1 Behavioral Fixture — Capability Degradation

This fixture proves that every platform adapter degrades explicitly when a
required capability is unavailable. It exercises native, manual-fallback, and
unsupported paths across the adapter set. No adapter may claim verification,
export, or deployment succeeded when the required capability was unavailable.

## Prerequisites

- Platform adapters are generated for codex, claude-code, and github-copilot
- The `conduct-work-object` skill has a `Required capabilities` section
- The `pressure-test-decision` skill has a `Required capabilities` section
- Each adapter's Platform Adapter section includes a Capability Degradation
  subsection with per-capability classification and degradation behavior
- `references/CAPABILITY-DEGRADATION.md` defines the three-tier model

## Shared across all platforms

### Scenario 1 — Native capability proceeds normally

**Given**: Any platform adapter with `file_read: native`.  
**When**: The skill needs to read a Work Object file.  
**Then**:
1. The adapter uses the native tool without any degradation message
2. No capability gap is recorded in the Work Object
3. The workflow proceeds to the next step

**Verification**: The skill completes the read step without mentioning
capability degradation.

### Scenario 2 — Core skills declare required capabilities

**Given**: The `conduct-work-object` core SKILL.md.  
**When**: Read the `Required capabilities` section.  
**Then**:
1. The section lists at least: `file_read`, `file_write`, `directory_list`,
   `glob_search`, `content_search`, `terminal_run`, `git_operations`,
   `structured_output`
2. Each capability has a brief description of why it's needed
3. The section references `references/CAPABILITY-DEGRADATION.md`

**Verification**: Core skills express capability requirements in abstract
terms, not platform-specific tool names.

### Scenario 3 — Platform adapter documents all classifications

**Given**: Any generated platform adapter (codex, claude-code, or
github-copilot).  
**When**: Read the Platform Adapter → Capability Mappings table.  
**Then**:
1. Every capability from the overlay is listed with its platform tool and
   classification
2. Classifications are one of: `native`, `manual-fallback`, `unsupported`
3. At least one capability per adapter is classified as non-native

**Verification**: The table is present and complete. Non-native capabilities
are clearly marked.

### Scenario 4 — Capability Degradation section explains the rules

**Given**: Any generated platform adapter.  
**When**: Read the Platform Adapter → Capability Degradation subsection.  
**Then**:
1. The three degradation rules are explained:
   - `manual-fallback`: Pause with one concrete instruction, record the gap
   - `unsupported`: Stop the path, record limitation, route elsewhere
   - Stricter safety wins: Platform constraints take precedence
2. The section explicitly states: "Never mark verification, export, or
   deployment as 'successful' when the required capability was unavailable"
3. Each non-native capability has its own sub-entry with behavior, recording
   rules, and (if applicable) a note from the overlay

**Verification**: The degradation rules are clearly documented. No platform
claims capabilities it doesn't have.

## Platform-specific

### Scenario 5 — Claude Code: manual-fallback pauses with one instruction

**Given**: Claude Code adapter with `browser_automation: manual-fallback`.  
**When**: A skill requires browser automation (e.g., verify-release-evidence
wants to check a rendered page).  
**Then**:
1. The adapter pauses the workflow: "Browser automation is manual-fallback
   on Claude Code."
2. The adapter gives exactly ONE concrete instruction:
   "Open http://localhost:3000/login in your browser. Confirm the page renders
   without errors and the login form is visible. Type 'done' when ready."
3. The adapter does NOT claim: "Verification passed" or "Page rendered
   correctly"
4. After the user responds, the adapter appends a History entry:
   - Action: "Manual browser verification"
   - Actor: `human`
   - Note: "Verified by human on Claude Code (browser_automation:
     manual-fallback). Automated verification not performed."

**Verification**: One instruction given. No false verification. History
records the gap.

### Scenario 6 — Claude Code: subagent_isolation manual-fallback

**Given**: Claude Code adapter with `subagent_isolation: manual-fallback`.  
**When**: A skill spawns sub-agents for parallel work (e.g., code-review
spawns Standards and Spec sub-agents).  
**Then**:
1. The adapter notes: "Claude Code sub-agents (Task tool) have different
   isolation guarantees than Codex subagents."
2. For sensitive multi-agent workflows, the adapter asks: "Do you need
   strong isolation guarantees for this parallel work? If yes, consider
   running the sub-tasks sequentially or on Codex."
3. The limitation is documented in the Platform Adapter section
4. The workflow proceeds with the user's choice, recording the decision

**Verification**: Limitation disclosed before proceeding. User choice
recorded.

### Scenario 7 — GitHub Copilot: parallel_tool_execution manual-fallback

**Given**: GitHub Copilot adapter with `parallel_tool_execution:
manual-fallback`.  
**When**: A skill attempts to run multiple independent operations in parallel.  
**Then**:
1. The adapter notes: "GitHub Copilot may serialize some parallel tool
   calls."
2. The adapter does NOT silently serialize — it informs the user that
   parallel execution is degraded
3. The adapter offers: "I'll run these sequentially. Each step will wait
   for the previous to complete. This may be slower but produces the same
   result."
4. If the result depends on parallelism (e.g., timing-sensitive), the
   adapter warns explicitly

**Verification**: Degradation disclosed. User informed before sequential
execution begins.

### Scenario 8 — Unsupported capability stops the path

**Given**: A hypothetical adapter with `structured_output: unsupported`.  
**When**: A skill needs to produce valid YAML frontmatter for a Work Object.  
**Then**:
1. The adapter stops: "`structured_output` is unsupported on this platform.
   Cannot produce schema-valid Work Object frontmatter."
2. The adapter records in the Work Object body: "Platform limitation:
   `structured_output` unsupported. Blocked action: Work Object creation."
3. The adapter routes: "This capability is available on Codex and Claude
   Code. Switch platforms or provide the YAML frontmatter manually."
4. The adapter does NOT produce invalid YAML, skip the requirement, or
   silently substitute

**Verification**: Path stopped. Limitation recorded. Route suggested. No
false output.

### Scenario 9 — No false verification on any platform

**Given**: Any platform adapter with any manual-fallback capability.  
**When**: The capability is required for a verification step.  
**Then**:
1. The adapter NEVER outputs "verified," "confirmed," "passed," or similar
   when the required capability was manual-fallback
2. Instead, it outputs: "Verification requires [capability], which is
   manual-fallback on [platform]. [One manual instruction]."

**Verification**: Grep the generated adapters for patterns like "verified"
or "confirmed" that appear without a preceding capability check. None should
exist for manual-fallback capabilities.

### Scenario 10 — Stricter safety constraint takes precedence

**Given**: Claude Code imposes a stricter constraint than the core (e.g.,
requires explicit confirmation for file writes outside the workspace).  
**When**: A skill attempts an action that triggers the stricter constraint.  
**Then**:
1. The adapter applies the platform rule, not the core rule
2. The divergence is disclosed: "Claude Code requires explicit confirmation
   for writes outside the workspace. This is stricter than the core default."
3. The adapter asks for confirmation before proceeding

**Verification**: Stricter rule applied. Divergence disclosed. Core semantics
not silently changed.

## Cross-platform comparison

### Scenario 11 — Same capability, different classifications

**Given**: The `browser_automation` capability across all three adapters.  
**When**: Compare the Capability Mappings tables.  
**Then**:
1. Codex: `browser_automation` is `manual-fallback`
2. Claude Code: `browser_automation` is `manual-fallback`
3. GitHub Copilot: `browser_automation` is `manual-fallback`
4. Each adapter's degradation behavior is documented in its own Platform
   Adapter section
5. The core decision logic (what browser automation is needed for) is
   identical across all adapters

**Verification**: Same core requirement, platform-specific degradation.
No adapter hides its limitation.

## Pass/Fail Criteria

| # | Scenario | Pass condition |
|---|----------|---------------|
| 1 | Native proceeds normally | No degradation message for native capabilities |
| 2 | Core declares capabilities | Required capabilities section present, abstract, references degradation doc |
| 3 | Adapter documents classifications | All capabilities listed with platform tool and classification |
| 4 | Degradation rules explained | Three rules present, "no false verification" stated |
| 5 | Manual-fallback pauses with one instruction | Exactly one instruction, no false verification, History records gap |
| 6 | Subagent isolation disclosed | Limitation disclosed, user choice recorded |
| 7 | Parallel execution degradation | Degradation disclosed, sequential fallback offered |
| 8 | Unsupported stops the path | Path stopped, limitation recorded, route suggested, no false output |
| 9 | No false verification | Grep confirms no unqualified "verified" for manual-fallback capabilities |
| 10 | Stricter safety wins | Platform rule applied, divergence disclosed |
| 11 | Cross-platform comparison | Same core requirement, different platform degradation, all disclosed |

All scenarios must pass for the fixture to be considered satisfied.
