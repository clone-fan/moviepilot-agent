---
name: Superpowers 工作流适配
version: 2.2.0
last_updated: 2026-06-07
---

# Superpowers 工作流适配

Superpowers 是工作流纪律层，不是身份层；不替代 MoviePilot Agent 身份、主链路和安全边界。

涉及工具、配置、排障、计划、实现、媒体业务时先检查适用 skill；显式触发类中文规范 skill 仅在用户明确要求时使用。

优先级：用户明确指令/安全边界 → MoviePilot Agent core → Superpowers → MoviePilot skills 管领域执行 → persona。

Superpowers 管流程，MoviePilot skills 管领域执行；不得抢占 MoviePilot 主流程。

核心规则：bug 先根因；新行为先设计；复杂任务先计划；完成前验证；不得用流程技能拖慢明确直通命令。

## MoviePilot 业务技能重叠裁决
业务重叠时按 `moviepilot-direct-routes` → `resource-search` → `moviepilot-cli` → `moviepilot-api` → `command-dispatch` → 专项技能仲裁。

## 显式触发例外
`chinese-code-review`、`chinese-commit-conventions`、`chinese-documentation`、`chinese-git-workflow` 等显式触发类 skill 仅在用户明确要求时使用，且不得抢占 MoviePilot 主流程。

业务路由以 `AGENT_SKILLS.md` 为准，Superpowers 只保留流程纪律边界。

