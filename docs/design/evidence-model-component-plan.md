# Evidence Model — Component Plan

Grilling Session 7 output. Scope: the evidence ledger implementation,
provenance lanes, structural fields, mutation integrity, and the
identification/linking of evidence and decision entries. Full session
ledger, including the turn-by-turn evidence trail behind every finding
below, is preserved at
`docs/design/grilling-session-7-evidence-model.md`.

## 1. Current-state findings (file paths)

- `references/EVIDENCE-MODEL.md:8-14` documents a 5-lane provenance
  taxonomy (Lived, Source, System, Inference, Decision) and a structured
  Work Object entry format (`**Provenance**:`, `**Claim**:`, `**Source**:`,
  `**Confidence**:`, `**Corroboration**:`, lines 26-36).
- `docs/adr/0016-evidence-ledger-uses-inline-provenance-tags-not-structured-fields.md`
  already declared that structured-field block dead — "never adopted in
  any real Work Object" — and named the real convention as inline tags:
  `[decision]`, `[system]`, `[inference]`, `[gap]`, `[testimony]`. It also
  stated `EVIDENCE-MODEL.md` "must be rewritten... has not been performed
  yet" (line 11). That rewrite is a real, standing gap this session closes.
- Grep across `.work-studio/objects/**` (15 real Work Objects): tag
  frequency is `[system]` 162, `[decision]` 115, `[inference]` 18, `[gap]`
  12, `[testimony]` 1, `[lived]` 1, `[source]` **0**.
- `references/AGREEMENT-LOOP.md:96-111` defines a second, more complete
  taxonomy — `[system]`, `[decision]`, `[memory]`, `[testimony]`,
  `[inference]`, `[gap]` — and is referenced by 14/14 core skills
  (`skills/core/*/SKILL.md`), versus `EVIDENCE-MODEL.md`'s 8/14. Six core
  skills, including `conduct-work-object` (the skill that actually owns
  Work Object persistence), reference Agreement Loop but never
  Evidence Model at all.
- `references/AGREEMENT-LOOP.md:108-110` — "Never present inference, stale
  documentation, or remembered context as current system fact" — is an
  existing, locatable laundering-guard sentence that matches real risk
  (inference/memory/stale-docs bleeding into `[system]`), unlike
  `EVIDENCE-MODEL.md:22`'s "[source] vs. [inference]" framing, which
  protects a lane with zero real instances.
- `.work-studio/objects/2026/07/2026-07-20-001-...md:146-183` — real
  Evidence ledger entry shape: `- <ISO8601 timestamp> — [tag] <free
  text>`. No entry ID, no structured fields.
- `.work-studio/objects/2026/07/2026-07-20-001-...md:210-255` — the
  separate `## Decisions and revisit triggers` section already carries
  real structured fields per decision: `**Branch chosen**`, `**Riskiest
  assumption**`, `**Authorization**`, `**Alternatives considered**`,
  `**Rationale**` (itself inline-tagged), `**Confidence**`, `**Actor**`,
  `**Revisit trigger**`. `**Authorization**` alone appears in 9 of 15 real
  Work Objects, always in this section, never in the Evidence ledger.
- `docs/adr/0017-work-object-history-is-append-only.md:13` — append-only
  protection applies to History only; its own text names the Evidence
  ledger, Decisions section, and frontmatter as sections that "may be
  edited or corrected." **The interim enforcement script this ADR
  describes does not exist anywhere in the repo** — confirmed by grep
  across `tools/*.py` and `tests/*.py` for any append-only/history-diff
  check. ADR 0017 describes a planned mechanism, not a built one.
- `docs/adr/0015-...md:3` specifies gates checking "verification evidence
  with `result: pass`" and a deployment authority record "with a `scope`
  field" — field-value language that matches the Decisions section's real
  shape, not the Evidence ledger's tag+prose shape, but the ADR never
  names which section its gates read.
- Redaction language (`docs/adr/0001`, `references/SHARED-PROTOCOL.md:48`,
  `docs/personal-institution-work-studio-protocol-spec.md:53`) governs
  only the Evidence Bridge — the Personal Institution → Work Object
  crossing point. No mechanism redacts a `[system]` entry's raw command
  output before it lands in a Work Object body.
