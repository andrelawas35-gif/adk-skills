# Grilling Session 7 — Evidence Model (ledger, in progress)

Ephemeral session ledger. Not a Work Object. Finalized component plan will
replace/extend this file when the session is explicitly ended.

## Session ledger

### Observed (repository evidence, file:line)

- `references/EVIDENCE-MODEL.md:8-14` — canonical doc defines 5 provenance
  lanes: Lived Evidence, Source Evidence, System Evidence, Inference,
  Decision — with a structured Work Object entry format (`**Provenance**:`,
  `**Claim**:`, `**Source**:`, `**Confidence**:`, `**Corroboration**:`,
  `EVIDENCE-MODEL.md:26-36`).
- `docs/adr/0016-evidence-ledger-uses-inline-provenance-tags-not-structured-fields.md`
  — declares the structured-field block "dead documentation... never adopted
  in any real Work Object," confirms real usage is inline tags
  (`[decision]`, `[system]`, `[inference]`, `[gap]`, `[testimony]`), and
  states `EVIDENCE-MODEL.md` "must be rewritten... deferred... has not been
  performed yet" (ADR 0016:11).
- Grep across `.work-studio/objects/**`: tag frequency in real Evidence
  ledgers — `[system]` 162, `[decision]` 115, `[inference]` 18, `[gap]` 12,
  `[testimony]` 1, `[lived]` 1, `[source]` **0**.
- `.work-studio/objects/2026/07/2026-07-20-001-...md:146-183` — real Evidence
  ledger entry shape: `- <ISO8601 timestamp> — [tag] <free-text sentence(s)>`.
  No entry ID, no structured fields, no explicit link to a Decision or
  History entry by identifier.
- `docs/adr/0017-work-object-history-is-append-only.md:13` — append-only
  applies to History only; explicitly states it "does not apply to... the
  Evidence ledger, all of which may be edited or corrected."
- `docs/adr/0015-...:3` — the `release` gate is specified as requiring
  "verification evidence with `result: pass`" and a deployment authority
  record "with a `scope` field" — i.e., gates are specified to check
  structured field values on evidence entries.
- `docs/design/shared-protocols-constitution.md:110-111` (Session 6 output,
  accepted) — constitution invariant "never launder inference as source
  evidence" is pinned by line-checksum to `EVIDENCE-MODEL.md:22`, i.e. to a
  file ADR 0016 already flagged as containing dead/superseded lane
  documentation not yet rewritten.
- No `[source]`-tagged entry exists anywhere in `.work-studio/objects/**`.

### Claimed (documentation assertions, not verified against behavior)

- `EVIDENCE-MODEL.md:18` — "Every factual claim must carry a provenance
  marker" (rule stated, not mechanically enforced anywhere in the repo).
- `EVIDENCE-MODEL.md:22` — "Do not launder inference as source evidence"
  (rule references a `[source]` lane that has zero real-world usage).
- ADR 0015 — gates "check evidence field values structurally... because
  evidence semantics are a human and model judgment, not a deterministic
  check" (aspirational; no field-value structure exists in the inline-tag
  convention ADR 0016 confirmed as canonical).

### Inferred (not yet accepted as decision)

