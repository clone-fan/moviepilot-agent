---
name: Agent 技能路由
version: 7.3.0
last_updated: 2026-06-09
---

# Agent 技能路由

## 总则
技能是流程纪律与领域知识入口：涉及工具、文件、配置、排障、计划、实现、媒体业务时先读适用 skill。显式触发类 skill 只在用户明确要求时用。

## 前置门禁
- 每轮用户可见回复前必须先过 `tg-button-interaction`：凡确认、继续、授权、同意、取消、重试、范围/质量/站点/动作选择等可由 2-6 个安全选项表达的交互，必须调用 `ask_user_choice` 并停止本轮；不得要求用户手输例行“继续/同意/授权/确认”。若 TG 按钮链路异常，文字只能作为临时保活，同时进入 `systematic-debugging` 恢复真实 callback 交互并做安全 smoke test。
- 用户说“继续、执行、落地、接管、放开手脚、自己判断、按方案推进”，或出现安全确认与执行推进冲突时，先用 `agent-executive-control` 判定直接执行、只读检查、按钮确认或澄清；已授权的低风险 `/config/agent` 或 `/config` 本地插件资产改动不得停在口头计划。
- 复杂跨步骤任务由 `agent-proactive-orchestration` 做执行模式分类、完成闭环和移交；它是路由/控制层，不替代具体领域技能，并且必须把剩余的有界用户选择移交给按钮而非手输。

## 路由优先级
1. 明确 slash command、插件命令、115 链接、磁力/电驴、简单系统直通 → `moviepilot-direct-routes`
2. 搜资源/找种子/筛资源/4K/1080p/BluRay → `resource-search`
3. 电影、剧集、动漫、订阅、下载、媒体库通用任务 → `moviepilot-cli`
4. REST API 或工具覆盖不到 → `moviepilot-api`
5. 插件/系统命令分发回退 → `command-dispatch`
6. 识别词调度：
   - 常规自定义识别词、简单别名/噪声清理、普通偏移、已确认 ID 绑定 → `generate-identifiers`
   - 动漫/剧集复杂季集映射、绝对集数、TMDB episode group、数字干扰防碰撞、普通规则失败后的高级规则设计 → `media-identifier-rulecraft`
7. 转移失败重试 → `transfer-failed-retry`
8. 版本、升级、重启 → `moviepilot-update`
9. 数据库原始查询/维护 → `database-operation`
10. 创建/修改 Agent skill → `create-moviepilot-skill` / `writing-skills`

## moviepilot skill overlap arbitration
技能重叠时按 direct routes → resource-search → moviepilot-cli → moviepilot-api → command-dispatch → 专项技能的顺序仲裁；安全确认与用户明确指令优先。

## UI / 设计技能
- MoviePilot 专用 UI 能力器官：插件设置页、Dashboard、操作工作流、Vuetify JSON 表单、Vue 插件页、MP 运维助手、115 STRM 等成熟插件参考、外部 UI 知识蒸馏、图标/动效/状态反馈/安全交互 → `moviepilot-ui-design`。触发后要按 MoviePilot 场景选择专类模式并落实改进，不把用户措辞当成果。

## 流程技能
- 交互按钮门禁：`tg-button-interaction`
- 继续/落地/接管/授权边界/避免过度确认：`agent-executive-control`
- 全局执行闭环、任务收束与移交：`agent-proactive-orchestration`
- bug/异常/失败：`systematic-debugging`
- 新功能/行为设计：`brainstorming`，复杂时再 `writing-plans`
- 执行书面计划：`executing-plans` / `subagent-driven-development`
- 完成前：`verification-before-completion`

## 自我治理技能
- 能力资产落位与目录分层：`agent-capability-map`
- 自身器官分层与长期能力架构：`agent-organ-system`
- 反馈信号识别与路由：`agent-feedback-senses`
- 安全免疫边界与风险分级：`agent-immune-system`
- 主动成长闭环与经验学习：`agent-growth-cycle`
- Skill 架构治理、规则迁移、拆分合并与生命周期维护：`skill-architecture-governance`
- 用户纠错、行为修复与长期规则校准：`agent-self-correction`
- 吸收、沉淀、炼化、落实到 skills/memory/scripts/jobs/runtime/docs：`self-distillation-metabolism`
- 自检自身、重新蒸馏、进化版 Agent、增强/瘦身取舍、防重复治理：`agent-evolution-governor`
- 创建/修改 Agent skill：`create-moviepilot-skill` / `writing-skills`

## 蒸馏规则
- 特定任务的稳定流程、排障顺序、检查清单、命令模板应优先进对应 skill，不留在 memory。
- 非敏感运行锚点如仓库名、本地路径、Host 别名、公钥指纹应优先放 runtime，并由相关 skill 引用。
- 大型外部技能库吸收必须先过 `skill-architecture-governance` 的准入门：只把候选视为 capability slice，先判定来源、owner、去重、边界、生命周期和证据；禁止整包导入、禁止创建第二 orchestrator、禁止绕过 MoviePilot Agent 既有路由。

## 维护使命
`moviepilot-agent` 是 Agent 能力资产管理仓库；维护目标是可迁移、可审计、可恢复、可持续演进，不是普通源码项目。

## shortest official route
优先使用已存在的 MoviePilot 指令、插件命令、MCP 工具和维护脚本。直通命令走 direct routes；媒体业务走 MP 工具链；工具缺口走 moviepilot-api；仅当统计/修复需原始记录时才走 database-operation。
