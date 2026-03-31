#!/usr/bin/env python3
"""Initialize benchmark run folder with task result stubs."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize benchmark run scaffolding")
    parser.add_argument("--run-id", required=True, help="Run id (folder name)")
    parser.add_argument("--tool", required=True, help="Tool/model label for this run")
    parser.add_argument("--owner-id", required=True, help="Owner id")
    parser.add_argument("--profile-version", required=True, help="Profile version")
    parser.add_argument("--runs-root", default="benchmarks/runs", help="Runs root")
    parser.add_argument("--tasks-root", default="benchmarks/tasks", help="Tasks root")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = Path(args.runs_root) / args.run_id
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    task_files = sorted(Path(args.tasks_root).glob("task-*.md"))
    if not task_files:
        print("ERROR: no benchmark tasks found")
        return 1

    meta = {
        "run_id": args.run_id,
        "date": date.today().isoformat(),
        "owner_id": args.owner_id,
        "profile_version": args.profile_version,
        "tools": [args.tool],
        "evaluator": "pending",
    }
    (run_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for task_path in task_files:
        task_id = task_path.stem
        result = {
            "task_id": task_id,
            "tool": args.tool,
            "style_fit": 0,
            "constraint_adherence": 0,
            "result_quality": 0,
            "edit_count": 0,
            "time_to_acceptable_min": 0,
            "notes": "pending",
        }
        (results_dir / f"{task_id}.json").write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    (run_dir / "notes.md").write_text("# Benchmark Notes\n\n- pending\n", encoding="utf-8")
    print(f"Initialized run: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
