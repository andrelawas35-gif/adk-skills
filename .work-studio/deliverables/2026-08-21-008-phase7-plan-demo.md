# Implementation Plan (synthesis-only draft) — Phase 7 continuation
Source: `2026-08-21-004`, Decisions 1-3 + History, no content added beyond what is already recorded there.

## Scope inherited, not re-decided
Compose native `retry_policy`/`timeout`/`error_handler`, an effect journal extending
`claim_idempotency_receipt`, and a generalized `authority_gate(reason)` node — no
dedicated recovery subgraph, one-effect-per-node discipline. (Decision 1, inherited
from ADR 0026; authority carries forward, not re-sought here.)

## What shipped
1. `authority_gate(reason)` — implemented, used for the `direction` gate
   (`runtime/graph.py:724`) and a separate research-fetch gate (`:935`).
2. `RetryPolicy` + `error_handler` — wired on `record_note`.
3. Effect journal status/attempt tracking — resolved by correction, not new code:
   status is already carried via `effect_name` suffixing, attempt-count via a
   marker file. No schema change was needed or made. (Corrects an earlier framing
   of this item as a pending SQLite migration — that framing did not survive
   Decision 2's tracer bullet and should not appear in a forward-looking plan.)
4. Hypothesis `RuleBasedStateMachine` exit-evidence suite — built
   (`test_phase7_hypothesis.py`), `hypothesis` added as a test-only dependency,
   3 tests executed, zero counterexamples found. (Decision 2.)
5. Irreversible-effects-without-authority — checked by code inspection across
   all three real graphs; holds today. One caveat carried forward below.

## What's explicitly not shipped, and why
- **Three of four director-gate types** (restricted handling, high consequence,
  release authority): blocked, not merely unbuilt. No node in any real graph
  performs an action these would gate. Release/deployment concerns first become
  concrete in Phase 8, which does not exist yet. (Decision 3.) The mechanism
  itself is proven and ready the moment a real call site exists — this is a
  target problem, not a capability problem.
- **Empirical proof of the rejection path**: `research_fetch_source`'s
  unreachability-without-approval claim rests on reading the code
  (`if not state.get("approved")`), not on an executed test exercising
  `Command(resume=False)` and asserting `fetch_url` was never called. Recorded
  as an accepted, revisitable gap at close, not an unknown.

## Next steps, as actually recorded (not invented)
- Revisit the three deferred gate types when Phase 8 work begins, or when any
  Work Object introduces a real restricted-content / high-consequence /
  release effect — at that point, apply the already-proven `authority_gate`
  pattern directly.
- The rejection-path gap remains open at closure; no committed next step exists
  for it beyond the option the director declined ("one more small test") when
  choosing to close instead.

---
*Everything above traces to Decisions 1–3 or a History entry in `2026-08-21-004`.
Nothing here is proposed, forecast, or invented beyond what those records state.*
