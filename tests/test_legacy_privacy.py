import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from privacy_policy import normalize_policy, access_allowed


def legacy():
    return {'policy_version': '1.0.0', 'owner_id': 'demo',
            'always_share': ['profiles.core.quality_bar'],
            'local_only': ['profiles.core.communication'],
            'task_class_scoped': {'profiles.core.tool_notes': ['coding']}}


class LegacyPrivacyTests(unittest.TestCase):
    def test_normalization_preserves_restrictions_and_source(self):
        source = legacy()
        before = copy.deepcopy(source)
        policy = normalize_policy(source, 'demo')
        self.assertEqual(source, before)
        self.assertTrue(access_allowed(policy, 'profiles.core.quality_bar', None))
        self.assertFalse(access_allowed(policy, 'profiles.core.communication', 'coding'))
        self.assertFalse(access_allowed(policy, 'unlisted', 'coding'))
        self.assertFalse(access_allowed(policy, 'profiles.core.tool_notes', None))
        self.assertFalse(access_allowed(policy, 'profiles.core.tool_notes', 'writing'))
        self.assertTrue(access_allowed(policy, 'profiles.core.tool_notes', 'coding'))

    def test_ambiguous_invalid_and_mismatched_policies_fail_closed(self):
        cases = [{}, [], {'rules': None}]
        for key, value in [('rules', []), ('always_share', 'bad'), ('owner_id', 'other'),
                           ('policy_version', '2.0.0'), ('task_class_scoped', {'field': []})]:
            policy = legacy(); policy[key] = value; cases.append(policy)
        conflict = legacy(); conflict['always_share'] += conflict['local_only']; cases.append(conflict)
        for policy in cases:
            with self.subTest(policy=policy), self.assertRaises(ValueError):
                normalize_policy(policy, 'demo')

    def test_legacy_exports_from_cli_keep_private_fields_and_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            def run(command, *args):
                result = subprocess.run([sys.executable, str(ROOT/'idcli.py'), command,
                                         '--owner-id', 'demo', *args], cwd=root, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            run('init'); run('export-interop')
            owner = root/'profiles/demo'
            path = owner/'interop.v1.json'
            doc = json.loads(path.read_text())
            doc['profiles']['core']['communication'] = ['PRIVATE_SENTINEL']
            path.write_text(json.dumps(doc))
            policy_path = owner/'privacy-policy.v1.json'
            policy_path.write_text(json.dumps(legacy()))
            before = policy_path.read_bytes()
            run('validate-privacy')
            for command, output in [('export-compact', 'context.compact.json'), ('export-mcp', 'mcp.context.resource.json')]:
                run(command)
                self.assertNotIn('PRIVATE_SENTINEL', (owner/output).read_text())
            self.assertEqual(policy_path.read_bytes(), before)
