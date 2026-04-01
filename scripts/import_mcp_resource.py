#!/usr/bin/env python3
"""Import an MCP context resource into a reviewable markdown draft."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from import_context_compact import render_markdown


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import mcp.context.resource.json into a markdown draft")
    parser.add_argument("--owner-id", help="Owner id under profiles/<owner-id>/")
    parser.add_argument("--input", help="Path to mcp.context.resource.json")
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root")
    parser.add_argument(
        "--output",
        help="Output path; defaults to profiles/<owner>/draft.from-mcp.md",
    )
    return parser.parse_args()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def resolve_paths(args: argparse.Namespace) -> tuple[Path, Path]:
    profiles_root = Path(args.profiles_root)
    if bool(args.owner_id) == bool(args.input):
        raise SystemExit("Provide exactly one of --owner-id or --input")

    input_path = (
        Path(args.input)
        if args.input
        else profiles_root / args.owner_id / "mcp.context.resource.json"
    )
    output_path = (
        Path(args.output)
        if args.output
        else profiles_root / (args.owner_id or input_path.parent.name) / "draft.from-mcp.md"
    )
    return input_path, output_path


def render_resource_markdown(resource: dict, source_path: str) -> str:
    compact_body = render_markdown(resource["contents"], source_path)
    policy = resource.get("policy", {})
    prefix = "\n".join(
        [
            "# Draft Profile From MCP Resource",
            "",
            f"- owner_id: `{resource['owner_id']}`",
            f"- resource_version: `{resource['resource_version']}`",
            f"- uri: `{resource['uri']}`",
            f"- mime_type: `{resource['mime_type']}`",
            f"- policy_applied: `{policy.get('applied')}`",
            f"- policy_task_class: `{policy.get('task_class')}`",
            f"- policy_source: `{policy.get('source')}`",
            "",
            "This file is a lossy import candidate generated from `mcp.context.resource.json`.",
            "Review manually before merging into canonical markdown profile files.",
            "",
        ]
    )
    return prefix + compact_body.split("\n", 1)[1]


def main() -> int:
    args = parse_args()
    input_path, output_path = resolve_paths(args)
    resource = load_json(input_path)
    markdown = render_resource_markdown(resource, str(input_path))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Generated: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
