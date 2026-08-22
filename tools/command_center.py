#!/usr/bin/env python3
"""Thin convenience wrapper -- the real logic lives in tools/ws/command_center.py.

Prefer `ws command-center` (or `python3 -m tools.ws command-center`) directly;
this script exists only for `python3 tools/command_center.py` as a shortcut.
WO 2026-08-22-006.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if __name__ == "__main__":
    sys.exit(subprocess.call([sys.executable, "-m", "tools.ws", "command-center"], cwd=ROOT))
