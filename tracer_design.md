# COMP-046 Tracer Bullet Design: Camera Mathematics Proof of Concept

## What I take the question to be
Design smallest bounded tracer proving camera mathematics can be computed purely 
(no external dependencies) and returns data compatible with existing Scene Planner infrastructure.

## Riskiest assumption (falsifiable)
Camera mathematics functions can be computed purely from scene parameters and emotional keywords 
without external dependencies, returning structured data compatible with Scene Planner's existing camera field.

This is falsifiable by attempting implementation and verifying:
1. Pure computation path works (no tool calls, no subprocesses)
2. Returns dict structure compatible with Scene Planner's camera field
3. Parameters come from scene planner input, not aesthetic judgment

## Recommendation: Bounded tracer bullet design

### Function signature
def focal_length_for_effect(
    scene_scale: float, 
    emotional_read: str,
    camera_height: float = 1.75
) -> dict[str, Any]:
    '''
    Computes focal length based on emotional keywords and scene scale.
    
    Parameters come from Scene Planner (camera field structure), not aesthetic judgment.
    
    Returns structured data compatible with Scene Planner's existing 'camera' field format.
    
    Pure computation only - no external dependencies.
    '''

### Entry state -> Resulting state
- Entry: Function called with scene_scale and emotional_read parameters from Scene Planner
- Result: dict containing focal_length, fov, depth_of_field, composition_notes

### State and authorization
- State transition: None - pure computation function returning data structure
- Authorization: Read-only access to scene parameters; no Blender API calls during design phase
- Implementation phase: Function writes only to return value, not filesystem

### Failure behavior
- Expected failure modes: 
  - Unknown emotional keyword -> returns default focal length with warning flag
  - Invalid scene scale -> raises ValueError with clear message (not silent failure)
- Safe response: Returns structured error dict or fallback values rather than crashing
- Do not claim: This proves all camera math functions work; only this one path

### Observability
- Minimal evidence: 
  - Unit test output showing function returns correct structure
  - Integration test with Scene Planner verifying data compatibility
  - No live Blender render required during design phase (deferred to build)

### Non-goals
- Implementing all 15 camera/composition/blocking functions (full implementation scope)
- Live Blender testing with actual rendering (belongs to verify/build phases)
- Creative decisions about what emotional effect to achieve (belongs to Scene Planner)
- Aesthetic judgment or shot interpretation

### Rollback
- Removal: Delete single function file or comment out import in Scene Planner
- Disable: Remove function call from scene planner workflow
- No durable state impact: Pure computation returns data only; no side effects

### Exit criteria and next route
- If assumption holds (tracer succeeds):
  - Route to implement-bounded-change for full COMP-046 implementation
  - Evidence: Unit tests pass, Scene Planner integration test passes
  
- If assumption fails (tracer fails):
  - Route to alawas-design-develop-idea to explore alternative approaches

### Decision status
Proposed design accepted - ready for implementation in next phase.

## Question
None - this is a bounded, low-consequence tracer bullet with clear acceptance criteria. 
User has already approved the single-function approach. Proceed to implement-bounded-change.

