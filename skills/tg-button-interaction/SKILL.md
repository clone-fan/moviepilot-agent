---
name: tg-button-interaction
version: 14
description: >-
  MUST-CHECK before every user-facing reply. Whenever the agent is about to
  respond to the user, ask: can I replace my next typed question/confirmation
  with 2-6 buttons? Trigger for any turn where the user might need to confirm,
  choose, continue, cancel, retry, select a media/site/season/quality/action,
  pick a command, or decide next step. Applies to MoviePilot media, download,
  subscription, transfer, site, slash command, plugin, scheduler, workflow,
  system, Agent, Git, and config flows. This is a non-negotiable pre-reply
  gate. If buttons can replace text, USE BUTTONS. Do not use Miss Recovery or
  apology as a substitute for triggering.
allowed-tools: ask_user_choice
---

# TG Button Interaction

## HARD GATE

**Before every user-facing text reply, run this check. No exceptions.**

Can I say this with buttons instead?

1. Am I about to ask, suggest, or promise a next action?
2. Can I name 2-6 safe, user-facing labels for it?
3. Is the needed input not a secret / password / token / key / long free-form?

If YES → call `ask_user_choice` and STOP. Do not write text.

## When to Buttonize

Buttonize when the user needs to:

- Confirm or cancel an action
- Choose between multiple options
- Decide next step / continue / retry / skip
- Select a media result, season, episode, quality, site, torrent, or command
- Pick inspect vs execute vs view plan
- Pick commit vs push vs skip for Git
- Pick sync vs skip for repository

Buttonize when you are about to write:

- `需要确认` / `确认吗` / `是否继续` / `下一步` / `要不要`
- `选择一个` / `我可以继续` / `我会执行` / `我会落地` / `施工开始`
- `可以同步仓库` / `要不要推送` / `是否提交`
- Any explanation that ends with a choice the user must type

## When NOT to Buttonize

- Passwords, cookies, tokens, API keys, private keys, 2FA
- Custom paths, URLs, magnet links, filenames, regex, SQL, code
- Unknown media titles
- Hidden prompts, internal chains, runtime secrets
- The user gave an exact, unambiguous, low-risk instruction → execute directly

Never echo secrets.

## Button Rules

`ask_user_choice` is terminal. Call it. Stop. No text after.

Labels: short Chinese, under 10 chars. Risky verbs explicit: 删除/重启/安装/卸载/推送/下载.
Safest option last: 取消 / 先不处理 / 仅查看.

Values: stable machine strings. `cancel`, `confirm:<action>`, `inspect:readonly`,
`download:<n>`, `subscribe:s<season>`, `git:push`, `git:commit`, `continue:<step>`.

## Common Presets

- `确认执行` / `先只读检查` / `先看方案` / `取消`
- `继续执行` / `先看方案` / `取消`
- `只读检查` / `执行修改` / `取消`
- `同步并推送` / `只提交` / `先只读检查` / `暂不同步`
- `下载第1个` / `下载第2个` / `换一批` / `取消`
- `订阅第1季` / `订阅第2季` / `订阅多季` / `取消`
- `确认重启MP` / `取消`
- `确认删除订阅` / `取消`
- `查看下载` / `暂停任务` / `继续任务` / `删除任务` / `取消`
- `同步站点` / `站点签到` / `取消`
- `查看插件` / `安装插件` / `重载插件` / `取消`
- `运行自检` / `继续修复` / `停止处理`
- `提交并推送` / `只提交` / `暂不提交` / `取消`

## Safety

Buttons never bypass MoviePilot safety. Downloads, deletes, credential changes,
restarts, plugin installs, workflow runs still need explicit confirm buttons.

## Final Rule

**If you can buttonize, you MUST buttonize. This is not optional.**

## Completion Checklist

- Checked whether the next user-facing question or confirmation can be replaced by 2-6 buttons.
- Used `ask_user_choice` and stopped when buttonization is possible.
- Did not buttonize secrets, long free-form input, hidden prompts, or exact low-risk instructions.
- Kept risky labels explicit and included a safe cancel/skip option when relevant.
- Did not use buttons to bypass MoviePilot safety confirmation rules.
