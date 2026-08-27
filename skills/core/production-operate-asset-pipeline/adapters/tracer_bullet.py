"""
Operator Adapter Layer — Tracer Bullet (WO 2026-08-25-006 Decision 2)

Creates a uniform interface for operator calls:
- submit_job(job_type, params) -> job_id
- poll_status(job_id) -> status
- get_result(job_id) -> result

WO 2026-08-25-010 Decision 1: ComfyUIAdapter gained a REAL dispatch path for
the concept_art stage (live_concept_art=True) — one Flux1-Krea-dev submission
through the local ComfyUI HTTP API (/prompt -> /history -> /view), replacing
the simulation for that stage only. All other job types and both adapters'
remaining paths remain simulated.
"""

import json
import tempfile
import time
import urllib.parse
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Optional


class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class JobResult:
    job_id: str
    status: JobStatus
    output: Optional[Any] = None
    error: Optional[str] = None


class OperatorAdapter(ABC):
    """Abstract base class for operator adapters."""
    
    @abstractmethod
    def submit_job(self, job_type: str, params: dict) -> str:
        """Submit a job to the operator. Returns job_id."""
        pass
    
    @abstractmethod
    def poll_status(self, job_id: str) -> JobStatus:
        """Poll the status of a job."""
        pass
    
    @abstractmethod
    def get_result(self, job_id: str) -> JobResult:
        """Get the result of a completed job."""
        pass


