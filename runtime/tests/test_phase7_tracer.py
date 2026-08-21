"""Phase 7 tracer bullet (WO 2026-08-17-015, Decision 2).

Tests the riskiest remaining assumption behind ADR 0026 (Branch B): that
langgraph's native retry_policy/error_handler, the existing effect journal
(claim_idempotency_receipt), and a generalized authority-gate interrupt()
pattern compose into one coherent path without a conflict that only appears
once they are actually wired together.

Self-contained by design (rollback = delete this file; no other file
touched): the 3-node graph (authority_gate -> risky_effect -> record_success)
is built entirely in this test module, using only the existing, unmodified
runtime.graph.claim_idempotency_receipt for the journal and
runtime.graph.build_checkpoint_serializer for the checkpointer -- both
imported, not altered. Does not wire into the real Phase 6/research graphs,
does not implement all four gate types, does not implement the multi-effect
node-granularity case (reasoned through in the decision record itself, not
retested here).

Run under the uv-managed Python 3.11 environment:
    uv run python -m unittest runtime.tests.test_phase7_tracer -v
"""

import sqlite3
import tempfile
import unittest
from pathlib import Path
from typing import Optional, TypedDict

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, RetryPolicy, interrupt

from runtime.graph import build_checkpoint_serializer, claim_idempotency_receipt


class TracerRetryable(Exception):
    """Raised by risky_effect while its configured failure budget remains."""


class TracerState(TypedDict, total=False):
    work_object_id: str
    thread_id: str
    gate_reason: str
    attempt_marker: str
    idempotency_db: str
    fail_until: int
    approved: Optional[bool]
    attempts: int
    effect_ran: bool
    outcome: str


def _effect_attempt(marker: Path, fail_until: int) -> int:
    """Increment and return the attempt count recorded at `marker`.

    Mirrors runtime.graph._phase6_crash_hook's marker-file convention: the
    node function itself is re-invoked by langgraph's retry loop with no
    state channel to carry an attempt counter between failed tries, so the
    counter lives in a file instead.
    """
    attempts = int(marker.read_text()) if marker.exists() else 0
    attempts += 1
    marker.write_text(str(attempts))
    if attempts <= fail_until:
        raise TracerRetryable(f"attempt {attempts} failed")
    return attempts


def authority_gate(state: dict) -> dict:
    """Pause for explicit approval; performs no effect itself."""
    approval = interrupt({"reason": state["gate_reason"], "ask": "approve?"})
    return {"approved": bool(approval)}


def _route_after_gate(state: dict) -> str:
    return "risky_effect" if state.get("approved") else END


def risky_effect(state: dict) -> dict:
    attempts = _effect_attempt(Path(state["attempt_marker"]), state["fail_until"])
    return {"attempts": attempts, "effect_ran": True}


def risky_effect_error_handler(state: dict) -> dict:
    """Fires once retries are exhausted; journals the failure, no effect claimed."""
    claim_idempotency_receipt(
        Path(state["idempotency_db"]),
        thread_id=state["thread_id"],
        work_object_id=state["work_object_id"],
        effect_name="risky_effect:failed",
    )
    return {"outcome": "failed"}


def record_success(state: dict) -> dict:
    claim_idempotency_receipt(
        Path(state["idempotency_db"]),
        thread_id=state["thread_id"],
        work_object_id=state["work_object_id"],
        effect_name="risky_effect:succeeded",
    )
    return {"outcome": "succeeded"}


def build_tracer_graph(checkpoint_db: Path, max_attempts: int):
    builder = StateGraph(TracerState)
    builder.add_node("authority_gate", authority_gate)
    builder.add_node(
        "risky_effect",
        risky_effect,
        retry_policy=RetryPolicy(max_attempts=max_attempts, retry_on=TracerRetryable),
        error_handler=risky_effect_error_handler,
    )
    builder.add_node("record_success", record_success)
    builder.add_edge(START, "authority_gate")
    builder.add_conditional_edges(
        "authority_gate", _route_after_gate, {"risky_effect": "risky_effect", END: END}
    )
    builder.add_edge("risky_effect", "record_success")
    builder.add_edge("record_success", END)
    conn = sqlite3.connect(str(checkpoint_db), check_same_thread=False)
    saver = SqliteSaver(conn, serde=build_checkpoint_serializer())
    return builder.compile(checkpointer=saver), conn


