---
name: 心跳播报固定模板规则
version: 2.1.0
last_updated: 2026-06-08
---

# 心跳/每日汇报固定模板规则

固定模板心跳播报/每日汇报走 MoviePilot 内置 `agent_heartbeat` 或 MP 运维助手 `AgentOpsAssistant` 的每日汇报链路，不走系统 cron 直跑。

## 固定模板
模板版本：`2026-05-29.fixed-v1`。模板、icon、标题、排版、栏目顺序固定只允许真实数据变化；数据来自 MoviePilot 内部路径、确定性脚本或 MP 运维助手同源数据层，AI 不生成业务数据。即使功能名称从“心跳播报”升级为“每日汇报”，也必须继续沿用用户已定下的固定模板模架，不能因插件重构、UI 重命名或日报升级而丢失栏目顺序与模板骨架。

栏目顺序：问候行 → 时间 → MoviePilot → 站点状态 → 站点增量 → 下载器 → 入库整理 → 订阅追新 → 存储空间 → 今日摘要/提醒。

下载器：无正在下载时固定 `⦁ 正在下载：无`；不显示 0 速度；不显示无法确认的做种/可转移字段。

固定脚本：`/config/heartbeat_report.py`；通知走 MoviePilot 内部 `post_message`。

## 心跳唤醒规则
- 唯一 Job：`/config/agent/jobs/locked-heartbeat-report/JOB.md`。
- Job frontmatter 必须保持 `schedule: recurring`、`status: pending`，并在 `description` 写明唯一执行命令 `/opt/venv/bin/python /config/heartbeat_report.py` 与成功输出 `OK`。
- recurring 执行成功后仍保持 `pending`，只更新 `last_run` 与简短执行日志。
- 禁止 `/etc/cron.d`、`/etc/crontab`、`/var/spool/cron` 直接执行 `/config/heartbeat_report.py`，避免绕过 Agent Job 或重复播报。
- 验收必须同时确认：`agent_heartbeat` 调度存在且等待、Job 元数据可解析、脚本可编译、直跑 cron 无生效入口。
