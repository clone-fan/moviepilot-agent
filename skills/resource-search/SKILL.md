---
name: resource-search
version: 9
description: >-
  Use this skill when the user asks to search MoviePilot tracker/torrent
  resources for a movie, TV show, anime, or ambiguous title. Resolve the media
  through the shortest MoviePilot-native path, present a compact poster-card
  source choice, then route 115 search or MoviePilot subscription directly via
  internal chains. Trigger phrases include 搜资源, 搜索资源, 找资源, 查种子,
  找种子, 搜片源, 下载哪个, 资源筛选, 4K资源, 1080p资源, BluRay资源, 搜片.
allowed-tools: search_media recognize_media query_library_exists query_subscribes add_subscribe search_subscribe send_message ask_user_choice run_slash_command
---

# Resource Search

## Goal

Use the nearest, straightest, lowest-token MoviePilot-native path for resource discovery:

1. Resolve media identity once.
2. Show one compact poster-card source choice.
3. After the user chooses, go directly to the chosen internal chain.
4. Do not repeat recognition, card text, library checks, site checks, or explanations unless a tool fails.

PT manual torrent search is no longer the default user-facing second branch. Replace it with **MoviePilot subscription**, because subscription uses MP's internal search/download/update chain and is more stable for ongoing acquisition.

## Minimal Recognition Path

Before tools, infer the best canonical title internally. Keep this private.

- Use `search_media` for normal titles.
- Use `recognize_media` only for filenames, torrent titles, or paths.
- Try the best candidate first; only try one fallback candidate if the first one fails.
- Do not use web search for the normal path.
- Cache the resolved `{title, year, media_type, season, tmdb_id, douban_id, poster_path}` in the conversation context for the next user choice.

## First Response Path

1. `search_media(best_candidate)`.
2. Choose the best result.
3. `query_library_exists` once for status. If it fails, mark `入库：未知` and continue.
4. Send the source choice card.
5. Stop and wait for the user's choice.

Do not call `/sh`, `add_subscribe`, `search_subscribe`, site checks, detail queries, or download tools before the user chooses a branch.

## Source Choice Card Template

Target UX: **poster image + compact media card + source buttons in the same interaction**.

```text
[poster]
《标题》（年份）
类型：电影/电视剧｜评分：评分｜TMDB：ID
入库：已入库/未入库/未知
简介：一句话，≤80字
[按钮：115资源] [按钮：订阅]
```

### Current Tool Fallback Template

If the current channel/tool cannot send image and buttons in one call, use this fixed two-call fallback:

1. `send_message(image_url=poster_path, title="《标题》资源搜索", message=<compact card text>)`
2. `ask_user_choice(title="选择获取方式", message="请选择获取方式：", options=[115资源, 订阅])`

Rules for the fallback:

- The first call carries poster + compact card.
- The second call carries buttons only.
- Never repeat title/year/summary/library status in the second call.
- Do not apologize or explain tool limitations unless the user asks.

## Compact Card Text

```text
《标题》（年份）
类型：电影/电视剧｜评分：评分｜TMDB：ID
入库：已入库/未入库/未知
简介：一句话，≤80字
```

Keep it short. No separate `需要搜索：1/2` line when buttons exist.

## After User Chooses

Use the cached media identity from the immediately preceding card. Do not re-run media search.

Once the user chooses a branch, the agent should hand off to MoviePilot's system chain and stop with the smallest possible confirmation. Do not keep supervising the chain unless the user asks for status, failure handling, or immediate missing-resource search.

### 115资源

Fire-and-stop path:

1. Run `run_slash_command` with `/sh <resolved Chinese title>`.
2. Stop after the tool result.
3. Final reply is one short sentence: `已触发 115 搜索：<关键词>`.

Do not query subscription, sites, library, download tasks, plugin data, or wait for 115 search results. The plugin/system chain owns the follow-up.

### 订阅

Fire-and-stop path:

1. Run `query_subscribes(tmdb_id/douban_id, media_type)` only to avoid duplicate subscription.
2. If no active duplicate exists, run `add_subscribe` with the cached identity.
3. Stop after `add_subscribe` returns success.
4. Final reply is one short sentence: `已订阅：<标题>（<年份>）`.

Defaults:

- Movie: subscribe once.
- TV/anime: if the card resolved a season, use it; otherwise default to season 1. Do not call `query_media_detail` just to learn episode count unless required by the tool or the user explicitly asks for season/episode precision.
- Let MoviePilot auto-detect total episodes when possible; do not query details only for a prettier confirmation.

Do not call `query_subscribes` again after adding, do not call `search_subscribe`, and do not inspect download/library/status unless the user explicitly asks.

Do not run manual PT tools in this branch.

## Failure Handling

- Recognition failed: say internal recognition failed and offer 115 keyword fallback or a more exact title.
- 115 command failed: report command failure only; do not switch to subscription automatically.
- Subscription already exists: report existing subscription; do not add a duplicate.
- Subscription add failed: report the failure and the cached media identity used.
- Download still requires explicit user confirmation unless the user already provided a direct link and asked to download.
