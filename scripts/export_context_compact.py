#!/usr/bin/env python3
"""Export a compact portable context payload from the core profile."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HEADING_RE = re.compile(r"^##\s+(.+)$")
TOP_BULLET_RE = re.compile(r"^-\s+(.+)$")
NESTED_BULLET_RE = re.compile(r"^\s{2,}-\s+(.+)$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export compact portable context JSON")
    parser.add_argument("--owner-id", required=True, help="Owner id, e.g. markoblogo")
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root")
    parser.add_argument(
        "--output",
        help="Explicit output path (default: profiles/<owner>/context.compact.json)",
    )
    return parser.parse_args()


def parse_front_matter(text: str) -> tuple[dict[str, str], list[str]]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}, lines

    meta: dict[str, str] = {}
    i = 1
    while i < len(lines):
        line = lines[i]
        if line.strip() == "---":
            return meta, lines[i + 1 :]
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip().strip('"')
        i += 1

    return meta, lines


def normalize_heading(heading: str) -> str:
    return re.sub(r"^[0-9]+\.\s*", "", heading.strip()).lower()


def parse_sections(body_lines: list[str]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {"_root": []}
    current = "_root"

    for line in body_lines:
        match = HEADING_RE.match(line)
        if match:
            current = normalize_heading(match.group(1))
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)

    return sections


def extract_bullets(lines: list[str]) -> list[str]:
    bullets: list[str] = []
    for line in lines:
        match = TOP_BULLET_RE.match(line.strip())
        if match:
            bullets.append(match.group(1).strip())
    return bullets


def extract_rule_blocks(lines: list[str]) -> dict[str, list[str]]:
    blocks = {
        "always_do": [],
        "never_do": [],
        "ask_before": [],
        "default_assumptions": [],
    }

    current_key: str | None = None
    for raw in lines:
        line = raw.rstrip()
        top = TOP_BULLET_RE.match(line.strip())
        nested = NESTED_BULLET_RE.match(line)

        if top:
            text = top.group(1).strip().lower()
            if text.startswith("always do"):
                current_key = "always_do"
                continue
            if text.startswith("never do"):
                current_key = "never_do"
                continue
            if text.startswith("ask before"):
                current_key = "ask_before"
                continue
            if text.startswith("default assumptions"):
                current_key = "default_assumptions"
                continue

        if nested and current_key:
            blocks[current_key].append(nested.group(1).strip())

    return blocks


def compact_payload(owner_id: str, meta: dict[str, str], sections: dict[str, list[str]]) -> dict:
    payload = {
        "context_version": "0.1.0",
        "owner_id": meta.get("owner_alias", "").strip() or owner_id,
        "updated_at": meta.get("updated_at", ""),
        "freshness_ttl_days": int(meta.get("freshness_ttl_days", "14")),
        "trust_level": meta.get("trust_level", "provisional"),
        "communication": [],
        "rules": {
            "always_do": [],
            "never_do": [],
            "ask_before": [],
            "default_assumptions": [],
        },
        "quality_bar": [],
        "priority_domains": [],
        "tool_notes": [],
        "loss_notes": [
            "Extended workflows omitted",
            "Historical corrections omitted",
            "Use full profile or interop.v1.json for richer context",
        ],
    }

    for heading, lines in sections.items():
        if heading == "_root":
            continue
        if "communication" in heading:
            payload["communication"] = extract_bullets(lines)
        elif "task execution rules" in heading:
            payload["rules"] = extract_rule_blocks(lines)
        elif "quality bar" in heading:
            payload["quality_bar"] = extract_bullets(lines)
        elif "priority domains" in heading:
            payload["priority_domains"] = extract_bullets(lines)
        elif "tool-specific notes" in heading or "tool notes" in heading:
            payload["tool_notes"] = extract_bullets(lines)

    return payload


def main() -> int:
    args = parse_args()
    owner_dir = Path(args.profiles_root) / args.owner_id
    core_path = owner_dir / "profile.core.md"
    out_path = Path(args.output) if args.output else owner_dir / "context.compact.json"

    if not core_path.exists():
        print("ERROR: missing profile.core.md")
        return 1

    text = core_path.read_text(encoding="utf-8", errors="ignore")
    meta, body = parse_front_matter(text)
    payload = compact_payload(args.owner_id, meta, parse_sections(body))

    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
