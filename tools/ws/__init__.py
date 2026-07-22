"""Deterministic CLI for Work Studio state file operations.

Python 3 stdlib-only. No external dependencies.

The CLI (tools/ws) is the sole write path for .work-studio/ state files.
Agents call it as an external tool rather than mutating files directly.
"""

VERSION = "1.0.0"
