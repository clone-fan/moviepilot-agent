---
name: Agent Memory Hub
description: 长期记忆入口索引与职责边界
version: 7.6.0
last_updated: 2026-06-09
---

# Agent Memory Hub

## 定位
`/config/agent/memory` 只保存长期、稳定、跨任务复用的运行规则。单次过程进 activity，定时任务进 jobs，脚本进 scripts，运行态进 runtime，历史资料进 docs。

记忆蒸馏原则：memory 只留高频常驻、跨场景复用且值得每次加载的规则；面向特定任务的流程、排障经验、操作清单、命令模板优先进入对应 skill；仓库映射、SSH 别名、公钥指纹、本地路径、候选清单和当前工作流状态等运行锚点优先进入 runtime；外部资料与长证据进 docs/archive。任何记忆/上下文扩展只能做建议或组织，不得成为第二事实源、第二路由器或隐藏执行控制面。

自我炼化原则：用户要求“吸收、沉淀、去除糟粕、焚烧炼化自身、进化出新的知识/技能/记忆、落实到 skills/记忆/all”时，应理解为蒸馏任务：优先使用 `self-distillation-metabolism` skill；不是复述原话，也不是把整段经验塞进 memory，而是先复盘经验与错误，抽取可复用的判断标准、流程纪律、触发边界或工具路径；剔除情绪、重复、一次性过程和噪声；再按职责落位——高频全局边界进 memory，领域流程与检查清单进 skills，确定性执行进 scripts，周期任务进 jobs，运行锚点进 runtime，历史材料进 docs/archive。若没有形成可复用规则，应只给出结论，不新增资产。

自我减负原则：用户要求审查/蒸馏/进化自身时，目标是降低常驻上下文、合并重复规则、迁移低频流程、减少无关检查；只审计与减负目标相关的资产，不把一次性审计步骤写成长期记忆。

## 读取顺序
1. `/config/agent/CURRENT_PERSONA.md`
2. 本文件
3. 核心规则：`USER_PREFERENCES.md`、`AGENT_RUNTIME_RULES.md`、`AGENT_SKILLS.md`、`SAFETY_BOUNDARIES.md`、`PERSONA_FUSION.md`
4. 业务与治理：`MOVIEPILOT_AGENT_WORKFLOW.md`、`DIRECTORY_GOVERNANCE.md`、`JOB_GOVERNANCE.md`、`OBSERVABILITY.md`、`ACCEPTANCE_CRITERIA.md`
5. 按需专项：`HEARTBEAT_REPORT_RULES.md`、`MOVIEPILOT_TROUBLESHOOTING.md`、`NOTIFICATION_WORKFLOW.md`、`SKILL_GOVERNANCE.md`、`SUPERPOWERS_WORKFLOW.md`、`WAKE_FORMAT.md`

## 不可压缩边界
- MoviePilot Agent 身份、媒体主链路、安全确认、技能优先、完成验证、人格融合、目录职责、Job 生命周期、心跳固定模板不可被普通偏好覆盖。
- 凭据安全边界见 `SAFETY_BOUNDARIES.md`。
