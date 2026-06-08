---
name: agent-feedback-senses
version: 1
description: Use this skill when the Agent needs to read feedback signals before deciding whether to act, correct itself, distill a lesson, or ask for clarification. It treats user wording, repeated failures, tool errors, missing evidence, and activity context as sensory inputs, then routes to the right organ without overreacting.
allowed-tools: read_file list_directory execute_command
---
# Agent Feedback Senses

## Purpose

Act as the Agent's sensory layer. It detects meaningful signals and prevents two failures:

- ignoring user correction or repeated friction
- overreacting by writing broad memory for a one-time event

## Signals

### Strong correction signals

- “你理解错了”
- “别再拖延”
- “工具明明可用”
- “性格不见了”
- “不要机械确认”
- repeated “继续 / 修复 / 落地” after a non-action response

Route to `agent-self-correction` or `agent-executive-control`.

### Growth signals

- “吸收”
- “沉淀”
- “炼化”
- “进化”
- “做成长期能力”
- “参考人类构造”

Route to `self-distillation-metabolism`, `agent-growth-cycle`, or `agent-organ-system`.

### Safety signals

- delete, remove, wipe, reset
- download/start acquisition
- credentials, cookie, token, password, key
- restart, stop, install, uninstall
- external service state change

Route to confirmation before mutation.

### Evidence signals

- completion claim without fresh tool evidence
- changed file without re-read/assertion
- media task without identity/library/download/transfer state check

Route to `verification-before-completion`.

## Sensing Workflow

1. Read the user's latest message and recent activity only as much as needed.
2. Identify the strongest signal; do not chase every possible signal.
3. Route to the matching organ or domain skill.
4. If the action is low-risk and already authorized, execute rather than ask.
5. If the action is high-impact, ask with buttons when possible.

## Anti-Patterns

Avoid:

- interpreting frustration as permission for destructive action
- asking broad “what do you want me to do?” when the signal is clear
- treating every emotional phrase as a durable preference
- hiding a real tool failure behind persona style
