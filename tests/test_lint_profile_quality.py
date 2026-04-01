from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LINTER = REPO_ROOT / "scripts" / "lint_profile_quality.py"


def write_profile(path: Path, content: str) -> None:
    path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")


class LintProfileQualityTests(unittest.TestCase):
    def test_good_profiles_pass_cleanly(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            owner_dir = Path(tmp) / "demo"
            owner_dir.mkdir(parents=True)
            write_profile(
                owner_dir / "profile.core.md",
                """
                ---
                profile_id: "demo"
                owner_alias: "demo"
                version: "0.1.0"
                created_at: "2026-04-01"
                updated_at: "2026-04-01"
                freshness_ttl_days: 30
                confidence_notes: "Built from direct owner input."
                trust_level: "trusted"
                ---

                ## 1. Communication Style
                - Preferred language(s): English
                - Tone preference: direct

                ## 2. Task Execution Rules
                - Always do:
                  - make assumptions explicit
                  - verify critical outputs
                - Never do:
                  - invent user facts
                  - hide uncertainty
                - Ask before:
                  - destructive changes
                - Default assumptions:
                  - the user wants a reproducible workflow

                ## 3. Quality Bar
                - Definition of "good result": correct and reviewable
                - What counts as "done": change + verification

                ## 4. Priority Domains
                - Protocol design
                - Interop workflows
                """,
            )
            result = subprocess.run(
                [sys.executable, str(LINTER), "--profiles-root", tmp],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("warnings=0", result.stdout)

    def test_advisory_mode_warns_but_returns_zero(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            owner_dir = Path(tmp) / "demo"
            owner_dir.mkdir(parents=True)
            write_profile(
                owner_dir / "profile.core.md",
                """
                ---
                profile_id: "demo"
                owner_alias: "demo"
                version: "0.1.0"
                created_at: "2026-04-01"
                updated_at: "2026-04-01"
                freshness_ttl_days: 30
                trust_level: "trusted"
                ---

                ## 1. Communication Style
                - TODO

                ## 2. Task Execution Rules
                - Always do:
                  - verify output
                - Never do:
                  - verify output
                """,
            )
            result = subprocess.run(
                [sys.executable, str(LINTER), "--profiles-root", tmp],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Missing confidence_notes", result.stdout)
        self.assertIn("Contains placeholder text", result.stdout)
        self.assertIn("Potential contradiction", result.stdout)

    def test_strict_mode_fails_on_warnings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            owner_dir = Path(tmp) / "demo"
            owner_dir.mkdir(parents=True)
            write_profile(
                owner_dir / "profile.extended.md",
                """
                ---
                profile_id: "demo"
                owner_alias: "demo"
                version: "0.1.0"
                created_at: "2026-04-01"
                updated_at: "2026-04-01"
                freshness_ttl_days: 30
                trust_level: "provisional"
                ---

                ## 1. Stable Preferences
                - TBD
                """,
            )
            result = subprocess.run(
                [sys.executable, str(LINTER), "--profiles-root", tmp, "--strict"],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("Profile may be underspecified", result.stdout)


if __name__ == "__main__":
    unittest.main()
