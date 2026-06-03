#!/opt/venv/bin/python3
from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import shutil
import stat
import struct
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

REPO = 'vernesong/mihomo'
TAG = 'Prerelease-Alpha'
ASSET_RE = re.compile(r'^mihomo-linux-amd64-v3-alpha-smart-([0-9a-f]+)\.gz$')
API_URL = f'https://api.github.com/repos/{REPO}/releases/tags/{TAG}'
REMOTE = 'root@10.0.0.2'
SSH_KEY = '/config/agent/runtime/ssh/mihomo-readonly_ed25519'
REMOTE_BIN = '/etc/mihomo/bin/mihomo'
REMOTE_CONFIG_DIR = '/etc/mihomo'
WORKDIR = Path('/config/agent/runtime/mihomo/core-update')


def run(cmd: list[str], *, check: bool = True, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    p = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    if check and p.returncode != 0:
        print(p.stdout, end='')
        print(p.stderr, end='', file=sys.stderr)
        raise SystemExit(p.returncode)
    return p


def ssh(remote_cmd: str, *, check: bool = True, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return run([
        'ssh', '-i', SSH_KEY,
        '-o', 'BatchMode=yes',
        '-o', 'ConnectTimeout=8',
        '-o', 'StrictHostKeyChecking=accept-new',
        REMOTE, remote_cmd,
    ], check=check, timeout=timeout)


def fetch_json(url: str, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, headers={'User-Agent': 'MoviePilot-Agent'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def select_asset(data: dict) -> tuple[str, str, int, str]:
    matches = []
    for asset in data.get('assets') or []:
        name = asset.get('name') or ''
        m = ASSET_RE.match(name)
        if not m:
            continue
        matches.append((name, asset.get('browser_download_url'), int(asset.get('size') or 0), m.group(1)))
    if not matches:
        raise SystemExit('FAIL no matching linux-amd64-v3-alpha-smart .gz asset found')
    matches.sort(key=lambda item: item[0])
    return matches[-1]


def parse_current_hash(version_text: str) -> str | None:
    m = re.search(r'alpha-smart-([0-9a-f]+)', version_text)
    return m.group(1) if m else None


def download(url: str, dest: Path, retries: int = 3, timeout: int = 120) -> None:
    tmp = dest.with_suffix(dest.suffix + '.part')
    tmp.unlink(missing_ok=True)
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'MoviePilot-Agent'})
            with urllib.request.urlopen(req, timeout=timeout) as r, tmp.open('wb') as f:
                shutil.copyfileobj(r, f)
            tmp.replace(dest)
            return
        except Exception as e:  # network/CDN may be flaky
            last_error = e
            tmp.unlink(missing_ok=True)
            print(f'WARN download attempt {attempt}/{retries} failed: {type(e).__name__}: {e}')
    raise SystemExit(f'FAIL download failed after {retries} attempts: {last_error}')


def gunzip(src: Path, dest: Path) -> None:
    with gzip.open(src, 'rb') as g, dest.open('wb') as f:
        shutil.copyfileobj(g, f)
    dest.chmod(dest.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


    with path.open('rb') as f:
        ident = f.read(20)
    if len(ident) < 20 or ident[:4] != b'\x7fELF':
        return 'not-elf'
    elf_class = {1: 'ELF32', 2: 'ELF64'}.get(ident[4], f'class-{ident[4]}')
    endian = '<' if ident[5] == 1 else '>' if ident[5] == 2 else '<'
    machine = struct.unpack(endian + 'H', ident[18:20])[0]
    machine_name = {62: 'x86-64', 183: 'aarch64', 40: 'arm'}.get(machine, f'machine-{machine}')
    return f'{elf_class} {machine_name}'


def main() -> int:
    parser = argparse.ArgumentParser(description='Dry-run updater for vernesong mihomo linux-amd64-v3 alpha-smart core.')
    parser.add_argument('--skip-download', action='store_true', help='Only query release and remote version; do not download asset.')
    args = parser.parse_args()

    print(f'INFO release_api={API_URL}')
    data = fetch_json(API_URL)
    name, url, size, remote_hash = select_asset(data)
    print(f'INFO selected_asset={name}')
    print(f'INFO selected_size={size}')
    print(f'INFO remote_hash={remote_hash}')

    current = ssh(f'{REMOTE_BIN} -v 2>&1 | head -5', timeout=30).stdout.strip()
    current_hash = parse_current_hash(current)
    print('INFO current_version_begin')
    print(current)
    print('INFO current_version_end')
    print(f'INFO current_hash={current_hash or "unknown"}')
    print(f'INFO update_needed={str(current_hash != remote_hash).lower()}')

    if args.skip_download:
        print('OK dry_run_skip_download')
        return 0

    WORKDIR.mkdir(parents=True, exist_ok=True)
    gz = WORKDIR / name
    bin_path = WORKDIR / name[:-3]
    print(f'INFO download_url={url}')
    download(url, gz)
    if gz.stat().st_size <= 0:
        raise SystemExit('FAIL downloaded file is empty')
    print(f'INFO downloaded={gz} bytes={gz.stat().st_size}')

    gunzip(gz, bin_path)
    print(f'INFO extracted={bin_path} bytes={bin_path.stat().st_size}')

    file_out = inspect_elf(bin_path)
    print(f'INFO file={file_out}')
    if 'x86-64' not in file_out:
        raise SystemExit('FAIL extracted binary is not x86-64')

    new_version = run([str(bin_path), '-v'], timeout=30).stdout.strip()
    print('INFO new_version_begin')
    print(new_version)
    print('INFO new_version_end')
    if f'alpha-smart-{remote_hash}' not in new_version:
        raise SystemExit('FAIL new binary version does not match selected asset hash')

    # Validate existing production config with the new core without changing remote host.
    config_copy = WORKDIR / 'config.remote.yaml'
    scp = run([
        'scp', '-i', SSH_KEY,
        '-o', 'BatchMode=yes',
        '-o', 'ConnectTimeout=8',
        '-o', 'StrictHostKeyChecking=accept-new',
        f'{REMOTE}:{REMOTE_CONFIG_DIR}/config.yaml',
        str(config_copy),
    ], check=False, timeout=60)
    if scp.returncode == 0:
        test = run([str(bin_path), '-t', '-d', str(WORKDIR), '-f', str(config_copy)], check=False, timeout=60)
        print('INFO config_test_stdout_begin')
        print(test.stdout.strip())
        print('INFO config_test_stdout_end')
        if test.stderr.strip():
            print('INFO config_test_stderr_begin')
            print(test.stderr.strip())
            print('INFO config_test_stderr_end')
        print(f'INFO config_test_returncode={test.returncode}')
    else:
        print('WARN remote config copy failed; skip config test')
        if scp.stderr.strip():
            print(scp.stderr.strip())

    print('OK dry_run_complete')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
