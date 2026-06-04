---
name: work-completion-workflow
version: 7
description: 工作完成标准流程 - 用于任务完成后的主动闭环：最小验证、整理归纳、必要归档与 hook 检查。避免机械式申请、逐步等待、手写 activity 或污染长期记忆。
allowed-tools: "edit_file write_file read_file"
compatibility: "适用于需要整理收尾的工作；不替代 verification-before-completion、agent-proactive-orchestration 或 moviepilot-agent-git-maintenance"
---

# 工作完成标准流程

## 目标

完成工作后主动收束，而不是让用户踢一步走一步。

本技能只负责收尾整理纪律；不负责业务策略，不替代完成前验证，不手写 activity log。

## 主动闭环

当用户要求完成、整理、归档、自检或收尾时，按以下顺序直接推进：

1. **确认实际改动**
   - 列出修改过的文件和职责范围。
   - 区分运行态、仓库、memory、jobs、scripts、docs。

2. **最小验证**
   - 使用能证明本次结论的实际检查。
   - 如果要宣称完成，必须遵循 `verification-before-completion`。

3. **整理归纳**
   - 总结做了什么、为什么这样归位、哪些职责边界被收敛。
   - 删除或指出临时文件、备份文件、冗余归档物。

4. **必要归档**
   - 只有历史资料、一次性参考材料才进入 `/config/agent/docs/archive/`。
   - 不把缓存、日志、脚本、Job 定义或运行态文件塞进 docs。

5. **Hook 检查**
   - `/config/agent` 能力资产变更并验证通过 → hand off 到
     `moviepilot-agent-git-maintenance` 提示仓库同步。
   - 需要用户选择 → hand off 到 `tg-button-interaction`。
   - 涉及 Git 提交/推送 → hand off 到 `moviepilot-agent-git-maintenance`。
   - 行动模式不清楚 → hand off 到 `agent-proactive-orchestration`。

6. **证据化汇报**
   - 汇报修改文件、验证输出、剩余阻塞。
   - 不用空泛"搞定"，用证据支撑。

## 禁止事项

- 不要先"申请检查 bug"再等用户批准；能自检就直接自检。
- 不要先"申请整理"再等用户批准；用户已要求整理时直接整理。
- 不要手写 activity log；活动日志由系统自动维护。
- 不要把单次过程写进长期记忆。
- 不要把稳定规则以外的内容写入 `/config/agent/memory`。
- 不要把脚本放 jobs，或把 Job 定义放 scripts/docs。
- 不要用道歉代替收束；给出原因、修正和验证。
- 不要把完成流程拆成"下一步、下一步、下一步"；能闭环就闭环。

## 何时更新 memory

只有当用户明确要求记住，或出现稳定、长期、跨任务复用的偏好/边界时，才考虑写入 memory。

单次任务过程、执行日志、临时结论、失败复盘，不进入长期记忆。

## 完成标志

只有在有新鲜验证证据时，才能说完成。最终回复应包含：

- 改了哪些文件。
- 验证证据。
- 是否触发了必要 hook。
- 是否还有阻塞或待用户选择。

验证纪律由 `verification-before-completion` 统一管理；Hook 触发由 `agent-proactive-orchestration` 统一路由。

## Distilled Rules

### Closure Patterns

- For `/config/agent/skills` changes: re-read frontmatter, check name equals directory, version exists, trigger description is concrete, and completion/safety rules exist.
- For jobs: verify `JOB.md` frontmatter, status lifecycle, last_run semantics, and that scripts live under `/config/agent/scripts`.
- For Git-backed capability assets: run the dedicated Git maintenance workflow after local validation; do not mix commit/push rules into the business skill.
- For media operations: completion means MoviePilot state changed or an external handoff was dispatched, not just that a plan was written.
- For failed or partial work: report exact remaining blockers and the smallest next safe action.

### Closure Steps

1. Verify the changed state with the smallest fresh check.
2. Summarize only what changed, what was validated, and any remaining blocker.
3. If `/config/agent` capability assets changed, trigger the repository sync reminder through `moviepilot-agent-git-maintenance`.
4. Do not write single-task history into memory; activity logs handle that.
5. Do not archive runtime caches, logs, secrets, or transient files.

### Output Shape

- Result first, evidence second, next blocker or optional sync choice last.
- Close with evidence, not ceremony. Avoid vague claims like "应该可以了".