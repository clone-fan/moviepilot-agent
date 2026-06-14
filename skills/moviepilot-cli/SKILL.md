---
name: moviepilot-cli
version: 9
description: >-
  Use this skill as the general MoviePilot media-operations fallback for movies,
  TV shows, anime, downloads, subscriptions, library management, sites, and
  files when no narrower MoviePilot skill fits. Do not use it before
  moviepilot-direct-routes for obvious slash-command/direct-link requests,
  resource-search for tracker/resource discovery, moviepilot-api for explicit
  REST API work, moviepilot-update for upgrade/restart/version tasks,
  transfer-failed-retry for failed organization retries, or identifier skills
  for recognition-word/custom-identifier work.
allowed-tools: execute_command subagent_task
---

# MoviePilot CLI

## Purpose

General MoviePilot media-operation fallback when MCP tools or narrower MoviePilot skills do not cover the request clearly.

Prefer current runtime MCP tools first. Use the CLI only when it gives a clearer path, a missing operation, or a command-level fallback.

## Routing Boundary

Use narrower routes first:

- `moviepilot-direct-routes`: slash commands, direct links, obvious command aliases.
- `resource-search`: search/filter tracker resources or choose a source.
- `moviepilot-api`: explicit REST API work or tool coverage gap.
- `moviepilot-update`: version, restart, upgrade.
- `transfer-failed-retry`: failed transfer/organization retry.
- `generate-identifiers` / `media-identifier-rulecraft`: recognition words or custom identifiers.

Use this skill only after that routing check for normal MoviePilot media operations.

## CLI Discipline

Script path is relative to this skill file:

```bash
node scripts/mp-cli.js list
node scripts/mp-cli.js show <command>
```

Rules:

- Always run `show <command>` before command execution; parameter names are not inferable.
- Do not guess parameter names or translate filter values.
- Prefer `tmdb_id`; use `douban_id` only when TMDB is unavailable.
- Omitting `sites=` uses default sites; if user names sites, query site IDs first.

Full command groups and command examples live in `REFERENCES.md`.

## Media Operation Flow

1. **Resolve media identity**
   - Use `search_media` for database lookup.
   - Use `recognize_media` for torrent/file/path parsing.
   - Do not confuse identity recognition with torrent search.
   - **Parallel context pre-fetch**: once TMDB ID and media_type are resolved,
     dispatch library and subscription checks in parallel via `subagent_task`
     instead of serial calls:

     | Check | Subagent | Probe |
     |---|---|---|
     | Library | `media-researcher` | `query_library_exists(tmdb_id, media_type)` |
     | Subscription | `subscription-analyst` | `query_subscribes(tmdb_id, media_type)` |
     | Sites | `resource-searcher` | `query_sites(status="active")` |

     Synthesize results privately before deciding acquisition mode. Fall back
     to direct tool calls if subagent infrastructure fails.

2. **Choose acquisition mode**
   - Immediate acquisition -> search torrents, present results, then confirm before download.
   - Automation -> subscription tools with season/quality/site constraints.
   - Direct link -> direct route skill, not generic CLI.

3. **Search resources**
   - Use `search_torrents` with `tmdb_id` when available.
   - When it returns filter options, stop and let the user choose filters before `get_search_results`.
   - Filter values must come from returned options; OR within one field, AND across fields.

4. **Present results**
   - Numbered list with title, size, seeders, resolution, release group, promotion/free state, and relevant expiry.
   - Do not start downloads without explicit confirmation.

5. **Verify state**
   - Subscription changes -> `query_subscribes`.
   - Download actions -> `query_download_tasks` or history.
   - Transfer actions -> `query_transfer_history` or `query_library_exists`.
   - No-result cases -> check site scope/health, recognition quality, and filters before concluding unavailable.
   - **Parallel post-action verification**: after download or transfer, verify
     download task status and transfer history in one parallel batch via
     `subagent_task` with `download-diagnostician` and `media-researcher`
     instead of two serial queries.

## File and Organization Discipline

- Use dedicated transfer or failed-retry skills before generic file operations.
- Keep source path, target library, media identity, transfer mode, and history state distinct.
- Verify configured directories and source existence before transfer.
- Do not delete, move, or overwrite files without explicit confirmation and post-action state check.
## Media File Inventory Boundary

When a task sounds like file organization or “what is available”, map it to MoviePilot state rather than a generic filesystem inventory:

- **Library availability** -> `query_library_exists` or media-server latest state when identity is known.
- **Downloaded but not organized** -> download tasks/history plus transfer history.
- **Failed organization** -> `transfer-failed-retry`, not manual moving.
- **Unrecognized local files** -> `recognize_media` first, then transfer with explicit identity if needed.
- **Tracker availability** -> `resource-search` / torrent tools, with site health and filters considered.

Keep source path, media identity, downloader task, transfer history, and final library state separate in the explanation.

## Safety

Explicit confirmation is required for:

- downloads;
- deletes;
- scheduler/workflow runs;
- site credential changes;
- plugin installs/uninstalls;
- restarts;
- destructive file operations.

For TV shows, never assume full-series subscription. Omitting season means season 1 only; multi-season subscriptions require explicit per-season handling.

## Handoff

If `/config/agent` capability assets changed during the task, hand off sync reminders to `moviepilot-agent-git-maintenance`.

Completion verification is delegated to `verification-before-completion`.
