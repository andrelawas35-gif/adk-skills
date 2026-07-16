# Skill-Aware Grilling

Use this protocol when an unresolved decision, design, or evidence boundary needs a conversation. It extends the Agreement Loop; it does not turn routine, discoverable work into an interview.

## Conversation and persistence

Ask one highest-information question at a time, with a recommendation and its trade-off first. Continue until every applicable component below is resolved, explicitly deferred with a revisit trigger, or marked `not applicable` with a reason. Do not impose a question cap or manufacture questions after the recommendation can no longer change.

On direct entry to a specialist, route first to `conduct-work-object` to discover or establish the Work Object. The conductor is the sole persistent writer. A specialist returns the compact handoff below; it never writes a transcript or silently edits another specialist's record.

Create the following section lazily, only for an activated skill-aware grilling session. Historical Work Objects without it remain valid.

```markdown
## Grilling

- **Coverage:** <lens, resolved components, and not-applicable components with reasons>
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

Apply only the named lens for the receiving specialist. Treat every listed component as required or explicitly not applicable with a reason.

### `conduct-work-object`

Intent and scope; existing-match check; type; consequence; sensitivity; success evidence; constraints and non-goals; active-role capacity; initial state and next move; persistence and History boundary.

### `turn-signal-into-work`

Original user-language signal; provenance and sensitivity; relevant existing context; discard/remember/incubate/activate classification; incubation revisit trigger; Evidence Bridge gate; explicit activation authority.

### `pressure-test-decision`

Decision statement and owner; evidence versus inference; dependencies; materially distinct alternatives; trade-offs; confidence and disconfirming evidence; edge, failure, and future tests; confirmed choice and revisit trigger.

### `design-tracer-bullet`

Riskiest falsifiable assumption; smallest end-to-end slice; entry and resulting state; authorization and data boundary; failure behavior; observability; non-goals; rollback; exit evidence; route for either outcome.

### `implement-bounded-change`

Accepted design boundary; repository seam and affected components; acceptance criteria; smallest implementation sequence; compatibility and data effects; failure and recovery behavior; focused checks; scope exclusions; deviation requiring renewed authority.

### `verify-release-evidence`

Acceptance criterion and executable check; material failure and recovery; retries or duplicate handling when relevant; dependency degradation; privacy and security boundary; evidence provenance; unverified gaps; exact next route.

### `deploy-with-recovery`

Deployment authority; target and bounded increment; artifact identity; readiness and capacity guardrails; migration status; access boundary; rollback owner and action; increment verification; observation window; stop and escalation criteria.

### `review-outcome-and-adapt`

Original hypothesis and success evidence; observed outcome; expectation comparison; contributing conditions; contrary evidence; unintended effects; confidence; learning and recommendation; follow-up threshold; close, observe, or successor route.

### `investigate-live-question`

Inquiry claim; current hypothesis; provenance-labelled evidence; source quality; contradictions; missing reality contact; smallest discriminating evidence move; privacy and authority boundaries; confidence; decision or design route.

### `diagnose-production-incident`

Incident scope and consequence; symptoms and timeline; affected users and systems; current containment; evidence gaps; plausible mechanisms; smallest safe diagnostic move; mitigation or recovery authority; communications boundary; recovery evidence before routing onward.

### `maintain-working-method`

Candidate identity; testable proposed rule and scope; origin; supporting and contrary evidence; bounded-test quality; Evidence Bridge boundary; lifecycle and relationship history; promotion prerequisites; uncertainty.

### `govern-scorecards`

Review boundary; each applicable dimension's evidence and provenance; inference, confidence, and exceptions; conflicts and evidence gaps; personal-fit boundary; novelty yield; bounded candidate proposal or successor relationship; appropriate route without aggregates, activity proxies, identity claims, or automatic rule changes.
