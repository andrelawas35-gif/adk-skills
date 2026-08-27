"""Full bounded tool surface for the Blender operator (COMP-042).

WO 2026-08-24-014 (governed-skill build, director option 1). Implements the
complete §4.2 tool surface from ``2026-08-23-001-production-skill-architecture
-implementation-plan.md`` (scene/object, camera/light, rig/animation, mesh,
material, image, render), with:

- **Governance gates** (``governance.py``): ``protect``-field enforcement on
  mutating ops, and the high-consequence ``execute_blender_python`` escalation
  gate requiring explicit director authority.
- **GPU claim** (``gpu_orchestrator.registry``, COMP-041): VRAM-heavy ops
  (render, import, texture) claim the single GPU slot before running and
  release after, per the sequential-VRAM discipline of WO 2026-08-24-013.

The module is imported by ``addon.py`` (bpy wiring) and by the headless
polling loop; ``bounded_execute`` is the single entry point.
"""

import math  # noqa: E402
import os  # noqa: E402
from pathlib import Path  # noqa: E402

import bpy  # noqa: E402

from blender_operator import governance  # noqa: E402
from gpu_orchestrator import registry as gpu_registry  # noqa: E402

GPU_STALE_AFTER_S = 60.0
GPU_OWNER = "blender"


def default_gpu_registry_dir() -> Path:
    env = os.environ.get("GPU_REGISTRY_DIR")
    if env:
        return Path(env)
    repo = Path(__file__).resolve().parent.parent.parent.parent
    return repo / "runtime" / "gpu_registry"


def _claim_gpu(owner_id: str):
    return gpu_registry.claim(
        default_gpu_registry_dir(),
        owner=GPU_OWNER,
        owner_id=owner_id,
        stale_after_s=GPU_STALE_AFTER_S,
    )


def _release_gpu(owner_id: str):
    gpu_registry.release(
        default_gpu_registry_dir(), owner=GPU_OWNER, owner_id=owner_id
    )


def _guard_gpu(op: str, params: dict, owner_id: str, fn):
    """Wrap a VRAM-heavy op with a GPU claim/release."""
    if op in governance.VRAM_OPS:
        claimed = _claim_gpu(owner_id)
        if not claimed.granted:
            return False, None, {
                "code": "gpu_occupied",
                "message": f"GPU slot held by {claimed.owner}/{claimed.owner_id}",
            }
        try:
            return fn()
        finally:
            _release_gpu(owner_id)
    return fn()


def _get_object(name: str):
    obj = bpy.data.objects.get(name)
    if obj is None:
        raise ValueError(f"no object named {name!r}")
    return obj


def _get_material(name: str):
    mat = bpy.data.materials.get(name)
    if mat is None:
        raise ValueError(f"no material named {name!r}")
    return mat


def _set_transform(obj, params: dict):
    if "location" in params:
        obj.location = params["location"]
    if "rotation_deg" in params:
        obj.rotation_euler = [math.radians(a) for a in params["rotation_deg"]]
    if "scale" in params:
        obj.scale = params["scale"]


