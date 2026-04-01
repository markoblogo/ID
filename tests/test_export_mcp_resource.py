from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_export_context_compact import write_interop, write_policy

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "export_mcp_resource.py"


class ExportMcpResourceTests(unittest.TestCase):
    def test_exports_policy_aware_mcp_resource(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            profiles_root = root / "profiles"
            owner_root = profiles_root / "markoblogo"
            write_interop(owner_root / "interop.v1.json")
            write_policy(owner_root / "privacy-policy.v1.json")

            output = owner_root / "mcp.context.resource.json"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--owner-id",
                    "markoblogo",
                    "--profiles-root",
                    str(profiles_root),
                    "--task-class",
                    "coding",
                    "--output",
                    str(output),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["owner_id"], "markoblogo")
            self.assertEqual(payload["uri"], "id://markoblogo/context.compact")
            self.assertEqual(payload["policy"]["applied"], True)
            self.assertEqual(payload["policy"]["task_class"], "coding")
            self.assertEqual(payload["contents"]["quality_bar"], ["correct before elegant"])
            self.assertEqual(payload["contents"]["tool_notes"], [])
            self.assertIn("Privacy policy applied", payload["contents"]["loss_notes"])
