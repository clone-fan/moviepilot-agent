---
name: mp-direct-command-router
version: 1
description: >-
  Use this skill when the user asks to bypass AI reasoning for MoviePilot native
  or plugin slash commands that already accomplish the task directly. This skill
  is for requests such as “直接执行内置指令”, “不要查媒体/查库”, “把自然语言转成
  slash command 直接跑”, “遇到能直接完成的 MP 功能就别绕 AI”, and any
  exact slash command or obvious command alias that should be dispatched without
  media search, database lookup, or extra explanation.
allowed-tools: list_slash_commands query_plugin_capabilities run_slash_command
---

# MP Direct Command Router

This is a standalone routing skill. It does not modify official built-in skills.
Its job is to recognize requests that already have a MoviePilot slash-command
path and dispatch them directly.

## Purpose

When the user clearly wants a built-in MoviePilot function or a plugin function
that already exists as a slash command, skip AI reasoning and call the matching
slash command immediately.

Do not:

- search media metadata
- query databases
- inspect libraries
- over-explain the mapping
- add unnecessary confirmation for non-destructive commands

## Core Routing Rule

If the user request can be executed by one existing slash command, translate it
into that command and run it with `run_slash_command`.

If multiple commands could work, prefer the shortest stable command that matches
the request.

## What This Skill Covers

- Exact slash commands from the user
- Obvious command aliases in natural language
- Non-destructive MP operations already exposed as commands
- Plugin commands that can be executed directly
- 115 share/offline/search command routing when the input clearly matches the
  corresponding command surface

## Workflow

### 1. Identify Command Intent

Classify the user message into one of these buckets:

- exact slash command
- simple built-in command intent
- simple plugin command intent
- 115 / magnet / ed2k direct route
- ambiguous request that still needs clarification

### 2. Resolve the Target Command

Use the current command inventory when necessary:

- `list_slash_commands` for all available system + plugin slash commands
- `query_plugin_capabilities` if a plugin’s direct command surface needs
  confirmation

Keep this lightweight. Do not turn a command-routing task into a media search.

### 3. Dispatch Immediately

Once the command is identified:

- preserve the user’s arguments
- preserve URLs exactly
- do not rewrite passwords, query strings, or hash values
- call `run_slash_command`

### 4. Report Minimal Result

After dispatching, give a short confirmation that the command has been sent or
started. Do not add unrelated analysis.

## Supported Fast-Path Patterns

Use direct routing for these common categories:

### System Commands

- `/cookiecloud`
- `/sites`
- `/mediaserver_sync`
- `/subscribes`
- `/downloading`
- `/transfer`
- `/redo`
- `/clear_cache`
- `/restart`
- `/version`
- `/clear_session`
- `/stop_agent`
- `/session_status`
- `/skills`

### Plugin Commands

- `/site_signin`
- `/update_covers`
- `/cd2_restart`
- `/cd2_info`
- `/cd`
- `/p115_full_sync`
- `/p115_inc_sync`
- `/p115_add_share`
- `/p115_share_strm`
- `/ol`
- `/p115_strm`
- `/sh`
- `/hdhivechin`
- `/p115_checkin`

### Natural-Language Aliases

Examples of phrases that should map directly:

- “同步站点” -> `/cookiecloud`
- “站点列表” -> `/sites`
- “查看下载” -> `/downloading`
- “整理下载” -> `/transfer`
- “手动整理 123” -> `/redo 123`
- “清理缓存” -> `/clear_cache`
- “重启系统” -> `/restart`
- “当前版本” -> `/version`
- “查看会话状态” -> `/session_status`
- “管理技能” -> `/skills`
- “站点签到” -> `/site_signin`
- “更新封面” -> `/update_covers`
- “115全量同步” -> `/p115_full_sync`
- “115增量同步” -> `/p115_inc_sync`
- “115转存 https://115.com/s/...” -> `/p115_add_share ...`
- “115分享直接生成STRM ...” -> `/p115_share_strm ...`
- “磁力离线 ...” -> `/ol ...`
- “搜索资源 沙丘2” -> `/sh 沙丘2`
- “HDHive签到” -> `/hdhivechin`
- “115签到” -> `/p115_checkin`

## Guardrails

- Use the exact existing command; do not invent new ones.
- If the user asks for a command that does not exist, say so briefly.
- If the request is destructive or high-impact and not explicitly stated as a
  command, ask for confirmation first.
- If the message is too ambiguous to map safely, ask one short clarification
  question.

## Implementation Notes

This skill is intentionally separate from official MoviePilot skills.
If MoviePilot adds or removes slash commands later, update this skill only.
Do not change official skills to achieve this routing behavior.
