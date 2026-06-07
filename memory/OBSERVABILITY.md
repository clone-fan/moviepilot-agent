---
name: 状态观测框架
version: 2.3.0
last_updated: 2026-06-07
---

# 状态观测框架

- 系统：`query_schedulers`、`query_workflows`、`query_downloaders`、`query_sites`、`test_site`。
- 业务：`query_subscribes`、`query_transfer_history`、`query_library_exists`、`query_library_latest`、`query_download_tasks`。
- 文件/目录：`query_directory_settings`、`list_directory`。
- Agent：仅查 `memory`、`jobs`、`skills`、`scripts`、`runtime` 关键状态；具体路径由对应 skill 或 runtime 管理。

原则：观测先于修改；无证据不下结论；心跳和自动任务数据必须来自真实路径或内部工具。自检观测必须服务当前目标，避免为了“看起来全面”引入无关扫描。

## 最小验证路径
状态类：查权威工具一次即可；配置类：查现状 → 最小修改 → 复查关键字段；Agent/Git：递归目录审计 → 旧备份/运行锚点核对 → 自检摘要 → git status；心跳：固定脚本或渲染断言，不由 AI 生成数据。
