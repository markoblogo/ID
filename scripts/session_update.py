#!/usr/bin/env python3
"""Append standardized post-session entry to profile CHANGELOG."""

from __future__ import annotations

import argparse
from datetime import date, timedelta
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Append session entry into profile CHANGELOG")
    parser.add_argument("--owner-id", required=True, help="Owner id, e.g. markoblogo")
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root")
    parser.add_argument("--date", help="Entry date YYYY-MM-DD (default: today)")
    parser.add_argument("--next-review-date", help="YYYY-MM-DD (default: +14 days)")
    parser.add_argument("--session-context", required=True, help="Session context summary")
    parser.add_argument("--sections-used", required=True, help="Profile sections used")
    parser.add_argument("--changes-made", required=True, help="What changed")
    parser.add_argument("--open-questions", default="None", help="Open questions")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    today = date.fromisoformat(args.date) if args.date else date.today()
    next_review = (
        date.fromisoformat(args.next_review_date)
        if args.next_review_date
        else today + timedelta(days=14)
    )

    owner_dir = Path(args.profiles_root) / args.owner_id
    owner_dir.mkdir(parents=True, exist_ok=True)
    changelog = owner_dir / "CHANGELOG.md"

    if changelog.exists():
        content = changelog.read_text(encoding="utf-8", errors="ignore")
    else:
        content = "# Profile Changelog\n\n## Entries\n\n"

    if "## Entries" not in content:
        content = content.rstrip() + "\n\n## Entries\n\n"

    entry = (
        f"- date: {today.isoformat()}\n"
        f"- session_context: \"{args.session_context}\"\n"
        f"- sections_used: \"{args.sections_used}\"\n"
        f"- changes_made: \"{args.changes_made}\"\n"
        f"- open_questions: \"{args.open_questions}\"\n"
        f"- next_review_date: {next_review.isoformat()}\n"
    )

    new_content = content.rstrip() + "\n\n" + entry
    changelog.write_text(new_content + "\n", encoding="utf-8")

    print(f"Updated: {changelog}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
