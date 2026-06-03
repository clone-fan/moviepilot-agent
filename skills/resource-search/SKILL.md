---
name: resource-search
version: 10
description: >-
  MUST-USE when the user asks to search MoviePilot tracker/torrent resources
  for a movie, TV show, anime, or ambiguous title. Do not route through generic
  CLI or API when the user says 搜资源, 搜索资源, 找资源, 查种子, 找种子,
  搜片源, 下载哪个, 资源筛选, 4K资源, 1080p资源, BluRay资源, 搜片. Resolve
  media through the shortest path, present one compact card with buttons, then
  route to 115 search or subscription. This is the primary resource discovery
  skill; do not bypass it with general media tools.
allowed-tools: search_media recognize_media query_library_exists query_subscribes add_subscribe search_subscribe send_message ask_user_choice run_slash_command
---

# Resource Search

## HARD GATE

When the user asks to find/search resources for a title, use this skill. Do not
route through general CLI or API. Do not search, download, or subscribe before
the user sees the card and chooses.

1. Resolve media identity once with `search_media`.
2. Present one compact card with source buttons.
3. After the user chooses, go directly to the chosen chain.
4. Do not repeat recognition, card text, or checks unless a tool fails.

## Minimal Recognition

- `search_media` for normal titles.
- `recognize_media` only for filenames, torrent titles, or paths.
- Best candidate first; one fallback if needed.
- No web search for the normal path.

## Source Choice Card

```text
[poster]
《标题》（年份）
类型：电影/电视剧｜评分：X｜TMDB：ID
入库：已入库/未入库/未知
简介：一句话，≤80字
[按钮：115资源] [按钮：订阅]
```

## After Choice

- 115资源 → trigger `/sh` or 115 search route.
- 订阅 → `add_subscribe` with TMDB ID and confirmed season.
- Stop and wait for the user's choice. Do not pre-download or pre-subscribe.

## Final Rule

**When the user asks for resources, use this skill. This is not optional.**