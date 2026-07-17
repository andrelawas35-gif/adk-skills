# Skill-Aware Grilling

This catalogue supplies the stage-specific **Skill Grilling Profiles** used by
the conversational engine in `AGREEMENT-LOOP.md`. A profile determines what to
inspect, which tension to pursue next, how to challenge the emerging answer,
where to route it, and when its stage has enough understanding. It is not a
checklist and never replaces the one-question conversational turn contract.

## Shared behavior

Use the active Work Object, project stage, codebase, tests, configuration,
ADRs, workflow records, and permitted conversation context before questioning
the user. Ask only about owner decisions or facts that cannot be discovered.

The Decision Frontier is selected by probability, impact, uncertainty,
irreversibility, and dependency reach. Authority or consent, privacy or data
boundaries, irreversible or external consequences, and ongoing harm form the
non-compensable safety floor. Surface those branches even when unlikely.

An explicit grilling request starts immediately. Otherwise, activate only when
a material unresolved choice can change the recommendation. If no such choice
exists, proceed normally and state why grilling was unnecessary.

Direct specialist entry routes through `conduct-work-object` to discover or
establish continuity. The conductor is the sole persistent writer. Routing
changes the active profile but preserves the same Grilling Session.

## Compact Grilling Session state

Create this Work Object section lazily, only when a session activates. Existing
objects remain valid and adopt it when resumed; never fabricate past reasoning.

```markdown
## Grilling Session

- **Revision:** <Work Object revision used for optimistic concurrency>
- **Context Card:** <goal, stage, approved preferences, inspected evidence>
- **Active profile and activation reason:** <skill + detected tension>
- **Decision Frontier:** <one active unresolved branch and why it matters>
- **Coverage:** <resolved | active | deferred with trigger | ruled out by evidence>
- **Current recommendation:** <one answer, trade-off, and change condition>
- **Confirmed decisions:** <links to canonical decisions>
- **Evidence Ledger:** <links, conflicts, assumptions, and explicit gaps>
- **Next question:** <one receiving-skill question, or none at convergence>
```

Store full decisions, evidence, verification, outcomes, and History in their
canonical sections. Do not persist transcripts or hidden reasoning.

## Continuity record

Every specialist returns the conductor:

1. current recommendation, trade-off, and what would change it;
2. confirmed decisions and the rationale/provenance links;
3. resolved, active, deferred, and ruled-out branches;
4. evidence, source conflicts, inferences, and gaps;
5. active or receiving profile, routing reason, and exactly one next question;
6. Coverage Proof when the profile or whole session converges.

The receiving skill first states what it inherited. `do recommended` accepts
only the current recommendation; it does not close branches or authorize Work
Object mutation beyond the named decision.

## Skill Grilling Profiles

### `turn-signal-into-work`

**Inspect** — The signal in the user's language, its provenance and sensitivity,
approved memory or Evidence Bridge, related Work Objects and decisions, and
overlapping code or project evidence.

**First frontier** — Confirm the interpretation before classifying activation,
incubation, retention, or discard. Keep ambiguous overlap with existing work
and record a split trigger.

**Challenge and novelty** — Challenge inferred meaning, duplicate outcomes,
weak provenance, private context crossing boundaries, and activation without a
meaningful outcome, evidence move, or available attention. Recommend a cheap
investigation when it can decide whether activation is worthwhile.

**Route** — Classification goes to `conduct-work-object`; uncertain evidence to
`investigate-live-question`. Classification authority never silently authorizes
Work Object creation.

**Complete when** — Interpretation, provenance, sensitivity, existing-work
relationship, classification, evidence gap, and next question are accepted.

### `conduct-work-object`

**Inspect** — Inherited conversation, existing Work Objects and relationships,
decisions, codebase seams, intended outcome, positive and negative evidence,
consequence, sensitivity, authority, and current lifecycle state.

**First frontier** — Express one coherent, testable outcome in the user's
language. Split independently completable outcomes; create linked children or
successors when consequence, evidence, ownership, or lifecycle differs.

**Challenge and novelty** — Challenge duplicate work by outcome rather than
title, activity-shaped success criteria, unexplained consequence labels,
impossible state jumps, and unowned decisions. Preserve rationale and
provenance for every consequential field.

**Route** — Recommend the next profile from consequence, uncertainty, and
project stage. The conductor alone validates schema, persists state, appends
History, and resolves optimistic-concurrency conflicts.

**Complete when** — The user accepts the compact object synthesis and the exact
authorized mutation. Routine updates inside accepted state use existing
authority; attention, ownership, external consequence, or lifecycle commitment
requires explicit approval.

### `pressure-test-decision`

**Inspect** — Decision owner, deadline, consequence of no decision, viable
alternatives, prior decisions, code constraints, dependencies, and acceptance
criteria.

