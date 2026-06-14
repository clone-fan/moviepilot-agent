---
name: moviepilot-agent-git-maintenance
version: 7
description: >-
  Use this skill when maintaining the moviepilot-agent Git repository, syncing
  Agent capability assets, prompting for repository sync after /config/agent
  capability changes, removing tracked directories, fixing failed Git pushes,
  initializing or restoring GitHub SSH/Deploy Key access, or performing
  handoff-safe Git cleanup and verification.
allowed-tools: read_file list_directory execute_command edit_file write_file ask_user_choice
---

# MoviePilot Agent Git Maintenance

## Purpose

Maintain `/config/agent/repo/moviepilot-agent` as the handoff-safe capability-asset repository for this Agent. This skill owns repository sync, sensitive scans, commit/push, SSH/Deploy Key troubleshooting, tracked cleanup, and final handoff evidence.

Do not use it for media search, downloads, subscriptions, or ordinary MoviePilot operations.

## Ownership Boundaries

- This skill: repository state, sync reminders, sensitive scans, Git/SSH repair, commit/push, final handoff evidence.
- `moviepilot-agent-weekly-sync` Job: recurring automatic sync.
- `create-moviepilot-skill` / `writing-skills`: authoring skill content before repository sync.
- `tg-button-interaction`: button UX for sync/push choices.

## Canonical Paths

```text
repo:        /config/agent/repo/moviepilot-agent
runtime git: /config/agent/runtime/git/
ssh map:     /config/agent/runtime/git/REPO_SSH_MAP.md
default host alias: github.com-moviepilot-agent
weekly job:  /config/agent/jobs/moviepilot-agent-weekly-sync/JOB.md
sync script: /config/agent/scripts/sync_moviepilot_agent_repo.py
```

Repository-specific non-secret anchors, such as local path, host alias and public-key fingerprint, belong in `REPO_SSH_MAP.md`, not memory.

## Hard Rules

- Never commit runtime secrets, tokens, cookies, passwords, private keys, logs, caches, activity data, databases, or transient archives.
- Never echo private key contents. Public key and public fingerprint are safe.
- Fetch before push. Do not force-push remote divergence.
- `ssh -T` or `git fetch` proves authentication/read access only; push can still fail if the Deploy Key is read-only.
- If deleting tracked content, remove both tracked files and future reintroduction paths in sync scripts/jobs/docs.
- `git status` alone is not completion evidence.

## Trigger Cases

Use this skill for requests like:

- “同步 / 提交 / 推送 Agent 能力资产”
- “维护 moviepilot-agent 仓库”
- “Agent skill / memory / job / script 改完后收尾”
- “Git 推送失败 / Deploy Key / SSH alias 有问题”
- “从 Git 删除某目录并防止再次同步”
- “做一次可交接的 Git 验收”

After reusable `/config/agent` capability assets change, offer repository sync unless the user already requested or declined it. If confirmation is needed, use buttons: `同步并推送`、`只提交`、`先只读检查`、`暂不同步`。

## Standard Sync Workflow

1. **Locate and inspect**
   - Confirm repo path, branch, remote and working tree.
   - If the canonical repo is missing, locate `.git` directories read-only.
2. **Fetch and detect divergence**
   - Fetch `origin main` through the configured SSH alias.
   - Interpret `git rev-list --left-right --count main...origin/main` before pushing.
   - If remote is ahead, prefer `pull --rebase --autostash`, then re-check.
3. **Sync Agent assets**
   - Prefer `/opt/venv/bin/python /config/agent/scripts/sync_moviepilot_agent_repo.py`.
   - Manual sync may include only approved assets: `skills/`, `runtime/personas/`, `memory/`, `jobs/`, `scripts/`, README and repo metadata.
   - Exclude docs unless explicitly intended, runtime secrets, logs, caches, activity, and databases.
4. **Sensitive and runtime pollution scan**
   - Check ignored/untracked generated files, logs, pyc, temp files and secret-like names.
   - Remove only exact generated files/directories after confirming they are safe.
5. **Validate before commit**
   - Compile repo scripts when relevant.
   - Run the repository self-audit; completion requires `fail=0`.
6. **Stage, commit, push**
   - Stage only approved capability assets.
   - Commit with an exact maintenance message.
   - Push through the configured SSH alias; if write access fails, keep the local commit and report the Deploy Key blocker.
7. **Final handoff verification**
   - Fetch again, confirm clean status, divergence `0 0`, sensitive scan clean or explained, audit `fail=0`, and report recent commit hash.

Detailed commands for each step are in `REFERENCES.md`.

## SSH / Deploy Key Troubleshooting

When push/fetch fails, inspect before asking for new credentials. `Permission denied (publickey)` often means the remote is not using the dedicated alias, not that the key is absent.

Inspection order:

1. Remote URL, status, branch tracking.
2. Runtime git directory and public key fingerprint.
3. SSH auth using `/config/agent/runtime/git/ssh_config`.
4. `git fetch origin main` through `GIT_SSH_COMMAND`.

Dedicated-alias remotes should look like:

```text
git@<host-alias>:OWNER/REPO.git
```

Deploy Key write failure usually looks like `Permission to OWNER/REPO.git denied to deploy key`. In that case, keep the local commit and ask the user to enable write access or add a writable Deploy Key; do not redo work.

First-time setup command templates are in `REFERENCES.md`.

## Tracked Directory Removal Checklist

For intentional repository cleanup:

- Confirm the directory is tracked.
- Remove tracked files with Git, not broad filesystem deletes.
- Check sync scripts, jobs, README, and `.gitignore` for reintroduction paths.
- Validate no tracked files remain and no sync command re-adds them.
- Run the standard sensitive scan, audit, commit, push, and final verification.
## Git Failure Triage

For failed sync, push, or CI-like repository maintenance checks, localize before changing credentials or history:

1. Identify the failing layer: working tree, sync script, sensitive scan, audit, commit, fetch, push auth, remote divergence, or branch protection.
2. Read the exact failing command and exit code; keep the smallest reproducible command.
3. Prefer non-destructive fixes: rerun sync, fix ignored generated files, pull/rebase, repair remote alias, or leave a local commit with a clear blocker.
4. Do not force-push, rewrite history, rotate keys, or delete tracked assets unless explicitly authorized.
## Plugin Release Handoff

When Agent capability work includes a local plugin repository or release asset, keep Git handoff explicit:

- distinguish Agent capability repo sync from plugin source repo sync; do not mix commits unless the user asked for both;
- before pushing plugin-related changes, check package metadata, generated ZIP/release artifacts, README/config notes, and secret/runtime exclusions;
- after push, report branch, commit, remote state, and whether the plugin still needs install/reload validation inside MoviePilot;
- if Deploy Key or remote write permission blocks push, keep local changes and report the exact repository blocker.

## Output Contract

Report only evidence-backed results:

- repository path and branch state;
- what changed or why no change was needed;
- validation/audit summary;
- push/sync result and commit hash when applicable;
- remaining blocker, especially missing Deploy Key write access.
