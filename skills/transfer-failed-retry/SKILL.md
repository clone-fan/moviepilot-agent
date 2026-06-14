---
name: transfer-failed-retry
version: 4
description: Use this skill when you need to retry failed file transfers/organizations. Given one or more failed transfer history record IDs, this skill guides you through querying the failure details, deleting the old records, and re-identifying and re-organizing the files. Supports batch processing multiple files from the same media.
allowed-tools: query_transfer_history delete_transfer_history recognize_media transfer_file search_media subagent_task
---

# Transfer Failed Retry

## Purpose

Retry failed MoviePilot file transfers safely. The goal is to inspect failure history, confirm whether retry is safe, remove stale failed records when authorized, and re-transfer with better media identity.

## Safety Gate

Deleting a failed transfer history record is required before retry, but it is still a destructive database action.

- If the user explicitly requested retry for specific history IDs, proceed with the smallest correct batch.
- If IDs or scope are unclear, query failed history first and ask for confirmation before deleting.
- Never delete records just because failures exist.

## Workflow

1. **Query failed records**
   - Use `query_transfer_history(status="failed")`.
   - Extract: id, source path, title, error message, type, TMDB ID, season/episode, downloader, hash.

2. **Analyze blocker**
   - `未识别到媒体信息`: recognize path, then search media if needed.
   - `源目录不存在`: skip; source is gone.
   - `目标路径不存在` or file operation failure: retry may work if config was fixed.
   - `文件已存在`: report duplicate/overwrite blocker.
   - `未找到有效的集数信息`: recognize path or retry with explicit TMDB/season.
   - `未获取到转移目录设置`: stop and report directory configuration blocker.

3. **Group safely**
   - Same media + same error reason -> identify once, process records sequentially.
   - Different media or different errors -> split into groups.
   - Missing source/config/permission errors -> stop early instead of repeatedly retrying.

4. **Delete stale history and retry**
   - Delete each failed history record immediately before retrying that file.
   - Use `transfer_file` with explicit `tmdbid`, `media_type`, and season when available.
   - For unrecognized media, prefer `recognize_media(path=...)` before `search_media`.

5. **Validate result**
   - Check transfer history and, when relevant, library existence.
   - Report success, failed, skipped counts and the remaining blocker.

Detailed examples and batch command patterns live in `REFERENCES.md`.

## Batch Optimization

For grouped failures from the same media:

- identify media once using the first representative file;
- reuse TMDB ID/media type for the batch;
- still delete and transfer each record individually;
- process sequentially to avoid race conditions.

### Parallel Recognition for Mixed-Media Batches

When failed records span multiple different media (different TMDB IDs or
unrecognized titles), parallelize the recognition phase:

1. Group records by media identity (same TMDB ID or same title).
2. For each group, dispatch one `media-researcher` subagent via
   `subagent_task` to run `recognize_media` on the representative path
   and, if needed, `search_media` for the resolved title.
3. Collect all subagent results, then proceed with per-record deletion
   and retransfer sequentially within each group.

This avoids serial `recognize_media` calls when the user asks to retry
"all failed transfers" or a large mixed batch. Fall back to direct
`recognize_media` calls if subagent infrastructure fails.
## File Organizer Invariants

Absorb file-organizer style logic as MoviePilot transfer discipline, not as arbitrary file moves:

- never organize from filename alone when transfer history has a TMDB/Douban ID, season, episode, downloader hash, or stored media type;
- keep grouped retries within the same media and same failure class;
- do not mix missing-source, permission/config, duplicate-target, and recognition failures in one retry batch;
- prefer explicit `tmdbid`, `media_type`, and `season` on retry when recognition previously failed;
- final success requires transfer history or library evidence, not merely that a file operation returned.

## Completion Checklist

- Failed records queried before deletion.
- Source path, failure reason, media identity, and grouping safety confirmed.
- Destructive deletion is authorized or confirmed.
- Retry result validated with transfer history or library evidence.
- Final summary includes success, failed, skipped counts and next blocker.
