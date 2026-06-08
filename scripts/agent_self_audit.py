#!/opt/venv/bin/python
"""Deterministic self-audit for MoviePilot agent directory governance."""
from pathlib import Path
import os
import subprocess
import sys
from collections import defaultdict

sys.dont_write_bytecode = True
ROOT = Path('/config/agent')
CHECKS = []
SUMMARY_MODE = '--summary' in sys.argv
CATEGORIES = defaultdict(lambda: [0, 0])


def category_for(name: str) -> str:
    if name.startswith('dir_') or name in {'root_files_allowed', 'docs_root_only_history_entries', 'memory_only_md_files'} or 'pycache' in name or 'temp_backup' in name:
        return 'directory'
    if name.startswith('job_') or name.startswith('archive_job') or name == 'jobs_only_job_md_no_pycache':
        return 'jobs'
    if 'heartbeat' in name:
        return 'heartbeat'
    if 'health_check' in name:
        return 'health'
    if 'skill' in name or 'superpowers' in name:
        return 'skills'
    if name.startswith('scripts_') or name.endswith('_runs') or name.startswith('py_compile') or name.startswith('cleanup_script'):
        return 'scripts'
    if any(key in name for key in ('memory', 'runtime_rules', 'safety', 'troubleshooting', 'observability', 'governance', 'notification', 'acceptance', 'persona', 'moviepilot_', 'current_persona', 'active_persona', 'runtime_cache', 'docs_', 'no_current_ref')):
        return 'memory'
    return 'runtime'


def run(cmd: str):
    env = os.environ.copy()
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    return subprocess.run(cmd, shell=True, text=True, capture_output=True, env=env)


def add(name: str, ok: bool, detail: str = ''):
    ok = bool(ok)
    CHECKS.append((name, ok, detail))
    cat = category_for(name)
    CATEGORIES[cat][0] += 1
    CATEGORIES[cat][1] += 0 if ok else 1
    if not SUMMARY_MODE:
        print(('PASS' if ok else 'FAIL') + f' | {name}' + (f' | {detail}' if detail else ''))


