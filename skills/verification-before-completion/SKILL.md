---
name: verification-before-completion
version: 2
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

1. What command proves my claim?
2. Run it fresh. Full output. Check exit code.
3. Does the output actually support the claim?
4. If NO → report actual state. If YES → state with evidence.

Skipping this = lying, not completing.

## 铁律

```
没有新鲜的验证证据，不许宣称完成。
```

## 红线

这些词出现时，必须停下并运行验证：

- "应该能行"、"大概"、"似乎"、"看起来"
- "搞定"、"完成"、"过了"、"没问题"
- 要提交/推送/创建 PR 但没有验证

## 反借口

| 借口 | 现实 |
|------|------|
| "应该能行" | 运行验证 |
| "我有信心" | 信心 ≠ 证据 |
| "Linter 过了" | Linter ≠ 完整验证 |
| "代理说成了" | 独立验证 |
| "就这一次" | 没有例外 |

## 最终规则

**No fresh evidence = no completion claim. This is not optional.**