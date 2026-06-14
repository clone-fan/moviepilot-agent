# TG Button Interaction Reference

本文件是 `tg-button-interaction` 的低频参考资料。常规路由优先看 `SKILL.md`；只有排障按钮链路、设计按钮值或做 smoke test 时再读取这里。

## Callback Debug Checkpoints

当用户反馈按钮/TG 交互失效时，按层检查：

1. `ask_user_choice` 发送结果。
2. 通知日志包含 `buttons=[...]`。
3. Telegram 日志收到 callback。
4. 消息链处理 `agent_interaction:choice`。
5. `agent_interaction_manager.resolve` 结果。
6. 下一轮 Agent 是否收到选中值。
7. 上游模型是否空回复或失败。

如果 callback 到达但 Agent 没继续，说明问题在消息链或 Agent 入口，不要归咎用户。

## Typed Continuity Fallback

按钮链路修复期间，可接受与最后按钮匹配的文本标签、值或数字：

- `2` 或 `修复TG交互` 选择第 2 项。
- `取消` 取消。
- `确认执行` 确认具名动作。

这不是成功状态。必须继续恢复真实 callback 交互。

## Button Presets

- `继续执行` / `先看方案` / `取消`
- `确认执行` / `先只读检查` / `取消`
- `同意授权` / `仅查看` / `取消`
- `同步并推送` / `只提交` / `暂不同步` / `取消`
- `下载第1个` / `下载第2个` / `换一批` / `取消`
- `订阅第1季` / `订阅多季` / `取消`
- `确认重启` / `取消`
- `确认删除` / `取消`
- `查看插件` / `重载插件` / `取消`
- `按钮正常` / `继续测试` / `文本模式`

## Value Presets

```text
cancel
confirm:<action>
inspect:readonly
execute:<action>
download:<n>
subscribe:s<season>
git:push
git:commit
continue:<step>
smoke:ok
smoke:again
fallback:text
```

## Safe Smoke Test

Smoke test must not change system state. Suggested options:

- `按钮正常` -> `smoke:ok`
- `继续测试` -> `smoke:again`
- `文本模式` -> `fallback:text`

Health levels:

1. **Sent** — `ask_user_choice` reports that options were sent.
2. **Returned** — the Agent receives the selected value in the next turn.
3. **Resolved** — fresh logs show Telegram callback receipt and `agent_interaction` resolution.
4. **Healthy** — all three levels above are true in the same verification window.

Reporting rule:

- If only Sent + Returned are proven, report “主链路可用”.
- Only report “完美 / fully healthy” when fresh log evidence also proves Resolved.

If any step fails, remain in repair mode and continue debugging.
