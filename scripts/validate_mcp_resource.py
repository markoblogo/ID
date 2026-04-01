#!/usr/bin/env python3
"""Validate a policy-aware MCP resource payload derived from ID context."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from validate_context_compact import find_errors as find_context_errors


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def find_errors(document: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["Document must be a JSON object"]

    required = {
        "resource_version",
        "owner_id",
        "uri",
        "name",
        "description",
        "mime_type",
        "contents",
        "policy",
    }
    for field in sorted(required):
        if field not in document:
            errors.append(f"Missing required field: {field}")
    if errors:
        return errors

    if not _is_non_empty_string(document["resource_version"]):
        errors.append("resource_version must be a non-empty string")
    if not _is_non_empty_string(document["owner_id"]):
        errors.append("owner_id must be a non-empty string")
    if not _is_non_empty_string(document["name"]):
        errors.append("name must be a non-empty string")
    if not _is_non_empty_string(document["description"]):
        errors.append("description must be a non-empty string")

    uri = document["uri"]
    if not _is_non_empty_string(uri) or not uri.startswith("id://") or not uri.endswith("/context.compact"):
        errors.append("uri must look like id://<owner-id>/context.compact")

    if document["mime_type"] != "application/json":
        errors.append("mime_type must be application/json")

    for error in find_context_errors(document["contents"]):
        errors.append(f"contents.{error}")

    policy = document["policy"]
    if not isinstance(policy, dict):
        errors.append("policy must be an object")
        return errors

    expected_fields = {"applied", "task_class", "source"}
    for field in sorted(expected_fields - set(policy.keys())):
        errors.append(f"policy missing required field: {field}")
    for field in sorted(set(policy.keys()) - expected_fields):
        errors.append(f"policy contains unexpected field: {field}")

    if "applied" in policy and not isinstance(policy["applied"], bool):
        errors.append("policy.applied must be a boolean")
    if "task_class" in policy and policy["task_class"] is not None and not _is_non_empty_string(policy["task_class"]):
        errors.append("policy.task_class must be null or a non-empty string")
    if "source" in policy and policy["source"] is not None and not _is_non_empty_string(policy["source"]):
        errors.append("policy.source must be null or a non-empty string")
    if policy.get("applied") and policy.get("source") is None:
        errors.append("policy.source must be present when policy.applied is true")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner-id", help="Profile owner id under profiles/<owner-id>/")
    parser.add_argument("--input", type=Path, help="Path to an MCP resource JSON file")
    parser.add_argument("--profiles-root", type=Path, default=Path("profiles"))
    args = parser.parse_args()

    if bool(args.owner_id) == bool(args.input):
        parser.error("Provide exactly one of --owner-id or --input")

    input_path = (
        args.input
        if args.input is not None
        else args.profiles_root / args.owner_id / "mcp.context.resource.json"
    )

    document = load_json(input_path)
    errors = find_errors(document)
    if errors:
        print(f"INVALID: {input_path}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"VALID: {input_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
