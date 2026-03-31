#!/usr/bin/env python3
"""Fail fast if forbidden raw data is staged/tracked for publish."""

from __future__ import annotations

import argparse
import subprocess


FORBIDDEN_PREFIX = "data/raw/"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check publish guard for data/raw/**")
    parser.add_argument(
        "--all-tracked",
        action="store_true",
        help="Check all tracked files in repo, not only staged files",
    )
    return parser.parse_args()


def list_paths(cmd: list[str]) -> list[str]:
    proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    if proc.returncode != 0:
        return []
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def find_forbidden(paths: list[str]) -> list[str]:
    return [p for p in paths if p.startswith(FORBIDDEN_PREFIX) and not p.endswith('.gitkeep')]


def main() -> int:
    args = parse_args()

    staged = list_paths(["git", "diff", "--cached", "--name-only"])
    bad_staged = find_forbidden(staged)

    bad_tracked: list[str] = []
    if args.all_tracked:
        tracked = list_paths(["git", "ls-files"])
        bad_tracked = find_forbidden(tracked)

    if bad_staged:
        for path in bad_staged:
            print(f"ERROR: staged forbidden path: {path}")

    if bad_tracked:
        for path in bad_tracked:
            print(f"ERROR: tracked forbidden path: {path}")

    if bad_staged or bad_tracked:
        return 1

    print("Publish guard passed: no forbidden data/raw paths found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
