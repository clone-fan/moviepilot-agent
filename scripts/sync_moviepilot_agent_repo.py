#!/opt/venv/bin/python
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SRC = Path('/config/agent')
REPO = Path('/config/agent/repo/moviepilot-agent')
SSH_CONFIG = Path('/config/agent/runtime/git/ssh_config')

SYNC_ITEMS = [
    ('skills', REPO / 'skills'),
    ('runtime/personas', REPO / 'runtime/personas'),
    ('memory', REPO / 'memory'),
    ('jobs', REPO / 'jobs'),
    ('scripts', REPO / 'scripts'),
    ('docs', REPO / 'docs'),
]

EXCLUDE_NAME_RE = re.compile(r'(token|secret|cookie|password|credential)', re.I)
EXCLUDE_SUFFIXES = {'.pyc', '.log', '.tmp', '.bak', '.db', '.sqlite', '.sqlite3', '.dump', '.sql', '.env'}
EXCLUDE_DIRS = {'.git', '__pycache__', 'cache', 'activity'}
SECRET_PATTERNS = [
    re.compile(r'BEGIN (RSA|OPENSSH|DSA|EC|PRIVATE) KEY'),
    re.compile(r'github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{20,}'),
]


def run(cmd: list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> str:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None, env=merged, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if proc.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd)}\n{proc.stdout}")
    return proc.stdout


def excluded(path: Path) -> bool:
    parts = set(path.parts)
    if parts & EXCLUDE_DIRS:
        return True
    name = path.name
    if EXCLUDE_NAME_RE.search(name):
        return True
    if path.suffix.lower() in EXCLUDE_SUFFIXES:
        return True
    if name.startswith('.env'):
        return True
    if name in {'id_rsa', 'id_ed25519'}:
        return True
    return False


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True, exist_ok=True)
    if not src.exists():
        return
    for item in src.rglob('*'):
        rel = item.relative_to(src)
        if excluded(rel) or excluded(item):
            continue
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def write_repo_basics() -> None:
    (REPO / '.gitignore').write_text("""# secrets / credentials
*.key
*.pem
*.crt
*.p12
*.pfx
*.env
.env*
*token*
*secret*
*cookie*
*password*
*credential*
id_rsa*
id_ed25519*

# runtime cache / logs / activity
runtime/cache/
activity/
logs/
*.log
*.pid
*.tmp
*.bak
*.swp

# databases / dumps / large runtime data
*.db
*.sqlite
*.sqlite3
*.dump
*.sql

# python
__pycache__/
*.py[cod]
.pytest_cache/
.venv/
venv/

# system
.DS_Store
Thumbs.db
""", encoding='utf-8')


def secret_scan() -> None:
    found: list[str] = []
    for p in REPO.rglob('*'):
        if not p.is_file() or '.git' in p.parts:
            continue
        try:
            text = p.read_text(errors='ignore')
        except Exception:
            continue
        for pat in SECRET_PATTERNS:
            if pat.search(text):
                found.append(str(p.relative_to(REPO)))
                break
    if found:
        raise RuntimeError('secret scan failed: ' + ', '.join(found[:20]))


def main() -> int:
    if not (REPO / '.git').exists():
        raise RuntimeError(f'repo missing: {REPO}')
    run(['git', 'pull', '--ff-only'], cwd=REPO, env={'GIT_SSH_COMMAND': f'ssh -F {SSH_CONFIG}'})
    write_repo_basics()
    for src_rel, dst in SYNC_ITEMS:
        copy_tree(SRC / src_rel, dst)
    # 仓库副本禁止携带运行环境固定凭据；同步阶段已排除敏感命名文件。
    secret_scan()
    status = run(['git', 'status', '--porcelain'], cwd=REPO)
    if not status.strip():
        print('OK no_changes')
        return 0
    run(['git', 'add', 'README.md', '.gitignore', 'skills', 'runtime', 'memory', 'jobs', 'scripts', 'docs'], cwd=REPO)
    staged = run(['git', 'diff', '--cached', '--name-only'], cwd=REPO)
    if not staged.strip():
        print('OK no_staged_changes')
        return 0
    env = {
        'GIT_AUTHOR_NAME': 'moviepilot-agent',
        'GIT_AUTHOR_EMAIL': 'moviepilot-agent@users.noreply.github.com',
        'GIT_COMMITTER_NAME': 'moviepilot-agent',
        'GIT_COMMITTER_EMAIL': 'moviepilot-agent@users.noreply.github.com',
        'GIT_SSH_COMMAND': f'ssh -F {SSH_CONFIG}',
    }
    run(['git', 'commit', '-m', 'chore: weekly sync agent capability assets'], cwd=REPO, env=env)
    run(['git', 'push', 'origin', 'main'], cwd=REPO, env=env)
    latest = run(['git', 'log', '--oneline', '-1'], cwd=REPO)
    print('OK committed_and_pushed ' + latest.strip())
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as e:
        print('ERROR', e)
        raise SystemExit(1)
