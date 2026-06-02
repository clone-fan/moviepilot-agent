---
name: 状态观测框架
version: 2.0.0
last_updated: 2026-06-02
---

# 状态观测框架

- 系统：`query_schedulers`、`query_workflows`、`query_downloaders`、`query_sites`、`test_site`。
- 业务：`query_subscribes`、`query_transfer_history`、`query_library_exists`、`query_library_latest`、`query_download_tasks`。
- 文件/目录：`query_directory_settings`、`list_directory`。
- Agent：`jobs/*/JOB.md`、`scripts/`、`memory/*.md`、`skills/`、`runtime/cache/`、`agent_self_audit.py`。

原则：观测先于修改；无证据不下结论；心跳和自动任务数据必须来自真实路径或内部工具。

## 最小验证路径
状态类：查权威工具一次即可；配置类：查现状 → 最小修改 → 复查关键字段；Agent/Git：同步脚本 → 自检摘要 → git status；心跳：固定脚本或渲染断言，不由 AI 生成数据。