**First frontier** — Find the assumption carrying the most decision risk and
seek the strongest codebase-grounded disconfirming evidence before comparing
minor trade-offs.

**Challenge and novelty** — Reject false binaries; introduce a third option,
staged trial, reversible experiment, or evidence-triggered deferral only when
grounded. Challenge unowned “must-have” criteria. Test the leading option
against one codebase counterexample and one low-probability/high-impact case.

**Route** — Prefer a cheap reversible experiment when it discriminates better
than discussion. Route missing evidence to investigation or tracer-bullet
design; keep the decision provisional until decisive evidence arrives.

**Complete when** — The decision brief records the selected branch, rejected
alternatives, supporting and contrary evidence, guardrails, residual risks,
authority, and revisit triggers.

### `design-tracer-bullet`

**Inspect** — The provisional decision, riskiest falsifiable assumption,
production code path, data and access boundaries, dependencies, observability,
failure behavior, and execution environment.

**First frontier** — Define observable exit evidence and the result that would
disprove the assumption before choosing the smallest end-to-end slice.

**Challenge and novelty** — Reject technical-connectivity demos that cannot
resolve the underlying assumption. Reject mocks replacing the dependency or
failure behavior under test. Make success and informative failure observable
without sensitive-data exposure; name realism lost by substitutes.

**Route** — Inconclusive results route to a smaller discriminating experiment
or investigation. Real-user or durable-production execution requires separate
authority from design acceptance.

**Complete when** — The design contains containment, external-effect limits,
stop conditions, cleanup/recovery, and a result-to-action table that reopens
the provisional decision on unexpected evidence.

### `implement-bounded-change`

**Inspect** — Accepted design, current repository and dirty state, intended
seams, protected behavior, compatibility obligations, non-goals, dependencies,
data boundaries, and focused verification path.

**First frontier** — Reconcile the accepted boundary with current code and
establish a failing or otherwise discriminating check whenever practical.

**Challenge and novelty** — Stop when the smallest viable change crosses an
unapproved schema, public interface, dependency, deployment configuration, data
boundary, or external effect. Keep adjacent cleanup outside scope unless its
causal necessity, risk, and revised verification plan are explicitly accepted.
Protect unrelated dirty changes.

**Route** — Run focused checks after coherent increments. Revert only the
skill's attributable latest increment when safe. Route scope changes back to
the conductor and implementation claims to independent verification.

**Complete when** — Every changed line maps to accepted behavior, necessary
support, or an attributable generated consequence, and the handoff states exact
changes, checks, gaps, compatibility risk, and recovery considerations. This
profile never marks the object verified.

### `verify-release-evidence`

**Inspect** — Every acceptance and negative-evidence claim, implementation
evidence versus independently reproduced evidence, integrated interfaces,
environment dependencies, recovery claims, privacy/security boundaries, and
downstream consumers.

**First frontier** — Test the consequential claim with the weakest direct
evidence. Require a reproducible check, observable artifact, or explicitly
authorized human judgment.

**Challenge and novelty** — Validate that consequential checks fail when their
protected behavior is safely violated. Test the strongest credible negative
case and inspect plausible unintended effects. A local pass cannot establish
environment-specific behavior without direct evidence.

**Route** — Classify every issue as release blocker, accepted residual risk, or
linked follow-up with trigger. Missing credible recovery blocks consequential
changes unless an accountable owner accepts the irreversible risk.

**Complete when** — A claim-by-claim matrix yields `ready`, `ready with accepted
risk`, or `not ready`, with provenance, negative evidence, environment limits,
recovery, and gaps. `not ready` cannot be overridden without new evidence or a
revised change.

### `deploy-with-recovery`

**Inspect** — Verified artifact identity, target configuration, residual risks,
current target health, concurrent changes, affected users/data, increment,
signals, observation window, rollback mechanism, and available rollback owner.

**First frontier** — Prove equivalence between the verified and deployable
artifact, then choose the smallest observable increment appropriate to
consequence and recoverability.

**Challenge and novelty** — Require success and failure signals, freshness
windows, stop conditions, and rehearsed or directly evidenced recovery. Freeze
expansion on uncertain signals. “No alert” is not success without relevant
instrumentation.

**Route** — Expand, hold, recover, or investigate after each observation
window. Potential ongoing harm routes to incident response; stable ambiguity
routes to investigation. Each increment requires positive outcome evidence and
absence of decisive negative evidence.

**Complete when** — The final increment passes its window, recovery remains
viable, operational ownership transfers, and artifact, target, evidence,
anomalies, risks, and the mandatory outcome-review trigger are recorded.

### `review-outcome-and-adapt`

**Inspect** — Original hypothesis, acceptance and negative evidence, deployed
boundary, residual risks, expected window, actual technical behavior,
user/system outcome, unintended effects, affected groups, and concurrent
factors.

