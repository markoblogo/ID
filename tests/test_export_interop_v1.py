from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "export_interop_v1.py"


class ExportInteropV1Tests(unittest.TestCase):
    def test_exports_typed_sections_and_extensions(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            owner_dir = root / "profiles" / "owner1"
            owner_dir.mkdir(parents=True)

            (owner_dir / "profile.core.md").write_text(
                """---
profile_id: core-owner1
owner_alias: owner1
version: 0.1.0
created_at: 2026-03-01
updated_at: 2026-04-01
freshness_ttl_days: 14
trust_level: trusted
---
# Core

## Communication Signals
- concise
- direct

## Task Execution Rules
- Always do
  - verify facts
- Never do
  - invent data
- Ask before
  - destructive changes
- Default assumptions
  - prefer local tooling

## Quality Bar
- production-grade

## Priority Domains
- coding

## Tool-Specific Notes
- codex: prefer minimal diffs

## Custom Block
- keep me
""",
                encoding="utf-8",
            )

            (owner_dir / "profile.extended.md").write_text(
                """---
profile_id: ext-owner1
owner_alias: owner1
version: 0.1.0
created_at: 2026-03-01
updated_at: 2026-04-01
freshness_ttl_days: 30
trust_level: provisional
---
# Extended

## Stable Preferences
- explicit reasoning

## Domain Workflows
### Coding
- inspect first
- test after

## Recurrent Misalignments
- too much verbosity

## Personal Lexicon
- thin slice

## Environment Assumptions
- macOS

## Decision Heuristics
- safety over speed

## Known Good Prompts
- review this diff

## Extra Section
- preserve as extension
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
            payload = json.loads((owner_dir / "interop.v1.json").read_text(encoding="utf-8"))

            self.assertEqual(payload["owner_id"], "owner1")
            self.assertEqual(payload["profiles"]["core"]["metadata"]["freshness_ttl_days"], 14)
            self.assertEqual(payload["profiles"]["core"]["communication"], ["concise", "direct"])
            self.assertEqual(
                payload["profiles"]["core"]["rules"]["always_do"],
                ["verify facts"],
            )
            self.assertEqual(
                payload["profiles"]["extended"]["domain_workflows"]["coding"],
                ["inspect first", "test after"],
            )
            self.assertEqual(
                payload["profiles"]["core"]["extensions"]["custom block"],
                ["keep me"],
            )
            self.assertEqual(
                payload["profiles"]["extended"]["extensions"]["extra section"],
                ["preserve as extension"],
            )

    def test_fails_when_profiles_are_missing(self) -> None:
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
            self.assertIn("missing profile.core.md or profile.extended.md", proc.stdout)


if __name__ == "__main__":
    unittest.main()
