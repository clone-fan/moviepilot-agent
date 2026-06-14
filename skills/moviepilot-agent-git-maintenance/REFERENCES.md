# moviepilot-agent Git 维护命令参考

本文件是 `moviepilot-agent-git-maintenance` 的低频命令模板。常规执行优先看 `SKILL.md`；进入具体 Git 同步、SSH 排障或首次接入时再读取这里。

## Locate and Inspect

```bash
cd /config/agent/repo/moviepilot-agent
pwd
git status --short --branch
git remote -v
git branch -vv
```

如果仓库缺失，只读定位：

```bash
find /config -maxdepth 4 -type d -name .git 2>/dev/null | sed 's#/.git$##' | sort
```

## Fetch and Divergence

```bash
GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' git fetch origin main
git rev-list --left-right --count main...origin/main
```

解释：

- `0 0`：本地远端一致。
- `0 N`：远端领先。
- `N 0`：本地领先。
- `N M`：双方分叉。

远端领先时：

```bash
git pull --rebase --autostash origin main
git rev-list --left-right --count main...origin/main
```

## Sync Agent Assets

优先使用确定性同步脚本：

```bash
/opt/venv/bin/python /config/agent/scripts/sync_moviepilot_agent_repo.py
```

常见结果：

- `OK no_changes`
- `OK no_staged_changes`
- `OK committed_and_pushed ...`

## Sensitive and Runtime Pollution Scan

```bash
git status --short --ignored
find . -path './.git' -prune -o -type f \
  \( -name '*.log' -o -name '*.tmp' -o -name '*.bak' -o -name '*~' -o -name '.DS_Store' -o -name '*.pyc' \
     -o -iname '*token*' -o -iname '*secret*' -o -iname '*cookie*' -o -iname '*password*' -o -iname '*credential*' \) \
  -print | sort
```

## Validate Before Commit

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile scripts/*.py
PYTHONDONTWRITEBYTECODE=1 /opt/venv/bin/python scripts/agent_self_audit.py
```

完成要求：审计摘要 `fail=0`。

## Stage, Commit, Push

```bash
git add README.md jobs scripts skills memory .gitignore
git status --short --branch
git diff --cached --stat
git commit -m "chore: describe exact maintenance change"
GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' git push origin main
```

## Final Handoff Verification

```bash
GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' git fetch origin main --quiet
git status --short --branch
git rev-list --left-right --count main...origin/main
git status --short --ignored
PYTHONDONTWRITEBYTECODE=1 /opt/venv/bin/python scripts/agent_self_audit.py | tail -n 20
git log --oneline --max-count=5
```

只有当工作区干净、分叉为 `0 0`、敏感扫描干净或已解释、审计 `fail=0` 时，才能说已同步。

## SSH / Deploy Key Inspection

```bash
git remote -v
git status --short
git branch -vv
find /config/agent/runtime/git /root/.ssh /home -maxdepth 2 -type f 2>/dev/null
ssh-keygen -lf /config/agent/runtime/git/<repo-key>.pub
ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -T git@<host-alias>
GIT_SSH_COMMAND='ssh -F /config/agent/runtime/git/ssh_config -o BatchMode=yes -o StrictHostKeyChecking=accept-new' git fetch origin main
```

## First-Time GitHub Access Setup

仅当仓库尚未接入或用户要求初始化访问时使用。

1. 确认 owner/repo、本地路径、Host alias，以及是否需要写权限。
2. 生成 runtime key，严禁写入 repo 或 memory：

```bash
mkdir -p /config/agent/runtime/git
chmod 700 /config/agent/runtime/git
ssh-keygen -t ed25519 -C moviepilot-agent-runtime -f /config/agent/runtime/git/moviepilot-agent_ed25519 -N ''
chmod 600 /config/agent/runtime/git/moviepilot-agent_ed25519
chmod 644 /config/agent/runtime/git/moviepilot-agent_ed25519.pub
ssh-keygen -lf /config/agent/runtime/git/moviepilot-agent_ed25519.pub
cat /config/agent/runtime/git/moviepilot-agent_ed25519.pub
```

3. 写 `/config/agent/runtime/git/ssh_config`：

```text
Host github.com-moviepilot-agent
  HostName github.com
  User git
  IdentityFile /config/agent/runtime/git/moviepilot-agent_ed25519
  IdentitiesOnly yes
```

4. 让用户把公钥添加为 GitHub Deploy Key。需要 push 时必须启用 write access。
5. 验证 auth 后 clone 或设置 remote：

```text
git@github.com-moviepilot-agent:clone-fan/moviepilot-agent.git
```
