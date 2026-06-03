---
name: moviepilot-api
version: 2
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

