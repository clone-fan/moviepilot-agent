---
version: 3
name: finishing-a-development-branch
description: 当实现完成、所有测试通过、需要决定如何集成工作时使用——通过提供合并、PR 或清理等结构化选项来引导开发工作的收尾
allowed-tools: execute_command ask_user_choice
---

# 完成开发分支

## Trigger Boundary

当实现完成、测试通过，并且用户需要决定如何处理当前开发分支时使用：本地合并、推送 PR、保持现状或丢弃。

不要让本技能抢占 MoviePilot 媒体、站点、下载、订阅、转移、插件运维或普通 Git 同步路线。若只是同步 Agent 仓库，优先走 `moviepilot-agent-git-maintenance`。

## Core Principle

验证测试 → 展示按钮选项 → 执行选择 → 必要清理。

不要在测试失败时继续集成；不要让用户手输例行选择；不要未确认就删除工作成果。

## Workflow

### 1. 验证测试

在展示选项前运行项目测试或用户指定的验证命令。

如果测试失败：报告失败数量和关键错误，停止，不继续合并或 PR。

### 2. 确定基础分支

优先自动识别 `main` / `master`：

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

如果无法确定，交给 `tg-button-interaction` 用按钮选择常见基础分支，不要求用户手输例行确认。

### 3. 展示按钮选项

通过 `ask_user_choice` 展示 4 个选项并停止本轮：

- `本地合并` -> `git:merge-local`
- `推送PR` -> `git:push-pr`
- `保持现状` -> `git:keep`
- `丢弃工作` -> `git:discard`

### 4. 执行选择

- **本地合并**：切换基础分支，拉取最新代码，合并功能分支，在合并结果上重新验证，通过后删除功能分支。
- **推送 PR**：推送功能分支并创建 PR；保留分支和工作树，便于后续评审修改。
- **保持现状**：只报告分支和工作树路径，不清理。
- **丢弃工作**：必须再次用按钮确认，提示中列出将删除的分支、提交和工作树；确认后才强制删除。

### 5. 清理工作树

只在 `本地合并` 和 `丢弃工作` 后清理工作树。`推送 PR` 与 `保持现状` 默认保留。

详细命令模板、PR body 示例和 worktree 清理命令见同目录 `REFERENCES.md`。

## Quick Matrix

| 选项 | 合并 | 推送 | 保留工作树 | 清理分支 |
|---|---|---|---|---|
| 本地合并 | 是 | 否 | 否 | 是 |
| 推送 PR | 否 | 是 | 是 | 否 |
| 保持现状 | 否 | 否 | 是 | 否 |
| 丢弃工作 | 否 | 否 | 否 | 是，需二次确认 |

## Red Lines

绝不：

- 测试失败时继续集成。
- 合并前不验证测试结果。
- 不确认就删除工作成果。
- 未经明确请求就强制推送。

始终：

- 在提供选项前验证测试。
- 用按钮展示结构化选项。
- 丢弃工作必须二次确认。
- 只在本地合并和丢弃后清理工作树。

## Integration

- `subagent-driven-development`：所有任务完成后可调用。
- `executing-plans`：所有批次完成后可调用。
- `using-git-worktrees`：清理由该技能创建的工作树。

## MoviePilot Agent Adaptation

本技能只是开发收尾支持，不是 MoviePilot 业务主路由。不得覆盖 direct routes、resource search、media operations、安全确认或完成验证。

## Completion Checklist

- 所选工作流确实匹配用户请求。
- 输出保持有界，不把简单 MoviePilot 任务变成重型开发流程。
- 完成声明前有新鲜验证证据。
- 若 `/config/agent` 能力资产变化，提醒走仓库同步路径。
