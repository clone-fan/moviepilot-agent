---
name: moviepilot-update
version: 6
description: Use this skill when you need to check MoviePilot versions, restart MoviePilot, or trigger a MoviePilot upgrade. Prefer the built-in system APIs instead of docker commands or manual file replacement. If auto-update on restart is already enabled, just restart. If it is disabled, call the upgrade API so MoviePilot performs a one-shot upgrade and restart.
---

# MoviePilot Update

> All script paths are relative to this skill file.

Use this skill for MoviePilot restart and upgrade operations.

## Setup

This skill reuses the `moviepilot-api` client configuration.

Configure host and API key once:

```bash
python ../moviepilot-api/scripts/mp-api.py configure --host http://localhost:3000 --apikey <API_TOKEN>
```

## Preferred Commands

### Check versions

```bash
python scripts/mp-update.py versions
```

This calls `GET /api/v1/system/versions`.

### Restart MoviePilot

```bash
python scripts/mp-update.py restart
```

This calls `GET /api/v1/system/restart`.

### Upgrade and restart MoviePilot

Release mode:

```bash
python scripts/mp-update.py upgrade
```

Dev mode:

```bash
python scripts/mp-update.py upgrade dev
```

This calls `POST /api/v1/system/upgrade`.

Behavior:

- If `MOVIEPILOT_AUTO_UPDATE` is already enabled (`release` or `dev`), MoviePilot only triggers a restart and lets the normal startup flow perform the upgrade.
- If `MOVIEPILOT_AUTO_UPDATE` is disabled, MoviePilot writes a one-shot upgrade flag, restarts itself, performs that single upgrade during startup, and then continues running without changing the persisted auto-update setting.

## Direct API Examples

```bash
python ../moviepilot-api/scripts/mp-api.py GET /api/v1/system/restart
python ../moviepilot-api/scripts/mp-api.py POST /api/v1/system/upgrade --json '"release"'
python ../moviepilot-api/scripts/mp-api.py POST /api/v1/system/upgrade --json '"dev"'
```

## Notes

- These operations require administrator authentication.
- Restart or upgrade will interrupt the current agent session. Do not rely on post-restart follow-up steps in the same run.
- Prefer the API flow above. Only fall back to manual container commands when the API is unavailable.

## Safety Gate

- Version checks are read-only and can run directly.
- Restart and upgrade are high-impact operations: ask for explicit confirmation before calling them.
- Prefer MoviePilot API/system route. Do not use docker restart, manual file replacement, or shell service control unless the built-in route is unavailable and the user explicitly asked for fallback handling.
- Warn that restart/upgrade can interrupt the current agent session; do not promise post-restart verification in the same turn unless an external check is available.

## Distilled Rules

### Flow

1. Check current version or update settings when relevant.
2. If auto-update on restart is enabled, prefer a confirmed restart.
3. If auto-update is disabled and the user asked to upgrade, use the official one-shot upgrade route.
4. Avoid docker/service commands unless official routes are unavailable and the user explicitly authorized the operational risk.

### Safety

- Version checks are read-only and may run directly. Restart and upgrade are high-impact and require explicit confirmation unless the user gave the exact restart/upgrade command.
- Prefer MoviePilot built-in API/update flow; do not replace files manually or run Docker-level restart unless the user explicitly asks and the API path is unavailable.
- Before upgrade, record current version/channel; after restart/upgrade, re-check version or service health before claiming success.
- If auto-update is enabled, restart is enough; if disabled, use the one-shot upgrade API rather than changing persistent settings.

### Verification

- After version check, report the actual version source.
- After restart/upgrade dispatch, verify the API returns or service becomes reachable when possible.
- If verification cannot be completed because the service is restarting, state the handoff and next check clearly.
- On failure, report the last confirmed state and next safe diagnostic step.

### Completion Checklist

- Version check -> report current version, latest/version source, and whether update is needed.
- Restart/upgrade dispatch -> report that the built-in operation was triggered, not that the service already recovered unless separately verified.
- If API call fails -> do one narrower fallback check of API configuration or system status, then report the blocker.