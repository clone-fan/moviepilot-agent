#!/bin/sh
set -eu

STATE_DIR="/config/agent/runtime/state"
MARKER_FILE="$STATE_DIR/moviepilot_selfheal_boot.marker"
PYTHON_BIN="/opt/venv/bin/python"
HEAL_SCRIPT="/config/agent/scripts/ensure_telegram_urllib3_patch.py"

mkdir -p "$STATE_DIR"

if [ ! -r /proc/1/stat ]; then
  echo "SKIP boot marker source unavailable: /proc/1/stat"
  exit 1
fi

CURRENT_BOOT_ID="$(awk '{print $22}' /proc/1/stat)"
LAST_BOOT_ID=""
if [ -f "$MARKER_FILE" ]; then
  LAST_BOOT_ID="$(cat "$MARKER_FILE" 2>/dev/null || true)"
fi

if [ "$CURRENT_BOOT_ID" = "$LAST_BOOT_ID" ]; then
  echo "OK boot selfheal already done boot_id=$CURRENT_BOOT_ID"
  exit 0
fi

echo "START boot selfheal boot_id=$CURRENT_BOOT_ID"
PYTHONDONTWRITEBYTECODE=1 "$PYTHON_BIN" "$HEAL_SCRIPT"
printf '%s\n' "$CURRENT_BOOT_ID" > "$MARKER_FILE"
echo "DONE boot selfheal boot_id=$CURRENT_BOOT_ID"
