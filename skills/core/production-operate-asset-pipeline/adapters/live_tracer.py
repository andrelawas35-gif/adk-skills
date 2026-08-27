"""
Live-dispatch tracer bullet (WO 2026-08-25-010 Decision 1).

One real Flux1-Krea-dev concept-art submission through ComfyUIAdapter's
existing uniform interface. Exit criteria: a real image file exists in the
scratch directory with nonzero size, tied to the returned prompt_id.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from tracer_bullet import ComfyUIAdapter, JobStatus


def main() -> int:
    adapter = ComfyUIAdapter(live_concept_art=True)
    job_id = adapter.submit_job("concept_art", {
        "prompt": "a simple gray cube prop on a white background, product photo",
        "width": 512,
        "height": 512,
        "steps": 4,
    })

    timeout_s = 300
    poll_interval_s = 2
    deadline = time.time() + timeout_s
    status = JobStatus.PENDING
    while time.time() < deadline:
        status = adapter.poll_status(job_id)
        if status in (JobStatus.COMPLETED, JobStatus.FAILED):
            break
        time.sleep(poll_interval_s)

    if status == JobStatus.FAILED:
        print("[tracer] FAILED: live dispatch reported error")
        return 1
    if status != JobStatus.COMPLETED:
        print(f"[tracer] TIMEOUT after {timeout_s}s, last status={status.value}")
        return 1

    result = adapter.get_result(job_id)
    image_path = result.output.get("file_path")
    if not image_path or not Path(image_path).exists():
        print(f"[tracer] FAILED: no image file at {image_path}")
        return 1

    size = Path(image_path).stat().st_size
    if size <= 0:
        print(f"[tracer] FAILED: image file is empty ({image_path})")
        return 1

    print("[tracer] EXIT CRITERIA MET")
    print(f"  prompt_id : {result.output.get('prompt_id')}")
    print(f"  image     : {image_path} ({size} bytes)")
    print(f"  prompt    : {result.output.get('prompt')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
