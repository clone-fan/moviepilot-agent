---
name: moviepilot-api
version: 5
description: >-
  Use this skill only when the user explicitly asks to interact with MoviePilot
  through REST/HTTP API endpoints, needs API endpoint details, or a required
  MoviePilot operation cannot be covered by existing MCP tools, direct routes,
  or moviepilot-cli. Do not use it as the default path for ordinary media,
  download, subscription, site, library, or plugin tasks.
---

# MoviePilot REST API

> All script paths are relative to this skill file.

Use `scripts/mp-api.py` to call MoviePilot REST API endpoints directly.

## Routing Boundary

Prefer, in order:

1. MoviePilot MCP tools / dedicated Agent tools.
2. `moviepilot-direct-routes` for slash-command/direct-link execution.
3. `resource-search` for resource discovery.
4. `moviepilot-cli` for broad MoviePilot operations.
5. This skill only for explicit REST API work or true tool/CLI gaps.

Do not expose or save API tokens. Do not use API calls to bypass confirmation
rules for downloads, deletion, restart, scheduler/workflow execution, or
credential changes.

## Setup

Configure the backend host and API key (persisted to `~/.config/moviepilot_api/config`):

```
python scripts/mp-api.py configure --host http://localhost:3000 --apikey <API_TOKEN>
```

The API key is the `API_TOKEN` value from MoviePilot settings.

## How to Call APIs

### General syntax

```
python scripts/mp-api.py <METHOD> <PATH> [key=value ...] [--json '<body>']
```

### Authentication

- By default, the key is sent via the `X-API-KEY` header.
- For endpoints suffixed with `2` (e.g. `/api/v1/dashboard/statistic2`), use `--token-param` to send the key as `?token=`.
- Both methods validate against the same `API_TOKEN` value.

### Examples

```bash
# GET with query params
python scripts/mp-api.py GET /api/v1/media/search title="Avatar" type="movie"

# POST with JSON body
python scripts/mp-api.py POST /api/v1/download/add --json '{"torrent_url":"abc1234:1"}'

# DELETE
python scripts/mp-api.py DELETE /api/v1/subscribe/123

# Endpoints that require ?token= auth
python scripts/mp-api.py GET /api/v1/dashboard/statistic2 --token-param
```

## Complete API Reference

All endpoints are under the base URL `{MP_HOST}`. Path parameters are shown as `{param}`.

---

### Media Search (13 endpoints)

## Distilled Operating Rules

- Use API only for explicit REST/API requests or real gaps in MCP/direct/CLI coverage. It is not the normal media-operation path.
- Never expose API tokens, cookies, passwords, private keys, or full credential-bearing URLs.
- Prefer read-only API checks first. Mutating API calls follow the same confirmation rules as MCP tools.
- Do not use raw API calls to bypass MoviePilot safety gates for download, deletion, restart, scheduler/workflow execution, or credentials.

## Completion Checklist

- State why API was necessary instead of MCP/direct/CLI.
- For GET/read-only calls, cite the endpoint and the observed result.
- For mutating calls, verify the changed state through API or the matching MCP tool.
- If auth or endpoint shape fails, fall back once to endpoint discovery or the corresponding MCP tool before asking the user.

## Distilled API Boundary

- Use REST only for explicit API questions or true tool gaps; ordinary media/site/download/subscription tasks stay on MCP tools or slash commands.
- Never expose API tokens, cookies, passwords, or private headers in replies, files, memory, or Git.
- Prefer read-only API calls first. For writes, require the same confirmation level as the equivalent MoviePilot tool action.
- Validate API mutations by querying the resulting resource, not by HTTP status alone.
- If an endpoint is uncertain, inspect available routes or use the documented client help before guessing method/path/body.

## Distilled API Fallback Rules

Use REST/API only when the user explicitly asks for API work or when existing MCP
tools, direct slash commands, and MoviePilot CLI-style tools cannot cover the
operation.

### Before API

- Check whether a dedicated MCP tool exists.
- Check whether a direct slash/plugin command is the official route.
- Avoid raw database writes unless the database-operation skill is explicitly
  needed.

### API Safety

- Never echo tokens, cookies, API keys, passwords, or private headers.
- For write endpoints, confirm intent unless the user explicitly requested that
  exact write operation.
- Prefer the smallest endpoint call and avoid broad configuration replacement
  when a partial update exists.

### Verification

- Re-query the corresponding MoviePilot state after a write.
- For upgrade/restart/version endpoints, defer to `moviepilot-update` where
  possible.
- For failures, capture endpoint, status class, and safe error summary without
  leaking credentials.

