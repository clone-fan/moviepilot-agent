---
name: p115-resource-workflow
version: 1
description: >-
  Use this skill when the user asks to search resources with 115/P115StrmHelper,
  search specified resources, handle Telegram resource cards, transfer/save 115
  share links, add 115 offline download tasks, or route magnet/ed2k/115 links.
  Trigger phrases include 搜索资源, 资源搜索, 115搜索, 115转存, 转存115, 115分享,
  115离线, 磁力离线, ed2k离线, /sh, /p115_add_share, /p115_share_strm, /ol.
allowed-tools: list_slash_commands query_plugin_capabilities run_slash_command browse_webpage search_web execute_command read_file
---

# P115 Resource Workflow

This skill restores the user's 115 resource search and transfer workflow around
MoviePilot's `P115StrmHelper` plugin.

## Purpose

Handle three closely related operations:

1. Search resources through P115StrmHelper.
2. Route discovered links to the correct 115 command.
3. Parse Telegram/resource-card text quickly enough to extract the real link and
   submit it without unnecessary detours.

## Required Command Surface

Before using plugin commands for the first time in a session, confirm the command
is registered when needed with `list_slash_commands` or
`query_plugin_capabilities`.

Expected P115StrmHelper commands:

- `/sh <keyword>`: search specified resource.
- `/p115_add_share <115 share link>`: transfer/save 115 share to the pending
  organize directory.
- `/p115_share_strm <115 share link>`: generate STRM interactively from a 115
  share link; use only when the user explicitly asks for share-to-STRM.
- `/ol <magnet|ed2k|direct offline link>`: add 115 offline download task.
- `/p115_inc_sync`: incremental sync after transfer/offline completion when the
  user asks to refresh STRM/library.
- `/p115_full_sync`: full sync only when explicitly requested or when incremental
  sync is insufficient.

## Link Routing Rules

Always classify the input before acting:

1. `https://115.com/s/...` or `https://115cdn.com/s/...` is a 115 share link.
   - Default command: `/p115_add_share <link>`.
   - If the user says direct STRM / 分享直生STRM / 生成STRM, use
     `/p115_share_strm <link>` instead.
2. `magnet:?...`, `ed2k://...`, or a clear offline-download direct link is an
   offline task.
   - Command: `/ol <link>`.
3. A plain title or keyword such as `搜 XXX`, `搜索资源 XXX`, `115搜 XXX` is a
   resource-search request.
   - Command: `/sh <keyword>`.
4. Do not send 115 share links to `/ol`.
5. Do not send magnet/ed2k links to `/p115_add_share`.
6. If the type is still ambiguous after lightweight parsing, ask one focused
   question instead of guessing.

## Resource Search Workflow

Use this when the user asks to search resources but has not provided a concrete
115/magnet/ed2k link.

1. Extract the search keyword from the user text.
   - Keep season/episode, year, resolution, and subtitle requirements when they
     are part of the query.
   - Remove trigger words such as `搜索资源`, `搜一下`, `115搜`, `帮我找`.
2. Confirm `/sh` exists if command capability is not already known.
3. Run `run_slash_command` with `/sh <keyword>`.
4. Treat successful command dispatch as submitted. The plugin may return results
   asynchronously through the chat channel.
5. If `/sh` is unavailable, fall back to MoviePilot torrent search only when the
   user's intent can accept tracker resources; otherwise report that
   P115StrmHelper search is unavailable.

Examples:

- `搜索资源 庆余年 第二季 2160p` -> `/sh 庆余年 第二季 2160p`
- `115搜 攻壳机动队 SAC` -> `/sh 攻壳机动队 SAC`
- `/sh 沙丘2` -> pass through as `/sh 沙丘2`

## 115 Share Transfer Workflow

Use this when the user provides a 115 share link or asks to transfer/save to 115.

1. Extract the first real 115 share URL from the message.
2. Preserve access code/password text if it is part of the URL or appears right
   after the link.
3. Unless the user explicitly asks for STRM generation, run:
   `/p115_add_share <link>`.
4. If the user explicitly asks for share-to-STRM, run:
   `/p115_share_strm <link>`.
5. Do not open or validate the share page before dispatch unless the command
   fails or the link is incomplete.

Examples:

- `https://115cdn.com/s/xxxxx?password=abcd` -> `/p115_add_share ...`
- `这个115分享直接生成STRM https://115.com/s/xxxxx` -> `/p115_share_strm ...`

## Offline Download Workflow

Use this when the user provides magnet, ed2k, or another offline-download link.

1. Extract the full link. For ed2k, keep the complete trailing `|/` when present.
2. Run `/ol <link>`.
3. If a later notification says media recognition failed, do not treat that as
   offline submission failure; it only means the file may need manual recognize
   or organize later.

Examples:

- `magnet:?xt=urn:btih:...` -> `/ol magnet:?xt=urn:btih:...`
- `ed2k://|file|xxx.mkv|123|HASH|/` -> `/ol ed2k://|file|xxx.mkv|123|HASH|/`

## Telegram / Card Parsing Rules

When the user forwards a resource card or text block:

1. First scan the visible text for real resource links:
   - `115cdn.com/s/`
   - `115.com/s/`
   - `magnet:?`
   - `ed2k://`
2. If found, route immediately using the rules above. Do not open the page.
3. If the text contains `链接：点击跳转(<real link>)`, extract the link inside
   parentheses.
4. If the card only contains a `查看资源` / `telegra.ph` link, fetch the page.
   - Prefer the same path on `te.legra.ph` if normal `telegra.ph` is unreliable.
   - Extract only real resource links; ignore ads, groups, bots, channels,
     airports, public Emby, and VIP/payment entrances.
5. If the page points to a text list such as `files.catbox.moe/*.txt`, fetch the
   text list and extract real links from it.
6. If multiple cloud links are present, prefer 115 for this workflow; keep other
   links only as fallback information.

## Safety and Confirmation

- Searching with `/sh` is non-destructive and can be run directly.
- Transferring a 115 share with `/p115_add_share` is considered the requested
  action when the user sends a 115 link; run directly unless the text suggests
  they only wanted analysis.
- Adding `/ol` offline tasks is considered the requested action when the user
  sends magnet/ed2k in a 115 context; run directly.
- If the user asks to delete, clean, overwrite, or full-sync large directories,
  ask for confirmation unless they explicitly used the exact command.

## Troubleshooting

If command dispatch fails or no response appears:

1. Confirm P115StrmHelper is installed/running with `query_plugin_capabilities`.
2. Confirm the slash command exists with `list_slash_commands`.
3. Check `/config/logs/moviepilot.log` and any P115StrmHelper log for the last
   error.
4. For share transfer failures, check link completeness and password/access code.
5. For offline failures, check magnet/ed2k format and whether the link was
   truncated by the chat client.

## Related Local Docs

Use these docs as detailed references when the workflow is unclear:

- `/config/agent/docs/p115-routing.md`
- `/config/agent/docs/p115-share.md`
- `/config/agent/docs/p115-offline.md`
- `/config/agent/docs/tg-card-parsing.md`
