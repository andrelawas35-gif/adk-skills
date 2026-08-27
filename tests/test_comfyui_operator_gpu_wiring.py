"""GPU-claim wiring tests for the bounded ComfyUI operator (WO 2026-08-24-015)."""

import sys
import tempfile
import time
import unittest
from pathlib import Path

TOOLS_PRODUCTION = Path(__file__).resolve().parent.parent / "tools" / "production"
sys.path.insert(0, str(TOOLS_PRODUCTION))

from comfyui_operator import ComfyUIClient, ComfyUIError  # noqa: E402
from gpu_orchestrator import registry as gpu_registry  # noqa: E402


class FakeTransport:
    def __init__(self):
        self.calls = []
        self.history_ready = True
        self.fail_prompt = False

    def __call__(self, method, url, payload):
        self.calls.append((method, url, payload))
        if url.endswith("/prompt"):
            if self.fail_prompt:
                raise RuntimeError("boom")
            return {"prompt_id": "prompt-1"}
        if url.endswith("/history/prompt-1"):
            if self.history_ready:
                return {"prompt-1": {"outputs": {"1": {"images": [{"filename": "out.png"}]}}}}
            return {}
        if url.endswith("/queue"):
            return {"queue_running": [], "queue_pending": []}
        if url.endswith("/object_info"):
            return {
                "CheckpointLoaderSimple": {
                    "input": {"required": {"ckpt_name": [["flux-dev-fp8.safetensors"]]}}
                },
                "LoraLoader": {
                    "input": {"required": {"lora_name": [["detail.safetensors"]]}}
                },
            }
        if url.endswith("/interrupt"):
            return {}
        raise AssertionError(f"unexpected URL: {url}")


class TestComfyUIGpuClaimWiring(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.registry_dir = Path(self._tmp.name)
        self.transport = FakeTransport()
        self.client = ComfyUIClient(
            registry_dir=self.registry_dir,
            owner_id="comfyui-test",
            transport=self.transport,
        )

    def tearDown(self):
        self._tmp.cleanup()

    def test_submit_claims_flux_and_await_releases_on_completion(self):
        submitted = self.client.execute(
            "workflow.submit",
            {"workflow_json": {"1": {"class_type": "KSampler"}}, "model_owner": "comfyui_flux"},
        )
        self.assertEqual(submitted["prompt_id"], "prompt-1")
        self.assertEqual(gpu_registry.query(self.registry_dir)["state"], "comfyui_flux_loaded")

        output = self.client.execute(
            "workflow.await_output",
            {"prompt_id": "prompt-1", "timeout_s": 0.1, "poll_interval_s": 0.001},
        )
        self.assertIn("prompt-1", output)
        self.assertEqual(gpu_registry.query(self.registry_dir)["state"], "idle")

    def test_hunyuan_owner_claim_is_supported(self):
        self.client.execute(
            "workflow.submit",
            {"workflow_json": {}, "model_owner": "comfyui_hunyuan"},
        )
        self.assertEqual(gpu_registry.query(self.registry_dir)["state"],
                         "comfyui_hunyuan_loaded")
        self.client.release()

    def test_competing_owner_blocks_before_http_prompt(self):
        gpu_registry.claim(
            self.registry_dir, "blender", "blender-1",
            stale_after_s=60, now_s=time.time(),
        )
        with self.assertRaisesRegex(ComfyUIError, "gpu_occupied"):
            self.client.execute("workflow.submit", {"workflow_json": {}})
        self.assertEqual(self.transport.calls, [])

    def test_submit_failure_releases_claim(self):
        self.transport.fail_prompt = True
        with self.assertRaises(RuntimeError):
            self.client.execute("workflow.submit", {"workflow_json": {}})
        self.assertEqual(gpu_registry.query(self.registry_dir)["state"], "idle")

    def test_list_models_uses_read_only_api_without_gpu_claim(self):
        checkpoints = self.client.execute("model.list_checkpoints")
        loras = self.client.execute("model.list_loras")
        self.assertEqual(checkpoints["ckpt_name"], ["flux-dev-fp8.safetensors"])
        self.assertEqual(loras["lora_name"], ["detail.safetensors"])
        self.assertEqual(gpu_registry.query(self.registry_dir)["state"], "idle")

    def test_output_get_images_does_not_release_unless_completion_path_requests_it(self):
        self.client.execute("workflow.submit", {"workflow_json": {}})
        images = self.client.execute("output.get_images", {"prompt_id": "prompt-1"})
        self.assertEqual(images["images"][0]["filename"], "out.png")
        self.assertEqual(gpu_registry.query(self.registry_dir)["state"], "comfyui_flux_loaded")
        self.client.release()


if __name__ == "__main__":
    unittest.main()
