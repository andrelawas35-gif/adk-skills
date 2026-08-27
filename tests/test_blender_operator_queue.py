"""Focused regression tests for the bounded Blender operator file queue (WO 2026-08-24-014).

Covers the crash-durable command/result file queue contract in
``tools/production/blender_operator/queue.py`` (Decision 2): the reserved
command-ID scheme, atomic command/result writes, the pending set (commands
whose result ack is missing), and the replay-on-restart semantics that the
tracer's mid-command-kill scenario depends on. No bpy dependency — the queue
logic is pure Python; a fake executor stands in for Blender.
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS_PRODUCTION = Path(__file__).resolve().parent.parent / "tools" / "production"
sys.path.insert(0, str(TOOLS_PRODUCTION))

from blender_operator import queue  # noqa: E402


class TestCommandIdScheme(unittest.TestCase):
    def test_reserved_id_shape(self):
        cid = queue.make_command_id(nonce="a1b2c3d4", seq=1)
        self.assertEqual(cid, "CMD-a1b2c3d4-0001")
        self.assertTrue(queue.is_command_id(cid))

    def test_default_nonce_is_8_hex(self):
        cid = queue.make_command_id(seq=7)
        self.assertTrue(queue.is_command_id(cid))
        self.assertRegex(cid, r"^CMD-[0-9a-f]{8}-0007$")

    def test_invalid_seq_rejected(self):
        with self.assertRaises(ValueError):
            queue.make_command_id(seq=0)
        with self.assertRaises(ValueError):
            queue.make_command_id(seq=10000)

    def test_sequence_zero_pad(self):
        self.assertEqual(queue.make_command_id(nonce="a1b2c3d4", seq=42),
                         "CMD-a1b2c3d4-0042")


class TestQueueFiles(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.queue_dir = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_write_and_read_command(self):
        cid = queue.write_command(self.queue_dir, "scene.get_objects",
                                  {"foo": "bar"}, command_id="CMD-a1b2c3d4-0001")
        self.assertEqual(cid, "CMD-a1b2c3d4-0001")
        cmd = queue.read_command(self.queue_dir, cid)
        self.assertEqual(cmd["op"], "scene.get_objects")
        self.assertEqual(cmd["params"], {"foo": "bar"})
        self.assertEqual(cmd["schema_version"], 1)

    def test_pending_is_commands_without_result(self):
        queue.write_command(self.queue_dir, "scene.get_objects",
                            command_id="CMD-a1b2c3d4-0001")
        queue.write_command(self.queue_dir, "scene.get_objects",
                            command_id="CMD-a1b2c3d4-0002")
        queue.write_result(self.queue_dir, "CMD-a1b2c3d4-0001", "ok", data={})
        self.assertEqual(queue.list_pending(self.queue_dir),
                         ["CMD-a1b2c3d4-0002"])

    def test_replay_safe_process_once(self):
        queue.write_command(self.queue_dir, "scene.get_objects",
                            command_id="CMD-a1b2c3d4-0001")
        processed = queue.process_once(
            self.queue_dir, execute=lambda op, p: (True, {"objects": []}, None))
        self.assertEqual(processed, ["CMD-a1b2c3d4-0001"])
        # A second pass must NOT re-execute (result ack exists).
        processed = queue.process_once(
            self.queue_dir, execute=lambda op, p: (True, {}, None))
        self.assertEqual(processed, [])

    def test_error_command_gets_error_ack(self):
        queue.write_command(self.queue_dir, "unknown.op",
                            command_id="CMD-a1b2c3d4-0001")
        queue.process_once(
            self.queue_dir,
            execute=lambda op, p: (False, None,
                                   {"code": "unknown_op", "message": f"no {op}"}))
        result = queue.read_result(self.queue_dir, "CMD-a1b2c3d4-0001")
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["error"]["code"], "unknown_op")

    def test_crash_simulation_replays_pending(self):
        # Simulate the TDR scenario: a command file is on disk, no result ack
        # (Blender died mid-command). A fresh process must replay it.
        queue.write_command(self.queue_dir, "scene.get_objects",
                            command_id="CMD-a1b2c3d4-0001")
        queue.write_result(self.queue_dir, "CMD-a1b2c3d4-0002", "ok", data={})
        pending = queue.list_pending(self.queue_dir)
        self.assertEqual(pending, ["CMD-a1b2c3d4-0001"])
        processed = queue.process_once(
            self.queue_dir, execute=lambda op, p: (True, {"objects": ["Cube"]}, None))
        self.assertEqual(processed, ["CMD-a1b2c3d4-0001"])
        result = queue.read_result(self.queue_dir, "CMD-a1b2c3d4-0001")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["data"], {"objects": ["Cube"]})


if __name__ == "__main__":
    unittest.main()
