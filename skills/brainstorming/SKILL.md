---
name: brainstorming
version: 4
description: "在需求不明确、需要设计取舍、创建新功能/新行为或范围较大的创造性工作之前使用；用户已给出明确最小修改、修复或落地执行指令时，不用它阻塞直接执行。"
allowed-tools: read_file list_directory execute_command write_file edit_file ask_user_choice
---

# 头脑风暴：将想法转化为设计

## 适用边界

使用本技能的场景：

- 用户提出新功能、新系统、新行为或复杂改造。
- 需求目标、范围、约束或成功标准不清楚。
- 存在多个合理方案，需要设计取舍。
- 修改会影响架构、长期维护方式、用户体验或安全边界。

不要用本技能阻塞这些场景：

- 用户已经给出明确、低风险、最小修改指令。
- 用户要求“落地执行”“继续执行”“按刚才方案执行”。
- 只是收窄文案、修正触发描述、同步配置、补充已确认规则。
- 已有计划足够明确，下一步应该执行、验证、整理。

这类明确执行场景交给 `agent-proactive-orchestration` 判断直接执行、按钮选择、只读检查或完成后 hook。

## 工作方式

当本技能适用时，通过简短协作把想法转化为可执行设计：

1. 只读了解必要上下文。
2. 每次只问一个关键问题；能用选项就用选项。
3. 给出 2-3 个方案和推荐。
4. 展示简短设计并获得用户确认。
5. 复杂任务再交给 `writing-plans` 形成实现计划。

## 设计重点

设计应覆盖：

- 目标与非目标。
- 影响范围。
- 职责边界。
- 风险与安全边界。
- 验证方式。
- 完成后是否需要 hook，例如仓库同步或按钮选择。

## MoviePilot Agent Adaptation

This skill is workflow support, not the primary MoviePilot business route.
It must never replace MoviePilot's operational chain:

site/auth -> recognition -> resource -> download/subscription -> transfer -> library verification.

For MoviePilot conversations:

- Resource search, torrent selection, subscriptions, downloads, transfers, site checks, plugin commands, and updates should route to the dedicated MoviePilot skills first.
- Use brainstorming only when the user is designing a new MoviePilot behavior, a new Agent skill, a recurring automation, a repository maintenance policy, or a broad interaction policy.
- If the user asks to “继续推进 / 执行 / 落地 / 自检”, do not brainstorm again unless a real decision is missing.
- If the design affects safety, explicitly identify which actions later require confirmation: downloads, deletes, restarts, credentials, plugin installs, workflow/scheduler execution, and destructive cleanup.

## Anti-Overplanning Rules

- Do not use brainstorming as an apology patch after missing a direct action.
- Do not ask for broad preferences when a safe default can be inferred from existing Agent rules.
- Do not create a plan for every small text edit; small confirmed changes should be executed and verified.
- Do not replace `tg-button-interaction`; if the next step is a choice, use buttons.
- Do not replace `verification-before-completion`; design is not evidence.

## Output Pattern

When used, keep the result compact:

1. State the decision problem.
2. Provide 2-3 options with trade-offs.
3. Recommend one option.
4. Name the verification method.
5. Ask for the next choice with buttons when the platform supports it.

For low-risk design questions, a concise recommendation can be enough. For high-impact changes, separate design approval from execution approval.

## Handoff Rules

After brainstorming:

- New or changed skill -> `create-moviepilot-skill`, then repository sync reminder.
- Multi-step implementation -> `writing-plans` or `executing-plans`.
- Bug/failure -> `systematic-debugging`.
- MoviePilot media operation -> the matching MoviePilot domain skill.
- User choice needed -> `tg-button-interaction`.

## Completion Checklist

- Confirm the selected workflow actually fits the user request.
- Keep outputs actionable and bounded; avoid turning simple MoviePilot tasks into heavy planning.
- Identify the next executor skill; do not leave only vague ideas.
- Before any completion claim, run or cite fresh verification appropriate to the change.
- If durable `/config/agent` capability assets changed, trigger the repository sync reminder path.
