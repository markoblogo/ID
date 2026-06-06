#!/usr/bin/env python3
"""Generate README evidence snippet from public benchmark metrics."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

START_MARKER = "<!-- METRICS_SNIPPET_START -->"
END_MARKER = "<!-- METRICS_SNIPPET_END -->"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate live metrics snippet in README")
    parser.add_argument("--metrics-json", default="benchmarks/runs/public-metrics.json")
    parser.add_argument("--readme", default="README.md")
    parser.add_argument("--snippet", default="docs/public-metrics-snippet.md")
    return parser.parse_args()


def build_snippet(payload: dict) -> str:
    lines: list[str] = [
        "### Live Public Metrics",
        "",
        f"Runs analyzed: `{len(payload.get('runs', []))}`",
        "",
        "| Metric | Value | Meaning |",
        "| --- | --- | --- |",
    ]

    deltas = payload.get("with_vs_without_id_delta") or {}
    averages = deltas.get("average_deltas") or {}
    if averages:
        items = [
            ("onboarding latency", averages.get("onboarding_latency_min", "n/a"), "Less is better"),
            ("clarification turns", averages.get("clarification_turns_avg", "n/a"), "Less hand-offs"),
            ("task success", averages.get("task_success_rate", "n/a"), "Higher is better"),
            ("alignment index", averages.get("alignment_index", "n/a"), "Higher is better"),
        ]
    else:
        items = [
            ("with-vs-without ID", "not yet available", "Requires matched control runs"),
        ]

    for metric, value, meaning in items:
        lines.append(f"| {metric} | {value} | {meaning} |")

    freshness = payload.get("profile_freshness", {})
    lines.extend(
        [
            "",
            f"Profile freshness score (owner `{freshness.get('owner_id', 'unknown')}`): `{freshness.get('overall_score', 'n/a')}`",
            "",
            "```",
            "Key artifacts:",
        ]
    )
    for profile in freshness.get("profiles", []):
        lines.append(
            f"- {profile.get('path')}: score={profile.get('freshness_score')} age={profile.get('age_days')} ttl={profile.get('freshness_ttl_days')}"
        )
    lines.append("```")
    return "\n".join(lines)


def update_readme(readme_path: Path, snippet: str, snippet_path: Path) -> None:
    readme = readme_path.read_text(encoding="utf-8")
    if START_MARKER not in readme or END_MARKER not in readme:
        raise SystemExit("README markers not found: add METRICS_SNIPPET_START/END")

    before, rest = readme.split(START_MARKER, 1)
    after = rest.split(END_MARKER, 1)[1]
    updated = f"{before}{START_MARKER}\n{snippet}\n\n{END_MARKER}{after}"
    readme_path.write_text(updated, encoding="utf-8")
    snippet_path.write_text(f"{snippet}\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    metrics_path = Path(args.metrics_json)
    if not metrics_path.exists():
        print(f"ERROR: metrics file missing: {metrics_path}")
        return 1

    payload = json.loads(metrics_path.read_text(encoding="utf-8"))
    snippet = build_snippet(payload)
    update_readme(Path(args.readme), snippet, Path(args.snippet))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
