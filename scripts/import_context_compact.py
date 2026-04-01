#!/usr/bin/env python3
"""Import a compact context artifact into a reviewable markdown draft."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import context.compact.json into a markdown draft")
    parser.add_argument("--owner-id", help="Owner id under profiles/<owner-id>/")
    parser.add_argument("--input", help="Path to context.compact.json")
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root")
    parser.add_argument(
        "--output",
        help="Output path; defaults to profiles/<owner>/draft.from-context-compact.md",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def format_list(items: list[str], fallback: str = "- [uncertain] none imported") -> str:
    if not items:
        return fallback
    return "\n".join(f"- {item}" for item in items)


def render_markdown(context: dict, source_path: str) -> str:
    rules = context.get("rules", {})
    loss_notes = context.get("loss_notes", [])
    return "\n".join(
        [
            "# Draft Profile From Compact Context",
            "",
            f"- owner_id: `{context['owner_id']}`",
            f"- context_version: `{context['context_version']}`",
            f"- updated_at: `{context['updated_at']}`",
            f"- freshness_ttl_days: `{context['freshness_ttl_days']}`",
            f"- trust_level: `{context['trust_level']}`",
            f"- source_artifact: `{source_path}`",
            "",
            "This file is a lossy import candidate generated from `context.compact.json`.",
            "Review manually before merging into canonical markdown profile files.",
            "",
            "## Communication Signals",
            "",
            format_list(context.get("communication", [])),
            "",
            "## Rules Signals",
            "",
            "### Always Do",
            "",
            format_list(rules.get("always_do", [])),
            "",
            "### Never Do",
            "",
            format_list(rules.get("never_do", [])),
            "",
            "### Ask Before",
            "",
            format_list(rules.get("ask_before", [])),
            "",
            "### Default Assumptions",
            "",
            format_list(rules.get("default_assumptions", [])),
            "",
            "## Quality Bar Signals",
            "",
            format_list(context.get("quality_bar", [])),
            "",
            "## Priority Domains Signals",
            "",
            format_list(context.get("priority_domains", [])),
            "",
            "## Tool Notes Signals",
            "",
            format_list(context.get("tool_notes", [])),
            "",
            "## Loss Notes",
            "",
            format_list(loss_notes),
            "",
        ]
    )


def resolve_paths(args: argparse.Namespace) -> tuple[Path, Path]:
    profiles_root = Path(args.profiles_root)
    if bool(args.owner_id) == bool(args.input):
        raise SystemExit("Provide exactly one of --owner-id or --input")

    input_path = (
        Path(args.input)
        if args.input
        else profiles_root / args.owner_id / "context.compact.json"
    )
    output_path = (
        Path(args.output)
        if args.output
        else profiles_root / (args.owner_id or input_path.parent.name) / "draft.from-context-compact.md"
    )
    return input_path, output_path


def main() -> int:
    args = parse_args()
    input_path, output_path = resolve_paths(args)
    context = load_json(input_path)
    markdown = render_markdown(context, str(input_path))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Generated: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
