from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "export_context_compact.py"


class ExportContextCompactTests(unittest.TestCase):
    def test_exports_compact_payload_from_core_profile(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            owner_dir = root / "profiles" / "owner1"
            owner_dir.mkdir(parents=True)
            (owner_dir / "profile.core.md").write_text(
                """---
profile_id: owner1
owner_alias: owner1
version: 0.1.0
created_at: 2026-03-31
updated_at: 2026-04-01
freshness_ttl_days: 14
trust_level: trusted
---
# Core

## Communication Style
- direct
- concise

## Task Execution Rules
- Always do
  - verify assumptions
- Never do
  - invent facts
- Ask before
  - destructive changes
- Default assumptions
  - prefer local files

## Quality Bar
- correct before elegant

## Priority Domains
- coding
- research

## Tool-Specific Notes
- codex: keep diffs small

## Corrections History
- ignore in compact export
""",
                encoding="utf-8",
            )

            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--owner-id",
                    "owner1",
                    "--profiles-root",
                    str(root / "profiles"),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            payload = json.loads((owner_dir / "context.compact.json").read_text(encoding="utf-8"))

            self.assertEqual(payload["context_version"], "0.1.0")
            self.assertEqual(payload["owner_id"], "owner1")
            self.assertEqual(payload["updated_at"], "2026-04-01")
            self.assertEqual(payload["freshness_ttl_days"], 14)
            self.assertEqual(payload["trust_level"], "trusted")
            self.assertEqual(payload["communication"], ["direct", "concise"])
            self.assertEqual(payload["rules"]["always_do"], ["verify assumptions"])
            self.assertEqual(payload["rules"]["never_do"], ["invent facts"])
            self.assertEqual(payload["quality_bar"], ["correct before elegant"])
            self.assertEqual(payload["priority_domains"], ["coding", "research"])
            self.assertEqual(payload["tool_notes"], ["codex: keep diffs small"])
            self.assertIn("Extended workflows omitted", payload["loss_notes"])

    def test_fails_when_core_profile_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "profiles" / "owner1").mkdir(parents=True)

            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--owner-id",
                    "owner1",
                    "--profiles-root",
                    str(root / "profiles"),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 1)
            self.assertIn("missing profile.core.md", proc.stdout)


if __name__ == "__main__":
    unittest.main()
