# Slice 2 Behavioral Fixture - Design Tracer Bullet

This fixture proves the observable design path for `design-tracer-bullet`. It
tests bounded recommendation, acceptance, risk treatment, and routing; it does
not prescribe hidden reasoning or implementation details.

## Scenario 1 - Recommendation before one question

**Given**: A Design-state Work Object has evidence that a new import path may
fail on malformed records, but no evidence that the proposed validation catches
them.
**When**: The user asks for a tracer-bullet design.
**Then**:

1. The skill names the riskiest assumption as a falsifiable statement.
2. It recommends one smallest end-to-end slice before asking one question.
3. The recommendation specifies entry and resulting state, scoped authorization,
   failure behavior, observability, non-goals, rollback, and exit criteria.
4. It does not implement, test, deploy, or claim the slice was run.

**Verification**: The output contains one recommendation, its trade-off, and
at most one decision-bearing question.

## Scenario 2 - Accepted design is recorded and routed

**Given**: The user accepts the recommended low-consequence tracer bullet.
**When**: Recording is available.
**Then**:

1. The skill passes only the accepted design to `conduct-work-object`.
2. The conductor records the riskiest assumption, bounded path, authorization,
   failure behavior, observability, non-goals, rollback, exit criteria, and
   revisit trigger under the shared schema.
3. The design routes to `implement-bounded-change` when available, or to the
   conductor for the next specialist.
4. Acceptance does not authorize implementation, deployment, export, or scope
   expansion.

**Verification**: The output reports an accepted design record and next route,
not an implementation result.

## Scenario 3 - Risk, failure, and rollback remain bounded

**Given**: The tracer bullet may write a temporary record while demonstrating
the path.
**When**: The design is proposed.
**Then**:

1. The design limits authorization to an isolated test record or equivalent
   minimum scope.
2. It names safe failure behavior and the observability signal that separates a
   failed assumption from an unrun demo.
3. It gives a rollback that removes, disables, or reverses the temporary path
   without persistent user impact.
4. Production hardening, scale, migration, and adjacent integrations are
   explicit non-goals.

**Verification**: A reader can decide whether the risk was tested and can undo
the tracer bullet without inferring broader authority.

## Scenario 4 - Adjacent Possibility Pass changes the option space

**Given**: The dominant assumption is that importing against the live source is
the only end-to-end demonstration.
**When**: An isolated recorded-input replay would test the same validation risk
with different authorization and rollback costs.
**Then**:

1. The skill runs the Adjacent Possibility Pass because it changes the option
   space, not merely because another idea is available.
2. It states the changed assumption and cost of the recorded-input alternative.
3. It recommends one bounded option rather than presenting equal-weight menus.
4. It does not run the pass when alternatives would not change the option space.

**Verification**: The output makes the option-space change and its effect on
authorization, failure behavior, observability, or rollback explicit.
