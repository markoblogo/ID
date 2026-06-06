from __future__ import annotations

import json
import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = REPO_ROOT / "schemas"
API_DIR = REPO_ROOT / "api"


def test_schema_ids_use_public_raw_url() -> None:
    for path in SCHEMA_DIR.glob("*.json"):
        if path.name == "README.md":
            continue
        schema = json.loads(path.read_text(encoding="utf-8"))
        schema_id = schema.get("$id", "")
        assert schema_id.startswith("https://raw.githubusercontent.com/markoblogo/ID/main/schemas/")


def test_mcp_manifest_points_to_known_contracts() -> None:
    manifest = json.loads((REPO_ROOT / "mcp-manifest.json").read_text(encoding="utf-8"))
    schema_paths = {Path(item["schema"]).name for item in manifest["artifacts"]}
    assert "interop-v1.schema.json" in schema_paths
    assert "context-compact-v0.schema.json" in schema_paths
    assert "mcp-context-resource-v1.schema.json" in schema_paths
    assert "privacy-policy-v1.schema.json" in schema_paths


def test_api_contracts_exist() -> None:
    assert (API_DIR / "id-protocol.openapi.yaml").exists()
    assert (API_DIR / "id-protocol.mcp.json").exists()


def test_version_in_sync_with_pyproject() -> None:
    pyproject = tomllib.loads(REPO_ROOT.joinpath("pyproject.toml").read_text(encoding="utf-8"))
    project_version = pyproject["project"]["version"]
    manifest = json.loads((REPO_ROOT / "mcp-manifest.json").read_text(encoding="utf-8"))
    assert manifest["version"] == project_version


def test_readme_declares_registry_mcp_name() -> None:
    readme = REPO_ROOT.joinpath("README.md").read_text(encoding="utf-8")
    assert "<!-- mcp-name: io.github.markoblogo/id -->" in readme
