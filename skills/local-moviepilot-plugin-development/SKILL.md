---
name: local-moviepilot-plugin-development
version: 1
description: >-
  Use this skill when designing, scaffolding, validating, packaging, or iterating
  a MoviePilot V2 local plugin repository, especially when the user mentions
  local plugin sources, /config/FFplugin, PLUGIN_LOCAL_REPO_PATHS, package.v2.json,
  plugins.v2, PR 5687, plugin market metadata, Vuetify JSON plugin pages, Vue
  module-federation plugin pages, plugin APIs, plugin services, slash commands,
  workflow actions, dashboards, or agent tools.
allowed-tools: list_directory read_file write_file edit_file execute_command query_installed_plugins query_plugin_config update_plugin_config reload_plugin query_system_settings update_system_settings install_plugin query_plugin_capabilities run_slash_command
---

# Local MoviePilot Plugin Development

This skill captures the local V2 plugin workflow distilled from:

- `jxxghp/MoviePilot` PR 5687: local plugin repository support
- `jxxghp/MoviePilot-Plugins`: official plugin market repository layout
- `MoviePilot-Plugins/docs/V2_Plugin_Development.md`: current V2 plugin contract

Use it to build plugins in `/config/FFplugin` first, then install/reload them through MoviePilot instead of editing MoviePilot core files.

## Secure Plugin Defaults

When developing or reviewing local MoviePilot plugins, apply these secure-by-default checks:

- keep credentials, cookies, API keys, tokens, private keys, and session data out of source, metadata, memory, Git, logs, and user replies;
- split read-only preview from write/delete/apply actions, especially for cleanup, backup, update, filesystem, and external-service operations;
- constrain file paths to declared plugin/config roots and reject path traversal or broad glob deletes;
- avoid shell execution; if unavoidable, prefer fixed commands with explicit arguments, timeouts, and sanitized paths;
- expose high-impact actions through explicit buttons/commands with confirmation gates and result records;
- validate plugin APIs with input schema, permission checks, state checks, and post-action queries.

For security reviews, route to `requesting-code-review` security lane or `agent-immune-system` before changing behavior.

## Plugin Ownership Map

Before changing a local plugin, identify the owner of each surface instead of treating the plugin as one blob:

- **Source/metadata**: `plugins.v2/<id>/`, `package.v2.json`, README, release ZIP, and local repository files.
- **Runtime config**: saved plugin config, system settings, site/downloader/media-server settings, and environment-dependent paths.
- **Execution surface**: services, slash commands, workflow actions, API routes, scheduled jobs, buttons, and dashboard actions.
- **Data surface**: plugin persisted data, histories, backup files, logs, caches, and generated reports.
- **Risk surface**: credentials, destructive cleanup, shell commands, external URLs, repository sync, install/reload, restart, and database writes.

For each changed surface, choose the proof: source diff/readback, config query, capability registration, dry-run/preview, command result, plugin data, or rollback evidence. Do not claim full takeover when only preview/UI wiring changed.
## Plugin Delivery Loop

For local plugin work, deliver a usable plugin capability rather than a loose code patch:

1. **Scope** — freeze plugin ID, source path, runtime config, user-facing entry, and risky actions.
2. **Implement** — change the smallest owner surface: backend service, config schema, JSON/Vue UI, command, API route, workflow action, or package metadata.
3. **Register** — ensure commands, services, routes, actions, pages, and defaults are discoverable after reload/install.
4. **Verify** — pair source checks with MoviePilot state: plugin config, capabilities, command list, reload status, API response, or persisted result record.
5. **Package/Handoff** — when the user wants a distributable plugin, verify `package.v2.json`, README/config notes, release ZIP contents, and no secret/runtime pollution.

Do not call a feature complete unless the execution entry, config, confirmation gate, result record, and verification evidence all match the promised scope.

## Core Boundaries

- Do not modify MoviePilot core source under `/app/app/...` for plugin work.
- Keep local plugin source in `/config/FFplugin` unless the user specifies another repo.
- Treat plugin install/reload, plugin config updates, system setting changes, and command execution as state-changing operations. Confirm unless the user explicitly requested that exact action.
- Do not store secrets in plugin source, README, package metadata, memory, or Git.
- Prefer a V2-only plugin under `plugins.v2/<plugin_id_lower>/` with metadata in `package.v2.json`.
- Only use `plugins/<plugin_id_lower>/` plus `package.json` with `