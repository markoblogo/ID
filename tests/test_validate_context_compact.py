from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "validate_context_compact.py"
SCHEMA = REPO_ROOT / "schemas" / "context-compact-v0.schema.json"


class ValidateContextCompactTests(unittest.TestCase):
    def test_accepts_valid_document(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            input_path = Path(td) / "context.compact.json"
            input_path.write_text(
                json.dumps(
                    {
                        "context_version": "0.1.0",
                        "owner_id": "markoblogo",
                        "updated_at": "2026-04-01",
                        "freshness_ttl_days": 14,
                        "trust_level": "trusted",
                        "communication": ["direct"],
                        "rules": {
                            "always_do": ["verify assumptions"],
                            "never_do": ["invent facts"],
                            "ask_before": ["destructive changes"],
                            "default_assumptions": ["prefer local files"],
                        },
                        "quality_bar": ["correct before elegant"],
                        "priority_domains": ["coding"],
                        "tool_notes": ["codex: keep diffs small"],
                        "loss_notes": ["Extended workflows omitted"],
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
            input_path = Path(td) / "context.compact.json"
            input_path.write_text(
                json.dumps(
                    {
                        "context_version": "invalid",
                        "owner_id": "",
                        "updated_at": "2026-99-99",
                        "freshness_ttl_days": 0,
                        "trust_level": "unknown",
                        "communication": "direct",
                        "rules": {"always_do": []},
                        "quality_bar": [],
                        "priority_domains": [],
                        "tool_notes": [],
                        "loss_notes": [],
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
            self.assertIn("context_version must be semver string", proc.stdout)
            self.assertIn("owner_id must be non-empty string", proc.stdout)
            self.assertIn("updated_at must be date string YYYY-MM-DD", proc.stdout)
            self.assertIn("freshness_ttl_days must be integer >= 1", proc.stdout)
            self.assertIn("trust_level must be one of", proc.stdout)
            self.assertIn("communication must be array of strings", proc.stdout)
            self.assertIn("rules missing key: never_do", proc.stdout)


if __name__ == "__main__":
    unittest.main()