def bounded_execute(op: str, params: dict, owner_id: str = "blender-0"):
    """Execute one bounded command. Returns ``(ok, data, error)``."""
    try:
        # ── High-consequence escalation gate ─────────────────────────────
        if op == "execute_blender_python":
            err = governance.authorize_execute_blender_python(params)
            if err:
                return False, None, err
            code = params.get("code") or params.get("python")
            if not code:
                return False, None, {"code": "no_python", "message": "no 'code' in params"}
            exec(code, {"bpy": bpy, "__builtins__": {}}, {})  # noqa: S102
            return True, {"executed": True}, None

        # ── Protect-field governance check (mutating ops) ────────────────
        err = governance.validate_command(op, params, params.get("protect"))
        if err:
            return False, None, err

        # ── Read-only scene surface ──────────────────────────────────────
        if op == "scene.get_objects":
            return True, {"objects": [o.name for o in bpy.data.objects]}, None

        if op == "scene.get_info":
            return True, {
                "scene": bpy.context.scene.name,
                "object_count": len(bpy.data.objects),
                "blender_version": bpy.app.version_string,
            }, None

        if op == "object.get":
            obj = _get_object(params["name"])
            return True, {
                "name": obj.name,
                "location": list(obj.location),
                "rotation": list(obj.rotation_euler),
                "scale": list(obj.scale),
                "parent": obj.parent.name if obj.parent else None,
            }, None

        # ── Object mutations ─────────────────────────────────────────────
        if op == "object.set_transform":
            obj = _get_object(params["name"])
            _set_transform(obj, params)
            return True, {"name": obj.name}, None

        if op == "object.duplicate":
            obj = _get_object(params["name"])
            new_obj = obj.copy()
            if obj.data:
                new_obj.data = obj.data.copy()
            bpy.context.collection.objects.link(new_obj)
            return True, {"name": new_obj.name}, None

        if op == "object.delete":
            obj = _get_object(params["name"])
            bpy.data.objects.remove(obj, do_unlink=True)
            return True, {"deleted": params["name"]}, None

        if op == "object.set_parent":
            obj = _get_object(params["name"])
            parent = _get_object(params["parent"])
            obj.parent = parent
            return True, {"name": obj.name, "parent": parent.name}, None

        if op == "object.select":
            obj = _get_object(params["name"])
            obj.select_set(True)
            return True, {"name": obj.name}, None

        if op == "object.deselect":
            obj = _get_object(params["name"])
            obj.select_set(False)
            return True, {"name": obj.name}, None

        if op == "object.import_mesh":
            return _guard_gpu(op, params, owner_id, lambda: _import_mesh(params))

        # ── Camera / light ───────────────────────────────────────────────
        if op == "camera.get":
            cams = [c.name for c in bpy.data.cameras]
            return True, {"cameras": cams}, None

        if op == "camera.set":
            cam = bpy.data.cameras.get(params["name"])
            if cam is None:
                cam = bpy.data.cameras.new(params["name"])
            if "lens_mm" in params:
                cam.lens = params["lens_mm"]
            return True, {"name": cam.name}, None

        if op == "camera.lock":
            cam = bpy.data.cameras.get(params["name"])
            if cam is None:
                raise ValueError(f"no camera named {params['name']!r}")
            cam["locked"] = True
            return True, {"name": cam.name, "locked": True}, None

        if op == "light.get":
            lights = [o.name for o in bpy.data.objects if o.type == "LIGHT"]
            return True, {"lights": lights}, None

        if op == "light.set":
            light = bpy.data.lights.get(params["name"])
            if light is None:
                light = bpy.data.lights.new(params["name"], type="POINT")
            if "energy" in params:
                light.energy = params["energy"]
            if "color" in params:
                light.color = params["color"]
            return True, {"name": light.name}, None

        # ── Rig / animation ──────────────────────────────────────────────
        if op == "rig.get_pose":
            obj = _get_object(params["name"])
            bones = {}
            if obj.type == "ARMATURE" and obj.pose:
                for bone in obj.pose.bones:
                    angle = bone.rotation_euler[2] if len(bone.rotation_euler) >= 3 else 0.0
                    bones[bone.name] = {"z_deg": math.degrees(angle)}
            return True, {"bones": bones}, None

        if op == "rig.set_bone_rotation":
            obj = _get_object(params["name"])
            bone = obj.pose.bones.get(params["bone"])
            if bone is None:
                raise ValueError(f"no bone {params['bone']!r} in {params['name']!r}")
            bone.rotation_euler[2] = math.radians(params.get("z_deg", 0.0))
            return True, {"bone": bone.name}, None

        if op == "animation.get_keyframes":
            obj = _get_object(params["name"])
            frames = set()
            if obj.animation_data and obj.animation_data.action:
                for fcurve in obj.animation_data.action.fcurves:
                    for kp in fcurve.keyframe_points:
                        frames.add(int(kp.co[0]))
            return True, {"keyframes": sorted(frames)}, None

        if op == "animation.move_keyframe":
            obj = _get_object(params["name"])
            delta = params.get("delta_frames", 1)
            if obj.animation_data and obj.animation_data.action:
                for fcurve in obj.animation_data.action.fcurves:
                    for kp in fcurve.keyframe_points:
                        kp.co[0] += delta
            return True, {"moved": delta}, None

        if op == "animation.set_interpolation":
            obj = _get_object(params["name"])
            interp = params.get("interpolation", "BEZIER")
            if obj.animation_data and obj.animation_data.action:
                for fcurve in obj.animation_data.action.fcurves:
                    for kp in fcurve.keyframe_points:
                        kp.interpolation = interp
            return True, {"interpolation": interp}, None

        # ── Mesh (asset cleanup) ─────────────────────────────────────────
        if op == "mesh.get_vertices":
            obj = _get_object(params["name"])
            if obj.type != "MESH":
                raise ValueError(f"{params['name']!r} is not a mesh")
            return True, {"vertex_count": len(obj.data.vertices)}, None

        if op == "mesh.move_vertices":
            obj = _get_object(params["name"])
            if obj.type != "MESH":
                raise ValueError(f"{params['name']!r} is not a mesh")
            indices = params.get("indices") or range(len(obj.data.vertices))
            offset = params.get("offset", [0, 0, 0])
            moved = 0
            for idx in indices:
                vertex = obj.data.vertices[int(idx)]
                vertex.co.x += offset[0]
                vertex.co.y += offset[1]
                vertex.co.z += offset[2]
                moved += 1
            return True, {"moved": moved}, None

        if op == "mesh.extrude":
            obj = _get_object(params["name"])
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.extrude_region_move()
            bpy.ops.object.mode_set(mode="OBJECT")
            return True, {"object": obj.name, "extruded": True}, None

        if op == "mesh.separate_by_material":
            obj = _get_object(params["name"])
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.separate(type="MATERIAL")
            bpy.ops.object.mode_set(mode="OBJECT")
            return True, {"object": obj.name, "separated_by": "material"}, None

        if op == "mesh.set_dimensions":
            obj = _get_object(params["name"])
            obj.dimensions = params.get("dimensions", [1, 1, 1])
            return True, {"dimensions": list(obj.dimensions)}, None

        if op == "mesh.set_origin":
            obj = _get_object(params["name"])
            obj.location = params.get("origin", [0, 0, 0])
            return True, {"origin": list(obj.location)}, None

        if op == "mesh.decimate":
            obj = _get_object(params["name"])
            mod = obj.modifiers.new(name="decimate_ws", type="DECIMATE")
            mod.ratio = params.get("ratio", 0.5)
            return True, {"ratio": mod.ratio}, None

        if op == "mesh.add_modifier":
            obj = _get_object(params["name"])
            mod = obj.modifiers.new(name=params.get("name", "mod_ws"),
                                    type=params.get("type", "SUBSURF"))
            return True, {"modifier": mod.name}, None

        if op == "mesh.remove_doubles":
            obj = _get_object(params["name"])
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.mode_set(mode="EDIT")
            bpy.ops.mesh.remove_doubles(threshold=params.get("threshold", 0.0001))
            bpy.ops.object.mode_set(mode="OBJECT")
            return True, {"object": obj.name, "threshold": params.get("threshold", 0.0001)}, None

        # ── Material ─────────────────────────────────────────────────────
        if op == "material.get":
            return True, {"materials": [m.name for m in bpy.data.materials]}, None

        if op == "material.set":
            mat = bpy.data.materials.get(params["name"]) or bpy.data.materials.new(params["name"])
            if "base_color" in params:
                color = list(params["base_color"])
                if len(color) == 3:
                    color.append(1.0)
                mat.diffuse_color = color
            return True, {"name": mat.name}, None

        if op == "material.assign":
            obj = _get_object(params["name"])
            mat = _get_material(params["material"])
            if len(obj.data.materials) == 0:
                obj.data.materials.append(mat)
            else:
                obj.data.materials[0] = mat
            return True, {"name": obj.name, "material": mat.name}, None

        if op == "material.set_texture":
            return _guard_gpu(op, params, owner_id, lambda: _set_texture(params))

        # ── Image ────────────────────────────────────────────────────────
        if op == "image.import_as_plane":
            return _guard_gpu(op, params, owner_id, lambda: _import_plane(params))

        if op == "image.set_as_reference":
            return _guard_gpu(op, params, owner_id, lambda: _set_reference(params))

        # ── Render ───────────────────────────────────────────────────────
        if op == "render.preview":
            return _guard_gpu(op, params, owner_id, lambda: _render_preview(params))

        if op == "render.final":
            return _guard_gpu(op, params, owner_id, lambda: _render_final(params))

        return False, None, {"code": "unknown_op", "message": f"no bounded handler for {op!r}"}
    except Exception as exc:  # noqa: BLE001
        return False, None, {"code": "blender_error", "message": str(exc)}


