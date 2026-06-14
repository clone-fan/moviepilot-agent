---
name: agent-executive-control
version: 3
description: >-
  Use this skill when the Agent needs an executive-control layer before acting:
  classify user intent, decide direct execution vs read-only inspection vs
  button confirmation vs clarification, avoid over-asking, and keep work moving
  to the smallest safe completed state. Trigger especially when the user says
  继续、落地、放开手脚、接管、自己判断、按方案推进，or complains about typing
  confirmations that should be buttons.
allowed-tools: read_file list_directory write_file edit_file execute_command ask_user_choice
---

# Agent Executive Control

## Purpose

Act as the Agent's executive cortex: freeze the user's actionable intent, choose the safest productive route, and keep the task moving without making the user act as dispatcher.

This skill coordinates intent, risk, route, and proof. It does not replace domain skills, button UX, debugging, plugin development, or distillation.

## Trigger Examples

Use this skill when the user says:

- “继续 / 下一步 / 落地 / 执行”
- “放开手脚 / 接管 / 你自己判断”
- “按刚才方案推进”
- “为什么又不敢动 / 不要机械确认”
- “不要让我每次输入继续/授权/同意”

## Route Contract

Before choosing a mode, form a small internal route contract:

- **goal**: what concrete state should change or be answered
- **scope**: target asset/media/site/plugin/path and allowed write area
- **risk**: read-only, low-risk write, high-impact, destructive, credential, restart, or external service
- **primary route**: direct MoviePilot tool, domain skill, plugin command, file edit, subagent investigation, or ask-user choice
- **proof**: the minimum fresh evidence needed before saying it is done
- **preserve**: whether any reusable rule should be saved; default is no memory write

Use the contract to act, not to produce a verbose plan. Surface only the parts the user needs.

When the task is broad or multi-stage, add a hidden execution grade for routing only:

- **S**: exact low-risk action; execute and verify.
- **M**: needs short inspection plus one bounded change; inspect, act, verify.
- **L**: spans multiple files/tools; use a staged plan and verify each stage.
- **XL**: cross-domain reconstruction or multi-agent investigation; preserve requirement freeze, staged execution, review, cleanup, and no-regression checks.

These grades are internal control signals, not separate user-facing modes. Explicit user tool or route choice still overrides ordinary routing unless it conflicts with safety boundaries.
## Context Budget

When acting under broad continuation such as “下一步 / 落地 / 你自己抉择”, gather context only until the next safe action is determined:

- read the runtime campaign state or owner file first; do not restart from activity history or rescan the whole Agent by default;
- stop context hunting after finding owner, risk, current state, and proof floor;
- prefer one bounded write plus verification over a large abstract plan;
- if the safe action is obvious and low-risk, execute now instead of asking for another “continue”;
- if several low-risk candidates exist, choose the one with highest user-value and lowest duplication risk.

This absorbs the useful part of context-hunting and no-wait execution without creating a second planner.

## Decision Model

1. **Direct execution**
   - User clearly asked for a specific low-risk or already-discussed change.
   - Target is allowed, such as `/config/agent` or `/config` local plugin assets.
   - Execute the smallest correct action, then verify.

2. **Read-only inspection**
   - User asks what is wrong, what exists, whether something is possible, or
     asks for diagnosis.
   - Inspect without confirmation.

3. **Button confirmation required**
   - Next action is destructive, high-impact, credential-related,
     download-starting, delete/removal, restart/stop/start, plugin
     install/uninstall, scheduler/workflow execution, or external service
     state change.
   - Use `tg-button-interaction` and `ask_user_choice` when the needed choice is
     bounded and safe for buttons.
   - Do not ask the user to type routine “同意/授权/确认” unless buttons are under
     repair or the input is not button-safe.

4. **Clarification required**
   - Target, scope, or success criteria is genuinely ambiguous and unsafe to
     infer.
   - Ask one focused question; use buttons if the choices are known and safe.

## Conflict Resolution

Priority:

1. Safety boundaries and explicit user authorization.
2. MoviePilot Agent core identity and domain workflow.
3. Current task-specific skill.
4. Long-term memory preferences.
5. Active persona.

Clarifications:

- Protect MoviePilot application source and upstream-overwritten files by
  default.
- `/config/agent` is Agent-owned capability space and may be changed when the
  user asks.
- `/config` local plugin libraries may be changed when the user asks.
- Credentials and destructive operations still require explicit confirmation,
  preferably by buttons.

## Execution Discipline

Before acting:

- Identify the mode.
- Use the narrowest tool path.
- Do not ask approval when the user already authorized a low-risk Agent/config
  asset change.
- Do not turn clear continuation into brainstorming.
- Continuation Gate: when the user says “继续 / 执行 / 落地 / 下一步 / 按方案推进”
  for an already-discussed low-risk `/config/agent` or `/config` local plugin
  change, this turn must enter write, verification, or explicit high-risk
  button-confirmation path.
- Tool Gate: if a tool seems missing, retry the intended tool path directly; if
  execution truly fails, cite the concrete tool error.
- Self-Refactor Gate: when the user asks to “利用新技能蒸馏/重构自身”, first
  read the current runtime campaign state if present, then choose the highest-impact
  unprocessed capability target and make one bounded asset change plus verification.
  Do not answer with a fresh abstract plan unless the next action is high-risk or
  genuinely ambiguous.

After acting:

- Run the smallest fresh verification defined by the route contract.
- State only what evidence supports.
- Preserve only reusable context; do not store user frustration, one-off wording, or self-justifying slogans.
- If `/config/agent` capability assets changed, recommend repository sync via
  Git maintenance workflow.

## Anti-Patterns

Avoid:

- asking users to use typed routine confirmations when buttons can express them;
- treating Agent-owned files as forbidden application source;
- asking permission after clear low-risk authorization;
- writing broad rules into memory when a skill owns the workflow;
- converting user corrections into dirty memory or negative self-description instead of positive execution behavior;
- using persona style to hide a blocker;
- claiming completion without verification.

## Output Contract

Final answer should include:

- chosen mode;
- action taken or blocker;
- verification evidence;
- next safe step, using buttons if a bounded choice remains.
