#!/opt/venv/bin/python
"""MoviePilot operational health check using internal API only."""
from __future__ import annotations
import contextlib
import io
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime

sys.dont_write_bytecode = True
API = 'http://127.0.0.1:3001/api/v1'
TOKEN = os.environ.get('MOVIEPILOT_API_TOKEN') or 'ixOAH5i85GaHQiFajFyBzw'


def get(path: str):
    separator = '&' if '?' in path else '?'
    url = API + path + separator + urllib.parse.urlencode({'token': TOKEN})
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = resp.read().decode('utf-8')
    try:
        return json.loads(data)
    except Exception:
        return data


def unwrap(data):
    if isinstance(data, dict):
        if data.get('success') is True and 'data' in data:
            return data['data']
        if 'data' in data and len(data) <= 3:
            return data['data']
    return data


def count_items(value):
    value = unwrap(value)
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        for key in ('items', 'list', 'data', 'results'):
            if isinstance(value.get(key), list):
                return len(value[key])
    return None


@contextlib.contextmanager
def quiet_moviepilot_imports():
    old_stdout, old_stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
    try:
        yield
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr


def main():
    checks = []
    def add(name, ok, detail=''):
        checks.append({'name': name, 'ok': bool(ok), 'detail': str(detail or '')})
        print(('PASS' if ok else 'FAIL') + f' | {name}' + (f' | {detail}' if detail else ''))

    print('MOVIEPILOT_HEALTH_CHECK', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    # Prefer endpoints that explicitly support API_TOKEN (?token=...).
    # Browser/JWT-only endpoints are intentionally not used here, otherwise
    # a headless health probe reports false 401 failures.
    for name, path in [
        ('subscribe', '/subscribe/list'),
    ]:
        try:
            data = get(path)
            item_count = count_items(data)
            detail = f'count={item_count}' if item_count is not None else f'type={type(unwrap(data)).__name__}'
            add(name, True, detail)
        except Exception as e:
            add(name, False, repr(e))

    # Site list, downloader config and scheduler list are superuser-session
    # endpoints in this MP build. Check the same operational state through
    # internal modules while suppressing MoviePilot module initialization logs.
    try:
        with quiet_moviepilot_imports():
            sys.path.insert(0, '/app')
            from app.db.models.site import Site
            sites = Site.list()
        active_sites = [s for s in sites if getattr(s, 'is_active', False)]
        add('sites', isinstance(sites, list), f'count={len(sites)} active={len(active_sites)}')
        add('sites_configured', len(sites) > 0, f'count={len(sites)}')
    except Exception as e:
        add('sites', False, repr(e))

    try:
        with quiet_moviepilot_imports():
            from app.db.systemconfig_oper import SystemConfigOper
            from app.schemas.types import SystemConfigKey
            downloaders = SystemConfigOper().get(SystemConfigKey.Downloaders) or []
        enabled = [d for d in downloaders if d.get('enabled')] if isinstance(downloaders, list) else []
        add('downloaders', isinstance(downloaders, list), f'count={len(downloaders)} enabled={len(enabled)}')
    except Exception as e:
        add('downloaders', False, repr(e))

    try:
        with quiet_moviepilot_imports():
            from app.scheduler import Scheduler
            sched = Scheduler()
            jobs = getattr(sched, '_jobs', {})
            scheduler_obj = getattr(sched, '_scheduler', None)
        add('scheduler', scheduler_obj is not None and isinstance(jobs, dict), f'jobs={len(jobs)}')
    except Exception as e:
        add('scheduler', False, repr(e))

    failures = [c for c in checks if not c['ok']]
    print('SUMMARY total=%d pass=%d fail=%d' % (len(checks), len(checks)-len(failures), len(failures)))
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
