"""Bounded ComfyUI API wrapper with COMP-041 GPU claim discipline."""

from __future__ import annotations

from dataclasses import dataclass
import json
import time
from pathlib import Path
from typing import Any, Callable, Optional
from urllib import error, request

from gpu_orchestrator import registry as gpu_registry

DEFAULT_BASE_URL = "http://127.0.0.1:8188"
DEFAULT_REGISTRY_DIR = Path("runtime") / "gpu_claims"
COMFYUI_GPU_OWNERS = frozenset({"comfyui_flux", "comfyui_hunyuan"})


class ComfyUIError(RuntimeError):
    """A bounded ComfyUI operator failure."""


@dataclass(frozen=True)
class HeldClaim:
    owner: str
    owner_id: str
    state: str


Transport = Callable[[str, str, Optional[dict]], Any]


class ComfyUIClient:
    """Small ComfyUI client that owns GPU claim/release around queued work."""

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_BASE_URL,
        registry_dir: Path = DEFAULT_REGISTRY_DIR,
        owner_id: str = "comfyui-0",
        stale_after_s: float = 60.0,
        transport: Optional[Transport] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.registry_dir = Path(registry_dir)
        self.owner_id = owner_id
        self.stale_after_s = stale_after_s
        self._transport = transport or self._urllib_transport
        self._held_claim: Optional[HeldClaim] = None

    def execute(self, op: str, params: Optional[dict] = None) -> dict:
        """Execute one bounded operation from the COMP-043 tool surface."""
        params = dict(params or {})
        if op == "workflow.submit":
            return self.submit_workflow(
                params["workflow_json"],
                model_owner=params.get("model_owner", "comfyui_flux"),
            )
        if op == "workflow.queue_status":
            return self.queue_status()
        if op == "workflow.get_output":
            return self.get_output(
                params["prompt_id"],
                release_on_complete=params.get("release_on_complete", True),
            )
        if op == "workflow.await_output":
            return self.await_output(
                params["prompt_id"],
                timeout_s=params.get("timeout_s", 600.0),
                poll_interval_s=params.get("poll_interval_s", 1.0),
                release_on_complete=params.get("release_on_complete", True),
            )
        if op == "workflow.interrupt":
            return self.interrupt(release=params.get("release", True))
        if op == "model.list_checkpoints":
            return self.list_node_inputs("CheckpointLoaderSimple", "ckpt_name")
        if op == "model.list_loras":
            return self.list_node_inputs("LoraLoader", "lora_name")
        if op == "model.get_loaded":
            return self.get_loaded()
        if op == "output.get_images":
            return self.output_items(params["prompt_id"], kind="images")
        if op == "output.get_mesh":
            return self.output_items(params["prompt_id"], kind="mesh")
        if op == "output.save_to":
            raise ComfyUIError("output.save_to requires caller-owned file materialization")
        raise ComfyUIError(f"unknown ComfyUI op: {op}")

    def submit_workflow(
        self,
        workflow_json: dict,
        *,
        model_owner: str = "comfyui_flux",
    ) -> dict:
        """Claim the GPU, submit a workflow, and keep the claim until completion."""
        self._claim(model_owner)
        try:
            response = self._request("POST", "/prompt", {"prompt": workflow_json})
        except Exception:
            self.release()
            raise
        prompt_id = response.get("prompt_id")
        if not prompt_id:
            self.release()
            raise ComfyUIError("ComfyUI /prompt response did not include prompt_id")
        return {
            "prompt_id": prompt_id,
            "gpu_owner": self._held_claim.owner if self._held_claim else None,
            "gpu_state": self._held_claim.state if self._held_claim else None,
        }

    def queue_status(self) -> dict:
        return self._request("GET", "/queue", None)

    def get_output(self, prompt_id: str, *, release_on_complete: bool = True) -> dict:
        history = self._request("GET", f"/history/{prompt_id}", None)
        if release_on_complete and self._history_has_prompt(history, prompt_id):
            self.release()
        return history

    def await_output(
        self,
        prompt_id: str,
        *,
        timeout_s: float,
        poll_interval_s: float,
        release_on_complete: bool = True,
    ) -> dict:
        deadline = time.time() + timeout_s
        while True:
            history = self.get_output(prompt_id, release_on_complete=False)
            if self._history_has_prompt(history, prompt_id):
                if release_on_complete:
                    self.release()
                return history
            if time.time() >= deadline:
                self.release()
                raise ComfyUIError(f"timed out waiting for ComfyUI prompt {prompt_id}")
            time.sleep(poll_interval_s)

    def interrupt(self, *, release: bool = True) -> dict:
        try:
            return self._request("POST", "/interrupt", {})
        finally:
            if release:
                self.release()

    def list_node_inputs(self, node_name: str, input_name: str) -> dict:
        object_info = self._request("GET", "/object_info", None)
        choices = (
            object_info.get(node_name, {})
            .get("input", {})
            .get("required", {})
            .get(input_name, [[]])[0]
        )
        return {input_name: list(choices or [])}

    def get_loaded(self) -> dict:
        return gpu_registry.query(self.registry_dir)

    def output_items(self, prompt_id: str, *, kind: str) -> dict:
        history = self.get_output(prompt_id, release_on_complete=False)
        prompt = history.get(prompt_id, history)
        outputs = prompt.get("outputs", {})
        items = []
        for node_output in outputs.values():
            if kind == "images":
                items.extend(node_output.get("images", []))
            elif kind == "mesh":
                items.extend(node_output.get("meshes", []))
                items.extend(node_output.get("mesh", []))
        return {kind: items}

    def release(self) -> dict:
        if self._held_claim is None:
            return gpu_registry.query(self.registry_dir)
        held = self._held_claim
        result = gpu_registry.release(
            self.registry_dir,
            held.owner,
            held.owner_id,
        )
        if result.granted:
            self._held_claim = None
        return gpu_registry.query(self.registry_dir)

    def _claim(self, owner: str) -> None:
        if owner not in COMFYUI_GPU_OWNERS:
            raise ComfyUIError(f"unknown ComfyUI GPU owner: {owner}")
        result = gpu_registry.claim(
            self.registry_dir,
            owner,
            self.owner_id,
            stale_after_s=self.stale_after_s,
        )
        if not result.granted:
            raise ComfyUIError(
                f"gpu_occupied: {result.state} owned by {result.owner}/{result.owner_id}"
            )
        self._held_claim = HeldClaim(owner=owner, owner_id=self.owner_id, state=result.state)

    def _request(self, method: str, path: str, payload: Optional[dict]) -> Any:
        try:
            return self._transport(method, f"{self.base_url}{path}", payload)
        except error.URLError as exc:
            raise ComfyUIError(f"ComfyUI request failed: {exc}") from exc

    @staticmethod
    def _history_has_prompt(history: dict, prompt_id: str) -> bool:
        return prompt_id in history or bool(history.get("outputs"))

    @staticmethod
    def _urllib_transport(method: str, url: str, payload: Optional[dict]) -> Any:
        data = None
        headers = {}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        req = request.Request(url, data=data, headers=headers, method=method)
        with request.urlopen(req, timeout=30) as resp:  # noqa: S310 - localhost tool API
            body = resp.read().decode("utf-8")
        return json.loads(body) if body else {}
