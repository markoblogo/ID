#!/usr/bin/env python3
"""Publish mcp-manifest.json to an MCP registry endpoint."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
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
    return "io.github.markoblogo/id-protocol"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync MCP manifest to configured registry endpoint.")
    parser.add_argument(
        "--manifest",
        default="mcp-manifest.json",
        help="Path to mcp manifest JSON.",
    )
    parser.add_argument(
        "--endpoint",
        help="Registry endpoint URL (for example https://registry.example.com/v1/manifests).",
        default=os.getenv("MCP_REGISTRY_ENDPOINT"),
    )
    parser.add_argument(
        "--token",
        help="Optional bearer token for registry auth.",
        default=os.getenv("MCP_REGISTRY_TOKEN"),
    )
    parser.add_argument(
        "--project",
        help="Optional project identifier reported to registry.",
        default=os.getenv("MCP_REGISTRY_PROJECT", "markoblogo/ID"),
    )
    parser.add_argument(
        "--version",
        help="Optional manifest/project version reported to registry.",
        default=os.getenv("MCP_REGISTRY_VERSION"),
    )
    parser.add_argument(
        "--registry-source",
        help="Optional source tag for payload metadata.",
        default=os.getenv("GITHUB_REPOSITORY", "markoblogo/ID"),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print payload and skip network call.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=15.0,
        help="HTTP timeout in seconds.",
    )
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_payload(manifest: dict[str, Any], args: argparse.Namespace) -> dict[str, Any]:
    repository_url = manifest.get("homepage") or (manifest.get("repository", {}).get("url") if isinstance(manifest.get("repository"), dict) else None)
    description = manifest.get("description") or manifest.get("display_name") or "Machine-readable MCP registry manifest."
    server_name = derive_server_name(manifest.get("name", ""), args.registry_source)

    payload = {
        "$schema": SERVER_JSON_SCHEMA_URL,
        "name": server_name,
        "description": description,
        "version": args.version or str(manifest.get("version", "")),
        "title": manifest.get("display_name") or manifest.get("name"),
        "websiteUrl": manifest.get("homepage"),
        "repository": {
            "url": repository_url,
        },
    }
    return {key: value for key, value in payload.items() if value not in (None, "", {}, {"url": ""})}


def publish(payload: dict[str, Any], endpoint: str, token: str | None, timeout: float) -> None:
    request = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "User-Agent": "id-protocol-manifest-sync/1.0",
        },
    )
    if token:
        request.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.getcode()
            body = response.read().decode("utf-8").strip()
            print(f"published: {status}")
            if body:
                print(body)
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"manifest publish failed: HTTP {exc.code}: {exc.read().decode('utf-8', errors='replace')}")
    except urllib.error.URLError as exc:
        raise SystemExit(f"manifest publish failed: {exc}")


def main() -> int:
    args = parse_args()
    if not args.endpoint:
        print("SKIP: MCP_REGISTRY_ENDPOINT is not configured; set it to enable registry sync.")
        return 0

    manifest_path = Path(args.manifest)
    manifest = load_manifest(manifest_path)
    payload = build_payload(manifest, args)

    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    publish(payload, args.endpoint, args.token, args.timeout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
