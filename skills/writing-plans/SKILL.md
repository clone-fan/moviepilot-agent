---
version: 2
name: writing-plans
description: 当需求需要多步骤执行、设计取舍或跨文件改动时使用；产出 MoviePilot Agent 可执行的简洁计划，并明确验证标准与风险确认点。
allowed-tools: read_file list_directory execute_command write_file edit_file ask_user_choice
---

# Writing Plans

## Purpose

Create an executable plan before complex work. The plan should reduce risk and make implementation clear, not become a long document for its own sake.

Use this skill when the user has a requirement that needs multiple coordinated steps, cross-file changes, or design choices.

## When to Plan

Plan first for:

- multi-file code, plugin, script, skill, or configuration changes;
- unclear implementation order;
- work with verification checkpoints;
- changes that may need user confirmation for high-impact actions;
- repository maintenance that should remain reversible.

Do not plan-block:

- exact low-risk edits already authorized;
- simple read-only diagnosis;
- direct MoviePilot slash commands or media operations covered by narrower skills.

## Spec-First Planning

For complex Agent/plugin/media work, write a mini spec before the steps:

- **Problem**: what concrete friction or missing capability is being solved.
- **Scope**: exact files, plugin, MoviePilot object, media chain, or config area.
- **Non-goals**: what will not be changed, imported, deleted, restarted, or downloaded.
- **Acceptance evidence**: the command/tool/state query that will prove each phase.
- **Risk gates**: what needs buttons or explicit confirmation.

Use this as a lightweight contract, not a separate documentation project. If the spec grows large, put long notes in `runtime/` or `docs/archive/` and keep the executable plan compact.


## Plan Shape

Keep the plan short and operational:

1. Goal and non-goals.
2. Current state to inspect.
3. Ordered steps with target files/tools.
4. Verification for each meaningful step.
5. Risk gates that require confirmation.
6. Rollback or safe recovery note when relevant.

Avoid copying long background references into the plan. Link or name supporting files when possible.

## MoviePilot Agent Rules

- Prefer existing MoviePilot tools, slash commands, and local skill workflows before inventing a custom path.
- For `/config/agent` assets, specify the exact skill/memory/job/script/runtime layer to change.
- For plugin work, separate source change, config update, reload, and capability verification.
- For media acquisition, preserve the site → identity → resource → download/subscription → transfer/library verification chain.
- For destructive or high-impact actions, place an explicit confirmation gate.

## Handoff to Execution

A good plan is ready for `executing-plans` when:

- steps are ordered;
- success criteria are concrete;
- risky operations are marked;
- required files or tools are named;
- no secret needs to be embedded.

## Output Contract

When producing a plan, include:

- the compact plan;
- what can be executed immediately;
- what requires confirmation;
- the first verification command or state query.
