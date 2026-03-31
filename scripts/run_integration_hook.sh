#!/usr/bin/env bash
set -euo pipefail

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

    if [[ ! -f "$CORE" ]]; then
      echo "ERROR: missing $CORE"
      exit 1
    fi

    if [[ ! -f "$HANDSHAKE" ]]; then
      echo "ERROR: missing $HANDSHAKE"
      exit 1
    fi

    echo "[pre_task] target=$TARGET owner=$OWNER_ID"
    echo "profile_core=$CORE"
    echo "handshake=$HANDSHAKE"
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
