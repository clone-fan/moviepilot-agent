---
name: moviepilot-direct-routes
version: 1
description: >-
  Use this skill when the user wants MoviePilot or installed plugin features to
  execute directly through existing slash commands instead of AI reasoning. This
  skill covers exact slash commands, obvious natural-language aliases, 115 share
  links, magnet/ed2k links, and simple command-style requests that should be
  translated straight into /cookiecloud, /sites, /subscribes, /downloading,
  /transfer, /redo, /clear_cache, /restart, /version, /clear_session,
  /stop_agent, /session_status, /skills, /site_signin, /update_covers,
  /cd2_restart, /cd2_info, /cd, /p115_full_sync, /p115_inc_sync,
  /p115_add_share, /p115_share_strm, /ol, /p115_strm, /sh, /hdhivechin, or
  /p115_checkin.
allowed-tools: list_slash_commands query_plugin_capabilities run_slash_command
---

# MoviePilot Direct Routes

This is the unified direct-routing skill. It replaces the overlapping local
skills that previously handled command dispatch, 115 routing, and other command
shortcuts separately.

## What This Skill Does

If the user request can be satisfied by a known MoviePilot slash command,
translate it directly and run it.

Do not:

- search media or torrents first
- inspect libraries first
- query databases first
- explain the mapping in detail
- touch official built-in skills

## Included Routing Areas

This single skill covers the previous overlapping local functions:

- system / plugin slash-command dispatch
- 115 share transfer and 115 offline routing
- 115 resource search routing
- exact slash-command passthrough

## Workflow

### 1. Detect Exact Commands

If the user sends a slash command, run it directly with `run_slash_command`.
Examples:

- `/sites`
- `/downloading`
- `/sh 沙丘2`
- `/p115_add_share https://115cdn.com/s/...`
- `/ol magnet:?xt=...`

### 2. Detect Direct Link Types

- `115cdn.com/s/` or `115.com/s/` -> `/p115_add_share`
- `magnet:?` or `ed2k://` -> `/ol`
- direct 115 share + explicit STRM wording -> `/p115_share_strm`
- plain resource search phrase like `115搜 xxx` or `搜索资源 xxx` -> `/sh xxx`

### 3. Detect Simple Alias Intent

Use the most stable existing slash command and preserve arguments exactly.

### 4. Dispatch

Call `run_slash_command` once the target command is identified.

### 5. Keep the Reply Minimal

Report only that the command has been dispatched or started.

## Alias Map

| Intent | Command |
|---|---|
| 同步站点 / 更新站点 / CookieCloud | `/cookiecloud` |
| 站点管理 / 站点列表 | `/sites` |
| 同步媒体服务器 / 刷新媒体库 | `/mediaserver_sync` |
| 管理订阅 / 订阅列表 | `/subscribes` |
| 正在下载 / 下载中 / 查看下载 | `/downloading` |
| 下载文件整理 / 触发整理 | `/transfer` |
| 手动整理 / 重新整理 | `/redo` |
| 清理缓存 | `/clear_cache` |
| 重启系统 | `/restart` |
| 当前版本 | `/version` |
| 清除会话 | `/clear_session` |
| 停止推理 / 停止AI | `/stop_agent` |
| 会话状态 | `/session_status` |
| 管理技能 / 查看技能 | `/skills` |
| 站点签到 | `/site_signin` |
| 更新封面 | `/update_covers` |
| 重启CloudDrive2 | `/cd2_restart` |
| CloudDrive2信息 | `/cd2_info` |
| 云下载 | `/cd` |
| 115全量同步 | `/p115_full_sync` |
| 115增量同步 | `/p115_inc_sync` |
| 115转存 / 保存115分享 | `/p115_add_share` |
| 115分享生成STRM | `/p115_share_strm` |
| 磁力离线 / ed2k离线 / 添加离线下载 | `/ol` |
| 115目录生成STRM | `/p115_strm` |
| 搜索指定资源 / 115搜索 | `/sh` |
| HDHive签到 | `/hdhivechin` |
| 115签到 | `/p115_checkin` |

## Guardrails

- Preserve URLs, passwords, hashes, and path arguments exactly.
- Do not invent new commands.
- If the command does not exist, say so briefly.
- For disruptive actions, ask for confirmation unless the user explicitly used
  the exact command.

## Relationship To Other Local Skills

This skill intentionally absorbs the overlapping behavior that used to be split
across multiple local skills. Keep the skill unified here instead of growing
parallel router skills.

If command capabilities change later, update this single file instead of adding
new overlapping router skills.
