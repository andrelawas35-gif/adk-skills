"""research_record_note: effect journal protects a real write (WO 2026-08-17-016, Decision 6).

Tests the riskiest assumption behind Decision 6: that claim_idempotency_receipt
genuinely prevents a duplicate log entry when record_note is retried -- the
first time the effect journal protects a real effect (a file append) rather
than the tracer's synthetic marker file.

Not self-contained the way the Phase 7 tracer/error-class tests are: this
exercises the real research graph (runtime.graph.build_research_graph),
since the node is wired into production code per Decision 6's scope. Uses a
real local HTTP server, same convention as test_research_graph.py.

Run under the uv-managed Python 3.11 environment:
    uv run python -m unittest runtime.tests.test_research_record_note -v
"""

import http.server
import json
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

from langgraph.types import Command

from runtime.graph import build_research_graph


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


class _OneShotHandler(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"
    body = b"hello from the local test server"

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(self.body)

    def log_message(self, *args):
        pass


class _LocalServer:
    def __enter__(self):
        self.httpd = http.server.HTTPServer(("127.0.0.1", 0), _OneShotHandler)
        self.port = self.httpd.server_address[1]
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        return self

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}/"

    def __exit__(self, *exc):
        self.httpd.shutdown()
        self.thread.join(timeout=5)
        self.httpd.server_close()


def _run_to_completion(checkpoint_db: Path, thread_id: str, url: str) -> dict:
    """Start, approve, and run one research thread to completion."""
    graph, conn = build_research_graph(checkpoint_db)
    try:
        graph.invoke(
            {"work_object_id": "2026-07-27-001", "thread_id": thread_id, "url": url},
            config={"configurable": {"thread_id": thread_id}},
        )
        return graph.invoke(
            Command(resume=True),
            config={"configurable": {"thread_id": thread_id}},
        )
    finally:
        conn.close()


class RecordNoteTests(unittest.TestCase):
    def test_note_is_appended_exactly_once_under_normal_completion(self):
        with _LocalServer() as server, tempfile.TemporaryDirectory() as tmp:
            checkpoint_db = Path(tmp) / "tracer.sqlite"
            result = _run_to_completion(checkpoint_db, "normal-note", server.url)

            self.assertTrue(result.get("note_recorded"))
            notes_dir = checkpoint_db.parent / "research_notes"
            log_path = notes_dir / "normal-note.jsonl"
            lines = log_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(1, len(lines))
            entry = json.loads(lines[0])
            self.assertEqual("completed", entry["status"])

    def test_transient_write_failure_retries_without_duplicating_the_entry(self):
        """Exit criterion: a retried record_note skips the append, not repeats it."""
        with _LocalServer() as server, tempfile.TemporaryDirectory() as tmp:
            checkpoint_db = Path(tmp) / "tracer.sqlite"
            thread_id = "retry-note"

            real_open = Path.open
            state = {"raised": False}

            def flaky_open(self, *args, **kwargs):
                if self.name == f"{thread_id}.jsonl" and not state["raised"]:
                    state["raised"] = True
                    raise OSError("simulated transient write failure")
                return real_open(self, *args, **kwargs)

            with mock.patch.object(Path, "open", flaky_open):
                result = _run_to_completion(checkpoint_db, thread_id, server.url)

            self.assertTrue(result.get("note_recorded"))
            notes_dir = checkpoint_db.parent / "research_notes"
            log_path = notes_dir / f"{thread_id}.jsonl"
            lines = log_path.read_text(encoding="utf-8").splitlines()
            self.assertEqual(
                1, len(lines),
                "record_note must retry the failed write, not duplicate a prior success",
            )

    def test_exhausted_retries_journal_failure_without_claiming_success(self):
        """Exit criterion (Decision 8): exhaustion journals record_note:failed
        exactly once and never claims the record_note success identity."""
        with _LocalServer() as server, tempfile.TemporaryDirectory() as tmp:
            checkpoint_db = Path(tmp) / "tracer.sqlite"
            thread_id = "exhaust-note"

            real_open = Path.open

            def always_flaky_open(self, *args, **kwargs):
                if self.name == f"{thread_id}.jsonl":
                    raise OSError("simulated persistent write failure")
                return real_open(self, *args, **kwargs)

            with mock.patch.object(Path, "open", always_flaky_open):
                result = _run_to_completion(checkpoint_db, thread_id, server.url)

            self.assertFalse(result.get("note_recorded"))
            idempotency_db = checkpoint_db.parent / "research_notes" / "idempotency.sqlite"
            self.assertEqual(
                1, _journal_count(idempotency_db, thread_id, "record_note:failed"),
                "exhaustion must journal exactly one record_note:failed receipt",
            )
            self.assertEqual(
                0, _journal_count(idempotency_db, thread_id, "record_note"),
                "an exhausted attempt must never claim the record_note success identity",
            )


if __name__ == "__main__":
    unittest.main()