- The constitution sentence accepted in Session 6 ("never launder inference
  as source evidence") is pinned to a lane taxonomy (`[source]`) that real
  Work Objects never use — the sentence may be citing a provenance
  distinction that does not exist in practice, only in unrewritten
  documentation.
- ADR 0015's gate mechanism ("checks evidence field values structurally") is
  currently unimplementable against ADR 0016's inline-tag format, because
  inline tags carry a type marker and free text, not named fields like
  `result:` or `scope:`.

### Decided (this session)

1. **[decision]** The constitution sentence "never launder inference as
   source evidence" (pinned to `EVIDENCE-MODEL.md:22`) is dropped. It must
   be re-grounded in real usage rather than carried forward or replaced by
   synthesized prose. — accepted by user, this session.
2. **[decision]** `EVIDENCE-MODEL.md`'s provenance-lane content is retired
   in favor of `AGREEMENT-LOOP.md:96-111`'s taxonomy and laundering-guard
   sentence, as the single canonical source. — accepted by user, this
   session.
3. **[decision]** `EVIDENCE-MODEL.md` is not deleted. It is rewritten thin,
   scoped only to how ledger entries attach to a persisted Work Object
   (the "In the Work Object" content it uniquely carries), deferring to
   `AGREEMENT-LOOP.md` by name for tag definitions rather than restating
   them. — accepted by user, this session.

### Newly observed — zero structural fields exist under any tag

- Sampled `[testimony]`, `[gap]`, `[inference]` entries across real Work
  Objects: none carry a confidence marker, stated uncertainty, or
  citation/source field — grep for "confiden|uncertain|probability|likely|
  source:" inside those entries returns nothing.
- Sampled `[system]` entries: command output, file paths, and test counts
  appear, but only as inline prose narrative — never as a separate,
  parseable field (no `command:`, `exit_status:`, `file:` key anywhere).
- Sampled `[decision]` entries: state the choice in prose ("The learner
  writes the implementation and owns the plan") but name no explicit
  authority/actor field distinct from the shared ledger timestamp and
  surrounding narrative voice.
- This confirms, for all five real tags, that every one of the Session 7
  charter's per-lane structural pressure-tests (does `[source]`/`[system]`
  require a citation or command reference as a *field*; does `[inference]`
  require stated uncertainty as a *field*; does `[decision]` require an
  authority/timestamp/scope as a *field*) currently fails — the tag is the
  only structure; everything else is unconstrained free text.
- **Correction to the above** — the structured-field rigor the charter is
  looking for is NOT absent from the Work Object, it just doesn't live in
  the Evidence ledger. `.work-studio/objects/2026/07/2026-07-20-001-...md:210-255`
  — the `## Decisions and revisit triggers` section already carries real
  structured fields per decision: `**Branch chosen**`, `**Riskiest
  assumption**`, `**Authorization**`, `**Alternatives considered**`,
  `**Rationale**` (itself inline-tagged, e.g. `**Rationale**: [system]
  ...`), `**Confidence**: medium-high`, `**Actor**: human`, `**Revisit
  trigger**`. Grep confirms `**Authorization**` alone appears in 9 of 15
  real Work Objects, always inside this section, never inside the Evidence
  ledger.
- This means ADR 0016's "structured fields were dead documentation, never
  adopted" verdict is true **only for the Evidence ledger section**. The
  Decisions section independently reinvented the same rigor (authority,
  confidence, rationale) under different field names, in a different
  section, without citing `EVIDENCE-MODEL.md` at all.

### Newly observed, in response to the "re-ground" instruction

- `references/AGREEMENT-LOOP.md:100-105` — a **second, competing** tag
  taxonomy exists, distinct from `EVIDENCE-MODEL.md`'s 5 lanes: `[system]`,
  `[decision]`, `[memory]`, `[testimony]`, `[inference]`, `[gap]` (6 tags,
  including one — `[memory]` — with **zero** real occurrences, same as
  `[source]`).
- `references/AGREEMENT-LOOP.md` is referenced by 14/14 core skills
  (confirmed by grep on `skills/core/*/SKILL.md`); `EVIDENCE-MODEL.md` is
  referenced by 8/14. Agreement Loop is the more universally-loaded file.
- `references/AGREEMENT-LOOP.md:108-110` already contains an existing,
  locatable sentence that functions as a laundering guard: "Never present
  inference, stale documentation, or remembered context as current system
  fact." This targets the boundary real practice actually stresses
  ([inference]/[memory]/stale-docs vs. [system]), not the
  [source]-vs-[inference] boundary `EVIDENCE-MODEL.md:22` names — a
  boundary with zero real [source] entries to protect.
- Real-practice tag set (`[system]` 162, `[decision]` 115, `[inference]`
  18, `[gap]` 12, `[testimony]` 1, `[lived]` 1, `[source]` 0, `[memory]` 0)
  matches Agreement Loop's taxonomy far more closely than Evidence Model's
  — 5 of 6 Agreement Loop tags have real instances; only 3 of 5 Evidence
  Model lanes do (`system`, `inference`, `decision`; `lived` has 1 instance,
  `source` has 0).

### Open

- What are the real structural fields per lane (if any), given lanes
  documented in `EVIDENCE-MODEL.md` don't match lanes observed in practice?
- Does a provenance label alone (a bracketed tag before free text) provide
  meaningful epistemic protection, or does it depend entirely on model
  compliance at write time?
- How, if at all, can evidence entries be referenced by ID and linked to
  Decisions/History/transitions, given none currently carry identifiers?
- Given ADR 0017 permits Evidence ledger entries to be "edited or
  corrected," what protects an entry's provenance tag or content from
  silent revision after other work (a Decision, a gate check) has already
  relied on it?

### Contradictions

1. `EVIDENCE-MODEL.md` (canonical reference, still live in
   `SHARED_REFERENCES` and constitution-pinned) documents a 5-lane taxonomy
   and a structured-field entry format that ADR 0016 already declared dead
   and scheduled for rewrite — a rewrite that has not happened. The doc
   currently disagrees with the ADR that supersedes it, and both are
   simultaneously "canonical."
2. ADR 0015 specifies gates that check structured field values
   (`result: pass`, `type: decision`, `scope`) on evidence entries. ADR
   0016's confirmed-canonical inline-tag format has no named fields —
   only a provenance tag and free text. As specified, no gate in ADR 0015
   can currently be evaluated deterministically against a real Evidence
   ledger entry.
3. Session 6 pinned a constitution invariant to `EVIDENCE-MODEL.md:22`,
   which asserts a `[source]` vs. `[inference]` distinction that has zero
   occurrences of `[source]` across every real Work Object. The
   line-checksum pinning mechanism protects the sentence's *wording* from
   drift, but not its *grounding* — the sentence can stay byte-identical
   while referring to a lane nobody uses.

## 1. Current evidence representation

Evidence lives only inside a Work Object body, as a flat, append-in-practice
(but not append-only-enforced) Markdown list under `## Evidence ledger`:
`- <timestamp> — [tag] <free text>`. Six tags are observed in real use
(`system`, `decision`, `inference`, `gap`, `testimony`, `lived`); the
documented model names a different five (`lived`, `source`, `system`,
`inference`, `decision`). There is no sidecar file, no YAML, no generated
section, no entry ID, and no explicit link field to a Decision or History
entry — linkage, if it exists, is implicit in shared timestamps and prose
proximity within the same file.

## 2. Unenforced provenance rules

- "Every factual claim must carry a provenance marker" — no linter or test
  checks this; it depends on the writing agent's compliance.
- "Do not launder inference as source evidence" — unenforceable as written;
  the `[source]` tag it presumes is not part of real practice.
- ADR 0015's structural gate checks (`result: pass`, `scope` field) — no
  code path in the repo currently parses an Evidence ledger entry into
  fields; `tools/verify-conformance.py` checks generated-adapter structure,
  not Work Object evidence content.
- Append-only protection — explicitly does *not* apply to Evidence ledger
  entries (ADR 0017:13), unlike History.

## 3. Evidence mutations that threaten integrity

- Entries may be edited or corrected post-hoc with no diff-based check
  (the ADR 0017 interim script covers History only).
- No entry ID means an edited entry cannot be distinguished from an
  originally-correct one by any later reader or gate — there is nothing to
  redirect a citation to.
- No mechanism observed for redaction, deletion tracking, or safe export;
  ADR 0017 states Evidence "may be edited or corrected" with no described
  boundary on what correction means (fixing a typo vs. changing a claim vs.
  changing a provenance tag).

## 4. Grounded question

(see recommendation below, logged per user request before the question was
answered)

## Recommendation (design preference — NOT yet accepted)

**Retire `EVIDENCE-MODEL.md`'s provenance-lane content. Treat
`AGREEMENT-LOOP.md:96-111` as the single canonical source for the tag
taxonomy and the laundering-guard sentence.**

Grounds for this, in order of weight:

1. `skills/core/conduct-work-object/SKILL.md` — the one skill that actually
   owns Work Object persistence, including the Evidence ledger — references
   `AGREEMENT-LOOP.md` but **not** `EVIDENCE-MODEL.md` at all. The skill
   responsible for writing the artifact never loads the file that claims to
   define its provenance model. `track-components`, `deploy-with-recovery`,
   `pressure-test-decision`, `verify-release-evidence`, and
   `grilling-session` are in the same position — Agreement-Loop-only.
2. Real tag distribution matches Agreement Loop's 6-tag list far more
   closely than Evidence Model's 5-lane list: 5 of Agreement Loop's 6 tags
   have real instances (`system`, `decision`, `inference`, `gap`,
   `testimony`); only `system`/`inference`/`decision` are solidly used from
   Evidence Model's list (`lived` has 1 instance, `source` has 0).
   Agreement Loop's `[memory]` also has 0 real instances, but it names a
   scope (session-local, user-approved reusable preference) that is
   plausibly real and just rare — not a lane whose underlying concept is
   absent from the system, unlike `[source]`.
3. Agreement Loop already contains an existing, locatable laundering-guard
   sentence (`AGREEMENT-LOOP.md:108-110`) that targets the boundary real
   entries actually risk crossing — inference, stale docs, or remembered
   context being presented as current system fact — rather than the
   `[source]`-vs-`[inference]` boundary Evidence Model names, which
   protects a lane nobody writes to.
4. This mirrors the constitution-file precedent Session 6 already
   established: one canonical source per invariant, referenced by name, not
   restated with drift risk. Keeping both files as competing definitions of
   the same taxonomy is the same "docstring vs. implementation" shape
   Session 6 flagged as a contradiction elsewhere in this repo.

**What I am not recommending yet**: a specific replacement wording for a
constitution sentence, or a specific fate for `EVIDENCE-MODEL.md` as a file
(delete vs. rewrite as a thin Work-Object-specific note that defers to
Agreement Loop for tag definitions). Both require a decision, not an
inference, and the file-fate question in particular needs the same
"what does each file uniquely provide" scrutiny before anything is deleted
— `EVIDENCE-MODEL.md:24-36`'s "In the Work Object" framing was the one
piece of scope Agreement Loop doesn't obviously cover (how ledger entries
attach to a persisted Work Object specifically, vs. a live grilling
session), and that scope question hasn't been pressure-tested yet.

