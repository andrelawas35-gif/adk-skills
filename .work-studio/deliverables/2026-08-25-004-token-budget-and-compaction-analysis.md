# Token-Budget and Compaction Strategy Analysis
**Work Object:** `2026-08-25-004`  
**Date:** 2026-08-25T21:45:00Z  
**Status:** Step 1 Complete — Problem Space Documented  

---

## Executive Summary

This document evaluates **token-budget management** and **context compaction strategies** from the "Local Multi-Agent Creative Production Architecture" proposal. These ideas address a real capability gap in the existing production skill system that has no equivalent mechanism for managing local model context constraints.

### Core Finding

The original proposal's execution-model ideas (progressive disclosure, token budgets, local-model orchestration) should be **preserved as future input** to enhance the existing architecture rather than replacing it. These strategies represent a genuine capability gap that affects production workflow reliability under strict token limits.

---

## 1. Problem Space: Why Token Budgets Matter for Local Models

### 1.1 Current State of Context Management

| Capability | Implementation | Status | Risk Level |
|------------|---------------|--------|------------|
| Context accumulation | Unbounded growth within model limits | ✅ Working but unmanaged | 🔴 High (token overflow) |
| Token budget enforcement | None (relies on model behavior) | ⚠️ Gap | 🔴 High (unpredictable usage) |
| Progressive context disclosure | Not implemented | ⚠️ Gap | 🟡 Medium (performance degradation) |
| Compaction/summarization | Not in existing skills | ⚠️ Gap | 🔴 High (decision quality loss) |
| Decision relevance filtering | Manual curation by user/director | ⚠️ Gap | 🟡 Medium (error-prone) |

### 1.2 The Local Model Constraint Reality

**Existing production skills (COMP-042 through COMP-047)** were designed for frontier-model reasoning:
- **Claude/Codex/Copilot**: Context windows of 128K+ tokens, tolerant of accumulation
- **Qwen3.5 9B / DeepSeek-V4**: Strict limits (~8K orchestrator, ~4-6K per agent)

**Real-world scenario demonstrating the gap:**

```
Production workflow example: Shot production (COMP-042 Blender Operator)

Turn 1 (Context: 2K tokens): Director specifies shot requirements  
→ Model generates initial scene spec

Turn 2 (Context: 4K total): Review feedback, minor adjustments needed  
→ Model incorporates changes

Turn 3 (Context: 6.5K total): Technical constraints identified by Blender operator  
→ Model must filter earlier conversation for relevant decisions

Turn 4 (Context: 8.2K - OVER LIMIT): Model truncates or loses critical decision context
→ Decision quality degrades, potentially invalid output
```

**Without explicit token management:** Each turn adds to the context, eventually exceeding model limits and causing unpredictable behavior.

### 1.3 Why This Can't Be Solved by Model Behavior Alone

The proposal correctly identified that relying on "model-native handling" is insufficient because:

1. **No transparency**: User/director cannot see when/how tokens are being used
2. **No control**: Cannot prioritize which information to keep vs. discard  
3. **No predictability**: Token usage varies by content, not just conversation length
4. **No governance**: No mechanism to enforce decision quality under pressure

---

## 2. Proposed Solutions: Extracted from Original Proposal

The original proposal (WO `2026-08-25-002` source) outlined three implementation approaches. Below is the detailed extraction with analysis.

### Solution A: Orchestrator-Level Budget Management

#### Mechanism Design

```
┌─────────────────────────────────────────────────────────────┐
│                    Main Orchestrator Layer                   │
│              Global Token Budget: ~8K tokens                 │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐│
│  │   Agent A        │  │   Agent B        │  │  Agent C    ││
│  │ (Blender Op)     │  │ (Scene Planner)  │  │  Critic     ││
│  │ Budget: 4K       │  │ Budget: 5K       │  │ Budget: 3K  ││
│  └──────────────────┘  └──────────────────┘  └─────────────┘│
└─────────────────────────────────────────────────────────────┘

Context flow:
1. Director message → Orchestrator filters/compacts based on global budget
2. Filtered context passed to Agent A with remaining budget
3. Agent A response consumes part of its 4K budget  
4. Remaining budget tracked for next agent's turn
```

