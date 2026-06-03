---
name: moviepilot-agent 每周维护同步
description: 每周同步 /config/agent 中允许备份的 Agent 能力资产到 GitHub 仓库 clone-fan/moviepilot-agent；执行敏感扫描；有变更则自动提交并推送。
schedule: recurring
status: pending
last_run: ""
---
# 任务详情

## 目标
每周维护 `moviepilot-agent` 仓库，将 MoviePilot Agent 的可复用能力资产同步到 Git：

- `skills/`
- `runtime/personas/`
- `memory/`
- `jobs/`
- `scripts/`

## 执行命令

```bash
/opt/venv/bin/python /config/agent/scripts/sync_moviepilot_agent_repo.py
```

## 执行频率
每 7 天执行一次。执行成功后本 recurring 任务保持 `pending`，只更新 `last_run` 与执行日志。

## 安全边界

- `docs/` 为本地归档目录，不同步到 Git。

- 不提交私钥、Token、Cookie、密码、数据库、日志、缓存、活动记录。
- 使用 `/config/agent/runtime/git/ssh_config` 指定专用 Deploy Key 推送。
- 推送前执行高置信敏感信息扫描。
- 如果扫描发现敏感内容，任务失败并停止推送。

## 成功判定

脚本输出以下之一即视为成功：

- `OK no_changes`
- `OK no_staged_changes`
- `OK committed_and_pushed ...`

## 执行日志

- **2026-06-02 14:30** - 创建每周维护同步任务；首次验证执行成功。
