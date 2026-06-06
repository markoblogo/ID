#!/usr/bin/env python3
"""Build a registry-compatible server.json from local project metadata."""

from __future__ import annotations

import argparse
import json
import os
import tomllib
from pathlib import Path
from typing import Any

SERVER_JSON_SCHEMA_URL = "https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json"


def derive_server_name(manifest_name: str, repo: str) -> str:
    if manifest_name and "/" in manifest_name:
        return manifest_name

    owner, _, project = repo.partition("/")
    if owner and project:
        project_slug = project.lower().replace("_", "-")
        return f"io.github.{owner}/{project_slug}"

    if manifest_name:
        return f"io.github.markoblogo/{manifest_name.lower().replace('_', '-')}"
    return "io.github.markoblogo/id"


def normalize_version(version: str | None) -> str:
    return (version or "").removeprefix("v")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build MCP registry server.json for PyPI publishing.")
    parser.add_argument("--manifest", default="mcp-manifest.json", help="Path to mcp manifest JSON.")
    parser.add_argument("--pyproject", default="pyproject.toml", help="Path to pyproject.toml.")
    parser.add_argument("--repo", default=os.getenv("GITHUB_REPOSITORY", "markoblogo/ID"), help="Repository slug used to derive the registry server name.")
    parser.add_argument("--version", default=os.getenv("MCP_REGISTRY_VERSION"), help="Release version. A leading 'v' is removed.")
    parser.add_argument("--output", default="server.json", help="Output path for the generated server.json.")
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_pyproject(path: Path) -> dict[str, Any]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def build_server_json(manifest: dict[str, Any], pyproject: dict[str, Any], repo: str, version: str | None) -> dict[str, Any]:
    project = pyproject["project"]
    repository = manifest.get("repository") if isinstance(manifest.get("repository"), dict) else {}
    repository_url = manifest.get("homepage") or repository.get("url")
    normalized_version = normalize_version(version) or str(manifest.get("version") or project["version"])

    server = {
        "$schema": SERVER_JSON_SCHEMA_URL,
        "name": derive_server_name(str(manifest.get("name", "")), repo),
        "title": manifest.get("display_name") or manifest.get("name") or project["name"],
        "description": manifest.get("description") or "Portable human-AI context protocol reference tooling.",
        "version": normalized_version,
        "packages": [
            {
                "registryType": "pypi",
                "identifier": project["name"],
                "version": normalized_version,
                "transport": {"type": "stdio"},
            }
        ],
        "repository": {
            "url": repository_url,
            "source": "github" if repository_url and "github.com" in repository_url else None,
        },
    }
    cleaned = {}
    for key, value in server.items():
        if value in (None, "", []):
            continue
        if isinstance(value, dict):
            value = {child_key: child_value for child_key, child_value in value.items() if child_value not in (None, "", [])}
            if not value:
                continue
        cleaned[key] = value
    return cleaned


def main() -> int:
    args = parse_args()
    manifest = load_manifest(Path(args.manifest))
    pyproject = load_pyproject(Path(args.pyproject))
    server = build_server_json(manifest, pyproject, args.repo, args.version)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(server, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
