from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
HOOK = REPO_ROOT / "scripts" / "run_integration_hook.sh"


class RunIntegrationHookTests(unittest.TestCase):
    def test_pre_task_exposes_soul_first_bootstrap(self) -> None:
        completed = subprocess.run(
            [
                "bash",
                str(HOOK),
                "pre_task",
                "--owner-id",
                "markoblogo",
                "--target",
                "agentsmd",
            ],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("soul=profiles/markoblogo/soul.md", completed.stdout)
        self.assertIn(
            "primary_human_bootstrap=profiles/markoblogo/soul.md",
            completed.stdout,
        )
        self.assertIn(
            "preferred_human_bootstrap=profiles/markoblogo/soul.md|profiles/markoblogo/profile.core.md|profiles/markoblogo/handshake.md",
            completed.stdout,
        )


if __name__ == "__main__":
    unittest.main()
