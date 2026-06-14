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

## Security Review Lane

Use a security-focused review path when the change touches credentials, auth/session logic, API endpoints, file handling, command execution, external URLs, plugin settings, database access, or logs.

Check at least:

- hardcoded secrets, token/cookie exposure, unsafe logging, and accidental persistence;
- authorization and confirmation gates for destructive or high-impact actions;
- command injection, path traversal, unsafe shell usage, SQL/string injection, SSRF/XSS-style URL or HTML handling;
- dangerous defaults in plugin config, broad file scopes, or missing dry-run/preview for cleanup actions;
- whether the proposed fix has a verification step and a safe rollback path.

Report severity as `CRITICAL / HIGH / MEDIUM / LOW` with evidence and concrete fix guidance. This lane is advisory; it does not replace MoviePilot safety boundaries.


## Review Matrix

For important changes, choose the review lens explicitly:

- **Correctness**: behavior matches the requirement and MoviePilot workflow.
- **Security**: credentials, auth, destructive actions, shell/path/URL/database risks.
- **Regression**: existing commands, routes, configs, plugin capabilities, or media flows still work.
- **Maintainability**: owner is right, duplication is avoided, and future routing is clear.
- **Evidence**: each claim has a fresh proof bundle.

A review finding must include severity, evidence, and a fix or deferral reason. Do not treat generic style opinions as blockers unless they affect safety, correctness, or maintainability.


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

## Documentation Review Checks

For docs, skills, plans, and reports, review:

- whether the stated route/owner matches the actual file changed;
- whether the document creates a duplicate source of truth;
- whether instructions are executable with available MoviePilot Agent tools;
- whether claims cite fresh evidence rather than summaries;
- whether long reference material should move to runtime/docs instead of skill or memory.

## Plugin / UI Documentation Consistency

For MoviePilot plugin or Agent capability changes, add a docs/config-surface lane when relevant:

- README, package metadata, config schema, UI labels, slash commands, workflow actions, and dashboard buttons describe the same behavior.
- Dangerous actions document preview/confirmation/result semantics, not just the happy path.
- Version, changelog, default config, and installed plugin capability output do not contradict each other.
- If a feature is only preview, linkage, or read-only inspection, the docs must not call it full takeover or complete replacement.

## Output Contract

Final response should include:

- what review/verification path was used;
- key finding;
- evidence after fixes;
- remaining risk or next handoff.
