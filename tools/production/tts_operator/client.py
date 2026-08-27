"""Bounded local Piper TTS operator for COMP-044."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import subprocess
import wave
from typing import Optional


LOCAL_TTS_ROOT = Path(r"C:\Users\Andre\Documents\Work_Studio\local_tts")
DEFAULT_PIPER_EXE = (
    LOCAL_TTS_ROOT / "piper-2023.11.14-2" / "piper" / "piper.exe"
)
DEFAULT_VOICE_ID = "en_US-lessac-medium"
DEFAULT_VOICE_MODEL = LOCAL_TTS_ROOT / "voices" / f"{DEFAULT_VOICE_ID}.onnx"
DEFAULT_VOICE_CONFIG = LOCAL_TTS_ROOT / "voices" / f"{DEFAULT_VOICE_ID}.onnx.json"
DEFAULT_OUTPUT_DIR = Path("runtime") / "tts_takes"
TIER_USED = "local_piper"


class TTSError(RuntimeError):
    """A bounded TTS operator failure."""


@dataclass(frozen=True)
class PiperVoice:
    voice_id: str
    model_path: Path
    config_path: Path
    tier_used: str = TIER_USED


class PiperTTSClient:
    """Small Piper wrapper that returns WAV take metadata without judging takes."""

    TAKE_PRESETS = (
        {"suffix": "A", "noise_scale": 0.60, "length_scale": 1.00, "noise_w": 0.75},
        {"suffix": "B", "noise_scale": 0.67, "length_scale": 0.95, "noise_w": 0.80},
        {"suffix": "C", "noise_scale": 0.74, "length_scale": 1.05, "noise_w": 0.85},
        {"suffix": "D", "noise_scale": 0.67, "length_scale": 1.12, "noise_w": 0.70},
    )

    def __init__(
        self,
        *,
        piper_exe: Path = DEFAULT_PIPER_EXE,
        voice_model: Path = DEFAULT_VOICE_MODEL,
        voice_config: Path = DEFAULT_VOICE_CONFIG,
        output_dir: Path = DEFAULT_OUTPUT_DIR,
        runner=subprocess.run,
    ) -> None:
        self.piper_exe = Path(piper_exe)
        self.voice = PiperVoice(
            voice_id=Path(voice_model).stem,
            model_path=Path(voice_model),
            config_path=Path(voice_config),
        )
        self.output_dir = Path(output_dir)
        self._runner = runner

    def execute(self, op: str, params: Optional[dict] = None) -> dict:
        """Execute one bounded operation from the COMP-044 tracer surface."""
        params = dict(params or {})
        if op == "tts.list_voices":
            return self.list_voices()
        if op == "tts.generate":
            return self.generate(
                text=params["text"],
                voice_id=params.get("voice_id", self.voice.voice_id),
                performance_params=params.get("performance_params", {}),
                take_count=params.get("take_count", 1),
                output_dir=Path(params["output_dir"]) if "output_dir" in params else None,
            )
        raise TTSError(f"unknown TTS op: {op}")

    def list_voices(self) -> dict:
        self._require_local_files()
        return {
            "voices": [
                {
                    "voice_id": self.voice.voice_id,
                    "tier_used": self.voice.tier_used,
                    "model_path": str(self.voice.model_path),
                    "config_path": str(self.voice.config_path),
                }
            ]
        }

    def generate(
        self,
        *,
        text: str,
        voice_id: str = DEFAULT_VOICE_ID,
        performance_params: Optional[dict] = None,
        take_count: int = 1,
        output_dir: Optional[Path] = None,
    ) -> dict:
        """Generate deterministic A/B/C/D WAV takes and return metadata."""
        self._require_local_files()
        if not text or not text.strip():
            raise TTSError("tts.generate requires non-empty text")
        if voice_id != self.voice.voice_id:
            raise TTSError(f"unknown local_piper voice_id: {voice_id}")
        if take_count < 1 or take_count > len(self.TAKE_PRESETS):
            raise TTSError("take_count must be between 1 and 4")

        output_root = Path(output_dir) if output_dir is not None else self.output_dir
        output_root.mkdir(parents=True, exist_ok=True)
        params = dict(performance_params or {})

        takes = []
        for index, preset in enumerate(self.TAKE_PRESETS[:take_count], start=1):
            take_id = f"{preset['suffix']}"
            wav_path = output_root / f"{_slug(text)}-{take_id}.wav"
            synthesis = self._synthesis_params(params, preset)
            self._run_piper(text, wav_path, synthesis)
            takes.append({
                "take_id": take_id,
                "file_path": str(wav_path),
                "duration_seconds": _wav_duration_seconds(wav_path),
                "tier_used": TIER_USED,
                "voice_id": self.voice.voice_id,
                "performance_params": synthesis,
                "index": index,
            })

        return {
            "tier_used": TIER_USED,
            "voice_id": self.voice.voice_id,
            "take_count": take_count,
            "takes": takes,
        }

    def _require_local_files(self) -> None:
        for path in (self.piper_exe, self.voice.model_path, self.voice.config_path):
            if not path.exists():
                raise TTSError(f"missing local_piper dependency: {path}")

    @staticmethod
    def _synthesis_params(performance_params: dict, preset: dict) -> dict:
        allowed = {
            "noise_scale": preset["noise_scale"],
            "length_scale": preset["length_scale"],
            "noise_w": preset["noise_w"],
            "sentence_silence": performance_params.get("sentence_silence", 0.2),
        }
        for key in ("noise_scale", "length_scale", "noise_w", "sentence_silence"):
            if key in performance_params:
                allowed[key] = performance_params[key]
        return allowed

    def _run_piper(self, text: str, wav_path: Path, synthesis: dict) -> None:
        cmd = [
            str(self.piper_exe),
            "--model", str(self.voice.model_path),
            "--config", str(self.voice.config_path),
            "--output_file", str(wav_path),
            "--noise_scale", str(synthesis["noise_scale"]),
            "--length_scale", str(synthesis["length_scale"]),
            "--noise_w", str(synthesis["noise_w"]),
            "--sentence_silence", str(synthesis["sentence_silence"]),
            "--quiet",
        ]
        result = self._runner(
            cmd,
            input=text,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode != 0:
            message = (result.stderr or result.stdout or "piper failed").strip()
            raise TTSError(f"local_piper failed: {message}")
        if not wav_path.exists():
            raise TTSError(f"local_piper produced no WAV file: {wav_path}")


def _slug(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return (slug[:48] or "take").strip("-")


def _wav_duration_seconds(path: Path) -> float:
    with wave.open(str(path), "rb") as wav:
        frames = wav.getnframes()
        rate = wav.getframerate()
    if rate <= 0:
        raise TTSError(f"invalid WAV sample rate: {path}")
    return round(frames / rate, 3)
