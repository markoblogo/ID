#!/usr/bin/env python3
"""Validate profile metadata freshness and publishing safety checks.

Checks:
- required metadata in profile front matter
- date/semver/trust-level formats
- freshness TTL against updated_at
- optional git staged/tracked guard for data/raw/**
"""

from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

REQUIRED_KEYS = {
    "profile_id",
    "owner_alias",
    "version",
    "created_at",
    "updated_at",
    "freshness_ttl_days",
    "trust_level",
}
TRUST_LEVELS = {"trusted", "provisional", "archival"}
SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


@dataclass
class ValidationIssue:
    level: str  # ERROR or WARN
    file: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate ID profiles and raw-data publishing guard")
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root directory")
    parser.add_argument("--owner-id", help="Validate specific owner only")
    parser.add_argument("--today", help="Override current date (YYYY-MM-DD)")
    parser.add_argument(
        "--allow-stale",
        action="store_true",
        help="Do not fail on stale profiles; emit warning instead",
    )
    parser.add_argument(
        "--check-raw-staged",
        action="store_true",
        help="Fail if staged files include data/raw/**",
    )
    parser.add_argument(
        "--check-raw-tracked",
        action="store_true",
        help="Fail if tracked files include data/raw/**",
    )
    return parser.parse_args()


def parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def parse_front_matter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}

    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def list_profile_files(root: Path, owner_id: str | None) -> Iterable[Path]:
    if owner_id:
        owner_dir = root / owner_id
        if not owner_dir.exists():
            return []
        return sorted(p for p in owner_dir.glob("profile*.md") if p.is_file())

    return sorted(p for p in root.rglob("profile*.md") if p.is_file())


def validate_profile(path: Path, today: date, allow_stale: bool) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    meta = parse_front_matter(path)

    if not meta:
        return [ValidationIssue("ERROR", str(path), "Missing or invalid front matter block")]

    missing = sorted(REQUIRED_KEYS - set(meta.keys()))
    for key in missing:
        issues.append(ValidationIssue("ERROR", str(path), f"Missing required metadata key: {key}"))

    version = meta.get("version", "")
    if version and not SEMVER_RE.match(version):
        issues.append(ValidationIssue("ERROR", str(path), "Invalid version format; expected semver X.Y.Z"))

    trust = meta.get("trust_level", "")
    if trust and trust not in TRUST_LEVELS:
        issues.append(
            ValidationIssue(
                "ERROR",
                str(path),
                f"Invalid trust_level '{trust}', expected one of: {', '.join(sorted(TRUST_LEVELS))}",
            )
        )

    created_at_raw = meta.get("created_at", "")
    updated_at_raw = meta.get("updated_at", "")
    created_at = parse_date(created_at_raw) if created_at_raw else None
    updated_at = parse_date(updated_at_raw) if updated_at_raw else None

    if created_at_raw and not created_at:
        issues.append(ValidationIssue("ERROR", str(path), "Invalid created_at date (expected YYYY-MM-DD)"))
    if updated_at_raw and not updated_at:
        issues.append(ValidationIssue("ERROR", str(path), "Invalid updated_at date (expected YYYY-MM-DD)"))

    ttl_raw = meta.get("freshness_ttl_days", "")
    ttl: int | None = None
    if ttl_raw:
        try:
            ttl = int(ttl_raw)
            if ttl <= 0:
                raise ValueError
        except ValueError:
            issues.append(ValidationIssue("ERROR", str(path), "freshness_ttl_days must be a positive integer"))

    if updated_at and ttl:
        age = (today - updated_at).days
        if age > ttl:
            level = "WARN" if allow_stale else "ERROR"
            issues.append(
                ValidationIssue(
                    level,
                    str(path),
                    f"Profile stale: updated_at={updated_at}, age={age} days > ttl={ttl}",
                )
            )

    return issues


def run_git_list(cmd: list[str]) -> list[str]:
    try:
        proc = subprocess.run(cmd, check=False, capture_output=True, text=True)
    except FileNotFoundError:
        return []

    if proc.returncode != 0:
        return []

    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def check_raw_guard(check_staged: bool, check_tracked: bool) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    if check_staged:
        staged = run_git_list(["git", "diff", "--cached", "--name-only"])
        bad = [p for p in staged if p.startswith("data/raw/") and not p.endswith(".gitkeep")]
        for p in bad:
            issues.append(ValidationIssue("ERROR", p, "Forbidden staged path under data/raw/**"))

    if check_tracked:
        tracked = run_git_list(["git", "ls-files"])
        bad = [p for p in tracked if p.startswith("data/raw/") and not p.endswith(".gitkeep")]
        for p in bad:
            issues.append(ValidationIssue("ERROR", p, "Forbidden tracked path under data/raw/**"))

    return issues


def main() -> int:
    args = parse_args()
    root = Path(args.profiles_root)
    today = parse_date(args.today) if args.today else date.today()
    if today is None:
        print("ERROR: --today must be YYYY-MM-DD")
        return 2

    issues: list[ValidationIssue] = []

    profile_files = list(list_profile_files(root, args.owner_id))
    if not profile_files:
        print("WARN: no profile files found to validate")

    for path in profile_files:
        issues.extend(validate_profile(path, today, args.allow_stale))

    issues.extend(check_raw_guard(args.check_raw_staged, args.check_raw_tracked))

    errors = [i for i in issues if i.level == "ERROR"]
    warns = [i for i in issues if i.level == "WARN"]

    for issue in issues:
        print(f"{issue.level}: {issue.file}: {issue.message}")

    print(
        f"Validation summary: files={len(profile_files)} errors={len(errors)} warnings={len(warns)}"
    )

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
