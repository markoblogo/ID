from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "export_context_compact.py"


def write_interop(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "interop_version": "1.0.0",
                "owner_id": "markoblogo",
                "generated_at": "2026-04-01",
                "profiles": {
                    "core": {
                        "metadata": {
                            "profile_id": "markoblogo",
                            "owner_alias": "markoblogo",
                            "version": "0.1.0",
                            "created_at": "2026-03-31",
                            "updated_at": "2026-04-01",
                            "freshness_ttl_days": 14,
                            "confidence_notes": "test",
                            "trust_level": "trusted",
                        },
                        "communication": ["direct"],
                        "rules": {
                            "always_do": ["verify"],
                            "never_do": ["invent"],
                            "ask_before": ["destructive changes"],
                            "default_assumptions": ["prefer local files"],
                        },
                        "quality_bar": ["correct before elegant"],
                        "priority_domains": ["coding"],
                        "tool_notes": ["keep diffs small"],
                        "extensions": {},
                    },
                    "extended": {},
                },
            }
        ),
        encoding="utf-8",
    )


def write_policy(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "policy_version": "1.0.0",
                "owner_id": "markoblogo",
                "updated_at": "2026-04-01",
                "default_access": "local_only",
                "task_classes": ["coding"],
                "rules": [
                    {
                        "field_path": "profiles.core.communication",
                        "access": "always_share",
                        "rationale": "safe",
                    },
                    {
                        "field_path": "profiles.core.rules.ask_before",
                        "access": "always_share",
                        "rationale": "safety-critical",
                    },
                    {
                        "field_path": "profiles.core.priority_domains",
                        "access": "always_share",
                        "rationale": "routing",
                    },
                    {
                        "field_path": "profiles.core.quality_bar",
                        "access": "task_class_scoped",
                        "allowed_task_classes": ["coding"],
                        "rationale": "task relevant",
                    },
                    {
                        "field_path": "profiles.core.tool_notes",
                        "access": "local_only",
                        "rationale": "private",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


class ExportContextCompactTests(unittest.TestCase):
    def test_exports_compact_context(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            profiles_root = root / "profiles"
            owner_root = profiles_root / "markoblogo"
            write_interop(owner_root / "interop.v1.json")

            output = owner_root / "context.compact.json"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--owner-id",
                    "markoblogo",
                    "--profiles-root",
                    str(profiles_root),
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
            self.assertEqual(payload["trust_level"], "trusted")
            self.assertEqual(payload["communication"], ["direct"])
            self.assertNotIn("Privacy policy applied", payload["loss_notes"])

    def test_applies_privacy_policy_for_generic_and_task_scoped_exports(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            profiles_root = root / "profiles"
            owner_root = profiles_root / "markoblogo"
            write_interop(owner_root / "interop.v1.json")
            write_policy(owner_root / "privacy-policy.v1.json")

            generic_output = owner_root / "context.generic.json"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--owner-id",
                    "markoblogo",
                    "--profiles-root",
                    str(profiles_root),
                    "--output",
                    str(generic_output),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            generic_payload = json.loads(generic_output.read_text(encoding="utf-8"))
            self.assertEqual(generic_payload["communication"], ["direct"])
            self.assertEqual(generic_payload["rules"]["ask_before"], ["destructive changes"])
            self.assertEqual(generic_payload["rules"]["always_do"], [])
            self.assertEqual(generic_payload["quality_bar"], [])
            self.assertEqual(generic_payload["tool_notes"], [])
            self.assertTrue(any("Provide --task-class" in note for note in generic_payload["loss_notes"]))

            scoped_output = owner_root / "context.coding.json"
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
                    str(scoped_output),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            scoped_payload = json.loads(scoped_output.read_text(encoding="utf-8"))
            self.assertEqual(scoped_payload["quality_bar"], ["correct before elegant"])
            self.assertEqual(scoped_payload["tool_notes"], [])
            self.assertTrue(any(note == "Task-class export: coding" for note in scoped_payload["loss_notes"]))


if __name__ == "__main__":
    unittest.main()
