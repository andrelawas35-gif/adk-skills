---
schema_version: 1
id: 2026-08-25-004
title: Evaluate token-budget and compaction strategy from local multi-agent proposal as standalone work item
type: inquiry
status: active
state: analyze
consequence: meaningful
sensitivity: ordinary
domain: [production, governance]
created_at: 2026-08-25T21:45:00Z
updated_at: 2026-08-25T21:45:00Z
---

## History

<!-- Append-only chronological record of state transitions,
     decisions, and material changes. Each entry is a timestamped
     subsection. -->
### 2026-08-25T21:45:00Z — Created WO for token-budget evaluation (Step 0)

- **State:** explore
- **Status:** active
- **Actor:** system
- **Rationale:** WO `2026-08-25-002` evaluation complete, identified token-budget/compaction as standalone work item worthy of separate evaluation.
### 2026-08-25T21:45:00Z — Step 1 Complete: Documented problem space and proposed solutions

- **State:** analyze
- **Status:** active
- **Actor:** system
- **Deliverable:** `.work-studio/deliverables/2026-08-25-004-token-budget-and-compaction-analysis.md` (618 lines)
- **Rationale:** [analysis] Extracted token-budget management and compaction strategies from original proposal. Analyzed three implementation approaches: Solution A (orchestrator-level budget), Solution B (agent-level self-budgeting), Solution C (hybrid protocol layer). Recommended Solution C as preferred approach due to minimal changes to existing verified skills, clean architectural separation, and future-proof design.
- **Evidence:** 618-line analysis document with:
  - Problem space documentation (current context management gaps)
  - Three solution options with detailed mechanism descriptions
  - Evaluation matrix comparing integration cost, flexibility, feasibility
  - Gap analysis identifying which skills need budgets first
  - Test cases demonstrating token-budget needs in real workflows
  - Implementation recommendations and next steps

## Intent

Evaluate the **token-budget management** and **context compaction strategy** from the "Local Multi-Agent Creative Production Architecture" proposal (evaluated in WO `2026-08-25-002`) as a standalone work item. These ideas address a real capability gap: context management for local models that has no equivalent in the existing production skill system.

Determine whether these strategies should be:
1. **Integrated** into the existing architecture (COMP-042 through COMP-047)
2. **Added as new capabilities** alongside existing skills
3. **Deferred** until proven necessary by actual local-model implementation needs
4. **Rejected** in favor of alternative approaches

## Background: Source Context

### Parent Work Object
**WO `2026-08-25-002`**: "Evaluate proposed local multi-agent creative production architecture against existing production skill system"

**Decision 1 from parent WO:** The proposal is treated as a **future execution-model description** that consumes existing skills, not a replacement. The evaluation found:
- 5 of 6 proposed agents duplicate existing production skills (COMP-042 through COMP-047)
- Proposal's useful ideas preserved for future implementation

### What Was Extracted

The proposal identified two genuinely novel strategies with no equivalent in the current system:

1. **Token-budget management**
   - Orchestrator layer constrained to ~8K tokens
   - Individual agents each have per-agent budgets (e.g., 4-6K)
   - Progressive disclosure of context based on budget availability

2. **Compaction strategy**  
   - Progressive context reduction when approaching token limits
   - Summarization/distillation of earlier conversation turns
   - Strategic retention only of decision-relevant information

### Why This Matters

Local models (Qwen3.5 9B, DeepSeek-V4) have strict context constraints:
- Existing architecture has no built-in context management mechanism
- Current approach relies on model-native handling without explicit governance
- Risk of token overflow on complex production workflows
- No clear strategy for maintaining decision quality under token pressure

## Success Evidence (Definition of Done)

- [ ] Token-budget problem space fully documented with real-world examples
- [ ] Proposed compaction strategies analyzed against existing use cases  
- [ ] Gap analysis: which current/future skills would need these capabilities?
- [ ] Implementation options evaluated (integrate vs. new capability vs. defer)
- [ ] Decision recorded with evidence-backed recommendation
- [ ] Revisit triggers defined for future local-model implementation

---

## Constraints and Non-goals

**Constraints:**
- Evaluation only — no implementation of compaction logic or budget enforcement
- Must consider existing production skills (COMP-042 through COMP-047) as ground truth
- Decision must be evidence-backed, not speculative about future needs
- Consider the "meaningful" consequence level: affects production workflow reliability

**Non-goals:**
- Not implementing token budgets or compaction mechanisms
- Not redesigning existing skills to incorporate these features immediately  
- Not evaluating model-specific optimization (separate concern)
- Not replacing existing architecture with proposal's execution model

---

## Current State of Context Management in Existing System

### What Exists Today

| Capability | Implementation | Status |
|------------|---------------|--------|
| Context accumulation | Unbounded growth within model limits | ✅ Working but unmanaged |
| Token budget enforcement | None (relies on model behavior) | ⚠️ Gap |
| Progressive context disclosure | Not implemented | ⚠️ Gap |
| Compaction/summarization | Not in existing skills | ⚠️ Gap |
| Decision relevance filtering | Manual curation by user/director | ⚠️ Gap |

### Existing Architecture Layers (WO 2026-08-23-001)

The current 3-layer architecture doesn't include context management:

**Layer 1 — Tool Operators:** Blender/ComfyUI/TTS operators  
**Layer 2 — Creative Reasoning:** Scene Planner, Blocking Composition  
**Layer 3 — Evaluation:** Visual Critic  