#### Key Features

- **Global orchestrator constraint**: ~8K tokens for overall conversation state
- **Per-agent sub-budgets**: Blender Operator: 4K, Scene Planner: 5K, Visual Critic: 3K
- **Progressive disclosure**: Context passed to each agent filtered based on current budget availability
- **Budget tracking**: Orchestrator maintains running total of tokens consumed

#### Advantages

1. ✅ Clear separation of concerns (orchestrator manages budgets, agents execute)
2. ✅ Predictable token usage per workflow stage
3. ✅ Can be added as protocol layer without changing existing skills
4. ✅ Scales to unlimited number of agents with same mechanism

#### Disadvantages/Challenges

1. ⚠️ Requires orchestrator to understand each agent's context needs upfront
2. ⚠️ Compaction logic must preserve decision-relevant information (complex)
3. ⚠️ May add latency from context filtering/summarization operations
4. ⚠️ "Under 8K" budget may be tight for complex multi-turn workflows

#### Implementation Complexity: **Medium-High**

Requires:
- Orchestrator to parse incoming requests and identify agent types
- Compaction algorithm that understands production workflow semantics
- Budget tracking across multiple agents/turns
- Fallback mechanism when budget constraints prevent full context delivery

---

### Solution B: Agent-Level Context Governance

#### Mechanism Design

```
┌─────────────────────────────────────────────────────────────┐
│                    Director / Governance Layer               │
│              Enforces global conversation limit (e.g., 20K)  │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐│
│  │   Agent A        │  │   Agent B        │  │  Agent C    ││
│  │ (Blender Op)     │  │ (Scene Planner)  │  │  Critic     ││
│  │ Self-budgeting:  │  │ Self-budgeting:  │  │ Self-       ││
│  │ Requests budget  │  │ Requests budget  │  │ budgeting   ││
│  │ when invoked     │  │ when invoked     │  │ when        ││
│  └──────────────────┘  └──────────────────┘  └─────────────┘│
│         4K              5K               3K                  │
└─────────────────────────────────────────────────────────────┘

Each skill implements its own context-awareness:
- Knows maximum tokens it can consume
- Requests specific budget when invoked  
- Truncates/compacts internally if exceeded
```

#### Key Features

- **Self-budgeting skills**: Each production skill (COMP-042 through COMP-047) manages its own token usage
- **Budget requests**: Skills declare their requirements when invoked
- **Internal compaction**: Skills handle context reduction themselves
- **Governance enforcement**: Director layer enforces overall conversation limits

#### Advantages

1. ✅ Skills self-manage their context consumption (no external orchestration needed)
2. ✅ More granular control per capability type  
3. ✅ Easier to reason about individual skill requirements
4. ✅ Can be implemented incrementally, one skill at a time

#### Disadvantages/Challenges

1. ⚠️ Requires modifying existing skills (COMP-042 through COMP-047) — higher risk
2. ⚠️ Coordination complexity: how do agents know total budget available?
3. ⚠️ May duplicate logic across multiple skills
4. ⚠️ Risk of inconsistent compaction strategies across different skills

#### Implementation Complexity: **High (for existing skills)**

Requires changes to:
- `runtime/orchestrator.py` — Budget tracking and enforcement
- COMP-042 Blender Operator — Context awareness and internal compaction  
- COMP-045 Scene Planner — Context-aware decision making
- COMP-047 Visual Critic — Feedback generation under constraints
- All other production skills

---

### Solution C: Hybrid Protocol Layer (RECOMMENDED)

#### Mechanism Design

```
┌─────────────────────────────────────────────────────────────┐
│              AgentContextEnvelope Protocol                  │
│  Wraps agent requests with context metadata                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐      ┌──────────────┐     ┌──────────┐       │
│  │Request   │      │Context Filter│     │Response  │       │
│  │Envelopes │──>──▶│& Compactor   │<───▶│Envelope  │       │
│  │Metadata: │      │(Orchestrator)│     │          │       │
│  │• Agent   │      │              │     │          │       │
│  │  type    │      │              │     │          │       │
│  │  budget  │      │              │     │          │       │
│  │  priority│      │              │     │          │       │
│  └──────────┘      └──────────────┘     └──────────┘       │
│                                                             │
│  Protocol layer sits between existing skills and           │
│  execution, adding context management without modifying    │
│  skill implementations                                      │
└─────────────────────────────────────────────────────────────┘
```

