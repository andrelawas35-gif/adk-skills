"""Baseline identity capture and check for Work Objects.

Two CLI commands:
    - ``ws baseline capture`` — Store SHA256 of ``git status --porcelain``
      plus current commit SHA in ``.work-studio/baseline.json``.
    - ``ws baseline check`` — Compare current state against stored baseline,
      exit 0 on match, non-zero with diff on mismatch.

Baseline format (JSON):

    {
      "commit_sha": "aefd8623...",
      "dirty_fingerprint": "sha256hex",
      "captured_at": "2026-07-28T...",
      "file_count": 0
    }
"""

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


BASELINE_FILENAME = "baseline.json"


def _find_work_studio_root() -> Path:
    """Walk upward from CWD to find .work-studio/ directory."""
    cwd = Path.cwd().resolve()
    for parent in [cwd] + list(cwd.parents):
        if (parent / ".work-studio").is_dir():
            return parent
    raise FileNotFoundError(
        ".work-studio/ not found in current directory or any parent. "
        "Run 'ws init' first to bootstrap the workspace."
    )


def _run_git_status() -> str:
    """Return the output of ``git status --porcelain``."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        capture_output=True, text=True,
        cwd=Path.cwd().resolve(),
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git status --porcelain failed: {result.stderr.strip()}"
        )
    return result.stdout


def _run_git_rev_parse() -> str:
    """Return the current commit SHA via ``git rev-parse HEAD``."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True, text=True,
        cwd=Path.cwd().resolve(),
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git rev-parse HEAD failed: {result.stderr.strip()}"
        )
    return result.stdout.strip()


def _compute_dirty_fingerprint(status_output: str) -> str:
    """Compute SHA256 hex digest of ``git status --porcelain`` output."""
    return hashlib.sha256(status_output.encode("utf-8")).hexdigest()


def cmd_baseline_capture(args: argparse.Namespace) -> int:
    """Capture a baseline fingerprint of the current git state."""
    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    try:
        status_output = _run_git_status()
        commit_sha = _run_git_rev_parse()
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    dirty_fingerprint = _compute_dirty_fingerprint(status_output)
    file_count = len([l for l in status_output.split("\n") if l.strip()])

    baseline = {
        "commit_sha": commit_sha,
        "dirty_fingerprint": dirty_fingerprint,
        "captured_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "file_count": file_count,
    }

    baseline_path = ws_root / ".work-studio" / BASELINE_FILENAME
    baseline_path.write_text(json.dumps(baseline, indent=2) + "\n")

    print(f"Baseline captured: .work-studio/{BASELINE_FILENAME}")
    print(f"  commit_sha:       {commit_sha}")
    print(f"  dirty_fingerprint: {dirty_fingerprint}")
    print(f"  file_count:       {file_count}")
    return 0


def cmd_baseline_check(args: argparse.Namespace) -> int:
    """Check current state against stored baseline.

    Returns exit code 0 on match, 1 on mismatch or error.
    """
    try:
        ws_root = _find_work_studio_root()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    baseline_path = ws_root / ".work-studio" / BASELINE_FILENAME
    if not baseline_path.exists():
        print(
            f"Error: No baseline found at .work-studio/{BASELINE_FILENAME}. "
            f"Run 'ws baseline capture' first.",
            file=sys.stderr,
        )
        return 1

    try:
        baseline = json.loads(baseline_path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        print(f"Error: Cannot read baseline: {e}", file=sys.stderr)
        return 1

    try:
        status_output = _run_git_status()
        current_commit = _run_git_rev_parse()
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    current_fingerprint = _compute_dirty_fingerprint(status_output)
    current_file_count = len([l for l in status_output.split("\n") if l.strip()])

    stored_fingerprint = baseline.get("dirty_fingerprint", "")
    stored_commit = baseline.get("commit_sha", "")
    stored_file_count = baseline.get("file_count", 0)

    if current_fingerprint == stored_fingerprint:
        print(f"Baseline match: .work-studio/{BASELINE_FILENAME}")
        print(f"  commit_sha:       {current_commit}")
        print(f"  dirty_fingerprint: {stored_fingerprint}")
        print(f"  file_count:       {stored_file_count}")
        return 0

    print(f"Baseline MISMATCH: .work-studio/{BASELINE_FILENAME}")
    print(f"  commit_sha:       stored={stored_commit} current={current_commit}")
    print(
        f"  dirty_fingerprint: stored={stored_fingerprint} "
        f"current={current_fingerprint}"
    )
    print(
        f"  file_count:       stored={stored_file_count} "
        f"current={current_file_count}"
    )
    return 1
