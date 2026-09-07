import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

CLI = Path(__file__).resolve().parents[1] / 'idcli.py'


class PortableReleaseTests(unittest.TestCase):
    def invoke(self, root, *args):
        return subprocess.run([sys.executable, str(CLI), *args], cwd=root, text=True, capture_output=True)

    def test_empty_profile_validation_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertNotEqual(self.invoke(Path(tmp), "validate", "--owner-id", "demo").returncode, 0)

    def test_owner_only_init_and_minimal_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for args in [('init',), ('refresh-soul',), ('export-interop',), ('export-compact',), ('validate-compact',)]:
                r = self.invoke(root, *args, '--owner-id', 'demo')
                self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            profile = (root / 'profiles/demo/profile.minimal.md').read_text()
            self.assertIn('owner_alias: "demo"', profile)
            self.assertIn('trust_level: "provisional"', profile)
            self.assertFalse((root / 'profiles/demo/profile.core.md').exists())

    def test_init_preflights_all_files_and_rejects_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            owner = root / 'profiles/demo'
            owner.mkdir(parents=True)
            (owner / 'handshake.md').write_text('Keep me')
            r = self.invoke(root, 'init', '--owner-id', 'demo')
            self.assertNotEqual(r.returncode, 0)
            self.assertFalse((owner / 'profile.minimal.md').exists())
            self.assertEqual((owner / 'handshake.md').read_text(), 'Keep me')
            r = self.invoke(root, 'init', '--owner-id', '../outside')
            self.assertNotEqual(r.returncode, 0)
            self.assertFalse((root / 'outside').exists())

    def test_missing_and_malformed_policy_do_not_export(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for command in ['init', 'export-interop']:
                r = self.invoke(root, command, '--owner-id', 'demo')
                self.assertEqual(r.returncode, 0, r.stderr)
            owner = root / 'profiles/demo'
            policy = owner / 'privacy-policy.v1.json'
            policy.unlink()
            for command in ['export-compact', 'export-mcp']:
                self.assertNotEqual(self.invoke(root, command, '--owner-id', 'demo').returncode, 0)
            policy.write_text('{}')
            self.assertNotEqual(self.invoke(root, 'export-compact', '--owner-id', 'demo').returncode, 0)
            self.assertFalse((owner / 'context.compact.json').exists())

    def test_set_hook_respects_owner_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for command in ['init', 'refresh-soul']:
                self.assertEqual(self.invoke(root, command, '--owner-id', 'demo').returncode, 0)
            (root / 'docs/ai').mkdir(parents=True)
            (root / 'docs/ai/id-context.json').write_text(json.dumps({'usage': {'preferred_human_bootstrap': ['/etc/passwd']}}))
            r = self.invoke(root, 'integration-hook', 'pre_task', '--owner-id', 'demo', '--target', 'set')
            self.assertNotEqual(r.returncode, 0)
            self.assertNotIn('primary_human_bootstrap=', r.stdout)