def _import_mesh(params: dict):
    path = Path(params["path"])
    if not path.exists():
        raise ValueError(f"mesh path does not exist: {path}")
    ext = path.suffix.lower()
    if ext == ".glb":
        bpy.ops.import_scene.gltf(filepath=str(path))
    elif ext == ".obj":
        bpy.ops.wm.obj_import(filepath=str(path))
    elif ext == ".fbx":
        bpy.ops.import_scene.fbx(filepath=str(path))
    else:
        raise ValueError(f"unsupported mesh extension: {ext}")
    return True, {"imported": path.name}, None


def _set_texture(params: dict):
    mat = _get_material(params["name"])
    image = bpy.data.images.load(params["image_path"], check_existing=True)
    if not mat.use_nodes:
        mat.use_nodes = True
    node = mat.node_tree.nodes.new("ShaderNodeTexImage")
    node.image = image
    return True, {"material": mat.name, "texture": image.name}, None


def _import_plane(params: dict):
    image_path = Path(params["image_path"])
    image = bpy.data.images.load(str(image_path), check_existing=True)
    bpy.ops.image.import_as_mesh_planes(
        files=[{"name": image.name}], directory=str(image_path.parent)
    )
    return True, {"plane": image.name}, None


def _set_reference(params: dict):
    image = bpy.data.images.load(params["image_path"], check_existing=True)
    obj = bpy.data.objects.get(params.get("name", "reference"))
    if obj is None:
        obj = bpy.data.objects.new("reference", None)
        bpy.context.collection.objects.link(obj)
    obj["reference_image"] = image.name
    return True, {"reference": obj.name, "image": image.name}, None


def _render_preview(params: dict):
    scene = bpy.context.scene
    scene.render.resolution_x = params.get("width", scene.render.resolution_x)
    scene.render.resolution_y = params.get("height", scene.render.resolution_y)
    return True, {
        "resolution": [scene.render.resolution_x, scene.render.resolution_y],
        "filepath": scene.render.filepath,
    }, None


def _render_final(params: dict):
    scene = bpy.context.scene
    scene.render.image_settings.file_format = params.get("format", "PNG")
    if params.get("filepath"):
        scene.render.filepath = params["filepath"]
    bpy.ops.render.render(write_still=True)
    return True, {"rendered": scene.render.filepath}, None
