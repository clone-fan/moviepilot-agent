---
name: Agent Memory Hub
description: Agent 记忆目录的入口说明与读取顺序
version: 6.0.0
last_updated: 2026-05-01
---

# Agent Memory Hub

## 目录结构
```text
/config/agent/
├── CURRENT_PERSONA.md
├── docs/
├── jobs/
├── scripts/
├── memory/
│   ├── MEMORY.md
│   ├── USER_PREFERENCES.md
│   ├── AGENT_RUNTIME_RULES.md
│   ├── AGENT_SKILLS.md
│   ├── DIRECTORY_GOVERNANCE.md
│   ├── SUPERPOWERS_WORKFLOW.md
│   ├── PERSONA_FUSION.md
│   ├── MOVIEPILOT_AGENT_WORKFLOW.md
│   ├── SAFETY_BOUNDARIES.md
│   ├── MOVIEPILOT_TROUBLESHOOTING.md
│   ├── OBSERVABILITY.md
│   ├── JOB_GOVERNANCE.md
│   ├── NOTIFICATION_WORKFLOW.md
│   ├── SKILL_GOVERNANCE.md
│   ├── ACCEPTANCE_CRITERIA.md
│   └── WAKE_FORMAT.md
├── runtime/
└── skills/
```

## 读取顺序
1. 读取 `/config/agent/CURRENT_PERSONA.md`
2. 读取 `/config/agent/memory/MEMORY.md`
3. 读取 `/config/agent/memory/` 下的规则文件：
   - `USER_PREFERENCES.md`
   - `AGENT_RUNTIME_RULES.md`
   - `AGENT_SKILLS.md`
   - `WAKE_FORMAT.md`
   - `DIRECTORY_GOVERNANCE.md`
   - `SUPERPOWERS_WORKFLOW.md`
   - `PERSONA_FUSION.md`
   - `MOVIEPILOT_AGENT_WORKFLOW.md`
   - `SAFETY_BOUNDARIES.md`
   - `MOVIEPILOT_TROUBLESHOOTING.md`
   - `OBSERVABILITY.md`
   - `JOB_GOVERNANCE.md`
   - `NOTIFICATION_WORKFLOW.md`
   - `SKILL_GOVERNANCE.md`
   - `ACCEPTANCE_CRITERIA.md`
4. `/config/agent/docs/` 仅作为过往文件、回溯资料和旧版记忆查询区；只有需要追溯历史资料时才读取，不作为现行系统运行数据来源

## 使用约束
1. 长期规则统一保存在 `/config/agent/memory/`，但必须按职责拆分。
2. `USER_PREFERENCES.md` 只记录用户长期、稳定、跨任务通用的个人偏好。
3. `CURRENT_PERSONA.md` 用于标识当前人格入口
4. `docs/` 用于补充说明与参考资料
5. 涉及能力、规则、方法与配置检查时，遵循 superpowers 工作方式
6. 现行系统运行态文件应放在 `runtime/`、`jobs/`、`memory/`、`skills/` 等对应职责目录，不放在 docs
7. `jobs/` 只放 Job 定义与执行日志；可执行脚本统一放在 `/config/agent/scripts/`
