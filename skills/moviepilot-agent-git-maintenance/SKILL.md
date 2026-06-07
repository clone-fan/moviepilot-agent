---
name: moviepilot-agent-git-maintenance
version: 5
description: >-
  Use this skill when maintaining the moviepilot-agent Git repository, syncing
  Agent capability assets, prompting for repository sync after /config/agent
  capability changes, removing tracked directories, fixing failed Git pushes,
  initializing GitHub SSH/Deploy Key access from zero, restoring SSH alias or
  Deploy Key access, or performing handoff-safe Git cleanup and final
  verification.
allowed-tools: read_file list_directory execute_command edit_file write_file ask_user_choice
---

# MoviePilot Agent Git Maintenance

## Purpose

Use this skill to maintain the `moviepilot-agent` repository as a handoff-safe
capability-asset store, not as a one-off Git command runner.

The goal is to leave the repository in a state that another agent can inspect and
continue without relying on chat context.

## Responsibility Split

- `moviepilot-agent-git-maintenance`: Agent Git repository maintenance,
  immediate sync reminders, self-checks, sensitive scans, commit, push, and
  handoff verification.
- `moviepilot-agent-weekly-sync` Job: recurring weekly automatic sync.
- `tg-button-interaction`: only button UX and safety for choices.
- `create-moviepilot-skill`: only skill creation/update workflow; hand off Git
  sync concerns here.

## Hard Rules

- Do not store operational lessons in long-term memory when the user asks for a
  reusable Git process. Put the process in this skill.
- Do not commit runtime secrets, tokens, cookies, private keys, cache files,
  logs, activity logs, or transient archives.
- Do not echo private key contents. Public key fingerprints are safe; private
  key contents are not.
- Do not assume `git status` alone proves completion.
- If deleting a tracked directory, also remove every future source that could
  reintroduce it.
- If the remote is ahead, do not force push. Fetch and rebase first.
- Repository sync prompts after capability changes are reminders, not permission
  to skip validation, sensitive scans, commit review, or push confirmation.

## Canonical Repository

Default repository path:

```text
/config/agent/repo/moviepilot-agent
```

Runtime SSH assets:

```text
/config/agent/runtime/git/
```

Typical dedicated alias:

```text
github.com-moviepilot-agent
```

Weekly sync Job and script:

```text
/config/agent/jobs/moviepilot-agent-weekly-sync/JOB.md
/config/agent/scripts/sync_moviepilot_agent_repo.py
```

## When To Use

Use this skill for requests like:

- “维护 moviepilot-agent 仓库”
- “把 Agent 能力资产同步到 Git”
- “Agent/skill 更新后提醒我同步仓库”
- “提交并推送 Agent 能力变更”
- “从 Git 删除某个目录并确保以后不再同步”
- “检查仓库还有哪里没有收尾”
- “Git 推送失败，恢复 Deploy Key / SSH alias”
- “做一次可交接的 Git 收尾校验”

Do not use it for ordinary media search, downloads, subscriptions, or
MoviePilot site tasks.

## Immediate Sync Reminder After `/config/agent` Changes

When an Agent capability asset under `/config/agent` is created, updated,
distilled, finalized, version-bumped, validated, or otherwise made reusable,
consider whether to offer an immediate `moviepilot-agent` repository sync in
addition to the weekly sync Job.

Typical trigger paths:

- `/config/agent/skills/**/SKILL.md`
- `/config/agent/jobs/*/JOB.md`
- `/config/agent/scripts/**`
- `/config/agent/runtime/personas/**/PERSONA.md`
- `/config/agent/memory/*.md` when the change is intentionally durable

Do not prompt for sync after purely transient cache/log/activity/runtime-secret
changes.

If the user has not already explicitly requested commit/push, use buttons when
available:

- `同步并推送`
- `只提交`
- `先只读检查`
- `暂不同步`

The reminder supplements, not replaces, the weekly Job. Before any commit/push,
run the normal inspect → validate → sensitive scan → staged diff → commit/push →
final verification sequence.

