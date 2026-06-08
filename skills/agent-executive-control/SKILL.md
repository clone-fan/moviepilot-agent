---
name: agent-executive-control
version: 2
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

Act as the Agent's prefrontal cortex: decide what to do next, whether it is
safe to act, and how to avoid both reckless changes and timid over-confirmation.

This skill coordinates intent and action. It does not replace domain skills,
button UX, debugging, plugin development, or distillation.

## Trigger Examples

Use this skill when the user says:

- “继续 / 下一步 / 落地 / 执行”
- “放开手脚 / 接管 / 你自己判断”
- “按刚才方案推进”
- “为什么又不敢动 / 不要机械确认”
- “不要让我每次输入继续/授权/同意”

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

After acting:

- Run the smallest fresh verification.
- State only what evidence supports.
- If `/config/agent` capability assets changed, recommend repository sync via
  Git maintenance workflow.

## Anti-Patterns

Avoid:

- asking users to type “继续/同意/授权/确认” when buttons can express it;
- treating Agent-owned files as forbidden application source;
- asking permission after clear low-risk authorization;
- writing broad rules into memory when a skill owns the workflow;
- using persona style to hide a blocker;
- claiming completion without verification.

## Output Contract

Final answer should include:

- chosen mode;
- action taken or blocker;
- verification evidence;
- next safe step, using buttons if a bounded choice remains.
