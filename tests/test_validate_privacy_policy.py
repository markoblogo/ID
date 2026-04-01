from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "validate_privacy_policy.py"
SCHEMA = REPO_ROOT / "schemas" / "privacy-policy-v1.schema.json"


class ValidatePrivacyPolicyTests(unittest.TestCase):
    def test_accepts_valid_document(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            input_path = Path(td) / "privacy-policy.v1.json"
            input_path.write_text(
                json.dumps(
                    {
                        "policy_version": "1.0.0",
                        "owner_id": "markoblogo",
                        "updated_at": "2026-04-01",
                        "default_access": "task_class_scoped",
                        "task_classes": ["coding", "research"],
                        "rules": [
                            {
                                "field_path": "profiles.core.communication",
                                "access": "always_share",
                                "rationale": "communication preferences are low-risk operational context",
                            },
                            {
                                "field_path": "profiles.extended.environment_assumptions",
                                "access": "local_only",
                                "rationale": "environment details may expose local infrastructure",
                            },
                            {
                                "field_path": "profiles.extended.domain_workflows",
                                "access": "task_class_scoped",
                                "allowed_task_classes": ["coding", "research"],
                                "rationale": "workflow details should be released only for relevant task classes",
                            },
                        ],
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
            input_path = Path(td) / "privacy-policy.v1.json"
            input_path.write_text(
                json.dumps(
                    {
                        "policy_version": "invalid",
                        "owner_id": "",
                        "updated_at": "2026-99-99",
                        "default_access": "unknown",
                        "task_classes": [],
                        "rules": [
                            {
                                "field_path": "profiles.core.communication",
                                "access": "task_class_scoped",
                                "allowed_task_classes": ["missing"],
                                "rationale": "",
                            },
                            {
                                "field_path": "profiles.core.communication",
                                "access": "always_share",
                                "allowed_task_classes": ["coding"],
                                "rationale": "dup",
                            },
                        ],
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
            self.assertIn("policy_version must be semver string", proc.stdout)
            self.assertIn("owner_id must be non-empty string", proc.stdout)
            self.assertIn("updated_at must be date string YYYY-MM-DD", proc.stdout)
            self.assertIn("default_access must be one of", proc.stdout)
            self.assertIn("task_classes must be non-empty array", proc.stdout)
            self.assertIn("allowed_task_classes has unknown task class", proc.stdout)
            self.assertIn("duplicate field_path", proc.stdout)
            self.assertIn("allowed_task_classes only allowed when access=task_class_scoped", proc.stdout)


if __name__ == "__main__":
    unittest.main()
