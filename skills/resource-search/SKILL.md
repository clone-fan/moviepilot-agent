---
name: resource-search
version: 15
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

1. Resolve media identity once with `search_media`.
2. Present one compact card with source buttons.
3. After the user chooses, go directly to the chosen chain.
4. Do not repeat recognition, card text, or checks unless a tool fails.

## Minimal Recognition

- `search_media` for normal titles.
- `recognize_media` only for filenames, torrent titles, or paths.
- Best candidate first; one fallback if needed.
- No web search for the normal path.

## Parallel Context Gathering

After resolving media identity (TMDB ID, media_type, season), gather library
and subscription state in one parallel batch instead of three serial calls.
This cuts user wait time by roughly 2/3 for the typical resource-search flow.

Use `subagent_task` with `action=run` and three tasks:

1. `media-researcher` — call `query_library_exists` with the resolved
   `tmdb_id` and `media_type`.
2. `subscription-analyst` — call `query_subscribes` with the resolved
   `tmdb_id` and `media_type`.
3. `resource-searcher` — call `query_sites(status="active")` to pre-warm
   site scope for later torrent search.

The main agent reads all three results privately, then synthesizes the card.

**Fallback**: if `subagent_task` fails or returns incomplete results, fall
back to direct tool calls one at a time. Do not block the user on a
subagent infrastructure issue.

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

## Distilled Rules

### Resource Discovery Flow

1. Resolve media identity with `search_media` or `recognize_media`.
2. Check library existence and existing subscriptions when duplication matters.
3. Search resources or route to 115/direct subscription flow as appropriate.
4. Present a compact resource card with quality, size, seeders/site, and the safest next choices.
5. Require explicit confirmation before starting downloads unless the user gave a direct link and explicitly asked to download it.

### Resource Card

- Resolve one best media identity first; do not repeatedly search the same title unless recognition fails.
- Check library/subscription state when it changes the recommendation, but do not turn a quick resource request into a long audit.
- Present a compact card before acquisition: title/year/type/TMDB, library state, and the safest next choices.
- Download is never implicit from search results. If the next step starts a download, use confirmation buttons or ask for explicit consent.

### TV Rule

Never omit season casually. In MoviePilot, TV subscription without season means season 1 only. For multiple seasons, create or search per season.

### No Result / Bad Result

- Re-check recognition and aliases.
- Check enabled site scope and site health when the result depends on trackers.
- Review filters before saying there is no resource.
- Offer subscription when immediate resources are poor but automated monitoring is useful.

#### Resource Availability Discipline

When a candidate skill suggests “get available resources”, map it to MoviePilot resource discovery, not a generic inventory scan:

- resolve media identity first;
- check library/subscription duplication when it affects action;
- inspect site scope/health when tracker results are empty or poor;
- present available choices with source/action boundaries;
- never convert availability into download without explicit confirmation.

### Availability Triage

When judging whether a media resource is available, separate four states instead of saying only “found/not found”:

- **available now**: matched resources exist and can be presented for user choice;
- **available but gated**: resources likely exist, but site scope, auth, filter groups, quality rules, or library duplication affects action;
- **monitor instead**: no good immediate result, but subscription/search-subscribe is useful;
- **blocked**: identity, site health, filter, or permission is unresolved.

For empty or poor results, check the first likely broken boundary: recognition -> library/subscription duplication -> site scope/health -> filters -> acquisition mode. Do not repeat broad searches when one boundary explains the result.

## Verification

- Download chosen resource → query download task.
- Create subscription → query subscription.
- Trigger subscription search → report that the system route has been handed off.

### Completion Checklist

- Search card includes title, year/type, TMDB/Douban identity when available, and existing library/subscription state when checked.
- If routing to 115 or subscription, trigger exactly that route and stop.
- If no resource path is available, report the checked identity and the next useful fallback.