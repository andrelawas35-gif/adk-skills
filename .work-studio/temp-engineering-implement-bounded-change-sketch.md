# alawas-engineering-implement-bounded-change

## Governing principle

This skill implements bounded change tracers — small, reversible work units scoped by a Work Object's existing decision record. It handles both design (specifying solutions to open questions) and implementation (code changes) within the WO's authority boundaries. For this invocation, it continues Step 4 of WO `2026-08-25-003`: consequence integration testing and remaining open questions 7-9.

## Personal working lens

The skill works in two modes:
1. **Design mode:** When facing an open question or design gap, specify a concrete solution with evidence, trade-offs, and implementation notes — then wait for confirmation before implementing.
2. **Implementation mode:** When given explicit direction to implement, make bounded changes to the codebase (typically < 300 lines), verify against existing tests, and report the change set.

For this Step 4 work:
- OQ 7-9 require design-first approach (no canonical solution exists yet)
- Consequence integration testing can be implemented directly with test cases defined by the WO's existing tracer bullet

## Boundaries and non-goals

**This skill does:**
- Design concrete solutions for open questions 7-9 from WO `2026-08-25-003`
- Implement consequence integration testing harness (test suite + assertions)
- Update `runtime/orchestrator.py` with priority ordering and compound request handling
- Resolve skill-invoking-skill nesting question via bounded change pattern or platform adapter mechanism

**This skill does NOT:**
- Change the WO's canonical decisions 1-6 without explicit director authorization (these are settled)
- Implement autonomous agent hierarchy, scoring/AI-routing, or full multi-agent proposal (explicitly rejected in earlier WOs)
- Deploy to production environments (bounded changes stay in dev/test)
- Make high-consequence authority calls beyond what the WO's `consequence: meaningful` field permits

## Inputs and preconditions

**Required input:** 
- Work Object context (`2026-08-25-003`) with settled decisions 1-6
- Step 4 scope defined (consequence testing + OQs 7-9)

**Preconditions:**
- `runtime/orchestrator.py` exists with tracer bullet implementation (Decisions 5, verified)
- `skills/core/orchestrate/SKILL.md` exists and tested across domains
- Test framework available (`tests/test_orchestrator_routing.py`)

## Required capabilities

- `file_read` — read WO frontmatter, existing code in `runtime/orchestrator.py`, test files
- `structured_output` — report design proposals with clear implementation steps
- `code_edit` — make bounded changes to Python files within the runtime package
- `test_execution` — run unit tests for verification

## Consequence and authority rules

Per WO `2026-08-25-003`:
- **Consequence:** meaningful (not high) — bounded changes are reversible via git, no production deployment required
- **Authority gates:** 
  - Decision modifications require explicit director confirmation
  - New authority patterns for skill-invoking-skill nesting must be specified before implementation
  - Testing can proceed without elevated authority (bounded changes)

## Workflow

1. **Read WO context** — re-read `2026-08-25-003` frontmatter and history to confirm current state
2. **For each open question:**
   - Read existing code (`runtime/orchestrator.py`) to understand current limitations
   - Propose concrete solution design with evidence (examples, trade-offs)
   - Wait for user confirmation before implementing
3. **After OQs 7-9 are designed:**
   - Implement consequence integration testing harness first (lowest risk, provides test cases)
   - Update `runtime/orchestrator.py` with priority ordering rules and compound request handling
   - Resolve skill-invoking-skill question via chosen pattern
4. **Verify** — run existing test suite (`tests/test_orchestrator_routing.py`) + new tests
5. **Report** — summarize changes made, files modified, and any remaining work

## Open questions from WO 2026-08-25-003 (to be resolved)

### OQ 7: Multi-domain compound requests handling

**Problem:** A request like "create a Work Object for shot 14 and render a preview" spans governance + production domains. Current deterministic matcher picks the first signal, but real users may expect different behavior.

**Proposed solution options (design to select):**
- **Option A — Sequential dispatch:** Route each domain component separately in sequence (WO creation → governance conductor → production renderer). User receives two discrete responses/actions.
  - *Pros:* Simple to implement, preserves existing components' integrity
  - *Cons:* May feel disjointed if user expects single response
  
