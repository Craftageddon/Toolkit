#!/usr/bin/env python3
"""Create a deterministic Craftageddon ZIP and internal SHA256SUMS.txt manifest.

The generated archive is *only* an offline release candidate. Passing archive
integrity does not certify plugins, hardware, CAD integration, or manufacturability.
"""
from __future__ import annotations
import argparse
import hashlib
from pathlib import Path
import stat
import sys
import zipfile

EXCLUDE_DIRS = {'__pycache__', '.git', '.pytest_cache'}
EXCLUDE_SUFFIXES = {'.pyc', '.pyo', '.tmp'}
ARCHIVE_TIME = (2026, 10, 20, 0, 0, 0)


def build(root: Path, target: Path) -> int:
    root = root.resolve()
    target = target.resolve()
    if target.exists():
        raise ValueError('Output exists: refusing overwrite')
    if target.is_relative_to(root):
        raise ValueError('Archive must be outside source package')
    if not target.parent.is_dir():
        raise ValueError('Output directory does not exist')
    paths = sorted((p for p in root.rglob('*') if p.is_file() and not
                    (set(p.relative_to(root).parts) & EXCLUDE_DIRS)
                    and p.suffix.lower() not in EXCLUDE_SUFFIXES), key=lambda p: p.relative_to(root).as_posix())
    if not paths:
        raise ValueError('No files found')
    sha_lines = []
    with zipfile.ZipFile(target, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in paths:
            if p.is_symlink():
                raise ValueError(f'Symlink not permitted: {p}')
            rel = p.relative_to(root).as_posix()
            data = p.read_bytes()
            sha_lines.append(f'{hashlib.sha256(data).hexdigest()}  {rel}')
            entry = zipfile.ZipInfo(f'{root.name}/{rel}', ARCHIVE_TIME)
            entry.external_attr = (stat.S_IFREG | 0o644) << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(entry, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        checksum_entry = zipfile.ZipInfo(f'{root.name}/SHA256SUMS.txt', ARCHIVE_TIME)
        checksum_entry.external_attr = (stat.S_IFREG | 0o644) << 16
        checksum_entry.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(checksum_entry, '\n'.join(sha_lines) + '\n')
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    sidecar = target.with_name(target.name + '.sha256')
    if sidecar.exists():
        target.unlink()
        raise ValueError('Checksum sidecar exists: refusing overwrite')
    sidecar.write_text(f'{digest}  {target.name}\n', encoding='utf-8')
    print(f'Wrote {target.name} ({len(paths)} source files + manifest), sha256 {digest}')
    return len(paths)


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
