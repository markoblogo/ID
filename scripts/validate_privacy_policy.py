#!/usr/bin/env python3
"""Validate machine-readable privacy policy JSON using stdlib checks aligned to schema."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path
from typing import Any

SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
ACCESS_LEVELS = {"always_share", "local_only", "task_class_scoped"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate machine-readable privacy policy JSON")
    parser.add_argument("--owner-id", help="Owner id used when --input is omitted")
    parser.add_argument("--profiles-root", default="profiles", help="Profiles root")
    parser.add_argument("--input", help="Path to privacy-policy.v1.json")
    parser.add_argument(
        "--schema",
        default="schemas/privacy-policy-v1.schema.json",
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
    if not isinstance(value, list) or not value or not all(isinstance(x, str) and x.strip() for x in value):
        errors.append(f"{field_name} must be non-empty array of non-empty strings")


def find_errors(doc: Any) -> list[str]:
    errors: list[str] = []

    if not isinstance(doc, dict):
        return ["root must be an object"]

    required = ["policy_version", "owner_id", "updated_at", "default_access", "task_classes", "rules"]
    for key in required:
        if key not in doc:
            errors.append(f"missing required field: {key}")

    value = doc.get("policy_version")
    if value is not None and (not isinstance(value, str) or not SEMVER_RE.match(value)):
        errors.append("policy_version must be semver string (x.y.z)")

    value = doc.get("owner_id")
    if value is not None and (not isinstance(value, str) or not value.strip()):
        errors.append("owner_id must be non-empty string")

    value = doc.get("updated_at")
    if value is not None and (not isinstance(value, str) or not validate_date(value)):
        errors.append("updated_at must be date string YYYY-MM-DD")

    value = doc.get("default_access")
    if value is not None and value not in ACCESS_LEVELS:
        errors.append("default_access must be one of: always_share, local_only, task_class_scoped")

    task_classes = doc.get("task_classes")
    if task_classes is not None:
        validate_string_array(task_classes, "task_classes", errors)
        known_task_classes = set(task_classes) if isinstance(task_classes, list) else set()
    else:
        known_task_classes = set()

    rules = doc.get("rules")
    if rules is not None and not isinstance(rules, list):
        errors.append("rules must be array of objects")
    elif isinstance(rules, list):
        seen_paths: set[str] = set()
        for index, rule in enumerate(rules):
            prefix = f"rules[{index}]"
            if not isinstance(rule, dict):
                errors.append(f"{prefix} must be object")
                continue
            for key in ("field_path", "access", "rationale"):
                if key not in rule:
                    errors.append(f"{prefix} missing key: {key}")
            field_path = rule.get("field_path")
            if field_path is not None:
                if not isinstance(field_path, str) or not field_path.strip():
                    errors.append(f"{prefix}.field_path must be non-empty string")
                elif field_path in seen_paths:
                    errors.append(f"duplicate field_path: {field_path}")
                else:
                    seen_paths.add(field_path)
            access = rule.get("access")
            if access is not None and access not in ACCESS_LEVELS:
                errors.append(f"{prefix}.access must be one of: always_share, local_only, task_class_scoped")
            rationale = rule.get("rationale")
            if rationale is not None and (not isinstance(rationale, str) or not rationale.strip()):
                errors.append(f"{prefix}.rationale must be non-empty string")
            allowed = rule.get("allowed_task_classes")
            if access == "task_class_scoped":
                validate_string_array(allowed, f"{prefix}.allowed_task_classes", errors)
                if isinstance(allowed, list):
                    unknown = [item for item in allowed if item not in known_task_classes]
                    for item in unknown:
                        errors.append(f"{prefix}.allowed_task_classes has unknown task class: {item}")
            elif allowed is not None:
                errors.append(f"{prefix}.allowed_task_classes only allowed when access=task_class_scoped")

    notes = doc.get("notes")
    if notes is not None and (not isinstance(notes, list) or not all(isinstance(item, str) for item in notes)):
        errors.append("notes must be array of strings")

    return errors


def main() -> int:
    args = parse_args()
    _ = load_json(Path(args.schema))

    if args.input:
        input_path = Path(args.input)
    elif args.owner_id:
        input_path = Path(args.profiles_root) / args.owner_id / "privacy-policy.v1.json"
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