## Grounded question (pending)

Given the recommendation above: do you accept retiring Evidence Model's
lane taxonomy in favor of Agreement Loop's, or is there a reason to keep
`EVIDENCE-MODEL.md` defining a competing list — and if you accept retiring
it, what happens to the file itself (deleted, or rewritten to a thin
Work-Object-scoped note deferring to Agreement Loop)?

**Answered**: rewrite (see Decided #3).

## Recommendation 2 (design preference — NOT yet accepted)

**Do not add structured fields to the Evidence ledger. Point ADR 0015's
gate checks at the `## Decisions and revisit triggers` section's existing
structured fields instead, and answer the "does a tag alone protect
anything" question as: no — the tag is a classification and audit surface,
not proof; real structural protection already exists in this Work Object,
just misfiled relative to where ADR 0015 looks for it.**

Grounds:

1. ADR 0016 killed structured fields in the Evidence ledger because real
   producers, in the flow of a grilling/build/verify session, could not
   produce `Confidence`/`Corroboration` at capture time. That finding is
   correct and should stand — re-imposing fields there repeats a change
   already tried and reverted in practice.
2. But the Decisions section shows producers *can* and *do* produce that
   exact rigor — `Authorization`, `Confidence`, `Actor`, `Revisit trigger`
   — when the claim is a decision, not a running observation. The
   difference is not producer capability; it's that decisions are made
   once, deliberately, at a natural pause point, while Evidence ledger
   entries are logged continuously mid-flow. Structure fits the former,
   not the latter.
3. ADR 0015 specifies gates checking "verification evidence with `result:
   pass`" and "a deployment authority record with a `scope` field" — this
   already sounds like the Decisions section's field shape
   (`Authorization`, `Actor`), not the Evidence ledger's tag+prose shape.
   The gate design was likely already written with the Decisions section
   in mind and just used the word "evidence" loosely to mean "the Work
   Object's evidentiary record" in general, not literally the `## Evidence
   ledger` heading. Session 7 should get this pinned down explicitly rather
   than left ambiguous, since a future CLI implementer will otherwise guess.
4. Net effect: no new structure needed anywhere. The fix is a
   clarifying/scoping edit to ADR 0015 (name the section its gates actually
   read), not a new mechanism.

**What I am not recommending**: any lint or enforcement addition this
session (e.g., requiring `[system]` entries to name a concrete artifact
inline) — real practice already does this informally and near-universally;
formalizing it would be adding enforcement for a problem with no observed
instances, which the charter's own contradiction-criteria warns against
("add abstractions without a demonstrated recurring problem").

## Grounded question (pending)

Do you accept Recommendation 2 — leave the Evidence ledger as unstructured
tag+prose, and fix ADR 0015 to name the `## Decisions and revisit
triggers` section explicitly as what its gates check, rather than adding
any new structure?

**Answered**: accepted.

### Decided (this session), continued

4. **[decision]** Recommendation 2 accepted: the Evidence ledger stays
   unstructured tag+prose; ADR 0015 is to be corrected to name the
   `## Decisions and revisit triggers` section explicitly as the gate
   read-target, rather than introducing new structure anywhere. — accepted
   by user, this session.

### Newly observed — the mutation-integrity risk transfers, not resolves

- `docs/adr/0017-work-object-history-is-append-only.md:13` — append-only
  protection applies to History **only**. Its own text: "does not apply
  to... frontmatter fields, body sections other than History, **or the
  Evidence ledger**, all of which may be edited or corrected." The
  Decisions and revisit triggers section is a body section other than
  History — it is explicitly named as freely editable/correctable by this
  same sentence.
- Decision #4 just accepted routes ADR 0015's gate checks to this same
  freely-editable section. The mutation-integrity gap identified earlier
  (Contradiction 3 / "Evidence mutations that threaten integrity") has not
  been closed by relocating the read-target from Evidence ledger to
  Decisions — it has moved wholesale to a section with the exact same
  absence of protection, and that section is now explicitly load-bearing
  for gate enforcement, which the Evidence ledger never actually was.
- Real practice already treats Decision revision as append, not edit:
  `2026-07-20-001-...md` shows 30 separate `### <timestamp> — <title>`
  decision headers over one Work Object's life, including explicit
  revision entries — "Reaffirmed clean-boundary hold," "Reaffirm
  clean-boundary hold pending attribution," "Decision recorded: require
  clean integration boundary" — each a *new* timestamped entry, none of
  which edits a prior entry's text in place. `supersedes` is the
  established repo-wide vocabulary for "this replaces that" (used for
  Workflow Candidates, scorecards) though it is not yet applied
  entry-to-entry within a single Work Object's Decisions section.

### Newly observed — no ID scheme exists, and the fallback (timestamp) is
not even unique

- Grep across all real Work Objects for any entry-level ID convention
  (`EV-`, `DEC-`, `#123`, markdown anchors) returns nothing. The only
  identifying information any Evidence, Decision, or History entry carries
  is its ISO8601 timestamp header/bullet.
- The Work Object itself has a stable ID (`id: "2026-07-20-001"` in
  frontmatter) — this exists at the object level only, not the entry
  level.
- Timestamps are **not unique even within one entry list**:
  `2026-07-20-001-...md`'s Evidence ledger has three separate bullets all
  stamped `2026-07-20T03:52:31+08:00` (the initial handoff-decision,
  handoff-direction, and audit-testimony entries). "See the entry
  timestamped X" does not resolve to one entry even inside a single
  section, let alone across the Evidence ledger, Decisions section, and
  History.
- This directly compounds the risk from Decisions #4/#5: gates and future
  readers have no way to cite *which* Decision or Evidence entry justified
  a transition unambiguously — not because linking is unimplemented, but
  because there is no addressable unit to link to in the first place.

## Recommendation 3 (design preference — NOT yet accepted)

**Do not make the whole Decisions and revisit triggers section append-only
in the blanket History sense — that would forbid the legitimate revision
the section is designed for. Instead, extend ADR 0017's existing
diff-based interim script so it also protects individual Decision entries
once written, and formalize the append-new-entry-to-revise pattern that
real practice already follows.**

Grounds:

1. History is append-only because it records a sequence that must never be
   rewritten — there is no legitimate reason to edit a past transition.
   Decisions are different by design: the `Revisit trigger` field exists
   specifically so a decision *can* be reconsidered. Blanket immutability
   would fight the section's own purpose.
2. But real practice already resolves this tension without needing new
   design: revision happens by **appending a new, later-timestamped
   decision entry** ("Reaffirmed clean-boundary hold pending attribution"),
   never by editing the original entry's text. This is the same
   append-in-practice-but-unenforced shape the Evidence ledger has — and
   it is exactly the shape ADR 0017 formalized for History. The fix is not
   invention; it is recognizing the same pattern already holds here and
   giving it the same protection.
3. ADR 0017's interim script is already a generic mechanism (diff a
   section against its last-committed version, fail if existing text
   changed, allow new appended text). Extending its scope to the Decisions
   section is a configuration change to an existing tool, not new
   infrastructure — consistent with this session's finding that most
   integrity gaps here are scoping/documentation problems, not missing
   mechanisms.
