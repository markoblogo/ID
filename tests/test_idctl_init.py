from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "idctl_init.py"


class IdctlInitTests(unittest.TestCase):
    def test_init_dry_run_without_interactive_reuses_owner_alias(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--owner-id",
                    "demo",
                    "--owner-alias",
                    "Demo Team",
                    "--profiles-root",
                    str(Path(tmp) / "profiles"),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            # bootstrap script writes files, including minimal + handshake + policy
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            owner_dir = Path(tmp) / "profiles" / "demo"
            self.assertTrue((owner_dir / "profile.minimal.md").exists())
            self.assertTrue((owner_dir / "handshake.md").exists())
            self.assertTrue((owner_dir / "privacy-policy.v1.json").exists())