## First-Time GitHub Access Setup

Use this section when the repository has not been connected yet, or when the user
asks to接入 GitHub / 新建仓库 / 配置 Deploy Key.

### 0. Required Inputs

Confirm these before creating credentials or changing remotes:

- GitHub repository owner/name, for example `clone-fan/moviepilot-agent`.
- Whether the key should be read-only or allow write access. For maintenance
  push, Deploy Key must allow write access.
- Local repository path, normally `/config/agent/repo/moviepilot-agent`.
- Dedicated alias, normally `github.com-moviepilot-agent`.

Never ask the user to paste private keys. Never save tokens or passwords in
memory or repository files.

### 1. Create Dedicated Runtime SSH Assets

Store Git SSH material under runtime, not memory and not the Git repository.

```bash
mkdir -p /config/agent/runtime/git
chmod 700 /config/agent/runtime/git
ssh-keygen -t ed25519 -C moviepilot-agent-runtime -f /config/agent/runtime/git/moviepilot-agent_ed25519 -N ''
chmod 600 /config/agent/runtime/git/moviepilot-agent_ed25519
chmod 644 /config/agent/runtime/git/moviepilot-agent_ed25519.pub
ssh-keygen -lf /config/agent/runtime/git/moviepilot-agent_ed25519.pub
cat /config/agent/runtime/git/moviepilot-agent_ed25519.pub
```

Only show the public key to the user. Ask the user to add it to GitHub repository
settings as a Deploy Key. For push maintenance, GitHub must enable write access
for that Deploy Key.

### 2. Write Dedicated SSH Config

```bash
cat > /config/agent/runtime/git/ssh_config <<'EOF'
Host github.com-moviepilot-agent
  HostName github.com
  User git
  IdentityFile /config/agent/runtime/git/moviepilot-agent_ed25519
  IdentitiesOnly yes
EOF
chmod 600 /config/agent/runtime/git/ssh_config
```

Do not put this private key or config inside the repository.

### 3. Verify GitHub Authentication

```bash
GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' \
  ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -T git@github.com-moviepilot-agent
```

Expected success:

```text
Hi OWNER/REPO! You've successfully authenticated, but GitHub does not provide shell access.
```

If GitHub says permission denied, the public key has not been added, was added to
the wrong repository, or lacks write access for push.

### 4. Clone Or Attach The Repository

For a fresh clone:

```bash
mkdir -p /config/agent/repo
GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' \
  git clone git@github.com-moviepilot-agent:clone-fan/moviepilot-agent.git /config/agent/repo/moviepilot-agent
```

For an existing local repository:

```bash
cd /config/agent/repo/moviepilot-agent
git remote set-url origin git@github.com-moviepilot-agent:clone-fan/moviepilot-agent.git
git remote -v
GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' git fetch origin main
```

### 5. Configure Repository Identity When Required

If commits show `root <root@moviepilot-v2>` and the user wants a stable author,
set repository-local identity only:

```bash
cd /config/agent/repo/moviepilot-agent
git config user.name 'MoviePilot Agent'
git config user.email 'moviepilot-agent@users.noreply.github.com'
git config --local --list | rg '^(user.name|user.email)'
```

Do not store personal email unless the user explicitly provides it and wants it
used.

## Git SSH / Deploy Key Troubleshooting Distillation

Use this distilled checklist whenever GitHub SSH, Deploy Key, remote alias,
or push permission problems appear. Do not put this workflow into long-term
memory; keep it here so it is loaded only when this Git maintenance skill is
selected.

### Evidence Before Judgement

Never treat `Permission denied (publickey)` as proof that the user has not
configured a public key. First distinguish these cases:

- a dedicated key exists but the repository remote still uses plain
  `git@github.com:OWNER/REPO.git`;
- an SSH Host alias exists but Git is not using the configured ssh config;
- authentication or `git fetch` works but the Deploy Key is read-only;
- the repository requires `ssh.github.com` on port `443`;
- the configured key belongs to another repository or another host alias.

