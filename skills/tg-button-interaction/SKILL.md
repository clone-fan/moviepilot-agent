---
name: tg-button-interaction
version: 22
description: >-
  MUST-CHECK before every user-facing reply. This is the Agent's always-on
  interaction spine and primary UX weapon: confirmations, continue/next-step,
  authorize, agree/cancel, retry, media/site/season/quality/action selection,
  command selection, repository/scheduler/workflow decisions, and safe smoke
  tests must use ask_user_choice whenever the channel can support it. It should
  simplify every bounded interaction by choosing good defaults, offering compact
  action buttons, and preventing the user from typing routine confirmations.
  Text fallback is only temporary continuity while diagnosing broken Telegram
  callbacks; it is never a successful replacement for real buttons. For
  perfection claims, require both a live callback and log-level callback
  evidence.
allowed-tools: ask_user_choice execute_command
---

# TG Button Interaction

## Mission

Make buttons the Agent's always-on interaction spine, not an occasional confirmation widget.

Whenever the next user interaction can be represented as a small safe choice, this skill should quietly take the lead: reduce the user's burden, provide the right buttons, and let the conversation advance by clicking instead of typing “下一步 / 继续 / 授权 / 同意 / 确认”.

This skill owns bounded interaction UX. Other skills should delegate routine user choices here instead of inventing typed prompts.

## Operating Principle

For every user-facing reply, decide whether buttons can make the next step easier:

- **Follow closely** — stay present at every turn, especially before completion, confirmation, retry, branching, and next-step handoff.
- **Simplify** — turn routine typed replies into 2-6 clear buttons.
- **Lead with defaults** — when one safe continuation is obvious, include it as the first button; keep cancel/view-only as safe exits.
- **Preserve momentum** — do not ask the user to type ritual words; either execute an exact low-risk request or buttonize the remaining choice.
- **Stay safe** — buttons confirm risky actions, never bypass safety boundaries.

## Non-Negotiable Rules

1. **Buttons are the target state.** Text fallback is only temporary repair continuity.
2. **Button gate runs before every user-facing reply.** If a bounded choice is needed and safe for buttons, call `ask_user_choice` and stop.
3. **No typed routine confirmations.** Use buttons unless the value is secret, long free-form, or the callback chain is known broken.
4. **`ask_user_choice` is terminal.** Put the full prompt and options in the tool call, then stop. Do not duplicate the question in text.
5. **Buttons never bypass safety.** They carry explicit confirmation for risky actions; they do not remove the confirmation requirement.
6. **Do not overclaim perfection.** A returned button value proves the main chain works; “perfect / fully healthy” also requires fresh log evidence for callback receipt and interaction resolution.

## Always-On Button Gate

Before any final text reply, ask:

1. Is there a next action, confirmation, retry, branch, handoff, or likely follow-up?
2. Can it be represented by 2-6 short options?
3. Is the input not a password, token, Cookie, 2FA, private key, long path, URL, magnet, filename, regex, SQL, or code block?
4. Would buttons reduce typing, ambiguity, or “please continue” loops?

If all are yes, call `ask_user_choice` and stop.

If the user's request is exact, low-risk, and needs no choice, execute directly and verify instead of buttonizing.

If buttons are reported broken, accept minimal typed continuity only long enough to keep work moving, then diagnose and restore callback interaction.

## Interaction Patterns

### Continue / Next Step

Use when a task is complete enough to offer bounded next work.

Typical buttons:

- `继续下一步` -> `continue:next`
- `先自检` -> `inspect:selfcheck`
- `暂时停止` -> `cancel`

### Execute vs Inspect

Use when the next step may change state but read-only inspection is also useful.

- `直接执行` -> `execute:<action>`
- `先只读检查` -> `inspect:readonly`
- `取消` -> `cancel`

### Risk Confirmation

Use for destructive or high-impact operations.

- `确认删除` / `确认重启` / `确认下载` -> `confirm:<action>`
- `仅查看` -> `inspect:readonly`
- `取消` -> `cancel`

### Media / Resource Choice

Use for media results, seasons, torrents, quality, sites, and subscription branches.

- `下载第1个` -> `download:1`
- `订阅第1季` -> `subscribe:s1`
- `换一批` -> `continue:more`
- `取消` -> `cancel`

### Repair / Retry

Use after failures or partial success.

- `重试` -> `retry:<action>`
- `换方案` -> `continue:alternative`
- `只看原因` -> `inspect:reason`
- `取消` -> `cancel`

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
- safe verification smoke tests;
- any bounded next step that would otherwise make the user type a ritual reply.

## Do Not Buttonize

Ask for typed input when the user must provide:

- secrets: passwords, cookies, tokens, API keys, private keys, 2FA;
- long or exact values: paths, URLs, magnet links, filenames, regex, SQL, code;
- unknown media titles or ambiguous free-form text.

Never echo or store secrets.

## Smoke-Test Levels

Use the narrowest honest health claim:

1. **Sent** — `ask_user_choice` reports that options were sent.
2. **Returned** — the Agent receives a selected value such as `smoke:ok` or `smoke:again` in the next turn.
3. **Resolved** — fresh logs show callback receipt and interaction resolution.
4. **Healthy** — sent, returned, and resolved are all true.

If only level 2 is verified, say “主链路可用”, not “完美”.

## Broken Button Handling

When the user reports buttons/TG interaction are broken:

1. Treat the channel as suspect immediately.
2. Do not send an operational confirmation only through buttons.
3. Diagnose the callback chain with `systematic-debugging`.
4. If callback arrives but the Agent does not continue, fix that layer instead of blaming the user.
5. After repair, run a safe smoke test.

Detailed callback checkpoints, typed fallback examples, value presets, and smoke-test criteria live in `REFERENCES.md`.

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
inspect:selfcheck
inspect:reason
execute:<action>
retry:<action>
download:<n>
subscribe:s<season>
git:push
git:commit
continue:next
continue:more
continue:alternative
smoke:ok
smoke:again
fallback:text
```

## Output Contract

When a button choice is needed, call `ask_user_choice` and stop. When no choice is needed, continue normally.

For long summaries where tool/runtime constraints make inline buttons impractical in the same user-visible reply, send the summary first, then immediately follow with a separate `ask_user_choice` reply carrying the bounded next-step buttons. Do not wait for the user to type “下一步” just to reveal routine options. This two-message handoff is preferred over a text-only next-step instruction.

When the user has already chosen an exact next action such as `重载并验收 v1.5.5`, execute it directly instead of re-buttonizing the same decision.

For task summaries, prefer ending with buttons when a bounded next step exists. For button health reports, include the verified level and evidence source. Do not claim levels that were not freshly checked.
