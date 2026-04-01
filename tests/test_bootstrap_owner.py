from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "bootstrap_owner.py"


class BootstrapOwnerTests(unittest.TestCase):
    def test_bootstrap_creates_starter_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            template_dir = Path(tmp) / "templates"
            template_dir.mkdir()
            (template_dir / "profile.minimal.md").write_text(
                '\n'.join(
                    [
                        '---',
                        'profile_id: "owner-id"',
                        'owner_alias: "owner-alias"',
                        'created_at: "YYYY-MM-DD"',
                        'updated_at: "YYYY-MM-DD"',
                        '---',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            profiles_root = Path(tmp) / "profiles"
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--owner-id",
                    "demo",
                    "--owner-alias",
                    "demo-alias",
                    "--profiles-root",
                    str(profiles_root),
                    "--today",
                    "2026-04-01",
                ],
                cwd=tmp,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            owner_dir = profiles_root / "demo"
            minimal = (owner_dir / "profile.minimal.md").read_text(encoding="utf-8")
            policy = json.loads((owner_dir / "privacy-policy.v1.json").read_text(encoding="utf-8"))
            handshake = (owner_dir / "handshake.md").read_text(encoding="utf-8")

        self.assertIn('profile_id: "demo"', minimal)
        self.assertIn('owner_alias: "demo-alias"', minimal)
        self.assertEqual(policy["owner_id"], "demo")
        self.assertIn("confirm the active profile source and freshness", handshake)

    def test_bootstrap_refuses_overwrite_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            template_dir = Path(tmp) / "templates"
            template_dir.mkdir()
            (template_dir / "profile.minimal.md").write_text('profile_id: "owner-id"\n', encoding="utf-8")
            owner_dir = Path(tmp) / "profiles" / "demo"
            owner_dir.mkdir(parents=True)
            (owner_dir / "profile.minimal.md").write_text("existing\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--owner-id",
                    "demo",
                    "--profiles-root",
                    str(Path(tmp) / "profiles"),
                    "--today",
                    "2026-04-01",
                ],
                cwd=tmp,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Refusing to overwrite existing file", result.stderr)


if __name__ == "__main__":
    unittest.main()