#### Key Features

- **New `AgentContextEnvelope` protocol**: Wraps agent requests with context metadata
- **Orchestrator enforces global budget**, delegates sub-budgets to adapter layer  
- **Compaction happens at adapter layer** before request reaches skill implementation
- **Protocol wrapper approach**: Minimal changes to existing skills (protocol wrapper only)

#### Implementation Details

```python
# Example: AgentContextEnvelope structure
class AgentContextEnvelope:
    """Wraps agent requests with context management metadata"""
    
    def __init__(self, 
                 agent_id: str,           # "blender_operator", "scene_planner"
                 max_tokens: int,         # Total conversation limit (e.g., 20K)
                 agent_budget: int,       # Per-agent budget (e.g., 4K for Blender)
                 remaining_context: list, # Current context tokens available
                 priority: str = "normal",# "high" | "medium" | "low"
                 decision_critical: set = None)  # Token IDs that must be preserved
    
    def filter_context(self):
        """Return only decision-relevant context within budget"""
        pass

class AgentContextAdapter:
    """Protocol adapter implementing context management"""
    
    def adapt_request(self, request: AgentRequest) -> AgentResult:
        # 1. Check global budget constraint
        if self.global_tokens_used + len(request.context) > MAX_TOKENS:
            raise ContextExceededError()
        
        # 2. Filter agent-specific context based on remaining budget  
        filtered_context = filter_by_budget(
            request.context, 
            self.agent_budget,
            preserve_decisions=self.decision_critical_ids
        )
        
        # 3. Wrap with envelope metadata
        return AgentContextEnvelope(request=filtered_context)
```

#### Key Protocol Fields

| Field | Purpose | Example Value |
|-------|---------|---------------|
| `agent_id` | Identifies which agent is being invoked | `"blender_operator"`, `"scene_planner"` |
| `max_tokens` | Total conversation limit for this session | `20000` |
| `agent_budget` | Per-agent context budget | `4096` (Blender), `5120` (Scene Planner) |
| `remaining_context` | Current available context tokens | List of token IDs or content |
| `priority` | Request urgency level | `"high"`, `"medium"`, `"low"` |
| `decision_critical` | Token IDs that must be preserved | `[142, 891, 1503]` (decision points) |

#### Advantages

1. ✅ Minimal changes to existing skills (protocol wrapper only)  
2. ✅ Clear separation: protocol handles budgets, skills remain agnostic
3. ✅ Future-proof for new agents without code changes
4. ✅ Protocol can evolve independently of skill implementations
5. ✅ Testable and observable through protocol layer

#### Disadvantages/Challenges

1. ⚠️ New abstraction to learn and maintain (protocol knowledge required)  
2. ⚠️ May add overhead in context serialization/deserialization  
3. ⚠️ Requires agent adapter implementation across all production skills
4. ⚠️ Initial development effort before benefits are realized

#### Implementation Complexity: **Medium**

Requires:
- Protocol definition and documentation (`AgentContextEnvelope`)
- Adapter layer implementation (wraps existing skills)  
- Orchestrator updates for budget tracking
- Test suite for protocol behavior
- **No modifications to existing skill implementations** (COMP-042 through COMP-047)

---

## 3. Analysis: Which Solution Should Be Chosen?

### Evaluation Criteria Matrix

