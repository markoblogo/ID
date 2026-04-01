from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "validate_interop_v1.py"
SCHEMA = REPO_ROOT / "schemas" / "interop-v1.schema.json"


class ValidateInteropV1Tests(unittest.TestCase):
    def test_accepts_valid_document(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            input_path = Path(td) / "interop.v1.json"
            input_path.write_text(
                json.dumps(
                    {
                        "interop_version": "1.0.0",
                        "owner_id": "markoblogo",
                        "generated_at": "2026-04-01",
                        "profiles": {"core": {}, "extended": {}},
                    }
                ),
                encoding="utf-8",
            )

            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--input",
                    str(input_path),
                    "--schema",
                    str(SCHEMA),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("VALID:", proc.stdout)

    def test_rejects_invalid_document(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            input_path = Path(td) / "interop.v1.json"
            input_path.write_text(
                json.dumps(
                    {
                        "interop_version": "not-semver",
                        "owner_id": "",
                        "generated_at": "2026-99-99",
                        "profiles": {"core": []},
                    }
                ),
                encoding="utf-8",
            )

            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--input",
                    str(input_path),
                    "--schema",
                    str(SCHEMA),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 1)
            self.assertIn("INVALID:", proc.stdout)
            self.assertIn("interop_version must be semver string", proc.stdout)
            self.assertIn("owner_id must be non-empty string", proc.stdout)
            self.assertIn("generated_at must be date string YYYY-MM-DD", proc.stdout)
            self.assertIn("profiles missing key: extended", proc.stdout)


if __name__ == "__main__":
    unittest.main()
