from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "benchmark_trend_report.py"


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


class BenchmarkTrendReportTests(unittest.TestCase):
    def test_generates_trend_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            runs_root = root / "benchmarks" / "runs"
            write_summary(
                runs_root / "run-a" / "summary.json",
                run_id="run-a",
                date="2026-03-31",
                tool="codex",
                averages={
                    "style_fit": 4.0,
                    "constraint_adherence": 4.5,
                    "result_quality": 4.0,
                    "edit_count": 1.0,
                    "time_to_acceptable_min": 5.0,
                },
            )
            write_summary(
                runs_root / "run-b" / "summary.json",
                run_id="run-b",
                date="2026-04-01",
                tool="claude",
                averages={
                    "style_fit": 4.5,
                    "constraint_adherence": 4.2,
                    "result_quality": 4.4,
                    "edit_count": 0.5,
                    "time_to_acceptable_min": 4.0,
                },
            )

            output_json = root / "benchmarks" / "runs" / "trends.json"
            output_md = root / "benchmarks" / "runs" / "trends.md"
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--runs-root",
                    str(runs_root),
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
            self.assertEqual(payload["delta_first_to_last"]["from"], "run-a")
            self.assertEqual(payload["delta_first_to_last"]["to"], "run-b")
            self.assertEqual(payload["delta_first_to_last"]["metrics"]["style_fit"], 0.5)
            self.assertEqual(payload["best_by_metric"]["style_fit"]["run_id"], "run-b")
            self.assertEqual(payload["best_by_metric"]["edit_count"]["run_id"], "run-b")
            self.assertIn("# Benchmark Trend Report", output_md.read_text(encoding="utf-8"))

    def test_requires_at_least_two_valid_summaries(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            runs_root = root / "benchmarks" / "runs"
            write_summary(
                runs_root / "run-a" / "summary.json",
                run_id="run-a",
                date="2026-03-31",
                tool="codex",
                averages={"style_fit": 4.0},
            )

            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--runs-root",
                    str(runs_root),
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
