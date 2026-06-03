---
name: moviepilot-direct-routes
version: 2
description: >-
  MUST-USE when the user sends a slash command, 115 share link, magnet/ed2k
  link, or obvious natural-language command alias. Do not route through AI
  reasoning, media search, library check, or database query when a direct
  slash command exists. Covers /cookiecloud, /sites, /subscribes, /downloading,
  /transfer, /redo, /clear_cache, /restart, /version, /clear_session,
  /stop_agent, /skills, /site_signin, /update_covers, /p115_full_sync,
  /p115_inc_sync, /p115_add_share, /p115_share_strm, /ol, /p115_strm, /sh,
  /p115_checkin, and similar. This is the first routing skill for direct
  command execution; do not bypass it with general tools.
allowed-tools: list_slash_commands query_plugin_capabilities run_slash_command
---

# MoviePilot Direct Routes

## HARD GATE

If the user request can be satisfied by a known MoviePilot slash command,
translate it directly and run it. Do not search, inspect, explain, or reason.

When the user sends:

- A slash command (`/sites`, `/downloading`, `/sh 沙丘2`)
- A 115 share link (`https://115cdn.com/s/...`)
- A magnet/ed2k link
- An obvious command alias (`同步站点`, `查看下载`, `签到`)

→ run it with `run_slash_command`. Do not add steps.

## Routing Priority

1. Exact slash command → execute directly.
2. 115 link / magnet / ed2k → execute directly.
3. Natural language alias → map to known command → execute.
4. Unknown command → hand off to `command-dispatch`.

## Do Not

- Search media or torrents first
- Inspect libraries or databases first
- Explain the mapping in detail
- Route through AI reasoning when a direct command exists

## Final Rule

**If a direct command exists, use it. This is not optional.**