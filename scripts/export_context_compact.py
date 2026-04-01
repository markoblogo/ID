#!/usr/bin/env python3
"""Export a compact portable context JSON from the interop artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from privacy_policy import append_policy_loss_notes, export_array, load_json, load_policy

BASE_LOSS_NOTES = [
    "Extended workflows omitted",
    "Historical corrections omitted",
    "Use full profile or interop.v1.json for richer context",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export compact portable context JSON")
    parser.add_argument("--owner-id", required=True, help="Owner id")
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root")
    parser.add_argument("--output", help="Output path; defaults to profiles/<owner>/context.compact.json")
    parser.add_argument(
        "--task-class",
        help="Optional task class for policy-aware inclusion of task_class_scoped fields",
    )
    return parser.parse_args()


def build_context(interop: dict, policy: dict | None, task_class: str | None) -> dict:
    core = interop["profiles"]["core"]
    metadata = core["metadata"]
    omissions: list[str] = []
    rules = core["rules"]

    return {
        "context_version": metadata["version"],
        "owner_id": interop["owner_id"],
        "updated_at": metadata["updated_at"],
        "freshness_ttl_days": metadata["freshness_ttl_days"],
        "trust_level": metadata["trust_level"],
        "communication": export_array(
            policy,
            "profiles.core.communication",
            core.get("communication", []),
            task_class,
            omissions,
        ),
        "rules": {
            "always_do": export_array(
                policy,
                "profiles.core.rules.always_do",
                rules.get("always_do", []),
                task_class,
                omissions,
            ),
            "never_do": export_array(
                policy,
                "profiles.core.rules.never_do",
                rules.get("never_do", []),
                task_class,
                omissions,
            ),
            "ask_before": export_array(
                policy,
                "profiles.core.rules.ask_before",
                rules.get("ask_before", []),
                task_class,
                omissions,
            ),
            "default_assumptions": export_array(
                policy,
                "profiles.core.rules.default_assumptions",
                rules.get("default_assumptions", []),
                task_class,
                omissions,
            ),
        },
        "quality_bar": export_array(
            policy,
            "profiles.core.quality_bar",
            core.get("quality_bar", []),
            task_class,
            omissions,
        ),
        "priority_domains": export_array(
            policy,
            "profiles.core.priority_domains",
            core.get("priority_domains", []),
            task_class,
            omissions,
        ),
        "tool_notes": export_array(
            policy,
            "profiles.core.tool_notes",
            core.get("tool_notes", []),
            task_class,
            omissions,
        ),
        "loss_notes": append_policy_loss_notes(BASE_LOSS_NOTES, omissions, policy, task_class),
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
    context = build_context(interop, policy, args.task_class)

    output_path = Path(args.output) if args.output else profiles_root / args.owner_id / "context.compact.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(context, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
