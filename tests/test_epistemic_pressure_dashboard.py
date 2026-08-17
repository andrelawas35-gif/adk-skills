"""Contract checks for the localhost epistemic-pressure dashboard."""

import contextlib
import importlib.util
import io
import json
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SERVER_PATH = ROOT / "apps" / "epistemic-pressure-dashboard" / "server.py"
SPEC = importlib.util.spec_from_file_location("epistemic_pressure_server", SERVER_PATH)
dashboard_server = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dashboard_server)


class RunningServer:
    def __enter__(self):
        self.server = dashboard_server.ThreadingHTTPServer(
            (dashboard_server.HOST, 0),
            dashboard_server.DashboardHandler,
        )
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
        host, port = self.server.server_address
        self.base_url = f"http://{host}:{port}"
        return self

    def __exit__(self, *_):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()

    def get(self, path):
        with urllib.request.urlopen(f"{self.base_url}{path}") as response:
            return response.status, response.read()


class EpistemicPressureDashboardTest(unittest.TestCase):
    def test_signal_endpoint_is_loopback_and_count_only(self):
        self.assertEqual(dashboard_server.HOST, "127.0.0.1")
        with mock.patch.object(
            dashboard_server, "count_unresolved_conflicts", return_value=7
        ):
            with RunningServer() as running:
                status, body = running.get(dashboard_server.SIGNAL_PATH)

        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body), {"count": 7})

    def test_reader_failure_is_generic_to_browser_and_detailed_locally(self):
        detail = "/private/work-object.md: malformed conflict heading: CONF-BROKEN"
        diagnostics = io.StringIO()
        with mock.patch.object(
            dashboard_server,
            "count_unresolved_conflicts",
            side_effect=ValueError(detail),
        ):
            with contextlib.redirect_stderr(diagnostics):
                with RunningServer() as running:
                    with self.assertRaises(urllib.error.HTTPError) as caught:
                        running.get(dashboard_server.SIGNAL_PATH)
                    body = caught.exception.read()

        self.assertEqual(caught.exception.code, 500)
        self.assertEqual(json.loads(body), {"error": "signal_unavailable"})
        self.assertNotIn(b"work-object", body)
        self.assertIn(detail, diagnostics.getvalue())

    def test_browser_contract_starts_without_a_numeric_count(self):
        html = (SERVER_PATH.parent / "index.html").read_text()

        self.assertIn(
            '<output data-signal="unresolved-material-conflicts" '
            'aria-live="polite">—</output>',
            html,
        )
        self.assertIn('fetch("/api/signals/unresolved-material-conflicts")', html)
        self.assertIn("Count unavailable—inspect the server output.", html)
        self.assertNotIn(">1</output>", html)
        self.assertNotIn("signal_unavailable", html)

    def test_second_signal_endpoint_is_loopback_and_count_only(self):
        with mock.patch.object(
            dashboard_server, "count_claims_below_support_adequacy", return_value=4
        ):
            with RunningServer() as running:
                status, body = running.get(dashboard_server.SIGNAL_PATH_2)

        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body), {"count": 4})

    def test_second_signal_reader_failure_is_generic_to_browser_and_detailed_locally(self):
        detail = "/private/work-object.md: malformed claim heading: CLM-BROKEN"
        diagnostics = io.StringIO()
        with mock.patch.object(
            dashboard_server,
            "count_claims_below_support_adequacy",
            side_effect=ValueError(detail),
        ):
            with contextlib.redirect_stderr(diagnostics):
                with RunningServer() as running:
                    with self.assertRaises(urllib.error.HTTPError) as caught:
                        running.get(dashboard_server.SIGNAL_PATH_2)
                    body = caught.exception.read()

        self.assertEqual(caught.exception.code, 500)
        self.assertEqual(json.loads(body), {"error": "signal_unavailable"})
        self.assertNotIn(b"work-object", body)
        self.assertIn(detail, diagnostics.getvalue())

    def test_browser_contract_includes_second_signal_card(self):
        html = (SERVER_PATH.parent / "index.html").read_text()

        self.assertIn("<title>Epistemic pressure dashboard</title>", html)
        self.assertIn(
            '<output data-signal="claims-below-support-adequacy" '
            'aria-live="polite">—</output>',
            html,
        )
        self.assertIn('fetch("/api/signals/claims-below-support-adequacy")', html)
        self.assertNotIn(">1</output>", html)
        self.assertNotIn("signal_unavailable", html)


if __name__ == "__main__":
    unittest.main()
