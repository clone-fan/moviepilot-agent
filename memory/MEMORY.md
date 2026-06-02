---
name: Agent Memory Hub
description: 长期记忆入口索引与职责边界
version: 7.0.0
last_updated: 2026-06-02
---

# Agent Memory Hub

## 定位
`/config/agent/memory` 只保存长期、稳定、跨任务复用的运行规则。单次过程进 activity，定时任务进 jobs，脚本进 scripts，运行态进 runtime，历史资料进 docs。

## 读取顺序
1. `/config/agent/CURRENT_PERSONA.md`
2. 本文件
3. 核心规则：`USER_PREFERENCES.md`、`AGENT_RUNTIME_RULES.md`、`AGENT_SKILLS.md`、`MOVIEPILOT_AGENT_WORKFLOW.md`、`SAFETY_BOUNDARIES.md`、`PERSONA_FUSION.md`
4. 治理与验收：`DIRECTORY_GOVERNANCE.md`、`JOB_GOVERNANCE.md`、`OBSERVABILITY.md`、`ACCEPTANCE_CRITERIA.md`、`WAKE_FORMAT.md`
5. 专项约束：`HEARTBEAT_REPORT_RULES.md`、`MOVIEPILOT_TROUBLESHOOTING.md`、`NOTIFICATION_WORKFLOW.md`、`SKILL_GOVERNANCE.md`、`SUPERPOWERS_WORKFLOW.md`

## 不可压缩边界
- MoviePilot Agent 身份、媒体主链路、安全确认、技能优先、完成验证、人格融合、目录职责、Job 生命周期、心跳固定模板不可被普通偏好覆盖。
- 不保存凭据、Token、Cookie、密码、私钥。
