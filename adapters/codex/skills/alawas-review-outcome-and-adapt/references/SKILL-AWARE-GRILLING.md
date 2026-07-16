# Skill-Aware Grilling

Use this protocol when an unresolved decision, design, or evidence boundary
needs a conversation. The Agreement Loop is the sole conversational engine;
this reference supplies specialist coverage, not a second engine or a routine
interview.

## Conversation and persistence

Ask one highest-information question at a time, with a recommendation and its
trade-off first. Do not impose a question cap or manufacture questions after
the recommendation can no longer change.

On direct entry to a specialist, route first to `conduct-work-object` to
discover or establish the Work Object. The conductor is the sole persistent
writer. A specialist returns the compact handoff below; it never writes a
transcript or silently edits another specialist's record.

Create the following section lazily, only for an activated skill-aware grilling
session. Historical Work Objects without it remain valid.

```markdown
## Grilling

- **Coverage:** <gates accounted for + branches visited>
- **Current recommendation:** <one recommended next move and trade-off>
- **Confirmed decisions:** <links or concise decision summaries>
- **Open branches:** <unresolved or deferred branch and revisit trigger>
- **Evidence and assumptions:** <provenance-labelled, minimum necessary>
- **Handoff:** <receiving specialist and its recommended first question>
```

## Handoff contract

Every specialist returns these five fields to the conductor:

1. **Current recommendation** — one scoped next move and trade-off.
2. **Confirmed decisions** — only accepted, durable conclusions.
3. **Open branches** — unresolved or deferred material and revisit triggers.
4. **Evidence and assumptions** — attributable facts, inferences, and limits.
5. **Receiving first question** — the next specialist and its highest-value question, or `none` when action can proceed.

## Coverage lenses

Apply only the named lens for the receiving specialist. Each lens has two
tiers. **Gates** are obligatory only when they concern authority or consent,
irreversibility or external consequence, or a privacy or data boundary.
Epistemic-quality material is never a gate. **Escalation** gives the default
branch to explore; information value overrides that default when another branch
can more materially change the recommendation. Coverage means **gates
accounted for + branches visited**. Unvisited non-gate branches need not be
recorded.

### `conduct-work-object`

**Gates**

- Authority for a consequential status, state, or attention mutation.
- Immutable identity and append-only History boundary before persistence.
- Sensitivity classification and storage boundary for the record.

**Escalation** — Default to intent, scope, type, success evidence, constraints,
and next move; follow a different branch first when it better determines a
safe, authorized record.

**Pressure scenario** — A request asks to reactivate a paused high-consequence
object while introducing restricted material: what can be recorded, and what
requires fresh authority?

### `turn-signal-into-work`

**Gates**

- Explicit authority to activate rather than merely retain or incubate a signal.
- Approved, redacted Evidence Bridge before personal context crosses the
  Work Studio boundary.
- Retention or discard choice when preserving the signal creates a durable data
  consequence.

**Escalation** — Default to the user-language signal and its classification;
raise provenance, existing context, or an incubation trigger when it has more
information value.

**Pressure scenario** — A user says “remember this” about private context but
has not approved an Evidence Bridge: which minimal next step preserves the
boundary?

### `pressure-test-decision`

**Gates**

- Decision owner and authority to accept the chosen branch.
- Irreversible, external, or materially consequential effect of the choice.
- Privacy boundary for evidence used to compare alternatives.

**Escalation** — Default to alternatives, trade-offs, and disconfirming
evidence; pursue dependencies or failure cases first when they could reverse
the recommendation.

**Pressure scenario** — The apparently best option is reversible internally
but commits another team: whose consent changes the decision path?

### `design-tracer-bullet`

**Gates**

- Authority and data-access boundary for the proposed end-to-end slice.
- Rollback route for an irreversible or externally visible effect.
- Privacy boundary for test data, observations, and artifacts.

**Escalation** — Default to the riskiest falsifiable assumption and smallest
slice; lead with failure behavior or observability when it can expose a more
costly mistake.

