from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "migrate.py"


class MigrateTests(unittest.TestCase):
    def test_dry_run_reports_would_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            owner_dir = Path(tmp) / "profiles" / "demo"
            owner_dir.mkdir(parents=True)
            (owner_dir / "profile.core.md").write_text(
                "\n".join(
                    [
                        "---",
                        'profile_id: "demo"',
                        "---",
                        "# Core",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--owner-id",
                    "demo",
                    "--from",
                    "v0.1",
                    "--to",
                    "v0.2",
                    "--profiles-root",
                    str(Path(tmp) / "profiles"),
                    "--dry-run",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(proc.returncode, 0)
        self.assertIn("would_write", proc.stdout)

    def test_json_output_is_machine_readable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            owner_dir = Path(tmp) / "profiles" / "demo"
            owner_dir.mkdir(parents=True)
            (owner_dir / "profile.core.md").write_text(
                "\n".join(
                    [
                        "---",
                        'profile_id: "demo"',
                        "---",
                        "# Core",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--owner-id",
                    "demo",
                    "--from",
                    "v0.1",
                    "--to",
                    "v0.2",
                    "--profiles-root",
                    str(Path(tmp) / "profiles"),
                    "--json",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            payload = json.loads(proc.stdout.strip())
        self.assertEqual(payload["from"], "v0.1")
        self.assertEqual(payload["to"], "v0.2")
        self.assertFalse(payload["dry_run"])
