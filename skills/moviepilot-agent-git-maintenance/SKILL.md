---
name: moviepilot-agent-git-maintenance
version: 1
description: >-
  Use this skill when maintaining the moviepilot-agent Git repository, syncing Agent capability assets, removing tracked directories from the repository, fixing failed Git pushes, restoring SSH alias or Deploy Key access, or performing handoff-safe Git cleanup and final verification.
allowed-tools: read_file list_directory execute_command edit_file write_file
---

# MoviePilot Agent Git Maintenance

## Purpose

Use this skill to maintain the `moviepilot-agent` repository as a handoff-safe capability-asset store, not as a one-off Git command runner.

The goal is to leave the repository in a state that another agent can inspect and continue without relying on chat context.

## Hard Rules

- Do not store operational lessons in long-term memory when the user asks for a reusable Git process. Put the process in this skill.
- Do not commit runtime secrets, tokens, cookies, private keys, cache files, logs, activity logs, or transient archives.
- Do not echo private key contents. Public key fingerprints are safe; private key contents are not.
- Do not assume `git status` alone proves completion.
- If deleting a tracked directory, also remove every future source that could reintroduce it.
- If the remote is ahead, do not force push. Fetch and rebase first.

## Canonical Repository

Default repository path used in this environment:

```text
/config/agent/repo/moviepilot-agent
```

Runtime SSH assets may live under:

```text
/config/agent/runtime/git/
```

Typical dedicated alias:

```text
github.com-moviepilot-agent
```

## When To Use

Use this skill for requests like:

- “维护 moviepilot-agent 仓库”
- “把 Agent 能力资产同步到 Git”
- “从 Git 删除某个目录并确保以后不再同步”
- “检查仓库还有哪里没有收尾”
- “Git 推送失败，恢复 Deploy Key / SSH alias”
- “做一次可交接的 Git 收尾校验”

Do not use it for ordinary media search, downloads, subscriptions, or MoviePilot site tasks.

## Workflow

### 1. Locate And Inspect

Start from the real repository, not the process working directory.

```bash
cd /config/agent/repo/moviepilot-agent
pwd
git status --short --branch
git remote -v
git branch -vv
```

If the repository is not found, locate it read-only:

```bash
find /config -maxdepth 4 -type d -name .git 2>/dev/null | sed 's#/.git$##' | sort
```

### 2. Check Remote And SSH Before Pushing

If the remote uses an alias, verify the alias and Deploy Key before changing URLs.

```bash
git remote -v
find /config/agent/runtime/git /root/.ssh /moviepilot/.ssh -maxdepth 2 -type f 2>/dev/null
ssh-keygen -lf /config/agent/runtime/git/moviepilot-agent_ed25519.pub
GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' \
  ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -T git@github.com-moviepilot-agent
```

Expected successful GitHub message:

```text
Hi clone-fan/moviepilot-agent! You've successfully authenticated, but GitHub does not provide shell access.
```

If standard `git@github.com:` fails with `Permission denied (publickey)`, restore the dedicated alias path instead of assuming credentials are missing.

### 3. Fetch And Resolve Remote Divergence

Always fetch before committing or pushing.

```bash
GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' \
  git fetch origin main

git rev-list --left-right --count main...origin/main
```

Interpretation:

- `0 0`: local and remote match.
- `0 N`: remote is ahead; run rebase before committing.
- `N 0`: local is ahead; verify then push.
- `N M`: branches diverged; inspect logs before changing history.

When remote is ahead:

```bash
GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' \
  git pull --rebase --autostash origin main
```

After `--autostash`, staged changes may become unstaged. Re-check and re-stage intentionally.

### 4. If Removing A Directory From Git

Deleting tracked files is only half the task. Also remove future reintroduction points.

Check tracked files:

```bash
git ls-files | rg '(^|/)docs(/|$)' || true
```

Check explicit sync or documentation references:

