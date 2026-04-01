#!/usr/bin/env python3
"""Bootstrap a new owner profile directory with minimal starter artifacts."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner-id", required=True, help="Owner id for profiles/<owner-id>/")
    parser.add_argument("--owner-alias", help="Owner alias; defaults to owner-id")
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root")
    parser.add_argument("--today", help="Override current date (YYYY-MM-DD)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing starter files")
    return parser.parse_args()


def build_privacy_policy(owner_id: str, today: str) -> dict:
    return {
        "policy_version": "1.0.0",
        "owner_id": owner_id,
        "updated_at": today,
        "default_access": "task_class_scoped",
        "task_classes": [
            "coding",
            "research",
            "writing",
            "agent_orchestration",
            "image_video",
        ],
        "rules": [
            {
                "field_path": "profiles.core.communication",
                "access": "always_share",
                "rationale": "Communication preferences are low-risk operational context and should travel with the profile.",
            },
            {
                "field_path": "profiles.core.rules.always_do",
                "access": "always_share",
                "rationale": "Core operational rules should remain portable across tools.",
            },
            {
                "field_path": "profiles.core.rules.never_do",
                "access": "always_share",
                "rationale": "Negative safety and behavior constraints should remain portable across tools.",
            },
            {
                "field_path": "profiles.core.rules.ask_before",
                "access": "always_share",
                "rationale": "Ask-before constraints are safety-critical and should not be dropped in portable contexts.",
            },
            {
                "field_path": "profiles.core.rules.default_assumptions",
                "access": "always_share",
                "rationale": "Default assumptions are part of the portable operating contract.",
            },
            {
                "field_path": "profiles.core.quality_bar",
                "access": "always_share",
                "rationale": "Quality bar is low-risk operational guidance and should remain visible in compact exports.",
            },
            {
                "field_path": "profiles.core.priority_domains",
                "access": "always_share",
                "rationale": "Priority domains are part of task routing rather than sensitive personal data.",
            },
            {
                "field_path": "profiles.core.tool_notes",
                "access": "always_share",
                "rationale": "Tool-level operating notes are safe-share by default.",
            },
            {
                "field_path": "profiles.extended.environment_assumptions",
                "access": "local_only",
                "rationale": "Environment details can expose local paths or private operational assumptions.",
            },
            {
                "field_path": "profiles.extended.domain_workflows",
                "access": "task_class_scoped",
                "allowed_task_classes": [
                    "coding",
                    "research",
                    "writing",
                    "agent_orchestration",
                ],
                "rationale": "Detailed workflows should be released only when directly relevant to the task class.",
            },
        ],
        "notes": [
            "Bootstrap policy created from the default starter template.",
            "Review before publishing or sharing artifacts outside trusted local workflows.",
        ],
    }


def build_handshake(owner_id: str) -> str:
    return "\n".join(
        [
            "# Handshake",
            "",
            f"Owner: `{owner_id}`",
            "",
            "Before acting:",
            "1. confirm the active profile source and freshness",
            "2. summarize understanding in 5-10 bullets",
            "3. list uncertainty and assumptions",
            "4. ask for correction if confidence is low",
            "",
        ]
    )


def render_minimal(template_path: Path, owner_id: str, owner_alias: str, today: str) -> str:
    text = template_path.read_text(encoding="utf-8")
    replacements = {
        '"owner-id"': f'"{owner_id}"',
        '"owner-alias"': f'"{owner_alias}"',
        '"YYYY-MM-DD"': f'"{today}"',
    }
    for src, dst in replacements.items():
        text = text.replace(src, dst)
    return text


def write_file(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite existing file without --force: {path}")
    path.write_text(content, encoding="utf-8")


def main() -> int:
    args = parse_args()
    today = args.today or date.today().isoformat()
    owner_alias = args.owner_alias or args.owner_id

    profiles_root = Path(args.profiles_root)
    owner_dir = profiles_root / args.owner_id
    owner_dir.mkdir(parents=True, exist_ok=True)

    template_path = Path(__file__).resolve().parents[1] / "templates" / "profile.minimal.md"
    if not template_path.exists():
        print(f"ERROR: missing template: {template_path}")
        return 1

    minimal_content = render_minimal(template_path, args.owner_id, owner_alias, today)
    privacy_policy = json.dumps(build_privacy_policy(args.owner_id, today), ensure_ascii=False, indent=2) + "\n"
    handshake = build_handshake(args.owner_id)

    write_file(owner_dir / "profile.minimal.md", minimal_content, args.force)
    write_file(owner_dir / "privacy-policy.v1.json", privacy_policy, args.force)
    write_file(owner_dir / "handshake.md", handshake, args.force)

    print(f"Bootstrapped: {owner_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
