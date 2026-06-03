---
name: moviepilot-cli
version: 2
description: >-
  Use this skill as the general MoviePilot media-operations fallback for movies,
  TV shows, anime, downloads, subscriptions, library management, sites, and
  files when no narrower MoviePilot skill fits. Do not use it before
  moviepilot-direct-routes for obvious slash-command/direct-link requests,
  resource-search for tracker/resource discovery, moviepilot-api for explicit
  REST API work, moviepilot-update for upgrade/restart/version tasks,
  transfer-failed-retry for failed organization retries, or identifier skills
  for recognition-word/custom-identifier work.
---

# MoviePilot CLI

> All script paths are relative to this skill file.

Use `scripts/mp-cli.js` to interact with the MoviePilot backend.

## Routing Boundary

This is the broad MoviePilot media-operation fallback, not the first skill for
every mention of MoviePilot.

Prefer narrower skills first:

- `moviepilot-direct-routes`: exact slash commands, direct links, obvious command aliases.
- `resource-search`: user asks to search/filter resources or pick a source.
- `moviepilot-api`: user explicitly asks for REST API or CLI/MCP cannot cover an operation.
- `moviepilot-update`: version, restart, upgrade.
- `transfer-failed-retry`: retry failed transfer/organization records.
- `generate-identifiers` / `media-identifier-rulecraft`: custom identifiers or recognition fixes.

Use this skill after that routing check for normal MoviePilot media operations.

## Discover Commands

List all available commands: `node scripts/mp-cli.js list`

Show parameters and usage for a specific command: `node scripts/mp-cli.js show <command>`

Always run `show <command>` before calling a command — parameter names are not inferable, do not guess.

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

## Workflows

### Search and Download

#### 1. Search TMDB

Search for a movie or TV show by title: 
`node scripts/mp-cli.js search_media title="..." media_type="movie"`

If the user specifies a TV season, run Season Validation step first — the season number provided by the user may not match TMDB.

#### 2. Search torrents

Prefer `tmdb_id`; use `douban_id` only when `tmdb_id` is unavailable.

Omitting `sites=` uses the user's default sites. If the user specifies sites, first retrieve site IDs:
`node scripts/mp-cli.js query_sites`

Search torrents using default sites:
`node scripts/mp-cli.js search_torrents tmdb_id=791373 media_type="movie"`

Search torrents using user-specified sites (pass site IDs from `query_sites`):
`node scripts/mp-cli.js search_torrents tmdb_id=791373 media_type="movie" sites='1,3'`

When `search_torrents` returns:
1. **Stop** — do not call `get_search_results` yet.
2. Present all `filter_options` fields and every value within each field to the user verbatim.
3. Do not pre-select, summarize, or omit any field or value.
4. Wait for the user to select filters or confirm no filters are needed before moving to the next step.

#### 3. Get filtered results (only after user has responded to filter_options)

Run `node scripts/mp-cli.js show get_search_results` to check available parameters. Filter logic: OR within a field, AND across fields.

Filter values must come from the `filter_options` returned by `search_torrents` — do not invent, translate, normalize, or use values from any other source. Note: `filter_options` keys are camelCase (e.g., `freeState`), but `get_search_results` params are snake_case (e.g., `free_state`).

Fetch results with selected filters:
`node scripts/mp-cli.js get_search_results resolution='1080p,2160p' free_state='免费,50%'`

If empty, tell the user which filter to relax and ask before retrying.

#### 4. Present results as a numbered list

Show all results without pre-selection. Each row: index, title, size, seeders, resolution, release group, `volume_factor`, `freedate_diff`.
