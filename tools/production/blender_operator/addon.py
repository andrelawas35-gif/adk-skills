"""Blender add-on: bounded operator via a crash-durable file command queue.

WO 2026-08-24-014 Decision 2 (2026-08-25T02:30:00Z) + governed-skill build
(director option 1). Registers a persistent Blender session that polls a local
directory for ``CMD-<id>.json`` command files, executes each via the bounded
§4.2 tool surface (``executor.py``), and writes a durable ``result-<id>.json``
ack keyed by the same ID. A mid-command crash leaves the command file on disk;
on restart the pending command replays (crash-durability, the riskiest
assumption).

Queue logic lives in ``queue.py`` (pure Python, no bpy); the full bounded tool
surface lives in ``executor.py``; this file is the thin bpy wiring (polling
session + modal operator).
"""

bl_info = {
    "name": "Work Studio Bounded Blender Operator (COMP-042)",
    "author": "Work Studio",
    "version": (0, 2, 0),
    "blender": (4, 0, 0),
    "location": "File > Work Studio > Bounded Operator",
    "description": "Crash-durable file-based command queue for bounded Blender operations",
    "category": "Development",
}

import os  # noqa: E402
import sys  # noqa: E402
from pathlib import Path  # noqa: E402

import bpy  # noqa: E402

# Ensure the pure-Python modules are importable whether this add-on is run
# from the repo tree or installed into Blender's add-ons directory.
_TOOLS_PRODUCTION = Path(__file__).resolve().parent.parent
if str(_TOOLS_PRODUCTION) not in sys.path:
    sys.path.insert(0, str(_TOOLS_PRODUCTION))

from blender_operator import executor  # noqa: E402
from blender_operator import queue  # noqa: E402


def default_queue_dir() -> Path:
    env = os.environ.get("QUEUE_DIR")
    if env:
        return Path(env)
    # Repo-relative default: <repo>/runtime/blender_queue
    repo = Path(__file__).resolve().parent.parent.parent.parent
    return repo / "runtime" / "blender_queue"


POLL_INTERVAL_S = 0.25


class WorkStudioOperatorManager:
    """Single polling session shared across the add-on's modal operator."""

    def __init__(self):
        self.queue_dir = None
        self.running = False
        self.session_id = "blender-0"

    def configure(self, queue_dir: Path, session_id: str = "blender-0"):
        self.queue_dir = Path(queue_dir)
        self.session_id = session_id
        self.queue_dir.mkdir(parents=True, exist_ok=True)

    def poll_once(self) -> int:
        if self.queue_dir is None or not self.running:
            return 0
        executor_fn = lambda op, p: executor.bounded_execute(  # noqa: E731
            op, p, owner_id=self.session_id)
        return len(queue.process_once(
            self.queue_dir,
            execute=executor_fn,
            poll_delay_s=0.05,
            log=lambda msg: print(f"[ws-blender-operator] {msg}"),
        ))

    def start(self):
        self.running = True

    def stop(self):
        self.running = False


_manager = WorkStudioOperatorManager()


class WS_BLENDER_OT_poll_queue(bpy.types.Operator):
    """Modal operator that polls the command queue while Blender is open."""

    bl_idname = "ws_blender.poll_queue"
    bl_label = "Work Studio: poll bounded command queue"
    bl_options = {"INTERNAL"}

    _timer = None

    def modal(self, context, event):
        if not _manager.running:
            self.cancel(context)
            return {"CANCELLED"}
        if event.type == "TIMER":
            _manager.poll_once()
        return {"PASS_THROUGH"}

    def execute(self, context):
        _manager.start()
        _manager.configure(default_queue_dir())
        wm = context.window_manager
        self._timer = wm.event_timer_add(POLL_INTERVAL_S, window=context.window)
        wm.modal_handler_add(self)
        print(f"[ws-blender-operator] polling {_manager.queue_dir}")
        return {"RUNNING_MODAL"}

    def cancel(self, context):
        wm = context.window_manager
        if self._timer is not None:
            wm.event_timer_remove(self._timer)
        _manager.stop()


def register():
    bpy.utils.register_class(WS_BLENDER_OT_poll_queue)


def unregister():
    _manager.stop()
    bpy.utils.unregister_class(WS_BLENDER_OT_poll_queue)


if __name__ == "__main__":
    # Headless entry point: run a blocking poll loop (or --one for a single
    # pass, used by the crash-durability test harness).
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--one", action="store_true", help="poll once, then exit")
    parser.add_argument("--queue-dir", default=None, help="override queue directory")
    parser.add_argument("--session-id", default="blender-0", help="GPU owner id")
    args, _ = parser.parse_known_args()

    qdir = Path(args.queue_dir) if args.queue_dir else default_queue_dir()
    _manager.configure(qdir, session_id=args.session_id)
    _manager.start()
    print(f"[ws-blender-operator] headless queue dir: {qdir}")
    if args.one:
        _manager.poll_once()
        _manager.stop()
        print("[ws-blender-operator] one-shot poll complete")
    else:
        import time
        try:
            while True:
                _manager.poll_once()
                time.sleep(POLL_INTERVAL_S)
        except KeyboardInterrupt:
            _manager.stop()
