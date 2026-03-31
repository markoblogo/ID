#!/usr/bin/env python3
"""Aggregate benchmark run results into summary JSON/Markdown."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

METRICS = ["style_fit", "constraint_adherence", "result_quality", "edit_count", "time_to_acceptable_min"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate benchmark run results")
    parser.add_argument("--run-id", required=True, help="Run id under benchmarks/runs/")
    parser.add_argument("--runs-root", default="benchmarks/runs", help="Runs root directory")
    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8", errors="ignore"))


def main() -> int:
    args = parse_args()
    run_dir = Path(args.runs_root) / args.run_id
    results_dir = run_dir / "results"
    meta_path = run_dir / "meta.json"

    if not results_dir.exists():
        print(f"ERROR: missing results directory: {results_dir}")
        return 1

    meta = load_json(meta_path) if meta_path.exists() else {"run_id": args.run_id}

    rows = []
    for path in sorted(results_dir.glob("*.json")):
        try:
            rows.append(load_json(path))
        except json.JSONDecodeError:
            print(f"WARN: invalid JSON skipped: {path}")

    if not rows:
        print("ERROR: no valid result files found")
        return 1

    summary = {
      "run_id": args.run_id,
      "meta": meta,
      "tasks": len(rows),
      "averages": {}
    }

    for metric in METRICS:
        values = [float(r.get(metric, 0)) for r in rows]
        summary["averages"][metric] = round(sum(values) / len(values), 3)

    summary_json = run_dir / "summary.json"
    summary_md = run_dir / "summary.md"
    summary_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        f"# Benchmark Summary: {args.run_id}",
        "",
        f"- tasks: {summary['tasks']}",
        "",
        "## Averages",
        "",
    ]
    for metric in METRICS:
        lines.append(f"- {metric}: {summary['averages'][metric]}")

    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated: {summary_json}")
    print(f"Generated: {summary_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
