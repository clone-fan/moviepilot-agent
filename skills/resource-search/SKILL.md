---
name: resource-search
version: 19
description: >-
  MUST-USE when the user asks to search MoviePilot tracker/torrent resources
  for a movie, TV show, anime, or ambiguous title. Trigger for: 搜资源, 搜索资源,
  找资源, 查种子, 找种子, 搜片源, 下载哪个, 资源筛选, 4K资源, 1080p资源, BluRay资源,
  搜片, 搜[片名], 找[片名], 查[片名]. Resolve media through the shortest path,
  present one compact card with buttons first, then route to resource search,
  115 search, or subscription based on user choice. This is the primary resource
  discovery skill; do not bypass it with direct search_media + text reply.
allowed-tools: search_media recognize_media query_library_exists query_subscribes add_subscribe search_subscribe send_message ask_user_choice run_slash_command subagent_task search_torrents
---

# Resource Search

## Trigger Recognition

**Use this skill when the user's request matches any of:**
- Explicit resource keywords: 搜资源, 找资源, 查种子, 找种子, 搜片源, 资源筛选, 下载哪个
- Short search patterns: 搜[片名], 找[片名], 查[片名], 搜片
- Quality-specific: 4K资源, 1080p资源, BluRay资源, WEB-DL资源
- Ambiguous media questions where user likely wants to see options before deciding

**Do NOT use when:**
- User only asks for media info/details without download/subscription intent
- User explicitly says "只看信息" or "不下载"
- Request is clearly about library status check only

## HARD GATE: Card-First Rule

**🚫 卡片强制门禁（不可绕过）：**

任何触发 resource-search 的请求，完成 Step 1 media identity resolution 后，
**必须立即**执行 Step 2 并行查询 → Step 3 发送卡片 → Step 4 发送按钮。

**禁止在卡片之前输出任何文字结论**，包括但不限于：
- "媒体库已有，不用下载"
- "无资源"
- "已订阅"
- "找到了 XXX"
- 任何形式的状态说明

**卡片是用户看到的第一条回复内容，不是可选项。**

## Core Flow

### Step 1 — Resolve Media Identity

Use `search_media` for normal titles. Use `recognize_media` only for filenames,
torrent titles, or paths.

**Output requirement:** Obtain best candidate with TMDB ID, media_type, year,
title. One fallback attempt if first result is clearly wrong. No web search
for normal path.

**Immediately proceed to Step 2 after resolution. Do not output text conclusion.**

### Step 2 — Parallel Context Gathering

After resolving media identity (TMDB ID, media_type, season), **immediately**
gather library and subscription state in one parallel batch:

Use `subagent_task` with `action=run` and two tasks:

1. `media-researcher` — call `query_library_exists` with resolved `tmdb_id`
   and `media_type`.
2. `subscription-analyst` — call `query_subscribes` with resolved `tmdb_id`.

**Fallback**: if `subagent_task` fails, fall back to direct tool calls
(`query_library_exists` + `query_subscribes`) one at a time.

**Do not block the user. Do not output text. Proceed to Step 3.**

### Step 3 — Send Media Info Card (Mandatory)

**🚫 硬规则：无论查询结果如何，必须发卡片。**

Use `send_message` with `image_url` (poster on top) + text below, matching
MP 入库通知 / 暂停播放通知 style.

**Format:**
```
send_message(
  title="🎬 标题 (年份)",
  image_url="https://image.tmdb.org/t/p/original/{poster_path}",
  message="⭐ 评分：X.X/10\n\n📖 剧情简介：\n{完整剧情简介，不截断}\n\n🔗 TMDB：https://www.themoviedb.org/{type}/{tmdb_id}\n\n📌 当前状态：{库存状态} · {订阅状态} · {资源预判}"
)
```

**状态说明示例：**
- 库存状态: `媒体库已入库` / `媒体库未入库`
- 订阅状态: `订阅中` / `无订阅`
- 资源预判: `待搜索站点资源` / `站点暂无资源` / `资源丰富`

