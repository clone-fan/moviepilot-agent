---
version: 2
name: requesting-code-review
description: 完成任务、实现重要功能或合并前使用，用于验证工作成果是否符合要求；在 MoviePilot Agent 中优先使用只读子代理或本地验证命令，不依赖外部审查者。
allowed-tools: task subagent_task execute_command read_file list_directory
---

# Requesting Code Review

## Purpose

Use this skill to get an independent check before claiming that an important implementation, skill change, plugin change, or repository sync is ready.

It is a verification aid, not a replacement for the main Agent's responsibility. The main Agent still owns final decisions, writes, confirmations, and user-facing conclusions.

## When to Use

Use before:

- merging or syncing meaningful `/config/agent` capability changes;
- shipping a local plugin change;
- claiming a bug fix is stable;
- completing a multi-file implementation;
- touching workflows, jobs, scripts, or routing rules that affect future behavior.

Skip when the change is a tiny text-only correction already covered by a direct structural check.

## Review Paths

Choose the smallest adequate path:

1. **Local verification only**
   - For simple file edits, run syntax, frontmatter, grep, or command checks.
2. **Read-only subagent review**
   - For multi-file or cross-domain changes, delegate isolated review with `task` or `subagent_task`.
   - Ask the subagent to inspect scope, risks, missing validation, and stale references.
3. **Domain-specific check**
   - For MoviePilot media/config/plugin work, use the relevant MoviePilot tool or skill to verify real state.

## Review Brief Template

Give reviewers compact context:

- changed files or operations;
- intended behavior;
- risk boundaries;
- commands already run;
- exact questions to answer.

Do not expose secrets. Do not ask subagents to perform writes.

## Integration Rules

After review:

1. Read the findings.
2. Fix only confirmed, relevant issues.
3. Re-run fresh verification.
4. If the review is inconclusive, say so; do not inflate it into success.

## Output Contract

Final response should include:

- what review/verification path was used;
- key finding;
- evidence after fixes;
- remaining risk or next handoff.
