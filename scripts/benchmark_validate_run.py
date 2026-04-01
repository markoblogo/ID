#!/usr/bin/env python3
"""Validate benchmark run completeness against task suite."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

VALID_CONTEXT_MODES = {"id", "no_id"}
REQUIRED_PROMPT_SEGMENTS = {"system", "profile_context", "task_context", "task_instruction"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate benchmark run completeness")
    parser.add_argument("--run-id", required=True, help="Run id")
    parser.add_argument("--runs-root", default="benchmarks/runs", help="Runs root")
    parser.add_argument("--tasks-root", default="benchmarks/tasks", help="Tasks root")
    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8", errors="ignore"))


def prompt_payload_valid(path: Path, task_id: str) -> tuple[bool, str]:
    payload = load_json(path)
    if payload.get("task_id") != task_id:
        return False, f"prompt payload task_id mismatch for {task_id}"
    segments = payload.get("prompt_segments")
    if not isinstance(segments, dict):
        return False, f"prompt_segments missing for {task_id}"
    missing = sorted(REQUIRED_PROMPT_SEGMENTS - set(segments))
    if missing:
        return False, f"prompt_segments missing keys for {task_id}: {', '.join(missing)}"
    for key in REQUIRED_PROMPT_SEGMENTS:
        if not isinstance(segments.get(key), str):
            return False, f"prompt_segments.{key} must be a string for {task_id}"
    return True, ""


def main() -> int:
    args = parse_args()
    run_dir = Path(args.runs_root) / args.run_id
    results_dir = run_dir / "results"
    prompts_dir = run_dir / "prompts"
    meta_path = run_dir / "meta.json"

    if not run_dir.exists() or not results_dir.exists() or not prompts_dir.exists():
        print(f"ERROR: missing run/results/prompts dir for {args.run_id}")
        return 1

    if not meta_path.exists():
        print(f"ERROR: missing meta.json for {args.run_id}")
        return 1

    meta = load_json(meta_path)
    context_mode = meta.get("context_mode")
    if context_mode and context_mode not in VALID_CONTEXT_MODES:
        print(f"ERROR: invalid context_mode in meta.json: {context_mode}")
        return 1

    tasks = sorted(p.stem for p in Path(args.tasks_root).glob("task-*.md"))
    missing_results = []
    missing_prompts = []
    invalid_prompts = []

    for task_id in tasks:
        if not (results_dir / f"{task_id}.json").exists():
            missing_results.append(task_id)
        prompt_path = prompts_dir / f"{task_id}.json"
        if not prompt_path.exists():
            missing_prompts.append(task_id)
        else:
            valid, reason = prompt_payload_valid(prompt_path, task_id)
            if not valid:
                invalid_prompts.append(reason)

    if missing_results:
        print("ERROR: missing result files for tasks:")
        for task_id in missing_results:
            print(f"- {task_id}")
        return 1

    if missing_prompts:
        print("ERROR: missing prompt payloads for tasks:")
        for task_id in missing_prompts:
            print(f"- {task_id}")
        return 1

    if invalid_prompts:
        print("ERROR: invalid prompt payloads:")
        for reason in invalid_prompts:
            print(f"- {reason}")
        return 1

    print(f"Run '{args.run_id}' is complete for {len(tasks)} tasks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
