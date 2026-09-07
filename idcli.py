"""Thin installed CLI wrapper for the ID reference tooling."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from importlib.metadata import version
import tomllib
from scripts.runtime_paths import validate_owner_id

from id_diff import run_cli as run_diff_cli
from id_soul import run_cli as run_soul_cli

REPO_ROOT = Path(__file__).resolve().parent

COMMANDS: dict[str, list[str]] = {
    "bootstrap-owner": ["scripts/bootstrap_owner.py"],
    "diff": [],
    "integration-hook": ["scripts/run_integration_hook.sh"],
    "install-set-hook": [],
    "refresh-soul": [],
    "init": ["scripts/idctl_init.py"],
    "migrate": ["scripts/migrate.py"],
    "validate": ["scripts/validate_profile.py"],
    "validate-privacy": ["scripts/validate_privacy_policy.py"],
    "validate-compact": ["scripts/validate_context_compact.py"],
    "validate-mcp": ["scripts/validate_mcp_resource.py"],
    "validate-observed": ["scripts/validate_observed_behavior.py"],
    "export-interop": ["scripts/export_interop_v1.py"],
    "export-compact": ["scripts/export_context_compact.py"],
    "export-mcp": ["scripts/export_mcp_resource.py"],
    "import-compact": ["scripts/import_context_compact.py"],
    "import-mcp": ["scripts/import_mcp_resource.py"],
    "metrics-readme": ["scripts/generate_metrics_readme.py"],
    "metrics": ["scripts/benchmark_public_report.py"],
    "trend": ["scripts/benchmark_trend_report.py"],
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="idctl",
        description="Thin installed CLI wrapper for the ID reference tooling.",
    )
    parser.add_argument("--version", action="version", version=(tomllib.loads((REPO_ROOT / "pyproject.toml").read_text())["project"]["version"] if (REPO_ROOT / "pyproject.toml").is_file() else version("id-protocol")))
    parser.add_argument("command", nargs="?", choices=sorted(COMMANDS))
    parser.add_argument("args", nargs=argparse.REMAINDER)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    ns = parser.parse_args(argv)
    if not ns.command:
        parser.print_help()
        return 0

    for index, item in enumerate(ns.args):
        if item == "--owner-id" and index + 1 < len(ns.args):
            owner_id = ns.args[index + 1]
        elif item.startswith("--owner-id="):
            owner_id = item.split("=", 1)[1]
        else:
            continue
        try:
            validate_owner_id(owner_id)
        except ValueError as exc:
            parser.error(str(exc))
    if ns.command == "install-set-hook":
        hook_parser = argparse.ArgumentParser(prog="idctl install-set-hook")
        hook_parser.add_argument("--path", type=Path, default=Path.cwd())
        opts = hook_parser.parse_args(ns.args)
        destination = opts.path / "scripts" / "run_integration_hook.sh"
        body = '#!/usr/bin/env bash\nset -euo pipefail\ncd "$(dirname "${BASH_SOURCE[0]}")/.."\nexec idctl integration-hook "$@"\n'
        if destination.is_symlink() or (destination.exists() and destination.read_text() != body):
            parser.error(f"Refusing to replace existing hook: {destination}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(body)
        destination.chmod(0o755)
        print(f"Installed SET hook: {destination}")
        return 0
    if ns.command == "refresh-soul":
        return run_soul_cli(ns.args)
    if ns.command == "diff":
        return run_diff_cli(ns.args)

    script = REPO_ROOT / COMMANDS[ns.command][0]
    interpreter = "bash" if ns.command == "integration-hook" else sys.executable
    env = dict(os.environ, ID_PYTHON=sys.executable)
    completed = subprocess.run([interpreter, str(script), *ns.args], check=False, env=env)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
