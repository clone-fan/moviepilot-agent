---
version: 2
name: executing-plans
description: 当已有书面实现计划且需要按检查点执行、验证和收尾时使用；适用于 MoviePilot Agent 可用工具链，不依赖外部任务清单工具。
allowed-tools: read_file list_directory execute_command edit_file write_file ask_user_choice
---

# Executing Plans

## Purpose

Execute an existing written plan without turning it into endless discussion. This skill is for implementation discipline, not for designing the plan itself.

Use it after a plan already exists and the next step is to carry it out safely inside the MoviePilot Agent environment.

## Entry Check

Before executing:

1. Read the plan or the referenced task context.
2. Identify the target files, commands, or MoviePilot operations.
3. Classify risk:
   - Low-risk `/config/agent` or `/config` local plugin asset change → execute directly when the user asked to continue.
   - High-impact action such as deletion, download start, credential change, plugin install/uninstall, restart, scheduler/workflow execution, or broad cleanup → ask for confirmation, preferably with buttons.
   - Ambiguous target or missing required input → ask one focused clarification.
4. If the plan is unsafe or internally inconsistent, stop before mutation and report the concrete issue.

## Execution Loop

For each plan item:

1. Re-read the item and its acceptance condition.
2. Perform the smallest correct action with the narrowest tool path.
3. Run fresh verification before moving on.
4. If verification fails, diagnose once with a narrower check; do not claim completion.
5. Continue to the next independent item only after the current item has evidence.

Do not wait for the user after every tiny step when the plan is clear and authorized.

## MoviePilot Agent Adaptation

- Use available MCP tools and shell diagnostics directly; do not reference unavailable external task-list tools.
- Use subagents only for independent read-only investigation or planning; main agent handles writes and confirmations.
- For `/config/agent` capability assets, prefer editing the relevant skill or memory file, then verify by re-reading or running structural checks.
- For MoviePilot media operations, follow the domain router: sites → identity → resources → download/subscription/transfer → verification.
- For repository synchronization, hand off to `moviepilot-agent-git-maintenance` after local verification.

## Verification Contract

A plan item is not complete until fresh evidence exists:

- File/config change → re-read changed lines or run syntax/structure checks.
- Script/plugin change → compile/check and, if safe, run the minimal command or reload after confirmation when required.
- Media task → query the relevant MoviePilot state after action.
- Job task → verify frontmatter status, schedule, last_run behavior, and command result.

## Failure Handling

If execution fails:

1. Report the exact command/tool error, not a vague “工具不可用”.
2. Try one smaller diagnostic path if safe.
3. If still blocked, state the blocker and the smallest user decision needed.

## Output Contract

Final response should include:

- what was executed;
- what verification passed;
- what remains blocked, if anything;
- the next safe handoff such as repository sync when relevant.
