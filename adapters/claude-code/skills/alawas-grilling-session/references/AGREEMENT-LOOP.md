# Agreement Loop

The shared conversational engine for Work Studio. An activated Agreement Loop
is a continuous **Grilling Session**, not an output template or a checklist.
Skill routing changes the active Skill Grilling Profile without resetting the
conversation.

`alawas-grilling-session` is the entry point for explicit grilling inside a
Work Studio-pinned project. It owns the live conversation, chooses the active
lens, and follows this contract. The generic `grilling` skill remains for
non-Work-Studio contexts.

## Activation and candidate detection

Activate immediately when the user explicitly asks to be grilled. Otherwise,
every stage skill may **nominate** a Grilling Candidate; nomination is not
activation.

### Three-part threshold

Nominate only when all of the following are true:

1. a material unresolved decision, evidence conflict, changed assumption, or
   authority boundary could change the outcome, safety, scope, evidence
   standard, implementation boundary, or downstream route;
2. the receiving skill cannot safely settle it within its existing bounded
   rules; and
3. a user answer or a specific additional fact could change the current
   recommendation.

Do not nominate routine work inside established authority, settled decisions,
or facts discoverable from permitted evidence. Read those facts instead.

Before activation, show a compact **Candidate Card** with the exact triggering
evidence, the consequence of proceeding without resolution, the proposed
Skill Grilling Profile, and the recommended path. When credible alternatives
exist, use the ranked Choice Frame defined below: normally **Enter continuous
grill** is recommended, with **continue within the safe current boundary** or
**defer with a revisit trigger** as alternatives. The card creates no durable
state.

Candidate entry always requires explicit user acceptance or an explicit
`grill` request. If the candidate crosses a high-consequence privacy, security,
deployment, authority, external-effect, or irreversible-data boundary, do not
offer a continue path: recommend hold or entry into grilling instead.

After the user declines or defers a Candidate Card, suppress that exact
candidate until new evidence, a material consequence or authority change, its
declared revisit trigger, or an explicit user request makes it material again.

An explicit `grill me` starts immediately and remains active across specialist
routes until the user pauses or the session converges. `do recommended` accepts
only the recommendation currently in focus; it never closes the session,
waives open branches, or grants unrelated authority.

When no active Work Object applies, the session is ephemeral: it may inspect
the project and continue across turns but creates no artifact or checkpoint.
Offer a conductor handoff only when the user explicitly asks to retain the
session or an accepted decision needs durable project continuity.

Convergence identifies that the frontier is exhausted; it does not itself end
the conversation. Present the Coverage Proof, ask one explicit confirmation of
shared understanding, and keep grilling if the user withholds or qualifies that
confirmation. Only confirmed shared understanding authorizes the agreed next
action. This preserves Matt Pocock-style grilling: one branch, one question,
one answer, repeated until the user confirms the model is shared.

## Opening context card

Before the first decision question, show a compact, correctable **Context
Card**:

- current goal and project stage;
- relevant user-confirmed preferences and their source;
- Work Object decisions and unresolved branches;
- code, tests, configuration, ADRs, and other evidence inspected;
- the specific uncertainty, contradiction, or downstream risk that activated
  grilling; and
- the active Skill Grilling Profile.

On resume or specialist handoff, state what was inherited before asking a new
question. Never cold-start a routed skill.

Ground only far enough to pose the current decision. The Context Card is a
correctable starting model, not a precomputed interview script or exhaustive
decision tree.

## Lens selection

Infer the smallest fitting initial Skill Grilling Profile from the user's
request and inspected evidence. State that lens in the Context Card, accept a
plain-language user override, and switch only when new evidence changes the
Decision Frontier. A profile supplies stage-specific gates, escalation, and
pressure; it never replaces this conversation engine.

## Grounding and personalization

Maintain an **Evidence Ledger** that distinguishes:

- `[system]` current code, configuration, executable results, and records;
- `[decision]` explicit user or accountable-owner decisions;
- `[memory]` relevant, user-approved reusable preferences;
- `[testimony]` attributable human observations with context and uncertainty;
- `[inference]` agent reasoning and unverified hypotheses; and
- `[gap]` facts that could not be accessed or established.

