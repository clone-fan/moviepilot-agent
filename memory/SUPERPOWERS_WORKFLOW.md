---
name: Superpowers 工作流适配
version: 2.1.0
last_updated: 2026-06-02
---

# Superpowers 工作流适配

Superpowers is workflow not identity：Superpowers 是流程纪律层，不是身份层；does not replace MoviePilot，不替代 MoviePilot Agent 身份、主链路和安全边界。

涉及工具、配置、排障、计划、实现、媒体业务时先检查 skill；explicit trigger exceptions：显式触发类中文规范 skill 只在用户明确要求时使用。

优先级：用户明确指令/安全边界 → MoviePilot Agent core → Superpowers → 业务 skill → persona。

核心规则：bug 先根因；新行为先设计；复杂任务先计划；完成前验证；不得用流程技能拖慢明确直通命令。

## 自检锚点
Superpowers 管流程，MoviePilot skills 管领域执行。MoviePilot 业务技能重叠裁决：moviepilot-direct-routes > resource-search > moviepilot-cli > moviepilot-api。explicit trigger exceptions 仅在用户明确要求时触发。
工作流纪律层；不是身份层；MoviePilot Agent。
显式触发例外：chinese-code-review 等中文规范技能不得抢占 MoviePilot 主流程。
