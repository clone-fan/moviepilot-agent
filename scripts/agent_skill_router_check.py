#!/opt/venv/bin/python
"""Deterministic routing sanity checks for MoviePilot Agent skills."""
from __future__ import annotations
import sys
sys.dont_write_bytecode = True
CASES = [
    ('/sites', 'moviepilot-direct-routes'),
    ('查看正在下载', 'moviepilot-direct-routes'),
    ('帮我搜阿凡达 4K 资源', 'resource-search'),
    ('订阅绝命毒师第一季', 'moviepilot-cli'),
    ('调用 MoviePilot API 查询站点', 'moviepilot-api'),
    ('重启 MoviePilot', 'moviepilot-update'),
    ('转移失败记录 123 重试', 'transfer-failed-retry'),
]


def route(text: str) -> str:
    t = text.lower()
    if t.startswith('/') or any(k in t for k in ('115', '磁力', 'magnet', 'ed2k', '正在下载', '查看下载')):
        return 'moviepilot-direct-routes'
    if any(k in t for k in ('搜', '资源', '种子', '4k', '1080p', 'bluray')) and not any(k in t for k in ('订阅', 'api')):
        return 'resource-search'
    if 'api' in t:
        return 'moviepilot-api'
    if any(k in t for k in ('重启', '升级', '版本')):
        return 'moviepilot-update'
    if any(k in t for k in ('转移失败', '失败记录', '重新整理')):
        return 'transfer-failed-retry'
    return 'moviepilot-cli'


def main():
    failed = 0
    for text, expected in CASES:
        actual = route(text)
        ok = actual == expected
        failed += 0 if ok else 1
        print(('PASS' if ok else 'FAIL') + f' | {text} | expected={expected} actual={actual}')
    print(f'SUMMARY total={len(CASES)} pass={len(CASES)-failed} fail={failed}')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
