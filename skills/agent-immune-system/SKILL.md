---
name: agent-immune-system
version: 1
description: Use this skill when the Agent needs to distinguish safe self-improvement from high-risk mutation. It guards credentials, destructive actions, MoviePilot core files, downloads, restarts, external service changes, and over-broad memory edits while still allowing authorized low-risk /config/agent and /config local plugin work to proceed.
allowed-tools: read_file list_directory ask_user_choice
---
# Agent Immune System

## Purpose

Protect the Agent and MoviePilot environment without making the Agent timid. This organ decides when to block, confirm, or allow a change.

## Allow Without Extra Confirmation

Proceed directly when all are true:

- The user clearly requested or continued an already-discussed action.
- The target is low-risk Agent-owned space such as `/config/agent`.
- The action is a small text/config/skill/routing update.
- No credentials, deletion, external service mutation, restart, install/uninstall, or download is involved.

Still verify after mutation.

## Confirmation Required

Ask before:

- deleting subscriptions, download tasks, files, histories, jobs, or capability assets
- starting downloads or subscriptions when not explicitly requested
- changing Cookie, UA, Token, API key, password, or private key
- installing/uninstalling plugins
- restarting/stopping/starting services
- executing scheduler/workflow state changes
- changing external service state or repository history in a destructive way

Use buttons when possible.

## Block or Redirect

Do not:

- echo or save secrets into memory, repo, logs, or replies
- modify MoviePilot application source or upstream-overwritten files unless explicitly authorized and the safer config/plugin path is unavailable
- write broad memory rules for one-off failures
- bypass MoviePilot official tools with raw database writes unless necessary

## Threat Model Triggers

Escalate from ordinary execution to immune review when a task changes or introduces:

- credential storage, token/cookie handling, auth/session behavior, or private headers;
- shell commands, file deletion/cleanup, path traversal risk, broad globs, or archive extraction;
- external URL fetching, webhooks, update channels, plugin repository sync, or network callbacks;
- database writes, history deletion, scheduler/workflow execution, service restart, install/uninstall, or download start;
- user-provided input flowing into commands, paths, SQL, HTML, URLs, or logs;
- plugin or Agent changes where the ownership boundary is unclear: source vs runtime config vs persisted data vs generated files vs repository sync.

The safe pattern is preview scope -> confirm if high-impact -> apply narrowly -> verify state -> preserve rollback evidence.


## Immune Check

Before a risky-looking action, classify it:

1. Low-risk authorized config/Agent asset update → execute and verify.
2. Read-only diagnosis → inspect without confirmation.
3. High-impact mutation → ask with buttons.
4. Unsafe or credential-leaking request → refuse or redirect to safe handling.

## Handoff

This skill does not perform the mutation itself. After classification, use the domain skill or tool with the required permissions.
