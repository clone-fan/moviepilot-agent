---
name: 档案馆资料自动销毁
description: 每 60 天执行一次；唯一执行命令：/opt/venv/bin/python /config/agent/scripts/cleanup_docs_archive.py；成功输出 OK deleted_files=... deleted_dirs=...；recurring 执行后保持 pending。
schedule: recurring
status: pending
last_run: "2026-06-01 13:54"
---
# 档案馆资料自动销毁

## 目标
每 60 天执行一次，清理 `/config/agent/docs/` 历史资料区下超过 60 天的资料。

## 执行范围
- 只处理 `/config/agent/docs/` 历史资料区下的文件与空目录。
- `/config/agent/docs/` 只能作为过往文件、回溯资料和旧版记忆查询区，不允许存放现行系统运行态数据。
- 不处理 `/config/agent/jobs/` 下的 active Job。
- 不处理 `/config/agent/memory/`、`/config/agent/skills/`、`/config/agent/runtime/` 等其他目录。
- 清理脚本位于脚本目录：`/config/agent/scripts/cleanup_docs_archive.py`，不在 docs 历史资料区内，也不放在 jobs 定义目录内。

## 执行命令
```bash
/opt/venv/bin/python /config/agent/scripts/cleanup_docs_archive.py
```

## 运行周期
- recurring
- 60 天执行一次。
- 执行完成后更新 `last_run`，状态保持 `pending`。

## 销毁规则
- 资料按文件/目录修改时间计算。
- 超过 60 天的文件自动删除。
- 超过 60 天且已为空的目录自动删除。
- 未超过 60 天的不删除。

## 执行日志
- **2026-05-29 15:10** - 心跳触发执行清理脚本成功；deleted_files=0，deleted_dirs=0；状态保持 pending。
- **2026-05-29 16:39** - 按少爷确认的架构边界迁移清理脚本到 Job 自身目录，docs 明确为历史资料区，不再承载现行系统运行态文件。
- **2026-05-29 17:14** - 按少爷进一步蒸馏要求，将清理脚本从 Job 目录迁入 `/config/agent/scripts/`；Job 目录恢复为只保存 `JOB.md` 的任务定义与执行日志。
- **2026-05-29** - 创建自动销毁 Job；目标为 docs 档案馆资料，每 60 天执行一次清理脚本。
- **2026-06-01 13:31** - 误报：报告曾记录“未找到硬锁路径脚本”，后复核脚本实际存在于 `/config/agent/scripts/cleanup_docs_archive.py`；根因为心跳 Agent 未按 JOB.md 的“执行命令”读取完整任务详情，只依赖注入摘要判断。
- **2026-06-01 13:54** - 修复调度文档：在 frontmatter description 中加入唯一执行命令；已实际执行 `/opt/venv/bin/python /config/agent/scripts/cleanup_docs_archive.py`，输出 `OK deleted_files=0 deleted_dirs=0`；状态保持 pending。
