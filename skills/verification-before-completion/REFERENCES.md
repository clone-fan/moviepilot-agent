# 完成前验证参考

本文件是 `verification-before-completion` 的低频参考资料。常规执行优先看 `SKILL.md`；需要扩展 proof floors、异步规则、性能基线或报告模板时再读取这里。

## Red Words

出现这些词前必须停下并验证：

- “应该能行”、“大概”、“似乎”、“看起来”
- “搞定”、“完成”、“过了”、“没问题”
- “已修复”、“已同步”、“已提交”、“已推送”
- 要提交 / 推送 / 创建 PR 但没有验证

## Preview Before Apply

广泛写入维护时，尽量使用预览边界：

1. **Precheck** — 确认根目录、目标范围、风险。
2. **Preview** — 列出计划写入或影响对象，不突变。
3. **Apply** — 只执行已授权的有界改动。
4. **Postcheck** — 运行对应 proof floor。

Preview 只能证明计划范围，不能证明最终状态已改变。

## Evidence Selection Rules

- “文件已更新” -> 重读文件或 grep 精确规则。
- “语法有效” -> 运行适合格式的 parser / compile / lint。
- “自检通过” -> 至少一次真实运行相关脚本、job 命令、路由检查、dry-run 或权威查询；静态检查不能单独证明。
- “任务已派发” -> 工具成功只证明派发，不证明下游完成。
- “系统已修复” -> 修复后查询真实系统状态。
- “无待提交变更” -> 检查相关仓库或配置状态。

## Quality Assurance Distillation

吸收外部验证/QA 候选时，只保留证明质量原则，不引入第二套评分系统：

- **Verification quality**：每个完成声明需要 freshness、authority、scope、narrow claim。
- **Report generation**：报告保留 `Command/Tool -> Output/State -> Claim`，不要装饰性摘要遮住失败。
- **Regression detection**：行为变更要比较 baseline 和 after；没有 baseline 就声明限制。
- **Rollback thinking**：高风险变更应用前先说明可回退路径；不自动回滚。
- **Quality floor**：证据应能被用户或未来 Agent 从命令、工具、文件或状态查询复现。

拒绝：外部 truth-score 仪表盘、Claude Flow 命令、自动回滚系统、不存在的 CI/CD 假设。

## Async / Background Work

异步工作：

- 只说“已触发 / 已派发”，除非最终状态确认。
- 说明仍未验证什么。
- 给出下一条权威检查路径。

示例：

- `run_slash_command` 成功证明命令派发，不证明下载/转码完成。
- scheduler/workflow start 证明执行被请求，不证明业务产出已落地。
- restart command 证明重启被请求，服务回来后要单独健康检查。

## Performance Proof

性能或回归声明必须有 baseline 和 after：

```text
Baseline: <command/tool/state> -> <metric>
After: <same or comparable check> -> <metric>
Claim: <only the measured improvement or regression status>
```

可用轻量指标：运行时、工具调用次数、行数、输出大小、pass/fail 状态、重复 owner 数量、MoviePilot 状态查询结果。

## Report Template

```text
验证：<工具/命令> -> <关键输出/状态>
结论：<只声明证据支持的结果>
范围：<文件/配置/对象>
```

如果验证失败：

```text
验证失败：<工具/命令> -> <失败输出>
当前状态：<已写入/已触发/待验证/未生效>
下一步：<最小安全动作>
```
