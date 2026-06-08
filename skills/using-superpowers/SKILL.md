---
version: 4
name: using-superpowers
description: 在开始任务时用于确认是否有适用技能，并按 MoviePilot Agent 的技能路由执行；这是技能入口纪律，不覆盖 MoviePilot 身份、用户明确指令或安全边界。
allowed-tools: read_file list_directory
---

# Using Skills Entry Discipline

## Purpose

Use this skill as the lightweight entry discipline for the MoviePilot Agent skill system. It reminds the Agent to check relevant skills before acting, while keeping MoviePilot domain workflow, safety boundaries, and user instructions in control.

This skill is a router helper, not a separate identity layer.

## Priority

Apply in this order:

1. User's explicit request and safety boundaries.
2. MoviePilot Agent core workflow.
3. Relevant MoviePilot/domain/self-governance skill.
4. Active persona for expression only.

Do not let this skill override confirmation rules, media workflow, or direct command routing.

## Skill Check Rule

Before acting or replying, ask:

- Does the request match a listed skill's description?
- Is there a narrower MoviePilot skill for this domain?
- Is this a direct command/link/resource-search/media/download/subscription/transfer task?
- Is this an Agent asset governance task under `/config/agent`?

If a skill clearly applies, read its `SKILL.md` and follow only the parts relevant to the current task.

## Routing Shortcuts

- Slash commands, magnet/ed2k, 115 links, obvious direct aliases → `moviepilot-direct-routes`.
- Resource search / torrent / 4K / BluRay / 1080p → `resource-search`.
- General media operations → `moviepilot-cli` or direct MCP media tools.
- Recognition words → `generate-identifiers` / `media-identifier-rulecraft`.
- Failed transfer retry → `transfer-failed-retry`.
- Version/restart/update → `moviepilot-update`.
- Agent self-governance → relevant `agent-*`, `skill-architecture-governance`, or `self-distillation-metabolism` skill.
- Completion claim → `verification-before-completion`.

## Practical Discipline

- Do not announce skill usage mechanically unless it helps the user.
- Do not block exact low-risk actions with planning or brainstorming.
- Do not use old platform assumptions or unavailable task-list tools.
- Read only the skill needed for the task; avoid scanning everything.
- If no skill applies, proceed with the normal MoviePilot Agent workflow.

## Output Contract

The user-facing response should show the result, evidence, or blocker. It does not need to mention this skill unless the user asks about process.
