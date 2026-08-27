"""Tracer harness: crash-durability of the file command queue against real Blender.

WO 2026-08-24-014 Decision 2 (2026-08-25T02:30:00Z). Proves the riskiest
assumption end-to-end with a real Blender subprocess:

1. Start a headless Blender session running ``addon.py`` (persistent poller).
2. Drop ``CMD-<id>.json`` with a ``delay_ms`` test seam so the command is
   guaranteed in-flight.
3. Kill the Blender subprocess mid-command (the TDR failure mode in WO
   2026-08-23-002) — no result ack should exist yet.
4. Restart Blender with the same queue directory.
5. Assert the pending command replays to a durable ``result-<id>.json``.

Read-only ``scene.get_objects`` is used so a replay is harmless. Rollback:
delete the queue directory + these scripts; all local, no durable state.
"""

import subprocess
import sys
import tempfile
import time
from pathlib import Path

BLENDER_EXE = Path(r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe")
REPO = Path(__file__).resolve().parent.parent.parent.parent
ADDON = REPO / "tools" / "production" / "blender_operator" / "addon.py"

sys.path.insert(0, str(REPO / "tools" / "production"))
from blender_operator import queue  # noqa: E402


def start_blender(queue_dir: Path, one_shot: bool):
    """Launch a headless Blender subprocess running the add-on poller."""
    cmd = [str(BLENDER_EXE), "--background", "--factory-startup", "--python", str(ADDON)]
    if one_shot:
        cmd += ["--", "--one", "--queue-dir", str(queue_dir)]
    else:
        cmd += ["--", "--queue-dir", str(queue_dir)]
    env = dict(os_environ_with_queue(queue_dir))
    return subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)


def os_environ_with_queue(queue_dir: Path):
    import os
    env = dict(os.environ)
    env["QUEUE_DIR"] = str(queue_dir)
    return env


def wait_for(predicate, timeout_s: float, step_s: float = 0.25) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        if predicate():
            return True
        time.sleep(step_s)
    return False


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ws-blender-queue-") as tmp:
        queue_dir = Path(tmp)
        cid = queue.make_command_id(seq=1)
        print(f"[tracer] queue dir: {queue_dir}")
        print(f"[tracer] command ID: {cid}")

        # Step 1: write the command with an in-flight delay (test seam) so we
        # can reliably kill mid-command.
        queue.write_command(queue_dir, "scene.get_objects",
                            command_id=cid, delay_ms=4000)
        print("[tracer] command file written (delay_ms=4000, read-only scene.get_objects)")

        # Step 2: start Blender, let it begin executing.
        proc = start_blender(queue_dir, one_shot=False)
        time.sleep(6.0)  # enough for Blender to boot + begin the delayed command

        # Step 3: kill mid-command — the result ack must NOT exist.
        proc.kill()
        proc.wait(timeout=10)
        time.sleep(0.5)
        has_ack = queue.has_result(queue_dir, cid)
        print(f"[tracer] killed Blender mid-command; result ack present? {has_ack}")
        if has_ack:
            print("[tracer] FAIL: result ack appeared before the kill — command was not in-flight")
            return 2

        # Step 4: restart Blender; pending command must replay.
        proc2 = start_blender(queue_dir, one_shot=False)
        replayed = wait_for(lambda: queue.has_result(queue_dir, cid), timeout_s=25.0)
        proc2.kill()
        proc2.wait(timeout=10)

        if not replayed:
            print("[tracer] FAIL: pending command was NOT replayed after restart")
            return 3

        result = queue.read_result(queue_dir, cid)
        print(f"[tracer] result ack: status={result.get('status')} "
              f"data_keys={list((result.get('data') or {}).keys())}")
        if result.get("status") != "ok":
            print(f"[tracer] FAIL: replay produced error: {result.get('error')}")
            return 4

        print("[tracer] PASS: read-only command round-tripped and a mid-command "
              "kill left a replayable queue entry that completed on restart.")
        print("[tracer] crash-durability assumption HOLDS against a real Blender subprocess.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
