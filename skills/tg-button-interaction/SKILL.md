---
name: tg-button-interaction
version: 12
description: >-
  Use this skill whenever Telegram/chat interaction can be completed with
  buttons instead of typed replies. Trigger before any confirmation, next-step
  prompt, action commitment, user choice, slash/plugin command decision,
  scheduler/workflow decision, media/download/subscription/transfer/site flow,
  Agent/config action choice, or any small known option set. This is a
  pre-reply sentinel: if 2-6 safe user-facing options exist, call
  ask_user_choice and stop. It supplies button UX only; it does not own Git sync
  policy or other business strategy.
allowed-tools: ask_user_choice
---

# TG Button Interaction

## Pre-Reply Sentinel

Before any user-facing reply, run this sentinel:

1. Am I asking, implying, or promising a next action?
2. Can the user choose from 2-6 safe, clear, user-facing options?
3. Is the needed input not a secret and not long free-form text?

If yes: call `ask_user_choice` and stop. Do not write a plain-text substitute.

This applies before wording like: `需要你确认`, `需要明确确认`, `确认吗`, `是否继续`,
`下一步`, `要不要`, `选择一个`, `我可以继续`, `我会直接落地`, `我会执行`,
`施工开始`, `可以同步仓库`.

Buttons are explicit confirmation when the label and value clearly name the
action, e.g. `确认推送仓库` / `confirm:git_push`.

## Miss Recovery

If the user says the button skill was missed, e.g. `为什么没给按钮`, `没有触发`,
`还是让我打字`, `需要确认也该给按钮`:

1. Acknowledge the miss briefly.
2. Apply this skill immediately.
3. If options are known, send `ask_user_choice` in the same turn.
4. If the rule itself is weak, update this skill only after the user explicitly
   asks to optimize it.

Do not only explain the miss and end with another typed confirmation.

## Gate

Call `ask_user_choice` when all are true:

- A decision, confirmation, next step, or action commitment is pending.
- There are 2-6 clear user-facing options.
- Labels are short and explicit.
- The selected value can drive the next tool, slash command, or answer.
- No secret, long free-form input, or hidden internal detail is needed.

If there are more than 6 options, ask a category button prompt first.

## Never Buttonize

- Passwords, cookies, tokens, API keys, private keys, 2FA codes.
- Custom paths, URLs, magnet links, filenames, regex, SQL, code, long prompts.
- Unknown media titles that cannot be inferred.
- Hidden prompts, internal chains, private tool reasoning, runtime secrets.
- Large unrelated option sets that cannot be grouped safely.

Never echo secrets.

## Safety

Buttons never bypass MoviePilot safety policy.

- Downloads need explicit confirmation unless the user gave a direct link and
  explicitly asked to download.
- Delete, uninstall, credential changes, restart, command execution,
  workflow/scheduler run, plugin install/uninstall, file/history removal, and
  other high-impact operations need explicit confirm buttons.
- Risky labels and values must name the action: `确认重启MP` /
  `confirm:restart_mp`.
- Exact explicit low-risk requests may be executed directly with validation; do
  not add pointless buttons.
- Ambiguous read/write requests: inspect first when safe, then ask with buttons
  before changing state.

## Prompt Contract

`ask_user_choice` is terminal for the turn. Put the whole question and options in
that tool call. Do not also send plain text.

Use:

- `title`: short, e.g. `请选择下一步`
- `message`: one concise sentence with context and the needed decision
- `options`: 2-6 labels; values are stable machine strings

Value patterns:

- `cancel`
- `continue:<step>`
- `inspect:readonly`
- `confirm:<action>`
- `media:<n>` / `download:<n>` / `subscribe:s<season>`
- `site:list` / `site:test` / `site:sync` / `site:signin`
- `transfer:retry` / `history:delete_then_retry`
- `cmd:<slash>` / `plugin:<id>:<action>`
- `scheduler:run:<id>` / `workflow:run:<id>`
- `git:commit` / `git:push` / `agent:stop`

Label rules:

