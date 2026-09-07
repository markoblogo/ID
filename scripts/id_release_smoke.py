"""Installed-package demos using synthetic profiles only."""
import argparse
from importlib.metadata import version
import hashlib
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    versions = {name: version(name) for name in ("id-protocol", "agentsgen", "abvx-set")}
    assert versions == {"id-protocol": "0.5.0", "agentsgen": "0.5.0", "abvx-set": "0.3.1"}, versions
    rows = []
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        def run(*command, expected=0, env=None):
            r = subprocess.run(command, cwd=root, env=env, capture_output=True, text=True)
            if r.returncode != expected:
                raise SystemExit(f'{command}: {r.returncode}\n{r.stdout}\n{r.stderr}')
            return r.stdout
        start = time.perf_counter()
        run('idctl', 'init', '--owner-id', 'demo')
        owner = root / 'profiles/demo'
        profile = owner / 'profile.minimal.md'
        profile.write_text(profile.read_text().replace('- Preferred language(s):', '- Preferred language(s): SYNTHETIC_PRIVATE_SENTINEL'))
        original_hash = hashlib.sha256(profile.read_bytes()).hexdigest()
        for command in ['refresh-soul', 'validate', 'export-interop', 'export-compact', 'validate-compact', 'export-mcp', 'validate-mcp']:
            run('idctl', command, '--owner-id', 'demo')
        rows.append({'demo': 'installed-minimal-profile', 'passed': True, 'seconds': round(time.perf_counter()-start, 3)})

        start = time.perf_counter()
        policy_path = owner / 'privacy-policy.v1.json'
        policy = json.loads(policy_path.read_text())
        for rule in policy['rules']:
            if rule['field_path'] == 'profiles.core.communication':
                rule['access'] = 'local_only'
        policy_path.write_text(json.dumps(policy))
        for command in ['export-compact', 'export-mcp']:
            run('idctl', command, '--owner-id', 'demo')
        for name in ['context.compact.json', 'mcp.context.resource.json']:
            assert 'SYNTHETIC_PRIVATE_SENTINEL' not in (owner/name).read_text()
        rows.append({'demo': 'policy-omission', 'passed': True, 'seconds': round(time.perf_counter()-start, 3)})

        start = time.perf_counter()
        run('agentsgen', 'init', '.', '--defaults', '--autodetect')
        run('agentsgen', 'pack', '.', '--autodetect')
        run('agentsgen', 'check', '.', '--pack-check', '--ci')
        run('idctl', 'install-set-hook')
        hook = run('bash', 'scripts/run_integration_hook.sh', 'pre_task', '--owner-id', 'demo', '--target', 'set')
        fields = dict(line.split('=', 1) for line in hook.splitlines() if '=' in line and not line.startswith('['))
        assert fields['primary_human_bootstrap'] == 'profiles/demo/soul.md'
        mapping = {'soul':'SET_ID_SOUL_PATH', 'profile_core':'SET_ID_PROFILE_CORE', 'handshake':'SET_ID_HANDSHAKE', 'primary_human_bootstrap':'SET_ID_PRIMARY_BOOTSTRAP', 'preferred_human_bootstrap':'SET_ID_PREFERRED_BOOTSTRAP', 'integration_guide':'SET_ID_INTEGRATION_GUIDE'}
        env = dict(os.environ, SET_RESOLVED_ID_OWNER_ID='demo', SET_RESOLVED_ID_TARGET='set', INPUT_PATH=str(root))
        env.update({value: fields[key] for key, value in mapping.items()})
        import sys
        run(sys.executable, '-m', 'scripts.export_id_bootstrap', env=env)
        packet = json.loads((root/'docs/ai/id-bootstrap.json').read_text())
        assert packet['id']['primary_human_bootstrap'] == 'profiles/demo/soul.md'
        for path in packet['id']['preferred_human_bootstrap']:
            assert (root/path).is_file()
        config = {'version':1,'repo':'example/demo','presets':['repo-docs'],'tools':{'agentsgen':{'init':True,'pack':True,'check':True},'id':{'enabled':True,'owner_id':'demo','target':'set','pre_task':True}}}
        (root/'.set.json').write_text(json.dumps(config))
        plan = json.loads(run('set-plan-config-apply','--config','.set.json','--format','json','--export-dir','review'))
        assert plan['dry_run'] is True
        assert not (root/'.github/workflows/set.yml').exists()
        assert hashlib.sha256(profile.read_bytes()).hexdigest() == original_hash
        rows.append({'demo':'agentsgen-0.5.0-set-0.3.1', 'passed':True,'source_profile_preserved':True,'seconds':round(time.perf_counter()-start,3)})
    report = {'version':1,'packages':versions,'measurement':'Local CLI wall time; synthetic data; not an AI quality benchmark','results':rows}
    output = json.dumps(report, indent=2)+'\n'
    if args.output:
        args.output.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
