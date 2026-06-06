#!/usr/bin/env python3
"""Wrapper for `idctl init` with optional interactive wizard UX."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialize owner artifacts via bootstrap flow")
    parser.add_argument("--owner-id", help="Owner id for profiles/<owner-id>/")
    parser.add_argument("--owner-alias", help="Owner alias")
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root")
    parser.add_argument("--today", help="Date override in YYYY-MM-DD")
    parser.add_argument("--force", action="store_true", help="Overwrite existing starter files")
    parser.add_argument("--interactive", action="store_true", help="Prompt for required values")
    return parser.parse_args()


def resolve_value(name: str, value: str | None, interactive: bool, fallback: str | None = None) -> str:
    if value:
        return value
    if interactive:
        prompt = f"{name}: "
        response = input(prompt).strip()
        if response:
            return response
        if fallback is not None:
            return fallback
    raise SystemExit(f"--{name.lower().replace(' ', '-') if ' ' not in name else name.replace(' ', '-')} is required")


def main() -> int:
    args = parse_args()
    owner_id = resolve_value("Owner ID", args.owner_id, args.interactive)
    owner_alias = resolve_value("Owner alias", args.owner_alias, args.interactive, fallback=owner_id)

    command = [
        sys.executable,
        str(Path(__file__).resolve().parents[1] / "scripts" / "bootstrap_owner.py"),
        "--owner-id",
        owner_id,
        "--owner-alias",
        owner_alias,
        "--profiles-root",
        args.profiles_root,
    ]
    if args.today:
        command.extend(["--today", args.today])
    if args.force:
        command.append("--force")

    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
