---
version: 3
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
   - **Parallel boundary probe**: when the failure could span multiple independent
     layers (e.g. site + downloader + scheduler + logs), dispatch parallel
     read-only probes via `subagent_task` instead of serial tool calls:

     | Suspected layer | Subagent | Probe |
     |---|---|---|
     | Site/auth | `resource-searcher` | `query_sites` + `test_site` |
     | Downloader | `download-diagnostician` | `query_downloaders` + `query_download_tasks` |
     | Scheduler/workflow | `system-diagnostician` | `query_schedulers` + `query_workflows` |
     | Plugin/config | `system-diagnostician` | `query_plugin_config` + `query_plugin_capabilities` |
     | Code/log | `moviepilot-explorer` | read source files + grep logs |
     | Media/library | `media-researcher` | `query_library_exists` + `query_transfer_history` |

     Synthesize all subagent results privately, then form one hypothesis from
     the combined evidence. Fall back to direct tool calls if subagent
     infrastructure fails.

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


## Error Intake Contract

When the failure is an explicit error message, stack trace, command failure, or log exception, use this compact intake before hypothesizing:

1. **Classify** — category such as syntax, type, reference, runtime, network, permission, dependency, configuration, database, memory, MoviePilot site/auth, downloader, transfer, plugin, scheduler, or Agent router.
2. **Parse** — extract exact code/message, path, line, function, command/tool, status code, and the last meaningful stack/log frame.
3. **Match** — compare with a known working config, previous local pattern, plugin route, or similar MoviePilot workflow. Use pattern memory as evidence hints, not as proof.
4. **Analyze** — explain the root cause chain with concrete evidence; use a short 5-whys style chain only when the first cause is still too shallow.
5. **Resolve** — separate immediate workaround, proper fix, and prevention when all three are useful; otherwise apply the smallest safe proper fix.

Do not ask the user to paste more context if the current error already names a safe next diagnostic command or authoritative MoviePilot query.

## Replay Discipline

After a recurring error is fixed, preserve only reusable prevention value:

- stable prevention rule -> owning skill;
- deterministic check -> script;
- current local anchor or candidate pattern -> runtime;
- long incident evidence -> docs/archive;
- one-off stack trace or noisy log -> do not preserve manually.

A replay tag is useful only when it helps future routing or diagnosis; never create a second error database inside memory.

## MoviePilot Evidence Hints

- Site/search issue → check enabled sites, auth/test result, search scope, recognition, and filters.
- Download issue → check downloader config, task status, save path, tracker/site health, and seeds.
- Subscription issue → check subscription state, season/episode counts, filters, sites, library existence, and history.
- Transfer/library issue → check transfer history, source path, permissions, recognition, target directory, and media server state.
- Plugin issue → check installed plugin, saved config, capabilities, logs, reload state, and registered commands/services.
- Agent skill issue → check relevant `SKILL.md`, memory/router references, stale platform terms, frontmatter, and minimal structure assertions.

## Performance Optimization Advice

When the issue is performance, slowness, repeated retries, large output, or context bloat:

1. Establish a baseline: command time, output size, query count, line count, API/tool calls, or user-visible latency.
2. Identify the hot path or repeated work before optimizing.
3. Prefer removing unnecessary work over adding caching or complexity.
4. Verify improvement with the same measurement or a clearly comparable check.
5. If measurement is not possible, label the change as a readability/structure improvement, not a proven performance fix.

Do not import external benchmark frameworks unless the project already uses them or the user explicitly asks.


## Regression And Performance Signals

Treat regression evidence as a debugging input when:

- a previously passing command, route, plugin capability, scheduler, or media workflow now fails;
- execution time, output size, repeated retries, or context growth suddenly increases;
- a UI/plugin/API change breaks an older command or expected state query.

Debug regressions by comparing current evidence with the last known working command, config, route, or file version. If no baseline exists, create a minimal baseline before changing behavior.

## Error Fingerprints

When there are many logs or repeated failures, group by stable fingerprints before fixing:

- exception type, command, plugin ID, scheduler/job ID, route, status code, path, or first meaningful stack frame;
- count and recency if available, but do not build a new observability service unless the project already has one;
- pick the first actionable boundary failure, not the noisiest downstream symptom.

For MoviePilot Agent work, lightweight grep/log grouping is enough unless the user explicitly asks to integrate an external error platform.

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