class ComfyUIAdapter(OperatorAdapter):
    """Adapter for ComfyUI operator (COMP-043)."""

    # Real Flux1-Krea-dev workflow components verified against the live
    # server's /object_info on 2026-08-26 (WO 2026-08-25-010 Decision 1).
    FLUX_UNET = "flux1-krea-dev_fp8_scaled.safetensors"
    FLUX_CLIP1 = "clip_l.safetensors"
    FLUX_CLIP2 = "t5xxl_fp16.safetensors"
    FLUX_VAE = "ae.safetensors"

    # Real Hunyuan3D-2 components verified live (WO 2026-08-25-010 Decision 2).
    HUNYUAN3D_CHECKPOINT = "hunyuan3d-dit-v2.safetensors"
    HUNYUAN3D_CLIP_VISION = "sigclip_vision_patch14_384.safetensors"

    def __init__(
        self,
        comfyui_url: str = "http://localhost:8188",
        live_concept_art: bool = False,
        live_mesh_generation: bool = False,
    ):
        self.comfyui_url = comfyui_url.rstrip("/")
        self.live_concept_art = live_concept_art
        self.live_mesh_generation = live_mesh_generation
        self.jobs: dict[str, dict] = {}

    def _http_json(self, method: str, path: str, body: Optional[dict] = None, timeout: float = 30.0) -> Any:
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(
            f"{self.comfyui_url}{path}",
            data=data,
            headers={"Content-Type": "application/json"} if data else {},
            method=method,
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _build_flux_workflow(self, prompt: str, width: int, height: int, steps: int, seed: int) -> dict:
        """Minimal Flux1-Krea-dev txt2img graph (verified node schemas)."""
        return {
            "1": {"class_type": "UNETLoader", "inputs": {
                "unet_name": self.FLUX_UNET, "weight_dtype": "default"}},
            "2": {"class_type": "DualCLIPLoader", "inputs": {
                "clip_name1": self.FLUX_CLIP1, "clip_name2": self.FLUX_CLIP2, "type": "flux"}},
            "3": {"class_type": "VAELoader", "inputs": {"vae_name": self.FLUX_VAE}},
            "4": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": prompt}},
            "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["2", 0], "text": ""}},
            "6": {"class_type": "EmptyLatentImage", "inputs": {
                "width": width, "height": height, "batch_size": 1}},
            "7": {"class_type": "FluxGuidance", "inputs": {
                "conditioning": ["4", 0], "guidance": 3.5}},
            "8": {"class_type": "KSampler", "inputs": {
                "model": ["1", 0], "positive": ["7", 0], "negative": ["5", 0],
                "latent_image": ["6", 0], "seed": seed, "steps": steps,
                "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}},
            "9": {"class_type": "VAEDecode", "inputs": {
                "samples": ["8", 0], "vae": ["3", 0]}},
            "10": {"class_type": "SaveImage", "inputs": {
                "images": ["9", 0], "filename_prefix": "ws-pipeline-tracer/concept"}},
        }

    def submit_job(self, job_type: str, params: dict) -> str:
        """Submit a job to ComfyUI.

        Args:
            job_type: Type of job (e.g., "concept_art", "mesh_generation")
            params: Job parameters (e.g., {"prompt": "a cube", "model": "flux"})

        Returns:
            job_id: Unique identifier for the submitted job
        """
        if self.live_concept_art and job_type == "concept_art":
            return self._submit_live(job_type, params)
        if self.live_mesh_generation and job_type == "mesh_generation":
            return self._submit_live_mesh(job_type, params)

        job_id = f"comfyui-{job_type}-{int(time.time())}"

        # Simulate ComfyUI API call
        # In production, this would call the actual ComfyUI HTTP API
        print(f"[comfyui_adapter] Submitting job: {job_type}")
        print(f"[comfyui_adapter] Parameters: {params}")
        print(f"[comfyui_adapter] URL: {self.comfyui_url}")

        # Simulate job submission
        self.jobs[job_id] = {
            "type": job_type,
            "params": params,
            "status": JobStatus.PENDING,
            "submitted_at": time.time(),
        }

        print(f"[comfyui_adapter] Job submitted: {job_id}")
        return job_id

    def _submit_live(self, job_type: str, params: dict) -> str:
        """Real dispatch: POST the Flux graph to /prompt, map job_id -> prompt_id."""
        workflow = self._build_flux_workflow(
            prompt=params.get("prompt", ""),
            width=params.get("width", 512),
            height=params.get("height", 512),
            steps=params.get("steps", 4),
            seed=params.get("seed", int(time.time())),
        )
        resp = self._http_json("POST", "/prompt", {"prompt": workflow})
        prompt_id = resp["prompt_id"]
        job_id = f"comfyui-{job_type}-{int(time.time())}"
        self.jobs[job_id] = {
            "type": job_type,
            "params": params,
            "status": JobStatus.PENDING,
            "submitted_at": time.time(),
            "live": True,
            "prompt_id": prompt_id,
        }
        print(f"[comfyui_adapter] LIVE submission {job_id} -> prompt_id={prompt_id}")
        return job_id

    def _upload_image(self, image_path: str) -> dict:
        """Upload a local image to ComfyUI's input dir via /upload/image."""
        boundary = "----ws-pipeline-tracer"
        payload_name = Path(image_path).name
        with open(image_path, "rb") as f:
            file_bytes = f.read()
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="image"; filename="{payload_name}"\r\n'
            f"Content-Type: image/png\r\n\r\n"
        ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")
        req = urllib.request.Request(
            f"{self.comfyui_url}/upload/image",
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=60.0) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _build_hunyuan3d_workflow(self, image_ref: dict, steps: int, seed: int,
                                  octree_resolution: int) -> dict:
        """Hunyuan3D-2 image-to-shape graph, matching the official ComfyUI
        template (3d_hunyuan3d_image_to_model.json) node-for-node.

        Key points learned from the template: ImageOnlyCheckpointLoader
        supplies the checkpoint's own CLIP_VISION encoder (slot 1) — no
        external CLIPVisionLoader model; ModelSamplingAuraFlow shift 1.0;
        cfg 4-8; VoxelToMesh (surface net) after VAEDecodeHunyuan3D.
        """
        subfolder = image_ref.get("subfolder", "")
        load_ref = f"{subfolder}/{image_ref['name']}" if subfolder else image_ref["name"]
        return {
            "1": {"class_type": "ImageOnlyCheckpointLoader", "inputs": {
                "ckpt_name": self.HUNYUAN3D_CHECKPOINT}},
            "2": {"class_type": "ModelSamplingAuraFlow", "inputs": {
                "model": ["1", 0], "shift": 1.0}},
            "3": {"class_type": "LoadImage", "inputs": {"image": load_ref}},
            "4": {"class_type": "CLIPVisionEncode", "inputs": {
                "clip_vision": ["1", 1], "image": ["3", 0], "crop": "none"}},
            "5": {"class_type": "Hunyuan3Dv2Conditioning", "inputs": {
                "clip_vision_output": ["4", 0]}},
            "6": {"class_type": "EmptyLatentHunyuan3Dv2", "inputs": {
                "resolution": 3072, "batch_size": 1}},
            "7": {"class_type": "KSampler", "inputs": {
                "model": ["2", 0], "positive": ["5", 0], "negative": ["5", 1],
                "latent_image": ["6", 0], "seed": seed, "steps": steps,
                "cfg": 8.0, "sampler_name": "euler", "scheduler": "normal",
                "denoise": 1.0}},
            "8": {"class_type": "VAEDecodeHunyuan3D", "inputs": {
                "samples": ["7", 0], "vae": ["1", 2],
                "num_chunks": 8000, "octree_resolution": octree_resolution}},
            "8b": {"class_type": "VoxelToMesh", "inputs": {
                "voxel": ["8", 0], "algorithm": "surface net", "threshold": 0.6}},
            "9": {"class_type": "SaveGLB", "inputs": {
                "mesh": ["8b", 0], "filename_prefix": "ws-pipeline-tracer/mesh"}},
        }

    def _submit_live_mesh(self, job_type: str, params: dict) -> str:
        """Real dispatch: upload image, POST the Hunyuan3D graph to /prompt."""
        upload = self._upload_image(params["image_path"])
        workflow = self._build_hunyuan3d_workflow(
            image_ref=upload,
            steps=params.get("steps", 20),
            seed=params.get("seed", int(time.time())),
            octree_resolution=params.get("octree_resolution", 256),
        )
        resp = self._http_json("POST", "/prompt", {"prompt": workflow})
        prompt_id = resp["prompt_id"]
        job_id = f"comfyui-{job_type}-{int(time.time())}"
        self.jobs[job_id] = {
            "type": job_type,
            "params": params,
            "status": JobStatus.PENDING,
            "submitted_at": time.time(),
            "live": True,
            "prompt_id": prompt_id,
        }
        print(f"[comfyui_adapter] LIVE mesh submission {job_id} -> prompt_id={prompt_id} (upload: {upload['name']})")
        return job_id

    def poll_status(self, job_id: str) -> JobStatus:
        """Poll the status of a ComfyUI job.

        Args:
            job_id: The job identifier returned by submit_job

        Returns:
            status: Current job status
        """
        if job_id not in self.jobs:
            raise ValueError(f"Unknown job: {job_id}")

        job = self.jobs[job_id]

        if job.get("live"):
            history = self._http_json("GET", f"/history/{job['prompt_id']}")
            entry = history.get(job["prompt_id"])
            if not entry:
                status = JobStatus.PENDING
            elif entry.get("status", {}).get("status_str") == "error":
                status = JobStatus.FAILED
            elif any("images" in out for out in (entry.get("outputs") or {}).values()):
                status = JobStatus.COMPLETED
            else:
                status = JobStatus.RUNNING
            job["status"] = status
            print(f"[comfyui_adapter] Job {job_id} status: {status.value}")
            return status

        # Simulate status progression
        elapsed = time.time() - job["submitted_at"]
        if elapsed < 0.1:
            job["status"] = JobStatus.PENDING
        elif elapsed < 0.2:
            job["status"] = JobStatus.RUNNING
        else:
            job["status"] = JobStatus.COMPLETED

        print(f"[comfyui_adapter] Job {job_id} status: {job['status'].value}")
        return job["status"]

    def get_result(self, job_id: str) -> JobResult:
        """Get the result of a completed ComfyUI job.

        Args:
            job_id: The job identifier returned by submit_job

        Returns:
            result: Job result with output or error
        """
        if job_id not in self.jobs:
            raise ValueError(f"Unknown job: {job_id}")

        job = self.jobs[job_id]

        if job["status"] != JobStatus.COMPLETED:
            return JobResult(
                job_id=job_id,
                status=job["status"],
                error=f"Job not completed: {job['status'].value}",
            )

        if job.get("live"):
            output = self._fetch_live_outputs(job)
            print(f"[comfyui_adapter] Job {job_id} LIVE result: {output}")
            return JobResult(job_id=job_id, status=JobStatus.COMPLETED, output=output)

        # Simulate result based on job type
        if job["type"] == "concept_art":
            output = {
                "image_path": f"/tmp/comfyui/{job_id}.png",
                "prompt": job["params"].get("prompt", ""),
                "model": job["params"].get("model", "flux"),
            }
        elif job["type"] == "mesh_generation":
            output = {
                "mesh_path": f"/tmp/comfyui/{job_id}.glb",
                "source_image": job["params"].get("image_path", ""),
                "model": job["params"].get("model", "hunyuan3d"),
            }
        else:
            output = {"raw": f"Output for {job['type']}"}

        print(f"[comfyui_adapter] Job {job_id} result: {output}")
        return JobResult(
            job_id=job_id,
            status=JobStatus.COMPLETED,
            output=output,
        )

    def _fetch_live_outputs(self, job: dict) -> dict:
        """Download completed outputs from /view into a local scratch dir.

        Handles both image outputs (SaveImage -> "images" key) and 3D outputs
        (SaveGLB -> "gltf" key): any output list whose entries carry a
        filename is fetched.
        """
        history = self._http_json("GET", f"/history/{job['prompt_id']}")
        entry = history[job["prompt_id"]]
        scratch = Path(tempfile.gettempdir()) / "ws-pipeline-tracer"
        scratch.mkdir(parents=True, exist_ok=True)

        file_paths: dict[str, list[str]] = {}
        first_file: Optional[str] = None
        for node_output in (entry.get("outputs") or {}).values():
            for key, items in node_output.items():
                if not isinstance(items, list):
                    continue
                for item in items:
                    if not isinstance(item, dict) or "filename" not in item:
                        continue
                    query = urllib.parse.urlencode({
                        "filename": item["filename"],
                        "subfolder": item.get("subfolder", ""),
                        "type": item.get("type", "output"),
                    })
                    with urllib.request.urlopen(
                        f"{self.comfyui_url}/view?{query}", timeout=120.0
                    ) as resp:
                        dest = scratch / item["filename"]
                        dest.write_bytes(resp.read())
                    file_paths.setdefault(key, []).append(str(dest))
                    if first_file is None:
                        first_file = str(dest)

        return {
            "file_path": first_file,
            "files": file_paths,
            "prompt": job["params"].get("prompt", ""),
            "prompt_id": job["prompt_id"],
        }


class BlenderAdapter(OperatorAdapter):
    """Adapter for Blender operator (COMP-042)."""
    
    def __init__(self, queue_dir: str = "/tmp/blender-queue"):
        self.queue_dir = queue_dir
        self.jobs: dict[str, dict] = {}
    
    def submit_job(self, job_type: str, params: dict) -> str:
        """Submit a job to Blender.
        
        Args:
            job_type: Type of job (e.g., "import_mesh", "cleanup", "assign_material", "rig")
            params: Job parameters (e.g., {"mesh_path": "/tmp/model.glb", "scene": "default"})
        
        Returns:
            job_id: Unique identifier for the submitted job
        """
        job_id = f"blender-{job_type}-{int(time.time())}"
        
        # Simulate Blender API call
        # In production, this would call the actual Blender file-based command queue
        print(f"[blender_adapter] Submitting job: {job_type}")
        print(f"[blender_adapter] Parameters: {params}")
        print(f"[blender_adapter] Queue dir: {self.queue_dir}")
        
        # Simulate job submission
        self.jobs[job_id] = {
            "type": job_type,
            "params": params,
            "status": JobStatus.PENDING,
            "submitted_at": time.time(),
        }
        
        print(f"[blender_adapter] Job submitted: {job_id}")
        return job_id
    
    def poll_status(self, job_id: str) -> JobStatus:
        """Poll the status of a Blender job.
        
        Args:
            job_id: The job identifier returned by submit_job
        
        Returns:
            status: Current job status
        """
        if job_id not in self.jobs:
            raise ValueError(f"Unknown job: {job_id}")
        
        job = self.jobs[job_id]
        
        # Simulate status progression
        elapsed = time.time() - job["submitted_at"]
        if elapsed < 0.1:
            job["status"] = JobStatus.PENDING
        elif elapsed < 0.2:
            job["status"] = JobStatus.RUNNING
        else:
            job["status"] = JobStatus.COMPLETED
        
        print(f"[blender_adapter] Job {job_id} status: {job['status'].value}")
        return job["status"]
    
    def get_result(self, job_id: str) -> JobResult:
        """Get the result of a completed Blender job.
        
        Args:
            job_id: The job identifier returned by submit_job
        
        Returns:
            result: Job result with output or error
        """
        if job_id not in self.jobs:
            raise ValueError(f"Unknown job: {job_id}")
        
        job = self.jobs[job_id]
        
        if job["status"] != JobStatus.COMPLETED:
            return JobResult(
                job_id=job_id,
                status=job["status"],
                error=f"Job not completed: {job['status'].value}",
            )
        
        # Simulate result based on job type
        if job["type"] == "import_mesh":
            output = {
                "object_name": job["params"].get("mesh_path", "").split("/")[-1].split(".")[0],
                "mesh_path": job["params"].get("mesh_path", ""),
                "scene": job["params"].get("scene", "default"),
            }
        elif job["type"] == "cleanup":
            output = {
                "object_name": job["params"].get("object_name", ""),
                "vertices_removed": 150,
                "faces_removed": 75,
                "scene": job["params"].get("scene", "default"),
            }
        elif job["type"] == "assign_material":
            output = {
                "object_name": job["params"].get("object_name", ""),
                "material_name": job["params"].get("material_name", "default"),
                "scene": job["params"].get("scene", "default"),
            }
        elif job["type"] == "rig":
            output = {
                "object_name": job["params"].get("object_name", ""),
                "armature_name": f"{job['params'].get('object_name', '')}_armature",
                "bones_count": 12,
                "scene": job["params"].get("scene", "default"),
            }
        else:
            output = {"raw": f"Output for {job['type']}"}
        
        print(f"[blender_adapter] Job {job_id} result: {output}")
        return JobResult(
            job_id=job_id,
            status=JobStatus.COMPLETED,
            output=output,
        )


def main():
    """Tracer bullet: test ComfyUIAdapter and BlenderAdapter."""
    
    print("=" * 60)
    print("OPERATOR ADAPTER LAYER TRACER BULLET")
    print("WO 2026-08-25-007 Decision 1")
    print("=" * 60)
    
    # Test ComfyUIAdapter
    print("\n--- Test ComfyUIAdapter ---")
    comfyui_adapter = ComfyUIAdapter()
    
    # Test 1: Submit concept art job
    print("\n--- Test 1: Submit concept art job ---")
    job_id = comfyui_adapter.submit_job("concept_art", {
        "prompt": "A simple cube prop, white background",
        "model": "flux",
    })
    
    # Test 2: Poll status
    print("\n--- Test 2: Poll status ---")
    time.sleep(0.3)  # Simulate waiting
    status = comfyui_adapter.poll_status(job_id)
    assert status == JobStatus.COMPLETED, f"Expected COMPLETED, got {status}"
    
    # Test 3: Get result
    print("\n--- Test 3: Get result ---")
    result = comfyui_adapter.get_result(job_id)
    assert result.status == JobStatus.COMPLETED, f"Expected COMPLETED, got {result.status}"
    assert result.output is not None, "Expected output, got None"
    assert "image_path" in result.output, "Expected image_path in output"
    
    # Test BlenderAdapter
    print("\n--- Test BlenderAdapter ---")
    blender_adapter = BlenderAdapter()
    
    # Test 4: Submit cleanup job
    print("\n--- Test 4: Submit cleanup job ---")
    job_id = blender_adapter.submit_job("cleanup", {
        "object_name": "cube",
        "scene": "default",
    })
    
    # Test 5: Poll status
    print("\n--- Test 5: Poll status ---")
    time.sleep(0.3)  # Simulate waiting
    status = blender_adapter.poll_status(job_id)
    assert status == JobStatus.COMPLETED, f"Expected COMPLETED, got {status}"
    
    # Test 6: Get result
    print("\n--- Test 6: Get result ---")
    result = blender_adapter.get_result(job_id)
    assert result.status == JobStatus.COMPLETED, f"Expected COMPLETED, got {result.status}"
    assert result.output is not None, "Expected output, got None"
    assert "object_name" in result.output, "Expected object_name in output"
    
    # Test 7: Verify uniform interface for both adapters
    print("\n--- Test 7: Verify uniform interface ---")
    for adapter_name, adapter in [("ComfyUIAdapter", comfyui_adapter), ("BlenderAdapter", blender_adapter)]:
        assert hasattr(adapter, "submit_job"), f"{adapter_name} missing submit_job method"
        assert hasattr(adapter, "poll_status"), f"{adapter_name} missing poll_status method"
        assert hasattr(adapter, "get_result"), f"{adapter_name} missing get_result method"
        print(f"[verify] {adapter_name} uniform interface verified")
    
    # Summary
    print("\n" + "=" * 60)
    print("TRACER BULLET RESULTS")
    print("=" * 60)
    print(f"ComfyUIAdapter: VERIFIED")
    print(f"BlenderAdapter: VERIFIED")
    print(f"Uniform interface: VERIFIED")
    print(f"Adapter layer pattern: PROVEN")
    print("=" * 60)


if __name__ == "__main__":
    main()
