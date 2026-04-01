"""Thin installed CLI wrapper for the ID reference tooling."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

COMMANDS: dict[str, list[str]] = {
    "bootstrap-owner": ["scripts/bootstrap_owner.py"],
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
    "metrics": ["scripts/benchmark_public_report.py"],
    "trend": ["scripts/benchmark_trend_report.py"],
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="idctl",
        description="Thin installed CLI wrapper for the ID reference tooling.",
    )
    parser.add_argument("command", nargs="?", choices=sorted(COMMANDS))
    parser.add_argument("args", nargs=argparse.REMAINDER)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    ns = parser.parse_args(argv)
    if not ns.command:
        parser.print_help()
        return 0

    script = REPO_ROOT / COMMANDS[ns.command][0]
    completed = subprocess.run([sys.executable, str(script), *ns.args], check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