**First frontier** — Compare expected and observed reality with an explicit
counterfactual and attribution strength; do not equate healthy deployment with
achieved outcome.

**Challenge and novelty** — Search for contrary evidence and subgroup harm
hidden by aggregates. Compare every accepted risk and deferred branch with what
occurred. Route each material mismatch to the earliest invalid assumption.

**Route** — Close as achieved, close with uncertainty, continue, or create a
linked successor when outcome, evidence, owner, consequence, or lifecycle is
distinct. Produce working-method candidates without promoting them.

**Complete when** — The learning record preserves expected versus observed
results, attribution, unintended effects, mismatches, routed follow-ups, and
next observation trigger. Consequential or uncertain closure requires owner
acceptance.

### `investigate-live-question`

**Inspect** — One falsifiable question, existing code/tests/records/ADRs,
operational evidence, prior conversation, source freshness, and permitted
evidence boundaries.

**First frontier** — Identify the smallest evidence gap most likely to change
the recommendation, and predefine what results support, weaken, or leave the
hypothesis unresolved.

**Challenge and novelty** — Maintain multiple viable hypotheses, expose source
conflicts, and test the strongest plausible alternative unless the next move is
safe and useful under either. Add a novel hypothesis only when evidence or a
contradiction warrants it.

**Route** — Prefer existing artifacts and local checks before people,
production, sensitive data, or external sources. Obtain narrow authority for
consequential collection. Treat human evidence as attributable testimony.

**Complete when** — The hypothesis is supported, weakened, unresolved with a
named next test, or escalated to incident response. Return evidence to the
accountable skill; do not change consequential lifecycle state directly.

### `diagnose-production-incident`

**Inspect** — Current harm, affected boundary, severity, onset, symptoms,
recent changes, containment, target health, evidence freshness, access and
communications authority, and recovery state.

**First frontier** — Reduce growing harm with the safest reversible containment
that works across leading hypotheses; preserve minimum safe evidence when that
does not prolong harm.

**Challenge and novelty** — Maintain separate impact/containment,
mechanism-diagnosis, and communication tracks with a live timeline and
hypothesis set. Recent changes are hypotheses, not causes without timeline and
mechanism evidence. Use narrow, redacted diagnostics and expiring emergency
access.

**Route** — Apply containment incrementally when the harm trajectory permits.
Keep the incident open until user-facing recovery, data integrity, affected
scope, dependencies, and containment side effects are bounded or owned.

**Complete when** — Timeline, hypotheses, containment/recovery evidence,
affected scope, communications, access review, uncertainty, and follow-ups are
recorded. Always route to outcome review; high-consequence or recurring
patterns also route to working-method maintenance.

### `maintain-working-method`

**Inspect** — Concrete observed behavior, linked Work Objects, reviews,
incidents, repeated and contrary evidence, current rules, personal-fit context,
and the outcome the candidate should improve.

**First frontier** — Require an observable behavior and reviewable outcome,
then find contexts where the proposed rule creates friction, ceremony, lost
autonomy, or worse results.

**Challenge and novelty** — Define `use when`, `do not use when`, and exception
authority. Test through a bounded trial with benefit, counter-signals, burden,
and rollback. Temporary guardrails expire automatically. Frequent exceptions
challenge the rule boundary before they imply noncompliance.

**Route** — Separate attributed, overrideable personal-fit defaults from shared
rules requiring evidence across affected participants and contexts.

**Complete when** — Promotion preserves evidence history, trial and contrary
results, applicability, exceptions, owner, and review trigger. Materially
changed rules become linked successors rather than silent edits.

### `govern-scorecards`

**Inspect** — The decision the scorecard informs, dimensions, evidence sources,
freshness, uncertainty, distributions, exceptions, subgroup effects, current
rules, and personal/privacy boundaries.

**First frontier** — Determine whether each dimension has attributable,
decision-relevant evidence. Reject activity proxies used as outcome quality
without demonstrated correlation.

**Challenge and novelty** — Separate observation, interpretation, and action.
Do not aggregate away non-compensable failures or subgroup harm. Missing
evidence is unknown, never zero. Retire dimensions that repeatedly fail to
inform decisions; challenge identity claims and surveillance-like proxies.

**Route** — Thresholds trigger evidence inspection, not automatic action.
Personal evidence is private by default; aggregation, sharing, or system-wide
rule creation requires explicit purpose, minimal disclosure, and authority.

**Complete when** — Rule versions preserve the basis of historical results,
and every change states whether old and new results are comparable. Scorecard
evidence may recommend investigation or review but cannot silently mutate work
or policy.

## Coverage Proof across profiles

Before ending the Grilling Session, verify that relevant upstream, current, and
downstream profiles were considered by probability and consequence. A profile
need not be visited when evidence rules it out; record why. No numerical turn
target substitutes for this proof.
