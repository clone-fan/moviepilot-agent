---
version: 2
name: systematic-debugging
description: 遇到任何 bug、测试失败或异常行为时使用，在提出修复方案之前执行；要求先定位根因、再做最小修复、最后用新鲜证据验证。
allowed-tools: execute_command read_file list_directory task subagent_task
---

# Systematic Debugging

## Purpose

Use this skill whenever something is failing, flaky, inconsistent, or surprising. The goal is to fix the root cause with evidence, not to stack guesses.

Core rule:

```text
No root-cause evidence, no fix claim.
```

## When to Use

Use for:

- test, build, script, plugin, scheduler, workflow, or command failures;
- MoviePilot site/search/download/subscription/transfer/library anomalies;
- repeated Agent behavior failures such as tool misuse, missed verification, or wrong routing;
- performance or integration issues where the broken layer is unclear.

Do not use it to delay exact low-risk work that already has a known fix and verification path.

## Debugging Loop

1. **Read the failure**
   - Capture the exact error, command output, log line, status, file path, or tool result.
   - Do not paraphrase away important details.

2. **Reproduce or confirm state**
   - Run the smallest command or MoviePilot query that proves the issue still exists.
   - If it cannot be reproduced, collect more state instead of guessing.

3. **Localize the layer**
   - Identify where the chain breaks: configuration, authentication, scheduler, plugin, API, database, downloader, transfer, media recognition, filesystem, or Agent skill/router.
   - For multi-component flows, check boundaries in order and stop at the first unsupported assumption.

4. **Compare with a working reference**
   - Find a similar working config, command, plugin route, skill file, or media workflow.
   - Note the meaningful differences.

5. **Form one hypothesis**
   - State: “I think X is the cause because Y evidence.”
   - Change only what tests that hypothesis.

6. **Apply the smallest safe fix**
   - Respect confirmation policy for destructive/high-impact actions.
   - Avoid unrelated cleanup while debugging.

7. **Verify fresh**
   - Re-run the failing command/query or an authoritative equivalent.
   - Check exit code, returned state, logs, or file content.
   - If the check fails, do not stack random patches; return to localization with the new evidence.

## MoviePilot Evidence Hints

- Site/search issue → check enabled sites, auth/test result, search scope, recognition, and filters.
- Download issue → check downloader config, task status, save path, tracker/site health, and seeds.
- Subscription issue → check subscription state, season/episode counts, filters, sites, library existence, and history.
- Transfer/library issue → check transfer history, source path, permissions, recognition, target directory, and media server state.
- Plugin issue → check installed plugin, saved config, capabilities, logs, reload state, and registered commands/services.
- Agent skill issue → check relevant `SKILL.md`, memory/router references, stale platform terms, frontmatter, and minimal structure assertions.

## Escalation Rules

- After two failed fixes, pause and re-check the layer boundary.
- After three failed fixes, treat it as a design or assumption problem and produce options instead of another patch.
- If credentials, deletion, restart, download start, plugin install/uninstall, or external service changes are required, ask confirmation first.

## Output Contract

When reporting debugging work, include:

- observed failure evidence;
- root-cause hypothesis or confirmed cause;
- exact fix applied, if any;
- fresh verification evidence;
- remaining blocker if the root cause is not yet proven.