```bash
python3 - <<'PY'
from pathlib import Path
patterns=["('docs'", '"docs"', "'docs'", 'git add docs', '`docs/`：', '└── docs/', '- `docs/`']
for file in ['README.md','jobs/moviepilot-agent-weekly-sync/JOB.md','scripts/sync_moviepilot_agent_repo.py']:
    p=Path(file)
    if not p.exists():
        continue
    for i,line in enumerate(p.read_text().splitlines(),1):
        if any(x in line for x in patterns):
            print(f'{file}:{i}:{line}')
PY
```

For the `docs` cleanup case, ensure all of these are true:

- No tracked `docs/**` files remain.
- Sync script does not copy `docs`.
- Sync script does not run `git add ... docs`.
- Weekly sync Job no longer lists `docs/` as a synced asset.
- README no longer presents `docs/` as repository content.

### 5. Check For Runtime Or Sensitive Pollution

Before commit:

```bash
git status --short --ignored
find . -path './.git' -prune -o -type f \
  \( -name '*.log' -o -name '*.tmp' -o -name '*.bak' -o -name '*~' -o -name '.DS_Store' -o -name '*.pyc' \
     -o -iname '*token*' -o -iname '*secret*' -o -iname '*cookie*' -o -iname '*password*' -o -iname '*credential*' \) \
  -print | sort
```

If Python generated `__pycache__`, remove only the exact generated directories. Do not use broad destructive delete commands.

### 6. Validate Before Commit

Run syntax and project self-checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile scripts/*.py
PYTHONDONTWRITEBYTECODE=1 /opt/venv/bin/python scripts/agent_self_audit.py
```

Do not claim success unless the audit ends with:

```text
SUMMARY total=76 pass=76 fail=0
```

If totals change because the audit script changed, report the new total and the exact pass/fail summary.

### 7. Stage, Commit, Push

After rebase/autostash, stage again.

```bash
git add README.md jobs scripts skills memory .gitignore
# For intentional deletions, ensure deletion entries are staged too.
git status --short --branch
git diff --cached --stat
git commit -m "chore: describe exact maintenance change"
GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' \
  git push origin main
```

If Git identity appears as `root <root@...>`, treat it as a non-blocking hygiene issue unless the user requires author correction. Mention it separately.

### 8. Final Handoff Verification

A handoff-safe finish requires fresh evidence:

```bash
GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' \
  git fetch origin main --quiet

git status --short --branch
git rev-list --left-right --count main...origin/main
git ls-files | rg '(^|/)docs(/|$)' || true
git status --short --ignored
PYTHONDONTWRITEBYTECODE=1 /opt/venv/bin/python scripts/agent_self_audit.py | tail -n 20
git log --oneline --max-count=5
```

Minimum final evidence:

- `git status --short --branch` shows no dirty files.
- `git rev-list --left-right --count main...origin/main` returns `0 0`.
- Removed tracked directories have no `git ls-files` output.
- Relevant reference checks return no output or an explicit `OK`.
- Self-audit is green.
- Latest commit is visible in `git log`.

## Common Failure Patterns

### Alias Missing

Symptom:

```text
ssh: Could not resolve hostname github.com-moviepilot-agent
```

Likely cause: SSH alias config not loaded or missing. Use runtime SSH config explicitly rather than changing strategy blindly.

### Standard GitHub SSH Denied

Symptom:

```text
git@github.com: Permission denied (publickey)
```

Likely cause: default SSH key is not the repository Deploy Key. Restore the dedicated alias and key path.

### Remote Ahead After User Or Web Change

Symptom:

```text
0 1
```

Likely cause: a commit exists on GitHub already. Rebase with autostash, then re-stage local changes.

### Commit Says No Changes Added

Cause: `pull --rebase --autostash` reapplied changes unstaged. Run `git status`, `git add`, and `git diff --cached --stat` again.

### Directory Deleted But Later Reappears

Cause: sync script, Job, or README still references it. Remove the future source, not only tracked files.

## Final Response Pattern

Report compactly:

- What changed.
- Commit hash and push result.
- Verification evidence.
- Remaining non-blocking hygiene items, if any.

Never say “完成” from memory. Say it only after fresh verification output supports it.
