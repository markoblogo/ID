"""Installed resource lookup and portable owner identifiers."""
from __future__ import annotations

import re
import sys
from pathlib import Path


def resource_path(relative: str) -> Path:
    source = Path(__file__).resolve().parents[1] / relative
    if source.is_file():
        return source
    installed = Path(sys.prefix) / 'share' / 'id-protocol' / relative
    if not installed.is_file():
        raise FileNotFoundError(f'Missing ID package resource: {relative}; reinstall id-protocol')
    return installed


def validate_owner_id(owner_id: str) -> str:
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}', owner_id):
        raise ValueError('owner-id must be 1-128 letters, digits, dots, underscores or hyphens, starting with a letter or digit')
    return owner_id
