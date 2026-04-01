#!/usr/bin/env bash
set -euo pipefail

# Cleanup only known ID-related stuck commands.
PATTERN='python3 scripts/(export_interop_v1|validate_interop_v1|validate_profile|check_publish_guard|benchmark_init_run|benchmark_validate_run|benchmark_report)\.py|/bin/zsh -c python3 scripts/'

echo "[cleanup] scanning for stuck ID jobs"
PIDS=$(ps aux | grep -E "$PATTERN" | grep -v grep | awk '{print $2}' || true)

if [[ -z "${PIDS:-}" ]]; then
  echo "[cleanup] no matching jobs found"
  exit 0
fi

echo "[cleanup] terminating pids: $PIDS"
# shellcheck disable=SC2086
kill $PIDS || true
sleep 1

LEFT=$(ps aux | grep -E "$PATTERN" | grep -v grep | wc -l | tr -d ' ')
echo "[cleanup] remaining matching jobs: $LEFT"

if [[ "$LEFT" != "0" ]]; then
  echo "[cleanup] forcing termination"
  # shellcheck disable=SC2086
  kill -9 $PIDS || true
fi

echo "[cleanup] done"
