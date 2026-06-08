---
name: tg-button-interaction
version: 19
description: >-
  MUST-CHECK before every user-facing reply. This is the single source of truth
  for button-first interaction: confirmations, continue/next-step, authorize,
  agree/cancel, retry, media/site/season/quality/action selection, command
  selection, repository/scheduler/workflow decisions, and safe smoke tests must
  use ask_user_choice whenever the channel can support it. Text fallback is only
  temporary continuity while diagnosing broken Telegram callbacks; it is never a
  successful replacement for real buttons.
allowed-tools: ask_user_choice
---

# TG Button Interaction

## Mission

Make the Agent interact through Telegram buttons whenever a bounded user choice
exists. The user should not need to type “下一步 / 继续 / 授权 / 同意 / 确认” for
choices that can be represented as buttons.

This skill owns interaction UX routing. Other skills must defer their user
choices to this skill instead of asking the user to type routine confirmations.

## Non-Negotiable Rules

1. **Buttons are the target state.** Text fallback is only a temporary repair
   bridge, not a completed solution.
2. **Button gate runs before every user-facing reply.** If a bounded choice is
   needed and the input is safe for buttons, call `ask_user_choice` and stop.
3. **No typed routine confirmations.** Do not request typed routine confirmations.
   Use buttons unless the value is secret, long free-form, or the callback chain
   is known broken.
4. **`ask_user_choice` is terminal.** Put the full prompt and all options in the
   tool call, then stop the turn. Do not duplicate the same question in text.
5. **Buttons never bypass safety.** They carry explicit confirmation for risky
   actions; they do not remove the confirmation requirement.

## Button Gate

Before replying, ask:

1. Does the next step need continue, authorize, agree, confirm, cancel, retry,
   or one choice among known options?
2. Can it be represented by 2-6 short labels?
3. Is the needed input not a password, token, Cookie, 2FA, private key, long
   path, URL, magnet, filename, regex, SQL, or code block?
4. Is the channel healthy/unproven, or is this a safe smoke test?

If all are yes, call `ask_user_choice` immediately and stop.

If the channel is reported broken, accept minimal typed continuity only long
enough to keep work moving, and route to debugging plus a safe smoke test.

## Must Buttonize

Use buttons for:

- 继续 / 下一步 / 重试 / 跳过;
- 授权 / 同意 / 确认 / 取消;
- destructive or high-impact confirmation with explicit risky labels;
- media result, season, episode, quality, site, torrent, command selection;
- inspect vs execute vs plan;
- plugin reload/install choice;
- scheduler/workflow run choice;
- Git commit/push/sync decisions;
- repository sync reminders;
- safe verification smoke tests.

## Do Not Buttonize

Ask for typed input when the user must provide:

- secrets: passwords, cookies, tokens, API keys, private keys, 2FA;
- long or exact values: paths, URLs, magnet links, filenames, regex, SQL, code;
- unknown media titles or ambiguous free-form text.

Never echo or store secrets.

## Broken Button Handling

When the user reports buttons/TG interaction are broken:

1. Treat the channel as **suspect** immediately.
2. Do not send an operational confirmation only through buttons.
3. Diagnose the real callback chain using `systematic-debugging`:
   - `ask_user_choice` send result;
   - notification log containing `buttons=[...]`;
   - Telegram log for received callback;
   - message-chain log for callback processing;
   - `agent_interaction_manager.resolve` result;
   - next Agent turn or upstream model failure.
4. If the callback arrives but the Agent does not continue, say so plainly and
   fix that layer; do not blame the user.
5. After repair, run a safe smoke test.

## Typed Continuity Fallback

While repairing, accept typed labels, values, or numbers that match the last
buttons. Examples:

- `2` or `修复TG交互` selects option 2.
- `取消` cancels.
- `确认执行` confirms the named action.

This is not success. Keep restoring real callback-based interaction.

## Button Message Rules

Labels:

- short Chinese labels, preferably under 10 characters;
- explicit risky verbs: 删除 / 重启 / 安装 / 卸载 / 推送 / 下载;
- safest option usually last: 取消 / 先不处理 / 仅查看.

Values:

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

## Presets

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

## Safe Smoke Test

A smoke test must not change system state. Use it after repair or when the user
asks to verify interaction.

Suggested options:

- `按钮正常` -> `smoke:ok`
- `继续测试` -> `smoke:again`
- `文本模式` -> `fallback:text`

Healthy only if all are true:

1. Button message is sent.
2. Telegram callback is logged.
3. Message chain processes `agent_interaction:choice`.
4. Agent receives the selected value and continues the expected next turn.

If any step fails, stay in repair mode and continue debugging.
