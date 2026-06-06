#!/usr/bin/env python3
"""Lightweight migration helper for profile metadata upgrades."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

KNOWN_VERSIONS = {"v0.1", "v0.2", "v0.3"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply explicit migration steps across owner artifacts")
    parser.add_argument("--owner-id", required=True, help="Owner id under profiles/<owner-id>/")
    parser.add_argument("--from", dest="from_version", required=True)
    parser.add_argument("--to", dest="to_version", required=True)
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes only")
    parser.add_argument("--json", action="store_true", help="Machine-readable plan output")
    return parser.parse_args()


def parse_profile_file(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    meta: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')

    return meta, parts[2].lstrip("\n")


def render_front_matter(meta: dict[str, str]) -> str:
    lines = ["---"]
    for key in sorted(meta.keys()):
        value = meta[key]
        if value.isdigit():
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: \"{value}\"")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def migration_steps(meta: dict[str, str], owner_id: str, from_version: str, to_version: str, today: str) -> list[str]:
    changes: list[str] = []

    if not meta.get("owner_alias"):
        meta["owner_alias"] = owner_id
        changes.append("added owner_alias")

    if not meta.get("trust_level"):
        meta["trust_level"] = "trusted"
        changes.append("added trust_level")

    if not meta.get("created_at"):
        meta["created_at"] = today
        changes.append("added created_at")

    if not meta.get("updated_at"):
        meta["updated_at"] = today
        changes.append("added updated_at")

    if not meta.get("freshness_ttl_days"):
        meta["freshness_ttl_days"] = "14"
        changes.append("added freshness_ttl_days")

    if from_version == "v0.1" and to_version == "v0.2":
        current = meta.get("version", "")
        if not current.startswith("0.2"):
            meta["version"] = "0.2.0"
            changes.append("upgraded version to 0.2.0")

    return changes


def apply_profile_migration(path: Path, *, owner_id: str, from_version: str, to_version: str, dry_run: bool, today: str) -> list[str]:
    meta, body = parse_profile_file(path)
    if not meta:
        return ["missing front matter"]

    changes = migration_steps(meta, owner_id, from_version, to_version, today)
    if changes and not dry_run:
        path.write_text(f"{render_front_matter(meta)}{body}", encoding="utf-8")
    return changes


def migrate_owner(owner_dir: Path, *, today: str, from_version: str, to_version: str, dry_run: bool) -> list[dict[str, Any]]:
    if not owner_dir.exists():
        return [{"file": str(owner_dir), "changes": ["owner directory missing"]}]

    profile_files = [
        owner_dir / "profile.core.md",
        owner_dir / "profile.extended.md",
        owner_dir / "profile.minimal.md",
    ]

    actions: list[dict[str, Any]] = []
    for path in profile_files:
        if not path.exists():
            continue
        changes = apply_profile_migration(
            path,
            owner_id=owner_dir.name,
            from_version=from_version,
            to_version=to_version,
            dry_run=dry_run,
            today=today,
        )
        actions.append(
            {
                "file": str(path),
                "dry_run": dry_run,
                "changes": changes,
            }
        )

    if not actions:
        actions.append({"file": str(owner_dir), "dry_run": dry_run, "changes": ["no known profile files to migrate"]})

    return actions


def main() -> int:
    args = parse_args()

    if args.from_version not in KNOWN_VERSIONS or args.to_version not in KNOWN_VERSIONS:
        print("ERROR: unsupported migration versions")
        print(f"supported: {', '.join(sorted(KNOWN_VERSIONS))}")
        return 1

    if args.from_version == args.to_version:
        print("No migration needed: source and destination versions match")
        return 0

    plan = migrate_owner(
        Path(args.profiles_root) / args.owner_id,
        today=date.today().isoformat(),
        from_version=args.from_version,
        to_version=args.to_version,
        dry_run=args.dry_run,
    )

    if args.json:
        print(json.dumps({"owner": args.owner_id, "from": args.from_version, "to": args.to_version, "dry_run": args.dry_run, "plan": plan}, indent=2, ensure_ascii=False))
        return 0

    for item in plan:
        status = "changed" if item["changes"] else "no-op"
        if args.dry_run and item["changes"]:
            status = "would_write"
        print(f"{status}: {item['file']}")
        for change in item["changes"]:
            print(f"  - {change}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
