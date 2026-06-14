# MoviePilot CLI Reference

本文件是 `moviepilot-cli` 的低频命令参考。常规媒体任务优先用 MCP 工具和 `SKILL.md` 的路由；只有明确需要 CLI fallback 时再读取这里。

## Discover Commands

```bash
node scripts/mp-cli.js list
node scripts/mp-cli.js show <command>
```

必须先 `show <command>` 再执行命令。

## Command Groups

| Category | Commands |
|---|---|
| Media Search | search_media, recognize_media, query_media_detail, get_recommendations, search_person, search_person_credits |
| Torrent | search_torrents, get_search_results |
| Download | add_download, query_download_tasks, delete_download, query_downloaders |
| Subscription | add_subscribe, query_subscribes, update_subscribe, delete_subscribe, search_subscribe, query_subscribe_history, query_popular_subscribes, query_subscribe_shares |
| Library | query_library_exists, query_library_latest, transfer_file, scrape_metadata, query_transfer_history |
| Files | list_directory, query_directory_settings |
| Sites | query_sites, query_site_userdata, test_site, update_site, update_site_cookie |
| System | query_schedulers, run_scheduler, query_workflows, run_workflow, query_rule_groups, query_episode_schedule, send_message |

## Search and Download Example

### 1. Search TMDB

```bash
node scripts/mp-cli.js search_media title="..." media_type="movie"
```

If the user specifies a TV season, validate the season against TMDB before assuming it matches.

### 2. Search torrents

```bash
node scripts/mp-cli.js search_torrents tmdb_id=791373 media_type="movie"
```

Specific sites require site IDs:

```bash
node scripts/mp-cli.js query_sites
node scripts/mp-cli.js search_torrents tmdb_id=791373 media_type="movie" sites='1,3'
```

When `search_torrents` returns `filter_options`:

1. Stop.
2. Present every filter field/value to the user verbatim.
3. Do not pre-select, summarize, translate, or omit.
4. Wait for user selection or confirmation that no filters are needed.

### 3. Get filtered results

```bash
node scripts/mp-cli.js show get_search_results
node scripts/mp-cli.js get_search_results resolution='1080p,2160p' free_state='免费,50%'
```

Filter logic: OR within a field, AND across fields. `filter_options` keys may be camelCase, but CLI params may be snake_case.

If empty, explain which filter to relax and ask before retrying.

### 4. Present results

Show all results as a numbered list:

- index
- title
- size
- seeders
- resolution
- release group
- `volume_factor`
- `freedate_diff`

## No-Result Fallback

Before concluding unavailable:

- check enabled/search site scope;
- check site health/auth;
- check media recognition and aliases;
- check overly strict filters;
- try one narrower fallback path only, then report blocker.
