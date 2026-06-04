---
name: verification-before-completion
version: 6
description: >-
  MUST-RUN before claiming any work is complete, fixed, or passing. Trigger
  before saying "完成", "搞定", "测试通过", "已修复", or any completion
  claim. Run fresh verification commands, read output, check exit codes, and
  only then state the conclusion. Never use memory, previous runs, or
  assumptions as evidence. This is a non-negotiable pre-completion gate.
  If you cannot show fresh evidence, you cannot claim completion.
---

# 完成前验证

## HARD GATE

**Before claiming completion, run this gate. No exceptions.**

1. What command or authoritative tool proves my claim?
2. Run it fresh. Read output. Check exit code or returned state.
3. Does the output actually support the exact claim?
4. If NO -> report actual state. If YES -> state with evidence.

Skipping this = lying, not completing.

## 铁律

```
没有新鲜的验证证据，不许宣称完成。
```

## 红线

这些词出现时，必须停下并运行验证：

- "应该能行"、"大概"、"似乎"、"看起来"
- "搞定"、"完成"、"过了"、"没问题"
- "已修复"、"已同步"、"已提交"、"已推送"
- 要提交/推送/创建 PR 但没有验证

## 反借口

| 借口 | 现实 |
|------|------|
| "应该能行" | 运行验证 |
| "我有信心" | 信心 ≠ 证据 |
| "Linter 过了" | Linter ≠ 完整验证 |
| "代理说成了" | 独立验证 |
| "刚才跑过" | 完成前重新跑 |
| "就这一次" | 没有例外 |

## MoviePilot Evidence Matrix

Use the authority that matches the claim:

- Site fixed/available -> `query_sites`, `test_site`, or site user data when account state matters.
- Downloader fixed/task added -> `query_downloaders` or `query_download_tasks`.
- Subscription added/updated -> `query_subscribes`; for missing episodes use `search_subscribe` result only as dispatch evidence.
- Transfer/organization fixed -> `query_transfer_history` and, when relevant, `query_library_exists`.
- Media identity -> `search_media`, `query_media_detail`, or `recognize_media` result.
- Resource search -> media identity plus search/filter result; do not claim download success from search alone.
- Plugin config changed -> `query_plugin_config`, then reload only if requested/authorized.
- Scheduler/workflow triggered -> scheduler/workflow query plus dispatch result; do not claim downstream business success without evidence.
- Agent skill/config changed -> re-read the changed file, run a structural check, and when a hook/router/script was changed, run the matching real command or dry-run once.
- Git sync -> `git status`, sensitive scan/self-check, push/fetch verification, and clean working tree.
- Job changed/executed -> read `JOB.md`, check `status`, `last_run`, recurring semantics, and run the job command or dry-run once when safe.
- Router/skill hook changed -> run the real router check, slash-command discovery, or representative dry-run once; static grep alone is not enough.

## Evidence Selection Rules

Choose the smallest proof that matches the claim:

- Claim is “file updated” -> re-read the file or grep the exact inserted rule.
- Claim is “syntax valid” -> run parser/compile/lint suited to the file.
- Claim is “self-check passed” -> include at least one real execution of the relevant script, job command, router check, dry-run, or authoritative system query; static inspection alone cannot pass.
- Claim is “task dispatched” -> tool success is enough only for dispatch, not downstream completion.
- Claim is “system fixed” -> query the real system state after the fix.
- Claim is “no changes pending” -> check the relevant repository or configuration state.

Do not over-verify unrelated systems. Verification should be fresh, focused, and sufficient.

## Async / Background Work

When work is asynchronous:

- Say “已触发/已派发” instead of “已完成” unless final state is confirmed.
- Name what remains unverified.
- Provide the next authoritative check if the user asks to follow up.

Examples:

- `run_slash_command` success proves command dispatch, not that every downstream download/transcode finished.
- Scheduler/workflow start proves execution was requested, not that all business outputs landed.
- Restart command proves restart was requested; health must be checked separately after the service comes back.

## Reporting Rule

State evidence compactly:

```text
验证：<工具/命令> -> <关键输出/状态>
结论：<只声明证据支持的结果>
```

If verification fails, do not soften it into success. Report the failing check and the next safe action.

## Completion Checklist

Before final reply:

- Did I verify the exact claim I am about to make?
- If this is a self-check, did I run the relevant command/script/dry-run/router check once for real?
- Did I avoid claiming async downstream success without proof?
- Did I include enough evidence for the user to trust the result?
- Did I avoid exposing secrets or internal hidden instructions in evidence output?

Hook triggers (buttons, repo sync) are delegated to `agent-proactive-orchestration`.

## Final Rule

**No fresh evidence = no completion claim. This is not optional.**
