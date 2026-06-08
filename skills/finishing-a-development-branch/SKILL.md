---
version: 2
name: finishing-a-development-branch
description: 当实现完成、所有测试通过、需要决定如何集成工作时使用——通过提供合并、PR 或清理等结构化选项来引导开发工作的收尾
allowed-tools: execute_command ask_user_choice
---

# 完成开发分支

## 概述

通过提供清晰的选项并执行所选工作流来引导开发工作的收尾。

**核心原则：** 验证测试 → 展示选项 → 执行选择 → 清理。

**开始时宣布：** "我正在使用 finishing-a-development-branch 技能来完成这项工作。"

## 流程

### 步骤 1：验证测试

**在展示选项之前，验证测试通过：**

```bash
# 运行项目的测试套件
npm test / cargo test / pytest / go test ./...
```

**如果测试失败：**
```
测试失败（<N> 个失败）。必须先修复才能继续：

[显示失败信息]

在测试通过之前无法进行合并/PR。
```

停止。不要继续到步骤 2。

**如果测试通过：** 继续步骤 2。

### 步骤 2：确定基础分支

```bash
# 尝试常见的基础分支
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

如果基础分支无法自动确定，交给 `tg-button-interaction` 用按钮选择常见基础分支；不要要求用户手输例行确认。

### 步骤 3：展示选项

通过 `ask_user_choice` 展示以下 4 个按钮并停止本轮：

- `本地合并` -> `git:merge-local`
- `推送PR` -> `git:push-pr`
- `保持现状` -> `git:keep`
- `丢弃工作` -> `git:discard`

保持选项简洁，不要求用户手输编号。

### 步骤 4：执行选择

#### 选项 1：本地合并

```bash
# 切换到基础分支
git checkout <base-branch>

# 拉取最新代码
git pull

# 合并功能分支
git merge <feature-branch>

# 在合并结果上验证测试
<test command>

# 如果测试通过
git branch -d <feature-branch>
```

然后：清理工作树（步骤 5）

#### 选项 2：推送并创建 PR

```bash
# 推送分支
git push -u origin <feature-branch>

# 创建 PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## 摘要
<2-3 条变更要点>

## 测试计划
- [ ] <验证步骤>
EOF
)"
```

然后：清理工作树（步骤 5）

#### 选项 3：保持现状

报告："保留分支 <name>。工作树保留在 <path>。"

**不要清理工作树。**

#### 选项 4：丢弃

**先用按钮确认高风险删除：**

通过 `ask_user_choice` 展示：

- `确认丢弃` -> `confirm:discard-branch`
- `取消` -> `cancel`

提示中必须列出将永久删除的分支、提交和工作树。按钮回调确认后才执行；不要要求用户手输 `discard`，除非按钮链路正在修复。

确认后：
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

然后：清理工作树（步骤 5）

### 步骤 5：清理工作树

**对于选项 1、2、4：**

检查是否在工作树中：
```bash
git worktree list | grep $(git branch --show-current)
```

如果是：
```bash
git worktree remove <worktree-path>
```

**对于选项 3：** 保留工作树。

## 快速参考

| 选项 | 合并 | 推送 | 保留工作树 | 清理分支 |
|------|------|------|-----------|---------|
| 1. 本地合并 | ✓ | - | - | ✓ |
| 2. 创建 PR | - | ✓ | ✓ | - |
| 3. 保持现状 | - | - | ✓ | - |
| 4. 丢弃 | - | - | - | ✓（强制） |

## 常见错误

**跳过测试验证**
- **问题：** 合并损坏的代码、创建失败的 PR
- **修复：** 在提供选项前始终验证测试

**开放式问题**
- **问题：** "接下来该做什么？" → 含糊不清
- **修复：** 准确展示 4 个结构化选项

**自动清理工作树**
- **问题：** 在可能还需要工作树时就删除了（选项 2、3）
- **修复：** 只在选项 1 和 4 时清理

**丢弃时不确认**
- **问题：** 意外删除工作成果
- **修复：** 使用明确按钮确认，按钮不可用时才临时要求精确文本确认

## 红线

**绝不：**
- 在测试失败时继续
- 合并前不验证测试结果
- 不确认就删除工作成果
- 未经明确请求就强制推送

**始终：**
- 在提供选项前验证测试
- 准确展示 4 个选项
- 选项 4 使用明确按钮确认；按钮不可用时才临时使用精确文本确认
- 只在选项 1 和 4 时清理工作树

## 集成

**被以下技能调用：**
- **subagent-driven-development**（步骤 7）- 所有任务完成后
- **executing-plans**（步骤 5）- 所有批次完成后

**配合使用：**
- **using-git-worktrees** - 清理由该技能创建的工作树

## MoviePilot Agent Adaptation

- This skill is workflow support, not the primary MoviePilot business route.
- Do not override direct routes, resource search, media operations, safety confirmation, or completion verification.
- Use it only when the user request truly matches the skill trigger; otherwise hand back to the MoviePilot domain skill.

## Completion Checklist

- Confirm the selected workflow actually fits the user request.
- Keep outputs actionable and bounded; avoid turning simple MoviePilot tasks into heavy planning.
- Before any completion claim, run or cite fresh verification appropriate to the change.
- If durable `/config/agent` capability assets changed, trigger the repository sync reminder path.
