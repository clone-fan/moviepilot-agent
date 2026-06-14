# Transfer Failed Retry Reference

本文件是 `transfer-failed-retry` 的低频参考资料。常规执行优先看 `SKILL.md`；需要示例或错误矩阵时再读取这里。

## Failure Matrix

| Error Message | Cause | Solution |
|---|---|---|
| 未识别到媒体信息 | 文件名无法匹配媒体 | 用 `recognize_media`，必要时 `search_media`，然后显式 `tmdbid` 转移 |
| 源目录不存在 | 源文件已移动或删除 | 不能重试，跳过并报告 |
| 目标路径不存在 | 目标目录或配置问题 | 配置已修复后可重试 |
| 文件已存在 | 目标文件已存在 | 报告重复/覆盖阻塞 |
| 未找到有效的集数信息 | 集数识别失败 | 路径识别或显式指定 TMDB/season |
| 未获取到转移目录设置 | 未配置转移目录 | 需要用户修复目录配置 |

## Single File Example

```text
# 1. Query failed record
query_transfer_history(status="failed", page=1)
# Found: id=42, src="/downloads/Movie.Name.2024.1080p.mkv", errmsg="未识别到媒体信息"

# 2. Recognize from path
recognize_media(path="/downloads/Movie.Name.2024.1080p.mkv")

# 3. If recognition fails, search TMDB
search_media(title="Movie Name", year="2024", media_type="movie")

# 4. Delete stale history
delete_transfer_history(history_id=42)

# 5. Re-transfer with explicit identity
transfer_file(file_path="/downloads/Movie.Name.2024.1080p.mkv", tmdbid=123456, media_type="movie")
```

## Batch Example

```text
# Failed records: [42, 43, 44, 45], same show, same error
query_transfer_history(status="failed")

# Identify once
recognize_media(path="/downloads/Show.Name.S01E01.1080p.mkv")
# Found: tmdb_id=789, media_type="tv"

# Then process each record sequentially
delete_transfer_history(history_id=42)
transfer_file(file_path="/downloads/Show.Name.S01E01.1080p.mkv", tmdbid=789, media_type="tv")

delete_transfer_history(history_id=43)
transfer_file(file_path="/downloads/Show.Name.S01E02.1080p.mkv", tmdbid=789, media_type="tv")
```

## Notes

- Always delete the old failed history record before retrying; MoviePilot may skip files that already have transfer history.
- Do not retry missing source files.
- Do not retry missing transfer directory configuration until the config is fixed.
- For TV shows, ensure season/episode recognition is correct.
- For batch processing, reuse media identity but process each record individually.