- **Option B — Request splitting with confirmation:** Detect compound signals, ask user which domain they want to prioritize or split into separate requests.
  - *Pros:* User controls sequencing, avoids unintended side effects  
  - *Cons:* Adds friction (confirmation step), may not match user intent if they expect auto-splitting
  
- **Option C — Dominant domain detection:** Use WO reference as dominant signal (if present) to set overall consequence level and authority gate; route secondary domains but warn about mixed consequences.
  - *Pros:* Consistent consequence handling, clear priority rules
  - *Cons:* May miss cases where user wants both domains treated equally
  
- **Option D — Reject with clarification:** For truly compound requests (no single WO reference), ask caller to split or specify primary domain.
  - *Pros:* Avoids ambiguity, clean boundaries
  - *Cons:* High friction for legitimate multi-domain workflows

**Recommendation:** Start with **Option C** as the core behavior (WO ID dominates for consequence/authority) with an optional "split" mode that can be toggled. This matches how WOs already carry their own domain/consequence fields.

### OQ 8: Deterministic matcher priority order for mixed-signal requests

**Problem:** A request like "update the Work Object for the lighting setup" carries both governance (WO ID) and production (lighting keyword) signals. Current implementation needs explicit priority rules.

**Proposed priority order (design to select):**
1. **Work Object ID reference** — extracts domain/consequence from referenced WO frontmatter (highest priority)
   - *Rationale:* WO is the canonical authority source; lifecycle operations on any domain go through the conductor anyway
   
2. **Explicit skill name mention** — e.g., "run alawas-production-operate-blender"
   - *Rationale:* Skill names encode their own domain prefix, unambiguous signal
   
3. **COMP reference (COMP-042 through COMP-047)** → maps to production/production-plan-scene
   - *Rationale:* Production components are explicitly named artifacts
   
4. **Domain-specific keywords** — "render," "implement," "pricing," "design tokens," etc.
   - *Rationale:* Natural language signal, weaker than explicit identifiers
   
5. **No signal** → triggers LLM fallback

**Edge cases to handle:**
- WO ID present but operation doesn't match WO's domain (e.g., transition governance WO to production skill) → Route to WO's governing component regardless of content (lifecycle operations always go through conductor)
- Multiple WOs referenced → Use most recent by timestamp, or ask for clarification

### OQ 9: Skill-invoking-skill nesting at platform adapter level

**Problem:** The orchestrator may route to another skill (`/orchestrate` calls `alawas-production-operate-blender`). How does the platform handle this without creating infinite loops?

**Proposed solution options (design to select):**
- **Option A — Direct invocation with guardrails:** Platform adapter supports nested skill calls. Implement recursion limit (max 3 levels), cycle detection via call stack logging.
  - *Pros:* Simple, preserves existing skill architecture
  - *Cons:* Requires platform support changes
  
- **Option B — Return routing instruction instead of invoking:** Orchestrator returns a `RoutingDecision` object with target skill name; platform adapter (which knows the full context) decides whether to invoke directly or continue orchestration.
  - *Pros:* No recursion, platform controls execution flow
  - *Cons:* Requires platform-level changes to accept routed decisions
  
- **Option C — Handoff envelope pattern:** Orchestrator wraps request in `HandoffEnvelope` with target skill; platform deserializes and invokes as a "sub-request" within the same session context.
  - *Pros:* Clean encapsulation, reuses existing handoff infrastructure (if exists)
  - *Cons: Requires designing new envelope structure

**Recommendation:** Start with **Option B** for the tracer bullet — return `RoutingDecision` objects instead of invoking directly. This avoids recursion entirely and keeps the orchestrator as a pure classifier/delegator. The platform adapter can then decide whether to execute directly or pass through another orchestrator call if needed (e.g., "route this request to production, but first check if it's already in a multi-domain queue").

## Design proposals for Step 4 implementation

### Proposal 1: Consequence integration testing harness

**What:** Create test suite that verifies consequence gates fire correctly when:
- WO reference suggests `low` consequence but operation is GPU-intensive (should still allow, GPU claim happens at operator level)
- WO reference suggests `meaningful` but routed skill has its own high-consequence gate
- Multiple WOs with different consequences referenced in same request

