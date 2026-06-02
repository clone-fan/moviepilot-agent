---
name: Agent Memory Bridge
description: 原生 Agent 的入口与读取约束，不存放业务细节，仅保留最小必要规则
version: 2.0.0
last_updated: 2026-04-23
---

# Agent Memory Bridge

## 1. 核心规则
1. **人格指定**：当前激活人格由 `/config/agent/CURRENT_PERSONA.md` 唯一指定
2. **唤醒流程**：助手被唤醒后，必须先读取 `CURRENT_PERSONA.md`，再读取 `/config/agent` 根目录下的原生 agent 文件
3. **文件检查**：必须完整读取并检查 `MEMORY.md`、`USER_PREFERENCES.md`、`AGENT_PROFILE.md`、`AGENT_SKILLS.md`、`AGENT_WORKFLOW.md`、`AGENT_HOOKS.md`、`WAKE_FORMAT.md` 的一致性
4. **立即接管**：读取完成后，必须立即以原生 agent 接管
5. **写回规则**：新记忆、规则、技能只写回 `/config/agent` 根目录，不再依赖子人格目录

## 2. 接管约束
1. **根层接管**：任意 AI 接手时，必须先完成一次根层接管后才能继续对话
2. **残留清理**：若发现旧路径、冲突、残留或污染，必须先清理并收口到根层文件
3. **修改限制**：当需要更换人格或规则体系时，只允许修改 `/config/agent/CURRENT_PERSONA.md` 与根层原生 agent 文件

## 3. 文件结构
```
/config/agent/
├── MEMORY.md
├── CURRENT_PERSONA.md
├── AGENT_PROFILE.md
├── AGENT_SKILLS.md
├── AGENT_WORKFLOW.md
├── AGENT_HOOKS.md
├── USER_PREFERENCES.md
├── WAKE_FORMAT.md
├── skills/
├── jobs/
└── docs/
```

## 4. 说明
桥接层只保留最小必要规则，所有业务细节收口到根层骨架、技能、任务与文档。

## 长期上下文
- GitHub 账号主页：`https://github.com/clone-fan`
- 默认公开仓库名候选：`moviepilot-agent-config`
- Git 推送偏好：优先 `SSH`

## 用户执行偏好
- 对涉及 Agent 能力、规则、方法论、配置完整性的检查任务，必须严格按 superpowers 工作流执行：先读技能/方法文件，再做现状核查，给出证据、缺口、修复建议与下一步，不得跳步或只做口头判断。
