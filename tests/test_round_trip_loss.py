from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_COMPACT = REPO_ROOT / "scripts" / "export_context_compact.py"
EXPORT_MCP = REPO_ROOT / "scripts" / "export_mcp_resource.py"
IMPORT_COMPACT = REPO_ROOT / "scripts" / "import_context_compact.py"
IMPORT_MCP = REPO_ROOT / "scripts" / "import_mcp_resource.py"


def write_interop(owner_dir: Path) -> None:
    payload = {
        "owner_id": "demo",
        "profiles": {
            "core": {
                "metadata": {
                    "version": "0.1.0",
                    "updated_at": "2026-04-01",
                    "freshness_ttl_days": 14,
                    "trust_level": "trusted",
                },
                "communication": ["direct"],
                "rules": {
                    "always_do": ["make assumptions explicit"],
                    "never_do": ["invent user facts"],
                    "ask_before": ["destructive changes"],
                    "default_assumptions": ["reproducible workflow"],
                },
                "quality_bar": ["correct before elegant"],
                "priority_domains": ["protocol design"],
                "tool_notes": ["use explicit operations"],
            }
        },
    }
    (owner_dir / "interop.v1.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def write_policy(owner_dir: Path) -> None:
    payload = {
        "policy_version": "1.0.0",
        "owner_id": "demo",
        "always_share": [
            "profiles.core.communication",
            "profiles.core.rules.always_do",
            "profiles.core.rules.never_do",
            "profiles.core.rules.ask_before",
            "profiles.core.rules.default_assumptions",
            "profiles.core.quality_bar",
            "profiles.core.priority_domains",
            "profiles.core.tool_notes",
        ],
        "local_only": [],
        "task_class_scoped": {},
    }
    (owner_dir / "privacy-policy.v1.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


class RoundTripLossTests(unittest.TestCase):
    def test_compact_round_trip_preserves_core_signals_and_exposes_loss(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            owner_dir = Path(tmp) / "demo"
            owner_dir.mkdir(parents=True)
            write_interop(owner_dir)
            write_policy(owner_dir)

            compact_path = owner_dir / "context.compact.json"
            draft_path = owner_dir / "draft.from-context-compact.md"
            subprocess.run(
                [sys.executable, str(EXPORT_COMPACT), "--owner-id", "demo", "--profiles-root", tmp],
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                [sys.executable, str(IMPORT_COMPACT), "--owner-id", "demo", "--profiles-root", tmp],
                capture_output=True,
                text=True,
                check=True,
            )
            compact = json.loads(compact_path.read_text(encoding="utf-8"))
            draft = draft_path.read_text(encoding="utf-8")

        self.assertIn("make assumptions explicit", draft)
        self.assertIn("Extended workflows omitted", draft)
        self.assertIn("Use full profile or interop.v1.json for richer context", compact["loss_notes"])

    def test_mcp_round_trip_preserves_policy_context_and_exposes_loss(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            owner_dir = Path(tmp) / "demo"
            owner_dir.mkdir(parents=True)
            write_interop(owner_dir)
            write_policy(owner_dir)

            mcp_path = owner_dir / "mcp.context.resource.json"
            draft_path = owner_dir / "draft.from-mcp.md"
            subprocess.run(
                [sys.executable, str(EXPORT_MCP), "--owner-id", "demo", "--profiles-root", tmp, "--task-class", "coding"],
                capture_output=True,
                text=True,
                check=True,
            )
            subprocess.run(
                [sys.executable, str(IMPORT_MCP), "--owner-id", "demo", "--profiles-root", tmp],
                capture_output=True,
                text=True,
                check=True,
            )
            mcp = json.loads(mcp_path.read_text(encoding="utf-8"))
            draft = draft_path.read_text(encoding="utf-8")

        self.assertEqual(mcp["policy"]["task_class"], "coding")
        self.assertIn("policy_task_class: `coding`", draft)
        self.assertIn("lossy import candidate", draft)


if __name__ == "__main__":
    unittest.main()
