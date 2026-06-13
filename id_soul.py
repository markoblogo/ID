from __future__ import annotations

import argparse
import difflib
import json
import re
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path


MANUAL_START = "<!-- SOUL_MANUAL_START -->"
MANUAL_END = "<!-- SOUL_MANUAL_END -->"
SECTION_NUMBER_RE = re.compile(r"^\d+\.\s*")
KEY_VALUE_RE = re.compile(r"^- ([a-z_]+):\s*(.*)$")
PLACEHOLDER_VALUES = {"", "-", "—", "TBD", "TODO", "None yet"}


@dataclass(frozen=True)
class SourceProfile:
    path: Path
    label: str
    metadata: dict[str, str]
    sections: dict[str, list[str]]


def parse_date(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}, text

    data: dict[str, str] = {}
    body_start = 0
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            body_start = index + 1
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data, "\n".join(lines[body_start:]).strip() + "\n"


def _normalize_heading(title: str) -> str:
    return SECTION_NUMBER_RE.sub("", title).strip()


def _clean_value(value: str) -> str | None:
    value = value.strip()
    if value in PLACEHOLDER_VALUES:
        return None
    return value


def extract_markdown_sections(body: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current_h2: str | None = None
    current_h3: str | None = None
    current_label: str | None = None

    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if line.startswith("## "):
            current_h2 = _normalize_heading(line[3:])
            current_h3 = None
            current_label = None
            sections.setdefault(current_h2, [])
            continue
        if line.startswith("### "):
            current_h3 = _normalize_heading(line[4:])
            current_label = None
            continue
        if not stripped.startswith("- "):
            continue
        if current_h2 is None:
            continue

        indent = len(line) - len(line.lstrip(" "))
        content = stripped[2:].strip()
        if not content:
            continue

        statement: str | None = None
        if ":" in content:
            key, value = content.split(":", 1)
            value = value.strip()
            if value:
                cleaned = _clean_value(value)
                if cleaned is not None:
                    statement = f"{key.strip()}: {cleaned}"
                current_label = None
            else:
                current_label = key.strip()
                continue
        else:
            cleaned = _clean_value(content)
            if cleaned is None:
                continue
            if indent >= 2 and current_label:
                statement = f"{current_label}: {cleaned}"
            else:
                statement = cleaned

        if statement is None:
            continue
        if current_h3:
            statement = f"{current_h3}: {statement}"
        sections.setdefault(current_h2, []).append(statement)

    return sections


def load_source_profiles(owner_dir: Path) -> list[SourceProfile]:
    file_order = [
        ("profile.minimal.md", "minimal"),
        ("profile.core.md", "core"),
        ("profile.extended.md", "extended"),
    ]
    sources: list[SourceProfile] = []
    for filename, label in file_order:
        path = owner_dir / filename
        if not path.is_file():
            continue
        metadata, body = parse_front_matter(path.read_text(encoding="utf-8", errors="ignore"))
        sources.append(
            SourceProfile(
                path=path,
                label=label,
                metadata=metadata,
                sections=extract_markdown_sections(body),
            )
        )
    return sources


def parse_changelog_entries(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    entries: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        match = KEY_VALUE_RE.match(raw_line)
        if not match:
            continue
        key, value = match.group(1), match.group(2).strip().strip('"')
        if key == "date" and current:
            entries.append(current)
            current = {}
        current[key] = value
    if current:
        entries.append(current)
    return entries


def extract_manual_block(existing_text: str | None) -> str:
    if not existing_text:
        return (
            "- Add owner-reviewed corrections here.\n"
            "- Prefix uncertain edits with `[manual-review]`.\n"
        )
    start = existing_text.find(MANUAL_START)
    end = existing_text.find(MANUAL_END)
    if start == -1 or end == -1 or end <= start:
        return (
            "- Add owner-reviewed corrections here.\n"
            "- Prefix uncertain edits with `[manual-review]`.\n"
        )
    content = existing_text[start + len(MANUAL_START):end].strip("\n")
    return (content + "\n") if content else ""


def _unique_bullets(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        normalized = item.strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        result.append(normalized)
    return result


def _section_items(sources: list[SourceProfile], section_names: tuple[str, ...]) -> list[str]:
    items: list[str] = []
    for source in sources:
        for section_name in section_names:
            for item in source.sections.get(section_name, []):
                items.append(f"[owner-stated/{source.label}] {item}")
    return _unique_bullets(items)


def _recent_signal_items(entries: list[dict[str, str]]) -> list[str]:
    signals: list[str] = []
    for entry in entries[-3:]:
        stamp = entry.get("date", "unknown-date")
        session = entry.get("session_context")
        changes = entry.get("changes_made")
        questions = entry.get("open_questions")
        if session:
            signals.append(f"[recent-session] {stamp}: {session}")
        if changes and changes != "None":
            signals.append(f"[recent-change] {stamp}: {changes}")
        if questions and questions not in {"None", "Closed", "None."}:
            signals.append(f"[open-question] {stamp}: {questions}")
    return _unique_bullets(signals)


def _freshness_lines(sources: list[SourceProfile], today: date, review_cadence_days: int) -> list[str]:
    lines: list[str] = []
    for source in sources:
        updated_at = parse_date(source.metadata.get("updated_at"))
        ttl_raw = source.metadata.get("freshness_ttl_days")
        ttl = int(ttl_raw) if ttl_raw and ttl_raw.isdigit() else None
        age_fragment = "unknown-age"
        status = "unknown"
        if updated_at:
            age = (today - updated_at).days
            age_fragment = f"age={age}d"
            if ttl is not None:
                status = "stale" if age > ttl else "fresh"
            else:
                status = "unbounded"
        ttl_fragment = f"ttl={ttl}d" if ttl is not None else "ttl=unknown"
        lines.append(
            f"- `{source.path.name}`: updated_at={source.metadata.get('updated_at', 'unknown')}, "
            f"{age_fragment}, {ttl_fragment}, status={status}"
        )
    next_review = today + timedelta(days=review_cadence_days)
    lines.append(f"- Suggested next soul review: {next_review.isoformat()}")
    return lines


def render_soul(owner_id: str, owner_dir: Path, today: date, review_cadence_days: int) -> str:
    sources = load_source_profiles(owner_dir)
    if not sources:
        raise SystemExit(f"No source profiles found in {owner_dir}")

    existing_path = owner_dir / "soul.md"
    manual_block = extract_manual_block(
        existing_path.read_text(encoding="utf-8", errors="ignore") if existing_path.exists() else None
    )
    entries = parse_changelog_entries(owner_dir / "CHANGELOG.md")

    profile_id = sources[0].metadata.get("profile_id", owner_id)
    owner_alias = sources[0].metadata.get("owner_alias", owner_id)
    source_updated = [
        parse_date(source.metadata.get("updated_at"))
        for source in sources
        if parse_date(source.metadata.get("updated_at")) is not None
    ]
    latest_updated = max(source_updated).isoformat() if source_updated else today.isoformat()

    stable_preferences = _section_items(
        sources,
        (
            "Communication Style",
            "Task Execution Rules",
            "Quality Bar",
            "Stable Preferences",
            "Decision Heuristics",
            "Tool Notes",
            "Tool-Specific Notes",
        ),
    )
    working_domains = _section_items(
        sources,
        (
            "Priority Domains",
            "Domain Workflows",
            "Environment Assumptions",
            "Personal Lexicon",
            "Known Good Prompts",
            "Image/Video Generator Preferences",
        ),
    )
    misalignments = _section_items(
        sources,
        (
            "Corrections History (Recent)",
            "Recurrent Misalignments",
        ),
    )
    recent_signals = _recent_signal_items(entries)

    if not stable_preferences:
        stable_preferences = ["[derived] No stable preferences extracted yet; fill profile.minimal.md or profile.core.md."]
    if not working_domains:
        working_domains = ["[derived] No domain workflow layer extracted yet."]
    if not misalignments:
        misalignments = ["[derived] No recurring misalignments or correction history captured yet."]
    if not recent_signals:
        recent_signals = ["[derived] No recent session log entries captured yet."]

    frontmatter = [
        "---",
        f'profile_id: "{profile_id}"',
        f'owner_alias: "{owner_alias}"',
        'format: "soul.v0.1"',
        f'generated_at: "{today.isoformat()}"',
        f'latest_source_update: "{latest_updated}"',
        f"review_cadence_days: {review_cadence_days}",
        'generated_by: "idctl refresh-soul"',
        'confidence_notes: "Derived summary from owner-maintained profile files and recent changelog entries. Manual corrections remain owner-editable."',
        "source_files:",
    ]
    for source in sources:
        frontmatter.append(f'  - "{source.path.name}"')
    frontmatter.extend(["---", ""])

    body: list[str] = [
        "# Soul Profile",
        "",
        "Compact working self-model for agents. This file is derived from the owner-maintained profile files and recent session history. It is not a substitute for the canonical source profiles.",
        "",
        "## Stable Preferences",
        "",
    ]
    body.extend(f"- {item}" for item in stable_preferences)
    body.extend(
        [
            "",
            "## Working Domains And Defaults",
            "",
        ]
    )
    body.extend(f"- {item}" for item in working_domains)
    body.extend(
        [
            "",
            "## Known Misalignments And Corrections",
            "",
        ]
    )
    body.extend(f"- {item}" for item in misalignments)
    body.extend(
        [
            "",
            "## Recent Operational Signals",
            "",
        ]
    )
    body.extend(f"- {item}" for item in recent_signals)
    body.extend(
        [
            "",
            "## Manual Corrections",
            "",
            "Owner-reviewed layer. Keep only durable, operationally useful corrections here.",
            "",
            MANUAL_START,
            manual_block.rstrip(),
            MANUAL_END,
            "",
            "## Freshness And Provenance",
            "",
            f"- Source owner directory: `{owner_dir}`",
            "- Source of truth: `profile.minimal.md`, `profile.core.md`, `profile.extended.md`, and `CHANGELOG.md`",
            "- Provenance tags:",
            "  - `[owner-stated/<source>]` = copied from owner-maintained profile files",
            "  - `[recent-session]` / `[recent-change]` / `[open-question]` = recent changelog-derived signals",
            "  - `[derived]` = generated filler when source coverage is missing",
            "",
        ]
    )
    body.extend(_freshness_lines(sources, today, review_cadence_days))
    body.append("")
    return "\n".join(frontmatter + body)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Refresh derived soul.md from ID source profiles")
    parser.add_argument("--owner-id", required=True, help="Owner id under profiles/<owner-id>/")
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root")
    parser.add_argument("--today", help="Override current date (YYYY-MM-DD)")
    parser.add_argument("--review-cadence-days", type=int, default=30, help="Suggested soul review cadence")
    parser.add_argument("--output", help="Override output path; defaults to profiles/<owner-id>/soul.md")
    parser.add_argument("--check", action="store_true", help="Fail if the derived soul file would change")
    parser.add_argument("--dry-run", action="store_true", help="Render without writing")
    parser.add_argument("--print-diff", action="store_true", help="Print unified diff when content changes")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Output format")
    return parser


def run_cli(argv: list[str]) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)
    today = parse_date(args.today) if args.today else date.today()
    if today is None:
        parser.error("--today must be YYYY-MM-DD")

    owner_dir = Path(args.profiles_root) / args.owner_id
    output_path = Path(args.output) if args.output else owner_dir / "soul.md"
    content = render_soul(args.owner_id, owner_dir, today, args.review_cadence_days)
    existed_before = output_path.exists()
    existing = output_path.read_text(encoding="utf-8", errors="ignore") if existed_before else ""
    changed = existing != content
    diff = ""
    if args.print_diff and changed:
        diff = "".join(
            difflib.unified_diff(
                existing.splitlines(keepends=True),
                content.splitlines(keepends=True),
                fromfile=str(output_path),
                tofile=str(output_path),
            )
        )

    if not (args.dry_run or args.check):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8", newline="\n")

    action = "created" if not existed_before and changed else "skipped"
    if existed_before and changed:
        action = "updated"
    elif not changed:
        action = "skipped"

    if args.format == "json":
        payload = {
            "owner_id": args.owner_id,
            "output": str(output_path),
            "changed": changed,
            "action": action,
            "check": bool(args.check),
            "dry_run": bool(args.dry_run),
            "diff": diff,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"{action}: {output_path}")
        if args.print_diff and diff:
            print(diff)

    return 1 if args.check and changed else 0