4. This directly protects the specific risk Decision #4 introduced: once a
   gate has read `Authorization`/`Confidence`/`scope` from a decision
   entry to permit a `build`/`release`/`close` transition, that entry's
   text is what future readers must be able to trust unchanged. A later
   revision creates a new entry (optionally referencing the superseded one
   by timestamp), it does not rewrite the one the gate already consumed.

**What I am not recommending**: adopting `supersedes` as a required
explicit link between decision entries this session — real practice
doesn't do this yet even though the vocabulary exists elsewhere in the
repo, and requiring it would be new authored convention, not something
grounded in observed practice. Flagging it as a natural follow-on, not
deciding it here.

## Grounded question (pending)

Do you accept Recommendation 3 — extend ADR 0017's interim append-only
script to also cover the Decisions and revisit triggers section (protecting
individual entries once written, not freezing the whole section), rather
than leaving Decision records exactly as mutable as the Evidence ledger
they were just made the gate read-target instead of?

**Answered**: accepted.

### Decided (this session), continued

5. **[decision]** Recommendation 3 accepted: ADR 0017's interim append-only
   script is extended to protect individual Decision entries once written
   (append-to-revise, not blanket section freeze), rather than leaving
   Decision records as mutable as the Evidence ledger they now gate against.
   — accepted by user, this session.

