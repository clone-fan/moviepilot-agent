---
name: moviepilot-ui-design
version: 3
description: >-
  Use this skill when designing, reviewing, or improving MoviePilot-specific UI:
  local plugins, settings pages, dashboards, Vuetify JSON forms, Vue plugin
  pages, MP 运维助手界面, “参考115 STRM”, “今日UI大学习”, “太丑了”,
  “像正经插件”, icons, layout, micro-interactions, accessibility, and design
  distillation for MoviePilot.
allowed-tools: read_file list_directory execute_command write_file edit_file browse_webpage search_web query_installed_plugins query_plugin_config reload_plugin query_plugin_capabilities
---
# MoviePilot UI Design

## Mission

MoviePilot 专用 UI 能力器官：把截图、参考插件、用户吐槽或设置页问题，转成 MP 原生、可操作、可验证的界面改进。

它负责 UI 判断与结构设计；不替代插件开发、系统排障、媒体业务或直接命令路由。

## Trigger

使用本技能处理：

- MoviePilot 插件设置页、Dashboard、操作页、历史表格、Vuetify JSON 表单、Vue 插件页。
- 用户说“UI 太丑”“像正经插件”“参考 115 STRM”“今日 UI 大学习”“优化界面/交互/图标/布局”。
- 需要把外部 UI/UX 资料蒸馏进 MoviePilot 场景。

低频资料、外部 UI 候选、图表/动效扩展清单见同目录 `REFERENCES.md`。

## Design Bar

合格的 MP UI 必须让用户更快、更安全地完成媒体/系统操作：

- 目标清楚：状态、配置、动作、结果或风险只能有一个主线。
- 层级清楚：概览 → 推荐路径 → 配置 → 操作 → 危险区。
- 尊重 MP：保留官方主题变量与语义色，不复制外部皮肤。
- 渐进披露：基础优先，高级折叠，危险动作隔离。
- 状态完整：loading、empty、success、warning、error、disabled、confirm。
- 文案实用：明确数据、路径、站点、插件、任务或影响范围。

## Routing by Surface

- **插件设置页**：基础/高级/危险分区，预设、提示、保存与动作分离。
- **运维 Dashboard**：状态卡、最近结果、告警、快捷动作、历史入口。
- **清理/备份/更新**：预览 → 范围 → 确认 → 执行 → 结果/备份记录。
- **媒体/媒体库流程**：身份 → 来源/站点 → 动作 → 转移/入库状态。
- **高风险动作**：独立警告区、影响范围、可回退方案、确认门禁。
- **复杂 Vue 页面**：仅在复杂状态流、表格、对话框、向导或用户明确要求时使用；轻量插件优先 JSON/Vuetify。

## Structural Patterns

### Vuetify JSON

轻量插件或用户明确“不升级 Vue”时优先：

- 外层 `VCard` 承载主界面，标题/状态在顶部。
- `VExpansionPanels` 放基础、高级、危险配置。
- `VTabs` + `VWindow` 放同级功能组。
- `VCardActions` 集中常用按钮，避免按钮散落。
- `VAlert` 表达提示、风险、执行结果。

### Vue Rich Page

仅在以下情况升级：复杂 Dashboard、固定操作栏、目录选择、登录/扫描、复杂表格、预览/确认向导、细粒度异步状态。

### 115 STRM Lesson

借结构，不借皮肤：主卡片、标题栏、折叠基础设置、tabs/window 功能区、集中 action bar、风险 dialog、密集但有组织的字段。

## Anti-Slop

不要做：

- 一长串平铺字段；
- 无层级重复卡片；
- 覆盖 MP 主题色的大面积皮肤；
- 危险按钮贴着常规按钮；
- “优化体验”这类无操作意义文案；
- 每个 label 都塞装饰图标；
- 为运维页面加入分散注意力的动效。

## Workflow

1. **Inspect**：确认当前是 JSON/Vuetify 还是 Vue；保留 config key、按钮、API、命令和风险动作。
2. **Spec**：冻结界面类型、主目标、借鉴模式、禁止事项和验收标准。
3. **Restructure**：先做层级和分区，再做视觉。
4. **Polish**：补文案、状态 chip、图标语义、间距密度；不随意覆盖主题色。
5. **Verify**：语法/构建、配置键保留、必要时重载插件、检查命令/能力注册、断言关键组件存在。

## Review Checklist

- 新用户 10 秒内能找到推荐路径吗？
- 页面是否按“状态 → 范围 → 预览风险 → 执行 → 结果”组织？
- 高级字段是否不会压过推荐路径？
- 危险动作是否隔离且确认门禁清楚？
- 常规按钮是否按任务分组？
- 空/加载/错误/成功状态是否可见？
- 字段与配置键是否兼容未丢失？
- 若动作入口改变，是否检查插件命令/能力注册？

## Plugin Delivery UI Proof

When UI work is part of plugin delivery, verify the user-facing entry as well as the layout:

- config fields preserve saved keys and safe defaults;
- buttons map to real slash commands, API routes, workflow actions, or service methods;
- preview/result areas show what happened, not only that a button was clicked;
- dangerous actions are separated from routine actions and keep confirmation wording visible;
- JSON/Vue changes are checked by component/key assertions, and browser/screenshot proof is added only when visible state matters.

## Visual Verification

For UI-heavy plugin work, prefer a small visible-state proof when practical:

- final screenshot or browser text confirming the page, tab, button, dialog, or alert exists;
- component/key assertions for JSON/Vuetify when browser access is unnecessary;
- backend proof for actions: plugin config, capability registration, command result, or persisted result record.

A screenshot proves appearance only. Pair it with MoviePilot state when claiming an action works.

## Output Contract

汇报只说有用证据：处理的 MP UI 类型、采用的结构模式、结构/行为变化、拒绝了哪些不适合 MP 的做法、验证证据与剩余限制。

完成标准是实现或评审质量与新鲜证据，不是复述用户原话。