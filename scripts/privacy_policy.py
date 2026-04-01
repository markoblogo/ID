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
    return load_json(path)


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
