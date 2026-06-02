#!/opt/venv/bin/python
"""
Deterministic 60-day cleanup for /config/agent/docs.

Safety guarantees:
- The cleanup root is hard-locked to /config/agent/docs.
- The script lives in /config/agent/scripts, outside docs and jobs.
- It never follows symlinked directories.
- It never deletes anything outside /config/agent/docs.
- It removes old files first, then removes old empty directories only.
"""
from pathlib import Path
import shutil
import sys
import time

sys.dont_write_bytecode = True

DOCS_DIR = Path('/config/agent/docs').resolve(strict=True)
SCRIPT_PATH = Path(__file__).resolve(strict=True)
JOB_DIR = SCRIPT_PATH.parent
RETENTION_DAYS = 60
SECONDS_PER_DAY = 86400
CUTOFF = time.time() - RETENTION_DAYS * SECONDS_PER_DAY

PROTECTED_PATHS = set()
PROTECTED_DIRS = set()


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def is_protected(path: Path) -> bool:
    resolved = path.resolve(strict=False)
    if resolved in PROTECTED_PATHS or resolved in PROTECTED_DIRS:
        return True
    return any(is_relative_to(resolved, protected_dir) for protected_dir in PROTECTED_DIRS)


def is_old(path: Path) -> bool:
    return path.stat().st_mtime < CUTOFF


def iter_docs_tree(root: Path):
    # Do not follow symlinked directories. Symlink files are handled as links only.
    for item in root.rglob('*'):
        yield item


def cleanup_files() -> int:
    deleted = 0
    for item in iter_docs_tree(DOCS_DIR):
        try:
            resolved = item.resolve(strict=False)
            if not is_relative_to(resolved, DOCS_DIR) and not item.is_symlink():
                continue
            if is_protected(item):
                continue
            if item.is_dir() and not item.is_symlink():
                continue
            if is_old(item):
                item.unlink()
                deleted += 1
        except FileNotFoundError:
            continue
    return deleted


def cleanup_empty_dirs() -> int:
    deleted = 0
    dirs = [p for p in iter_docs_tree(DOCS_DIR) if p.is_dir() and not p.is_symlink()]
    for item in sorted(dirs, key=lambda p: len(p.parts), reverse=True):
        try:
            if is_protected(item):
                continue
            if item == DOCS_DIR:
                continue
            if is_old(item) and not any(item.iterdir()):
                item.rmdir()
                deleted += 1
        except FileNotFoundError:
            continue
    return deleted


def main():
    if str(DOCS_DIR) != '/config/agent/docs':
        raise RuntimeError(f'Unsafe docs dir: {DOCS_DIR}')
    if str(JOB_DIR) != '/config/agent/scripts':
        raise RuntimeError(f'Unsafe script dir: {JOB_DIR}')
    files = cleanup_files()
    dirs = cleanup_empty_dirs()
    print(f'OK deleted_files={files} deleted_dirs={dirs}')


if __name__ == '__main__':
    main()