If the user says the key was already configured, assume an alias/remote/key
permission mapping issue until inspected.

### Canonical Inspection Order

For any maintained Git repository, inspect in this order before changing
configuration or asking the user to regenerate keys:

```bash
git remote -v
git status --short
git branch -vv
find /config/agent/runtime/git /root/.ssh /home -maxdepth 2 -type f 2>/dev/null
ssh-keygen -lf /config/agent/runtime/git/<repo-key>.pub
ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -T git@<host-alias>
GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' \
  git fetch origin main
```

Prefer reading `/config/agent/runtime/git/REPO_SSH_MAP.md` for repository-specific
non-secret anchors: repository name, local path, Host alias, public-key
fingerprint, and purpose. This runtime file should contain facts only, not lessons, and is not part of always-loaded long-term memory.

### Remote Alias Rules

If a repository has a dedicated Host alias, its remote should use that alias:

```text
git@<host-alias>:OWNER/REPO.git
```

Example:

```text
git@github.com-moviepilot-css:clone-fan/moviepilot-css.git
```

When running Git commands against aliased hosts in this runtime, explicitly pass
the ssh config unless already proven unnecessary:

```bash
GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' git fetch origin main
```

### Read Access Is Not Write Access

`ssh -T` success or `git fetch` success only proves the key can authenticate
and read. It does not prove push permission. For Deploy Keys, write permission
requires GitHub repository settings to enable `Allow write access`.

If push fails with:

```text
ERROR: Permission to OWNER/REPO.git denied to deploy key
```

then keep the local commit, ask for write access or a new writable Deploy Key,
and after permission is fixed continue pushing the existing `HEAD`. Do not redo
the work.

### Generating Or Replacing Deploy Keys

When generating a repository-specific key:

- store it under `/config/agent/runtime/git/`;
- use a repository-specific filename and comment, e.g.
  `moviepilot-css_ed25519` / `moviepilot-css-runtime`;
- never show or store the private key;
- show only the `.pub` content and public fingerprint;
- configure a dedicated Host alias in `/config/agent/runtime/git/ssh_config`;
- update the repository remote to the Host alias after user authorization;
- record only non-sensitive anchors in `/config/agent/runtime/git/REPO_SSH_MAP.md`.

### Completion Verification

After a push, verify with fresh evidence:

```bash
git fetch origin main
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
git status --short
git --no-pager log --oneline -3
```

Only then claim that the repository is synchronized.

## Maintenance Workflow

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

If the remote uses an alias, verify the alias and Deploy Key before changing
URLs.

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

If standard `git@github.com:` fails with `Permission denied (publickey)`, restore
the dedicated alias path instead of assuming credentials are missing.

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

After `--autostash`, staged changes may become unstaged. Re-check and re-stage
intentionally.

### 4. Sync Runtime Assets Into Repo

Prefer the deterministic sync script for normal capability-asset sync:

```bash
/opt/venv/bin/python /config/agent/scripts/sync_moviepilot_agent_repo.py
```

Expected success includes one of:

```text
OK no_changes
OK no_staged_changes
OK committed_and_pushed ...
```

If doing a manual sync, copy only allowed asset classes and keep exclusions:

- include: `skills/`, `runtime/personas/`, `memory/`, `jobs/`, `scripts/`
- exclude: `docs/`, runtime secrets, logs, caches, activity, databases

### 5. If Removing A Directory From Git

Deleting tracked files is only half the task. Also remove future reintroduction
points.

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

### 6. Check For Runtime Or Sensitive Pollution

Before commit:

```bash
git status --short --ignored
find . -path './.git' -prune -o -type f \
  \( -name '*.log' -o -name '*.tmp' -o -name '*.bak' -o -name '*~' -o -name '.DS_Store' -o -name '*.pyc' \
     -o -iname '*token*' -o -iname '*secret*' -o -iname '*cookie*' -o -iname '*password*' -o -iname '*credential*' \) \
  -print | sort
```

