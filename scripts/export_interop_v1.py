#!/usr/bin/env python3
"""Export markdown profiles to interop v1 JSON envelope with typed mapping."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


HEADING_RE = re.compile(r"^##\s+(.+)$")
TOP_BULLET_RE = re.compile(r"^-\s+(.+)$")
NESTED_BULLET_RE = re.compile(r"^\s{2,}-\s+(.+)$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export profile to interop v1 JSON")
    parser.add_argument("--owner-id", required=True, help="Owner id, e.g. markoblogo")
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root")
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
    heading = re.sub(r"^[0-9]+\.\s*", "", heading.strip())
    return heading.lower()


def parse_sections(body_lines: list[str]) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current = "_root"
    sections[current] = []

    for line in body_lines:
        m = HEADING_RE.match(line)
        if m:
            current = normalize_heading(m.group(1))
            sections.setdefault(current, [])
            continue
        sections.setdefault(current, []).append(line)

    return sections


def extract_bullets(lines: list[str]) -> list[str]:
    bullets: list[str] = []
    for line in lines:
        m = TOP_BULLET_RE.match(line.strip())
        if m:
            bullets.append(m.group(1).strip())
    return bullets


def extract_rule_blocks(lines: list[str]) -> dict[str, list[str]]:
    blocks = {
        "always_do": [],
        "never_do": [],
        "ask_before": [],
        "default_assumptions": [],
    }

    current_key = None
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


def map_core_profile(meta: dict[str, str], sections: dict[str, list[str]]) -> dict:
    out = {
        "metadata": meta,
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
        "extensions": {},
    }

    for heading, lines in sections.items():
        if heading == "_root":
            continue
        if "communication" in heading:
            out["communication"] = extract_bullets(lines)
        elif "task execution rules" in heading:
            out["rules"] = extract_rule_blocks(lines)
        elif "quality bar" in heading:
            out["quality_bar"] = extract_bullets(lines)
        elif "priority domains" in heading:
            out["priority_domains"] = extract_bullets(lines)
        elif "tool-specific notes" in heading:
            out["tool_notes"] = extract_bullets(lines)
        else:
            out["extensions"][heading] = extract_bullets(lines)

    return out


def map_extended_profile(meta: dict[str, str], sections: dict[str, list[str]]) -> dict:
    out = {
        "metadata": meta,
        "stable_preferences": [],
        "domain_workflows": {},
        "misalignments": [],
        "lexicon": [],
        "environment_assumptions": [],
        "decision_heuristics": [],
        "known_good_prompts": [],
        "extensions": {},
    }

    for heading, lines in sections.items():
        if heading == "_root":
            continue
        bullets = extract_bullets(lines)
        if "stable preferences" in heading:
            out["stable_preferences"] = bullets
        elif "domain workflows" in heading:
            out["domain_workflows"][heading] = bullets
        elif "recurrent misalignments" in heading:
            out["misalignments"] = bullets
        elif "personal lexicon" in heading:
            out["lexicon"] = bullets
        elif "environment assumptions" in heading:
            out["environment_assumptions"] = bullets
        elif "decision heuristics" in heading:
            out["decision_heuristics"] = bullets
        elif "known good prompts" in heading:
            out["known_good_prompts"] = bullets
        else:
            out["extensions"][heading] = bullets

    return out


def parse_profile(path: Path, profile_type: str) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    meta, body = parse_front_matter(text)
    sections = parse_sections(body)

    if profile_type == "core":
        return map_core_profile(meta, sections)
    return map_extended_profile(meta, sections)


def main() -> int:
    args = parse_args()
    owner_dir = Path(args.profiles_root) / args.owner_id

    core_path = owner_dir / "profile.core.md"
    ext_path = owner_dir / "profile.extended.md"
    out_path = owner_dir / "interop.v1.json"

    if not core_path.exists() or not ext_path.exists():
        print("ERROR: missing profile.core.md or profile.extended.md")
        return 1

    payload = {
        "interop_version": "1.0.0",
        "owner_id": args.owner_id,
        "generated_at": date.today().isoformat(),
        "profiles": {
            "core": parse_profile(core_path, "core"),
            "extended": parse_profile(ext_path, "extended"),
        },
    }

    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
