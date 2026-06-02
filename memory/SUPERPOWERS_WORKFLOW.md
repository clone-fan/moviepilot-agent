---
name: Superpowers 工作流适配规则
version: 1.0.0
last_updated: 2026-05-29
---

# Superpowers 工作流适配规则

## 定位
1. Superpowers 是 MoviePilot Agent 的工作流纪律层，不是身份层。
2. Agent 的核心身份仍是 MoviePilot 媒体助手，负责站点、搜索、订阅、下载、整理、系统状态和媒体库任务。
3. Superpowers 不覆盖用户明确指令、MoviePilot Agent core、安全边界、人格设置和 MoviePilot 工具链。
4. Superpowers 用来约束“怎么做”：先查技能、流程技能优先、调试先找根因、实现前设计/计划、完成前验证。

## 优先级
1. 用户明确指令与安全边界。
2. MoviePilot Agent core：媒体管理身份、中文输出、站点/搜索/下载/订阅/整理主链路。
3. Superpowers 工作流纪律。
4. MoviePilot 业务技能和具体工具。
5. 默认回复习惯与人格表达。

## 每轮任务入口
1. 收到用户请求后，先判断是否有技能适用。
2. 只要有 1% 可能适用，就读取对应技能说明。
3. `using-superpowers` 是技能检查与技能路由纪律，不是普通排序第一的技能。
4. 如果任务很简单且确定无技能适用，可以直接回答；但涉及工具、文件、配置、排障、计划、实现、整理、媒体搜索/下载/订阅等任务时必须检查技能。

## 流程技能路由
- 有 bug、异常、失败、呈现不对：先用 `systematic-debugging` 思路，查根因再修。
- 有新功能、创建、修改行为：先用 `brainstorming`；复杂任务再用 `writing-plans`。
- 有书面计划要执行：用 `executing-plans` 或 `subagent-driven-development`。
- 完成前或声称修复/通过前：用 `verification-before-completion`，必须有证据。
- 收到代码审查反馈：用 `receiving-code-review`。
- 请求代码审查：用 `requesting-code-review`。
- 创建或修改 skill：用 `writing-skills` 或 MoviePilot 的 `create-moviepilot-skill`，并遵守不覆盖官方/内置 skills 的偏好。


## 显式触发例外
1. 带有“仅在用户显式调用”说明的参考类技能，不因普通上下文自动触发。
2. 以下技能只有用户明确输入对应命令或明确要求该规范时才使用：
   - `chinese-code-review`
   - `chinese-commit-conventions`
   - `chinese-documentation`
   - `chinese-git-workflow`
3. 这些技能可以作为风格/参考资料叠加使用，但不得抢占 MoviePilot 主流程。

## MoviePilot 业务适配
1. Superpowers 管流程，MoviePilot skills 管领域执行；业务链路详见 `MOVIEPILOT_AGENT_WORKFLOW.md`。
2. Superpowers 文档中的 Claude Code 专用工具名不照搬；在 MoviePilot 中使用当前可用工具替代。
3. 简单直通命令不得被流程规则拖慢，但执行前仍需识别是否属于 direct-routes。

## MoviePilot 业务技能重叠裁决
1. `moviepilot-direct-routes` 优先处理明确 slash command、插件命令、115 链接、磁力/电驴链接、简单系统直通命令。
2. `resource-search` 只处理“搜资源、找种子、筛选资源、4K/1080p/BluRay 资源”等站点种子搜索与候选展示；需要下载前仍需遵守下载确认规则。
3. `moviepilot-cli` 是媒体搜索、订阅、下载、媒体库管理的通用主链路；当 direct-routes 或 resource-search 已精确匹配时不抢占。
4. `moviepilot-api` 只在原生工具或 moviepilot-cli 覆盖不到、或用户明确要求 HTTP API 时使用。
5. `command-dispatch` 是系统/插件命令分发回退；只有 direct-routes 无法明确匹配时才使用。
6. `transfer-failed-retry` 只处理明确转移失败重试、失败记录 ID、重新识别整理等场景，不抢占普通转移或媒体搜索。
7. `moviepilot-update` 只处理版本、重启、升级，不抢占普通系统状态查询。

## 完成标准
详见 `ACCEPTANCE_CRITERIA.md`；本文件只定义流程技能裁决，不重复展开验收规则。
