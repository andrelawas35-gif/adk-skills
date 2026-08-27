"""Bounded Blender operator (COMP-042) — file-based command queue.

WO 2026-08-24-014, Decision 2 (2026-08-25T02:30:00Z). The transport is a
crash-durable file-based command queue: a persistent Blender add-on polls a
local directory for JSON command files, executes each via the bounded API,
and writes a JSON result file keyed by the same command ID. Command IDs are a
stable, reserved identifier scheme so a future socket-based notification layer
can be added without redesigning the queue.

This package keeps the queue logic in pure Python (``queue.py``) so it is
testable without Blender; ``addon.py`` is the thin bpy add-on that wires the
same logic into a live Blender session.
"""

__version__ = "0.1.0"
