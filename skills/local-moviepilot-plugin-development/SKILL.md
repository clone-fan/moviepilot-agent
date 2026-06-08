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

## Core Boundaries

- Do not modify MoviePilot core source under `/app/app/...` for plugin work.
- Keep local plugin source in `/config/FFplugin` unless the user specifies another repo.
- Treat plugin install/reload, plugin config updates, system setting changes, and command execution as state-changing operations. Confirm unless the user explicitly requested that exact action.
- Do not store secrets in plugin source, README, package metadata, memory, or Git.
- Prefer a V2-only plugin under `plugins.v2/<plugin_id_lower>/` with metadata in `package.v2.json`.
- Only use `plugins/<plugin_id_lower>/` plus `package.json` with `