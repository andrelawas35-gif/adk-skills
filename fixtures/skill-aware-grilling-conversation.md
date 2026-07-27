# Skill-Aware Grilling Behavioral Fixture

These scenarios validate observable conversation behavior. They do not
prescribe hidden reasoning or exact prose.

## Scenario 1 — Explicit grilling starts a conversation, not an artifact

**Given** an active Work Object in `design` and the user says, “Use
design-tracer-bullet and grill me.”

**Then** the agent:

1. shows a correctable Context Card with goal, stage, approved preferences,
   inspected evidence, open branches, and the design profile;
2. states why grilling activated;
3. recommends one answer with a trade-off and change condition;
4. asks exactly one question and waits; and
5. does not emit a completed design, plan, or implementation.

## Scenario 2 — The next turn changes because of the answer

**Given** Scenario 1 and the user answers the question.

**Then** the agent distinguishes confirmed information, inference, and
uncertainty; states what changed; names the next tension or codebase-grounded
counterexample; recommends one answer; asks one new question; and waits.

**Prohibited outcome:** repeating the next item in a fixed coverage checklist.

## Scenario 3 — `do recommended` is narrow acceptance

**Given** an active Grilling Session with several open branches.

**When** the user says `do recommended`.

**Then** only the recommendation currently in focus becomes accepted. The
agent states what changed and selects the next Decision Frontier. It does not
close the session, waive other branches, persist an unrelated mutation, or
begin implementation.

## Scenario 4 — Codebase challenges require exact evidence

**Given** the user's intent conflicts with current code, tests, configuration,
or a Work Object decision.

**Then** the agent cites the exact local evidence, distinguishes current fact
from inference, explains the contradiction, recommends a route, and asks one
question. Inaccessible evidence is an explicit gap.

**Prohibited outcome:** “the code does X” without a file, check, configuration,
or record reference.

## Scenario 5 — Personalization is attributable and correctable

**Given** the agent uses a remembered preference such as recommendation-first,
deep one-question grilling.

**Then** the Context Card identifies it as approved memory, the user can
override it for the session, and a newly inferred preference remains local
until approved. A correction causes dependent recommendations to be
re-evaluated. Sensitive or mistaken memory is removed rather than preserved.

## Scenario 6 — Specialist routing preserves one conversation

**Given** the design profile discovers that verification owns the current
Decision Frontier.

**Then** routing to `verify-release-evidence` preserves the Context Card,
Evidence Ledger, confirmed decisions, branch map, and current recommendation.
The receiving skill states what it inherited and asks its own exactly one next
question. It does not cold-start or replay the transcript.

Apply the same continuity contract to all profiles:

- `turn-signal-into-work`
- `conduct-work-object`
- `pressure-test-decision`
- `design-tracer-bullet`
- `implement-bounded-change`
- `verify-release-evidence`
- `deploy-with-recovery`
- `review-outcome-and-adapt`
- `investigate-live-question`
- `diagnose-production-incident`
- `maintain-working-method`
- `govern-scorecards`
- `track-components`
- `audit-product-interface`
- `build-design-foundation`
- `model-user-flow`
- `define-interface-architecture`
- `apply-design-direction`
- `verify-design-implementation`

## Scenario 7 — Stage-specific challenge follows project reality

**Given** any active profile.

**Then** it inspects its named evidence, pursues the branch most likely to
change the recommendation, applies its own counterexamples and failure cases,
considers relevant adjacent stages, and routes or converges by its profile's
criteria. It does not ask generic “tell me more” questions when project
evidence supplies a sharper challenge.

## Scenario 8 — Routine work does not trigger ceremony

**Given** a settled, reversible, routine action inside existing authority and
no explicit grilling request.

**Then** the skill proceeds normally and may state why grilling is unnecessary.
It does not create a Grilling Session or ask questions whose answers cannot
change the recommendation.

## Scenario 9 — Probability coverage includes a safety floor

**Given** several plausible branches.

**Then** the agent ranks them by probability, impact, uncertainty,
irreversibility, and dependency reach. It always surfaces relevant privacy,
security, authority, irreversible-data, external-harm, and unrecoverable
deployment branches, even when their probability is low. Lower-value branches
are deferred with a receiving skill or owner and revisit trigger.

## Scenario 10 — Long loops have no cap and every turn progresses

**Given** a complex project with more than 200 material, novel, dependent
questions.

**Then** the session may exceed 200 turns. Every turn reduces uncertainty,
resolves a contradiction, obtains authority, adds discriminating evidence,
opens a material novel branch, or resolves/routes/defers one. It does not stop
because of a numerical limit and does not continue merely to reach a count.

## Scenario 10a — Two answers do not end the session

**Given** the agent has asked one question, received an answer, asked a second
question, and received its answer; material decision branches remain open.

**Then** it updates the same Grilling Session and asks exactly one third
decision-bearing question. It does not summarize, offer a pair of questions,
ask an "anything else" fallback, or declare the session complete merely
because two questions were answered.

## Scenario 10b — The frontier is discovered progressively

**Given** an explicit grilling request about a codebase decision.

**Then** the agent first inspects only the code and documents needed to pose
the highest-value initial question. After each answer, it inspects evidence
newly relevant to that answer, re-ranks the live Decision Frontier, discards
invalidated branches, and asks exactly one next question. It does not infer an
exhaustive list of grill questions at activation and drip-feed that fixed list.

## Scenario 11 — Convergence requires Coverage Proof and scoped authority

**Given** no remaining question is likely to change the recommendation.

**Then** the agent presents a Coverage Proof containing resolved, ruled-out,
and deferred branches; codebase contradictions; evidence gaps; residual risks;
and the exact next action. A separate confirmation names affected files or
systems, external effects, and verification boundary.

## Scenario 12 — Persistence, recovery, and concurrency stay honest

**Given** an accepted decision, material evidence change, or specialist route.

**Then** `conduct-work-object` checkpoints compact Grilling Session state in
the Work Object without transcripts. On failure, it compares the last persisted
checkpoint with the recoverable summary. On a concurrent revision, it pauses
consequential action and presents conflicting decisions and Decision Frontiers
for reconciliation; it never silently overwrites.

## Scenario 13 — Coverage Proof requires confirmation of shared understanding

**Given** a Grilling Session has a Coverage Proof.

**Then** the agent asks exactly one question for confirmation of shared
understanding. It does not conclude, implement, or treat `do recommended` as
session closure until the user explicitly confirms the model is shared.

## Scenario 14 — Canonical engine is the pinned-project entry point

**Given** the user says “grill me” in a Work Studio-pinned project without an
active Work Object.

**Then** `grilling-session` starts an ephemeral, codebase-grounded session,
infers and states a correctable initial lens, asks one question, and creates no
Work Object. It offers conductor persistence only when the user explicitly
asks to retain the session or an accepted decision needs durable continuity.

## Scenario 15 — Skills nominate, but never silently enter, grilling

**Given** a stage skill finds a material unresolved boundary that it cannot
safely settle within its bounded rules, and a user answer or specific fact
could change the recommendation.

**Then** it shows a Candidate Card with exact triggering evidence, consequence,
proposed profile, and ranked choices. It does not silently enter a Grilling
Session. A declined or deferred card stays suppressed until its revisit trigger
or material new evidence. A high-consequence card offers hold or entry rather
than a continue path. Once active, changed rank or confidence is named in a
Changed since last turn line; when all credible options are low confidence, the
recommendation is the smallest discriminating evidence move.
