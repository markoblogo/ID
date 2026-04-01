from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "benchmark_public_report.py"


def write_summary(path: Path, *, run_id: str, date: str, tool: str, averages: dict[str, float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "run_id": run_id,
                "meta": {
                    "date": date,
                    "tools": [tool],
                    "profile_version": "0.1.0",
                },
                "tasks": 2,
                "averages": averages,
            }
        ),
        encoding="utf-8",
    )


def write_result(path: Path, *, style: int, constraint: int, quality: int, edits: float, minutes: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "style_fit": style,
                "constraint_adherence": constraint,
                "result_quality": quality,
                "edit_count": edits,
                "time_to_acceptable_min": minutes,
            }
        ),
        encoding="utf-8",
    )


def write_profile(path: Path, *, updated_at: str, ttl_days: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        textwrap.dedent(
            f"""\
            ---
            profile_id: "markoblogo"
            updated_at: "{updated_at}"
            freshness_ttl_days: {ttl_days}
            ---
            # Profile
            """
        ),
        encoding="utf-8",
    )


class BenchmarkPublicReportTests(unittest.TestCase):
    def test_generates_public_metric_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            runs_root = root / "benchmarks" / "runs"
            profiles_root = root / "profiles"

            write_summary(
                runs_root / "run-a" / "summary.json",
                run_id="run-a",
                date="2026-03-31",
                tool="codex",
                averages={
                    "style_fit": 4.6,
                    "constraint_adherence": 4.8,
                    "result_quality": 4.5,
                    "edit_count": 0.5,
                    "time_to_acceptable_min": 3.0,
                },
            )
            write_result(runs_root / "run-a" / "results" / "task-1.json", style=5, constraint=5, quality=5, edits=0, minutes=2)
            write_result(runs_root / "run-a" / "results" / "task-2.json", style=4, constraint=4, quality=4, edits=0, minutes=4)

            write_summary(
                runs_root / "run-b" / "summary.json",
                run_id="run-b",
                date="2026-04-01",
                tool="claude",
                averages={
                    "style_fit": 3.8,
                    "constraint_adherence": 4.0,
                    "result_quality": 3.9,
                    "edit_count": 1.5,
                    "time_to_acceptable_min": 5.0,
                },
            )
            write_result(runs_root / "run-b" / "results" / "task-1.json", style=4, constraint=4, quality=4, edits=0, minutes=4)
            write_result(runs_root / "run-b" / "results" / "task-2.json", style=3, constraint=4, quality=3, edits=3, minutes=6)

            write_profile(profiles_root / "markoblogo" / "profile.core.md", updated_at="2026-03-31", ttl_days=14)
            write_profile(profiles_root / "markoblogo" / "profile.extended.md", updated_at="2026-04-01", ttl_days=30)

            output_json = root / "benchmarks" / "runs" / "public-metrics.json"
            output_md = root / "benchmarks" / "runs" / "public-metrics.md"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--runs-root",
                    str(runs_root),
                    "--profiles-root",
                    str(profiles_root),
                    "--owner-id",
                    "markoblogo",
                    "--output-json",
                    str(output_json),
                    "--output-md",
                    str(output_md),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            payload = json.loads(output_json.read_text(encoding="utf-8"))
            self.assertEqual(len(payload["runs"]), 2)
            self.assertEqual(payload["runs"][0]["public_metrics"]["task_success_rate"], 1.0)
            self.assertEqual(payload["runs"][1]["public_metrics"]["task_success_rate"], 0.5)
            self.assertEqual(payload["best_by_public_metric"]["best_task_success_rate"]["run_id"], "run-a")
            self.assertEqual(payload["best_by_public_metric"]["best_onboarding_latency"]["run_id"], "run-a")
            self.assertIn("prompt_length_reduction", payload["not_yet_instrumented"])
            self.assertIn("# Public Benchmark Metrics", output_md.read_text(encoding="utf-8"))

    def test_requires_at_least_two_valid_summaries(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            runs_root = root / "benchmarks" / "runs"
            profiles_root = root / "profiles"

            write_summary(
                runs_root / "run-a" / "summary.json",
                run_id="run-a",
                date="2026-03-31",
                tool="codex",
                averages={"style_fit": 4.0},
            )
            write_profile(profiles_root / "markoblogo" / "profile.core.md", updated_at="2026-03-31", ttl_days=14)

            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--runs-root",
                    str(runs_root),
                    "--profiles-root",
                    str(profiles_root),
                    "--output-json",
                    str(root / "out.json"),
                    "--output-md",
                    str(root / "out.md"),
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(proc.returncode, 1)
            self.assertIn("need at least 2 run summaries", proc.stdout)


if __name__ == "__main__":
    unittest.main()
