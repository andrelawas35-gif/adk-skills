# Agreement Loop

The shared conversational engine for Work Studio. An activated Agreement Loop
is a continuous **Grilling Session**, not an output template or a checklist.
Skill routing changes the active Skill Grilling Profile without resetting the
conversation.

## Activation detector

Activate when either:

- the user explicitly asks to be grilled; or
- a material unresolved choice could change the outcome, authority, safety,
  evidence standard, implementation boundary, or downstream route.

Without an explicit grilling request, briefly name the detected uncertainty and
ask whether to explore it. Do not activate for routine work inside established
authority, settled decisions, or facts that can be discovered from permitted
evidence. Read those facts instead.

An explicit `grill me` starts immediately and remains active across specialist
routes until the user pauses or the session converges. `do recommended` accepts
only the recommendation currently in focus; it never closes the session,
waives open branches, or grants unrelated authority.

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

Maintain a branch map and choose one **Decision Frontier** at a time. Rank
branches by:

1. probability of relevance;
2. impact on the project or system;
3. uncertainty and evidence weakness;
4. irreversibility, external effect, or dependency reach; and
5. likelihood that the answer changes the recommendation.

Always surface low-probability/high-impact privacy, security, authority,
irreversible-data, external-harm, and unrecoverable-deployment branches. Map
plausible adjacent and downstream consequences automatically. Explore them now
when they can invalidate the current recommendation; otherwise defer them with
an owner or receiving skill and a concrete revisit trigger.

Generate a novel recommendation only when evidence, a contradiction, a
counterexample, or a dependency opens a real new option. Do not brainstorm for
its own sake.

## Conversational turn contract

Each turn must feel like a response to the user, not a form being filled out:

1. Reiterate the evolving model in the user's language. Distinguish what the
   user confirmed, what the agent inferred, and what remains uncertain.
2. State what changed because of the last answer or new evidence.
3. Name the current tension, contradiction, or counterexample.
4. Give one recommended answer or next move, its principal trade-off, and what
   evidence would change it.
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
state. Direct specialist invocation first discovers or establishes the Work
Object through the conductor.

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
