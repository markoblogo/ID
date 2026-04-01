from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "benchmark_public_report.py"


def write_summary(path: Path, *, run_id: str, averages: dict[str, float]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "run_id": run_id,
                "tasks": 2,
                "averages": averages,
            }
        ),
        encoding="utf-8",
    )


def write_meta(path: Path, *, run_id: str, date: str, tool: str, profile_version: str, context_mode: str, comparison_group: str | None = None) -> None:
    payload = {
        "run_id": run_id,
        "date": date,
        "owner_id": "markoblogo",
        "profile_version": profile_version,
        "tools": [tool],
        "evaluator": "manual-self-eval",
        "context_mode": context_mode,
    }
    if comparison_group:
        payload["comparison_group"] = comparison_group
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


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


def write_prompt(path: Path, *, task_id: str, tool: str, context_mode: str, system: str, profile_context: str, task_context: str, task_instruction: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "task_id": task_id,
                "tool": tool,
                "context_mode": context_mode,
                "prompt_segments": {
                    "system": system,
                    "profile_context": profile_context,
                    "task_context": task_context,
                    "task_instruction": task_instruction,
                },
                "notes": "test payload",
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
            profile_id: \"markoblogo\"
            updated_at: \"{updated_at}\"
            freshness_ttl_days: {ttl_days}
            ---
            # Profile
            """
        ),
        encoding="utf-8",
    )


def write_fixture(root: Path) -> tuple[Path, Path, Path, Path]:
    runs_root = root / "benchmarks" / "runs"
    profiles_root = root / "profiles"

    write_meta(
        runs_root / "run-a" / "meta.json",
        run_id="run-a",
        date="2026-03-31",
        tool="codex",
        profile_version="0.1.0",
        context_mode="id",
        comparison_group="pair-a",
    )
    write_summary(
        runs_root / "run-a" / "summary.json",
        run_id="run-a",
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
    write_prompt(
        runs_root / "run-a" / "prompts" / "task-1.json",
        task_id="task-1",
        tool="codex",
        context_mode="id",
        system="short system",
        profile_context="compact profile",
        task_context="repo context",
        task_instruction="do task 1",
    )
    write_prompt(
        runs_root / "run-a" / "prompts" / "task-2.json",
        task_id="task-2",
        tool="codex",
        context_mode="id",
        system="short system",
        profile_context="compact profile",
        task_context="repo context",
        task_instruction="do task 2",
    )

    write_meta(
        runs_root / "run-a-no-id" / "meta.json",
        run_id="run-a-no-id",
        date="2026-03-31",
        tool="codex",
        profile_version="none",
        context_mode="no_id",
        comparison_group="pair-a",
    )
    write_summary(
        runs_root / "run-a-no-id" / "summary.json",
        run_id="run-a-no-id",
        averages={
            "style_fit": 3.5,
            "constraint_adherence": 4.0,
            "result_quality": 3.8,
            "edit_count": 1.5,
            "time_to_acceptable_min": 5.0,
        },
    )
    write_result(runs_root / "run-a-no-id" / "results" / "task-1.json", style=4, constraint=4, quality=4, edits=1, minutes=4)
    write_result(runs_root / "run-a-no-id" / "results" / "task-2.json", style=3, constraint=4, quality=3, edits=2, minutes=6)
    write_prompt(
        runs_root / "run-a-no-id" / "prompts" / "task-1.json",
        task_id="task-1",
        tool="codex",
        context_mode="no_id",
        system="long system prompt with repeated rules",
        profile_context="manual preferences repeated in full detail",
        task_context="repo context and additional reminders",
        task_instruction="do task 1 with repeated constraints",
    )
    write_prompt(
        runs_root / "run-a-no-id" / "prompts" / "task-2.json",
        task_id="task-2",
        tool="codex",
        context_mode="no_id",
        system="long system prompt with repeated rules",
        profile_context="manual preferences repeated in full detail",
        task_context="repo context and additional reminders",
        task_instruction="do task 2 with repeated constraints",
    )

    write_profile(profiles_root / "markoblogo" / "profile.core.md", updated_at="2026-03-31", ttl_days=14)
    write_profile(profiles_root / "markoblogo" / "profile.extended.md", updated_at="2026-04-01", ttl_days=30)

    output_json = root / "benchmarks" / "runs" / "public-metrics.json"
    output_md = root / "benchmarks" / "runs" / "public-metrics.md"
    return runs_root, profiles_root, output_json, output_md


class BenchmarkPublicReportTests(unittest.TestCase):
    def test_generates_public_metric_outputs_and_control_deltas(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            runs_root, profiles_root, output_json, output_md = write_fixture(root)

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
            self.assertEqual(payload["runs"][0]["context_mode"], "id")
            self.assertEqual(payload["runs"][1]["context_mode"], "no_id")
            self.assertEqual(payload["with_vs_without_id_delta"]["pairs"][0]["comparison_group"], "pair-a")
            self.assertEqual(payload["with_vs_without_id_delta"]["pairs"][0]["deltas"]["task_success_rate"], 0.5)
            self.assertEqual(payload["with_vs_without_id_delta"]["pairs"][0]["deltas"]["onboarding_latency_min"], 2.0)
            self.assertGreater(payload["prompt_length_reduction"]["average_reduction_ratio"], 0)
            self.assertNotIn("with_vs_without_id_delta", payload["not_yet_instrumented"])
            self.assertNotIn("prompt_length_reduction", payload["not_yet_instrumented"])
            self.assertNotIn("optional_instrumentation", payload)
            self.assertNotIn("tokenizer_prompt_length_reduction", payload)
            markdown = output_md.read_text(encoding="utf-8")
            self.assertIn("# Public Benchmark Metrics", markdown)
            self.assertIn("With vs Without ID Delta", markdown)
            self.assertIn("Prompt Length Reduction", markdown)
            self.assertNotIn("Optional Tokenizer-Aware Prompt Metrics", markdown)

    def test_supports_optional_tokenizer_metrics_when_provider_is_available(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            runs_root, profiles_root, output_json, output_md = write_fixture(root)
            fake_lib = root / "fake_lib"
            fake_lib.mkdir()
            (fake_lib / "tiktoken.py").write_text(
                textwrap.dedent(
                    """\
                    class _Encoding:
                        def encode(self, text):
                            return [token for token in text.split() if token]

                    def get_encoding(name):
                        return _Encoding()

                    def encoding_for_model(name):
                        return _Encoding()
                    """
                ),
                encoding="utf-8",
            )
            env = os.environ.copy()
            env["PYTHONPATH"] = str(fake_lib)
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
                    "--tokenizer-provider",
                    "tiktoken",
                    "--tokenizer-encoding",
                    "fake-encoding",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                env=env,
                check=False,
            )

            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            payload = json.loads(output_json.read_text(encoding="utf-8"))
            self.assertEqual(payload["optional_instrumentation"]["tokenizer_provider"], "tiktoken")
            self.assertEqual(payload["optional_instrumentation"]["tokenizer_encoding"], "fake-encoding")
            self.assertIsNone(payload["optional_instrumentation"]["tokenizer_model"])
            self.assertIn("tokenizer_prompt_length_reduction", payload)
            self.assertGreater(payload["tokenizer_prompt_length_reduction"]["average_reduction_ratio"], 0)
            self.assertGreater(payload["runs"][0]["prompt_payload_avg_tokens"], 0)
            markdown = output_md.read_text(encoding="utf-8")
            self.assertIn("Optional Tokenizer-Aware Prompt Metrics", markdown)
            self.assertIn("avg_tokens=", markdown)

    def test_requires_at_least_two_valid_summaries(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            runs_root = root / "benchmarks" / "runs"
            profiles_root = root / "profiles"

            write_meta(
                runs_root / "run-a" / "meta.json",
                run_id="run-a",
                date="2026-03-31",
                tool="codex",
                profile_version="0.1.0",
                context_mode="id",
            )
            write_summary(
                runs_root / "run-a" / "summary.json",
                run_id="run-a",
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
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("need at least 2 run summaries", proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
