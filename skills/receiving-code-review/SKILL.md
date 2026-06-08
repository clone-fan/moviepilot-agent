---
version: 2
name: receiving-code-review
description: 收到代码审查反馈后、实施建议之前使用，尤其当反馈不明确或技术上有疑问时——需要技术严谨性和验证，而非敷衍附和或盲目执行。
allowed-tools: read_file list_directory execute_command edit_file write_file ask_user_choice
---

# 接收代码审查

## Purpose

Use this skill when the user gives code review feedback, asks to apply review suggestions, or provides external review comments that need technical evaluation before implementation.

The goal is not to agree politely. The goal is to understand, verify, decide, implement safely, and prove the result.

## Core Principle

Review feedback is a technical input, not an automatic command.

Default flow:

1. Read the feedback completely.
2. Identify each actionable item.
3. Clarify ambiguous or conflicting items before writing.
4. Verify suggestions against the actual codebase.
5. Decide: implement, reject with evidence, defer, or ask for scope.
6. Apply one coherent change set at a time.
7. Run fresh verification before claiming completion.

## When To Clarify

Ask before implementing when:

- the requested change has multiple plausible meanings;
- multiple review items are interdependent and some are unclear;
- the feedback conflicts with previous user instructions or safety boundaries;
- the suggestion is destructive, high-impact, credential-related, or changes external services;
- the reviewer asks for a feature whose usage or value is uncertain.

Use buttons when the user needs to choose between a few concrete options.

## Technical Evaluation Checklist

Before applying a review suggestion, check:

- Does the current code actually have the reported problem?
- Would the suggestion break existing behavior, compatibility, or tests?
- Is the current implementation intentional because of platform, version, or deployment constraints?
- Is the suggested feature actually used, or is it YAGNI?
- Does a smaller fix solve the same issue with less risk?
- What verification will prove the change worked?

For YAGNI checks, inspect actual usage with code search before adding abstractions or unused features.

## Implementation Order

For multi-item feedback:

1. Security, data-loss, crash, or blocking issues.
2. Small correctness fixes.
3. Compatibility or regression fixes.
4. Refactors and cleanup.
5. Nice-to-have polish.

Do not batch unrelated changes if separate verification would be clearer.

## Responding To Feedback

When feedback is correct:

- state the concrete issue and fix;
- implement the smallest correct change;
- show verification evidence.

When feedback is wrong or risky:

- explain the technical reason briefly;
- cite code, tests, logs, docs, or compatibility constraints;
- propose a safer alternative when possible.

When verification is impossible with current access:

- state the exact missing evidence;
- offer the smallest read-only investigation or ask for the missing artifact.

Avoid performative agreement, defensive arguing, long apologies, or implementing before validation.

## MoviePilot Agent Adaptation

- This is a workflow support skill, not a MoviePilot media route.
- Do not use it for ordinary site/search/download/subscription/transfer tasks.
- For `/config/agent` and `/config` local plugin assets, user-authorized low-risk review fixes can be applied directly and verified.
- MoviePilot core source, credentials, destructive actions, restarts, plugin install/uninstall, and external service changes still follow confirmation policy.
- If the review concerns an Agent skill, also apply `writing-skills` / `skill-architecture-governance` checks as needed.

## Verification

After changes, run the smallest fresh verification that proves the reviewed issue is addressed:

- syntax or compile checks for code;
- targeted tests for behavior;
- grep/assertion for wording or rule changes;
- frontmatter checks for skills/jobs;
- repository status and sensitive scan when preparing commit/push.

Never claim that review feedback is resolved without fresh evidence.

## Output Contract

Report:

- review items understood;
- what was implemented, rejected, deferred, or clarified;
- verification evidence;
- remaining risks or next review item;
- repository sync reminder if durable `/config/agent` assets changed.
