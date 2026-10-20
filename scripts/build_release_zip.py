#!/usr/bin/env python3
"""Create a deterministic Craftageddon ZIP and internal SHA256SUMS.txt manifest.

The generated archive is *only* an offline release candidate. Passing archive
integrity does not certify plugins, hardware, CAD integration, or manufacturability.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile

EXCLUDE_DIRS = {'__pycache__', '.git', '.pytest_cache', '.venv', 'venv',
                'dist', 'build', 'verification', '.ssh', '.aws', '.codex'}
EXCLUDE_SUFFIXES = {'.pyc', '.pyo', '.tmp', '.zip', '.sha256', '.pem', '.key'}
ARCHIVE_TIME = (2026, 10, 20, 0, 0, 0)


def excluded(rel: PurePosixPath) -> bool:
    return (bool({part.lower() for part in rel.parts[:-1]} & EXCLUDE_DIRS)
            or rel.suffix.lower() in EXCLUDE_SUFFIXES
            or rel.name.lower() == '.env' or rel.name.lower().startswith('.env.'))


def source_files(root: Path) -> list[tuple[str, bytes]]:
    """Snapshot reviewed bytes; an existing checksum manifest is an allowlist."""
    manifest = root / 'SHA256SUMS.txt'
    listed = {}
    if manifest.is_symlink():
        raise ValueError('Symlink manifest not permitted')
    if manifest.exists():
        for line in manifest.read_text(encoding='utf-8').splitlines():
            match = re.fullmatch(r'([0-9a-fA-F]{64})  (.+)', line)
            if not match:
                raise ValueError('Invalid SHA256SUMS.txt entry')
            digest, name = match.groups()
            rel = PurePosixPath(name)
            if (rel.is_absolute() or '..' in rel.parts or '\\' in name or ':' in name
                    or rel.as_posix() != name or name.casefold() == 'sha256sums.txt'
                    or name.casefold() in {n.casefold() for n in listed} or excluded(rel)):
                raise ValueError(f'Unsafe, excluded, or duplicate manifest entry: {name}')
            listed[name] = digest.lower()
        names = sorted(listed)
    else:
        names = sorted(p.relative_to(root).as_posix() for p in root.rglob('*')
                       if p.is_file() and p.name.casefold() != 'sha256sums.txt'
                       and not excluded(PurePosixPath(p.relative_to(root).as_posix())))
    files = []
    for name in names:
        path = root / name
        cursor = root
        for part in PurePosixPath(name).parts:
            cursor = cursor / part
            if cursor.is_symlink():
                raise ValueError(f'Symlink not permitted: {name}')
        if not path.is_file() or not path.resolve().is_relative_to(root):
            raise ValueError(f'Missing or unsafe source: {name}')
        data = path.read_bytes()
        if name in listed and hashlib.sha256(data).hexdigest() != listed[name]:
            raise ValueError(f'Source checksum mismatch: {name}')
        files.append((name, data))
    if not files:
        raise ValueError('No files found')
    return files


def build(root: Path, target: Path) -> int:
    root = root.resolve()
    if target.is_symlink():
        raise ValueError('Symlink output not permitted')
    target = target.resolve()
    if target.exists():
        raise ValueError('Output exists: refusing overwrite')
    if target.is_relative_to(root):
        raise ValueError('Archive must be outside source package')
    if not target.parent.is_dir():
        raise ValueError('Output directory does not exist')
    sidecar = target.with_name(target.name + '.sha256')
    if sidecar.exists() or sidecar.is_symlink():
        raise ValueError('Checksum sidecar exists: refusing overwrite')
    files = source_files(root)
    sha_lines = [f'{hashlib.sha256(data).hexdigest()}  {name}' for name, data in files]
    created_target = created_sidecar = False
    try:
        with target.open('xb') as out:
            created_target = True
            with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
                payload = files + [('SHA256SUMS.txt', ('\n'.join(sha_lines) + '\n').encode())]
                for rel, data in payload:
                    entry = zipfile.ZipInfo(f'{root.name}/{rel}', ARCHIVE_TIME)
                    entry.external_attr = (stat.S_IFREG | 0o644) << 16
                    entry.compress_type = zipfile.ZIP_DEFLATED
                    z.writestr(entry, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        with sidecar.open('x', encoding='utf-8', newline='\n') as out:
            created_sidecar = True
            out.write(f'{digest}  {target.name}\n')
    except BaseException:
        if created_sidecar:
            sidecar.unlink(missing_ok=True)
        if created_target:
            target.unlink(missing_ok=True)
        raise
    print(f'Wrote {target.name} ({len(files)} source files + manifest), sha256 {digest}')
    return len(files)


if __name__ == '__main__':
    a = argparse.ArgumentParser(description=__doc__)
    a.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    a.add_argument('--output', type=Path, required=True)
    opts = a.parse_args()
    try:
        build(opts.root, opts.output)
    except (ValueError, OSError, zipfile.BadZipFile) as exc:
        print('BLOCKED: ' + str(exc), file=sys.stderr)
        sys.exit(2)
