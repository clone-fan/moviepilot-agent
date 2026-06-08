#!/bin/sh
set -eu

STATE_DIR="/config/agent/runtime/state"
MARKER_FILE="$STATE_DIR/cron_boot.marker"
mkdir -p "$STATE_DIR"

if [ ! -r /proc/1/stat ]; then
  echo "SKIP cron boot marker source unavailable: /proc/1/stat"
  exit 1
fi

CURRENT_BOOT_ID="$(awk '{print $22}' /proc/1/stat)"
LAST_BOOT_ID=""
if [ -f "$MARKER_FILE" ]; then
  LAST_BOOT_ID="$(cat "$MARKER_FILE" 2>/dev/null || true)"
fi

if [ "$CURRENT_BOOT_ID" = "$LAST_BOOT_ID" ]; then
  if ps -ef | grep -v grep | grep -q '^root .* /usr/sbin/cron$'; then
    echo "OK cron already running boot_id=$CURRENT_BOOT_ID"
    exit 0
  fi
fi

if ps -ef | grep -v grep | grep -q '^root .* /usr/sbin/cron$'; then
  printf '%s\n' "$CURRENT_BOOT_ID" > "$MARKER_FILE"
  echo "OK cron detected and marker refreshed boot_id=$CURRENT_BOOT_ID"
  exit 0
fi

/usr/sbin/cron
sleep 1
if ps -ef | grep -v grep | grep -q '^root .* /usr/sbin/cron$'; then
  printf '%s\n' "$CURRENT_BOOT_ID" > "$MARKER_FILE"
  echo "DONE cron started boot_id=$CURRENT_BOOT_ID"
  exit 0
fi

echo "FAIL cron did not stay running boot_id=$CURRENT_BOOT_ID"
exit 1