**Files to create:**
```
tests/test_orchestrator_consequences.py
  - Test case: WO-reference-with-low-consequence-routes-to-production-renderer
  - Test case: Mixed-WO-consequences-in-single-request (WO1=low, WO2=high) → highest dominates? or reject?
  - Test case: Operation-level consequence gates still fire even if orchestrator says "low"
```

**Expected outcome:** Confirms that the "default low for WO-less requests" behavior is safe because downstream components enforce their own gates.

### Proposal 2: Priority ordering implementation in runtime/orchestrator.py

**Current code pattern (from tracer bullet):**
```python
def route_request(request_text):
    # Extract signals, return RoutingDecision
    ...
```

**Proposed change — explicit priority function:**
```python
def extract_signal_priority(request_text) -> list[Signal]:
    """Return signals in order of extraction priority."""
    signals = []
    
    # 1. WO ID (highest priority)
    wo_match = re.search(r'WO\s+20\d{6}-\d{4}-\d{3}', request_text, re.IGNORECASE)
    if wo_match:
        signals.append(Signal(type='wo_id', text=wo_match.group()))
    
    # 2. Explicit skill name
    skill_patterns = [f'/alawas-{s.split("/")[-1]}' for s in ALL_SKILLS]
    for pattern in skill_patterns:
        if re.search(re.escape(pattern), request_text, re.IGNORECASE):
            signals.append(Signal(type='skill_name', text=pattern))
    
    # 3. COMP references (COMP-042 through COMP-047)
    comp_matches = re.findall(r'COMP-\d{3}', request_text)
    for match in comp_matches:
        if 42 <= int(match.split('-')[1]) <= 47:
            signals.append(Signal(type='comp_reference', text=match))
    
    # 4. Domain keywords (lower priority, last)
    domain_keywords = {
        'production': ['render', 'shot', 'scene', 'comfyui', 'blender'],
        'governance': ['work object', 'transition', 'status', 'conduct'],
        ...
    }
    for domain, keywords in domain_keywords.items():
        for kw in keywords:
            if re.search(re.escape(kw), request_text):
                signals.append(Signal(type='domain_keyword', text=kw, domain=domain))
    
    return signals  # Sorted by type priority above
```

**Files to modify:**
- `runtime/orchestrator.py` — add explicit signal extraction with priority ordering

### Proposal 3: Compound request handling (Option C — dominant WO ID)

**Design spec for runtime/orchestrator.py:**
```python
def route_request(request_text):
    signals = extract_signal_priority(request_text)
    
    # Check for compound signals (multiple distinct domains)
    if len(signals) > 1:
        domain_set = {s.domain for s in signals}
        if len(domain_set) > 1 and 'wo_id' not in [s.type for s in signals]:
            # No WO ID to dominate → ask user to clarify or split
            return RoutingDecision(
                needs_llm_fallback=True,
                reason='compound_request_no_dominant_signal',
                suggested_action='split_into_separate_requests_or_specify_primary_domain'
            )
    
    # With WO ID present, extract all domains but use first signal's consequence for gating
    if signals and 'wo_id' in [s.type for s in signals]:
        wo_signals = [s for s in signals if s.type == 'wo_id']
        wo_text = wo_signals[0].text
        
        # Read WO frontmatter to get domain/consequence
        wo_data = load_wo_frontmatter(wo_text)
        
        return RoutingDecision(
            domain=[wo_data['domain']],  # Use referenced WO's domain
            consequence=wo_data.get('consequence', 'low'),
            skill=None,  # Let downstream component decide specific operation
            note='compound_request_handled_via_wo_reference'
        )
    
    # Fall through to existing logic for single-domain requests
    ...
```

**Files to modify:**
- `runtime/orchestrator.py` — add compound request detection and WO-dominant routing
- `tests/test_orchestrator_compound_requests.py` (new) — test cases for multi-domain scenarios

### Proposal 4: Skill-invoking-skill via RoutingDecision return pattern (Option B)