| Criterion | Solution A (Orchestrator-Level) | Solution B (Agent-Level) | Solution C (Hybrid Protocol) |
|-----------|----------------------------------|--------------------------|------------------------------|
| **Integration cost** (to existing skills) | ✅ Low (no skill changes needed) | 🔴 High (modify COMP-042 through COMP-047) | ✅ Medium (protocol wrapper only) |
| **Future flexibility** (new agents/workflows) | ✅ Good (orchestrator manages all) | 🟡 Variable (depends on each skill's implementation) | ✅ Excellent (protocol handles any agent type) |
| **Decision quality preservation** | ⚠️ Medium (compaction logic complexity unknown) | 🟡 Medium (varies by skill implementation) | ✅ Good (explicit decision-critical field) |
| **Implementation feasibility** (current team/resources) | ✅ High (orchestrator already exists) | 🔴 Low (requires skill modifications) | ✅ High (protocol approach is cleanest) |
| **Urgency vs. benefit** | 🟡 Medium-term benefit | 🔴 Long-term only | ✅ Near-term achievable, scalable future |

### Recommendation: Solution C (Hybrid Protocol Layer)

**Rationale:**
1. **Preserves existing verified work**: No modifications to COMP-042 through COMP-047 needed
2. **Clean architectural separation**: Protocol layer handles context management; skills focus on creative production
3. **Future-proof design**: New agents can use protocol without code changes
4. **Testable and observable**: Protocol behavior is explicit, not hidden in skill implementations
5. **Balanced complexity**: Medium implementation effort with maximum future benefit

**Trade-offs accepted:**
- Initial development of protocol layer before benefits are realized (acceptable given long-term value)
- Some context serialization overhead (minimal compared to token overflow risk)

---

## 4. Implementation Options for Protocol Layer

### Option C1: Full Context Wrapping (Recommended)

```python
# Complete envelope with all metadata
class AgentContextEnvelope:
    agent_id = "blender_operator"
    max_tokens = 20000
    agent_budget = 4096
    remaining_context = [token_1, token_50, token_892, ...]
    priority = "normal"
    decision_critical = {142, 891, 1503}  # Decision point tokens
    
# Adapter processes full envelope, compacts as needed
```

**Pros:** Maximum control and observability  
**Cons:** Most verbose, requires context serialization overhead

### Option C2: Lightweight Budget Declaration

```python
# Minimal metadata, assumes standard compaction behavior
class AgentContextEnvelope:
    agent_id = "blender_operator"
    budget_limit = 4096
    
# Adapter applies default compaction algorithm  
# (e.g., preserve most recent context + decision markers)
```

**Pros:** Simpler implementation, less overhead  
**Cons:** Less control over what gets preserved

### Option C3: Priority-Based Context Selection

```python
class AgentContextEnvelope:
    agent_id = "blender_operator"  
    priority = ["high", "normal", "low"]  # Tiered context importance
    
# Adapter prioritizes high-priority context, compacts low-priority first
```

**Pros:** Explicit control over what matters most  
**Cons:** Requires user/director to assign priorities correctly

---

## 5. Gap Analysis: Which Skills Need Context Management?

### Immediate Priority (High Token Usage)

| Skill | Current Token Risk | Why It Needs Budgets |
|-------|-------------------|---------------------|
| **COMP-042 Blender Operator** 🔴 | High | Multi-turn technical workflows, complex scene specifications |
| **COMP-045 Scene Planner** 🟡 | Medium-High | Iterative refinement of scene specs based on feedback |
| **COMP-047 Visual Critic** 🟡 | Medium | Vision model feedback can grow quickly across multiple shots |

### Future Needs (Emerging Use Cases)

| Skill | Token Risk Level | Rationale |
|-------|------------------|-----------|
| COMP-046 Blocking Composition | Medium | Camera mathematics + creative decisions accumulate |
| COMP-021 Screenplay Pipeline | High | Long-form content generation with extensive context |
| NEW Animation Agent* | 🔴 Critical | No existing skill equivalent; character motion/timing needs explicit budgets |

\* **Animation capability gap**: WO 2026-08-25-002 noted the original proposal's "Animation Agent" (8-12K token context) has no direct equivalent. If animation work proceeds, this is new capability to design with built-in budget management.

---

## 6. Evaluation Test Cases: Demonstrating Token-Budget Needs

### Test Case 1: Blender Operator Multi-Turn Workflow

**Setup:**
```yaml
Workflow: Shot refinement via Blender operator
Turns expected: 5-8 technical refinement iterations  
Context growth per turn: ~1K tokens (feedback + model response)
Total without management: ~7K+ tokens
Token limit: 6.5K for this agent type
```

**Expected failure without budget enforcement:**
- Turn 4-5: Context exceeds agent's 4K budget
- Model truncates earlier context, loses initial shot requirements  
- Output drifts from original direction (invalidates production decision)

### Test Case 2: Scene Planner Iterative Refinement

**Setup:**
```yaml
Workflow: Multi-shot scene specification refinement  
Feedback loops: Director provides feedback on each iteration
Context accumulation: Each response adds ~800 tokens to conversation
Budget needed per iteration: ~5K (Scene Planner's complex reasoning)
```

**Expected failure without progressive disclosure:**
- By turn 4, context exceeds available budget
- Scene planner loses earlier camera/mathematical constraints  
- Generated specs drift from original directorial intent

### Test Case 3: Visual Critic Feedback Escalation

**Setup:**
```yaml
Workflow: Iterative visual feedback across multiple shots  
Critic responses: Can be detailed (200+ tokens each)
Escalation pattern: Small issues → major revisions needed
Budget consumption: ~3K per shot, 5+ shots in sequence = 15K+ total
```

**Expected failure without compaction:**
- Critic feedback becomes truncated or lost  
- Production team lacks visibility into decision rationale  
- Revision cycles become unpredictable and unreliable

---

## 7. Decision Criteria for Moving Forward

### Thresholds for Implementation Priority

| Metric | Current State | Required for Local Models | Gap Severity |
|--------|--------------|--------------------------|--------------|
| **Orchestrator token limit** | None (unbounded) | ~8K tokens maximum | 🔴 Critical |
| **Per-agent budget awareness** | Unknown | Explicit per-skill budgets | 🟡 High |
| **Progressive context disclosure** | Not implemented | Required for multi-turn workflows | 🔴 Critical |
| **Compaction with decision preservation** | Manual curation only | Automated, quality-preserving compaction | 🔴 Critical |

### When to Implement (Decision Triggers)

1. **Implement immediately if:**
   - Local-model prototype is actively being built and tested
   - Current token usage patterns show approaching limits in real workflows
   - Decision quality degradation observed under current unmanaged approach

2. **Defer to future implementation wave if:**
   - Existing skills still function acceptably with frontier models (128K+ context)
   - No immediate local-model deployment planned  
   - Team resources fully allocated to other priorities

3. **Revisit decision when:**
   - First production workflow shows token overflow symptoms
   - Local model benchmarking indicates need for explicit budget management
   - Animation capability (COMP-048 equivalent) begins design phase

---

## 8. Work Plan and Next Steps

### Step 2: Analyze Integration Options ⏳ PENDING

**Tasks:**
1. Evaluate cost of adding context management to existing skills (COMP-042 through COMP-047)
   - Code review of current implementations
   - Estimate lines of code needed for budget awareness
   - Identify risk areas in verified, tested skills
   
2. Model protocol-layer approach vs. embedded implementation  
   - Protocol definition effort estimation
   - Adapter layer complexity assessment
   - Test suite development requirements

3. Compare against WO 2026-08-25-001 execution model
   - Ensure compatibility with cross-harness agent adapter work
   - Confirm protocol approach fits existing architecture

### Step 3: Design Evaluation Test Cases ⏳ PENDING

**Tasks:**
1. Create scenarios that would expose token-budget needs  
   - Multi-turn Blender operator workflows (Test Case 1)
   - Scene planner iterative refinement chains (Test Case 2)
   - Visual critic feedback escalation patterns (Test Case 3)

2. Define success criteria for compaction quality preservation  
   - Decision critical tokens must remain intact
   - Context summary preserves essential constraints
   - No loss of production-relevant information

3. Build test harness to evaluate different approaches  
   - Protocol layer implementation and testing
   - Comparison against baseline (no budget management)

### Step 4: Make Recommendation and Record Decision ⏳ PENDING

**Tasks:**
1. Synthesize findings into implementation recommendation  
   - Preferred solution (likely Solution C: Hybrid Protocol Layer)
   - Implementation timeline and milestones
   - Risk assessment and mitigation strategies

2. Document trade-offs accepted  
   - What we're choosing vs. what we're deferring
   - Known limitations and workarounds

3. Set revisit triggers for future local-model implementation  
   - Decision to re-evaluate when specific conditions met
   - Metrics that would indicate need for immediate action

---

## 9. Related Work Objects and Dependencies

### Direct Parent Context
- **WO `2026-08-25-002`**: "Evaluate proposed local multi-agent architecture" (evaluation complete)  
  → Source of token-budget ideas, decision to create separate WO

### Architecture Foundation
- **WO `2026-08-25-001`**: "Cross-harness agent type adapter for execution-shaped skills"  
  → Protocol layer must integrate with this cross-domain adapter work

### Target Skills (No modifications needed in initial implementation)
| Skill | WO ID | Status | Context Management Need |
|-------|-------|--------|-------------------------|
| Blender Operator | COMP-042 | verify, live smoke test passed | 🔴 High priority |
| Scene Planner | COMP-045 | design | 🟡 Medium-high |
| Blocking Composition | COMP-046 | design | 🟡 Medium |
| Visual Critic | COMP-047 | design | 🟡 Medium |

### Future Work Dependencies
- **Animation capability gap**: WO 2026-08-25-002 noted "Animation Agent" has no existing equivalent  
  → If animation work proceeds, design should incorporate built-in budget management from this protocol layer

---

## 10. Summary and Recommendation

### Core Conclusion

**Token-budget and compaction strategies represent a genuine capability gap** that must be addressed for reliable local-model production workflows. The original proposal's ideas (progressive disclosure, token budgets, local-model orchestration) should **not be lost**.

### Recommended Approach

**Solution C: Hybrid Protocol Layer**
- **Why:** Minimal changes to existing verified skills, clean architectural separation, future-proof design
- **Implementation effort:** Medium — protocol definition + adapter layer development
- **Timeline:** Can be developed alongside other production skill enhancements  
- **Risk:** Low — no modifications to tested, deployed skills

### Immediate Next Step

**Proceed to Step 2: Analyze Integration Options**
1. Code review of existing production skills for budget-awareness requirements
2. Protocol layer design and effort estimation
3. Compatibility check with WO 2026-08-25-001 cross-harness adapter work

### Revisit Triggers

This decision should be revisited when:
- Local-model prototype is built and actively tested (budget needs empirically verified)
- First production workflow shows token overflow symptoms  
- Animation capability design begins (new skill with inherent budget requirements)
- Token usage metrics indicate approaching model limits in current workflows

---

## Appendix A: Original Proposal Sections Referenced

### Section 5: Token-Budget Management
**Extracted concepts:**
- Orchestrator layer constrained to ~8K tokens for overall conversation state
- Individual agents each have dedicated sub-budgets (4-6K range)
- Progressive disclosure of context based on budget availability

### Section 9: Compaction Strategy  
**Extracted concepts:**
- Progressive context reduction when approaching token limits
- Summarization/distillation of earlier conversation turns
- Strategic retention only of decision-relevant information
- No equivalent in existing architecture (manual curation only)

---

## Appendix B: Token Budget Guidelines for Local Models

### Recommended Budgets by Agent Type

| Agent Type | Context Window Size | Use Case | Rationale |
|------------|---------------------|----------|-----------|
| Orchestrator | ~8K tokens | Overall conversation state, coordination | High-level decisions need broad context but not full detail |
| Blender Operator | 4-6K tokens | Technical scene specification, multi-turn refinement | Complex technical workflows need moderate context depth |
| Scene Planner | 5-7K tokens | Camera mathematics + creative staging decisions | Iterative refinement requires preserving earlier constraints |
| Visual Critic | 3-5K tokens | Vision model feedback per shot | Detailed feedback but can be focused on current decision point |
| Animation Agent* (future) | 8-12K tokens | Character motion, timing, action blocking | Complex temporal reasoning needs larger context window |

\* Based on original proposal's "Animation Agent" specification; no existing equivalent in current system

### Budget Enforcement Guidelines

**Global limits:** Never exceed model's maximum context window  
**Per-agent budgets:** Set to 75-80% of available window (leave headroom for overhead)  
**Progressive disclosure:** Compaction preserves most recent + decision-critical tokens first  
**Emergency handling:** When budget exceeded, prioritize high-priority requests over low-priority

---

<EOF>