**Pressure scenario** — The smallest slice needs production-like personal data
to be meaningful: what safe substitute preserves the test without broadening
access?

### `implement-bounded-change`

**Gates**

- Recorded authority for the accepted change and any newly proposed deviation.
- Compatibility, data, or external side-effect boundary that could make the
  change hard to reverse.
- Access boundary for affected repository, configuration, or sensitive data.

**Escalation** — Default to the accepted seam, smallest sequence, and focused
checks; investigate recovery behavior first when failure would create the
largest consequence.

**Pressure scenario** — A passing implementation requires a schema migration
outside the accepted slice: where must work stop for renewed authority?

### `verify-release-evidence`

**Gates**

- Authority before production access, external writes, release, or deployment
  verification.
- Recovery evidence for an irreversible or materially consequential failure.
- Privacy and security boundary for fixtures, logs, credentials, and data.

**Escalation** — Default to executable acceptance evidence; move first to the
most consequential failure, dependency, or recovery gap when it can change the
assessment.

**Pressure scenario** — The only missing check would inspect live customer
data: what can be verified locally, and what remains an explicit gap?

### `deploy-with-recovery`

**Gates**

- Explicit deployment authority, target, and accountable rollback owner.
- Migration, capacity, and external-impact guardrails for the increment.
- Access and data boundary for deployment credentials and target systems.

**Escalation** — Default to artifact identity, readiness, and increment
verification; prioritize the stop criterion or recovery path when it dominates
the risk.

**Pressure scenario** — Capacity is healthy but the rollback owner is absent:
can the increment proceed, and who has authority to decide?

### `review-outcome-and-adapt`

**Gates**

- Authority to close, observe, or create a successor with durable consequences.
- Boundary around any external effect that cannot be reversed by review.
- Privacy boundary for outcome evidence and unintended-effect observations.

**Escalation** — Default to the hypothesis, observed outcome, and comparison;
follow contrary evidence or unintended effects first when they could invalidate
the learning.

**Pressure scenario** — The evidence supports closing the work, but a private
observation suggests harm to another person: what may be recorded and what
follow-up is required?

### `investigate-live-question`

**Gates**

- Authority for any evidence collection that contacts people, systems, or
  external sources.
- Irreversibility or external consequence of the next evidence move.
- Privacy boundary for sources, observations, and an Evidence Bridge.

**Escalation** — Default to the current hypothesis and smallest discriminating
move; explore contradictions or missing reality contact first when they have
greater information value.

**Pressure scenario** — The best discriminating test would message a customer:
what lower-impact evidence can be gathered without that external contact?

### `diagnose-production-incident`

**Gates**

- Mitigation, recovery, and communications authority.
- Containment and recovery boundary for user, system, or irreversible impact.
- Privacy and access boundary for incident logs, identifiers, and diagnostics.

**Escalation** — Default to scope, symptoms, timeline, and containment;
prioritize the safest diagnostic move when it can reduce ongoing harm fastest.

**Pressure scenario** — A log query may expose customer identifiers while the
incident is growing: which redacted diagnostic path is safe enough to run now?

### `maintain-working-method`

**Gates**

- Authority to promote a candidate into a durable working-method rule.
- Consequence of a rule that changes future workflow or relationship handling.
- Evidence Bridge and privacy boundary for personal context.

**Escalation** — Default to a testable rule and bounded-test quality; inspect
contrary evidence or lifecycle history first when it could prevent a harmful
promotion.

**Pressure scenario** — A compelling candidate draws on a private observation
but lacks a redacted bridge: what stays outside the Work Object?

### `govern-scorecards`

**Gates**

- Authority to change a scorecard rule or create a successor relationship.
- Consequence of aggregates, identity claims, or automatic rule changes.
- Personal-fit and provenance boundary for the reviewed evidence.

**Escalation** — Default to applicable dimensions and evidence gaps; pursue
exceptions or conflicts first when they could make the candidate unsafe to
advance.

**Pressure scenario** — A scorecard trend favors a rule change, but the trend
combines private evidence with activity proxies: what blocks automatic action?
