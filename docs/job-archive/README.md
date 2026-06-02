---
name: Job 归档目录
retention_days: 60
last_updated: 2026-05-29
---
# Job 归档目录

本目录用于归档已停用或已蒸馏迁移的 Agent Job。

注意：自动销毁 Job 的实际清理根目录是 `/config/agent/docs/`，不是只清理本子目录。

## 保留策略
- 归档文件保留 60 天。
- 超过 60 天的归档目录可自动删除。
- 当前清理脚本：`/config/agent/docs/cleanup_docs_archive.py`

## 当前归档
- `simple-heartbeat-report-*`：旧版简单心跳播报，已蒸馏迁移到 `/config/agent/jobs/locked-heartbeat-report/JOB.md`。

## 自动销毁 Job
- Job 路径：`/config/agent/jobs/archive-auto-destroy/JOB.md`
- 周期：60 天执行一次
- 命令：`/opt/venv/bin/python /config/agent/docs/cleanup_docs_archive.py`
- 范围：只清理 `/config/agent/docs/` 下超过 60 天的资料，不处理 active jobs。
