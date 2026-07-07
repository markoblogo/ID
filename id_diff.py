"""Semantic profile diff for ID owner profiles."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from dataclasses import dataclass, asdict
from datetime import date, timedelta
from pathlib import Path


PROFILE_NAMES = ("profile.minimal.md", "profile.core.md", "profile.extended.md")
SECTION_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
SEMANTIC_GROUPS = {
    "current goals": ("goal", "priority", "blocked", "waiting", "project"),
    "interaction contract": ("communication", "style", "answer", "risk", "citation", "decision"),
    "preferences": ("preference", "preferred", "never do", "always do", "ask before"),
    "domain focus": ("domain", "interest", "tool-specific", "workflow"),
}


@dataclass(frozen=True)
class FileDiff:
    path: str
    added_sections: list[str]
    removed_sections: list[str]
    changed_sections: list[str]


@dataclass(frozen=True)
class StaleFinding:
    path: str
    updated_at: str
    age_days: int
    ttl_days: int


@dataclass(frozen=True)
class IdentityDiff:
    owner_id: str
    base: str
    target: str
    changed_files: list[FileDiff]
    semantic_changes: dict[str, list[str]]
    stale_assumptions: list[StaleFinding]


def parse_front_matter(text: str) -> dict[str, str]:
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


def parse_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current = "_frontmatter"
    sections[current] = []

    for line in text.splitlines():
        match = SECTION_RE.match(line)
        if match:
            current = match.group(2).strip()
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line.rstrip())

    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def run_git(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=cwd, check=False, capture_output=True, text=True)


def resolve_since_ref(since: str, cwd: Path, today: date) -> str:
    if since.endswith("d") and since[:-1].isdigit():
        target_date = today - timedelta(days=int(since[:-1]))
    else:
        try:
            target_date = date.fromisoformat(since)
        except ValueError as exc:
            raise ValueError("--since must be an ISO date or duration like 7d") from exc

    completed = run_git(["rev-list", "-1", f"--before={target_date.isoformat()} 23:59:59", "HEAD"], cwd)
    if completed.returncode != 0 or not completed.stdout.strip():
        raise RuntimeError(f"no git revision found before {target_date.isoformat()}")
    return completed.stdout.strip()


def read_at_ref(path: Path, ref: str, cwd: Path) -> str | None:
    abs_path = path if path.is_absolute() else cwd / path
    rel = abs_path.relative_to(cwd).as_posix()
    if ref == "WORKTREE":
        return abs_path.read_text(encoding="utf-8") if abs_path.exists() else None

    completed = run_git(["show", f"{ref}:{rel}"], cwd)
    if completed.returncode != 0:
        return None
    return completed.stdout


def list_profile_paths(owner_id: str, profiles_root: Path) -> list[Path]:
    owner_dir = profiles_root / owner_id
    return [owner_dir / name for name in PROFILE_NAMES]


def classify_section(section: str) -> str | None:
    lowered = section.lower()
    if "domain" in lowered or "interest" in lowered:
        return "domain focus"
    for group, needles in SEMANTIC_GROUPS.items():
        if any(needle in lowered for needle in needles):
            return group
    return None


def diff_text(path: Path, old_text: str | None, new_text: str | None) -> FileDiff | None:
    if old_text == new_text:
        return None

    old_sections = parse_sections(old_text or "")
    new_sections = parse_sections(new_text or "")
    old_keys = set(old_sections)
    new_keys = set(new_sections)
    common = old_keys & new_keys

    added = sorted(k for k in new_keys - old_keys if k != "_frontmatter")
    removed = sorted(k for k in old_keys - new_keys if k != "_frontmatter")
    changed = sorted(k for k in common if old_sections[k] != new_sections[k] and k != "_frontmatter")
    return FileDiff(str(path), added, removed, changed)


def find_stale(path: Path, text: str | None, today: date) -> StaleFinding | None:
    if text is None:
        return None
    meta = parse_front_matter(text)
    try:
        updated_at = date.fromisoformat(meta.get("updated_at", ""))
        ttl = int(meta.get("freshness_ttl_days", "0"))
    except ValueError:
        return None

    age = (today - updated_at).days
    if ttl > 0 and age > ttl:
        return StaleFinding(str(path), updated_at.isoformat(), age, ttl)
    return None


def build_identity_diff(
    owner_id: str,
    profiles_root: Path,
    base_ref: str,
    target_ref: str,
    today: date,
    cwd: Path,
) -> IdentityDiff:
    paths = list_profile_paths(owner_id, profiles_root)
    changed_files: list[FileDiff] = []
    semantic_changes = {group: [] for group in SEMANTIC_GROUPS}
    stale_assumptions: list[StaleFinding] = []

    for path in paths:
        old_text = read_at_ref(path, base_ref, cwd)
        new_text = read_at_ref(path, target_ref, cwd)
        diff = diff_text(path, old_text, new_text)
        if diff:
            changed_files.append(diff)
            for section in diff.added_sections + diff.removed_sections + diff.changed_sections:
                group = classify_section(section)
                if group:
                    semantic_changes[group].append(f"{path.name}: {section}")

        stale = find_stale(path, new_text, today)
        if stale:
            stale_assumptions.append(stale)

    semantic_changes = {key: sorted(values) for key, values in semantic_changes.items() if values}
    return IdentityDiff(owner_id, base_ref, target_ref, changed_files, semantic_changes, stale_assumptions)


def render_text(diff: IdentityDiff) -> str:
    lines = [
        "Identity Diff",
        f"Owner: {diff.owner_id}",
        f"Base: {diff.base}",
        f"Target: {diff.target}",
        "",
    ]

    if not diff.changed_files:
        lines.append("Changed files: none")
    else:
        lines.append("Changed files:")
        for item in diff.changed_files:
            lines.append(f"- {item.path}")
            for label, values in (
                ("added", item.added_sections),
                ("removed", item.removed_sections),
                ("changed", item.changed_sections),
            ):
                if values:
                    lines.append(f"  {label}: {', '.join(values)}")

    lines.append("")
    if diff.semantic_changes:
        lines.append("Semantic changes:")
        for group, values in diff.semantic_changes.items():
            lines.append(f"- {group}")
            for value in values:
                lines.append(f"  - {value}")
    else:
        lines.append("Semantic changes: none detected")

    lines.append("")
    if diff.stale_assumptions:
        lines.append("Stale assumptions:")
        for stale in diff.stale_assumptions:
            lines.append(
                f"- {stale.path}: updated_at={stale.updated_at}, age={stale.age_days}d, ttl={stale.ttl_days}d"
            )
    else:
        lines.append("Stale assumptions: none")

    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Show semantic changes in an owner ID profile.")
    parser.add_argument("--owner-id", required=True, help="Owner profile id under profiles/<owner-id>")
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root directory")
    parser.add_argument("--from", dest="base_ref", help="Base git ref")
    parser.add_argument("--to", dest="target_ref", default="WORKTREE", help="Target git ref or WORKTREE")
    parser.add_argument("--since", help="Base revision by ISO date or duration like 7d")
    parser.add_argument("--today", help="Override current date (YYYY-MM-DD)")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    return parser


def run_cli(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    today = date.today()
    if args.today:
        try:
            today = date.fromisoformat(args.today)
        except ValueError:
            print("ERROR: --today must be YYYY-MM-DD")
            return 2

    cwd = Path.cwd()
    profiles_root = Path(args.profiles_root)
    try:
        base_ref = args.base_ref or (resolve_since_ref(args.since, cwd, today) if args.since else "HEAD")
    except (RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 2

    diff = build_identity_diff(args.owner_id, profiles_root, base_ref, args.target_ref, today, cwd)
    if args.json:
        print(json.dumps(asdict(diff), indent=2, ensure_ascii=False))
    else:
        print(render_text(diff))
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli())