**Design spec:**
Instead of invoking skills directly, the orchestrator returns a `RoutingDecision` with fields like:
```python
class RoutingDecision(BaseModel):
    domain: list[str] | None = None
    consequence: str | None = None
    skill: str | None = None  # Full path to target skill (e.g., "production-operate-blender")
    needs_llm_fallback: bool = False
    
    # New fields for Step 4:
    compound_request_handled: bool = False  # If True, compound request was processed via WO ID dominance
    routing_note: str | None = None  # Human-readable explanation of routing choice
    split_suggestion: list[str] | None = None  # For compound requests without dominant signal, suggest splits
```

**Platform adapter changes needed:**
When orchestrator returns a `RoutingDecision` with `skill` set:
1. Check if target skill is already in the current invocation chain (cycle detection)
2. If valid, either:
   - Invoke directly if platform supports nested skill calls, OR
   - Pass through to next layer of dispatch (e.g., another orchestrator call for multi-domain handling)

**For Step 4 tracer bullet:** Implement the return pattern only; assume platform adapter will handle direct invocation as a separate step. This avoids recursion issues while still providing delegated routing.

**Files to modify:**
- `runtime/orchestrator.py` — update `RoutingDecision` model with new fields, change from invoke-return to return-only pattern
- `tests/test_orchestrator_routing.py` — add test cases for compound requests and routing decision structure

## Implementation sequence (recommended)

### Step 4.1: Consequence integration testing (lowest risk, provides concrete test cases)
- Create `tests/test_orchestrator_consequences.py` with 3 test cases
- Verify existing behavior matches expected gates
- This validates that "default low for WO-less requests" is safe

### Step 4.2: Priority ordering in deterministic matcher
- Update `runtime/orchestrator.py` signal extraction to explicit priority order (WO ID > skill name > COMP > keywords)
- Add tests verifying mixed-signal routing goes to correct component

### Step 4.3: Compound request handling (Option C — WO dominance)
- Implement compound detection and WO-dominant routing in orchestrator
- Add test cases for multi-domain scenarios
- This resolves OQ 7 and partially addresses OQ 8

### Step 4.4: RoutingDecision return pattern (resolves OQ 9)
- Update `RoutingDecision` model with new fields
- Remove direct skill invocation, replace with return-only pattern
- Platform adapter handles invocation as separate step
- Add cycle detection logic in tests/documentation

## Exit criteria for Step 4

All of the following must be true:
1. Consequence integration test suite passes (3+ test cases covering mixed scenarios)
2. Deterministic matcher handles priority ordering correctly (verified against all 6 tracer cases + compound requests)
3. Compound request handling implemented with WO ID as dominant signal when present
4. RoutingDecision return pattern implemented (no direct skill invocation)
5. All existing tests pass (zero regressions from tracer bullet)

## Verification commands (after each step)

```bash
# Run all orchestrator-related tests
uv run --python 3.11 python -m unittest runtime.tests.test_orchestrator_routing -v
uv run --python 3.11 python -m unittest runtime.tests.test_orchestrator_consequences -v
uv run --python 3.11 python -m pytest tests/ -k orchestrator -v

# Run full runtime test suite (sanity check)
uv run --python 3.11 python -m unittest discover -s runtime/tests -v
```

## Escalation path

If any of the following occur, route back to `governance-conduct-work-object` for WO state update:
- Consequence gates fail unexpectedly (security/regression risk)
- Compound request logic introduces ambiguity or errors in routing
- Platform adapter changes required exceed bounded change scope (need separate decision)
- Testing reveals fundamental design flaws requiring re-architecture

---

## Current invocation context

**Work Object:** `2026-08-25-003`  
**Status:** verify → continuing to implement Step 4  
**Consequence:** meaningful  
**Domains:** engineering, governance, production (mixed)  

**Tasks assigned in this invocation:**
1. Design and test consequence integration scenarios
2. Implement priority ordering for OQ 8
3. Design solution for OQ 7 (compound requests) — recommend Option C (WO dominance)
4. Implement return-only RoutingDecision pattern for OQ 9

---

## Action requested from director

Proceed with Step 4 implementation as outlined above, or:
- Select alternative design options for any open question
- Modify the implementation sequence
- Provide specific test case requirements for consequence integration testing