def _journal_count(idempotency_db: Path, thread_id: str, effect_name: str) -> int:
    if not idempotency_db.exists():
        return 0
    with sqlite3.connect(str(idempotency_db)) as conn:
        cur = conn.execute(
            "SELECT COUNT(*) FROM idempotency_receipts "
            "WHERE thread_id = ? AND effect_name = ?",
            (thread_id, effect_name),
        )
        return cur.fetchone()[0]


class Phase7TracerTests(unittest.TestCase):
    def _base_input(self, tmp: Path, thread_id: str, fail_until: int) -> dict:
        return {
            "work_object_id": "2026-08-17-015",
            "thread_id": thread_id,
            "gate_reason": "high_consequence",
            "attempt_marker": str(tmp / f"{thread_id}-attempts.txt"),
            "idempotency_db": str(tmp / "journal.sqlite"),
            "fail_until": fail_until,
        }

    def test_gate_reject_no_effect_no_journal(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            graph, conn = build_tracer_graph(tmp / "ckpt.sqlite", max_attempts=3)
            try:
                cfg = {"configurable": {"thread_id": "reject-t"}}
                graph.invoke(self._base_input(tmp, "reject-t", fail_until=0), config=cfg)
                result = graph.invoke(Command(resume=False), config=cfg)
                self.assertFalse(result.get("approved"))
                self.assertFalse((tmp / "reject-t-attempts.txt").exists())
                self.assertEqual(
                    0, _journal_count(tmp / "journal.sqlite", "reject-t", "risky_effect:succeeded")
                )
                self.assertEqual(
                    0, _journal_count(tmp / "journal.sqlite", "reject-t", "risky_effect:failed")
                )
            finally:
                conn.close()

    def test_gate_approve_retry_then_succeed_journals_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            graph, conn = build_tracer_graph(tmp / "ckpt.sqlite", max_attempts=3)
            try:
                cfg = {"configurable": {"thread_id": "succeed-t"}}
                # fail_until=2: fails attempts 1-2, succeeds on attempt 3 (within budget).
                graph.invoke(self._base_input(tmp, "succeed-t", fail_until=2), config=cfg)
                result = graph.invoke(Command(resume=True), config=cfg)
                self.assertEqual("succeeded", result.get("outcome"))
                self.assertEqual(3, result.get("attempts"))
                self.assertEqual(
                    1, _journal_count(tmp / "journal.sqlite", "succeed-t", "risky_effect:succeeded")
                )
                self.assertEqual(
                    0, _journal_count(tmp / "journal.sqlite", "succeed-t", "risky_effect:failed")
                )
            finally:
                conn.close()

    def test_gate_approve_retries_exhausted_error_handler_journals_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            graph, conn = build_tracer_graph(tmp / "ckpt.sqlite", max_attempts=2)
            try:
                cfg = {"configurable": {"thread_id": "exhaust-t"}}
                # fail_until=99: always fails; max_attempts=2 exhausts quickly.
                graph.invoke(self._base_input(tmp, "exhaust-t", fail_until=99), config=cfg)
                result = graph.invoke(Command(resume=True), config=cfg)
                self.assertEqual("failed", result.get("outcome"))
                self.assertEqual(
                    1, _journal_count(tmp / "journal.sqlite", "exhaust-t", "risky_effect:failed")
                )
                self.assertEqual(
                    0, _journal_count(tmp / "journal.sqlite", "exhaust-t", "risky_effect:succeeded")
                )
            finally:
                conn.close()

    def test_journal_claim_is_idempotent_on_replay(self):
        """Composition-risk check: a second claim for the same identity never
        double-records, proving the journal side of the composition holds
        even if a thread were somehow re-driven after reaching a terminal
        state."""
        with tempfile.TemporaryDirectory() as tmp:
            idempotency_db = Path(tmp) / "journal.sqlite"
            first = claim_idempotency_receipt(
                idempotency_db,
                thread_id="replay-t",
                work_object_id="2026-08-17-015",
                effect_name="risky_effect:succeeded",
            )
            second = claim_idempotency_receipt(
                idempotency_db,
                thread_id="replay-t",
                work_object_id="2026-08-17-015",
                effect_name="risky_effect:succeeded",
            )
            self.assertTrue(first)
            self.assertFalse(second)
            self.assertEqual(
                1, _journal_count(idempotency_db, "replay-t", "risky_effect:succeeded")
            )


if __name__ == "__main__":
    unittest.main()
