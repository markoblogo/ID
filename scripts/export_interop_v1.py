#!/usr/bin/env python3
"""Export markdown profiles to interop v1 JSON envelope (MVP parser)."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export profile to interop v1 JSON")
    parser.add_argument("--owner-id", required=True, help="Owner id, e.g. markoblogo")
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root")
    return parser.parse_args()


def parse_front_matter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        return {}

    meta: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    return meta


def extract_sections(text: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    current = "_root"
    for raw in text.splitlines():
        line = raw.rstrip()
        if re.match(r"^##\s+", line):
            current = re.sub(r"^##\s+", "", line).strip()
            sections.setdefault(current, [])
            continue
        if line.startswith("- "):
            sections.setdefault(current, []).append(line[2:].strip())
    return sections


def parse_profile(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return {
        "metadata": parse_front_matter(text),
        "sections": extract_sections(text),
    }


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
            "core": parse_profile(core_path),
            "extended": parse_profile(ext_path),
        },
    }

    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
