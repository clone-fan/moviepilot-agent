---
version: 2
name: using-git-worktrees
description: 当需要开始与当前工作区隔离的功能开发或执行实现计划之前使用——创建具有智能目录选择和安全验证的隔离 git 工作树。
allowed-tools: execute_command read_file list_directory ask_user_choice
---

# 使用 Git 工作树

## Purpose

Git worktree 用于在同一仓库下创建隔离工作区，适合并行开发、执行实现计划、接收代码审查修改或处理高风险改动。

这是开发隔离辅助技能，不是 MoviePilot 媒体业务主路线。普通搜索、订阅、下载、转移、站点任务不要因此变成重型开发流程。

## When To Use

使用场景：

- 用户要求开始一项需要改代码或多文件实现的开发任务；
- 当前仓库已有未完成工作，继续修改会污染工作区；
- 需要保留主工作区稳定，同时试验新方案；
- 执行书面计划、TDD、代码审查修改或插件开发前需要隔离。

不使用场景：

- 只读排查；
- 单文件低风险配置修正；
- `/config/agent` 小型 skill/memory 调整；
- MoviePilot 业务操作可直接通过 MCP/插件/slash command 完成。

## Directory Selection

按优先级选择：

1. 仓库内已有 `.worktrees/`，优先使用。
2. 仓库内已有 `worktrees/`，次选。
3. 项目文档明确指定 worktree 目录时，遵循项目约定。
4. 仍无约定时，用按钮询问用户：`.worktrees/`、`worktrees/`、外部临时目录、取消。

项目内目录必须确认被 Git 忽略，避免工作树内容被误跟踪。

```bash
git check-ignore -q .worktrees || git check-ignore -q worktrees
```

若未忽略，先说明风险；只有在用户授权或任务已授权修改仓库配置时，才追加 `.gitignore` 并验证。

## Creation Workflow

1. 确认当前路径是 Git 仓库：
   ```bash
   git rev-parse --show-toplevel
   git status --short --branch
   ```
2. 选择目录并生成分支名，分支名应描述任务，例如 `feature/agent-ops-buttons`。
3. 创建工作树：
   ```bash
   git worktree add <path> -b <branch>
   cd <path>
   ```
4. 自动识别项目类型并做最小依赖准备：
   - `package.json` → `npm install` 或项目约定命令；
   - `pyproject.toml` / `requirements.txt` → Python 依赖准备；
   - `go.mod` → `go mod download`；
   - `Cargo.toml` → `cargo build`。
5. 运行最小基线验证。若失败，报告失败并询问是否继续排查，不要假装基线干净。

## Safety Rules

- 不在未确认目录约定时擅自创建大范围目录。
- 不把 worktree 目录加入 Git 跟踪。
- 不带着失败基线继续实现，除非用户明确要求继续。
- 不为简单 MoviePilot 操作创建工作树。
- 不删除工作树或分支，除非用户明确要求。

## Handoff

创建成功后报告：

- 工作树路径；
- 分支名；
- 基线验证结果；
- 下一步要在隔离工作区执行的任务。

开发完成后的清理、合并或保留，由 `finishing-a-development-branch` 接管。

## MoviePilot Agent Adaptation

- 本技能只提供开发隔离能力，不覆盖 MoviePilot Agent 身份和业务主链路。
- 对 `/config/agent` 能力资产的小改动，通常直接改并验证，不必创建 worktree。
- 对独立插件仓库、样式仓库、Agent 仓库的大型实现或高风险实验，优先使用 worktree。

## Verification

完成前至少验证：

```bash
git worktree list
git status --short --branch
```

如修改了仓库配置或 `.gitignore`，还要验证相关目录确实被忽略。
