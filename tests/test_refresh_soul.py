from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
IDCLI = REPO_ROOT / "idcli.py"


MINIMAL_PROFILE = textwrap.dedent(
    """\
    ---
    profile_id: "demo"
    owner_alias: "Demo"
    version: "0.1.0"
    created_at: "2026-06-01"
    updated_at: "2026-06-10"
    freshness_ttl_days: 14
    confidence_notes: "Manual"
    trust_level: "trusted"
    ---

    # Minimal Interaction Profile

    ## 1. Communication Style

    - Preferred language(s): English
    - Tone preference: direct
    - Brevity/detail preference: concise

    ## 2. Task Execution Rules

    - Always do:
      - show assumptions
      - verify risky changes
    - Ask before:
      - destructive actions

    ## 3. Quality Bar

    - Definition of "good result": correct and reviewable

    ## 4. Priority Domains

    - Tooling
    """
)


EXTENDED_PROFILE = textwrap.dedent(
    """\
    ---
    profile_id: "demo"
    owner_alias: "Demo"
    version: "0.1.1"
    created_at: "2026-06-01"
    updated_at: "2026-06-11"
    freshness_ttl_days: 30
    confidence_notes: "Manual"
    trust_level: "provisional"
    ---

    # Extended Interaction Profile

    ## 1. Stable Preferences

    - Working rhythm: short loops
    - Decision style: structure first

    ## 2. Domain Workflows

    ### Software / Automation

    - Preferred output: spec + scripts
    - Constraints:
      - keep portability explicit

    ## 3. Recurrent Misalignments

    - Model forgets previous constraints
    """
)


CHANGELOG = textwrap.dedent(
    """\
    # Profile Changelog

    ## Entries

    - date: 2026-06-12
    - session_context: "Refined workflow defaults"
    - sections_used: "Core profile"
    - changes_made: "Added stronger review expectations"
    - open_questions: "None"
    - next_review_date: 2026-07-12
    """
)


class RefreshSoulTests(unittest.TestCase):
    def test_refresh_soul_creates_expected_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            owner_dir = Path(tmp) / "profiles" / "demo"
            owner_dir.mkdir(parents=True, exist_ok=True)
            (owner_dir / "profile.minimal.md").write_text(MINIMAL_PROFILE, encoding="utf-8")
            (owner_dir / "profile.extended.md").write_text(EXTENDED_PROFILE, encoding="utf-8")
            (owner_dir / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")

            proc = subprocess.run(
                [
                    sys.executable,
                    str(IDCLI),
                    "refresh-soul",
                    "--owner-id",
                    "demo",
                    "--profiles-root",
                    str(Path(tmp) / "profiles"),
                    "--today",
                    "2026-06-13",
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            soul_path = owner_dir / "soul.md"
            self.assertTrue(soul_path.exists())
            soul = soul_path.read_text(encoding="utf-8")
            self.assertIn('format: "soul.v0.1"', soul)
            self.assertIn("[owner-stated/minimal] Preferred language(s): English", soul)
            self.assertIn("[owner-stated/extended] Software / Automation: Preferred output: spec + scripts", soul)
            self.assertIn("[recent-session] 2026-06-12: Refined workflow defaults", soul)
            self.assertIn("<!-- SOUL_MANUAL_START -->", soul)

    def test_refresh_soul_preserves_manual_block_and_check_stabilizes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            owner_dir = Path(tmp) / "profiles" / "demo"
            owner_dir.mkdir(parents=True, exist_ok=True)
            (owner_dir / "profile.minimal.md").write_text(MINIMAL_PROFILE, encoding="utf-8")
            (owner_dir / "CHANGELOG.md").write_text(CHANGELOG, encoding="utf-8")

            first = subprocess.run(
                [
                    sys.executable,
                    str(IDCLI),
                    "refresh-soul",
                    "--owner-id",
                    "demo",
                    "--profiles-root",
                    str(Path(tmp) / "profiles"),
                    "--today",
                    "2026-06-13",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(first.returncode, 0, first.stdout + first.stderr)

            soul_path = owner_dir / "soul.md"
            original = soul_path.read_text(encoding="utf-8")
            updated = original.replace(
                "<!-- SOUL_MANUAL_START -->\n- Add owner-reviewed corrections here.\n- Prefix uncertain edits with `[manual-review]`.\n<!-- SOUL_MANUAL_END -->",
                "<!-- SOUL_MANUAL_START -->\n- [manual-review] Prefer weekly refresh during active projects.\n<!-- SOUL_MANUAL_END -->",
            )
            soul_path.write_text(updated, encoding="utf-8")

            second = subprocess.run(
                [
                    sys.executable,
                    str(IDCLI),
                    "refresh-soul",
                    "--owner-id",
                    "demo",
                    "--profiles-root",
                    str(Path(tmp) / "profiles"),
                    "--today",
                    "2026-06-13",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            preserved = soul_path.read_text(encoding="utf-8")
            self.assertIn("[manual-review] Prefer weekly refresh during active projects.", preserved)

            check = subprocess.run(
                [
                    sys.executable,
                    str(IDCLI),
                    "refresh-soul",
                    "--owner-id",
                    "demo",
                    "--profiles-root",
                    str(Path(tmp) / "profiles"),
                    "--today",
                    "2026-06-13",
                    "--check",
                    "--format",
                    "json",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(check.returncode, 0, check.stdout + check.stderr)
            self.assertIn('"changed": false', check.stdout)


if __name__ == "__main__":
    unittest.main()
