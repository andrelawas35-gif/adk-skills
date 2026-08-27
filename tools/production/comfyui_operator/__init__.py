"""Bounded ComfyUI operator (COMP-043).

Wraps the local ComfyUI HTTP API and gates GPU-heavy workflow/model operations
through the COMP-041 file-backed GPU claim registry.
"""

from .client import ComfyUIClient, ComfyUIError

__all__ = ["ComfyUIClient", "ComfyUIError"]
