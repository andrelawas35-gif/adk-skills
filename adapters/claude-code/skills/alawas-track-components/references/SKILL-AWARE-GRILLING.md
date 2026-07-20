# Skill-Aware Grilling

This catalogue supplies the stage-specific **Skill Grilling Profiles** used by
the conversational engine in `AGREEMENT-LOOP.md`. A profile determines what to
inspect, which tension to pursue next, how to challenge the emerging answer,
where to route it, and when its stage has enough understanding. It is not a
checklist and never replaces the one-question conversational turn contract.

## Skill Grilling Profiles

### `turn-signal-into-work`

**Gates** — (1) Provenance and sensitivity: confirm the signal's source and
whether using it crosses a privacy or data boundary before acting on it. (2)
Classification authority: confirm that classifying or activating the signal
does not silently authorize Work Object creation without the authority that
requires.

**Escalation** — Default: confirm the interpretation, check `active.md` and
existing Work Objects for overlap, classify as activation, incubation,
retention, or discard, and route classification to `conduct-work-object`.
Information value overrides the default when evidence strongly indicates
duplicate work or an unresolved evidence gap — escalate directly to
`investigate-live-question` before classifying.

**Pressure scenario** — The signal is ambiguous between two established Work
Objects: would classifying it as new silently fork tracked work, and which
existing object's evidence would that duplicate?

### `conduct-work-object`

**Gates** — (1) Consequence and authority: confirm whether the requested
mutation is attention, ownership, external consequence, or lifecycle
commitment, which requires explicit user approval, versus a routine update
inside existing authority. (2) Concurrency integrity: confirm `updated_at`
has not changed since read before writing, preventing a silent overwrite of
another actor's concurrent edit.

**Escalation** — Default: read existing Work Objects and decisions, express
one coherent testable outcome, recommend the next profile by consequence,
uncertainty, and stage, and apply routine updates under existing authority.
Information value overrides the default when evidence shows duplicate work by
outcome (not title) or an unowned decision — escalate to reconciling the
duplication or naming an owner before continuing.

**Pressure scenario** — Two Work Objects converge on the same outcome under
different titles: does completing one silently obsolete evidence in the
other, and who owns reconciling them?

### `pressure-test-decision`

**Gates** — (1) Decision authority: confirm who owns the decision and that
recording it does not exceed the Work Object's consequence-based authority.
(2) Irreversibility of the chosen branch: confirm the branch's reversibility
before recording it, since an irreversible branch chosen on weak evidence is
a harm-bearing outcome.

**Escalation** — Default: find the assumption carrying the most decision
risk, seek the strongest disconfirming evidence, recommend one branch, test
it against a counterexample, and record it with rationale and a revisit
trigger. Information value overrides the default when a cheap reversible
experiment would discriminate better than continued discussion — escalate to
`design-tracer-bullet` before recording a provisional decision.

**Pressure scenario** — The leading branch reverses easily today but becomes
irreversible after the next deploy: does that change which branch should be
recommended, and does the decision need to be made before or after that
deploy?

### `design-tracer-bullet`

**Gates** — (1) External-effect and data boundary: confirm the design's
containment and access boundary before treating any exit evidence as safe to
observe. (2) Production execution authority: confirm that real-user or
durable-production execution is separately authorized beyond design
acceptance.

**Escalation** — Default: define observable exit evidence and the falsifying
result, choose the smallest end-to-end slice, and require containment, stop
conditions, and cleanup. Information value overrides the default when a
smaller discriminating experiment or investigation could resolve the
assumption more cheaply — escalate there instead of building the full tracer
bullet.

**Pressure scenario** — The smallest slice that produces informative failure
also touches sensitive data: is there a substitute that preserves
informativeness without the exposure, and what realism does it lose?

### `implement-bounded-change`

**Gates** — (1) Scope boundary: confirm the smallest viable change does not
cross an unapproved schema, public interface, dependency, deployment
configuration, data boundary, or external effect. (2) Unrelated dirty-work
preservation: confirm existing unrelated working-tree changes are protected
and never staged, committed, or altered.

**Escalation** — Default: reconcile the accepted boundary with current code,
establish a discriminating check, implement the smallest reversible path, and
run focused verification after each increment. Information value overrides
the default when a material new decision or authority boundary appears
mid-implementation — escalate by stopping and routing back to the conductor
for scoped confirmation rather than proceeding.

**Pressure scenario** — The bounded change verifies locally, but the working
tree also contains unrelated uncommitted work touching the same files: is the
diff actually separable for its own commit, or does isolating it require
hunk-level surgery?

### `verify-release-evidence`

**Gates** — (1) Recovery credibility: confirm a credible, reproducible
recovery path exists before treating a consequential change as ready; missing
recovery blocks readiness unless an accountable owner explicitly accepts the
irreversible risk. (2) Environment-specific behavior: confirm a local pass is
never treated as evidence of environment-specific behavior without direct
evidence from that environment.

**Escalation** — Default: test the weakest direct evidence for the most
consequential claim, require a reproducible check or explicitly authorized
human judgment, and classify every issue as blocker, accepted risk, or linked
follow-up. Information value overrides the default when the strongest
credible negative case surfaces a new failure mode — escalate to re-testing
that specific case before continuing the matrix.

**Pressure scenario** — All consequential claims pass locally, but the target
environment's data shape has never been exercised: does "ready" still hold,
or does this drop to "ready with accepted risk" pending an owner's explicit
sign-off?

