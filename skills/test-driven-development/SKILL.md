---
version: 2
name: test-driven-development
description: 在实现功能、修复 bug 或改变可执行行为前使用；要求先定义失败验证或可观察验收，再做最小实现，最后用新鲜证据确认通过。
allowed-tools: execute_command read_file list_directory
---

# Test-Driven Development

## Purpose

Use this skill to keep implementation honest: prove the current behavior fails or is missing, make the smallest change, then prove the target behavior works.

It is a discipline for executable behavior, not a ritual that blocks every small documentation, frontmatter, or configuration cleanup.

## When to Use

Use for:

- new executable features;
- bug fixes;
- behavior changes in scripts, plugins, workflows, jobs, APIs, or routing;
- refactors where behavior must remain stable.

Use a lighter verification path instead of full TDD for:

- pure documentation edits;
- skill frontmatter fixes;
- small memory/routing wording changes;
- formatting-only changes;
- configuration changes where an authoritative state query is the correct proof.

## Core Loop

1. **Define the behavior**
   - State the expected behavior and the current failure or missing capability.
2. **Create a failing check**
   - Prefer an existing test command.
   - If no test framework exists, use a small script, dry-run, grep assertion, parser check, or authoritative MoviePilot query that should fail before the fix.
3. **Verify red**
   - Run the check and confirm it fails for the expected reason.
   - If it fails for setup/syntax reasons, fix the check first.
4. **Make the smallest change**
   - Change only what is needed to satisfy the behavior.
   - Do not bundle unrelated cleanup.
5. **Verify green**
   - Re-run the same check and any minimal related regression checks.
6. **Refactor only if needed**
   - Keep the green checks passing.

## Property And Invariant Checks

When unit tests are unavailable, define property-style checks for behavior that should always hold:

- parser/frontmatter inputs should preserve required fields and reject malformed structures;
- routing changes should keep the intended owner discoverable and avoid duplicate owners;
- plugin/config operations should preserve existing keys unless intentionally removed;
- media workflows should not confuse recognition, search, download, subscription, transfer, and library states;
- cleanup or file operations should never expand beyond declared scope.

Use generated or varied inputs only when safe and bounded. For MoviePilot operations, prefer read-only state queries and dry-runs over synthetic destructive tests.


## MoviePilot Agent Adaptation

Acceptable checks include:

- `python -m py_compile` or a focused script run;
- plugin capability/config queries after safe reload when authorized;
- scheduler/workflow/query tools for state behavior;
- skill/frontmatter structure assertions for Agent skill changes;
- `git diff`/`git status` for repository hygiene;
- media/library/subscription/download state queries for MoviePilot behavior.

Do not force a unit-test framework where the repository or task does not have one. The important part is observable red/green evidence.

## Safety Rules

- Do not use TDD to bypass confirmation for destructive or high-impact actions.
- Do not start downloads, delete files, change credentials, install/uninstall plugins, restart services, or trigger workflows merely to create a test without user consent.
- For risky operations, design a dry-run or read-only check first.

## Output Contract

When this skill shapes the work, report:

- the failing check or baseline evidence;
- the smallest change made;
- the passing verification evidence;
- any remaining risk or skipped test with reason.
