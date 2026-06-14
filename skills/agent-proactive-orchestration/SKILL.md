---
name: agent-proactive-orchestration
version: 5
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

Provide the Agent's governed runtime rhythm for MoviePilot work. A long skill list is not enough: the Agent must know when to inspect, when to plan, when to call a domain skill, when to ask, and when to prove the work is ready.

This skill decides interaction mode, domain routing, bounded execution, verification, and cleanup hooks. It prevents the user from becoming the full-time dispatcher.

## Mandatory Button Gate

Before every user-facing reply, apply `tg-button-interaction`:

- If the next step is continue, authorize, agree, confirm, cancel, retry, or a
  bounded selection, and the input is safe for buttons, use `ask_user_choice`
  and stop.
- Do not ask the user to type routine confirmations such as “继续 / 同意 /
  授权 / 下一步”.
- If the user reports buttons are broken, typed fallback is only temporary;
  route the failure to debugging and restore real callback-based interaction.

## Runtime Rhythm

Use this governed runtime rhythm before ordinary execution. It is the MoviePilot Agent adaptation of the Vibe-style harness, but MoviePilot domain routing and safety remain the authority:

1. **Skeleton check** — identify whether this is direct media work, Agent/config asset work, plugin work, diagnosis, or a high-impact operation. Reject unsafe branches early.
2. **Freeze intent** — reduce the user request to goal, target, constraints, risk, and success evidence. Do not copy emotional filler into memory.
3. **Interview only if needed** — ask one focused question only when required input is missing; use buttons for bounded choices. Do not interview when the next safe action is obvious.
4. **Stage plan** — for multi-step work, create or use a compact staged plan with acceptance evidence per stage; for clear low-risk continuation, execute directly. For Agent self-refactor campaigns, prefer the existing `runtime/self-refactor-campaign.md` state over creating a new plan.
5. **Route specialist skill** — choose one primary domain skill or direct MoviePilot tool path; support skills may advise planning, debugging, verification, or governance but never become a second runtime authority.
6. **Execute bounded work** — act inside the current authorized scope; gather only context that affects the next action.
7. **Verify evidence** — prove the changed state with tools, commands, or fresh status checks before completion claims.
8. **Cleanup and preserve context** — keep only reusable rules in skills/memory/runtime; archive historical material in docs; discard one-off process noise.

Internal size labels such as quick/small/XL are planning aids only. They must not create user-facing ceremony or bypass requirement freeze, review, cleanup, and no-regression discipline.

## Pre-Action Router

After the runtime rhythm and button gate, classify the request:

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

## Spec And Plan Distillation

When absorbing planning/spec candidates such as `create-plan`, `context-fundamentals`, `speckit-*`, and Vibe planning wrappers, keep one MoviePilot Agent runtime:

- **Intent spec**: freeze user goal, non-goals, target assets/media/plugin, risk, and acceptance evidence before broad work.
- **Clarification budget**: ask only for missing inputs that block safe execution; do not create a second interview ritual.
- **Plan contract**: plans should name owner files/tools, ordered phases, proof floors, and confirmation gates.
- **Task slicing**: split work by owner and verification boundary, not by arbitrary role labels.
- **Constitution boundary**: project rules and safety boundaries are constraints, not a separate route authority.

Rejected from upstream candidates: second plan runtime, standalone spec engine, auto task-to-issue workflow, and external command wrappers.

## Autonomous Batch Selection

When the user authorizes self-improvement broadly, choose the next batch by this order:

1. Directly improves current user collaboration: fewer needless prompts, clearer ownership, stronger verification, safer plugin/media operations.
2. Has an existing local owner and can be absorbed in a small checklist update.
3. Avoids duplicate routes, second runtimes, external dependencies, and memory expansion.
4. Can be verified by structural checks plus one discoverability assertion.

Default to `update existing skill` or `runtime admission`. Create no new skill unless the trigger, tools, and proof boundary are genuinely distinct.

## Task Closure Loop

For actionable tasks:

1. Resolve frozen intent and primary skill/tool route.
2. Gather only state that affects the action.
3. Execute the smallest correct action when authorized.
4. Validate with fresh evidence.
5. Preserve only reusable context and discard dirty one-off wording.
6. Summarize result and blocker, if any.
7. Trigger completion hooks.

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

- Do not use self-negating statements as capability, such as “not a phrase list” or “not an apology”; replace them with positive execution contracts.
- Do not use apology as the fix; change the responsible rule and verify.
- Do not create endless “next step” prompts. If safe and clear, continue.
- Do not over-buttonize exact low-risk instructions.
- Do not under-buttonize real choices or high-impact confirmations.
- Do not button-loop when buttons are broken; use typed continuity and diagnose.
- Do not split completion into multiple approvals when the user already asked to
  self-check, organize, or archive.
- Do not restart an Agent self-refactor campaign from activity history when a
  runtime campaign state exists; continue the next unprocessed capability target.

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
