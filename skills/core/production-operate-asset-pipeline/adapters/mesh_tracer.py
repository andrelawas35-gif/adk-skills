"""
Mesh-stage tracer bullet (WO 2026-08-25-010 Decision 2).

Real image-to-3D: uploads the concept image from Decision 1's tracer into
ComfyUI, runs Hunyuan3D-2 through ComfyUIAdapter's uniform interface, and
verifies a real GLB lands in scratch with valid glTF magic bytes.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from tracer_bullet import ComfyUIAdapter, JobStatus


def main() -> int:
    concept = Path(r"C:\Users\Andre\AppData\Local\Temp\ws-pipeline-tracer\concept_00001_.png")
    if not concept.exists():
        print(f"[tracer] FAILED: concept image from Decision 1 not found at {concept}")
        return 1

    adapter = ComfyUIAdapter(live_mesh_generation=True)
    job_id = adapter.submit_job("mesh_generation", {
        "image_path": str(concept),
        "steps": 20,
        "octree_resolution": 256,
    })

    timeout_s = 2400
    poll_interval_s = 3
    deadline = time.time() + timeout_s
    status = JobStatus.PENDING
    while time.time() < deadline:
        status = adapter.poll_status(job_id)
        if status in (JobStatus.COMPLETED, JobStatus.FAILED):
            break
        time.sleep(poll_interval_s)

    if status == JobStatus.FAILED:
        print("[tracer] FAILED: live mesh dispatch reported error")
        return 1
    if status != JobStatus.COMPLETED:
        print(f"[tracer] TIMEOUT after {timeout_s}s, last status={status.value}")
        return 1

    result = adapter.get_result(job_id)
    glb_path = result.output.get("file_path")
    if not glb_path or not Path(glb_path).exists():
        print(f"[tracer] FAILED: no GLB file at {glb_path}")
        return 1

    data = Path(glb_path).read_bytes()
    if len(data) <= 0:
        print(f"[tracer] FAILED: GLB file is empty ({glb_path})")
        return 1
    if data[:4] != b"glTF":
        print(f"[tracer] FAILED: file lacks glTF magic bytes: {data[:8]!r}")
        return 1

    print("[tracer] EXIT CRITERIA MET")
    print(f"  prompt_id : {result.output.get('prompt_id')}")
    print(f"  glb       : {glb_path} ({len(data)} bytes, glTF magic ok)")
    print(f"  source    : {concept.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