### `deploy-with-recovery`

**Gates** — (1) Rollback viability: confirm a rehearsed or directly evidenced
rollback mechanism and an available rollback owner exist before any increment
ships. (2) Affected scope: confirm which users or data are exposed by the
increment, sized to consequence and recoverability.

**Escalation** — Default: prove artifact equivalence, choose the smallest
observable increment, require success and failure signals with stop
conditions, and expand only after each window passes with positive evidence.
Information value overrides the default when a signal is ambiguous or ongoing
harm is possible — escalate immediately to holding, recovering, or routing to
incident response rather than expanding.

**Pressure scenario** — The observation window shows no alert, but there is
no instrumentation covering the affected path: is "no alert" actually
evidence of success here, or a false-negative gap that should hold the
rollout?

### `review-outcome-and-adapt`

**Gates** — (1) Subgroup and unintended-effect harm: confirm aggregate
success does not hide subgroup harm or an unintended effect on an affected
group. (2) Closure consequence: confirm that consequential or uncertain
closure has explicit owner acceptance before the object closes.

**Escalation** — Default: compare expected versus observed reality with a
counterfactual and attribution strength, search for contrary evidence, and
route each mismatch to its earliest invalid assumption. Information value
overrides the default when a subgroup shows harm the aggregate doesn't —
escalate to naming that subgroup explicitly before closing as achieved.

**Pressure scenario** — The aggregate outcome looks achieved, but one
affected subgroup's data is thin: is "achieved" actually supported, or does
the object need to close with documented uncertainty for that subgroup?

### `investigate-live-question`

**Gates** — (1) Evidence-source authority: confirm narrow, scoped authority
exists before collecting people, production, or sensitive-source evidence,
rather than defaulting to it. (2) Testimony attribution: confirm human
evidence is recorded as attributable testimony, never silently promoted to
system fact.

**Escalation** — Default: identify the smallest evidence gap most likely to
change the recommendation, predefine what results support, weaken, or leave
it unresolved, and prefer existing artifacts and local checks first.
Information value overrides the default when only people, production, or
sensitive sources can resolve the gap — escalate to obtaining narrow
authority before collecting.

**Pressure scenario** — The fastest way to resolve the question is a
production query against data the requester isn't scoped to see: does the
investigation stop here, or is there a narrower authorized query that still
discriminates?

### `diagnose-production-incident`

**Gates** — (1) Ongoing-harm containment: confirm the safest reversible
containment is applied before anything else when harm is actively growing.
(2) Emergency-access scope: confirm diagnostic access and communications
authority are narrow, redacted, and expiring, never standing.

**Escalation** — Default: reduce growing harm with safe reversible
containment across leading hypotheses, maintain separate impact, mechanism,
and communication tracks, and apply containment incrementally as the harm
trajectory permits. Information value overrides the default when a recent
change is only a hypothesis without timeline or mechanism evidence — escalate
to confirming mechanism before treating it as the cause.

**Pressure scenario** — The fastest containment also cuts off legitimate
traffic for unaffected users: does the harm trajectory justify that trade, or
is there a narrower containment that protects the same boundary?

### `maintain-working-method`

**Gates** — (1) Exception authority: confirm `use when`, `do not use when`,
and exception authority are explicit before a rule can override normal
judgment. (2) Guardrail expiry: confirm a temporary guardrail expires
automatically rather than becoming permanent by default.

**Escalation** — Default: require an observable behavior and reviewable
outcome, find contexts where the proposed rule creates friction or worse
results, and run a bounded trial with a rollback path. Information value
overrides the default when exceptions to a rule become frequent — escalate to
challenging the rule boundary itself before treating exceptions as
noncompliance.

**Pressure scenario** — A working-method rule has had three quiet exceptions
this month: is the rule still correct as stated, or does the boundary itself
need revising before a fourth exception happens?

### `govern-scorecards`

**Gates** — (1) Personal/privacy default: confirm personal evidence stays
private by default and that aggregation, sharing, or system-wide rule
creation requires explicit purpose, minimal disclosure, and authority. (2)
Non-compensable failure visibility: confirm aggregation never averages away a
subgroup harm or non-compensable failure.

**Escalation** — Default: determine whether each dimension has attributable,
decision-relevant evidence, separate observation from interpretation from
action, and let thresholds trigger evidence inspection rather than automatic
action. Information value overrides the default when a dimension repeatedly
fails to inform decisions — escalate to retiring it rather than continuing to
track it.

**Pressure scenario** — A scorecard dimension trends downward in aggregate
but is flat for every subgroup except one: does the aggregate trend justify
action, or does this need subgroup-level inspection before any rule changes?

### `track-components`

**Gates** — (1) Registry and mutation authority: confirm that registration,
retirement, cascade, or a schema change has the Work Object or owner authority
the ledger contract requires. (2) Finding-to-commitment boundary: confirm a
sweep queues signals only and never silently creates or changes Work Objects.

**Escalation** — Default: resolve locations and lineage, calculate grilling
debt from declared consequence, staleness, blast radius, and git drift, then
run the owning profile against applicable inline dimensions. Information value
overrides the default when a missing dependency edge or contrary outcome
evidence could invalidate a settled status — escalate to the smallest
evidence-gathering or owner decision before re-stamping the entry.

**Pressure scenario** — A high-blast-radius component is settled and inside its
cooldown, but a dependent declares a contract change: does the cascade reopen
it before any ordinary debt ranking, and is the declared edge sufficient?
