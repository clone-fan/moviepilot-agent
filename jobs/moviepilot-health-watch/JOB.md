---
name: MoviePilot 健康巡检
description: 每天最多一次轻量健康巡检；唯一执行命令：PYTHONDONTWRITEBYTECODE=1 /opt/venv/bin/python /config/agent/scripts/moviepilot_health_check.py；成功输出 SUMMARY ... fail=0；recurring 执行后保持 pending。
schedule: recurring
status: pending
last_run: "2026-06-07 15:23"
---
# MoviePilot 健康巡检

## 目标
在 `agent_heartbeat` 唤醒时，定期执行轻量健康检查，持续验证 MoviePilot Agent 的核心运行链路是否可用。

本 Job 只做巡检，不改配置、不触发下载、不修改站点、不改变心跳播报模板。

## 执行范围
- 订阅 API_TOKEN 只读探针：`/api/v1/subscribe/list?token=***`
- 站点配置内部探针：读取已配置站点数量与启用站点数量
- 下载器配置内部探针：读取下载器配置数量与启用下载器数量
- 调度器内部探针：读取系统调度器任务数量

## 执行命令
```bash
PYTHONDONTWRITEBYTECODE=1 /opt/venv/bin/python /config/agent/scripts/moviepilot_health_check.py
```

成功标准：脚本退出码为 `0`，并输出 `SUMMARY ... fail=0`。

## 运行周期
- recurring
- 由系统 `agent_heartbeat` 唤醒检查是否执行。
- 建议每天最多执行一次；如未来需要更高频，可调整为每 6 小时。
- 执行完成后更新 `last_run`，状态保持 `pending`。

## 通知策略
1. 成功时只写入本 Job 执行日志，不主动通知，避免打扰。
2. 失败时发送通知，标题建议为 `MoviePilot 健康巡检异常`。
3. 失败时保留脚本输出摘要，便于后续排查。

## 安全边界
1. 不保存、回显或写入完整 Token、Cookie、密码、API Key。
2. 不调用删除、下载、订阅新增、站点更新等高影响接口。
3. 不读取聊天上下文生成健康状态。
4. 不把本 Job 接入心跳固定模板，避免污染心跳排版。
5. 不在 Job 目录存放脚本、缓存、日志文件或临时文件。

## 执行日志

- **2026-06-07 15:23** - 执行命令：PYTHONDONTWRITEBYTECODE=1 /opt/venv/bin/python /config/agent/scripts/moviepilot_health_check.py；结果：成功；输出：SUMMARY total=5 pass=5 fail=0。
- **2026-06-02 20:02** - 执行命令：/opt/venv/bin/python /config/agent/scripts/moviepilot_health_check.py；结果：成功；输出：SUMMARY total=5 pass=5 fail=0

- **2026-06-01 13:54** - 联动复核 Agent Job 执行链路：脚本 `/config/agent/scripts/moviepilot_health_check.py` 通过编译并实际执行成功；SUMMARY total=5 pass=5 fail=0；状态保持 pending。
- **2026-06-01 01:30** - 心跳触发执行健康巡检成功；subscribe=5，sites=6/6 active，downloaders=2/2 enabled，scheduler_jobs=20；SUMMARY total=5 pass=5 fail=0；状态保持 pending。
- **2026-05-29 21:17** - 心跳触发执行健康巡检成功；subscribe=13，sites=6/6 active，downloaders=2/2 enabled，scheduler_jobs=20；SUMMARY total=5 pass=5 fail=0；状态保持 pending。
- **2026-05-29 19:15** - 创建健康巡检 Job；脚本 `/config/agent/scripts/moviepilot_health_check.py` 已单独验证通过，输出 `SUMMARY total=5 pass=5 fail=0`；总自检 `agent_self_audit.py` 已验证 `SUMMARY total=69 pass=69 fail=0`；状态保持 pending。
