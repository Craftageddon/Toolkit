"""Regression checks for release archives and non-destructive source staging."""
import hashlib
import importlib.util
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('hardened_packer', ROOT / 'scripts/build_release_zip.py')
packer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packer)
POWERSHELL = os.environ.get('TOOLKIT_POWERSHELL') or shutil.which('pwsh') or shutil.which('powershell')


class ReleaseRegressionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.root = self.base / 'source'
        self.root.mkdir()
        (self.root / 'a.txt').write_bytes(b'reviewed bytes\n')
        self.target = self.base / 'release.zip'

    def test_repository_archive_and_publisher_match_reviewed_manifest(self):
        reviewed = {name: digest for digest, name in
                    (line.split('  ', 1) for line in (ROOT/'SHA256SUMS.txt').read_text().splitlines())}
        publisher = (ROOT/'scripts/publish_to_github.ps1').read_text()
        listed = re.findall(r"'([^']+)'", publisher.split('$allowedFiles = @(', 1)[1].split('\n)', 1)[0])
        self.assertEqual(len(listed), len(set(listed)))
        self.assertEqual(set(listed), (set(reviewed) | {'SHA256SUMS.txt'}) - {'LICENSE'})
        output = self.base/'toolkit.zip'
        self.assertEqual(packer.build(ROOT, output), len(reviewed))
        with zipfile.ZipFile(output) as z:
            self.assertEqual(len(z.namelist()), len(reviewed) + 1)
            self.assertEqual(len(set(z.namelist())), len(z.namelist()))
            for name, digest in reviewed.items():
                self.assertEqual(hashlib.sha256(z.read(f'{ROOT.name}/{name}')).hexdigest(), digest)

    def manifest(self, lines=None):
        text = lines if lines is not None else hashlib.sha256((self.root/'a.txt').read_bytes()).hexdigest() + '  a.txt\n'
        (self.root/'SHA256SUMS.txt').write_text(text, encoding='utf-8', newline='\n')

    def test_existing_manifest_is_replaced_once_and_round_trip_matches(self):
        self.manifest()
        (self.root/'unreviewed.txt').write_text('must not ship')
        packer.build(self.root, self.target)
        with zipfile.ZipFile(self.target) as z:
            self.assertIsNone(z.testzip())
            self.assertEqual(z.namelist().count('source/SHA256SUMS.txt'), 1)
            self.assertEqual(set(z.namelist()), {'source/a.txt', 'source/SHA256SUMS.txt'})
            self.assertEqual(z.read('source/a.txt'), (self.root/'a.txt').read_bytes())
            self.assertEqual(z.read('source/SHA256SUMS.txt'), (self.root/'SHA256SUMS.txt').read_bytes())

    def test_stale_manifest_fails_before_creating_outputs(self):
        self.manifest()
        (self.root/'a.txt').write_text('changed after review')
        with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
            packer.build(self.root, self.target)
        self.assertFalse(self.target.exists())
        self.assertFalse(self.target.with_suffix('.zip.sha256').exists())

    def test_unsafe_duplicate_and_secret_manifest_paths_rejected(self):
        for name in ('../outside.txt', '/absolute.txt', 'C:/file.txt', 'a/../a.txt', 'a\\b.txt', '.env', 'private.key', 'SHA256SUMS.txt'):
            with self.subTest(name=name):
                self.manifest('0'*64 + '  ' + name + '\n')
                with self.assertRaises(ValueError):
                    packer.build(self.root, self.target)
                self.assertFalse(self.target.exists())
        self.manifest('0'*64 + '  a.txt\n' + '0'*64 + '  A.txt\n')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            packer.build(self.root, self.target)

    def test_generated_and_conventional_private_files_excluded_without_manifest(self):
        names = ['.env', '.env.local', 'private.pem', 'private.key', 'old.zip', 'old.zip.sha256',
                 '.venv/private.txt', 'verification/state.json', '.git/config', '__pycache__/cache.pyc', 'dist/old.txt']
        for name in names:
            file = self.root/name
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text('not source')
        packer.build(self.root, self.target)
        with zipfile.ZipFile(self.target) as z:
            self.assertEqual(set(z.namelist()), {'source/a.txt', 'source/SHA256SUMS.txt'})

    def test_existing_output_and_sidecar_are_preserved(self):
        self.target.write_bytes(b'KEEP ZIP')
        with self.assertRaises(ValueError):
            packer.build(self.root, self.target)
        self.assertEqual(self.target.read_bytes(), b'KEEP ZIP')
        self.target.unlink()
        sidecar = self.target.with_suffix('.zip.sha256')
        sidecar.write_bytes(b'KEEP CHECKSUM')
        with self.assertRaises(ValueError):
            packer.build(self.root, self.target)
        self.assertEqual(sidecar.read_bytes(), b'KEEP CHECKSUM')
        self.assertFalse(self.target.exists())

    def test_archive_write_failure_removes_partial_output(self):
        with mock.patch.object(zipfile.ZipFile, 'writestr', side_effect=OSError('simulated disk failure')):
            with self.assertRaises(OSError):
                packer.build(self.root, self.target)
        self.assertFalse(self.target.exists())
        self.assertFalse(self.target.with_suffix('.zip.sha256').exists())

    def test_manifest_symlink_parent_cannot_include_external_data(self):
        outside = self.base/'outside'
        outside.mkdir()
        (outside/'private.txt').write_text('external')
        try:
            (self.root/'link').symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest('Host does not permit unprivileged symlink creation')
        self.manifest(hashlib.sha256(b'external').hexdigest() + '  link/private.txt\n')
        with self.assertRaisesRegex(ValueError, 'Symlink'):
            packer.build(self.root, self.target)
        self.assertFalse(self.target.exists())