- "Portable... across repositories" (this session's own charter framing)
  has no referent anywhere in the corpus. Every real "portable" mention
  (`README.md:13`, `docs/work-studio-planning-session-2026-07-15.md:12`)
  describes skill-code portability across Codex/Claude Code/GitHub
  Copilot adapters, not Work Object export.
- No entry-level ID convention exists anywhere. `2026-07-20-001-...md`'s
  Evidence ledger has three separate bullets stamped the identical
  timestamp (`2026-07-20T03:52:31+08:00`) — timestamp-as-identifier
  already fails empirically in production data.
- `docs/design/shared-protocols-component-plan.md:110-111` (Session 6,
  accepted) pinned a constitution invariant to `EVIDENCE-MODEL.md:22` —
  now dropped by this session (Decision 1) and requires a follow-up edit
  to that accepted artifact (see §6, migration step 6).

## 2. Contradictions and risks

1. **Canonical doc disagreed with its own superseding ADR.**
   `EVIDENCE-MODEL.md` documented a 5-lane taxonomy and dead structured
   fields that `docs/adr/0016` had already declared wrong, with the
   rewrite never performed. Resolved by Decision 2/3.
2. **Two competing tag taxonomies, unreconciled.** `EVIDENCE-MODEL.md`'s 5
   lanes and `AGREEMENT-LOOP.md`'s 6 tags never referenced each other.
   Real practice matched Agreement Loop far more closely. Resolved by
   Decision 2.
3. **A constitution invariant was grounded in wording, not referent.**
   Session 6 pinned "never launder inference as source evidence" by
   line-checksum, which protects exact wording but not whether the
   sentence's underlying concept (`[source]`) is real. It wasn't — 0 real
   instances. Resolved by Decision 1 (sentence dropped, not re-pinned to
   a new sentence this session).
4. **ADR 0015's gate spec cannot be evaluated against ADR 0016's canonical
   format.** Gates were specified to check structured field values;
   real Evidence ledger entries have no fields, only a tag and prose. This
   was a real implementability gap, not just a documentation gap — no
   gate in ADR 0015 could be mechanically evaluated as written. Resolved
   by Decision 4 (gates read the Decisions section, which already has the
   needed fields) — **but ADR 0015's text itself still needs a clarifying
   edit** to name that section explicitly (deferred to migration, not yet
   written).
5. **Making Decisions the gate read-target moved an unsolved risk, it
   didn't solve one.** ADR 0017 exempts the Decisions section from
   append-only protection exactly as it exempts the Evidence ledger.
   Routing gates to Decisions without also protecting Decisions would
   have made a freely-editable section load-bearing for enforcement.
   Resolved by Decision 5.
6. **Decision Rationales restate Evidence ledger claims without a link.**
   Real `**Rationale**` fields embed inline-tagged claims (e.g.
   `**Rationale**: [system] The fixture passes...`) that read as
   summaries of a fuller Evidence ledger entry. Protecting the Decision
   text alone leaves the summarized source free to drift underneath it.
   Resolved by Decision 8 (Evidence ledger gets the same protection) —
   but note this protects entries from *drifting*, not from being
   *un-linkable*: nothing formally connects a Rationale to the specific
   Evidence entry it drew from (see Deferred Decisions).
7. **Timestamp collisions are a real, observed defect, not a hypothetical
   one.** Three Evidence ledger bullets in one real Work Object share an
   identical second-precision timestamp. Any future gate or human citing
   "the entry timestamped X" cannot resolve to one entry today. Resolved
   by Decision 7 (enforce uniqueness; no new ID field).
8. **The append-only interim script ADR 0017 describes does not exist.**
   This was assumed mid-session to be an existing mechanism being
   "extended." It is not built. This changes the migration's actual first
   step from a config change to new tooling (see §6).
9. **Redaction and cross-repository portability were charter assumptions
   with no grounding.** Neither was fabricated into a decision this
   session — both are named explicitly as deferred, not solved, to avoid
   inventing requirements the corpus doesn't support.

## 3. Accepted decisions

1. Drop the constitution sentence "never launder inference as source
   evidence" (was pinned to `EVIDENCE-MODEL.md:22`). Do not carry it
   forward or replace it with synthesized prose this session.
2. Retire `EVIDENCE-MODEL.md`'s provenance-lane content. Adopt
   `AGREEMENT-LOOP.md:96-111`'s taxonomy and its laundering-guard sentence
   (line 108-110) as the single canonical source.
3. Do not delete `EVIDENCE-MODEL.md`. Rewrite it thin, scoped only to how
   ledger entries attach to a *persisted Work Object* specifically (its
   one piece of unique scope), deferring to `AGREEMENT-LOOP.md` by name
   for tag definitions rather than restating them.
4. Do not add structured fields to the Evidence ledger. Correct
   `docs/adr/0015` to name the `## Decisions and revisit triggers` section
   explicitly as what its gates check, rather than adding new structure
   anywhere.
5. Do not make the whole Decisions section append-only in the blanket
   History sense. Extend the append-only interim mechanism to protect
   individual Decision entries once written (append-to-revise, not
   section freeze) — formalizing the append-new-entry pattern real
   practice already follows.
6. Leave the `[system]`-entry redaction gap (raw command/file output with
   no privacy tier) open for a future session; no stated-boundary text is
   authored now, consistent with not building for unobserved incidents.
7. Do not introduce a new entry-level ID field. Enforce unique
   whole-second timestamps per entry within a Work Object as the
   identifier mechanism instead.
8. Extend the append-only mechanism a third time to cover the full
   Evidence ledger (not just Decisions and History). Correction happens
   by appending a new entry in all three sections, never by editing an
   existing one.

## 4. Target component boundary

- **Changed**: `references/EVIDENCE-MODEL.md` — rewritten thin; keeps only
  the Work-Object-attachment scope (how a persisted Work Object's Evidence
  ledger relates to the tags), removes the 5-lane taxonomy and the
  structured-field block, adds an explicit deferral to
  `AGREEMENT-LOOP.md` for tag definitions.
- **Changed**: `references/AGREEMENT-LOOP.md` — becomes the sole source of
  the provenance tag taxonomy and the laundering-guard sentence. No
  structural change to its own content required by this session's
  decisions, but it becomes the target of external references that used
  to point at Evidence Model.
- **Changed**: `docs/design/shared-protocols-component-plan.md` (Session 6,
  already accepted) — the constitution entry pinned to
  `EVIDENCE-MODEL.md:22` must be removed. This is a real edit to a
  previously-accepted artifact, not just this session's own ledger.
- **Changed**: `docs/adr/0015-...md` — add explicit language naming
  `## Decisions and revisit triggers` as the section its five prerequisite
  gates read, replacing the current ambiguous "evidence" wording.
- **Changed**: `docs/adr/0016-...md` — update to record that the
  `EVIDENCE-MODEL.md` rewrite (deferred in that ADR, never performed) is
  now complete, or supersede it with a short follow-up ADR (mirroring the
  ADR-0013/ADR-0021 pattern already used in this repo).
- **Changed**: `docs/adr/0017-...md` — needs a follow-up ADR (or direct
  amendment) narrowing its stated scope from "History only" to "History,
  Decisions, and Evidence ledger," all governed by the same
  append-to-revise mechanism.
- **New**: an append-only verification script (does not exist today —
  ADR 0017 describes it, nothing implements it). Must check, for a given
  Work Object, that no existing text in History, Decisions, or the
  Evidence ledger changed relative to the last-committed version; new
  appended entries pass.
- **New**: a timestamp-uniqueness check, most naturally the same script —
  fails if any two entries (in any of the three sections, or across them)
  in one Work Object share an identical timestamp.

## 5. Recommended architecture

One taxonomy, one enforcement mechanism, applied uniformly to three
sections:

1. **Taxonomy**: `AGREEMENT-LOOP.md` is canonical for provenance tags and
   the laundering guard. `EVIDENCE-MODEL.md` becomes a thin satellite
   describing only Work-Object-specific attachment, not a competing
   definition.
2. **Structure**: no new structured fields anywhere. The Evidence ledger
   stays tag+prose (matches capture-time reality, per ADR 0016's already-
   correct finding). The Decisions section keeps its already-real
   structured fields (`Authorization`, `Confidence`, `Actor`, `Revisit
   trigger`) and becomes the sole gate read-target, stated explicitly in
   ADR 0015.
3. **Integrity**: one append-only verification mechanism, applied to all
   three body sections that carry a permanent record (History, Decisions,
   Evidence ledger) rather than History alone. Correction is always
   append-a-new-entry, never edit-in-place. This is the same mechanism
   ADR 0017 already proposed for History — this plan only widens its
   scope and, critically, actually builds it, since it does not exist yet.
4. **Identity**: no new ID field. Entry timestamps are the de facto
   identifier; the fix is enforcing their uniqueness, not adding a
   parallel numbering system that requires writer bookkeeping.
5. **Explicitly out of scope for this plan**: redaction of raw `[system]`
   evidence content, and any Work-Object export/cross-repository
   portability mechanism. Both are named gaps, deliberately left
   unaddressed rather than solved with invented requirements.

## 6. Migration steps

1. Rewrite `references/EVIDENCE-MODEL.md` to its thin, Work-Object-scoped
   form (Decision 3); remove the 5-lane taxonomy and structured-field
   block; add an explicit pointer to `AGREEMENT-LOOP.md` for tag
   definitions.
2. Remove the constitution entry in
   `docs/design/shared-protocols-component-plan.md` that pins
   `EVIDENCE-MODEL.md:22` (Decision 1); do not replace it with a new
   pinned sentence this session.
3. Edit `docs/adr/0015-...md` to name `## Decisions and revisit triggers`
   explicitly as the section its five gates read (Decision 4).
4. Write a follow-up ADR (or direct amendment) to `docs/adr/0017-...md`
   narrowing/widening its scope statement to cover History, Decisions,
   and the Evidence ledger uniformly under one append-to-revise rule
   (Decisions 5 and 8).
5. Update `docs/adr/0016-...md` to record that the `EVIDENCE-MODEL.md`
   rewrite it deferred is now complete (or supersede it with a short
   follow-up ADR, mirroring the ADR-0013/ADR-0021 precedent already used
   in this repo).
6. Build the append-only verification script (does not exist yet):
   diff each of the three sections against the last-committed version;
   fail on any changed or removed existing text; pass on new appended
   entries. Include the timestamp-uniqueness check in the same pass.
7. Regenerate adapters if `EVIDENCE-MODEL.md`'s content change affects the
   generated `references/` output for any of the 8 skills that carry it
   (`tools/generate-adapters.py`).
8. Run the new script against all 15 real Work Objects as a baseline —
   expect it to pass cleanly (no known corruption), establishing the
   starting baseline the diff check will compare future changes against.

## 7. Tests and evidence required

- New test: hand-edit an existing entry's text in a scratch-copy Work
  Object's History, Decisions, and Evidence ledger sections in turn;
  confirm the script fails loudly for each. Then append a new entry in
  each section and confirm the script still passes — proving append
  is distinguished from edit, not just that "any change" is blocked.
- New test: construct a scratch Work Object with two entries sharing an
  identical timestamp; confirm the uniqueness check fails; bump one by a
  whole second and confirm it passes.
- New test/manual check: regenerate adapters after the `EVIDENCE-MODEL.md`
  rewrite; confirm the 8 skills that reference it still build without
  broken content, and confirm no skill's prose still describes the
  retired 5-lane taxonomy as canonical.
- Manual verification: grep all 15 real Work Objects post-migration for
  any remaining `[source]`- or `[lived]`-style reliance in skill prose
  (not the historical ledger entries themselves, which are not rewritten
  retroactively) to confirm nothing still authors against the retired
  taxonomy going forward.
- Re-run `tests/test_shared_protocol.py` and
  `tools/verify-conformance.py --check` unchanged — confirm this plan's
  changes don't regress the existing cross-package or structural checks.

## 8. Deferred decisions

- Disposition of the `[system]`-entry redaction gap (raw command/file
  output with no privacy tier, no boundary text). Left open per Decision
  6 — revisit only if a real incident or concrete need surfaces.
- Whether Decision Rationale entries should carry an explicit link
  (`supersedes`-style or otherwise) to the specific Evidence ledger
  entry(ies) they summarize. The append-only fix (Decision 8) stops
  drift but does not add a citation mechanism — entries remain connected
  only by prose proximity and adjacent timestamps.
- `[memory]`'s status in `AGREEMENT-LOOP.md`'s taxonomy: it has zero real
  instances, same as the retired `[source]`, but this session did not
  examine whether `[memory]` names a real-but-rare concept (session-local
  preference tracking) worth keeping, versus a second dead lane worth
  flagging in a future session.
- Whether the "portable... across repositories" framing should be
  corrected in future session charters, since this session found it
  ungrounded. Not resolved — noted as a charter-writing observation, not
  a repository decision.
- Whether `EVIDENCE-MODEL.md`'s rewrite (migration step 1) needs its own
  formal follow-up ADR the way ADR 0013's narrowing produced ADR 0021, or
  whether amending ADR 0016 directly is sufficient. Left to the
  implementer to decide when the rewrite actually happens.

## 9. Smallest tracer bullet

Prove the one genuinely new mechanism — a three-section append-only +
uniqueness check that does not exist today — on the smallest real case
before wiring it into any gate or CI path:

1. Copy one small, closed real Work Object
   (`.work-studio/objects/2026/07/2026-07-15-002-confirm-native-codex-creation.md`
   or similarly small) into a scratch fixture.
2. Write a ~40-line standalone script that diffs History, Decisions, and
   Evidence ledger sections against a saved baseline copy, flags any
   changed/removed existing line, and flags any duplicate timestamp
   within or across the three sections.
3. Run it green against the untouched fixture.
4. Hand-edit one existing Evidence ledger bullet's text — confirm the
   script fails loudly. Revert; hand-edit one existing Decision entry's
   `**Authorization**` value — confirm it fails loudly. Revert; append a
   brand-new entry to each section with a fresh timestamp — confirm the
   script still passes.
5. Duplicate an existing timestamp on a new entry — confirm the
   uniqueness check fails loudly; correct it — confirm it passes.
6. Only after this round-trip is proven on one object, extend the check
   to run across all 15 real Work Objects as the baseline (migration step
   8), and only then consider wiring it into `tools/verify-conformance.py`
   or a pre-commit path.

This isolates the one piece of genuinely new infrastructure (three-section
diff-based integrity checking) from the more mechanical parts of this plan
(the `EVIDENCE-MODEL.md` rewrite, the ADR text edits), so a failure in the
new mechanism is caught before any gate or generated adapter depends on it.
