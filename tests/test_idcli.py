from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
IDCLI = REPO_ROOT / "idcli.py"


class IdCliTest(unittest.TestCase):
    def test_help_lists_known_commands(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(IDCLI), "--help"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertIn("bootstrap-owner", completed.stdout)
        self.assertIn("init", completed.stdout)
        self.assertIn("migrate", completed.stdout)
        self.assertIn("export-compact", completed.stdout)
        self.assertIn("refresh-soul", completed.stdout)

    def test_validate_observed_passes(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(IDCLI), "validate-observed"],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0)
        self.assertIn(
            "VALID: evidence/observed-behavior/chatgpt.family.v1.json",
            completed.stdout,
        )


if __name__ == "__main__":
    unittest.main()
