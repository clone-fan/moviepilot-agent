---
name: 状态观测框架
version: 1.0.0
last_updated: 2026-05-29
---

# 状态观测框架

## 系统观测
- 调度器：`query_schedulers`
- 工作流：`query_workflows`
- 下载器：`query_downloaders`、`query_download_tasks`
- 站点：`query_sites`、`test_site`、`query_site_userdata`

## 业务观测
- 订阅：`query_subscribes`、`query_subscribe_history`
- 转移：`query_transfer_history`
- 媒体库：`query_library_exists`、`query_library_latest`
- 目录：`query_directory_settings`、`list_directory`

## Agent 自身观测
- `jobs/*/JOB.md` 状态与 `last_run`
- `scripts/` 中脚本可执行性
- `memory/` 规则文件完整性
- `docs/` 是否只作历史区
- `runtime/cache/` 是否承载运行态缓存
- `agent_self_audit.py` 是否全绿

## 原则
1. 观测优先于修改。
2. 无证据不下结论。
3. 自动任务和心跳数据必须来自真实路径或内部工具。
4. 运行状态与目录结构都应能被自检脚本或工具验证。
