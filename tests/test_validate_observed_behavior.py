from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "validate_observed_behavior.py"


def valid_note() -> dict:
    return {
        "schema_version": "1.0.0",
        "tool_family": "ChatGPT",
        "confidence": "medium",
        "observed_at": "2026-04-01",
        "summary": "Compact context plus handshake works best.",
        "onboarding_mode": ["compact context plus handshake"],
        "best_artifacts": ["context.compact.json"],
        "degradation_patterns": ["freshness semantics weaken if not restated explicitly"],
        "evidence": {
            "basis": ["repo workflow observation"],
            "artifact_refs": ["docs/OBSERVED_BEHAVIOR.md"],
            "run_refs": ["baseline-2026-03-31-codex"],
            "scope_limits": ["repo-level observation, not vendor certification"],
        },
    }


class ValidateObservedBehaviorTests(unittest.TestCase):
    def test_valid_note_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chatgpt.family.v1.json"
            path.write_text(json.dumps(valid_note(), indent=2) + "\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), "--input", str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("VALID:", result.stdout)

    def test_invalid_note_fails(self) -> None:
        payload = valid_note()
        payload["confidence"] = "maybe"
        payload["evidence"]["basis"] = []
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chatgpt.family.v1.json"
            path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), "--input", str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("confidence must be one of: low, medium, high", result.stdout)
        self.assertIn("evidence.basis must contain at least 1 item(s)", result.stdout)

    def test_stale_note_fails_default_freshness_hook(self) -> None:
        payload = valid_note()
        payload["observed_at"] = "2025-01-01"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chatgpt.family.v1.json"
            path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR),
                    "--input",
                    str(path),
                    "--today",
                    "2026-04-01",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("observed_at is stale", result.stdout)


if __name__ == "__main__":
    unittest.main()
