#!/usr/bin/env python3
"""Lint profile content quality heuristics without replacing structural validation."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from validate_profile import list_profile_files, parse_front_matter

PLACEHOLDER_RE = re.compile(r"\b(todo|tbd|fixme|lorem ipsum)\b|\?\?\?", re.IGNORECASE)
CORE_REQUIRED_HEADINGS = {
    "## 1. Communication Style",
    "## 2. Task Execution Rules",
    "## 3. Quality Bar",
    "## 4. Priority Domains",
}


@dataclass
class LintIssue:
    level: str
    file: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root directory")
    parser.add_argument("--owner-id", help="Lint a specific owner only")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return non-zero when warnings are found",
    )
    return parser.parse_args()


def read_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    if not text.startswith("---\n"):
        return text
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return text
    return parts[2]


def normalize_phrase(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", value.lower())).strip()


def collect_nested_rule_items(lines: list[str], label: str) -> set[str]:
    target = f"- {label}:"
    values: set[str] = set()
    active = False
    for line in lines:
        if line.startswith("- ") and line.strip().endswith(":"):
            active = line.strip() == target
            continue
        if active and line.startswith("  - "):
            normalized = normalize_phrase(line[4:])
            if normalized:
                values.add(normalized)
        elif active and line.startswith("- "):
            active = False
    return values


def lint_profile(path: Path) -> list[LintIssue]:
    issues: list[LintIssue] = []
    meta = parse_front_matter(path)
    body = read_body(path)
    lines = body.splitlines()

    if not meta.get("confidence_notes"):
        issues.append(LintIssue("WARN", str(path), "Missing confidence_notes; provenance/confidence is underspecified"))

    if PLACEHOLDER_RE.search(body):
        issues.append(LintIssue("WARN", str(path), "Contains placeholder text (TODO/TBD/FIXME/???)"))

    bullet_lines = [line for line in lines if line.lstrip().startswith("- ")]
    h2_lines = [line.strip() for line in lines if line.startswith("## ")]

    if len(bullet_lines) < 8:
        issues.append(LintIssue("WARN", str(path), f"Profile may be underspecified: only {len(bullet_lines)} bullet lines found"))
    if len(h2_lines) < 3:
        issues.append(LintIssue("WARN", str(path), f"Profile may be underspecified: only {len(h2_lines)} level-2 sections found"))

    if path.name == "profile.core.md":
        missing_headings = sorted(CORE_REQUIRED_HEADINGS - set(h2_lines))
        for heading in missing_headings:
            issues.append(LintIssue("WARN", str(path), f"Missing expected core heading: {heading}"))

        always_do = collect_nested_rule_items(lines, "Always do")
        never_do = collect_nested_rule_items(lines, "Never do")
        overlap = sorted(always_do & never_do)
        for item in overlap:
            issues.append(LintIssue("WARN", str(path), f"Potential contradiction between Always do and Never do: {item}"))

    return issues


def main() -> int:
    args = parse_args()
    root = Path(args.profiles_root)
    profile_files = list(list_profile_files(root, args.owner_id))
    if not profile_files:
        print("WARN: no profile files found to lint")
        return 0

    issues: list[LintIssue] = []
    for path in profile_files:
        issues.extend(lint_profile(path))

    warns = [issue for issue in issues if issue.level == "WARN"]
    for issue in issues:
        print(f"{issue.level}: {issue.file}: {issue.message}")

    print(f"Lint summary: files={len(profile_files)} warnings={len(warns)}")
    return 1 if args.strict and warns else 0


if __name__ == "__main__":
    raise SystemExit(main())
