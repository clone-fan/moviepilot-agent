---
name: Agent 技能路由
version: 7.1.0
last_updated: 2026-06-02
---

# Agent 技能路由

## 总则
技能是流程纪律与领域知识入口：涉及工具、文件、配置、排障、计划、实现、媒体业务时先读适用 skill。显式触发类 skill 只在用户明确要求时用。

## 路由优先级
1. 明确 slash command、插件命令、115 链接、磁力/电驴、简单系统直通 → `moviepilot-direct-routes`
2. 搜资源/找种子/筛资源/4K/1080p/BluRay → `resource-search`
3. 电影、剧集、动漫、订阅、下载、媒体库通用任务 → `moviepilot-cli`
4. REST API 或工具覆盖不到 → `moviepilot-api`
5. 插件/系统命令分发回退 → `command-dispatch`
6. 识别词 → `generate-identifiers` / `media-identifier-rulecraft`
7. 转移失败重试 → `transfer-failed-retry`
8. 版本、升级、重启 → `moviepilot-update`
9. 数据库原始查询/维护 → `database-operation`
10. 创建/修改 Agent skill → `create-moviepilot-skill` / `writing-skills`

## moviepilot skill overlap arbitration
技能重叠时按 direct routes → resource-search → moviepilot-cli → moviepilot-api → command-dispatch → 专项技能的顺序仲裁；安全确认与用户明确指令优先。

## 流程技能
- bug/异常/失败：`systematic-debugging`
- 新功能/行为设计：`brainstorming`，复杂时再 `writing-plans`
- 执行书面计划：`executing-plans` / `subagent-driven-development`
- 完成前：`verification-before-completion`

## 维护使命
`moviepilot-agent` 是 Agent 能力资产管理仓库；维护目标是可迁移、可审计、可恢复、可持续演进，不是普通源码项目。
