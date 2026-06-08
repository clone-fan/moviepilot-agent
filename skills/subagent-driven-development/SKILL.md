---
version: 2
name: subagent-driven-development
description: 当在当前会话中执行包含独立任务的实现计划时使用；主 Agent 负责写入与确认，子代理仅做隔离的只读调查、审查或方案建议。
allowed-tools: task subagent_task execute_command read_file list_directory
---

# Subagent-Driven Development

## Purpose

Use subagents to keep complex implementation work focused without polluting the main context. In MoviePilot Agent, subagents are investigators and reviewers by default; the main Agent owns all writes, confirmations, and final user-facing conclusions.

This skill complements `executing-plans` and `dispatching-parallel-agents`:

- `executing-plans`: execute a written plan step by step.
- `dispatching-parallel-agents`: run independent read-only investigations in parallel.
- `subagent-driven-development`: coordinate a plan with subagent research/review checkpoints while the main Agent performs changes.

## When to Use

Use when:

- there is an implementation or optimization plan with several separable areas;
- independent investigation can reduce risk before writing;
- review is useful before claiming completion;
- multiple files or modules may interact but can be inspected separately.

Do not use when:

- one direct tool call is enough;
- the next step is a high-impact action needing user confirmation;
- subagents would need to modify files or system state.

## Workflow

1. **Read the plan or task context**
   - Identify target files, expected outcome, and verification standards.
2. **Split read-only scopes**
   - Give each subagent a narrow investigation or review question.
   - Include exact paths, known constraints, and “do not modify anything”.
3. **Main Agent decides**
   - Synthesize private subagent results.
   - Choose the smallest safe change.
4. **Main Agent writes**
   - Perform edits directly with the normal confirmation policy.
   - Do not ask subagents to write or trigger high-impact actions.
5. **Verify**
   - Run fresh checks in the main session.
   - Optionally ask a read-only subagent for review after changes.
6. **Close**
   - Report only synthesized results, evidence, and remaining blockers.

## Subagent Prompt Requirements

Each subagent task should include:

- scope and file/path/media/system area;
- whether it is read-only;
- what evidence to return;
- what decisions it should not make;
- any safety boundary such as no credentials, no writes, no restarts.

## Safety Rules

- Subagents must not ask the user questions.
- Subagents must not send user-facing messages.
- Subagents must not perform writes, downloads, deletion, plugin install/uninstall, restarts, or credential changes.
- Main Agent must still ask confirmation for high-impact actions.
- Do not paste subagent output verbatim; summarize only what matters.

## Verification Contract

Before completion, verify with fresh evidence:

- changed files re-read or structure-checked;
- scripts/plugins compiled or minimally run when safe;
- MoviePilot state queried after media/config actions;
- repository status checked before any sync handoff.

## Output Contract

Final response should include:

- which parts were delegated for read-only support, if any;
- what the main Agent changed;
- verification evidence;
- remaining confirmed blockers or next safe action.
