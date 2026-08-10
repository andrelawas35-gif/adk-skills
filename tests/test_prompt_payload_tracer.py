import json
import tempfile
import unittest
from pathlib import Path

from tools.prompt_payload_tracer import TraceError, baseline, load_spec, package, scenario_trace


ROOT = Path(__file__).resolve().parents[1]


class PromptPayloadTracerContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest, cls.scenarios = load_spec(ROOT)

    def test_dependency_closure_is_deterministic_and_scenario_scoped(self):
        first = scenario_trace(self.manifest, self.scenarios, "capture")
        second = scenario_trace(self.manifest, self.scenarios, "capture")
        self.assertEqual(first, second)
        self.assertEqual(first["loaded_nodes"], ["kernel", "capture"])
        self.assertNotIn("conductor", first["loaded_nodes"])

    def test_activation_loads_conductor_and_rejects_unapproved_entry(self):
        trace = scenario_trace(self.manifest, self.scenarios, "activate")
        self.assertIn("conductor", trace["loaded_nodes"])
        self.assertNotIn("capture", trace["loaded_nodes"])
        with self.assertRaisesRegex(TraceError, "authorization required"):
            scenario_trace(self.manifest, self.scenarios, "activate", authorized=False)

    def test_package_is_deterministic_dependency_closed_and_has_no_platform_appendix(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "package"
            first = package(ROOT, output, "capture")
            first_bytes = (output / "package.json").read_bytes()
            second = package(ROOT, output, "capture")
            self.assertEqual(first, second)
            self.assertEqual(first_bytes, (output / "package.json").read_bytes())
            skill = (output / "SKILL.md").read_text(encoding="utf-8")
            self.assertNotIn("## Platform Adapter", skill)
            self.assertNotIn("platform-specific metadata", skill)
            self.assertEqual(set(second["manifest"]["loaded_nodes"]), {"kernel", "capture"})

    def test_package_manifest_has_one_entry_per_output_file(self):
        with tempfile.TemporaryDirectory() as temp:
            result = package(ROOT, Path(temp) / "package", "activate")
            paths = [entry["path"] for entry in result["manifest"]["files"]]
            self.assertEqual(len(paths), len(set(paths)))
            self.assertIn("modules/activation-route.md", paths)

    def test_generated_description_is_meaningful_and_trigger_bearing(self):
        self.assertIn("turn-signal-into-work", self.manifest["description"])
        self.assertIn("signal", self.manifest["description"])

    def test_baseline_is_recorded_for_comparison(self):
        result = baseline(ROOT)
        self.assertGreater(result["total_bytes"], 0)
        self.assertGreater(result["total_words"], 0)
        self.assertTrue(result["source"].endswith("alawas-thinking-turn-signal-into-work"))

    def test_unknown_dependency_and_scenario_fail_closed(self):
        broken = json.loads(json.dumps(self.manifest))
        broken["nodes"]["capture"]["requires"] = ["does-not-exist"]
        with self.assertRaisesRegex(TraceError, "unknown dependency"):
            scenario_trace(broken, self.scenarios, "capture")
        with self.assertRaisesRegex(TraceError, "unknown scenario"):
            scenario_trace(self.manifest, self.scenarios, "not-a-scenario")


if __name__ == "__main__":
    unittest.main()
