#!/usr/bin/env python3
"""Redact normalized text/json files into safe-share layer.

Input:  data/normalized
Output: data/processed/redacted
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".md", ".json"}

EMAIL_RE = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b")
PHONE_RE = re.compile(r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)")
URL_RE = re.compile(r"\b(?:https?://|www\.)[^\s<>()]+", re.IGNORECASE)
HANDLE_RE = re.compile(r"(?<!\w)@[A-Za-z0-9_\.]{2,}")
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Redact normalized files for external sharing")
    parser.add_argument("--input-dir", default="data/normalized", help="Input directory")
    parser.add_argument("--output-dir", default="data/processed/redacted", help="Output directory")
    parser.add_argument(
        "--report",
        default="data/processed/redaction-report.json",
        help="Path to JSON report with counters",
    )
    return parser.parse_args()


def redact_text(text: str) -> tuple[str, dict[str, int]]:
    counts = {
        "emails": 0,
        "phones": 0,
        "urls": 0,
        "handles": 0,
        "ipv4": 0,
    }

    text, counts["emails"] = EMAIL_RE.subn("[REDACTED_EMAIL]", text)
    text, counts["phones"] = PHONE_RE.subn("[REDACTED_PHONE]", text)
    text, counts["urls"] = URL_RE.subn("[REDACTED_URL]", text)
    text, counts["handles"] = HANDLE_RE.subn("[REDACTED_HANDLE]", text)
    text, counts["ipv4"] = IPV4_RE.subn("[REDACTED_IP]", text)

    return text, counts


def redact_json_payload(value, counters: dict[str, int]):
    if isinstance(value, dict):
        return {k: redact_json_payload(v, counters) for k, v in value.items()}
    if isinstance(value, list):
        return [redact_json_payload(v, counters) for v in value]
    if isinstance(value, str):
        redacted, local = redact_text(value)
        for key, num in local.items():
            counters[key] += num
        return redacted
    return value


def should_process(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS


def main() -> int:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    report_path = Path(args.report)

    output_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    files = sorted(p for p in input_dir.rglob("*") if should_process(p)) if input_dir.exists() else []

    report = {
        "input_dir": str(input_dir),
        "output_dir": str(output_dir),
        "files_processed": 0,
        "totals": {"emails": 0, "phones": 0, "urls": 0, "handles": 0, "ipv4": 0},
        "files": [],
    }

    for path in files:
        rel = path.relative_to(input_dir)
        dst = output_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)

        raw = path.read_text(encoding="utf-8", errors="ignore")
        counters = {"emails": 0, "phones": 0, "urls": 0, "handles": 0, "ipv4": 0}

        if path.suffix.lower() == ".json":
            try:
                payload = json.loads(raw)
                redacted_payload = redact_json_payload(payload, counters)
                dst.write_text(
                    json.dumps(redacted_payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
            except json.JSONDecodeError:
                redacted, local = redact_text(raw)
                for k, n in local.items():
                    counters[k] += n
                dst.write_text(redacted, encoding="utf-8")
        else:
            redacted, local = redact_text(raw)
            for k, n in local.items():
                counters[k] += n
            dst.write_text(redacted, encoding="utf-8")

        report["files_processed"] += 1
        for k, n in counters.items():
            report["totals"][k] += n

        report["files"].append(
            {
                "source": str(path),
                "output": str(dst),
                "replacements": counters,
            }
        )

    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Processed files: {report['files_processed']}")
    print(f"Report: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
