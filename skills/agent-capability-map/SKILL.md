---
name: agent-capability-map
version: 1
description: >-
  Use this skill when the Agent needs to decide where a capability, rule,
  workflow, runtime anchor, script, job, document, persona change, plugin asset,
  or repository maintenance item should live. It provides a layered map of the
  Agent's durable assets so requests to “落实到 all”, “整理自身框架”, or “细化自身”
  do not bloat memory or scatter files.
allowed-tools: read_file list_directory
---

# Agent Capability Map

## Purpose

Provide a compact body map for Agent assets so durable knowledge lands in the right layer instead of bloating memory or scattering across directories.

## Use When

- “落实到 all”
- “整理自身框架” / “细化自身”
- “这个应该放哪里”
- “记忆、技能、脚本、job 怎么分”
- “不要一股脑塞进 memory”
- “参考人类构造补能力模块”

## Layer Map

- `memory/`: high-frequency global rules loaded every session: identity, safety, durable user preferences, global routing, verification boundaries. Never store secrets, one-time logs, transient state, or long checklists.
- `skills/`: reusable workflows, checklists, troubleshooting sequences, routing disciplines, and self-improvement procedures. Use when the content answers “how should I do this kind of task?”
- `scripts/`: deterministic repeatable commands or maintenance actions. Scripts should be minimal, documented by an owning skill/job, and safe around secrets.
- `jobs/`: scheduled or deferred work. Each job owns one directory with `JOB.md` and follows the pending/in_progress/completed/cancelled lifecycle.
- `runtime/`: non-secret current anchors and local state such as paths, repository mapping, active runtime notes, or generated state that should not be loaded as memory.
- `docs/archive/`: long-form references, old plans, investigation notes, or historical documents not needed every turn.
- `activity/`: recent interaction history; read-only for the Agent and never manually written.
- `personas/`: speaking style only. Persona never overrides MoviePilot identity, safety, workflow, or verification.
- `/config` local plugin libraries: user-owned MoviePilot plugin source, configs, release assets, and development material when explicitly requested.
- MoviePilot tools / slash commands: operational reflexes. Prefer existing commands, MCP tools, plugin commands, schedulers, and workflows before inventing new mechanisms.

## Placement Decision Tree

1. Must it be loaded every session? -> `memory/`
2. Is it a reusable procedure, checklist, or routing discipline? -> `skills/`
3. Is it deterministic executable logic? -> `scripts/`
4. Is it scheduled or deferred? -> `jobs/`
5. Is it current non-secret local state or an anchor? -> `runtime/`
6. Is it historical or long-form reference? -> `docs/archive/`
7. Is it only speaking style? -> persona definition
8. Is it local plugin development material under `/config`? -> local plugin library
9. Is it one-time conversation history? -> no manual asset; activity handles it

## Verification

After changing a capability asset:

- re-read the changed file
- check frontmatter for skills/jobs
- verify directory-name conventions
- run a minimal assertion when possible
- recommend repository sync for `/config/agent` capability changes

## Output Contract

State the selected layer, reason, assets changed or intentionally untouched, and verification evidence if changes were made.
