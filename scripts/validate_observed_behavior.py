#!/usr/bin/env python3
"""Validate structured observed-behavior evidence notes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any


DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CONFIDENCE = {"low", "medium", "high"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_string_list(value: Any, field: str, errors: list[str], min_items: int = 1) -> None:
    if not isinstance(value, list):
        errors.append(f"{field} must be an array")
        return
    if len(value) < min_items:
        errors.append(f"{field} must contain at least {min_items} item(s)")
        return
    for index, item in enumerate(value):
        if not _is_non_empty_string(item):
            errors.append(f"{field}[{index}] must be a non-empty string")


def parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def find_errors(document: Any, today: date | None = None, max_age_days: int | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(document, dict):
        return ["Document must be a JSON object"]

    required = {
        "schema_version",
        "tool_family",
        "confidence",
        "observed_at",
        "summary",
        "onboarding_mode",
        "best_artifacts",
        "degradation_patterns",
        "evidence",
    }
    for field in sorted(required):
        if field not in document:
            errors.append(f"Missing required field: {field}")
    if errors:
        return errors

    if document["schema_version"] != "1.0.0":
        errors.append("schema_version must be 1.0.0")
    if not _is_non_empty_string(document["tool_family"]):
        errors.append("tool_family must be a non-empty string")
    if document["confidence"] not in CONFIDENCE:
        errors.append("confidence must be one of: low, medium, high")
    if not _is_non_empty_string(document["summary"]):
        errors.append("summary must be a non-empty string")
    if not _is_non_empty_string(document["observed_at"]) or not DATE_RE.match(document["observed_at"]):
        errors.append("observed_at must be YYYY-MM-DD")
    elif today is not None and max_age_days is not None:
        observed_at = parse_date(document["observed_at"])
        if observed_at is None:
            errors.append("observed_at must be YYYY-MM-DD")
        else:
            age = (today - observed_at).days
            if age > max_age_days:
                errors.append(
                    f"observed_at is stale: {document['observed_at']} is {age} days old > max_age_days={max_age_days}"
                )

    _validate_string_list(document["onboarding_mode"], "onboarding_mode", errors)
    _validate_string_list(document["best_artifacts"], "best_artifacts", errors)
    _validate_string_list(document["degradation_patterns"], "degradation_patterns", errors)

    evidence = document["evidence"]
    if not isinstance(evidence, dict):
        errors.append("evidence must be an object")
        return errors

    evidence_required = {"basis", "artifact_refs", "run_refs", "scope_limits"}
    for field in sorted(evidence_required):
        if field not in evidence:
            errors.append(f"evidence missing required field: {field}")
    extra = set(evidence.keys()) - evidence_required
    for field in sorted(extra):
        errors.append(f"evidence contains unexpected field: {field}")
    if any(error.startswith("evidence missing required field:") or error.startswith("evidence contains unexpected field:") for error in errors):
        return errors

    _validate_string_list(evidence["basis"], "evidence.basis", errors)
    _validate_string_list(evidence["artifact_refs"], "evidence.artifact_refs", errors, min_items=0)
    _validate_string_list(evidence["run_refs"], "evidence.run_refs", errors, min_items=0)
    _validate_string_list(evidence["scope_limits"], "evidence.scope_limits", errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence-root", type=Path, default=Path("evidence/observed-behavior"))
    parser.add_argument("--input", type=Path, help="Validate a single evidence note")
    parser.add_argument("--today", help="Override current date (YYYY-MM-DD)")
    parser.add_argument("--max-age-days", type=int, default=180, help="Maximum allowed evidence age in days")
    args = parser.parse_args()

    today = parse_date(args.today) if args.today else date.today()
    if today is None:
        print("ERROR: --today must be YYYY-MM-DD")
        return 2

    paths = [args.input] if args.input else sorted(args.evidence_root.glob("*.json"))
    if not paths:
        print("WARN: no observed behavior evidence notes found")
        return 0

    failures = 0
    for path in paths:
        errors = find_errors(load_json(path), today=today, max_age_days=args.max_age_days)
        if errors:
            print(f"INVALID: {path}")
            for error in errors:
                print(f"- {error}")
            failures += 1
        else:
            print(f"VALID: {path}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
