#!/usr/bin/env python3
"""Validate benchmark run completeness against task suite."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate benchmark run completeness")
    parser.add_argument("--run-id", required=True, help="Run id")
    parser.add_argument("--runs-root", default="benchmarks/runs", help="Runs root")
    parser.add_argument("--tasks-root", default="benchmarks/tasks", help="Tasks root")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_dir = Path(args.runs_root) / args.run_id
    results_dir = run_dir / "results"

    if not run_dir.exists() or not results_dir.exists():
        print(f"ERROR: missing run/results dir for {args.run_id}")
        return 1

    tasks = sorted(p.stem for p in Path(args.tasks_root).glob("task-*.md"))
    missing = []

    for task_id in tasks:
        if not (results_dir / f"{task_id}.json").exists():
            missing.append(task_id)

    if missing:
        print("ERROR: missing result files for tasks:")
        for task_id in missing:
            print(f"- {task_id}")
        return 1

    print(f"Run '{args.run_id}' is complete for {len(tasks)} tasks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
