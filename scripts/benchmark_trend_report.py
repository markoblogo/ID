#!/usr/bin/env python3
"""Generate cross-run benchmark trend report from run summaries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HIGHER_BETTER = {"style_fit", "constraint_adherence", "result_quality"}
METRICS = [
    "style_fit",
    "constraint_adherence",
    "result_quality",
    "edit_count",
    "time_to_acceptable_min",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build benchmark trend report across runs")
    parser.add_argument("--runs-root", default="benchmarks/runs", help="Runs root")
    parser.add_argument("--output-json", default="benchmarks/runs/trends.json", help="Output JSON path")
    parser.add_argument("--output-md", default="benchmarks/runs/trends.md", help="Output markdown path")
    parser.add_argument("--include-control", action="store_true", help="Include context_mode=no_id control runs")
    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8", errors="ignore"))


def load_run_meta(run_dir: Path, summary: dict) -> dict:
    meta_path = run_dir / "meta.json"
    if meta_path.exists():
        try:
            return load_json(meta_path)
        except json.JSONDecodeError:
            pass
    return summary.get("meta", {})


def main() -> int:
    args = parse_args()
    runs_root = Path(args.runs_root)

    summaries: list[tuple[Path, dict, dict]] = []
    for path in sorted(runs_root.glob("*/summary.json")):
        try:
            summary = load_json(path)
        except json.JSONDecodeError:
            continue
        meta = load_run_meta(path.parent, summary)
        if not args.include_control and meta.get("context_mode") == "no_id":
            continue
        summaries.append((path.parent, summary, meta))

    if len(summaries) < 2:
        print("ERROR: need at least 2 run summaries to compute trends")
        return 1

    summaries.sort(key=lambda item: (item[2].get("date", ""), item[1].get("run_id", "")))

    rows = []
    for run_dir, summary, meta in summaries:
        tool_list = meta.get("tools", [])
        tool = tool_list[0] if tool_list else "unknown"
        rows.append(
            {
                "run_id": summary.get("run_id"),
                "date": meta.get("date"),
                "tool": tool,
                "profile_version": meta.get("profile_version"),
                "tasks": summary.get("tasks", 0),
                "averages": summary.get("averages", {}),
            }
        )

    best_by_metric = {}
    for metric in METRICS:
        metric_rows = [r for r in rows if metric in r["averages"]]
        if not metric_rows:
            continue
        reverse = metric in HIGHER_BETTER
        best = sorted(metric_rows, key=lambda r: r["averages"][metric], reverse=reverse)[0]
        best_by_metric[metric] = {
            "run_id": best["run_id"],
            "tool": best["tool"],
            "value": best["averages"][metric],
            "direction": "higher_better" if metric in HIGHER_BETTER else "lower_better",
        }

    first = rows[0]
    last = rows[-1]
    delta = {}
    for metric in METRICS:
        if metric in first["averages"] and metric in last["averages"]:
            delta[metric] = round(last["averages"][metric] - first["averages"][metric], 3)

    payload = {
        "runs": rows,
        "delta_first_to_last": {
            "from": first["run_id"],
            "to": last["run_id"],
            "metrics": delta,
        },
        "best_by_metric": best_by_metric,
    }

    out_json = Path(args.output_json)
    out_md = Path(args.output_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)

    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Benchmark Trend Report",
        "",
        f"Runs analyzed: {len(rows)}",
        "",
        "## Runs",
        "",
    ]
    for row in rows:
        averages = row["averages"]
        lines.append(
            f"- {row['date']} | {row['run_id']} | {row['tool']} | "
            f"style={averages.get('style_fit')} constraint={averages.get('constraint_adherence')} "
            f"quality={averages.get('result_quality')} edits={averages.get('edit_count')} "
            f"time={averages.get('time_to_acceptable_min')}"
        )

    lines.extend(["", "## Delta (first -> last)", ""])
    lines.append(f"- from: {first['run_id']}")
    lines.append(f"- to: {last['run_id']}")
    for metric in METRICS:
        if metric in delta:
            lines.append(f"- {metric}: {delta[metric]}")

    lines.extend(["", "## Best By Metric", ""])
    for metric in METRICS:
        if metric in best_by_metric:
            best = best_by_metric[metric]
            lines.append(f"- {metric}: {best['value']} ({best['tool']} / {best['run_id']})")

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated: {out_json}")
    print(f"Generated: {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
