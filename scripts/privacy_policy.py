"""Shared helpers for machine-readable privacy-policy enforcement."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8", errors="ignore"))


def load_policy(profiles_root: Path, owner_id: str) -> dict | None:
    path = profiles_root / owner_id / "privacy-policy.v1.json"
    if not path.exists():
        return None
    return normalize_policy(load_json(path), owner_id)


def normalize_policy(doc: Any, owner_id: str) -> dict:
    """Read the legacy list format without changing the owner's source file."""
    from validate_privacy_policy import find_errors
    legacy_keys = {"always_share", "local_only", "task_class_scoped"}
    if isinstance(doc, dict) and legacy_keys.intersection(doc):
        allowed = legacy_keys | {"policy_version", "owner_id", "updated_at", "notes"}
        if set(doc) - allowed or not legacy_keys.issubset(doc):
            raise ValueError("mixed or incomplete legacy privacy policy; review its access rules")
        if doc.get("policy_version") != "1.0.0":
            raise ValueError("unsupported legacy privacy policy version")
        rules = []
        seen = set()
        classes = set()
        def add(field, access, scoped=None):
            if not isinstance(field, str) or not field.strip() or field in seen:
                raise ValueError("legacy policy has an invalid or conflicting field path")
            seen.add(field)
            rule = {"field_path": field, "access": access, "rationale": "Preserved from legacy privacy policy"}
            if scoped is not None:
                if not isinstance(scoped, list) or not scoped or not all(isinstance(x, str) and x.strip() for x in scoped):
                    raise ValueError("legacy scoped rules require field-path to non-empty task-class list mappings")
                rule["allowed_task_classes"] = sorted(set(scoped))
                classes.update(scoped)
            rules.append(rule)
        for access in ("always_share", "local_only"):
            fields = doc[access]
            if not isinstance(fields, list):
                raise ValueError(f"legacy {access} must be a list of field paths")
            for field in fields:
                add(field, access)
        scoped = doc["task_class_scoped"]
        if not isinstance(scoped, dict):
            raise ValueError("legacy task_class_scoped must map field paths to task-class lists")
        for field, task_classes in scoped.items():
            add(field, "task_class_scoped", task_classes)
        # The synthetic class grants nothing: the default remains local_only.
        doc = {"policy_version": "1.0.0", "owner_id": doc.get("owner_id"),
               "updated_at": doc.get("updated_at", "1970-01-01"),
               "default_access": "local_only", "task_classes": sorted(classes) or ["legacy"],
               "rules": rules, "notes": doc.get("notes", [])}
    try:
        errors = find_errors(doc)
    except (TypeError, ValueError):
        raise ValueError("privacy policy contains invalid field types") from None
    if errors:
        raise ValueError("invalid privacy policy: " + "; ".join(errors))
    if doc.get("owner_id") != owner_id:
        raise ValueError("privacy policy owner_id does not match the requested owner")
    return doc


def rule_by_path(policy: dict | None, field_path: str) -> dict | None:
    if not isinstance(policy, dict):
        return None
    for rule in policy.get("rules", []):
        if isinstance(rule, dict) and rule.get("field_path") == field_path:
            return rule
    return None


def access_allowed(policy: dict | None, field_path: str, task_class: str | None) -> bool:
    if not isinstance(policy, dict):
        return True

    rule = rule_by_path(policy, field_path)
    if rule is None:
        access = policy.get("default_access", "always_share")
        allowed_task_classes = policy.get("task_classes", []) if access == "task_class_scoped" else None
    else:
        access = rule.get("access", policy.get("default_access", "always_share"))
        allowed_task_classes = rule.get("allowed_task_classes")

    if access == "always_share":
        return True
    if access == "local_only":
        return False
    if access == "task_class_scoped":
        if not task_class:
            return False
        if isinstance(allowed_task_classes, list) and allowed_task_classes:
            return task_class in allowed_task_classes
        task_classes = policy.get("task_classes", [])
        return task_class in task_classes if isinstance(task_classes, list) else False
    return False


def export_array(policy: dict | None, field_path: str, value: Any, task_class: str | None, omissions: list[str]) -> list[str]:
    if access_allowed(policy, field_path, task_class):
        return list(value) if isinstance(value, list) else []
    omissions.append(field_path)
    return []


def append_policy_loss_notes(loss_notes: list[str], omissions: list[str], policy: dict | None, task_class: str | None) -> list[str]:
    notes = list(loss_notes)
    if omissions:
        notes.append("Privacy policy omitted fields: " + ", ".join(sorted(set(omissions))))
        if task_class is None:
            notes.append("Provide --task-class to include task_class_scoped fields when allowed by policy")
    if policy is not None:
        notes.append("Privacy policy applied")
        if task_class is not None:
            notes.append(f"Task-class export: {task_class}")
    return notes
