from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "import_mcp_resource.py"


def sample_context() -> dict:
    return {
        "context_version": "0.1.0",
        "owner_id": "markoblogo",
        "updated_at": "2026-04-01",
        "freshness_ttl_days": 30,
        "trust_level": "trusted",
        "communication": ["direct, pragmatic, no fluff"],
        "rules": {
            "always_do": ["make assumptions explicit"],
            "never_do": ["invent user facts"],
            "ask_before": ["destructive changes"],
            "default_assumptions": ["user wants reproducible workflow"],
        },
        "quality_bar": ["correct before elegant"],
        "priority_domains": ["protocol design"],
        "tool_notes": ["coding agents need explicit operations"],
        "loss_notes": ["Extended workflows omitted"],
    }


class ImportMcpResourceTests(unittest.TestCase):
    def test_import_mcp_generates_reviewable_draft(self) -> None:
        payload = {
            "resource_version": "1.0.0",
            "owner_id": "markoblogo",
            "uri": "id://markoblogo/context.compact",
            "name": "ID Context: markoblogo",
            "description": "Policy-aware MCP resource derived from ID compact context",
            "mime_type": "application/json",
            "contents": sample_context(),
            "policy": {
                "applied": True,
                "task_class": "coding",
                "source": "profiles/markoblogo/privacy-policy.v1.json",
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "mcp.context.resource.json"
            output_path = Path(tmp) / "draft.md"
            input_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(input_path), "--output", str(output_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            rendered = output_path.read_text(encoding="utf-8")

        self.assertIn("# Draft Profile From MCP Resource", rendered)
        self.assertIn("policy_applied: `True`", rendered)
        self.assertIn("policy_task_class: `coding`", rendered)
        self.assertIn("make assumptions explicit", rendered)


if __name__ == "__main__":
    unittest.main()
