from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "validate_mcp_resource.py"


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def valid_document() -> dict[str, object]:
    return {
        "resource_version": "1.0.0",
        "owner_id": "markoblogo",
        "uri": "id://markoblogo/context.compact",
        "name": "ID Context: markoblogo",
        "description": "Policy-aware MCP resource derived from ID compact context",
        "mime_type": "application/json",
        "contents": {
            "context_version": "0.1.0",
            "owner_id": "markoblogo",
            "source_profile": "profiles/markoblogo/interop.v1.json",
            "summary": "Compact summary",
            "updated_at": "2026-04-01",
            "freshness_ttl_days": 30,
            "trust_level": "trusted",
            "communication": [],
            "rules": {
                "default_assumptions": [],
                "ask_before": [],
                "never_do": [],
                "always_do": []
            },
            "priority_domains": [],
            "quality_bar": ["correct before elegant"],
            "preferences": [],
            "constraints": [],
            "working_modes": [],
            "tool_notes": [],
            "loss_notes": ["Privacy policy applied"]
        },
        "policy": {
            "applied": True,
            "task_class": "coding",
            "source": "profiles/markoblogo/privacy-policy.v1.json"
        }
    }


class ValidateMcpResourceTests(unittest.TestCase):
    def test_valid_resource_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "mcp.context.resource.json"
            write_json(path, valid_document())
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), "--input", str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("VALID:", result.stdout)

    def test_invalid_resource_fails(self) -> None:
        payload = valid_document()
        payload["mime_type"] = "text/plain"
        payload["policy"] = {"applied": True, "task_class": "", "source": None}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "mcp.context.resource.json"
            write_json(path, payload)
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), "--input", str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("mime_type must be application/json", result.stdout)
        self.assertIn("policy.task_class must be null or a non-empty string", result.stdout)
        self.assertIn("policy.source must be present when policy.applied is true", result.stdout)
