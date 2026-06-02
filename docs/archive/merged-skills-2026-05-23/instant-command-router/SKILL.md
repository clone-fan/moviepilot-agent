---
name: instant-command-router
version: 2
description: >-
  Use this skill as the first, low-token dispatch layer for MoviePilot built-in
  slash commands and plugin slash commands that do not need AI reasoning. When
  the user sends an exact slash command, a known short natural-language command,
  a 115 share link, magnet/ed2k link, or a simple request matching current MP
  command capabilities, execute the matching command directly via
  run_slash_command without database/media reasoning, site checks, or extra
  explanation. Covers /cookiecloud, /sites, /mediaserver_sync, /subscribes,
  /downloading, /transfer, /redo, /clear_cache, /restart, /version,
  /clear_session, /stop_agent, /session_status, /skills, /site_signin,
  /update_covers, /cd2_restart, /cd2_info, /cd, /p115_full_sync,
  /p115_inc_sync, /p115_add_share, /p115_share_strm, /ol, /p115_strm, /sh,
  /hdhivechin, and /p115_checkin.
allowed-tools: run_slash_command list_slash_commands query_plugin_capabilities
---

# Instant Command Router

This skill is the fast path for functions that MoviePilot or installed plugins
already expose as slash commands. Its job is to preserve the original command
chain even when the AI agent globally receives user messages.

## Core Principle

If the user's intent maps cleanly to an existing slash command, run that command
directly with `run_slash_command`.

Do not spend tokens on media search, site inspection, plugin analysis, database
queries, or long explanations for these cases. The command itself is the product
feature.

## Dispatch Priority

Apply this skill before heavier skills such as `moviepilot-cli`,
`resource-search`, `p115-resource-workflow`, and `command-dispatch` when the
request is one of the known simple command intents below.

Priority order:

1. Exact slash command from user: execute as-is.
2. Direct resource/link routing: 115 share, magnet, ed2k, or `/sh` style search.
3. Known natural-language aliases in this file.
4. If no alias matches, fall back to `command-dispatch` or other domain skills.

## Exact Slash Commands

When the message starts with `/`, run it directly unless it is clearly malformed.
Examples:

- `/sites`
- `/downloading`
- `/sh 沙丘2`
- `/p115_add_share https://115cdn.com/s/...`
- `/ol magnet:?xt=...`

Use:

```text
run_slash_command(command=<the original message>)
```

## Link Fast Path

### 115 Share Links

Triggers:

- Text contains `115cdn.com/s/`
- Text contains `115.com/s/`

Default command:

```text
/p115_add_share <full link and access-code/password text if present>
```

If the user explicitly says `生成STRM`, `直生STRM`, `分享转STRM`, or
`share strm`, use:

```text
/p115_share_strm <full link and access-code/password text if present>
```

Never route 115 share links to `/ol`.

### Magnet / ed2k Links

Triggers:

- Text contains `magnet:?`
- Text contains `ed2k://`

Command:

```text
/ol <full magnet or ed2k link>
```

For ed2k links, preserve the complete link including trailing `|/` when present.

### 115 Resource Search

Triggers:

- `115搜 <keyword>`
- `115搜索 <keyword>`
- `搜115 <keyword>`
- `网盘搜 <keyword>`
- `资源搜索 <keyword>` when the wording clearly refers to 115/P115
- `搜索资源 <keyword>` when the user previously requested the 115 resource workflow

Command:

```text
/sh <keyword>
```

## Natural-Language Alias Table

Match these aliases case-insensitively where applicable. Execute the target
command directly.