@unittest.skipUnless(POWERSHELL, 'PowerShell required for actual staging-helper execution')
class StagingRegressionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.source = self.base/'source'
        self.dest = self.base/'destination'
        self.source.mkdir()
        self.dest.mkdir()
        (self.source/'a.txt').write_bytes(b'A')
        (self.source/'nested').mkdir()
        (self.source/'nested/b.txt').write_bytes(b'B')

    def stage(self, paths=('a.txt', 'nested/b.txt'), *, ok=True, preview=False, error=None):
        def quote(value):
            return "'" + str(value).replace("'", "''") + "'"
        command = (f"& {quote(ROOT/'scripts/stage_toolkit_source.ps1')} -SourceRoot {quote(self.source)} "
                   f"-DestinationRoot {quote(self.dest)} -Paths @({','.join(quote(p) for p in paths)})"
                   + (' -WhatIf' if preview else ''))
        proc = subprocess.run([POWERSHELL, '-NoProfile', '-NonInteractive', '-Command', command], capture_output=True, text=True)
        if ok:
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        else:
            self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn(error, proc.stdout + proc.stderr)
        return proc

    def test_new_files_copy_and_identical_existing_file_is_preserved(self):
        existing = self.dest/'a.txt'
        existing.write_bytes(b'A')
        timestamp = existing.stat().st_mtime_ns
        self.stage()
        self.assertEqual(existing.read_bytes(), b'A')
        self.assertEqual(existing.stat().st_mtime_ns, timestamp)
        self.assertEqual((self.dest/'nested/b.txt').read_bytes(), b'B')

    def test_conflict_in_later_path_prevents_any_copy(self):
        (self.dest/'nested').mkdir()
        (self.dest/'nested/b.txt').write_bytes(b'KEEP EXISTING')
        self.stage(ok=False, error='Existing repository file differs')
        self.assertFalse((self.dest/'a.txt').exists())
        self.assertEqual((self.dest/'nested/b.txt').read_bytes(), b'KEEP EXISTING')

    def test_missing_source_prevents_any_copy(self):
        self.stage(('a.txt', 'missing.txt'), ok=False, error='Missing source')
        self.assertEqual(list(self.dest.iterdir()), [])

    def test_path_escape_and_duplicate_paths_are_rejected(self):
        for paths in (('a.txt', '../outside.txt'), ('a.txt', 'a.txt'), ('/a.txt',), ('C:/a.txt',)):
            with self.subTest(paths=paths):
                self.stage(paths, ok=False, error='Unsafe or duplicate source path')
                self.assertEqual(list(self.dest.iterdir()), [])

    def test_preview_creates_no_files_or_directories(self):
        self.stage(preview=True)
        self.assertEqual(list(self.dest.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
