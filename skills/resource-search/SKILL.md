---
name: resource-search
version: 18
description: >-
  MUST-USE when the user asks to search MoviePilot tracker/torrent resources
  for a movie, TV show, anime, or ambiguous title. Do not route through generic
  CLI or API when the user says 搜资源, 搜索资源, 找资源, 查种子, 找种子,
  搜片源, 下载哪个, 资源筛选, 4K资源, 1080p资源, BluRay资源, 搜片. Resolve
  media through the shortest path, present one compact card with buttons, then
  route to 115 search or subscription. This is the primary resource discovery
  skill; do not bypass it with general media tools.
allowed-tools: search_media recognize_media query_library_exists query_subscribes add_subscribe search_subscribe send_message ask_user_choice run_slash_command subagent_task
---

# Resource Search

## HARD GATE

When the user asks to find/search resources for a title, use this skill. Do not
route through general CLI or API. Do not search, download, or subscribe before
the user sees the card and chooses.

**🚫 卡片强制门禁：任何搜片请求，第一步 resolve media identity 后必须立即走 Step 3 发卡片+按钮。禁止在卡片之前输出任何文字结论，包括"媒体库已有""无资源""已订阅"等。卡片是用户看到的第一条回复，不是可选项。**

## Core Flow

### Step 1 — Resolve Media Identity

Use `search_media` for normal titles. Use `recognize_media` only for filenames,
torrent titles, or paths. Best candidate first; one fallback if needed. No web
search for the normal path.

### Step 2 — Parallel Context Gathering

After resolving media identity (TMDB ID, media_type, season), gather library
and subscription state in one parallel batch:

Use `subagent_task` with `action=run` and two tasks:

1. `media-researcher` — call `query_library_exists` with the resolved
   `tmdb_id` and `media_type`.
2. `subscription-analyst` — call `query_subscribes` with the resolved
   `tmdb_id` and `media_type`.

**Fallback**: if `subagent_task` fails or returns incomplete results, fall
back to direct tool calls one at a time. Do not block the user.

### Step 3 — Send Media Info Card (TG 卡片优先)

**🚫 硬规则：禁止跳过卡片直接文字回复！**

无论媒体库状态如何（已入库/未入库/订阅中/无订阅），必须先发卡片+按钮。
任何情况下不得在卡片之前输出纯文字结论。即使媒体库已有、无资源、识别失败，
也要先发卡片（或兜底卡片）再跟按钮。

**常见违规场景（必须杜绝）：**
- ❌ 媒体库已有 → 直接文字说"已经有了不用下" → 跳过卡片
- ❌ 无资源 → 直接文字说"没找到" → 跳过卡片
- ❌ 已订阅 → 直接文字说"已订阅了" → 跳过卡片
- ✅ 正确做法：无论什么状态，先发卡片，再跟按钮让用户选择

Use `send_message` with `image_url` to show poster on top, text below — same
style as MP 入库通知/暂停播放通知.

```
send_message(
  title="🎬 标题 (年份)",
  image_url="https://image.tmdb.org/t/p/original/{poster_path}",
  message="⭐ 评分：X.X\n\n📖 剧情简介：\n{完整简介}\n\n🔗 TMDB：https://www.themoviedb.org/{type}/{tmdb_id}\n\n📌 当前状态：媒体库已入库/未入库 · 订阅中/无订阅 · 站点有资源/暂无资源"
)
```

### Step 4 — Action Buttons

Use `ask_user_choice` with these options:

- **搜索资源** → go to Step 5
- **添加订阅** → call `add_subscribe` with TMDB ID and confirmed season
- **换一部电影** → ask user for new title, restart from Step 1
- **不用了** → done

### Step 5 — Resource Search (only after user chooses)

Call `search_torrents` with the resolved TMDB ID and media_type. Present
results with quality, size, seeders/site. Require explicit confirmation before
starting downloads unless the user gave a direct link and explicitly asked to
download it.

## TV Rule

Never omit season casually. In MoviePilot, TV subscription without season means
season 1 only. For multiple seasons, create or search per season.

## No Result / Bad Result

- Re-check recognition and aliases.
- Check enabled site scope and site health when the result depends on trackers.
- Review filters before saying there is no resource.
- Offer subscription when immediate resources are poor but automated monitoring
  is useful.

### Availability Triage

Separate four states instead of saying only "found/not found":

- **available now**: matched resources exist and can be presented for user choice;
- **available but gated**: resources likely exist, but site scope, auth, filter
  groups, quality rules, or library duplication affects action;
- **monitor instead**: no good immediate result, but subscription/search-subscribe
  is useful;
- **blocked**: identity, site health, filter, or permission is unresolved.

For empty or poor results, check the first likely broken boundary: recognition
-> library/subscription duplication -> site scope/health -> filters ->
acquisition mode. Do not repeat broad searches when one boundary explains the
result.

## Verification

- Download chosen resource → query download task.
- Create subscription → query subscription.
- Trigger subscription search → report that the system route has been handed off.

### Completion Checklist

- Media info card sent via `send_message` with `image_url` (poster on top, text below).
- Action buttons presented via `ask_user_choice` after the card.
- If routing to 115 or subscription, trigger exactly that route and stop.
- If no resource path is available, report the checked identity and the next
  useful fallback.