#!/usr/bin/env python3
"""Generate public-facing benchmark utility metrics across runs."""

from __future__ import annotations

import argparse
import json
from datetime import date, datetime
from pathlib import Path

SUCCESS_THRESHOLD = 4
LOWER_BETTER_PUBLIC_METRICS = {"onboarding_latency_min", "clarification_turns_avg"}
PROMPT_SEGMENT_KEYS = ("system", "profile_context", "task_context", "task_instruction")
METRIC_NOTES = {
    "prompt_length_reduction": "not yet instrumented; requires comparable prompts/<task-id>.json payloads in matched control runs",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build public benchmark utility report across runs")
    parser.add_argument("--runs-root", default="benchmarks/runs", help="Runs root")
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root")
    parser.add_argument("--owner-id", default="markoblogo", help="Owner id for freshness snapshot")
    parser.add_argument("--output-json", default="benchmarks/runs/public-metrics.json", help="Output JSON path")
    parser.add_argument("--output-md", default="benchmarks/runs/public-metrics.md", help="Output markdown path")
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


def parse_iso_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def parse_front_matter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return {}
    front_matter: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        front_matter[key.strip()] = value.strip().strip('"')
    return front_matter


def freshness_entry(path: Path, root: Path) -> dict | None:
    if not path.exists():
        return None
    front_matter = parse_front_matter(path)
    updated_at = front_matter.get("updated_at")
    ttl_raw = front_matter.get("freshness_ttl_days")
    if not updated_at or not ttl_raw:
        return None
    ttl_days = int(ttl_raw)
    age_days = (date.today() - parse_iso_date(updated_at)).days
    ratio = max(0.0, 1.0 - (age_days / ttl_days)) if ttl_days > 0 else 0.0
    return {
        "path": str(path.relative_to(root)),
        "updated_at": updated_at,
        "freshness_ttl_days": ttl_days,
        "age_days": age_days,
        "freshness_score": round(ratio * 100, 1),
    }


def profile_freshness_snapshot(profiles_root: Path, owner_id: str) -> dict:
    owner_root = profiles_root / owner_id
    entries = []
    for name in ("profile.core.md", "profile.extended.md"):
        entry = freshness_entry(owner_root / name, profiles_root.parent)
        if entry is not None:
            entries.append(entry)
    overall = min((entry["freshness_score"] for entry in entries), default=0.0)
    return {
        "owner_id": owner_id,
        "overall_score": overall,
        "profiles": entries,
    }


def read_results(run_dir: Path) -> list[dict]:
    rows = []
    for path in sorted((run_dir / "results").glob("*.json")):
        try:
            rows.append(load_json(path))
        except json.JSONDecodeError:
            continue
    return rows


def prompt_char_count(prompt_payload: dict) -> int:
    segments = prompt_payload.get("prompt_segments", {})
    return sum(len(str(segments.get(key, ""))) for key in PROMPT_SEGMENT_KEYS)


def read_prompt_payloads(run_dir: Path) -> dict[str, dict]:
    payloads = {}
    for path in sorted((run_dir / "prompts").glob("*.json")):
        try:
            payload = load_json(path)
        except json.JSONDecodeError:
            continue
        task_id = payload.get("task_id") or path.stem
        payloads[task_id] = payload
    return payloads


def success(result: dict) -> bool:
    return result.get("result_quality", 0) >= SUCCESS_THRESHOLD and result.get("constraint_adherence", 0) >= SUCCESS_THRESHOLD


def high_alignment(result: dict) -> bool:
    return success(result) and result.get("style_fit", 0) >= SUCCESS_THRESHOLD


def first_pass_success(result: dict) -> bool:
    return success(result) and float(result.get("edit_count", 0)) == 0.0


def alignment_index(summary: dict) -> float:
    averages = summary.get("averages", {})
    components = [
        averages.get("style_fit", 0.0),
        averages.get("constraint_adherence", 0.0),
        averages.get("result_quality", 0.0),
    ]
    return round((sum(components) / 15.0) * 100.0, 1)


def build_run_row(run_dir: Path, summary: dict) -> dict:
    meta = load_run_meta(run_dir, summary)
    results = read_results(run_dir)
    prompts = read_prompt_payloads(run_dir)
    tool_list = meta.get("tools", [])
    tool = tool_list[0] if tool_list else "unknown"
    total = len(results)
    success_rate = round(sum(1 for row in results if success(row)) / total, 3) if total else 0.0
    high_alignment_rate = round(sum(1 for row in results if high_alignment(row)) / total, 3) if total else 0.0
    first_pass_rate = round(sum(1 for row in results if first_pass_success(row)) / total, 3) if total else 0.0
    prompt_lengths = [prompt_char_count(payload) for payload in prompts.values()]
    return {
        "run_id": summary.get("run_id"),
        "date": meta.get("date"),
        "tool": tool,
        "profile_version": meta.get("profile_version"),
        "context_mode": meta.get("context_mode", "id"),
        "comparison_group": meta.get("comparison_group"),
        "tasks": summary.get("tasks", total),
        "prompt_payload_avg_chars": round(sum(prompt_lengths) / len(prompt_lengths), 1) if prompt_lengths else 0.0,
        "public_metrics": {
            "onboarding_latency_min": summary.get("averages", {}).get("time_to_acceptable_min", 0.0),
            "clarification_turns_avg": summary.get("averages", {}).get("edit_count", 0.0),
            "task_success_rate": success_rate,
            "high_alignment_rate": high_alignment_rate,
            "first_pass_success_rate": first_pass_rate,
            "alignment_index": alignment_index(summary),
        },
    }


def best_run(rows: list[dict], metric: str, reverse: bool) -> dict:
    return sorted(rows, key=lambda row: row["public_metrics"][metric], reverse=reverse)[0]


def delta_value(metric: str, with_id: float, without_id: float) -> float:
    if metric in LOWER_BETTER_PUBLIC_METRICS:
        return round(without_id - with_id, 3)
    return round(with_id - without_id, 3)


def with_vs_without_delta(rows: list[dict]) -> dict | None:
    grouped: dict[str, dict[str, dict]] = {}
    for row in rows:
        comparison_group = row.get("comparison_group")
        context_mode = row.get("context_mode")
        if not comparison_group or context_mode not in {"id", "no_id"}:
            continue
        grouped.setdefault(comparison_group, {})[context_mode] = row

    pairs = []
    metric_totals: dict[str, list[float]] = {}
    for comparison_group, contexts in sorted(grouped.items()):
        with_id = contexts.get("id")
        without_id = contexts.get("no_id")
        if with_id is None or without_id is None:
            continue
        deltas = {}
        for metric in with_id["public_metrics"]:
            value = delta_value(
                metric,
                float(with_id["public_metrics"][metric]),
                float(without_id["public_metrics"][metric]),
            )
            deltas[metric] = value
            metric_totals.setdefault(metric, []).append(value)
        pairs.append(
            {
                "comparison_group": comparison_group,
                "with_id_run_id": with_id["run_id"],
                "without_id_run_id": without_id["run_id"],
                "tool": with_id["tool"],
                "deltas": deltas,
            }
        )

    if not pairs:
        return None

    return {
        "pairs": pairs,
        "average_deltas": {
            metric: round(sum(values) / len(values), 3)
            for metric, values in metric_totals.items()
            if values
        },
    }


def prompt_length_reduction(rows: list[dict], runs_root: Path) -> dict | None:
    grouped: dict[str, dict[str, dict]] = {}
    for row in rows:
        comparison_group = row.get("comparison_group")
        context_mode = row.get("context_mode")
        if not comparison_group or context_mode not in {"id", "no_id"}:
            continue
        grouped.setdefault(comparison_group, {})[context_mode] = row

    pairs = []
    ratio_values = []
    char_values = []
    for comparison_group, contexts in sorted(grouped.items()):
        with_id = contexts.get("id")
        without_id = contexts.get("no_id")
        if with_id is None or without_id is None:
            continue
        with_prompts = read_prompt_payloads(runs_root / with_id["run_id"])
        without_prompts = read_prompt_payloads(runs_root / without_id["run_id"])
        shared_tasks = sorted(set(with_prompts) & set(without_prompts))
        if not shared_tasks:
            continue
        reductions = []
        pair_ratio_values = []
        pair_char_values = []
        for task_id in shared_tasks:
            with_chars = prompt_char_count(with_prompts[task_id])
            without_chars = prompt_char_count(without_prompts[task_id])
            if without_chars <= 0:
                continue
            reduction_chars = without_chars - with_chars
            reduction_ratio_exact = reduction_chars / without_chars
            reductions.append(
                {
                    "task_id": task_id,
                    "with_id_chars": with_chars,
                    "without_id_chars": without_chars,
                    "reduction_chars": reduction_chars,
                    "reduction_ratio": round(reduction_ratio_exact, 3),
                }
            )
            pair_ratio_values.append(reduction_ratio_exact)
            pair_char_values.append(reduction_chars)
            ratio_values.append(reduction_ratio_exact)
            char_values.append(reduction_chars)
        if not reductions:
            continue
        pairs.append(
            {
                "comparison_group": comparison_group,
                "with_id_run_id": with_id["run_id"],
                "without_id_run_id": without_id["run_id"],
                "average_reduction_ratio": round(sum(pair_ratio_values) / len(pair_ratio_values), 3),
                "average_reduction_chars": round(sum(pair_char_values) / len(pair_char_values), 1),
                "tasks": reductions,
            }
        )

    if not pairs:
        return None

    return {
        "pairs": pairs,
        "average_reduction_ratio": round(sum(ratio_values) / len(ratio_values), 3),
        "average_reduction_chars": round(sum(char_values) / len(char_values), 1),
    }


def build_payload(runs_root: Path, profiles_root: Path, owner_id: str) -> dict:
    summaries: list[tuple[Path, dict]] = []
    for path in sorted(runs_root.glob("*/summary.json")):
        try:
            summaries.append((path.parent, load_json(path)))
        except json.JSONDecodeError:
            continue

    if len(summaries) < 2:
        raise ValueError("need at least 2 run summaries to compute public metrics")

    summaries.sort(key=lambda item: (load_run_meta(item[0], item[1]).get("date", ""), item[1].get("run_id", "")))
    rows = [build_run_row(run_dir, summary) for run_dir, summary in summaries]

    best_task_success = best_run(rows, "task_success_rate", True)
    best_latency = best_run(rows, "onboarding_latency_min", False)
    best_alignment = best_run(rows, "alignment_index", True)
    best_first_pass = best_run(rows, "first_pass_success_rate", True)
    paired_delta = with_vs_without_delta(rows)
    prompt_reduction = prompt_length_reduction(rows, runs_root)
    not_yet_instrumented = dict(METRIC_NOTES)
    if paired_delta is None:
        not_yet_instrumented["with_vs_without_id_delta"] = (
            "not yet available; requires matched control runs with comparison_group and context_mode=no_id"
        )
    if prompt_reduction is None:
        not_yet_instrumented["prompt_length_reduction"] = (
            "not yet available; requires comparable prompts/<task-id>.json payloads in matched control runs"
        )
    else:
        not_yet_instrumented.pop("prompt_length_reduction", None)

    return {
        "runs": rows,
        "profile_freshness": profile_freshness_snapshot(profiles_root, owner_id),
        "with_vs_without_id_delta": paired_delta,
        "prompt_length_reduction": prompt_reduction,
        "best_by_public_metric": {
            "best_task_success_rate": {
                "run_id": best_task_success["run_id"],
                "value": best_task_success["public_metrics"]["task_success_rate"],
            },
            "best_onboarding_latency": {
                "run_id": best_latency["run_id"],
                "value": best_latency["public_metrics"]["onboarding_latency_min"],
            },
            "best_alignment_index": {
                "run_id": best_alignment["run_id"],
                "value": best_alignment["public_metrics"]["alignment_index"],
            },
            "best_first_pass_success_rate": {
                "run_id": best_first_pass["run_id"],
                "value": best_first_pass["public_metrics"]["first_pass_success_rate"],
            },
        },
        "not_yet_instrumented": not_yet_instrumented,
    }


def write_markdown(path: Path, payload: dict) -> None:
    lines = [
        "# Public Benchmark Metrics",
        "",
        f"Runs analyzed: {len(payload['runs'])}",
        "",
        "## Public Utility Signals",
        "",
    ]
    for row in payload["runs"]:
        metrics = row["public_metrics"]
        lines.append(
            f"- {row['date']} | {row['run_id']} | {row['tool']} | mode={row['context_mode']} | "
            f"success={metrics['task_success_rate']} alignment={metrics['alignment_index']} "
            f"latency={metrics['onboarding_latency_min']} clarify={metrics['clarification_turns_avg']} "
            f"first_pass={metrics['first_pass_success_rate']} prompt_avg_chars={row['prompt_payload_avg_chars']}"
        )

    paired_delta = payload.get("with_vs_without_id_delta")
    if paired_delta is not None:
        lines.extend(["", "## With vs Without ID Delta", ""])
        for pair in paired_delta["pairs"]:
            deltas = pair["deltas"]
            lines.append(
                f"- {pair['comparison_group']} | with_id={pair['with_id_run_id']} | without_id={pair['without_id_run_id']} | "
                f"success_delta={deltas['task_success_rate']} alignment_delta={deltas['alignment_index']} "
                f"latency_improvement={deltas['onboarding_latency_min']} clarify_improvement={deltas['clarification_turns_avg']}"
            )
        lines.append("")
        lines.append("Average deltas:")
        for metric, value in paired_delta["average_deltas"].items():
            lines.append(f"- {metric}: {value}")

    prompt_reduction = payload.get("prompt_length_reduction")
    if prompt_reduction is not None:
        lines.extend(["", "## Prompt Length Reduction", ""])
        lines.append(f"- average_reduction_ratio: {prompt_reduction['average_reduction_ratio']}")
        lines.append(f"- average_reduction_chars: {prompt_reduction['average_reduction_chars']}")
        for pair in prompt_reduction["pairs"]:
            lines.append(
                f"- {pair['comparison_group']} | with_id={pair['with_id_run_id']} | without_id={pair['without_id_run_id']} | "
                f"avg_ratio={pair['average_reduction_ratio']} avg_chars={pair['average_reduction_chars']}"
            )

    freshness = payload["profile_freshness"]
    lines.extend(["", "## Profile Freshness", ""])
    lines.append(f"- owner: {freshness['owner_id']}")
    lines.append(f"- overall_score: {freshness['overall_score']}")
    for profile in freshness["profiles"]:
        lines.append(
            f"- {profile['path']}: score={profile['freshness_score']} age_days={profile['age_days']} ttl={profile['freshness_ttl_days']}"
        )

    lines.extend(["", "## Not Yet Instrumented", ""])
    for metric, note in payload["not_yet_instrumented"].items():
        lines.append(f"- {metric}: {note}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    runs_root = Path(args.runs_root)
    profiles_root = Path(args.profiles_root)
    try:
        payload = build_payload(runs_root, profiles_root, args.owner_id)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    out_json = Path(args.output_json)
    out_md = Path(args.output_md)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_markdown(out_md, payload)
    print(f"Generated: {out_json}")
    print(f"Generated: {out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
