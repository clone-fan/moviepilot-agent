#!/opt/venv/bin/python
from __future__ import annotations
import os, re, subprocess, sys
from pathlib import Path

REPO = Path('/config/agent/repo/Mihomo_Yaml')
RAW = Path('/config/agent/runtime/mihomo/config.raw.yaml')
OUT = REPO / 'mihomo_smart_config.yaml'
SSH_KEY = '/config/agent/runtime/ssh/mihomo-readonly_ed25519'
GIT_SSH_CFG = '/config/agent/runtime/git/ssh_config_mihomo_yaml'
REMOTE = 'root@10.0.0.2'
REMOTE_CONFIG = '/etc/mihomo/config.yaml'

SENSITIVE_RE = re.compile(r'nishisb|AAAAC3|BEGIN OPENSSH|PRIVATE KEY|url:\s*https?://|password:\s*[^<\"\']|secret:\s*[^<\"\']|token[:=]|机场订阅填到这里', re.I)

def run(cmd, cwd=None, input_text=None, check=True, env=None):
    p = subprocess.run(cmd, cwd=cwd, input=input_text, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    if check and p.returncode != 0:
        print(p.stdout, end='')
        print(p.stderr, end='', file=sys.stderr)
        raise SystemExit(p.returncode)
    return p

def main() -> int:
    RAW.parent.mkdir(parents=True, exist_ok=True)
    data = run(['ssh','-i',SSH_KEY,'-o','BatchMode=yes','-o','StrictHostKeyChecking=accept-new',REMOTE,'cat '+REMOTE_CONFIG]).stdout
    RAW.write_text(data, encoding='utf-8')
    RAW.chmod(0o600)

    run(['python3','scripts/sanitize_config.py',str(RAW),str(OUT)], cwd=REPO)
    run(['/opt/venv/bin/python','scripts/validate_yaml.py',str(OUT)], cwd=REPO)

    scan_text = ''
    for p in REPO.rglob('*'):
        if '.git' in p.parts or not p.is_file():
            continue
        try:
            txt = p.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        for i, line in enumerate(txt.splitlines(), 1):
            if SENSITIVE_RE.search(line):
                scan_text += f'{p.relative_to(REPO)}:{i}:{line}\n'
    # allow explicit placeholders only
    bad = []
    for line in scan_text.splitlines():
        if '<REDACTED_' in line:
            continue
        bad.append(line)
    if bad:
        print('FAIL sensitive content detected')
        print('\n'.join(bad))
        return 2

    env = os.environ.copy()
    env['GIT_SSH_COMMAND'] = f'ssh -F {GIT_SSH_CFG} -o BatchMode=yes -o StrictHostKeyChecking=accept-new'
    run(['git','fetch','origin','main'], cwd=REPO, env=env)
    div = run(['git','rev-list','--left-right','--count','main...origin/main'], cwd=REPO).stdout.strip()
    if div != '0\t0' and div != '0 0':
        run(['git','pull','--rebase','--autostash','origin','main'], cwd=REPO, env=env)
    run(['git','add','mihomo_smart_config.yaml'], cwd=REPO)
    staged = run(['git','diff','--cached','--quiet'], cwd=REPO, check=False)
    if staged.returncode == 0:
        print('OK no_changes')
        return 0
    run(['git','commit','-m','chore: daily update sanitized mihomo config'], cwd=REPO)
    run(['git','push','origin','main'], cwd=REPO, env=env)
    head = run(['git','rev-parse','--short','HEAD'], cwd=REPO).stdout.strip()
    print(f'OK committed_and_pushed {head}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
