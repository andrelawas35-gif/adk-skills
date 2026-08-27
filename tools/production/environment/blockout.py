"""COMP-050 tracer bullet: environment-language spec -> blockout geometry.

WO 2026-08-24-022 Decision 2 (fresh implementation; prior uncheckpointed pass
deleted by director authority). Compiles a structured environment spec into
existing blender_operator queue commands only — no new executor ops:

  object.import_mesh (unit-cube placeholder, primitive-gap option b)
  object.set_transform / mesh.set_dimensions / material.set / material.assign
  light.set / camera.set (lens) / object.set_transform (camera + light aim)
  render.final (two camera-test angles)

GPU: claims the COMP-041 'blender' slot for the whole run (import_mesh and
render.final are VRAM-guarded ops), releases in a finally block.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO = Path(r"C:\Users\Andre\Documents\Work_Studio\andrelawas-work-studio")
PROD = REPO / "tools" / "production"
sys.path.insert(0, str(PROD))

from blender_operator import queue  # noqa: E402

QUEUE_DIR = REPO / "runtime" / "blender_queue"
POLL_S = 1.0
CMD_TIMEOUT_S = 300.0


class BlockoutError(RuntimeError):
    pass


def _run_cmd(op: str, params: dict) -> dict:
    cid = queue.write_command(QUEUE_DIR, op, params)
    deadline = time.monotonic() + CMD_TIMEOUT_S
    while time.monotonic() < deadline:
        if queue.has_result(QUEUE_DIR, cid):
            result = queue.read_result(QUEUE_DIR, cid)
            if result.get("status") != "ok":
                raise BlockoutError(f"{op} failed: {result.get('error')}")
            return result.get("data") or {}
        time.sleep(POLL_S)
    raise BlockoutError(f"{op} timed out after {CMD_TIMEOUT_S}s (cmd {cid})")


def _probe_scene() -> dict:
    objs = _run_cmd("scene.get_objects", {})
    names = objs.get("objects", [])
    camera = next((n for n in names if n.lower().startswith("camera")), None)
    light = next((n for n in names
                  if n.lower().startswith(("light", "lamp", "sun"))), None)
    return {"objects": names, "camera": camera, "light": light}


def _clear_defaults(names: list[str], keep: list[str]) -> None:
    for n in names:
        if n not in keep:
            _run_cmd("object.delete", {"name": n})


def build_blockout(spec_path: Path, scratch: Path) -> dict:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    cube_path = scratch / "assets" / "unit_cube.obj"
    render_root = scratch / "renders"
    render_root.mkdir(parents=True, exist_ok=True)

    # No manual GPU claim: the executor claims/releases the COMP-041 'blender'
    # slot itself around each VRAM-guarded op (import_mesh, render.final).
    try:
        scene = _probe_scene()
        keep = [n for n in (scene["camera"], scene["light"]) if n]
        _clear_defaults([o for o in scene["objects"] if o not in keep], keep)

        materials = {}
        for mat_name, mat_spec in spec["materials"].items():
            _run_cmd("material.set", {"name": mat_name,
                                      "base_color": mat_spec["base_color"]})
            materials[mat_name] = mat_name

        # Import the placeholder cube once; it BECOMES the first mass (ground).
        _run_cmd("object.import_mesh", {"path": str(cube_path)})
        scene = _probe_scene()
        imported = [o for o in scene["objects"] if o not in keep]
        if not imported:
            raise BlockoutError("unit-cube import produced no object")
        proto = imported[0]

        masses = [spec["ground"]] + spec["masses"]
        for i, mass in enumerate(masses):
            name = mass.get("name", f"mass_{i:02d}")
            if i == 0:
                obj = proto
            else:
                obj = (_run_cmd("object.duplicate", {"name": proto})
                       .get("name") or f"{proto}.{i:03d}")
            _run_cmd("object.set_transform", {
                "name": obj,
                "location": mass["position_m"],
                "rotation_deg": [0, 0, 0],  # kill OBJ importer's Z-up rotation
                "scale": [1, 1, 1],
            })
            _run_cmd("mesh.set_dimensions",
                     {"name": obj, "dimensions": mass["size_m"]})
            _run_cmd("material.assign",
                     {"name": obj, "material": mass["material"]})

        light_name = scene["light"]
        if not light_name:
            raise BlockoutError("no light object in scene to configure")
        light_spec = spec["lighting"]
        _run_cmd("light.set", {"name": light_name,
                               "energy": light_spec["energy"],
                               "color": light_spec["color"]})
        _run_cmd("object.set_transform",
                 {"name": light_name, "location": light_spec["position_m"]})

        rendered = []
        for cam_spec in spec["cameras"]:
            cam_obj = scene["camera"]
            if not cam_obj:
                raise BlockoutError("no camera object in scene")
            _run_cmd("camera.set", {"name": cam_obj,
                                    "lens_mm": cam_spec.get("lens_mm", 32)})
            _run_cmd("object.set_transform", {
                "name": cam_obj,
                "location": cam_spec["location_m"],
                "rotation_deg": cam_spec["rotation_deg"],
            })
            render_spec = next(r for r in spec["renders"]
                               if r["name"] == cam_spec["name"])
            out = render_root / Path(render_spec["filepath"]).name
            _run_cmd("render.final", {"filepath": str(out), "format": "PNG"})
            rendered.append(str(out))

        return {"rendered": rendered,
                "masses_built": len(masses) - 1,
                "materials": list(materials)}
    except Exception:
        raise


if __name__ == "__main__":
    scratch = Path(__file__).resolve().parent
    result = build_blockout(scratch / "spec.json", scratch)
    print(json.dumps(result, indent=2))
