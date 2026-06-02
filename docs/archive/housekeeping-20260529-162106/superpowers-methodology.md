---
name: Superpowers 方法吸收笔记
description: 吸收 obra/superpowers 的工程方法论，并映射到当前 MoviePilot Agent 的可落地执行规则
source: https://github.com/obra/superpowers
last_updated: 2026-04-22
---

# Superpowers 方法吸收笔记

## 1. 外部框架定位
`obra/superpowers` 不只是若干 `SKILL.md`，而是一套完整的 Agent 工程方法：
- Skills（技能）
- Subagents（子智能体/任务分拆）
- Slash Commands（命令入口）
- Hooks（会话/执行钩子）
- Multi-platform Adapters（多平台适配）

## 2. 当前环境可吸收部分
结合当前 MoviePilot Agent 能力，优先吸收以下原则：

1. **技能优先**：复杂任务先归类到技能，再执行，不直接裸跑工具链
2. **任务拆分**：复杂任务拆成可验证的小步，每步都要有明确产物
3. **命令即入口**：能用 slash command / 调度器 / 固定链路解决的，优先走稳定入口
4. **过程钩子化**：把“执行前检查、执行后自检、完成后收口”固化成默认动作
5. **平台无关表达**：规则尽量写成与具体模型/前端无关的流程，而不是绑定某个会话习惯
6. **评审意识**：执行后默认进行一次最小必要复核，不把未验证状态当完成
7. **结果成品化**：交付给少爷的是结果、成品、可选下一步，不是零散中间态

## 3. 对当前 Agent 的映射
| Superpowers 概念 | 当前可用映射 |
|---|---|
| Skills | `/config/agent/skills/*` + 显式技能工作流 |
| Subagents | 通过“任务拆分 + 并行工具调用 + 分阶段执行”近似实现 |
| Slash Commands | `run_slash_command` + 固定插件命令 |
| Hooks | `AGENT_WORKFLOW.md` 中的默认自检、自动收口、连续任务承接 |
| Adapters | MoviePilot CLI / API / 插件 / 浏览器 / 文件 / 命令行 多链路回退 |

## 4. 落地约束
1. 当前环境**不原生提供真正的子Agent编排层**，因此只吸收“分治与复核”的方法，不伪装成已具备完整多Agent调度
2. 不把工程方法泛化成冗长流程，仍保持少爷偏好的短句、直接、结果优先
3. 新方法只作为增强，不替代 MoviePilot 原生稳定链路

## 5. 默认执行模板
1. 先判断：这是查询、执行、修复、比较，还是长期任务
2. 再选技能：优先匹配已有技能或固定命令入口
3. 能并行的并行：搜索、状态检查、库检查尽量同时做
4. 关键动作前确认：删除、开下、批量改动必须确认
5. 执行后自检：至少补一次最小验证
6. 最终收口：给少爷一句话结果 + 必要时给下一步选项
