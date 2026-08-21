"""Phase 7 error-class discrimination (WO 2026-08-17-016, Decision 4).

Tests the riskiest assumption behind Decision 3/4: that RetryableError and
TerminalError, as separate sibling classes (not one subclassing the other),
make RetryPolicy(retry_on=RetryableError) retry RetryableError up to
max_attempts while TerminalError propagates immediately with zero retries.
The library mechanics (isinstance-based matching in
langgraph.pregel._retry._should_retry_on) were confirmed by direct source
inspection during design; this test proves *our* class definitions actually
produce that behavior when executed, which inspection alone cannot catch
(e.g. an accidental subclass relationship would defeat the discrimination
silently).

Self-contained by design (rollback = delete this file; no other file
touched other than the additive class declarations in runtime/graph.py):
the one-node graph is built entirely in this test module. Does not wire
into any real Phase 6/research node -- RetryableError/TerminalError remain
undeployed primitives after this test, per Decision 3/4's explicit
non-goal.

Run under the uv-managed Python 3.11 environment:
    uv run python -m unittest runtime.tests.test_phase7_error_classes -v
"""

import tempfile
import unittest
from pathlib import Path

from langgraph.graph import END, START, StateGraph
from langgraph.types import RetryPolicy
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from typing import TypedDict

from runtime.graph import (
    AuthorityRequiredError,
    RetryableError,
    TerminalError,
    build_checkpoint_serializer,
)


class _AttemptState(TypedDict, total=False):
    thread_id: str
    fail_mode: str  # "retryable" or "terminal"
    fail_until: int
    marker_path: str
    outcome: str


def _record_attempt(marker: Path) -> int:
    """Append one line to marker and return the new attempt count."""
    marker.parent.mkdir(parents=True, exist_ok=True)
    with marker.open("a", encoding="utf-8") as fh:
        fh.write("attempt\n")
    return len(marker.read_text(encoding="utf-8").splitlines())


def _risky_node(state: _AttemptState) -> dict:
    marker = Path(state["marker_path"])
    attempt = _record_attempt(marker)
    if state["fail_mode"] == "retryable" and attempt <= state["fail_until"]:
        raise RetryableError(f"attempt {attempt} failed, retryable")
    if state["fail_mode"] == "terminal":
        raise TerminalError(f"attempt {attempt} failed, terminal")
    return {"outcome": "succeeded"}


def _build_graph(checkpoint_db: Path, max_attempts: int):
    conn = sqlite3.connect(str(checkpoint_db), check_same_thread=False)
    saver = SqliteSaver(conn, serde=build_checkpoint_serializer())
    builder = StateGraph(_AttemptState)
    builder.add_node(
        "risky",
        _risky_node,
        retry_policy=RetryPolicy(
            max_attempts=max_attempts,
            retry_on=RetryableError,
            initial_interval=0.0,
            jitter=False,
        ),
    )
    builder.add_edge(START, "risky")
    builder.add_edge("risky", END)
    return builder.compile(checkpointer=saver), conn


class ErrorClassDiscriminationTests(unittest.TestCase):
    def test_retryable_error_is_retried_up_to_max_attempts(self):
        """RetryableError retries: fails twice, succeeds on the third attempt."""
        with tempfile.TemporaryDirectory() as tmp:
            checkpoint_db = Path(tmp) / "checkpoint.sqlite"
            marker = Path(tmp) / "attempts.log"
            graph, conn = _build_graph(checkpoint_db, max_attempts=3)
            try:
                result = graph.invoke(
                    {
                        "thread_id": "retryable-case",
                        "fail_mode": "retryable",
                        "fail_until": 2,
                        "marker_path": str(marker),
                    },
                    config={"configurable": {"thread_id": "retryable-case"}},
                )
                self.assertEqual("succeeded", result["outcome"])
                self.assertEqual(3, len(marker.read_text().splitlines()))
            finally:
                conn.close()

    def test_terminal_error_is_not_retried(self):
        """TerminalError propagates on the first attempt -- zero retries."""
        with tempfile.TemporaryDirectory() as tmp:
            checkpoint_db = Path(tmp) / "checkpoint.sqlite"
            marker = Path(tmp) / "attempts.log"
            graph, conn = _build_graph(checkpoint_db, max_attempts=3)
            try:
                with self.assertRaises(TerminalError):
                    graph.invoke(
                        {
                            "thread_id": "terminal-case",
                            "fail_mode": "terminal",
                            "fail_until": 0,
                            "marker_path": str(marker),
                        },
                        config={"configurable": {"thread_id": "terminal-case"}},
                    )
                self.assertEqual(1, len(marker.read_text().splitlines()))
            finally:
                conn.close()

    def test_authority_required_error_is_not_a_retry_condition(self):
        """AuthorityRequiredError and TerminalError are not RetryableError subclasses."""
        self.assertFalse(issubclass(AuthorityRequiredError, RetryableError))
        self.assertFalse(issubclass(TerminalError, RetryableError))


if __name__ == "__main__":
    unittest.main()
