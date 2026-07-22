#!/usr/bin/env python3
"""Deprecated: use `python3 -m tools.ws validate append-only` instead.

This wrapper exists for backward compatibility with existing scripts
and pre-commit hooks. It delegates to the ws CLI.

Usage:
    python3 tools/verify-append-only.py <work-object-path>...
    python3 tools/verify-append-only.py --all

Both forms delegate to: python3 -m tools.ws validate append-only [--files ...]
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    args = [sys.executable, "-m", "tools.ws", "validate", "append-only"]

    if "--all" in sys.argv:
        # ws validate with no --files scans all objects
        pass
    else:
        paths = [a for a in sys.argv[1:] if not a.startswith("-")]
        if paths:
            args.extend(["--files"] + paths)

    result = subprocess.run(args, cwd=ROOT)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
