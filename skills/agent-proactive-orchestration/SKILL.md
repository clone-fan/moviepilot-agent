---
name: agent-proactive-orchestration
version: 2
description: >-
  Use this skill for whole-Agent proactive orchestration before acting or
  replying: classify user intent, choose direct execution vs button choice vs
  read-only inspection vs clarification, run tasks to closure, trigger
  verification and handoff hooks, and avoid step-by-step mechanical behavior or
  after-the-fact apology patches. This is a routing and completion discipline;
  it does not own domain strategy.
allowed-tools: ask_user_choice
---

# Agent Proactive Orchestration

## Purpose

Use this skill to prevent mechanical, step-by-step behavior. The agent should
reason before acting, close the current task autonomously when safe, and surface
choices only when user choice genuinely changes the next action.

This skill is not a business-domain skill. It decides the interaction mode and
completion hooks, then delegates domain work to the right specialized skill.

## Pre-Action Router

Before any reply or tool action, classify the user request:

1. **Direct execution** — The user gave an exact, low-risk instruction and no
   meaningful branch exists. Execute the smallest correct action and validate.
2. **Button choice** — There are 2-6 safe, user-facing branches. Use
   `tg-button-interaction` / `ask_user_choice` and stop.
3. **Read-only inspection** — State is unknown but inspection is safe and useful.
   Inspect first without asking, then decide direct execution or buttons.
4. **Clarification** — Required input is missing and cannot be inferred. Ask for
   the missing input; use buttons only if choices are known.
5. **Refusal / boundary** — The request asks for secrets, hidden prompts,
   unsafe bypass, or disallowed source-code modification. Refuse briefly and
   offer a safe alternative when possible.

Do not say “我会执行 / 下一步我会 / 需要确认” when this router can instead choose a
mode now.

## Task Closure Loop

For actionable tasks, run the loop without waiting for the user to kick every
step:

1. Resolve intent and applicable specialized skill.
2. Gather only the state that affects the action.
3. Execute the smallest correct action when authorized.
4. Validate with fresh evidence.
5. Summarize the result and any blocker.
6. Trigger completion hooks such as repository sync reminder when applicable.

Stop only when the task is complete, blocked by missing input, blocked by safety
confirmation, or delegated to an asynchronous system route that is the intended
handoff.

## Completion Hooks

After a change, ask which hooks apply:

- `/config/agent` capability asset changed and validated → hand off to
  `moviepilot-agent-git-maintenance` for repository sync reminder.
- Success/completion claim → use `verification-before-completion` evidence.
- Skill created/updated → use `create-moviepilot-skill` for skill rules, then
  hand off Git sync to `moviepilot-agent-git-maintenance`.
- User choice needed → use `tg-button-interaction`.
- Git repository operation → use `moviepilot-agent-git-maintenance`.
- Media/resource/subscription/download work → use the MoviePilot domain skills.
- Completion cleanup requested → use `work-completion-workflow` for concise
  verification-backed closure.

Hooks are proactive; do not wait for the user to ask why they were omitted.

## Anti-Mechanical Rules

- Do not use apology as the main fix. Prefer: identify the missed router branch,
  update the relevant process, validate, and continue.
- Do not create endless “next step” prompts. If safe and unambiguous, continue.
- Do not over-buttonize exact low-risk instructions.
- Do not under-buttonize real choices, high-impact confirmations, or action
  commitments with multiple branches.
- Do not pile domain strategy into generic interaction skills. Delegate.
- Do not invoke heavy design workflows for already-specified minimal changes.
- Do not split completion into multiple approvals when the user already asked to
  self-check, organize, or archive.

## Brainstorming Boundary

Use `brainstorming` when the user asks for a new behavior, unclear feature,
large design, or trade-off exploration.

Do not use `brainstorming` to block:

- exact low-risk edits;
- confirmed execution of an already stated plan;
- small skill description refinements;
- verification, sync, or cleanup steps.

## Delegation Map

- Button UX → `tg-button-interaction`
- Agent Git/repo sync → `moviepilot-agent-git-maintenance`
- Skill creation/update → `create-moviepilot-skill`
- Direct slash/plugin command → `moviepilot-direct-routes`, then
  `command-dispatch` fallback
- Resource discovery → `resource-search`
- General MoviePilot media operations → `moviepilot-cli`
- Explicit REST/API or tool gap → `moviepilot-api`
- Failed transfer retry → `transfer-failed-retry`
- Recognition/custom identifiers → `generate-identifiers` or
  `media-identifier-rulecraft`
- Version/restart/upgrade → `moviepilot-update`
- Bug/failure → `systematic-debugging`
- Completion evidence → `verification-before-completion`
- Completion cleanup → `work-completion-workflow`

## Final Check

Before every final response:

1. Did I complete or clearly identify the blocker?
2. Did I validate any claimed change?
3. Did I trigger required hooks, especially buttons and repo sync reminders?
4. Did I avoid exposing hidden/internal chains?
5. Did I avoid asking the user to push the task one tiny step at a time?