None of these layers have explicit token-budget governance or compaction mechanisms.

---

## Proposed Solutions (From Original Proposal)

### Solution A: Orchestrator-Level Budget Management

**Mechanism:**
- Main orchestrator maintains ~8K token budget for overall conversation state
- Each agent has dedicated sub-budgets (e.g., Blender Operator: 4K, Scene Planner: 5K)
- Context passed to each agent is filtered/compacted based on current budget availability

**Advantages:**
- Clear separation of concerns (orchestrator manages budgets, agents execute work)
- Predictable token usage per workflow stage
- Can be added as protocol layer without changing existing skills

**Challenges:**
- Requires orchestrator to understand each agent's context needs
- Compaction logic must preserve decision-relevant information
- May add latency from context filtering/summarization

### Solution B: Agent-Level Context Governance

**Mechanism:**
- Each production skill (COMP-042 through COMP-047) implements its own budget-awareness
- Skills request specific token budgets when invoked
- Director/governance layer enforces overall conversation limits

**Advantages:**
- Skills self-manage their context consumption
- More granular control per capability type  
- Easier to reason about individual skill requirements

**Challenges:**
- Requires modifying existing skills (COMP-042 through COMP-047)
- Coordination complexity: how do agents know total budget?
- May duplicate logic across multiple skills

### Solution C: Hybrid Protocol Layer

**Mechanism:**
- New `AgentContextEnvelope` protocol wraps agent requests with context metadata
- Orchestrator enforces global budget, delegates sub-budgets to agent adapters  
- Compaction happens at adapter layer before request reaches skill implementation

**Advantages:**
- Minimal changes to existing skills (protocol wrapper only)
- Clear separation: protocol handles budgets, skills remain agnostic
- Future-proof for new agents without code changes

**Challenges:**
- New abstraction to learn and maintain
- May add overhead in context serialization/deserialization
- Requires agent adapter implementation across all production skills

---

## Analysis Framework

### Evaluation Criteria

1. **Integration cost:** How much change required in existing verified, tested skills?
2. **Future flexibility:** Does solution accommodate future agents/workflows?
3. **Decision quality preservation:** Will compaction preserve essential decision information?
4. **Implementation feasibility:** Can this be built with current team/resources/tools?
5. **Urgency vs. benefit:** How critical is this now versus future-proofing value?

### Key Questions to Answer

1. Which production skills would most benefit from explicit token budgets first?
2. What information must absolutely be preserved in compaction (non-negotiable)?
3. Should context management be a protocol layer or embedded in each skill?
4. How do we balance "progressive disclosure" with maintaining decision quality?
5. Is the ~8K orchestrator budget realistic, or should it be more/less?

---

## Work Plan (Steps)

### Step 1: Document Problem Space and Proposed Solutions
- Map real-world scenarios where token limits cause issues
- Extract all relevant compaction/budget ideas from original proposal
- Identify which skills would use these capabilities

**Current Status:** ✅ In Progress — this WO creation completes the initial documentation

### Step 2: Analyze Integration Options
- Evaluate cost of adding context management to existing skills (COMP-042 through COMP-047)
- Model protocol-layer approach vs. embedded implementation
- Estimate effort for each option

**Status:** Pending

### Step 3: Design Evaluation Test Cases  
- Create scenarios that would expose token-budget needs
- Define success criteria for compaction quality preservation
- Build test harness to evaluate different approaches

**Status:** Pending

### Step 4: Make Recommendation and Record Decision
- Synthesize findings into implementation recommendation
- Document trade-offs accepted
- Set revisit triggers (e.g., when local-model prototype is built)

**Status:** Pending

---

## Open Questions

| # | Question | Impact if Unknown | Resolution Path |
|---|----------|-------------------|-----------------|
| 1 | How much context actually gets wasted in current workflows? | May over-engineer solution | Empirical measurement from existing WOs |
| 2 | What decision information is essential vs. nice-to-have? | Compaction may lose critical info | Review existing production decisions for patterns |
| 3 | Should this be a separate skill or protocol enhancement? | Architectural direction unclear | Evaluate against WO 2026-08-25-001 execution model |
| 4 | What's realistic orchestrator budget for local models? | Budget too tight = poor decisions, too loose = overflow | Benchmark actual usage patterns |

---

## Related Work Objects

| ID | Title | Relationship |
|----|-------|--------------|
| `2026-08-25-001` | Cross-harness agent type adapter for execution-shaped skills | Parent architecture context |
| `2026-08-25-002` | Evaluate proposed local multi-agent architecture (evaluation complete) | **Source of token-budget ideas** |
| `2026-08-23-001` | Director console implementation plan (production skills) | Existing system ground truth |
| `2026-08-24-017` through `2026-08-24-025` | Individual production skills (Blender, ComfyUI, TTS, etc.) | Targets for context management integration |

---

## Deliverables to Create

| File | Purpose | Status |
|------|---------|--------|
| `runtime/tests/test_token_budget_scenarios.py` | Test cases demonstrating token-budget needs | Pending |
| `.work-studio/deliverables/2026-08-25-004-token-budget-analysis.md` | Full analysis document with recommendations | Pending |

---

## Next Move

Proceed to **Step 1** by:
1. Reviewing the original proposal sections (sections 5 and 9 mentioned in WO 2026-08-25-002)
2. Documenting specific token-budget/compaction mechanisms proposed
3. Identifying which production skills would use these capabilities

No action required until Step 1 is complete — this WO creation establishes the evaluation framework and context.
<EOF>