| User intent / aliases | Command |
|---|---|
| 同步站点, 更新站点, CookieCloud, cookiecloud, 同步cookie | `/cookiecloud` |
| 管理站点, 站点列表, 打开站点管理, 查看站点 | `/sites` |
| 同步媒体服务器, 同步媒体库, 刷新媒体库, mediaserver sync | `/mediaserver_sync` |
| 管理订阅, 订阅列表, 查看订阅 | `/subscribes` |
| 正在下载, 下载中, 查看下载, 下载状态 | `/downloading` |
| 整理下载, 下载文件整理, 手动转移全部, 触发整理 | `/transfer` |
| 手动整理, 重新整理, redo | `/redo` plus any provided history id/path argument |
| 清理缓存, clear cache | `/clear_cache` |
| 重启系统, 重启MP, 重启MoviePilot, restart | `/restart` |
| 当前版本, 查看版本, version | `/version` |
| 清除会话, 清空会话, clear session | `/clear_session` |
| 停止推理, 停止AI, stop agent | `/stop_agent` |
| 会话状态, session status | `/session_status` |
| 管理技能, 技能列表, 查看技能 | `/skills` |
| 站点签到, 手动签到, 签到站点 | `/site_signin` |
| 更新封面, 刷新封面, 更新媒体库封面 | `/update_covers` |
| 重启CloudDrive2, 重启CD2, cd2重启 | `/cd2_restart` |
| CloudDrive2信息, CD2信息, cd2状态 | `/cd2_info` |
| 云下载, clouddrive下载 | `/cd` plus any provided link/path argument |
| 115全量同步, 全量同步115, 115 full sync | `/p115_full_sync` |
| 115增量同步, 增量同步115, 刷新115 STRM, 115 inc sync | `/p115_inc_sync` |
| 115转存, 转存115, 保存115分享 | `/p115_add_share` plus provided share link |
| 115分享生成STRM, 分享直生STRM, 115转STRM | `/p115_share_strm` plus provided share link |
| 115离线, 磁力离线, ed2k离线, 添加离线下载 | `/ol` plus provided link |
| 115目录生成STRM, 指定目录生成STRM | `/p115_strm` plus provided path/argument |
| 搜索指定资源, 115搜索, 115搜, 网盘搜 | `/sh` plus keyword |
| HDHive签到, hdhive签到 | `/hdhivechin` |
| 115签到, 手动115签到 | `/p115_checkin` |

## Additional Gap Coverage

The command surface is now broader than the first draft. Keep these extra cases
in the fast path instead of falling back to slower AI reasoning:

- `/cookiecloud` for站点同步类表述。
- `/mediaserver_sync` when the user asks to resync the media server or library.
- `/sites` for site management and site list viewing.
- `/subscribes` for subscription management/listing.
- `/clear_cache` and `/clear_session` when the user explicitly requests cleanup.
- `/version`, `/session_status`, `/skills`, `/cd2_info` as read/status commands.
- `/p115_full_sync` and `/p115_inc_sync` when the user explicitly asks to sync
  115 data or refresh STRM state.
- `/p115_strm` when the user asks to generate STRM from a known 115 directory.
- `/update_covers` for media cover refresh.
- `/hdhivechin` and `/p115_checkin` for manual check-in requests.

## Argument Handling

1. Preserve user-provided arguments after the trigger phrase.
2. Do not translate or rewrite URLs.
3. Do not strip query strings such as `?password=xxxx`.
4. For `/redo`, preserve numeric IDs or path-like arguments.
5. If a command requires an argument and none is present, ask one concise
   question instead of running an incomplete command.

## Safety Rules

Run directly without confirmation:

- read/list/status commands such as `/sites`, `/downloading`, `/version`,
  `/session_status`, `/skills`, `/cd2_info`
- sync/refresh commands explicitly requested by the user
- `/sh`, `/p115_add_share`, `/p115_share_strm`, `/ol` when the user supplies the
  relevant link or keyword
- check-in commands explicitly requested by the user

Ask for confirmation before dispatching if the user did not use the exact slash
command and the action is disruptive:

- `/restart`
- `/clear_cache`
- `/clear_session`
- `/stop_agent`
- `/p115_full_sync` if the wording is vague

If the user sends the exact slash command, respect it and dispatch directly.

## Validation and Drift Handling

This skill reflects the command surface observed on 2026-05-23. If a command
fails because it no longer exists, call `list_slash_commands` once, refresh the
mapping mentally for the current turn, then retry only if an obvious replacement
exists.

When plugins are installed/removed or commands change, update this skill file so
future turns can dispatch without listing commands first.