### Newly observed — redaction is a boundary concept, not a ledger concept

- Redaction language in this repo (`docs/adr/0001-...md`,
  `references/SHARED-PROTOCOL.md:48`, `docs/personal-institution-work-studio-protocol-spec.md:53`)
  attaches specifically to the **Evidence Bridge** — the one approved
  crossing point from the private Personal Institution layer into a Work
  Object. It describes redacting personal material *before* it becomes a
  `[testimony]`/`[lived]` entry, not redacting entries already inside a
  Work Object's Evidence ledger.
- Separately, `fixtures/slice-2-verify-release-evidence.md` Scenario 4
  requires the `verify-release-evidence` skill to "redact sensitive values
  from the report" — but this is the skill's output *report*, generated
  from evidence, not a rule about what may be written into the Evidence
  ledger entry itself.
- No mechanism observed anywhere that redacts a `[system]` entry's raw
  content before it is written into the ledger. Real `[system]` entries
  (see earlier samples) paste literal command output, file paths, and byte
  counts directly. If a command's output contained a secret or credential,
  nothing in the current design stops it from landing verbatim in a
  Work Object body — which, unlike Personal Institution records, has no
  stated privacy tier of its own.

### Decided (this session), continued

6. **[decision]** The absence of a `[system]`-entry redaction boundary is
   left open for a future session; no stated-boundary text is authored now,
   matching the repo's own bias against building for unobserved incidents.
   — accepted by user, this session.