If Python generated `__pycache__`, remove only the exact generated directories.
Do not use broad destructive delete commands.

### 7. Validate Before Commit

Run syntax and project self-checks:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile scripts/*.py
PYTHONDONTWRITEBYTECODE=1 /opt/venv/bin/python scripts/agent_self_audit.py
```

Do not claim success unless the audit ends with a green `SUMMARY ... fail=0`.
If totals change because the audit script changed, report the new total and the
exact pass/fail summary.

### 8. Stage, Commit, Push

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

If Git identity appears as `root <root@...>`, treat it as a non-blocking hygiene
issue unless the user requires author correction. Mention it separately.

### 9. Final Handoff Verification

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

Likely cause: SSH alias config not loaded or missing. Use runtime SSH config
explicitly rather than changing strategy blindly.

### Standard GitHub SSH Denied

Symptom:

```text
git@github.com: Permission denied (publickey)
```

Likely cause: default SSH key is not the repository Deploy Key. Restore the
dedicated alias and key path.

### Remote Ahead After User Or Web Change

Symptom:

```text
0 1
```

Likely cause: a commit exists on GitHub already. Rebase with autostash, then
re-stage local changes.

### Commit Says No Changes Added

Cause: `pull --rebase --autostash` reapplied changes unstaged. Run `git status`,
`git add`, and `git diff --cached --stat` again.

### Directory Deleted But Later Reappears

Cause: sync script, Job, or README still references it. Remove the future source,
not only tracked files.

## Final Response Pattern

Report compactly:

- What changed.
- Commit hash and push result.
- Verification evidence.
- Remaining non-blocking hygiene items, if any.

Never say “完成” from memory. Say it only after fresh verification output supports
it.

## Version Rollback Support

Use this section when the user asks to roll back, restore an older version,
recover from a bad maintenance sync, or inspect history for any maintained Git
repository.

### Rollback Principles

- Keep history, do not erase it by default.
- Prefer `git revert <commit>` for full-commit rollback because it preserves an
audit trail and is safe for shared remote branches.
- Prefer file-level restore plus a new commit when only one file or directory
should be restored.
- Avoid `git reset --hard` and force push unless the user explicitly asks to
rewrite remote history after seeing the risk.
- Before rollback, always inspect current status, fetch remote, and identify the
exact bad commit and target good commit.
- Before pushing rollback, run the same validation and sensitive scan used by the
normal maintenance workflow.

### Maintained Repository Inventory

Known maintained repositories may include:

```text
/config/agent/repo/moviepilot-agent
/config/agent/repo/Mihomo_Yaml
```

Discover current maintained repositories with:

```bash
find /config/agent/repo -maxdepth 2 -type d -name .git -print | sed 's#/.git$##' | sort
```

### Safe Rollback Workflow

1. Inspect history read-only:

```bash
cd <repo>
git fetch origin main
git status --short --branch
git log --oneline --decorate -20
```

2. Show the suspected bad change:

```bash
git show --stat <bad_commit>
git show --name-only <bad_commit>
```

3. Choose rollback mode:

- Whole commit rollback:

```bash
git revert <bad_commit>
```

- File-level restore from a known good commit:

```bash
git checkout <good_commit> -- path/to/file
# or: git restore --source <good_commit> -- path/to/file
git diff -- path/to/file
git commit -m "revert: restore <file> from <good_commit>"
```

- View only, no change:

```bash
git show <commit>:path/to/file
```

4. Validate before push:

```bash
git status --short --branch
# run repository-specific validation / dry-run / sensitive scan
```

5. Push only after confirmation or explicit user instruction:

```bash
git push origin main
```

6. Final verification:

```bash
git fetch origin main
git status --short --branch
git rev-parse HEAD
git rev-parse origin/main
```

### User Handoff

When the user reports a problem after maintenance:

- First ask or infer which repository is affected.
- Inspect recent commits and present candidate rollback points.
- Recommend the least destructive rollback path.
- Use buttons for rollback confirmation when available.
- Never force push as the default recovery path.
