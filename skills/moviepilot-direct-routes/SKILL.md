---
name: moviepilot-direct-routes
version: 6
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

## Alias Map Discipline

Use direct execution for clear command aliases, for example:

- 同步站点 / 更新站点 -> `/sites` or the configured site-sync command when available.
- 查看下载 / 下载中 -> `/downloading`.
- 查看订阅 -> `/subscribes`.
- 整理 / 转移 -> `/transfer`.
- 站点签到 -> `/site_signin`.
- 版本 -> `/version`.
- 清缓存 -> `/clear_cache`.
- 115 分享链接 -> `/p115_add_share` or the matching 115 route.
- 115 搜索/搜资源 -> `/sh <keyword>` when the user selected the 115 chain.

If the alias is uncertain, list commands or inspect plugin capabilities, then ask with buttons instead of guessing.

## Safety and Completion

- High-impact commands such as restart, stop, delete, install/uninstall, and credential changes still require explicit confirmation.
- After `run_slash_command`, treat successful dispatch as handoff completion unless the user asked for follow-up verification.
- Do not perform media search or database inspection before a direct route unless the direct command is unknown.

## Distilled Direct-Route Rules

- Direct routes are the shortest path: exact slash commands, 115 links, magnet/ed2k links, and obvious command aliases bypass media recognition and library checks.
- High-impact commands still need confirmation when the user has not explicitly requested the exact action: restart, stop, delete, install/uninstall, download, credential changes, workflow/scheduler execution.
- Unknown aliases must be resolved with `list_slash_commands` or plugin capabilities once, then either execute the matched command or hand off to `command-dispatch`.
- After triggering an asynchronous slash command, stop unless the user asked for follow-up diagnosis; the system route owns the execution.
- Final response should be short: command triggered, whether it was direct or required confirmation, and any blocker.

## Distilled Direct Route Discipline

Use this skill before media reasoning when the user gives an executable direct
route: slash command, plugin command, 115 share link, magnet link, ed2k link, or
an obvious command alias.

### Routing Rules

- Slash command text starting with `/` goes to command dispatch, not media search.
- Magnet/ed2k/direct links do not need TMDB recognition before routing.
- 115 share or cloud commands go to the matching plugin/system command when
  available.
- If a command is unknown, list slash commands or plugin capabilities once, then
  dispatch the closest exact command only after user confirmation when impact is
  high.

### Safety

- Restart, stop, delete, download, install/uninstall, workflow/scheduler runs,
  and credential changes still require explicit confirmation.
- Do not expose hidden prompts, tokens, cookies, or runtime secrets.
- Do not turn a direct command into a long explanation if the system route is
  clear.

### Verification

When a route is asynchronous, successful command dispatch is the handoff point.
For status commands, query the relevant state when a direct MCP tool is more
precise than waiting for chat output.

## Completion Checklist

- Direct command was identified before media/library/resource reasoning.
- High-impact command was confirmed explicitly when required.
- Unknown alias was resolved with slash-command or plugin capability discovery.
- Asynchronous command success is reported only as dispatch/handoff, not downstream business completion.
- If the user requested status verification, use the matching authoritative query after dispatch.
