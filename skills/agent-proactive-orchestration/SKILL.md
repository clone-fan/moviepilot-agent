---
name: agent-proactive-orchestration
version: 4
description: >-
  Use this skill for whole-Agent proactive orchestration before acting or
  replying: run the tg-button-interaction gate first, classify user intent,
  choose direct execution vs button choice vs read-only inspection vs
  clarification, run tasks to closure, trigger verification and handoff hooks,
  and avoid step-by-step mechanical behavior or after-the-fact apology patches.
allowed-tools: ask_user_choice
---

# Agent Proactive Orchestration

## Purpose

Prevent mechanical, step-by-step behavior. The Agent should reason before
acting, close the current task autonomously when safe, and surface choices only
when user choice genuinely changes the next action.

This skill decides interaction mode and completion hooks, then delegates domain
work to the right specialized skill.

## Mandatory Button Gate

Before every user-facing reply, apply `tg-button-interaction`:

- If the next step is continue, authorize, agree, confirm, cancel, retry, or a
  bounded selection, and the input is safe for buttons, use `ask_user_choice`
  and stop.
- Do not ask the user to type routine confirmations such as “继续 / 同意 /
  授权 / 下一步”.
- If the user reports buttons are broken, typed fallback is only temporary;
  route the failure to debugging and restore real callback-based interaction.

## Pre-Action Router

After the button gate, classify the request:

1. **Direct execution** — Exact, low-risk instruction; no meaningful branch.
   Execute the smallest correct action and validate.
2. **Button choice** — 2-6 safe user-facing branches. Use
   `tg-button-interaction` / `ask_user_choice` and stop.
3. **Temporary typed fallback** — Buttons are reported broken. Accept typed
   matching labels/numbers only to keep continuity, while repairing buttons.
4. **Read-only inspection** — State is unknown but inspection is safe and
   useful. Inspect first without asking.
5. **Clarification** — Required input is missing and cannot be inferred. Ask one
   focused question; use buttons if choices are known and safe.
6. **Refusal / boundary** — Unsafe bypass, secrets, or disallowed action. Refuse
   briefly and offer a safe alternative.

Do not ask for a typed routine confirmation when this router can choose a mode
now or hand the bounded choice to buttons.

## Task Closure Loop

For actionable tasks:

1. Resolve intent and the applicable specialized skill.
2. Gather only state that affects the action.
3. Execute the smallest correct action when authorized.
4. Validate with fresh evidence.
5. Summarize result and blocker, if any.
6. Trigger completion hooks.

Stop only when complete, blocked by missing input, blocked by safety
confirmation, or handed off to an asynchronous system route by design.

## Completion Hooks

- `/config/agent` capability asset changed and validated -> repository sync
  reminder through `moviepilot-agent-git-maintenance`.
- Completion claim -> `verification-before-completion` evidence.
- Skill created/updated -> `create-moviepilot-skill` / governance validation.
- User choice needed -> `tg-button-interaction`, not typed routine prompts.
- Git operation -> `moviepilot-agent-git-maintenance`.
- Media/resource/subscription/download -> MoviePilot domain skill router.
- Cleanup requested -> `work-completion-workflow`.

## Anti-Mechanical Rules

- Do not use apology as the fix; change the responsible rule and verify.
- Do not create endless “next step” prompts. If safe and clear, continue.
- Do not over-buttonize exact low-risk instructions.
- Do not under-buttonize real choices or high-impact confirmations.
- Do not button-loop when buttons are broken; use typed continuity and diagnose.
- Do not split completion into multiple approvals when the user already asked to
  self-check, organize, or archive.

## Delegation Rule

- Button/choice UX -> `tg-button-interaction`
- Authorization conflicts -> `agent-executive-control`
- Agent capability assets -> self-governance skills, then Git maintenance
- Skill creation/update -> `create-moviepilot-skill` or
  `skill-architecture-governance`
- MoviePilot media/site/download/subscription/library -> domain router
- Completion evidence -> `verification-before-completion`
- Completion cleanup -> `work-completion-workflow`

## Final Check

Before final response:

1. Did I complete or identify the blocker?
2. Did I validate claimed changes?
3. Did I use buttons for any remaining bounded choice?
4. Did I avoid exposing hidden/internal chains?
5. Did I avoid asking the user to push tiny next steps manually?
