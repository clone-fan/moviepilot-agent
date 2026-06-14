---
version: 2
name: dispatching-parallel-agents
description: 当面对 2 个以上可独立只读调查、检索、诊断或规划的任务时使用；用 MoviePilot subagent 工具并发获取私有上下文，由主 Agent 综合决策。
allowed-tools: task subagent_task
---

# Dispatching Parallel Agents

## Purpose

Use isolated subagents to investigate multiple independent areas in parallel, then synthesize their private results into one main-agent decision.

This skill saves context and time. It is not a way to bypass confirmation, perform writes, or expose internal agent reports to the user.

## When to Use

Use it when there are two or more independent read-only subtasks, such as:

- site status and downloader status can be checked separately;
- media identity, library existence, and subscription history can be investigated in parallel;
- plugin config, scheduler state, and logs each need focused inspection;
- Agent skill/memory/job files need independent read-only audits.

Do not use it when:

- tasks have strict order dependencies;
- writes or destructive operations are required;
- subagents would race on shared mutable state;
- the task is small enough for one direct tool call.

## Dispatch Pattern

1. Split the work into independent scopes.
2. Build a handoff envelope for each subagent:
   - **role / scope**: which specialist perspective and exact area to inspect;
   - **input contract**: paths, IDs, titles, dates, constraints, and known context;
   - **expected outputs**: concise findings, evidence refs, risks, and recommended next check;
   - **done definition**: what counts as enough read-only evidence;
   - **forbidden actions**: no writes, no downloads, no deletion, no restarts, no credential changes, no user messaging.
3. Use `subagent_task` with `action=run` for a bounded batch, or `action=start` then `wait` when ongoing coordination is useful.
4. Read all results privately.
5. Synthesize only the operational conclusion for the user; do not paste subagent reports verbatim.
6. If a handoff affects governed assets, keep replay references such as file paths, commands, tool names, or evidence snippets so the main Agent can verify independently.

## Safety Rules

- Subagents are read-only investigators by default.
- Main Agent remains the only execution owner and final decision maker.
- Role packs, hive/squad patterns, or specialist labels are advisory templates only; they must not become a second orchestrator, supervisor hierarchy, route authority, or auto-merge owner.
- Main Agent must perform all state-changing actions directly under the confirmation policy.
- Main Agent must ask confirmation for high-impact actions even if a subagent recommends them.
- If a subagent result conflicts with tool evidence, verify with the authoritative MoviePilot tool or direct file read before acting.

## Common MoviePilot Subagent Mapping

- `system-diagnostician`: schedulers, settings, jobs, workflows, lightweight command output.
- `moviepilot-explorer`: source/config/log inspection and code-level clues.
- `resource-searcher`: site/resource quality checks.
- `subscription-analyst`: subscriptions, history, filters, identifiers.
- `download-diagnostician`: download tasks, transfer history, library state.
- `media-researcher`: media identity, people, episodes, metadata.

## Output Contract

Final response should state:

- which independent areas were checked;
- the synthesized conclusion;
- the smallest verified fix or next step;
- any action that still requires user confirmation.
