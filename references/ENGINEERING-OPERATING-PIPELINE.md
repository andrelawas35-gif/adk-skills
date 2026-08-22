# Engineering Operating Pipeline

## Purpose

The engineering operating pipeline is the canonical routing spine for
engineering and operations questions in Work Studio. It does not replace the
Work Object lifecycle. A Work Object still governs durable state, authority,
evidence, and resumption; this pipeline decides which engineering, operations,
or governance skill owns the next engineering frontier.

## Pipeline distinction

| Pipeline | Owns | Does not own |
|----------|------|--------------|
| Work Object lifecycle | Work state: notice, explore, design, build, verify, release, observe, close. | Engineering judgment by itself. |
| Engineering operating pipeline | Cross-engineering routing from tracer design through implementation, verification, deployment recovery, incident diagnosis, and outcome review. | Lifecycle state transitions, live CI/CD mutation, production access, deployment, or external commitments. |
| Release pipeline | Environment-specific CI/CD execution, approvals, deployments, rollback, and operational change windows. | Work Object authority, evidence adequacy, or engineering route ownership by itself. |

## Canonical route

Use this order as a default route map, not a mandatory sequence. Enter at the
first skill that owns the current decision frontier, then route to the next
skill only when the evidence exposes that downstream question.

```text
design-tracer-bullet
→ engineering-implement-bounded-change
→ engineering-verify-release-evidence
→ operations-deploy-with-recovery
→ operations-diagnose-production-incident
→ governance-govern-scorecards
→ governance-review-outcome-and-adapt
→ design-tracer-bullet when evidence changes the tracer boundary
```

## Ownership map

| Engineering frontier | Owning skill |
|----------------------|--------------|
| Tracer boundary, riskiest assumption, observable exit evidence, rollback shape | `design-tracer-bullet` |
| Accepted implementation slice, code change, local repository edit, reversible bounded path | `engineering-implement-bounded-change` |
| CI failure, test failure, verification gap, release evidence, dependency degradation, privacy or security check | `engineering-verify-release-evidence` |
| Deployment plan, release gate, recovery plan, rollback drill, change window, deployment dependency | `operations-deploy-with-recovery` |
| Production incident, outage, symptom, suspected cause, mitigation, recovery evidence, recurrence risk | `operations-diagnose-production-incident` |
| Engineering scorecard, reliability trend, recurring pipeline gap, governance proposal candidate | `governance-govern-scorecards` and `governance-review-outcome-and-adapt` |

## Handoff rules

1. Stay inside the same Work Object when the next engineering question is part
   of the same bounded change and does not need separate ownership, acceptance
   evidence, or authority.
2. Create a linked Work Object when the next question has a different owner,
   consequence, sensitivity, material acceptance criteria, environment, or
   implementation path.
3. Route to the conductor for any lifecycle transition, History entry, Evidence
   ledger entry, successor Work Object, authority record, or external-effect
   boundary.
4. Treat production access, live CI/CD mutation, deployment, rollback against a
   live environment, incident tooling, secrets, customer data, and external
   service mutation as gated actions requiring scoped authority.
5. Do not let a later-stage skill silently settle an earlier-stage assumption.
   If downstream evidence contradicts tracer, implementation, verification,
   deployment, incident, or scorecard assumptions, route back to the owning
   skill and preserve the contradiction.

## Minimum handoff record

Every engineering-to-engineering-skill handoff should name:

- current Work Object ID and lifecycle state;
- current engineering frontier and owning skill;
- evidence that made the current frontier sufficiently answered;
- open assumption or gap that belongs to the next skill;
- whether the next question stays in the same Work Object or needs a linked
  successor;
- exact authority boundary if the next move would touch live CI/CD,
  production, secrets, deployment, incident tooling, external services, or user
  data.

## Revisit triggers

Revisit this pipeline when:

- real Work Object use shows recurring route ambiguity;
- missing engineering domains such as architecture review, dependency
  management, observability, security, data migration, or release management
  become repeated handoff gaps;
- Phase 6 needs deterministic `engineering_scope` routing rather than reference
  guidance;
- evidence shows the canonical order causes premature release work or hides
  upstream implementation or verification uncertainty.
