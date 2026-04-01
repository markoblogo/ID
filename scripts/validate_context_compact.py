#!/usr/bin/env python3
"""Validate compact portable context JSON using stdlib checks aligned to schema."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any


SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
TRUST_LEVELS = {"trusted", "provisional", "archival"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate compact portable context JSON")
    parser.add_argument("--owner-id", help="Owner id used when --input is omitted")
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root")
    parser.add_argument("--input", help="Path to context.compact.json")
    parser.add_argument(
        "--schema",
        default="schemas/context-compact-v0.schema.json",
        help="Schema path",
    )
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8", errors="ignore"))


def validate_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def validate_string_array(value: Any, field_name: str, errors: list[str]) -> None:
    if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
        errors.append(f"{field_name} must be array of strings")


def find_errors(doc: Any) -> list[str]:
    errors: list[str] = []

    if not isinstance(doc, dict):
        return ["root must be an object"]

    required = [
        "context_version",
        "owner_id",
        "updated_at",
        "freshness_ttl_days",
        "trust_level",
        "communication",
        "rules",
        "quality_bar",
        "priority_domains",
        "tool_notes",
        "loss_notes",
    ]
    for key in required:
        if key not in doc:
            errors.append(f"missing required field: {key}")

    value = doc.get("context_version")
    if value is not None and (not isinstance(value, str) or not SEMVER_RE.match(value)):
        errors.append("context_version must be semver string (x.y.z)")

    value = doc.get("owner_id")
    if value is not None and (not isinstance(value, str) or not value.strip()):
        errors.append("owner_id must be non-empty string")

    value = doc.get("updated_at")
    if value is not None and (not isinstance(value, str) or not validate_date(value)):
        errors.append("updated_at must be date string YYYY-MM-DD")

    value = doc.get("freshness_ttl_days")
    if value is not None and (not isinstance(value, int) or value < 1):
        errors.append("freshness_ttl_days must be integer >= 1")

    value = doc.get("trust_level")
    if value is not None and value not in TRUST_LEVELS:
        errors.append("trust_level must be one of: trusted, provisional, archival")

    for key in ("communication", "quality_bar", "priority_domains", "tool_notes", "loss_notes"):
        if key in doc:
            validate_string_array(doc[key], key, errors)

    if "rules" in doc:
        rules = doc["rules"]
        if not isinstance(rules, dict):
            errors.append("rules must be object")
        else:
            required_rules = {"always_do", "never_do", "ask_before", "default_assumptions"}
            for key in required_rules:
                if key not in rules:
                    errors.append(f"rules missing key: {key}")
                else:
                    validate_string_array(rules[key], f"rules.{key}", errors)
            for key in rules.keys():
                if key not in required_rules:
                    errors.append(f"rules has unsupported key: {key}")

    return errors


def main() -> int:
    args = parse_args()
    _ = load_json(Path(args.schema))

    if args.input:
        input_path = Path(args.input)
    elif args.owner_id:
        input_path = Path(args.profiles_root) / args.owner_id / "context.compact.json"
    else:
        print("ERROR: provide --input or --owner-id")
        return 1

    if not input_path.exists():
        print(f"ERROR: missing input file: {input_path}")
        return 1

    doc = load_json(input_path)
    errors = find_errors(doc)
    if errors:
        print(f"INVALID: {input_path}")
        for err in errors:
            print(f"- {err}")
        return 1

    print(f"VALID: {input_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