### Newly observed — the session's stated main question ("portable across
repositories") has no grounding

- Grep for "portab" across non-adapter docs finds exactly two hits:
  `README.md:13` ("Skills are authored once in a portable canonical
  core") and `docs/work-studio-planning-session-2026-07-15.md:12`
  ("portable personal operating system"). Both describe **skill code**
  portability across Codex/Claude Code/GitHub Copilot adapters — a
  generator/checksum mechanism that already exists and is tested.
- Neither hit, nor anything else found this session, describes a Work
  Object (and therefore its Evidence ledger) being exported from one
  repository/workspace to another. No fixture, ADR, or skill references
  moving a Work Object across repos.
- This session's own charter framed the central question as evidence
  structure "remaining usable by humans and portable across
  repositories" — that second clause currently has zero grounding in the
  corpus. It matches the `/grill-with-docs` red flag explicitly named in
  this session's brief: "claim portability without proving semantic
  equivalence." The claim should not be carried forward as if it were an
  existing requirement; it is, at most, an aspiration with no current
  referent.

### Newly observed — no ID scheme exists, and the fallback (timestamp) is
not even unique (see also the earlier note under Recommendation 3's
lead-in, same finding)

- No entry-level ID convention exists anywhere (`EV-`, `DEC-`, anchors).
  The Work Object has a stable ID at the object level
  (`id: "2026-07-20-001"`); entries below that have only a timestamp.
- Timestamps collide in real data: `2026-07-20-001-...md`'s Evidence
  ledger has three separate bullets stamped the identical second
  (`2026-07-20T03:52:31+08:00`). Timestamp-as-identifier does not resolve
  to one entry even within a single section.
- This compounds Decisions #4/#5 directly: a gate or reader has no way to
  unambiguously cite which entry satisfied a prerequisite.

## Recommendation 4 (design preference — NOT yet accepted)

**Do not introduce a new entry-level ID field (`EV-1`, `DEC-1`). Enforce
that entry timestamps are unique within a Work Object instead — the
identifier scheme was clearly already intended (every entry already
carries one), it's just not enforced.**

Grounds:

1. A sequence-number ID requires the writing agent to track and increment
   a counter correctly, per section, mid-session, while also composing
   prose. That is bookkeeping overhead at capture time — the exact failure
   mode ADR 0016 already documented and rejected for structured fields
   (`Confidence`/`Corroboration` never got produced because they demand
   formality the producer doesn't have in flow). A sequence counter is the
   same shape of demand: correct only if the writer does extra
   out-of-band accounting on every entry.
2. Timestamp uniqueness costs nothing new. Every entry already has a
   timestamp; the actual defect is that several bullets written in the
   same turn get stamped with the same captured "current time" instead of
   incrementing. The intended design — timestamp as de facto ID — already
   exists; it just isn't enforced. Fixing the enforcement gap is smaller
   than adding a parallel ID system that could itself drift out of sync
   with the timestamps everyone already reads.
3. This reuses the same lightweight-verification-script pattern already
   accepted twice this session (append-only checks for History and
   Decisions) rather than adding a fourth kind of mechanism: a check that
   fails if any two entries in the same Work Object body share a
   timestamp.
4. A new ID scheme is exactly the kind of abstraction the session brief
   warns against adding "without a demonstrated recurring problem." The
   demonstrated problem here is collision, not absence-of-an-ID-format —
   the fix should match the problem's actual shape.

**What I am not recommending**: sub-second timestamp precision as the
uniqueness mechanism. Real entries are read as prose by humans; a
`2026-07-20T03:52:31.482+08:00`-style timestamp is harder to scan than
`2026-07-20T03:52:32+08:00` bumped by a whole second. Whole-second
increments preserve current formatting and readability.

## Grounded question (pending)

Do you accept Recommendation 4 — no new ID field, just enforce unique
whole-second timestamps per entry within a Work Object — or is a real
sequence-number ID still warranted despite the bookkeeping-overhead risk?

**Answered**: accepted.

### Decided (this session), continued

7. **[decision]** No new entry-level ID field. Enforce unique whole-second
   timestamps per entry within a Work Object as the identifier mechanism.
   — accepted by user, this session.

### Newly observed — the Evidence ledger's own editability is still
unresolved, and Decisions cite it directly

- Real Decision entries embed inline-tagged claims inside their own
  `**Rationale**` field — e.g. `**Rationale**: [system] The fixture passes
  its focused and full checks...` (`2026-07-20-001-...md:240`). This is
  effectively a **restatement** of an Evidence ledger-style observation,
  inline inside a now-append-protected Decision entry.
- Decisions #4/#5 protect the Decision entry's own text once written. They
  do not protect the *separate* Evidence ledger entry the Rationale is
  presumably summarizing (if a fuller version exists there) — ADR 0017
  still permits that source entry to be "edited or corrected" with no
  diff-based check.
- This means a Decision's Rationale can become permanently frozen (good,
  per #5) while the Evidence entry it drew from silently drifts
  underneath it — an auditor could read a protected Rationale that no
  longer matches the (edited) Evidence ledger entry it summarized, with no
  signal that a mismatch occurred.

## Recommendation 5 (design preference)

**Extend the same append-only interim script to the full Evidence ledger
too — narrowing ADR 0017's exemption a third time this session. Rationale
restatement inside a Decision entry is not sufficient on its own.**

Grounds:

1. Unlike structured fields (rejected in ADR 0016 because they demand
   *more content at write time*), append-only protection asks for nothing
   extra when writing an entry — it only restricts rewriting after the
   fact. The producer-burden objection that killed structured fields does
   not apply here, the same distinction already used to justify
   Recommendation 3 for Decisions.
2. ADR 0017's own stated reason for protecting History — "an audit trail
   with gaps or altered entries is not an audit trail" — applies with
   equal force to the Evidence ledger. Decisions cite and restate selected
   Evidence claims, but the full ledger remains the primary record anyone
   would consult to check whether a cited claim was accurate at the time.
   If that record can drift silently, the Decision's frozen Rationale
   becomes unverifiable against its own stated source, not just untethered
   from it.
3. Legitimate correction (a misread command, a typo) is not blocked by
   this — it uses the identical append-a-new-entry pattern already
   established for Decisions and already observed in real Evidence ledger
   usage (later entries note dependency/fixture status changes rather
   than editing earlier ones).
4. This is a configuration change to the same interim script already
   extended once this session (to Decisions), not new infrastructure —
   consistent with the session's overall finding that most integrity gaps
   here are scoping gaps in an existing mechanism, not missing tooling.

Accepted per user instruction ("yes do recommended").

### Decided (this session), continued

8. **[decision]** ADR 0017's append-only interim script is extended a
   third time to cover the full Evidence ledger (not just Decisions and
   History). Correction happens by appending a new entry, never by
   editing an existing one, in all three sections. — accepted by user,
   this session.