def main() -> int:
    for dirname in ['activity', 'docs', 'jobs', 'memory', 'runtime', 'skills', 'scripts']:
        add(f'dir_exists:{dirname}', (ROOT / dirname).is_dir())

    root_files = {p.name for p in ROOT.iterdir() if p.is_file()}
    add('root_files_allowed', root_files <= {'CURRENT_PERSONA.md'}, ','.join(sorted(root_files)))

    docs_items = {p.name for p in (ROOT / 'docs').iterdir()}
    add('docs_root_only_history_entries', docs_items <= {'README.md', 'archive', 'job-archive'}, ','.join(sorted(docs_items)))

    job_bad = []
    for item in (ROOT / 'jobs').rglob('*'):
        if item.is_file() and item.name != 'JOB.md':
            job_bad.append(str(item))
        if item.is_dir() and item.name == '__pycache__':
            job_bad.append(str(item))
    add('jobs_only_job_md_no_pycache', not job_bad, '\n'.join(job_bad))

    # Clean Python bytecode caches before asserting directory hygiene.
    run("python - <<'PYCLEAN'\nfrom pathlib import Path\nimport shutil\nfor p in Path('/config/agent').rglob('__pycache__'):\n    if p.is_dir(): shutil.rmtree(p)\nPYCLEAN")
    script_bad = [str(p) for p in (ROOT / 'scripts').rglob('__pycache__') if p.is_dir()]
    add('scripts_no_pycache', not script_bad, '\n'.join(script_bad))
    add('scripts_cleanup_exists', (ROOT / 'scripts/cleanup_docs_archive.py').is_file())
    add('scripts_health_check_exists', (ROOT / 'scripts/moviepilot_health_check.py').is_file())
    add('scripts_router_check_exists', (ROOT / 'scripts/agent_skill_router_check.py').is_file())

    mem_bad = [str(p) for p in (ROOT / 'memory').iterdir() if not (p.is_file() and p.suffix == '.md')]
    add('memory_only_md_files', not mem_bad, '\n'.join(mem_bad))
    add('directory_governance_exists', (ROOT / 'memory/DIRECTORY_GOVERNANCE.md').is_file())
    add('agent_runtime_rules_exists', (ROOT / 'memory/AGENT_RUNTIME_RULES.md').is_file())
    add('old_split_agent_rules_absent', not any((ROOT / 'memory' / f).exists() for f in ['AGENT_PROFILE.md', 'AGENT_WORKFLOW.md', 'AGENT_HOOKS.md']))
    framework_files = {
        'safety_boundaries_exists': 'SAFETY_BOUNDARIES.md',
        'troubleshooting_exists': 'MOVIEPILOT_TROUBLESHOOTING.md',
        'observability_exists': 'OBSERVABILITY.md',
        'job_governance_exists': 'JOB_GOVERNANCE.md',
        'notification_workflow_exists': 'NOTIFICATION_WORKFLOW.md',
        'skill_governance_exists': 'SKILL_GOVERNANCE.md',
        'acceptance_criteria_exists': 'ACCEPTANCE_CRITERIA.md',
    }
    for check_name, filename in framework_files.items():
        add(check_name, (ROOT / 'memory' / filename).is_file())
    def memory_text(filename):
        path = ROOT / 'memory' / filename
        return path.read_text(encoding='utf-8') if path.is_file() else ''
    add('safety_has_secret_rule', '不保存密码、Token、Cookie、API Key' in memory_text('SAFETY_BOUNDARIES.md'))
    add('troubleshooting_has_moviepilot_matrix', '搜不到资源' in memory_text('MOVIEPILOT_TROUBLESHOOTING.md') and '转移失败' in memory_text('MOVIEPILOT_TROUBLESHOOTING.md'))
    add('observability_has_system_tools', 'query_schedulers' in memory_text('OBSERVABILITY.md') and 'query_sites' in memory_text('OBSERVABILITY.md'))
    add('job_governance_requires_job_md_only', 'Job 目录只放 `JOB.md`' in memory_text('JOB_GOVERNANCE.md'))
    add('notification_has_heartbeat_real_data_rule', 'AI 不生成、猜测或补全心跳业务数据' in memory_text('NOTIFICATION_WORKFLOW.md'))
    add('skill_governance_has_name_match_rule', 'frontmatter `name` 必须等于目录名' in memory_text('SKILL_GOVERNANCE.md'))
    add('acceptance_requires_evidence', '必须有实际工具结果、命令输出或状态查询证据' in memory_text('ACCEPTANCE_CRITERIA.md'))
    runtime_rules = memory_text('AGENT_RUNTIME_RULES.md')
    add('runtime_rules_merge_profile_workflow_hooks', 'Agent 负责 MoviePilot' in runtime_rules and '标准执行顺序' in runtime_rules and '执行钩子' in runtime_rules and 'Persona 是表达层，不是身份层' in runtime_rules)
    superpowers_workflow = ROOT / 'memory/SUPERPOWERS_WORKFLOW.md'
    add('superpowers_workflow_exists', superpowers_workflow.is_file())
    if superpowers_workflow.is_file():
        workflow_text = superpowers_workflow.read_text(encoding='utf-8')
        add('superpowers_is_workflow_not_identity', '工作流纪律层' in workflow_text and '不是身份层' in workflow_text and 'MoviePilot Agent' in workflow_text)
        add('superpowers_does_not_replace_moviepilot', 'Superpowers 管流程' in workflow_text and 'MoviePilot skills 管领域执行' in workflow_text)
        add('moviepilot_skill_overlap_arbitration', 'MoviePilot 业务技能重叠裁决' in workflow_text and 'moviepilot-direct-routes' in workflow_text and 'resource-search' in workflow_text and 'moviepilot-api' in workflow_text)
    add('using_superpowers_skill_exists', (ROOT / 'skills/using-superpowers/SKILL.md').is_file())
    persona_fusion = ROOT / 'memory/PERSONA_FUSION.md'
    add('persona_fusion_exists', persona_fusion.is_file())
    if persona_fusion.is_file():
        persona_text = persona_fusion.read_text(encoding='utf-8')
        add('persona_is_expression_not_identity', 'Persona 是表达层，不是身份层' in persona_text and 'MoviePilot Agent core 是身份层' in persona_text)
        add('persona_does_not_override_workflow', '不得覆盖 MoviePilot Agent 身份' in persona_text and '不得跳过 Superpowers 工作流纪律' in persona_text)
    moviepilot_workflow = ROOT / 'memory/MOVIEPILOT_AGENT_WORKFLOW.md'
    add('moviepilot_workflow_exists', moviepilot_workflow.is_file())
    if moviepilot_workflow.is_file():
        moviepilot_text = moviepilot_workflow.read_text(encoding='utf-8')
        add('moviepilot_identity_preserved', 'MoviePilot Agent 的核心身份是家庭媒体管理助手' in moviepilot_text and 'Superpowers 负责工作流纪律，不覆盖 MoviePilot Agent core' in moviepilot_text)
        add('moviepilot_business_chain_exists', '站点与认证' in moviepilot_text and '资源搜索' in moviepilot_text and '转移与入库规则' in moviepilot_text)
        add('moviepilot_routing_priority_exists', 'moviepilot-direct-routes' in moviepilot_text and 'resource-search' in moviepilot_text and 'moviepilot-cli' in moviepilot_text)
        add('moviepilot_confirmation_rule_exists', '除非用户明确给出链接并要求下载，否则下载前先展示候选资源并确认' in moviepilot_text)
        add('moviepilot_tv_season_rule_exists', 'TV 订阅不传 season 时默认仅第 1 季' in moviepilot_text)
        add('moviepilot_recognition_separation_exists', '`search_media` 用于数据库查找' in moviepilot_text and '`recognize_media` 用于解析文件名、种子名、路径' in moviepilot_text)
        add('moviepilot_transfer_failure_rule_exists', '转移失败重试优先使用 `transfer-failed-retry`' in moviepilot_text)
        add('persona_switch_uses_tools', 'query_personas' in persona_text and 'switch_persona' in persona_text)
    active_persona = ROOT / 'runtime/personas/clarisia/PERSONA.md'
    current_persona = ROOT / 'CURRENT_PERSONA.md'
    add('current_persona_entry_exists', current_persona.is_file())
    add('active_persona_file_exists', active_persona.is_file())
    if superpowers_workflow.is_file():
        workflow_text = superpowers_workflow.read_text(encoding='utf-8')
        add('superpowers_explicit_trigger_exceptions', '显式触发例外' in workflow_text and 'chinese-code-review' in workflow_text and '不得抢占 MoviePilot 主流程' in workflow_text)

    bad_skill_names = []
    import re
    for skill_md in sorted((ROOT / 'skills').glob('*/SKILL.md')):
        text = skill_md.read_text(encoding='utf-8', errors='ignore')
        match = re.search(r'^name:\s*(.+)$', text, re.M)
        name = match.group(1).strip().strip('"') if match else ''
        if name != skill_md.parent.name:
            bad_skill_names.append(f'{skill_md.parent.name}=>{name}')
    add('skill_name_matches_directory', not bad_skill_names, '\n'.join(bad_skill_names))

    add('runtime_cache_subscriber_exists', (ROOT / 'runtime/cache/subscribereminder_last_push.json').is_file())
    add('docs_subscriber_absent', not (ROOT / 'docs/subscribereminder_last_push.json').exists())
    add('docs_cleanup_script_absent', not (ROOT / 'docs/cleanup_docs_archive.py').exists())

    scan_targets = '/config/heartbeat_report.py /config/agent/jobs /config/agent/memory /config/agent/runtime /config/agent/skills'
    for pattern in [
        '/config/agent/docs/subscribereminder_last_push',
        '/config/agent/docs/cleanup_docs_archive',
        '/config/agent/jobs/archive-auto-destroy/cleanup_docs_archive',
    ]:
        result = run(f"rg -n {pattern!r} {scan_targets} -S")
        add(f'no_current_ref:{pattern}', result.returncode != 0, result.stdout.strip())

    heartbeat = Path('/config/heartbeat_report.py').read_text(encoding='utf-8')
    add('heartbeat_uses_runtime_cache', '/config/agent/runtime/cache/subscribereminder_last_push.json' in heartbeat)

    archive_job_path = ROOT / 'jobs/archive-auto-destroy/JOB.md'
    if archive_job_path.exists():
        archive_job = archive_job_path.read_text(encoding='utf-8')
        add('archive_job_uses_scripts_path', '/config/agent/scripts/cleanup_docs_archive.py' in archive_job)
        add('archive_job_no_old_script_path', '/config/agent/jobs/archive-auto-destroy/cleanup_docs_archive.py' not in archive_job)
    else:
        add('archive_job_absent_after_archive', True)

    result = run('python -m py_compile /config/heartbeat_report.py /config/agent/scripts/cleanup_docs_archive.py /config/agent/scripts/agent_self_audit.py')
    add('py_compile_core_scripts_no_bytecode', result.returncode == 0, result.stderr.strip())

    result = run('python /config/agent/scripts/cleanup_docs_archive.py')
    add('cleanup_script_runs', result.returncode == 0 and 'OK deleted_files=' in result.stdout, (result.stdout + result.stderr).strip()[-1000:])
    result = run('python /config/agent/scripts/agent_skill_router_check.py')
    add('skill_router_check_runs', result.returncode == 0 and 'fail=0' in result.stdout, (result.stdout + result.stderr).strip()[-1000:])
    result = run('python /config/agent/scripts/moviepilot_health_check.py')
    health_output = (result.stdout + result.stderr).strip()
    add('moviepilot_health_check_runs', result.returncode == 0 and 'MOVIEPILOT_HEALTH_CHECK' in result.stdout and 'fail=0' in result.stdout, health_output[-1200:])
    add('moviepilot_health_check_quiet_output', 'PostgreSQL database connected' not in result.stdout and 'module.py - Moudle Loaded' not in result.stdout and 'DEBUG:' not in result.stdout, result.stdout[-1200:])

    render_code = r'''
import contextlib
import io
import sys
sys.dont_write_bytecode = True
sys.path.insert(0, '/config')
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    import heartbeat_report
    msg = heartbeat_report.build_message()
order = ['少爷，', '🕒 时间：', '🤖 MoviePilot：', '📡 站点状态：', '📈 站点增量：', '⬇️ 下载器：', '📦 入库整理：', '📺 订阅追新：', '💾 存储空间：']
pos = -1
for item in order:
    cur = msg.find(item)
    assert cur > pos, (item, cur, pos)
    pos = cur
assert ('✅ 今日摘要：' in msg) ^ ('⚠️ 今日提醒：' in msg)
assert heartbeat_report.SUB_FILE.as_posix() == '/config/agent/runtime/cache/subscribereminder_last_push.json'
assert '可转移/做种' not in msg
assert '状态：在线' not in msg
assert '速度：↓ 0 B/s' not in msg
assert '\ufffd' not in msg
import os
print('RENDER_OK')
sys.stdout.flush()
sys.stderr.flush()
os._exit(0)
'''
    result = run("python - <<'PY'\n" + render_code + "\nPY")
    render_output = (result.stdout + result.stderr).strip()
    add('heartbeat_render_assertions', result.returncode == 0 and result.stdout.strip() == 'RENDER_OK', render_output[-2000:])
    add('heartbeat_render_quiet_output', result.stdout.strip() == 'RENDER_OK' and not result.stderr.strip(), render_output[-2000:])

    for jobmd in sorted((ROOT / 'jobs').glob('*/JOB.md')):
        text = jobmd.read_text(encoding='utf-8')
        add(f'job_frontmatter:{jobmd.parent.name}', text.startswith('---') and 'schedule:' in text and 'status:' in text)

    result = run("find /config/agent -maxdepth 5 -type f \\( -name '*.tmp' -o -name '*.bak' -o -name '*.old' -o -name '*~' -o -name '*.log' \\) -print | sort")
    add('no_temp_backup_log_files', not result.stdout.strip(), result.stdout.strip())

    run("python - <<'PYCLEAN'\nfrom pathlib import Path\nimport shutil\nfor p in Path('/config/agent').rglob('__pycache__'):\n    if p.is_dir(): shutil.rmtree(p)\nPYCLEAN")
    result = run("find /config/agent -maxdepth 5 -type d -name '__pycache__' -print | sort")
    add('no_pycache_under_agent', not result.stdout.strip(), result.stdout.strip())

    failures = [item for item in CHECKS if not item[1]]
    if SUMMARY_MODE:
        persona = 'unknown'
        persona_file = ROOT / 'runtime/CURRENT_PERSONA.md'
        if not persona_file.is_file():
            persona_file = ROOT / 'CURRENT_PERSONA.md'
        if persona_file.is_file():
            for line in persona_file.read_text(encoding='utf-8', errors='ignore').splitlines():
                if line.lower().startswith('persona:') or line.lower().startswith('active persona:'):
                    persona = line.split(':', 1)[1].strip().strip('`') or persona
                    break
            if persona == 'unknown':
                text = persona_file.read_text(encoding='utf-8', errors='ignore')
                if 'clarisia' in text:
                    persona = 'clarisia'
        memory_files = len(list((ROOT / 'memory').glob('*.md')))
        job_files = len(list((ROOT / 'jobs').glob('*/JOB.md')))
        skill_files = len(list((ROOT / 'skills').glob('*/SKILL.md')))
        print('AGENT_SELF_AUDIT')
        print('mode: summary')
        print(f'persona: {persona}')
        print(f'memory_files: {memory_files}')
        print(f'jobs: {job_files}')
        print(f'skills: {skill_files}')
        for cat in ['directory', 'memory', 'skills', 'scripts', 'health', 'heartbeat', 'jobs', 'runtime']:
            total, failed = CATEGORIES.get(cat, [0, 0])
            if total:
                print(f'{cat}: ' + ('PASS' if failed == 0 else 'FAIL') + f' ({total - failed}/{total})')
    print(f'\nSUMMARY total={len(CHECKS)} pass={len(CHECKS) - len(failures)} fail={len(failures)}')
    if failures:
        for name, _, detail in failures:
            print(f'FAILED {name}: {detail[:500]}')
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
