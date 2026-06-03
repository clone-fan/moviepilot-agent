---
name: command-dispatch
version: 2
description: >-
  Use this skill as the fallback dispatcher for unknown or plugin-provided slash
  commands after moviepilot-direct-routes cannot map the request. It can list
  available slash commands, inspect plugin command capabilities, and execute a
  selected command. Do not use it before moviepilot-direct-routes for exact
  MoviePilot commands, direct 115/magnet/ed2k links, or obvious built-in command
  aliases.
allowed-tools: list_slash_commands query_plugin_capabilities run_slash_command
---

# Command Dispatch

Use this skill to discover and dispatch system or plugin slash commands when the
more specific direct-route skill does not already cover the user's request.

## Routing Boundary

Prefer `moviepilot-direct-routes` first for:

- exact slash commands
- built-in MoviePilot command aliases
- 115 share links
- magnet / ed2k links
- simple direct command-style requests

Use this skill when:

- the command is unknown and needs discovery through `list_slash_commands`;
- the request appears to belong to an installed plugin;
- plugin capabilities must be queried before execution;
- direct-routes has no stable mapping.

## Tools

- `list_slash_commands` — List all available slash commands.
- `query_plugin_capabilities` — Query plugin commands, actions, and scheduled services.
- `run_slash_command` — Execute a specified command asynchronously.

## Workflow

### Step 1: Identify User Intent

Determine whether the user is requesting command execution.

- Direct command: message starts with `/`, e.g. `/sites`, `/subscribes`.
- Natural language: describes an actionable command-like request.

### Step 2: Find Matching Command

Use `list_slash_commands` to retrieve available commands. If a specific plugin
is involved, use `query_plugin_capabilities`.

Matching strategy:

- Prefer exact command or description matches.
- Then narrow down by category.
- Never guess non-existent commands.

### Step 3: Confirm Risky Commands

High-impact commands such as restart, deletion, credential changes, workflow or
scheduler execution require explicit user confirmation before `run_slash_command`.

### Step 4: Execute And Report

Use `run_slash_command` with `/command_name arg1 arg2`. Command execution is
asynchronous; report only that the command has started.
