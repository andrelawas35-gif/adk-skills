# Use a continuous cross-skill Grilling Session

## Context

The earlier two-tier coverage lenses ensured that safety gates were visible,
but an agent could satisfy them by emitting a polished result. They did not
require the agent to reflect what changed, ground challenges in exact project
evidence, adapt the next question to the user's answer, or preserve one
conversation across specialist routes. The result felt like a checklist rather
than Matt Pocock-style grilling.

## Decision

Use the Agreement Loop as one continuous Grilling Session attached lazily to a
Work Object. It begins with a correctable Context Card, maintains an
Evidence Ledger and one Decision Frontier, gives a recommendation before
exactly one question, waits, integrates the answer, and selects the next branch
by probability, impact, uncertainty, irreversibility, and dependency reach.

Skill invocation changes only the active Skill Grilling Profile. It never
resets the Grilling Session, Context Card, Evidence Ledger, Decision Frontier,
or accepted decisions. Each profile defines stage-specific evidence,
challenges, routes, and completion criteria. Codebase challenges require exact
local evidence; memory-derived personalization must be attributable,
user-approved, relevant, and correctable.

There is no numerical question cap. A turn must make decision progress, and the
session converges only with a Coverage Proof. `do recommended` accepts only the
current recommendation. Consequential action requires a separate scoped
confirmation naming affected systems and the verification boundary.

The conductor remains the sole persistent writer. It stores compact continuity
state rather than transcripts and uses optimistic concurrency across tasks.

This decision supersedes ADR 0011's two-tier coverage-lens model and refines
ADR 0010's Work Object persistence shape.

## Consequences

Grilling becomes a real, resumable conversation grounded in the project and
the user's approved working preferences. Cross-skill continuity and exhaustive
material coverage improve, including sessions longer than 200 turns when each
turn still changes the decision state.

The trade-off is more state and behavioral testing. Skills must prove both
activation and non-activation behavior, provenance discipline, one-question
turns, progress, routing continuity, and convergence. Revisit this decision if
the continuity state becomes too costly, if profiles drift, or if behavioral
fixtures show that the engine still produces artifacts before shared
understanding.
