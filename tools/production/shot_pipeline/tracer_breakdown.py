"""Slice 2 tracer: screenplay breakdown -> real linked Shot WOs (COMP-049).

WO 2026-08-25-011 slice 2. Proves programmatic creation + hierarchy linking:
parse breakdown text, create Shot WOs via ws create, link each depends_on the
V1 Scene (SC030, 2026-08-23-004) exactly like the seed shots, traverse via
ws graph trace, and keep ws validate regression-free.

Durable artifacts: two new Shot WOs remain as tracer records (V1 seed
precedent); relations are append-only.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent / "tools" / "production"))
from shot_pipeline import breakdown
from shot_pipeline.sync import StateSync

REPO = Path(breakdown.__file__).resolve().parent.parent.parent.parent
SHOT_SCENE_PARENT = "2026-08-23-004"  # SC030 — same parent as V1 seed shots

BREAKDOWN_TEXT = """\
# Market short — second unit breakdown
SHOT SH005: Leo counts coins at the stall, close on hands
# a comment line and a blank line follow

SHOT SH006: Mara walks away through the crowd, medium wide
"""


def main() -> int:
    sync = StateSync("2026-08-25-011")
    baseline = sync.validate(10**9)
    print(f"[breakdown] validate baseline errors: {baseline}")

    # ── Negative 1: malformed line is a hard error naming the line ──────
    try:
        breakdown.parse_breakdown("SHOT SH001: ok\nGARBAGE LINE HERE\n")
        print("[breakdown] NEG1 FAIL malformed line accepted")
        return 2
    except breakdown.BreakdownError as exc:
        assert "line 2" in str(exc) and "GARBAGE" in str(exc), exc
        print("[breakdown] NEG1 PASS: malformed line rejected with line number")

    # ── Negative 2: duplicate shot key rejected ─────────────────────────
    try:
        breakdown.parse_breakdown("SHOT SH001: a\nSHOT SH001: b\n")
        print("[breakdown] NEG2 FAIL duplicate accepted")
        return 3
    except breakdown.BreakdownError as exc:
        assert "duplicate shot key" in str(exc), exc
        print("[breakdown] NEG2 PASS: duplicate key rejected")

    # ── Parse + create + link ───────────────────────────────────────────
    parsed = breakdown.parse_breakdown(BREAKDOWN_TEXT)
    if [s["key"] for s in parsed] != ["SH005", "SH006"]:
        print(f"[breakdown] FAIL parse keys {[s['key'] for s in parsed]}")
        return 4

    results = breakdown.create_shot_wos(
        BREAKDOWN_TEXT, parent_wo_id=SHOT_SCENE_PARENT)
    if len(results) != 2 or not all(r["linked"] for r in results):
        print(f"[breakdown] FAIL create/link results {results}")
        return 5

    ids = [r["wo_id"] for r in results]

    # ── Hierarchy traversal: shot -> scene edge visible in graph trace ──
    # V1 note: child->parent depends_on edges are 'downstream' from the child.
    proc = breakdown._run_cli(["graph", "trace", ids[0], "--direction", "downstream"],
                              expect_ok=False)
    trace_out = proc.stdout + proc.stderr
    if SHOT_SCENE_PARENT not in trace_out:
        print(f"[breakdown] FAIL scene not in downstream trace:\n{trace_out[-800:]}")
        return 6
    print(f"[breakdown] graph trace upstream from {ids[0]} reaches {SHOT_SCENE_PARENT}")

    after = sync.validate(baseline)
    if after > baseline:
        print(f"[breakdown] FAIL validate regressed {baseline} -> {after}")
        return 7

    print(f"[breakdown] PASS: {len(results)} Shot WOs created programmatically "
          f"({', '.join(ids)}), linked depends_on {SHOT_SCENE_PARENT}, "
          f"traversable via ws graph, validate unchanged ({after}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