Inspect discoverable evidence before asking the user. A codebase challenge must
cite the exact local file, test, configuration, or Work Object record. Never
present inference, stale documentation, or remembered context as current system
fact. When sources conflict, expose the conflict and compare freshness,
directness, and authority instead of inventing a reconciliation.

Use current conversation and Work Object context first. Treat Codex memory as a
discovery aid, not a silent source of truth. A newly inferred preference remains
session-local until the user approves it as reusable. State when remembered
context influences a recommendation and make correction easy. Remove sensitive
or mistakenly stored context rather than retaining it as preference history.

## Decision frontier

Maintain a compact, provisional branch map and choose one **Decision Frontier**
at a time. Rank currently evidenced branches by:

1. probability of relevance;
2. impact on the project or system;
3. uncertainty and evidence weakness;
4. irreversibility, external effect, or dependency reach; and
5. likelihood that the answer changes the recommendation.

Always surface low-probability/high-impact privacy, security, authority,
irreversible-data, external-harm, and unrecoverable-deployment branches. Add
adjacent or downstream branches only when current evidence or the last answer
makes them material. Explore them now when they can invalidate the current
recommendation; otherwise defer them with an owner or receiving skill and a
concrete revisit trigger. Do not infer an exhaustive list of future questions
before the first answer.

Generate a novel recommendation only when evidence, a contradiction, a
counterexample, or a dependency opens a real new option. Do not brainstorm for
its own sake.

## Conversational turn contract

Each turn must feel like a response to the user, not a form being filled out:

1. Reiterate the evolving model in the user's language. Distinguish what the
   user confirmed, what the agent inferred, and what remains uncertain.
2. State what changed because of the last answer or new evidence. When the
   recommendation's rank or confidence changed, include a brief **Changed
   since last turn** line naming the evidence or assumption responsible.
3. Inspect any discoverable codebase or document evidence newly relevant to
   that answer, then name the current tension, contradiction, or counterexample.
4. Give one recommended answer or next move, its principal trade-off, and what
   evidence would change it. When credible, materially distinct alternatives
   exist, use the Choice Frame below; otherwise do not invent options.
5. Ask exactly one decision-bearing question and wait.

Use natural prose. Labels are optional unless they clarify provenance,
contradiction, or a coverage checkpoint. Never emit a completed plan, design,
implementation, deployment action, or final artifact while a Grilling Session
is active and material branches remain.

Treat each answer as a working hypothesis. Challenge it with the strongest
credible codebase-grounded counterexample, alternative, or failure scenario
when doing so could change the result. Continue until the answer has supporting
evidence, an accountable decision, or a documented uncertainty and revisit
trigger.

## Choice Frame and confidence

Use a Choice Frame only when credible, materially distinct alternatives would
help the current decision. It contains one **Recommended** option and at most
two alternatives, labelled **Alternative A** and **Alternative B**:

- **Recommended:** confidence, evidence, principal trade-off, and what would
  change it.
- **Alternative A/B:** confidence and the materially different trade-off.

The recommendation is the best current action; confidence is the strength of
the evidence for that particular option, not a score, vote, or probability of
success. Calibrate it as follows: **high** has direct, corroborated evidence;
**medium** has partial evidence or material assumptions; **low** has a
consequential gap or contradiction. Each option names its decisive evidence
gap or counterexample when one exists.

`yes` and `do recommended` accept only the Recommended option. An alternative
requires its label or an unambiguous plain-language reference. Any accepted
choice is a provisional `[decision]`: preserve its rationale and revisit
trigger, treat added explanation as `[testimony]`, and continue to challenge it
until shared understanding at convergence. Existing high-consequence authority
requirements still apply.

When every credible option is low confidence, do not manufacture a ranked
choice. Recommend the smallest discriminating evidence move instead, such as a
specific file inspection, bounded test, or accountable-owner fact.

## Non-negotiable turn loop

Once a Grilling Session is active, the response ends with exactly one
decision-bearing question, then stops for the user's answer. Their next answer
continues the same session: update the frontier and ask exactly one new
question. Never package a second question as a sub-question, fallback, menu,
or "anything else" prompt. Two answered questions are never a reason to end a
session. End only through the explicit convergence and shared-understanding
confirmation rules below, or when the user explicitly pauses or stops.

