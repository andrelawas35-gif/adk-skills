"""pywebview entry point for the local Director Console."""

from __future__ import annotations

import sys
from pathlib import Path

from .bridge import DirectorConsoleBridge


def static_index_path() -> Path:
    return Path(__file__).resolve().parent / "static" / "index.html"


def main() -> int:
    try:
        import webview
    except ImportError:
        print(
            "pywebview is not installed. Install it in this environment to "
            "launch the native Director Console window.",
            file=sys.stderr,
        )
        return 2

    bridge = DirectorConsoleBridge()
    index = static_index_path()
    webview.create_window(
        "Director Console",
        index.as_uri(),
        js_api=bridge,
        width=1280,
        height=840,
        min_size=(980, 640),
    )
    webview.start(debug=False)
    return 0
