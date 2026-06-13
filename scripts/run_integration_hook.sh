#!/usr/bin/env bash
set -euo pipefail

resolve_preferred_human_bootstrap() {
  local owner_id="$1"
  python3 - "$owner_id" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path

owner_id = sys.argv[1]
defaults = [
    f"profiles/{owner_id}/soul.md",
    f"profiles/{owner_id}/profile.core.md",
    f"profiles/{owner_id}/handshake.md",
]
paths: list[str] = []
context_path = Path("docs/ai/id-context.json")
if context_path.is_file():
    try:
        payload = json.loads(context_path.read_text(encoding="utf-8"))
        usage = payload.get("usage") if isinstance(payload, dict) else None
        bootstrap = usage.get("preferred_human_bootstrap") if isinstance(usage, dict) else None
        if isinstance(bootstrap, list):
            for item in bootstrap:
                if isinstance(item, str) and item.strip():
                    paths.append(item.replace("<owner>", owner_id))
    except Exception:
        pass

for item in defaults:
    if item not in paths:
        paths.append(item)

for item in paths:
    print(item)
PY
}

usage() {
  cat <<'USAGE'
Usage:
  scripts/run_integration_hook.sh pre_task --owner-id <id> --target <agentsmd|lab|set>
  scripts/run_integration_hook.sh post_task --owner-id <id> --session-context "..." --sections-used "..." --changes-made "..." [--open-questions "..."]
  scripts/run_integration_hook.sh weekly_review --owner-id <id>
USAGE
}

if [[ $# -lt 1 ]]; then
  usage
  exit 2
fi

HOOK="$1"
shift

OWNER_ID=""
TARGET=""
SESSION_CONTEXT=""
SECTIONS_USED=""
CHANGES_MADE=""
OPEN_QUESTIONS="None"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --owner-id)
      OWNER_ID="$2"
      shift 2
      ;;
    --target)
      TARGET="$2"
      shift 2
      ;;
    --session-context)
      SESSION_CONTEXT="$2"
      shift 2
      ;;
    --sections-used)
      SECTIONS_USED="$2"
      shift 2
      ;;
    --changes-made)
      CHANGES_MADE="$2"
      shift 2
      ;;
    --open-questions)
      OPEN_QUESTIONS="$2"
      shift 2
      ;;
    *)
      echo "Unknown arg: $1"
      usage
      exit 2
      ;;
  esac
done

if [[ -z "$OWNER_ID" ]]; then
  echo "ERROR: --owner-id is required"
  exit 2
fi

case "$HOOK" in
  pre_task)
    if [[ -z "$TARGET" ]]; then
      echo "ERROR: --target is required for pre_task"
      exit 2
    fi

    python3 scripts/validate_profile.py --owner-id "$OWNER_ID" --allow-stale

    CORE="profiles/${OWNER_ID}/profile.core.md"
    HANDSHAKE="profiles/${OWNER_ID}/handshake.md"
    SOUL="profiles/${OWNER_ID}/soul.md"

    BOOTSTRAP_CANDIDATES=()
    while IFS= read -r item; do
      [[ -n "$item" ]] || continue
      BOOTSTRAP_CANDIDATES+=("$item")
    done < <(resolve_preferred_human_bootstrap "$OWNER_ID")
    EXISTING_BOOTSTRAP=()
    for item in "${BOOTSTRAP_CANDIDATES[@]}"; do
      if [[ -f "$item" ]]; then
        EXISTING_BOOTSTRAP+=("$item")
      fi
    done

    if [[ ! -f "$CORE" ]]; then
      echo "ERROR: missing $CORE"
      exit 1
    fi

    if [[ ! -f "$HANDSHAKE" ]]; then
      echo "ERROR: missing $HANDSHAKE"
      exit 1
    fi

    echo "[pre_task] target=$TARGET owner=$OWNER_ID"
    if [[ -f "$SOUL" ]]; then
      echo "soul=$SOUL"
    fi
    echo "profile_core=$CORE"
    echo "handshake=$HANDSHAKE"
    if [[ ${#EXISTING_BOOTSTRAP[@]} -gt 0 ]]; then
      echo "primary_human_bootstrap=${EXISTING_BOOTSTRAP[0]}"
      echo "preferred_human_bootstrap=$(IFS='|'; echo "${EXISTING_BOOTSTRAP[*]}")"
    else
      echo "primary_human_bootstrap=$CORE"
      echo "preferred_human_bootstrap=$CORE|$HANDSHAKE"
    fi
    echo "integration_guide=integrations/${TARGET}/README.md"
    ;;

  post_task)
    if [[ -z "$SESSION_CONTEXT" || -z "$SECTIONS_USED" || -z "$CHANGES_MADE" ]]; then
      echo "ERROR: --session-context, --sections-used, --changes-made are required for post_task"
      exit 2
    fi

    python3 scripts/session_update.py \
      --owner-id "$OWNER_ID" \
      --session-context "$SESSION_CONTEXT" \
      --sections-used "$SECTIONS_USED" \
      --changes-made "$CHANGES_MADE" \
      --open-questions "$OPEN_QUESTIONS"

    echo "[post_task] changelog updated for owner=$OWNER_ID"
    ;;

  weekly_review)
    mkdir -p data/processed/integration
    REPORT="data/processed/integration/weekly-review-${OWNER_ID}-$(date +%F).txt"

    {
      echo "# Weekly Review"
      echo "date: $(date +%F)"
      echo "owner: $OWNER_ID"
      echo
      echo "## Profile Validation"
      python3 scripts/validate_profile.py --owner-id "$OWNER_ID" --allow-stale || true
      echo
      echo "## Raw Publish Guard"
      python3 scripts/check_publish_guard.py --all-tracked || true
    } > "$REPORT"

    echo "[weekly_review] report=$REPORT"
    ;;

  *)
    echo "ERROR: unknown hook '$HOOK'"
    usage
    exit 2
    ;;
esac
