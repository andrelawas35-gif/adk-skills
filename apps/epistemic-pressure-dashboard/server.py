"""Local-only transport for the epistemic-pressure dashboard tracer."""

import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


APP_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = APP_DIR.parents[1]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from tools.ws.dashboard_signals import (
    count_claims_below_support_adequacy,
    count_unresolved_conflicts,
)


HOST = "127.0.0.1"
PORT = 8765
SIGNAL_PATH = "/api/signals/unresolved-material-conflicts"
SIGNAL_PATH_2 = "/api/signals/claims-below-support-adequacy"


class DashboardHandler(BaseHTTPRequestHandler):
    """Serve the bounded dashboard assets and its one count endpoint."""

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path == SIGNAL_PATH:
            self._serve_signal()
        elif path == SIGNAL_PATH_2:
            self._serve_signal_claims_below_support_adequacy()
        elif path in ("/", "/index.html"):
            self._serve_file(APP_DIR / "index.html", "text/html; charset=utf-8")
        elif path == "/tokens.css":
            self._serve_file(APP_DIR / "tokens.css", "text/css; charset=utf-8")
        else:
            self._send_json(404, {"error": "not_found"})

    def _serve_signal(self) -> None:
        try:
            count = count_unresolved_conflicts()
        except (FileNotFoundError, OSError, ValueError) as error:
            print(f"signal_unavailable: {error}", file=sys.stderr)
            self._send_json(500, {"error": "signal_unavailable"})
            return
        self._send_json(200, {"count": count})

    def _serve_signal_claims_below_support_adequacy(self) -> None:
        try:
            count = count_claims_below_support_adequacy()
        except (FileNotFoundError, OSError, ValueError) as error:
            print(f"signal_unavailable: {error}", file=sys.stderr)
            self._send_json(500, {"error": "signal_unavailable"})
            return
        self._send_json(200, {"count": count})

    def _serve_file(self, path: Path, content_type: str) -> None:
        try:
            content = path.read_bytes()
        except OSError as error:
            print(f"asset_unavailable: {error}", file=sys.stderr)
            self._send_json(500, {"error": "asset_unavailable"})
            return
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, status: int, payload: dict) -> None:
        content = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


def run() -> None:
    server = ThreadingHTTPServer((HOST, PORT), DashboardHandler)
    print(f"Epistemic pressure dashboard: http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
