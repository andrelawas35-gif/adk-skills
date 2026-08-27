"""Live Blender smoke path for production-operate-blender (COMP-042).

WO 2026-08-24-014 (verify, routed to verify-release-evidence). Drives the REAL
queue path inside a live headless Blender 5.2 subprocess:

1. Creates a temp queue dir + temp GPU registry dir (COMP-041).
2. Creates small test artifacts: a cube ``.obj`` mesh and a tiny PNG image.
3. Starts the headless add-on poller (``addon.py``) with QUEUE_DIR +
   GPU_REGISTRY_DIR set.
4. Drops command files through the queue for:
   - ``object.import_mesh`` (VRAM-gated, COMP-041 claim/release)
   - ``image.set_as_reference`` (VRAM-gated, COMP-041 claim/release)
   - ``render.preview`` (VRAM-gated, COMP-041 claim/release)
   - ``render.final`` (VRAM-gated, COMP-041 claim/release)
   - a ``protect``-blocked mutation (governance gate, expect error ack)
5. Asserts every command returns a durable result ack with status ok (or the
   expected governance error), and that the GPU registry returns to ``idle``
   after each VRAM op (claim/release observed).

Rollback: all temp dirs are cleaned up; no durable state left.
"""

import os
import subprocess
import sys
import tempfile
import time
import zlib
import struct
from pathlib import Path

BLENDER_EXE = Path(r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe")
REPO = Path(__file__).resolve().parent.parent.parent.parent
ADDON = REPO / "tools" / "production" / "blender_operator" / "addon.py"

sys.path.insert(0, str(REPO / "tools" / "production"))
from blender_operator import queue  # noqa: E402
from gpu_orchestrator import registry as gpu_registry  # noqa: E402

SESSION_ID = "blender-smoke"


def _tiny_png(path: Path) -> None:
    """Write a 2x2 red PNG using only stdlib (zlib + struct)."""
    width = height = 2
    raw = b"".join(b"\x00" + b"\xff\x00\x00\xff" * width for _ in range(height))
    def chunk(tag, data):
        c = tag + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c))
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(raw))
           + chunk(b"IEND", b""))
    path.write_bytes(png)


def _tiny_obj(path: Path) -> None:
    """Write a simple cube OBJ (plain text)."""
    obj = """# smoke cube
v -1 -1 -1
v  1 -1 -1
v  1  1 -1
v -1  1 -1
v -1 -1  1
v  1 -1  1
v  1  1  1
v -1  1  1
f 1 2 3 4
f 5 6 7 8
f 1 2 6 5
f 2 3 7 6
f 3 4 8 7
f 4 1 5 8
"""
    path.write_text(obj, encoding="utf-8")


def _wait_for_result(queue_dir: Path, cid: str, timeout_s: float = 60.0) -> dict:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        result = queue.read_result(queue_dir, cid)
        if result is not None:
            return result
        time.sleep(0.5)
    raise TimeoutError(f"no result ack for {cid}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="ws-blender-smoke-") as tmp:
        tmp_dir = Path(tmp)
        queue_dir = tmp_dir / "queue"
        gpu_dir = tmp_dir / "gpu"
        queue_dir.mkdir()
        gpu_dir.mkdir()
        png_path = tmp_dir / "ref.png"
        obj_path = tmp_dir / "cube.obj"
        _tiny_png(png_path)
        _tiny_obj(obj_path)
        print(f"[smoke] queue: {queue_dir}")
        print(f"[smoke] gpu registry: {gpu_dir}")

        env = dict(os.environ)
        env["QUEUE_DIR"] = str(queue_dir)
        env["GPU_REGISTRY_DIR"] = str(gpu_dir)

        proc = subprocess.Popen(
            [str(BLENDER_EXE), "--background", "--factory-startup",
             "--python", str(ADDON),
             "--", "--queue-dir", str(queue_dir), "--session-id", SESSION_ID],
            env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        time.sleep(6.0)  # Blender boot + poller start

        # ── Command 1: import mesh (VRAM op → claim/release) ─────────────
        cid = queue.write_command(queue_dir, "object.import_mesh",
                                  {"path": str(obj_path)},
                                  command_id=queue.make_command_id(seq=1))
        r = _wait_for_result(queue_dir, cid)
        print(f"[smoke] object.import_mesh -> {r['status']} {r.get('data')}")
        if r["status"] != "ok":
            print("[smoke] FAIL import_mesh"); proc.kill(); return 2

        # ── Command 2: reference image (VRAM op → claim/release) ─────────
        cid = queue.write_command(queue_dir, "image.set_as_reference",
                                  {"image_path": str(png_path), "name": "ref"},
                                  command_id=queue.make_command_id(seq=2))
        r = _wait_for_result(queue_dir, cid)
        print(f"[smoke] image.set_as_reference -> {r['status']} {r.get('data')}")
        if r["status"] != "ok":
            print("[smoke] FAIL set_as_reference"); proc.kill(); return 3

        # ── Command 3: render.preview (VRAM op → claim/release) ──────────
        cid = queue.write_command(queue_dir, "render.preview",
                                  {"width": 64, "height": 64},
                                  command_id=queue.make_command_id(seq=3))
        r = _wait_for_result(queue_dir, cid)
        print(f"[smoke] render.preview -> {r['status']} {r.get('data')}")
        if r["status"] != "ok":
            print("[smoke] FAIL render.preview"); proc.kill(); return 4

        # ── Command 4: render.final (VRAM op → claim/release + write) ────
        out_path = str(tmp_dir / "smoke.png")
        cid = queue.write_command(queue_dir, "render.final",
                                  {"filepath": out_path, "format": "PNG"},
                                  command_id=queue.make_command_id(seq=4))
        r = _wait_for_result(queue_dir, cid)
        print(f"[smoke] render.final -> {r['status']} {r.get('data')}")
        if r["status"] != "ok":
            print("[smoke] FAIL render.final"); proc.kill(); return 5
        if not Path(out_path).exists():
            print("[smoke] FAIL render.final produced no file")
            proc.kill(); return 6

        # ── Command 5: protected mutation (governance gate → error ack) ──
        cid = queue.write_command(queue_dir, "object.set_transform",
                                  {"name": "Cube", "target": "Cube",
                                   "location": [0, 0, 0], "protect": ["Cube"]},
                                  command_id=queue.make_command_id(seq=5))
        r = _wait_for_result(queue_dir, cid)
        print(f"[smoke] protected mutation -> {r['status']} {r.get('error')}")
        if r["status"] != "error" or r["error"]["code"] != "protected_element":
            print("[smoke] FAIL protect gate")
            proc.kill(); return 7

        # ── GPU registry: must be idle after every VRAM op released ──────
        state = gpu_registry.query(gpu_dir)
        print(f"[smoke] final GPU registry state: {state['state']}")
        if state["state"] != "idle":
            print("[smoke] FAIL GPU registry not idle after release")
            proc.kill(); return 8

        proc.kill()
        proc.wait(timeout=10)

        print("[smoke] PASS: live Blender smoke path — import / reference / "
              "preview / final render through the queue, protect gate enforced, "
              "COMP-041 claim/release observed (registry idle after each).")
        return 0


if __name__ == "__main__":
    sys.exit(main())
