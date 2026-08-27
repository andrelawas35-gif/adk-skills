import subprocess
import sys
import tempfile
import unittest
import wave
from pathlib import Path


TOOLS_PRODUCTION = Path(__file__).resolve().parent.parent / "tools" / "production"
sys.path.insert(0, str(TOOLS_PRODUCTION))

from tts_operator import DEFAULT_VOICE_ID, PiperTTSClient, TTSError  # noqa: E402


class FakeCompletedProcess:
    returncode = 0
    stdout = ""
    stderr = ""


def write_wav(path: Path, seconds: float = 0.25) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    sample_rate = 22050
    frames = int(sample_rate * seconds)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(sample_rate)
        wav.writeframes(b"\x00\x00" * frames)


class FakeRunner:
    def __init__(self, fail: bool = False):
        self.calls = []
        self.fail = fail

    def __call__(self, cmd, *, input, text, capture_output, check):
        self.calls.append({
            "cmd": cmd,
            "input": input,
            "text": text,
            "capture_output": capture_output,
            "check": check,
        })
        if self.fail:
            return subprocess.CompletedProcess(cmd, 2, stdout="", stderr="boom")
        out_path = Path(cmd[cmd.index("--output_file") + 1])
        write_wav(out_path)
        return FakeCompletedProcess()


class PiperTTSClientTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.piper = self.root / "piper.exe"
        self.model = self.root / f"{DEFAULT_VOICE_ID}.onnx"
        self.config = self.root / f"{DEFAULT_VOICE_ID}.onnx.json"
        for path in (self.piper, self.model, self.config):
            path.write_text("stub", encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def client(self, runner=None):
        return PiperTTSClient(
            piper_exe=self.piper,
            voice_model=self.model,
            voice_config=self.config,
            output_dir=self.root / "takes",
            runner=runner or FakeRunner(),
        )

    def test_list_voices_reports_local_piper_voice(self):
        result = self.client().execute("tts.list_voices")
        self.assertEqual(result["voices"][0]["voice_id"], DEFAULT_VOICE_ID)
        self.assertEqual(result["voices"][0]["tier_used"], "local_piper")
        self.assertEqual(result["voices"][0]["model_path"], str(self.model))

    def test_generate_four_takes_returns_metadata_without_judgment(self):
        runner = FakeRunner()
        result = self.client(runner).execute(
            "tts.generate",
            {
                "text": "Hello from the local TTS tracer.",
                "voice_id": DEFAULT_VOICE_ID,
                "performance_params": {"sentence_silence": 0.1},
                "take_count": 4,
            },
        )
        self.assertEqual(result["tier_used"], "local_piper")
        self.assertEqual(result["take_count"], 4)
        self.assertEqual([take["take_id"] for take in result["takes"]], ["A", "B", "C", "D"])
        self.assertEqual(len(runner.calls), 4)
        for take in result["takes"]:
            self.assertTrue(Path(take["file_path"]).exists())
            self.assertGreater(take["duration_seconds"], 0)
            self.assertEqual(take["voice_id"], DEFAULT_VOICE_ID)
            self.assertEqual(take["tier_used"], "local_piper")
            self.assertNotIn("quality", take)
            self.assertNotIn("selected", take)

    def test_unknown_voice_rejected_before_piper_runs(self):
        runner = FakeRunner()
        with self.assertRaisesRegex(TTSError, "unknown local_piper voice_id"):
            self.client(runner).execute(
                "tts.generate",
                {"text": "Hello", "voice_id": "unknown", "take_count": 1},
            )
        self.assertEqual(runner.calls, [])

    def test_take_count_is_bounded_to_abcd(self):
        with self.assertRaisesRegex(TTSError, "take_count must be between 1 and 4"):
            self.client().execute("tts.generate", {"text": "Hello", "take_count": 5})

    def test_missing_dependency_is_reported(self):
        self.model.unlink()
        with self.assertRaisesRegex(TTSError, "missing local_piper dependency"):
            self.client().execute("tts.list_voices")

    def test_piper_failure_is_structured_error(self):
        with self.assertRaisesRegex(TTSError, "local_piper failed: boom"):
            self.client(FakeRunner(fail=True)).execute(
                "tts.generate",
                {"text": "Hello", "take_count": 1},
            )


if __name__ == "__main__":
    unittest.main()