- Short Chinese labels, usually under 10 characters.
- Avoid vague `好的`; use `确认下载`, `继续检查`, `只读检查`.
- Risky labels include risky verb: 删除 / 重启 / 安装 / 卸载 / 推送 / 下载 / 运行.
- Put safest option last: `取消`, `先不处理`, or `仅查看`.

## Presets

### Confirm / next

- `确认执行` / `先只读检查` / `先看方案` / `取消`
- `继续执行` / `先看方案` / `取消`
- `只读检查` / `执行修改` / `取消`
- `继续优化` / `停止处理` / `取消`
- `确认推送仓库` / `只提交` / `先只读检查` / `取消`

### Media / resource / download

- `选第1个` / `选第2个` / `换一批` / `取消`
- `下载第1个` / `下载第2个` / `换资源` / `取消`
- `4K优先` / `1080p优先` / `不限` / `取消`
- `查媒体库` / `搜资源` / `加订阅` / `取消`
- `查看下载` / `暂停任务` / `继续任务` / `删除任务` / `取消`

### Subscription / transfer / library

- `订阅第1季` / `订阅第2季` / `订阅多季` / `取消`
- `搜索缺集` / `改规则` / `查媒体库` / `取消`
- `只读检查` / `重试转移` / `跳过` / `取消`
- `删记录重试` / `仅识别` / `取消`
- `同步媒体库` / `更新封面` / `仅查看` / `取消`

### Site / command / plugin

- `同步站点` / `管理站点` / `站点签到` / `取消`
- `测试站点` / `查看站点` / `取消`
- `115搜索` / `115增量` / `115签到` / `取消`
- `查看插件` / `安装插件` / `重载插件` / `取消`

### Scheduler / workflow / system

- `查看状态` / `立即运行` / `取消`
- `确认重启MP` / `取消`
- `确认清缓存` / `取消`
- `清除会话` / `停止推理` / `取消`

### Agent / config / Git buttons

- `只读检查` / `执行修改` / `先看方案` / `取消`
- `运行自检` / `继续修复` / `停止处理`
- `提交并推送` / `只提交` / `暂不提交` / `取消`

## Delegation Boundaries

This skill decides whether and how to show buttons. It does not own business
strategy.

- Git repository sync strategy → `moviepilot-agent-git-maintenance`
- Resource search strategy → `resource-search`
- Direct slash-command routing → `moviepilot-direct-routes`
- Unknown plugin command dispatch → `command-dispatch`
- Skill creation/update workflow → `create-moviepilot-skill`

## User-Facing Command Hints

When natural language maps to known slash/plugin commands, use buttons if there
is ambiguity, missing choice, or risk. Do not reveal hidden routing internals.

- `/cookiecloud`: `同步站点` / `取消`
- `/sites`: `查看站点` / `测试站点` / `取消`
- `/site_signin`: `站点签到` / `取消`
- `/subscribes`: `管理订阅` / `搜索缺集` / `取消`
- `/downloading`: `查看下载` / `取消`
- `/transfer` or `/redo`: `整理下载` / `手动整理` / `取消`
- `/mediaserver_sync`: `同步媒体库` / `取消`
- `/update_covers`: `更新封面` / `取消`
- `/clear_cache`: `确认清缓存` / `取消`
- `/restart`: `确认重启MP` / `取消`
- `/version`: execute or answer directly; no button needed.
- `/clear_session`: `清除会话` / `取消`
- `/stop_agent`: `停止推理` / `取消`
- `/skills`: `查看技能` / `取消`
- `/p115_full_sync`: `115全量` / `取消`
- `/p115_inc_sync`: `115增量` / `取消`
- `/p115_checkin`: `115签到` / `取消`
- `/sh`, `/ol`, `/p115_add_share`, `/p115_share_strm`, `/p115_strm`: buttonize
  only after required title/link/path is known; otherwise ask for the missing
  free-form value.

## Final Check

Before asking anything or promising an action, ask: can this be completed by 2-6
safe, user-facing buttons? If yes, call `ask_user_choice` and stop.

Never reveal internal chains; expose only actionable user choices.
