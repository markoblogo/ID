#!/usr/bin/env python3
"""Validate interop v1 JSON using stdlib checks aligned to schema."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate interop v1 JSON")
    parser.add_argument("--owner-id", help="Owner id used when --input is omitted")
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root")
    parser.add_argument("--input", help="Path to interop.v1.json")
    parser.add_argument("--schema", default="schemas/interop-v1.schema.json", help="Schema path")
    return parser.parse_args()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8", errors="ignore"))


def validate_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def find_errors(doc: Any) -> list[str]:
    errors: list[str] = []

    if not isinstance(doc, dict):
        return ["root must be an object"]

    required = ["interop_version", "owner_id", "generated_at", "profiles"]
    for key in required:
        if key not in doc:
            errors.append(f"missing required field: {key}")

    if "interop_version" in doc:
        value = doc["interop_version"]
        if not isinstance(value, str) or not SEMVER_RE.match(value):
            errors.append("interop_version must be semver string (x.y.z)")

    if "owner_id" in doc:
        value = doc["owner_id"]
        if not isinstance(value, str) or not value.strip():
            errors.append("owner_id must be non-empty string")

    if "generated_at" in doc:
        value = doc["generated_at"]
        if not isinstance(value, str) or not validate_date(value):
            errors.append("generated_at must be date string YYYY-MM-DD")

    if "profiles" in doc:
        value = doc["profiles"]
        if not isinstance(value, dict):
            errors.append("profiles must be object")
        else:
            allowed = {"core", "extended"}
            for k in value.keys():
                if k not in allowed:
                    errors.append(f"profiles has unsupported key: {k}")
            for k in ("core", "extended"):
                if k not in value:
                    errors.append(f"profiles missing key: {k}")
                elif not isinstance(value[k], dict):
                    errors.append(f"profiles.{k} must be object")

    return errors


def main() -> int:
    args = parse_args()
    _ = load_json(Path(args.schema))

    if args.input:
        input_path = Path(args.input)
    elif args.owner_id:
        input_path = Path(args.profiles_root) / args.owner_id / "interop.v1.json"
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