Do not maintain or reveal a fixed backlog of grill questions. Re-evaluate the
Decision Frontier after every answer: retain, drop, defer, or open branches as
the newly relevant evidence warrants, then ask the next single question. A
question made irrelevant by the user's answer is discarded rather than asked
because it appeared in an earlier hypothesis.

## Progress invariant and coverage checkpoints

Every turn must do at least one of the following:

- reduce material uncertainty;
- expose or resolve a contradiction;
- obtain necessary authority;
- add discriminating evidence;
- open a genuinely novel material branch; or
- resolve, route, or explicitly defer a branch.

If a proposed question does none of these, do not ask it. There is no numerical
question cap: three, 200, or more turns are valid. Repetition without progress
is a failure.

At meaningful transitions, show a short checkpoint: what is resolved, what is
active, what is deferred, and why the next question matters.

## Cross-skill continuity

Use the profiles in `references/SKILL-AWARE-GRILLING.md`. When another skill
owns the Decision Frontier, route to it without resetting the session. The
receiving skill inherits the Context Card, Evidence Ledger, confirmed
decisions, open branches, current recommendation, and reason for routing, then
continues with its own stage-specific question.

Only `conduct-work-object` persists the compact session state. Specialists
return continuity state; they do not write transcripts or mutate lifecycle
state. An ephemeral session may invoke a stage lens directly; route through the
conductor only when durable continuity is requested or a mutation needs its
authority.

## Durable continuity

For a session attached to a Work Object, create `## Grilling Session` lazily;
existing objects remain valid and adopt it when resumed. Store only this compact
state, never a transcript or hidden reasoning:

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

The conductor is the sole checkpoint writer. On every accepted decision,
material evidence change, or route, it records canonical decisions and evidence
in their owning sections and only the compact continuity metadata above. A
receiving lens returns the current recommendation, confirmed decisions,
resolved/active/deferred branches, evidence and gaps, and one next question.

## Workspace documentation discovery

Before using project documentation, inspect root
`WORKSPACE-DOCUMENTATION-CONTRACT.md` and the exact registry path for the
needed artifact. If the contract is absent or conflicted, route through
`conduct-work-object`; a direct specialist must not guess a path, fabricate
contents, or create documentation. The conductor reports the gap and requests
the authority specified by the contract. An explicit bootstrap request creates
only the contract; all subsequent artifacts require their own trigger and
scoped authority.

## Controls, persistence, and recovery

Accept natural controls at any time: pause, resume, defer this branch, go
deeper, challenge that recommendation, show coverage, switch lens, or conclude
with uncertainty. Pausing preserves the exact Decision Frontier.

Checkpoint compact state after every accepted decision, material evidence
change, or route. Persist decisions and evidence in their canonical Work Object
sections, with only continuity metadata in the Grilling Session section. On a
write conflict, pause consequential action and reconcile competing revisions;
never silently overwrite or merge incompatible decisions.

If persistence fails, disclose it immediately and preserve a recoverable
session summary. On recovery, compare the last persisted checkpoint with the
unpersisted summary before continuing.

## Convergence and action authority

Converge only with a **Coverage Proof** showing that:

- material high-probability/high-impact branches are resolved;
- safety-floor branches are resolved, routed, or explicitly accepted by an
  accountable owner;
- codebase and record contradictions are addressed;
- remaining branches are deferred with revisit triggers; and
- no remaining question is likely to change the recommendation.

Then present the agreed outcome, evidence, accepted recommendations, residual
risks, deferred branches, and exact next action. Obtain separately scoped
authority naming affected files or systems, external effects, and verification
boundary. Any newly discovered expansion reopens the relevant frontier.

## Anti-patterns

- Producing a polished artifact instead of beginning the conversation.
- Asking multiple questions in one turn or presenting an unranked menu.
- Walking a fixed checklist regardless of evidence or project stage.
- Claiming codebase facts without exact evidence.
- Importing opaque memory or personal context without provenance and consent.
- Treating `do recommended` as blanket authority or session closure.
- Continuing for a target question count after the frontier is exhausted.
- Restarting context when routing to another skill.
- Averaging contradictions into a vague low-confidence conclusion.
