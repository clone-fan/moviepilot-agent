# 完成开发分支命令参考

本文件是 `finishing-a-development-branch` 的低频命令模板。常规执行优先看 `SKILL.md`；只有进入具体分支收尾动作时再读取这里。

## 测试验证

```bash
# 根据项目类型选择其一或使用用户指定命令
npm test
cargo test
pytest
go test ./...
```

## 本地合并

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

## 推送并创建 PR

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

## 丢弃工作

丢弃前必须二次确认，并在确认提示中列出将永久删除的分支、提交和工作树。

确认后：

```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

## Worktree 清理

对于本地合并和丢弃工作：

```bash
git worktree list | grep $(git branch --show-current)
git worktree remove <worktree-path>
```

对于推送 PR 和保持现状：保留工作树。

## 常见错误

- 跳过测试验证：会合并损坏代码或创建失败 PR。
- 开放式提问：应使用四个结构化按钮，不问“接下来做什么”。
- 自动清理工作树：只在本地合并和丢弃工作后清理。
- 丢弃时不确认：必须用按钮二次确认；按钮不可用时才临时使用精确文本确认。
