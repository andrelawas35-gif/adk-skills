# Use behavioral scenarios as the skill regression suite

Work Studio will validate skill and handoff changes against small behavioral fixtures containing realistic prompts, expected observable outcomes, and prohibited outcomes. The fixtures test contracts such as privacy boundaries, provenance, user authority, and graceful degradation rather than prescribing prompts or hidden reasoning.

## Consequences

New cross-package behavior is not considered cohesive until it has a scenario. A failed scenario should lead to a narrow instruction or protocol change before more skills are added.
