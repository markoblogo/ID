#!/usr/bin/env python3
"""Export a policy-aware MCP resource payload derived from ID context."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from export_context_compact import build_context
from privacy_policy import load_json, load_policy


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export MCP resource payload from ID context")
    parser.add_argument("--owner-id", required=True, help="Owner id")
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root")
    parser.add_argument("--output", help="Output path; defaults to profiles/<owner>/mcp.context.resource.json")
    parser.add_argument(
        "--task-class",
        help="Optional task class for policy-aware inclusion of scoped fields",
    )
    return parser.parse_args()


def build_resource(interop: dict, policy: dict | None, owner_id: str, task_class: str | None) -> dict:
    compact_context = build_context(interop, policy, task_class)
    return {
        "resource_version": "1.0.0",
        "owner_id": owner_id,
        "uri": f"id://{owner_id}/context.compact",
        "name": f"ID Context: {owner_id}",
        "description": "Policy-aware MCP resource derived from ID compact context",
        "mime_type": "application/json",
        "contents": compact_context,
        "policy": {
            "applied": policy is not None,
            "task_class": task_class,
            "source": f"profiles/{owner_id}/privacy-policy.v1.json" if policy is not None else None,
        },
    }


def main() -> int:
    args = parse_args()
    profiles_root = Path(args.profiles_root)
    interop_path = profiles_root / args.owner_id / "interop.v1.json"
    if not interop_path.exists():
        print(f"ERROR: missing input file: {interop_path}")
        return 1

    interop = load_json(interop_path)
    policy = load_policy(profiles_root, args.owner_id)
    resource = build_resource(interop, policy, args.owner_id, args.task_class)

    output_path = Path(args.output) if args.output else profiles_root / args.owner_id / "mcp.context.resource.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(resource, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
