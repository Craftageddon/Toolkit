"""Installed-skill behavior in disposable directories, never a real profile."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/craftageddon-release-qa'
POWERSHELL = os.environ.get('TOOLKIT_POWERSHELL') or shutil.which('pwsh') or shutil.which('powershell')


class StandaloneSkillTests(unittest.TestCase):
    def test_bundled_helper_matches_canonical_script(self):
        # The top-level CLI remains supported; its installed copy must not drift.
        self.assertEqual((SKILL/'scripts/triple_verify.py').read_bytes(),
                         (ROOT/'scripts/triple_verify.py').read_bytes())

    def test_copied_skill_runs_complete_tracker_from_unrelated_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp).resolve()
            installed = base/'installed skill'
            shutil.copytree(SKILL, installed)
            project = base/'separate project'
            project.mkdir()
            (project/'payload.txt').write_text('Synthetic integration-test artifact.\n')
            unrelated = base/'unrelated cwd'
            unrelated.mkdir()
            helper = installed/'scripts/triple_verify.py'

            def run(*args, ok=True):
                # -I proves the helper needs no repository/PYTHONPATH imports.
                p = subprocess.run([sys.executable, '-I', str(helper), *args,
                                    '--root', str(project)], cwd=unrelated,
                                   capture_output=True, text=True)
                self.assertEqual(p.returncode == 0, ok, p.stdout+p.stderr)
                return p

            run('init', '--project', 'Synthetic installed-skill contract', '--artifact', 'payload.txt')
            status = run('status')
            self.assertEqual(status.stdout.count('PENDING'), 3)
            run('finalize', ok=False)
            self.assertFalse((project/'verification/release.json').exists())
            evidence = project/'verification/evidence'
            evidence.mkdir(exist_ok=True, parents=True)
            for number, method in enumerate(('fixture-requirements', 'fixture-integrity', 'fixture-round-trip'), 1):
                (evidence/f'v{number}.txt').write_text(
                    f'CHECK: V{number}\nRESULT: PASS\n'
                    'Synthetic unit-test evidence only; no real product, publication or fit approval.\n')
                args = ['record', '--check', str(number), '--method', method,
                        '--reviewer', 'test fixture', '--evidence', f'verification/evidence/v{number}.txt']
                if number == 3:
                    args += ['--independence', 'Synthetic test uses a distinct final round-trip method.']
                run(*args)
            run('finalize')
            self.assertTrue((project/'verification/release.json').is_file())
            (project/'payload.txt').write_text('Modified after synthetic verification.\n')
            run('status', ok=False)
            run('resnapshot')
            self.assertEqual(run('status').stdout.count('PENDING'), 3)
            self.assertFalse((installed/'verification').exists())
            self.assertFalse((unrelated/'verification').exists())


@unittest.skipUnless(POWERSHELL, 'PowerShell required for disposable installer integration')
class SkillInstallerTests(unittest.TestCase):
    def install(self, dest, preview=False):
        p = subprocess.run([POWERSHELL, '-NoProfile', '-NonInteractive', '-File',
                            str(ROOT/'scripts/install_codex_skills.ps1'),
                            '-Destination', str(dest)] + (['-WhatIf'] if preview else []),
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout+p.stderr)
        return p

    def test_preview_does_not_create_destination(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)/'not a real profile'/'skills'
            self.install(dest, preview=True)
            self.assertFalse(dest.exists())

    def test_installer_copies_helper_and_preserves_existing_skill(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)/'not a real profile'/'skills'
            self.install(dest)
            self.assertEqual(len(list(dest.glob('*/SKILL.md'))), 6)
            target = dest/'craftageddon-release-qa'
            self.assertEqual((target/'scripts/triple_verify.py').read_bytes(),
                             (ROOT/'scripts/triple_verify.py').read_bytes())
            entry = target/'SKILL.md'
            entry.write_text('Owner customization: must survive installer rerun.\n')
            before = entry.stat().st_mtime_ns
            self.install(dest)
            self.assertEqual(entry.read_text(), 'Owner customization: must survive installer rerun.\n')
            self.assertEqual(entry.stat().st_mtime_ns, before)


if __name__ == '__main__':
    unittest.main()
