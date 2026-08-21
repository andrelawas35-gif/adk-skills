"""Phase 7 Hypothesis exit-evidence tracer bullet (WO 2026-08-21-004, Decision 2).

Tests the riskiest remaining assumption behind the build plan's Phase 7 exit
evidence (`references/architecture/langgraph-local-runtime-integrated-build-plan.md:370`):
that a `hypothesis.stateful.RuleBasedStateMachine`, driving the existing
self-contained tracer graph from `test_phase7_tracer.py` through random
sequences of gate/retry/replay actions, can exercise that graph without
finding an invariant violation the four hand-written cases in that file did
not already cover.

Self-contained by design (rollback = delete this file and the `test`
dependency-group entry in `pyproject.toml`; no other file touched): imports
the unmodified `build_tracer_graph`, `TracerRetryable`, and `_journal_count`
helpers from `test_phase7_tracer.py`, plus the unmodified
`runtime.graph.claim_idempotency_receipt`. Does not wire into the real
Phase 6/research graphs, does not implement the three missing real gate
types (restricted handling, high consequence, release authority), does not
add `hypothesis` as a production dependency.

Run under the uv-managed Python 3.11 environment:
    uv run --group test python -m unittest runtime.tests.test_phase7_hypothesis -v
"""

import shutil
import sqlite3
import tempfile
import unittest
from pathlib import Path

from hypothesis import settings
from hypothesis.stateful import Bundle, RuleBasedStateMachine, initialize, rule
from langgraph.types import Command

from runtime.tests.test_phase7_tracer import _journal_count, build_tracer_graph


class TracerGateRetryReplayMachine(RuleBasedStateMachine):
    """Drives the unmodified tracer graph through gate/retry/replay sequences.

    One state machine instance == one thread == one run of the 3-node graph
    (authority_gate -> risky_effect -> record_success). Rules model the six
    action types the build plan names for Phase 7 exit evidence: pause
    (graph.invoke to the gate interrupt), resume (Command(resume=...)),
    retry (fail_until drives risky_effect's internal retry loop), reject,
    replay (invoking again after a terminal state), and compensate
    (risky_effect_error_handler's failure-journal write, exercised when
    retries exhaust).
    """

    def __init__(self):
        super().__init__()
        self.tmp = Path(tempfile.mkdtemp())
        self.thread_id = "hyp-t"
        self.max_attempts = 3
        self.graph, self.conn = build_tracer_graph(
            self.tmp / "ckpt.sqlite", max_attempts=self.max_attempts
        )
        self.cfg = {"configurable": {"thread_id": self.thread_id}}
        self.idempotency_db = self.tmp / "journal.sqlite"
        self.gate_reached = False
        self.terminal = False
        self.terminal_outcome = None

    @initialize()
    def reach_gate(self):
        result = self.graph.invoke(
            {
                "work_object_id": "2026-08-21-004",
                "thread_id": self.thread_id,
                "gate_reason": "hypothesis_tracer",
                "attempt_marker": str(self.tmp / f"{self.thread_id}-attempts.txt"),
                "idempotency_db": str(self.idempotency_db),
                "fail_until": self.fail_until,
            },
            config=self.cfg,
        )
        assert "__interrupt__" in result
        self.gate_reached = True

    @rule()
    def reject_gate(self):
        if not self.gate_reached or self.terminal:
            return
        result = self.graph.invoke(Command(resume=False), config=self.cfg)
        self.terminal = True
        self.terminal_outcome = result.get("outcome")
        # Invariant: a rejected gate never runs the effect or journals anything.
        assert not (self.tmp / f"{self.thread_id}-attempts.txt").exists()
        assert _journal_count(self.idempotency_db, self.thread_id, "risky_effect:succeeded") == 0
        assert _journal_count(self.idempotency_db, self.thread_id, "risky_effect:failed") == 0

    @rule()
    def approve_gate(self):
        if not self.gate_reached or self.terminal:
            return
        result = self.graph.invoke(Command(resume=True), config=self.cfg)
        self.terminal = True
        self.terminal_outcome = result.get("outcome")
        succeeded = _journal_count(
            self.idempotency_db, self.thread_id, "risky_effect:succeeded"
        )
        failed = _journal_count(self.idempotency_db, self.thread_id, "risky_effect:failed")
        # Invariant: never both succeeded and failed for the same identity.
        assert not (succeeded and failed)
        # Invariant: exactly one terminal journal entry once resolved.
        assert succeeded + failed == 1
        assert self.terminal_outcome in ("succeeded", "failed")
        marker = self.tmp / f"{self.thread_id}-attempts.txt"
        if marker.exists():
            attempts = int(marker.read_text(encoding="utf-8"))
            # Invariant: attempt count never exceeds the configured budget.
            assert attempts <= self.max_attempts

    @rule()
    def replay_after_terminal(self):
        if not self.terminal:
            return
        before_succeeded = _journal_count(
            self.idempotency_db, self.thread_id, "risky_effect:succeeded"
        )
        before_failed = _journal_count(self.idempotency_db, self.thread_id, "risky_effect:failed")
        # Replaying a terminal thread must not re-run the node or re-journal.
        result = self.graph.invoke(None, config=self.cfg)
        after_succeeded = _journal_count(
            self.idempotency_db, self.thread_id, "risky_effect:succeeded"
        )
        after_failed = _journal_count(self.idempotency_db, self.thread_id, "risky_effect:failed")
        assert after_succeeded == before_succeeded
        assert after_failed == before_failed
        assert result.get("outcome") == self.terminal_outcome

    def teardown(self):
        self.conn.close()
        shutil.rmtree(self.tmp, ignore_errors=True)


def _make_machine(fail_until: int):
    class _Bound(TracerGateRetryReplayMachine):
        pass

    _Bound.fail_until = fail_until
    return _Bound


# Two fixed instances rather than a Hypothesis-generated fail_until: the
# graph is compiled once per instance (expensive), and reject/approve/replay
# already generate the interesting sequences. fail_until=1 exercises
# retry-then-succeed (within the 3-attempt budget); fail_until=99 exercises
# exhaust-retries (always fails, budget-exceeding).
TestRetrySucceeds = _make_machine(fail_until=1).TestCase
TestRetryExhausts = _make_machine(fail_until=99).TestCase

for _cls in (TestRetrySucceeds, TestRetryExhausts):
    _cls.settings = settings(max_examples=25, stateful_step_count=6, deadline=None)


if __name__ == "__main__":
    unittest.main()
