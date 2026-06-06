from __future__ import annotations

import importlib.util
import unittest
import sys
from datetime import date
from pathlib import Path
from typing import Any

try:
    from hypothesis import given, strategies as st
except ModuleNotFoundError:  # pragma: no cover
    st = None
    given = None

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, REPO_ROOT / "scripts" / name)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    scripts_path = str(REPO_ROOT / "scripts")
    previous_paths = list(sys.path)
    sys.path.insert(0, scripts_path)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path = previous_paths
    return module


interop = _load_module("validate_interop_v1.py")
compact = _load_module("validate_context_compact.py")
privacy = _load_module("validate_privacy_policy.py")
mcp = _load_module("validate_mcp_resource.py")


if st is None:

    class TestPropertyValidatorsDependency(unittest.TestCase):
        @unittest.skip("hypothesis dependency is not installed")
        def test_dependency_missing(self) -> None:
            self.assertTrue(True)

else:

    dates = st.dates(min_value=date(2025, 1, 1), max_value=date(2026, 12, 31)).map(lambda d: d.isoformat())
    owner_name = st.text(alphabet="abcdefghijklmnopqrstuvwxyz0123456789-_", min_size=1, max_size=12)
    word = st.text(min_size=1, max_size=12, alphabet="abcdefghijklmnopqrstuvwxyz")

    def _valid_compact_payload(owner: str, updated_at: str, trust: str, ttl: int) -> dict[str, Any]:
        return {
            "context_version": "0.1.0",
            "owner_id": owner,
            "updated_at": updated_at,
            "freshness_ttl_days": ttl,
            "trust_level": trust,
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
            "loss_notes": [],
        }

    @st.composite
    def valid_interop_payload(draw) -> dict[str, Any]:
        owner_id = draw(owner_name)
        generated_at = draw(dates)
        return {
            "interop_version": "1.0.0",
            "owner_id": owner_id,
            "generated_at": generated_at,
            "profiles": {
                "core": {
                    "metadata": {
                        "version": "0.1.0",
                        "profile_id": owner_id,
                        "updated_at": generated_at,
                        "freshness_ttl_days": 14,
                        "trust_level": "trusted",
                    },
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
                },
                "extended": {
                    "metadata": {
                        "version": "0.1.0",
                        "profile_id": owner_id,
                        "updated_at": generated_at,
                        "freshness_ttl_days": 14,
                        "trust_level": "trusted",
                    },
                    "stable_preferences": [],
                    "domain_workflows": {},
                    "misalignments": [],
                    "lexicon": [],
                    "environment_assumptions": [],
                    "decision_heuristics": [],
                    "known_good_prompts": [],
                    "extensions": {},
                },
            },
        }

    @st.composite
    def valid_compact_payload(draw) -> dict[str, Any]:
        return _valid_compact_payload(
            owner=draw(owner_name),
            updated_at=draw(dates),
            trust=draw(st.sampled_from(["trusted", "provisional", "archival"])),
            ttl=draw(st.integers(min_value=1, max_value=60)),
        )

    @st.composite
    def valid_privacy_payload(draw) -> dict[str, Any]:
        access_level = draw(st.sampled_from(["always_share", "local_only", "task_class_scoped"]))
        task_classes = draw(st.lists(word, min_size=1, max_size=4, unique=True))
        return {
            "policy_version": "1.0.0",
            "owner_id": draw(owner_name),
            "updated_at": draw(dates),
            "default_access": access_level,
            "task_classes": task_classes,
            "rules": [
                {
                    "field_path": "profiles.core.communication",
                    "access": access_level,
                    "allowed_task_classes": task_classes[:1] if access_level == "task_class_scoped" else None,
                    "rationale": "policy rationale",
                }
            ],
            "notes": ["generated"],
        }

    @st.composite
    def valid_mcp_payload(draw) -> dict[str, Any]:
        owner = draw(owner_name)
        updated_at = draw(dates)
        content = _valid_compact_payload(
            owner=owner,
            updated_at=updated_at,
            trust=draw(st.sampled_from(["trusted", "provisional", "archival"])),
            ttl=14,
        )
        return {
            "resource_version": "1.0.0",
            "owner_id": owner,
            "uri": f"id://{owner}/context.compact",
            "name": f"ID Context: {owner}",
            "description": "Policy-aware MCP resource",
            "mime_type": "application/json",
            "contents": content,
            "policy": {
                "applied": True,
                "task_class": "coding",
                "source": "profiles/example/privacy-policy.v1.json",
            },
        }

    @given(payload=valid_interop_payload())
    def test_interop_validator_accepts_valid_fuzz_examples(payload: dict[str, Any]) -> None:
        assert interop.find_errors(payload) == []

    @given(payload=valid_compact_payload())
    def test_compact_validator_accepts_valid_fuzz_examples(payload: dict[str, Any]) -> None:
        assert compact.find_errors(payload) == []

    @given(payload=valid_privacy_payload())
    def test_privacy_validator_accepts_valid_fuzz_examples(payload: dict[str, Any]) -> None:
        errors = privacy.find_errors(payload)
        assert errors == []

    @given(payload=valid_mcp_payload())
    def test_mcp_validator_accepts_valid_fuzz_examples(payload: dict[str, Any]) -> None:
        assert mcp.find_errors(payload) == []

    @given(
        payload=valid_compact_payload(),
        key=st.sampled_from(["context_version", "owner_id", "updated_at", "trust_level"]),
    )
    def test_compact_validator_flags_removed_required_fields(payload: dict[str, Any], key: str) -> None:
        payload.pop(key)
        assert compact.find_errors(payload) != []
