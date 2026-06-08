---
name: moviepilot-agent-git-maintenance
version: 6
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

Maintain `/config/agent/repo/moviepilot-agent` as the handoff-safe capability-asset repository for this Agent. This skill owns sync, sensitive scans, commit/push, SSH/Deploy Key troubleshooting, and final repository verification.

Do not use it for media search, downloads, subscriptions, or ordinary MoviePilot operations.

## Ownership Boundaries

- This skill: repository state, sync reminders, sensitive scans, Git/SSH repair, commit/push, final handoff evidence.
- `moviepilot-agent-weekly-sync` Job: recurring automatic sync.
- `create-moviepilot-skill` / `writing-skills`: authoring skill content before repository sync.
- `tg-button-interaction`: button UX for sync/push choices.

## Hard Rules

- Never commit runtime secrets, tokens, cookies, passwords, private keys, logs, caches, activity data, databases, or transient archives.
- Never echo private key contents. Public key and public fingerprint are safe.
- Fetch before push. Do not force-push remote divergence.
- `ssh -T` or `git fetch` proves authentication/read access only; push can still fail if the Deploy Key is read-only.
- If deleting tracked content, remove both tracked files and future reintroduction paths in sync scripts/jobs/docs.
- `git status` alone is not completion evidence.

## Canonical Paths

```text
repo:        /config/agent/repo/moviepilot-agent
runtime git: /config/agent/runtime/git/
ssh map:     /config/agent/runtime/git/REPO_SSH_MAP.md
default host alias: github.com-moviepilot-agent
weekly job:  /config/agent/jobs/moviepilot-agent-weekly-sync/JOB.md
sync script: /config/agent/scripts/sync_moviepilot_agent_repo.py
```

Keep repository-specific non-secret anchors, such as local path, host alias and public-key fingerprint, in `REPO_SSH_MAP.md`, not memory.

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
   ```bash
   cd /config/agent/repo/moviepilot-agent
   pwd
   git status --short --branch
   git remote -v
   git branch -vv
   ```
   If missing, locate read-only:
   ```bash
   find /config -maxdepth 4 -type d -name .git 2>/dev/null | sed 's#/.git$##' | sort
   ```

2. **Fetch and detect divergence**
   ```bash
   GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' git fetch origin main
   git rev-list --left-right --count main...origin/main
   ```
   Interpret: `0 0` synced, `0 N` remote ahead, `N 0` local ahead, `N M` diverged. If remote is ahead, use `git pull --rebase --autostash origin main` and then re-check.

3. **Sync Agent assets**
   Prefer the deterministic script:
   ```bash
   /opt/venv/bin/python /config/agent/scripts/sync_moviepilot_agent_repo.py
   ```
   Expected outcomes include `OK no_changes`, `OK no_staged_changes`, or `OK committed_and_pushed ...`.

   Manual sync must include only approved assets: `skills/`, `runtime/personas/`, `memory/`, `jobs/`, `scripts/`; exclude `docs/`, runtime secrets, logs, caches, activity, and databases.

4. **Sensitive and runtime pollution scan**
   ```bash
   git status --short --ignored
   find . -path './.git' -prune -o -type f \
     \( -name '*.log' -o -name '*.tmp' -o -name '*.bak' -o -name '*~' -o -name '.DS_Store' -o -name '*.pyc' \
        -o -iname '*token*' -o -iname '*secret*' -o -iname '*cookie*' -o -iname '*password*' -o -iname '*credential*' \) \
     -print | sort
   ```
   Remove only exact generated files/directories after confirming they are safe.

5. **Validate before commit**
   ```bash
   PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile scripts/*.py
   PYTHONDONTWRITEBYTECODE=1 /opt/venv/bin/python scripts/agent_self_audit.py
   ```
   Completion requires the audit summary to show `fail=0`.

6. **Stage, commit, push**
   ```bash
   git add README.md jobs scripts skills memory .gitignore
   git status --short --branch
   git diff --cached --stat
   git commit -m "chore: describe exact maintenance change"
   GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' git push origin main
   ```
   If Git identity is `root <root@...>`, treat it as hygiene unless the user asked to fix authorship.

7. **Final handoff verification**
   ```bash
   GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' git fetch origin main --quiet
   git status --short --branch
   git rev-list --left-right --count main...origin/main
   git status --short --ignored
   PYTHONDONTWRITEBYTECODE=1 /opt/venv/bin/python scripts/agent_self_audit.py | tail -n 20
   git log --oneline --max-count=5
   ```
   Claim synced only when status is clean, divergence is `0 0`, sensitive scan is clean or explained, and audit ends with `fail=0`.

## SSH / Deploy Key Troubleshooting

When push/fetch fails, inspect before asking for new credentials. A `Permission denied (publickey)` may mean the remote is not using the dedicated alias, not that the key is absent.

Inspection order:

```bash
git remote -v
git status --short
git branch -vv
find /config/agent/runtime/git /root/.ssh /home -maxdepth 2 -type f 2>/dev/null
ssh-keygen -lf /config/agent/runtime/git/<repo-key>.pub
ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -T git@<host-alias>
GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' git fetch origin main
```

Alias rule: repositories with dedicated SSH aliases should use remotes like:

```text
git@<host-alias>:OWNER/REPO.git
```

Deploy Key write failure usually looks like:

```text
ERROR: Permission to OWNER/REPO.git denied to deploy key
```

In that case, keep the local commit and ask the user to enable write access or add a writable Deploy Key; do not redo work.

## First-Time GitHub Access Setup

Use only when the repository is not yet connected or the user asks to initialize access.

1. Confirm owner/repo, local path, host alias, and whether the key needs write access.
2. Generate runtime key; never store it in repo or memory:
   ```bash
   mkdir -p /config/agent/runtime/git
   chmod 700 /config/agent/runtime/git
   ssh-keygen -t ed25519 -C moviepilot-agent-runtime -f /config/agent/runtime/git/moviepilot-agent_ed25519 -N ''
   chmod 600 /config/agent/runtime/git/moviepilot-agent_ed25519
   chmod 644 /config/agent/runtime/git/moviepilot-agent_ed25519.pub
   ssh-keygen -lf /config/agent/runtime/git/moviepilot-agent_ed25519.pub
   cat /config/agent/runtime/git/moviepilot-agent_ed25519.pub
   ```
3. Write `/config/agent/runtime/git/ssh_config` with a dedicated host alias:
   ```text
   Host github.com-moviepilot-agent
     HostName github.com
     User git
     IdentityFile /config/agent/runtime/git/moviepilot-agent_ed25519
     IdentitiesOnly yes
   ```
4. Ask the user to add the public key as a GitHub Deploy Key. For push, GitHub must enable write access.
5. Verify auth, then clone or set the remote to `git@github.com-moviepilot-agent:clone-fan/moviepilot-agent.git`.

## Tracked Directory Removal Checklist

For intentional repository cleanup:

- Confirm the directory is tracked: `git ls-files | rg '(^|/)DIR(/|$)'`.
- Remove tracked files with Git, not broad filesystem deletes.
- Check sync scripts, jobs, README, and `.gitignore` for reintroduction paths.
- Validate no tracked files remain and no sync command re-adds them.
- Run the standard sensitive scan, audit, commit, push, and final verification.

## Output Contract

Report only evidence-backed results:

- repository path and branch state;
- what changed or why no change was needed;
- validation/audit summary;
- push/sync result and commit hash when applicable;
- remaining blocker, especially missing Deploy Key write access.
