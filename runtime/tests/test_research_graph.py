#!/usr/bin/env python3
"""Research graph tests (WO 2026-08-17-011 Decision 2).

Proves the accepted design: propose_fetch -> gate_fetch (interrupt) ->
fetch_source, one explicit URL, approval-gated before any network call,
checkpoint-safe, no compensation needed (read-only GET).

Uses a real local HTTP server (stdlib http.server) so the fetch path is
genuinely exercised over a real socket, without depending on external
network access.

Run under the uv-managed Python 3.11 environment:

    uv run python -m unittest discover -s runtime/tests -v
"""

import http.server
import tempfile
import threading
import unittest
from pathlib import Path

from langgraph.types import Command

from runtime.graph import build_research_graph, inspect_research, run_research
from runtime.research import fetch_url


class _OneShotHandler(http.server.BaseHTTPRequestHandler):
    """Serves a fixed body once per request; counts requests on the class."""

    protocol_version = "HTTP/1.0"  # close each connection; avoids keep-alive
    body = b"hello from the local test server"
    request_count = 0

    def do_GET(self):
        type(self).request_count += 1
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(self.body)

    def log_message(self, *args):
        pass  # silence test output


class _LocalServer:
    def __enter__(self):
        _OneShotHandler.request_count = 0
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


class FetchUrlTests(unittest.TestCase):
    """Unit tests for the pure fetch_url boundary function."""

    def test_successful_fetch_returns_body(self):
        with _LocalServer() as server:
            ok, body, detail = fetch_url(server.url)
            self.assertTrue(ok)
            self.assertEqual("hello from the local test server", body)
            self.assertEqual("", detail)

    def test_connection_error_is_reported_not_raised(self):
        # Port 1 is reserved/unassigned; connection should fail fast.
        ok, body, detail = fetch_url("http://127.0.0.1:1/", timeout=2)
        self.assertFalse(ok)
        self.assertEqual("", body)
        self.assertTrue(detail)

    def test_response_over_size_cap_is_rejected(self):
        with _LocalServer() as server:
            ok, body, detail = fetch_url(server.url, max_bytes=5)
            self.assertFalse(ok)
            self.assertIn("byte cap", detail)


class ResearchGraphTests(unittest.TestCase):
    """Exit criteria for WO 2026-08-17-011 Decision 2."""

    def test_no_fetch_occurs_without_approval(self):
        """Exit criterion 1."""
        with _LocalServer() as server, tempfile.TemporaryDirectory() as tmp:
            checkpoint_db = Path(tmp) / "tracer.sqlite"
            result = run_research("2026-07-27-001", "no-approval", server.url, checkpoint_db)

            self.assertIn("__interrupt__", result)
            self.assertEqual(0, _OneShotHandler.request_count)

            state = inspect_research("no-approval", checkpoint_db)
            self.assertTrue(state["awaiting_approval"])
            self.assertFalse(state["has_receipt"])

    def test_approved_fetch_produces_real_receipt(self):
        """Exit criterion 2."""
        with _LocalServer() as server, tempfile.TemporaryDirectory() as tmp:
            checkpoint_db = Path(tmp) / "tracer.sqlite"
            run_research("2026-07-27-001", "approved-fetch", server.url, checkpoint_db)
            result = run_research(
                "2026-07-27-001", "approved-fetch", server.url, checkpoint_db, approve=True
            )

            receipt = result["research_receipt"]
            self.assertEqual("completed", receipt["status"])
            self.assertEqual(server.url, receipt["source"])
            self.assertEqual("hello from the local test server", receipt["evidence"])
            self.assertEqual("low", receipt["confidence"])
            self.assertEqual(1, _OneShotHandler.request_count)

    def test_crash_resume_around_approval_never_duplicates_fetch(self):
        """Exit criterion 3: resuming a paused thread with approval fetches
        exactly once; inspecting or re-running inspect does not re-fetch."""
        with _LocalServer() as server, tempfile.TemporaryDirectory() as tmp:
            checkpoint_db = Path(tmp) / "tracer.sqlite"
            run_research("2026-07-27-001", "resume-once", server.url, checkpoint_db)
            self.assertEqual(0, _OneShotHandler.request_count)

            # Simulate a process restart: rebuild the graph fresh, then resume.
            result = run_research(
                "2026-07-27-001", "resume-once", server.url, checkpoint_db, approve=True
            )
            self.assertEqual(1, _OneShotHandler.request_count)
            self.assertEqual("completed", result["research_receipt"]["status"])

            # Inspecting the completed thread must not trigger another fetch.
            inspect_research("resume-once", checkpoint_db)
            self.assertEqual(1, _OneShotHandler.request_count)

    def test_failed_fetch_produces_failed_receipt_not_a_crash(self):
        """Exit criterion 4."""
        with tempfile.TemporaryDirectory() as tmp:
            checkpoint_db = Path(tmp) / "tracer.sqlite"
            bad_url = "http://127.0.0.1:1/"
            run_research("2026-07-27-001", "failed-fetch", bad_url, checkpoint_db)
            result = run_research(
                "2026-07-27-001", "failed-fetch", bad_url, checkpoint_db, approve=True
            )

            receipt = result["research_receipt"]
            self.assertEqual("failed", receipt["status"])
            self.assertEqual("", receipt["evidence"])
            self.assertEqual("none", receipt["confidence"])
            self.assertTrue(receipt["detail"])

    def test_no_canonical_state_touched(self):
        """Constraint: no .work-studio/ write from this node."""
        import hashlib

        ROOT = Path(__file__).resolve().parents[2]

        def _digest() -> str:
            h = hashlib.sha256()
            for p in sorted(ROOT.glob(".work-studio/**/*")):
                if p.is_file():
                    h.update(str(p.relative_to(ROOT)).encode())
                    h.update(p.read_bytes())
            return h.hexdigest()

        with _LocalServer() as server, tempfile.TemporaryDirectory() as tmp:
            checkpoint_db = Path(tmp) / "tracer.sqlite"
            before = _digest()
            run_research("2026-07-27-001", "no-canonical-write", server.url, checkpoint_db)
            run_research(
                "2026-07-27-001", "no-canonical-write", server.url, checkpoint_db, approve=True
            )
            self.assertEqual(before, _digest())


if __name__ == "__main__":
    unittest.main()
