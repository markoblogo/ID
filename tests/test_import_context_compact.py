from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "import_context_compact.py"


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


class ImportContextCompactTests(unittest.TestCase):
    def test_import_compact_generates_reviewable_draft(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            input_path = Path(tmp) / "context.compact.json"
            output_path = Path(tmp) / "draft.md"
            input_path.write_text(json.dumps(sample_context(), indent=2) + "\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--input", str(input_path), "--output", str(output_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            rendered = output_path.read_text(encoding="utf-8")

        self.assertIn("# Draft Profile From Compact Context", rendered)
        self.assertIn("lossy import candidate", rendered)
        self.assertIn("make assumptions explicit", rendered)
        self.assertIn("Extended workflows omitted", rendered)


if __name__ == "__main__":
    unittest.main()