**常见违规场景（必须杜绝）：**
- ❌ 媒体库已有 → 跳过卡片 → 直接文字说"已经有了"
- ❌ 无资源 → 跳过卡片 → 直接文字说"没找到"
- ❌ 已订阅 → 跳过卡片 → 直接文字说"已在订阅"
- ✅ 正确: 先发卡片，状态写在卡片里，再跟按钮

**After sending card, immediately proceed to Step 4. Do not wait. Do not output text.**

### Step 4 — Action Buttons (Mandatory)

Use `ask_user_choice` immediately after card with these options:

```
options = [
  {"label": "🔍 搜索资源", "value": "搜索《{标题}》({年份})的站点资源"},
  {"label": "📌 添加订阅", "value": "订阅《{标题}》({年份})"},
  {"label": "🎬 换一部", "value": "换一部电影"},
  {"label": "❌ 不用了", "value": "取消操作"}
]
```

**This is the last step of the initial flow. Stop here. Wait for user choice.**

### Step 5 — Resource Search (Only After User Chooses "搜索资源")

When user clicks "搜索资源" button:

1. Call `search_torrents` with resolved `tmdb_id` and `media_type`
2. Present results with: quality, size, seeders, site, free state
3. Use `ask_user_choice` to let user pick specific torrent or "全部下载"
4. Require explicit confirmation before calling `add_download_tasks`

**Exception:** if user originally provided a direct magnet/ed2k/115 link and
explicitly said "下载", skip confirmation.

### Step 6 — Subscription (Only After User Chooses "添加订阅")

When user clicks "添加订阅" button:

1. For movies: call `add_subscribe` with `tmdb_id`, `year`, `media_type=movie`
2. For TV: confirm season first (use `query_media_detail` if needed), then
   call `add_subscribe` per season
3. After successful subscription, call `query_subscribes` to verify

**TV rule reminder:** In MoviePilot, omitting `season` means season 1 only.
For multi-season or full-series subscription, call `add_subscribe` separately
for each season.

## No Result / Bad Result

If `search_media` returns empty or clearly wrong result:
- Try one fallback with alias or alternative keyword
- If still empty, send a fallback card with best-effort info + buttons:
  - "换个关键词重搜"
  - "取消"

If `search_torrents` returns empty:
- Check enabled site scope and site health
- Review filter groups
- Suggest subscription instead ("资源暂无，建议订阅后自动监控")

### Availability Triage

Separate four states instead of binary "found/not found":

- **available now**: matched resources exist, can present for user choice
- **available but gated**: resources likely exist, but site scope, auth,
  filters, or library duplication blocks action
- **monitor instead**: no good immediate result, subscription is useful
- **blocked**: identity unclear, site down, filter too strict, or permission issue

For empty or poor results, check the first likely boundary:
recognition → library/subscription duplication → site scope/health → filters →
acquisition mode.

Do not repeat broad searches when one boundary explains the result.

## Verification

After user action:
- Download chosen resource → call `query_download_tasks` to verify task created
- Create subscription → call `query_subscribes` to verify subscription active
- Trigger subscription search → report handoff, no further verification needed

## Completion Checklist

**Minimum required steps for every resource-search invocation:**
- ✅ Media identity resolved (`search_media` or `recognize_media`)
- ✅ Library + subscription context gathered (parallel or fallback)
- ✅ Media info card sent via `send_message` with `image_url` (poster on top)
- ✅ Action buttons sent via `ask_user_choice` immediately after card
- ✅ Stop and wait for user choice

**After user choice:**
- If "搜索资源" → execute Step 5
- If "添加订阅" → execute Step 6
- If "换一部" → ask for new title, restart from Step 1
- If "不用了" → done

**If routing to 115 search or other plugin command:**
- Call `run_slash_command` with appropriate command
- Report handoff, stop

**Never:**
- Skip card and reply with text conclusion
- Output text between card and buttons
- Proceed to resource search without user choosing button