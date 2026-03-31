#!/usr/bin/env python3
"""MVP profile extractor for ID Protocol.

Reads normalized text/json sources and produces:
- profiles/<owner-id>/draft.from-exports.md
- profiles/<owner-id>/conflicts.from-exports.md
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable

SUPPORTED_EXTENSIONS = {".txt", ".md", ".json"}
MAX_SNIPPETS_PER_BUCKET = 20


@dataclass
class Snippet:
    text: str
    source: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract profile draft from normalized exports")
    parser.add_argument("--owner-id", required=True, help="Profile owner id, e.g. markoblogo")
    parser.add_argument(
        "--input-dir",
        default="data/normalized",
        help="Directory with normalized exports (default: data/normalized)",
    )
    parser.add_argument(
        "--profiles-dir",
        default="profiles",
        help="Profiles root directory (default: profiles)",
    )
    return parser.parse_args()


def iter_files(input_dir: Path) -> Iterable[Path]:
    if not input_dir.exists():
        return []
    return sorted(
        p for p in input_dir.rglob("*") if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def flatten_json(value) -> Iterable[str]:
    if isinstance(value, dict):
        for v in value.values():
            yield from flatten_json(v)
    elif isinstance(value, list):
        for item in value:
            yield from flatten_json(item)
    elif isinstance(value, str):
        stripped = value.strip()
        if stripped:
            yield stripped


def read_text(path: Path) -> str:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() != ".json":
        return raw

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return raw

    return "\n".join(flatten_json(payload))


def split_to_snippets(text: str) -> list[str]:
    lines = []
    for chunk in text.splitlines():
        line = re.sub(r"\s+", " ", chunk).strip()
        if len(line) < 20:
            continue
        lines.append(line)

    snippets: list[str] = []
    for line in lines:
        parts = re.split(r"(?<=[.!?])\s+", line)
        for part in parts:
            part = part.strip()
            if 20 <= len(part) <= 280:
                snippets.append(part)
    return snippets


def classify(snippet: str) -> set[str]:
    s = snippet.lower()
    buckets = set()

    if any(k in s for k in ["tone", "тон", "style", "стиль", "формат", "format", "кратк", "подроб", "language", "язык"]):
        buckets.add("communication")

    if any(k in s for k in ["always", "всегда", "обязательно", "должен", "must"]):
        buckets.add("rules_always")

    if any(k in s for k in ["never", "никогда", "нельзя", "do not", "don't", "не "]):
        buckets.add("rules_never")

    if any(k in s for k in ["project", "проект", "направлен", "domain", "интерес", "focus", "приоритет"]):
        buckets.add("priority_domains")

    if any(k in s for k in ["problem", "проблем", "не понима", "сложно", "ошиб", "misalign", "conflict"]):
        buckets.add("misalignments")

    if any(k in s for k in ["quality", "качество", "готово", "done", "результат", "критер"]):
        buckets.add("quality_bar")

    return buckets


def dedupe(snippets: list[Snippet]) -> list[Snippet]:
    seen = set()
    out: list[Snippet] = []
    for item in snippets:
        key = item.text.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def build_conflicts(buckets: dict[str, list[Snippet]]) -> list[str]:
    conflicts = []

    comm_text = " ".join(s.text.lower() for s in buckets.get("communication", []))
    short_pref = any(k in comm_text for k in ["кратко", "brief", "short"])
    deep_pref = any(k in comm_text for k in ["подроб", "deep", "detailed"])
    if short_pref and deep_pref:
        conflicts.append("Communication detail level: both short and deep preferences detected.")

    rules_always = len(buckets.get("rules_always", []))
    rules_never = len(buckets.get("rules_never", []))
    if rules_always == 0 and rules_never == 0:
        conflicts.append("No explicit behavioral rules detected (always/never).")

    return conflicts


def render_section(title: str, items: list[Snippet]) -> str:
    if not items:
        return f"## {title}\n\n- [uncertain] no direct evidence extracted\n"

    lines = [f"## {title}", ""]
    for s in items[:MAX_SNIPPETS_PER_BUCKET]:
        lines.append(f"- {s.text}")
        lines.append(f"  - source: `{s.source}`")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    input_dir = Path(args.input_dir)
    profiles_dir = Path(args.profiles_dir)
    owner_dir = profiles_dir / args.owner_id
    owner_dir.mkdir(parents=True, exist_ok=True)

    files = list(iter_files(input_dir))
    buckets: dict[str, list[Snippet]] = {
        "communication": [],
        "rules_always": [],
        "rules_never": [],
        "quality_bar": [],
        "priority_domains": [],
        "misalignments": [],
    }

    for path in files:
        text = read_text(path)
        for snippet in split_to_snippets(text):
            bucket_names = classify(snippet)
            if not bucket_names:
                continue
            src = str(path)
            item = Snippet(text=snippet, source=src)
            for bucket_name in bucket_names:
                buckets[bucket_name].append(item)

    for key, values in list(buckets.items()):
        buckets[key] = dedupe(values)

    today = date.today().isoformat()
    draft_path = owner_dir / "draft.from-exports.md"
    conflict_path = owner_dir / "conflicts.from-exports.md"

    draft_parts = [
        "# Draft Profile From Exports (MVP)",
        "",
        f"- owner_id: `{args.owner_id}`",
        f"- generated_at: `{today}`",
        f"- source_root: `{input_dir}`",
        f"- files_scanned: `{len(files)}`",
        "",
        "This file is an extraction candidate. Review manually before merging into canonical profile files.",
        "",
        render_section("Communication Signals", buckets["communication"]),
        render_section("Always Rules Signals", buckets["rules_always"]),
        render_section("Never Rules Signals", buckets["rules_never"]),
        render_section("Quality Bar Signals", buckets["quality_bar"]),
        render_section("Priority Domains Signals", buckets["priority_domains"]),
        render_section("Misalignment Signals", buckets["misalignments"]),
    ]
    draft_path.write_text("\n".join(draft_parts), encoding="utf-8")

    conflicts = build_conflicts(buckets)
    conflict_parts = [
        "# Extracted Conflicts and Gaps (MVP)",
        "",
        f"- owner_id: `{args.owner_id}`",
        f"- generated_at: `{today}`",
        "",
    ]
    if conflicts:
        conflict_parts.extend(f"- {c}" for c in conflicts)
    else:
        conflict_parts.append("- No high-level conflicts detected by simple heuristics.")

    conflict_parts.extend(
        [
            "",
            "## Notes",
            "",
            "- Heuristics are intentionally simple; false positives/negatives are expected.",
            "- Treat this file as review checklist, not as final truth.",
        ]
    )
    conflict_path.write_text("\n".join(conflict_parts), encoding="utf-8")

    print(f"Generated: {draft_path}")
    print(f"Generated: {conflict_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
