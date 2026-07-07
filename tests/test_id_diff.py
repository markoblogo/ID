from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
IDCLI = REPO_ROOT / "idcli.py"


class IdDiffTest(unittest.TestCase):
    def test_diff_reports_semantic_sections_and_staleness(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init"], cwd=root, check=True, capture_output=True, text=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], cwd=root, check=True)
            owner_dir = root / "profiles" / "ada"
            owner_dir.mkdir(parents=True)
            profile = owner_dir / "profile.core.md"
            profile.write_text(
                """---
profile_id: "ada"
owner_alias: "Ada"
version: "0.1.0"
created_at: "2026-01-01"
updated_at: "2026-01-01"
freshness_ttl_days: 14
trust_level: "trusted"
---

# Core Interaction Profile

## Current Goals

- Ship the first profile.

## Communication Style

- Brief status, detailed architecture.
""",
                encoding="utf-8",
            )
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-m", "base profile"], cwd=root, check=True, capture_output=True, text=True)

            profile.write_text(
                """---
profile_id: "ada"
owner_alias: "Ada"
version: "0.2.0"
created_at: "2026-01-01"
updated_at: "2026-01-20"
freshness_ttl_days: 14
trust_level: "trusted"
---

# Core Interaction Profile

## Current Goals

- Ship the first profile.
- Port the profile across Claude Code and Cursor.

## Communication Style

- Brief status, detailed architecture.

## Priority Domains

- Portable AI identity context.
""",
                encoding="utf-8",
            )

            completed = subprocess.run(
                [
                    sys.executable,
                    str(IDCLI),
                    "diff",
                    "--owner-id",
                    "ada",
                    "--today",
                    "2026-02-10",
                ],
                cwd=root,
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("Identity Diff", completed.stdout)
        self.assertIn("changed: Current Goals", completed.stdout)
        self.assertIn("added: Priority Domains", completed.stdout)
        self.assertIn("current goals", completed.stdout)
        self.assertIn("domain focus", completed.stdout)
        self.assertIn("Stale assumptions:", completed.stdout)
        self.assertIn("age=21d, ttl=14d", completed.stdout)

    def test_diff_json_output(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(IDCLI),
                "diff",
                "--owner-id",
                "markoblogo",
                "--from",
                "HEAD",
                "--to",
                "WORKTREE",
                "--json",
                "--today",
                "2026-04-01",
            ],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn('"owner_id": "markoblogo"', completed.stdout)
        self.assertIn('"changed_files"', completed.stdout)


if __name__ == "__main__":
    unittest.main()
