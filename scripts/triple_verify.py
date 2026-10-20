#!/usr/bin/env python3
"""Craftageddon evidence-based, hash-bound three-stage release gate.

This validates recorded evidence structure and integrity, not the truth of a human claim.
No third-party packages required. Python 3.10+.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import sys

STATE_FILE = Path('verification') / 'state.json'
RELEASE_FILE = Path('verification') / 'release.json'
STAGES = ('Requirements and design', 'Technical and functional', 'Independent validation')


class GateError(Exception):
    pass


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def safe_file(root: Path, name: str, *, existing=True) -> Path:
    if not name or Path(name).is_absolute():
        raise GateError('Artifact/evidence paths must be relative to --root')
    value = (root / name).resolve()
    try:
        rel = value.relative_to(root)
    except ValueError as exc:
        raise GateError(f'Path escapes project root: {name}') from exc
    if rel.parts[0] == 'verification' and existing is True and name.startswith('verification') is False:
        raise GateError('Unexpected verification path')
    if existing and (not value.is_file() or value.is_symlink()):
        raise GateError(f'Missing/invalid file: {name}')
    return value


def artifact_file(root: Path, name: str) -> Path:
    f = safe_file(root, name)
    if f.relative_to(root).parts[0] == 'verification':
        raise GateError('Verification records must not be tracked as release artifacts')
    return f


def state_path(root: Path) -> Path:
    return root / STATE_FILE


def read_state(root: Path) -> dict:
    file = state_path(root)
    if not file.is_file():
        raise GateError('No verification state. Run init first.')
    try:
        state = json.loads(file.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        raise GateError(f'Cannot read verification state: {exc}') from exc
    if state.get('schema') != 1 or not isinstance(state.get('artifacts'), dict):
        raise GateError('Invalid verification state schema')
    return state


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('w', encoding='utf-8', newline='\n') as fh:
        json.dump(data, fh, indent=2, sort_keys=True)
        fh.write('\n')
        fh.flush()
        os.fsync(fh.fileno())
    tmp.replace(path)


def integrity_issues(root: Path, state: dict) -> list[str]:
    issues = []
    for name, expected in state['artifacts'].items():
        try:
            file = artifact_file(root, name)
            if sha256(file) != expected:
                issues.append(f'Artifact modified: {name}')
        except GateError as exc:
            issues.append(str(exc))
    for key, rec in state.get('checks', {}).items():
        if not isinstance(rec, dict) or 'evidence' not in rec:
            issues.append(f'Invalid check record {key}')
            continue
        try:
            file = safe_file(root, rec['evidence'])
            if file.relative_to(root).parts[:2] != ('verification', 'evidence'):
                issues.append(f'Evidence must be in verification/evidence: {key}')
            elif sha256(file) != rec.get('evidence_sha256'):
                issues.append(f'Evidence modified: {key}')
        except GateError as exc:
            issues.append(str(exc))
    return issues


def cmd_init(args: argparse.Namespace, root: Path) -> None:
    if state_path(root).exists() or (root / RELEASE_FILE).exists():
        raise GateError('Verification state exists; use resnapshot after changing artifacts')
    if not args.artifact:
        raise GateError('At least one --artifact is required')
    artifacts = {}
    for name in args.artifact:
        f = artifact_file(root, name)
        rel = f.relative_to(root).as_posix()
        if rel in artifacts:
            raise GateError(f'Duplicate tracked artifact: {name}')
        artifacts[rel] = sha256(f)
    write_json(state_path(root), {'schema': 1, 'project': args.project, 'created_at': now(),
                                  'artifacts': artifacts, 'checks': {}, 'status': 'DRAFT'})
    print(f'Initialized {args.project!r} with {len(artifacts)} hash-tracked artifacts. Status: DRAFT')


def cmd_resnapshot(args: argparse.Namespace, root: Path) -> None:
    state = read_state(root)
    original = state_path(root)
    backup = original.with_name('state.previous-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ') + '.json')
    backup.write_bytes(original.read_bytes())
    tracked = {}
    for name in state['artifacts']:
        tracked[name] = sha256(artifact_file(root, name))
    state['artifacts'] = tracked
    state['checks'] = {}
    state['status'] = 'DRAFT'
    state['created_at'] = now()
    write_json(original, state)
    (root / RELEASE_FILE).unlink(missing_ok=True)
    print('New artifact fingerprints saved; all checks reset to PENDING. Previous state archived.')


def cmd_record(args: argparse.Namespace, root: Path) -> None:
    state = read_state(root)
    if state.get('status') == 'FINALIZED':
        raise GateError('Already finalized. Use resnapshot for a new version/review cycle.')
    issues = integrity_issues(root, state)
    if issues:
        raise GateError('; '.join(issues) + '; resnapshot required')
    key = str(args.check)
    if key in state['checks']:
        raise GateError(f'V{key} already recorded; resnapshot to repeat verification')
    if args.check > 1 and str(args.check - 1) not in state['checks']:
        raise GateError(f'V{args.check - 1} must pass before V{key}')
    method = args.method.strip()
    reviewer = args.reviewer.strip()
    if len(method) < 5 or len(reviewer) < 2:
        raise GateError('Method (min 5 characters) and named reviewer (min 2) required')
    if method.casefold() in [v['method'].casefold() for v in state['checks'].values()]:
        raise GateError('Each verification needs a distinct test method')
    e = safe_file(root, args.evidence)
    relative = e.relative_to(root)
    if relative.parts[:2] != ('verification', 'evidence'):
        raise GateError('Evidence must be stored under verification/evidence/')
    if str(relative) in [v['evidence'] for v in state['checks'].values()]:
        raise GateError('Each stage needs its own evidence file')
    if e.stat().st_size > 2_000_000:
        raise GateError('Evidence file too large; link external reports from a summary file')
    try:
        content = e.read_text(encoding='utf-8')
    except UnicodeError as exc:
        raise GateError('Evidence must be UTF-8 text') from exc
    if len(content.strip()) < 60 or f'CHECK: V{args.check}' not in content or 'RESULT: PASS' not in content:
        raise GateError(f'Evidence must contain CHECK: V{args.check}, RESULT: PASS, and substantive observations')
    if args.check == 3:
        if not args.independence or len(args.independence.strip()) < 12:
            raise GateError('V3 requires --independence explaining how it is independent')
    rec = {'name': STAGES[args.check - 1], 'method': method, 'reviewer': reviewer,
           'date_utc': now(), 'evidence': relative.as_posix(), 'evidence_sha256': sha256(e),
           'independence': args.independence.strip() if args.check == 3 else None,
           'result': 'PASS'}
    state['checks'][key] = rec
    state['status'] = f'V{key}_PASS'
    write_json(state_path(root), state)
    print(f'V{key} recorded. {3 - args.check} check(s) remain before finalization.')


def cmd_status(args: argparse.Namespace, root: Path) -> None:
    state = read_state(root)
    issues = integrity_issues(root, state)
    print(f"Project: {state['project']} | Status: {'STALE / BLOCKED' if issues else state['status']}")
    for n, name in enumerate(STAGES, 1):
        print(f" V{n} {name}: {'PASS (recorded)' if str(n) in state['checks'] and not issues else 'BLOCKED' if issues else 'PENDING'}")
    if issues:
        print('Integrity issues:')
        for issue in issues:
            print(' - ' + issue)
    if issues:
        raise GateError('Integrity failed: release not permitted')


def cmd_finalize(args: argparse.Namespace, root: Path) -> None:
    state = read_state(root)
    if state.get('status') == 'FINALIZED':
        raise GateError('Already finalized')
    issues = integrity_issues(root, state)
    if issues:
        raise GateError('; '.join(issues))
    if sorted(state['checks']) != ['1', '2', '3']:
        raise GateError('All three recorded PASS checks required')
    methods = [state['checks'][str(i)]['method'].casefold() for i in range(1, 4)]
    if len(set(methods)) < 3 or not state['checks']['3'].get('independence'):
        raise GateError('Independent methods and V3 independence justification required')
    state['status'] = 'FINALIZED'
    state['finalized_at'] = now()
    write_json(state_path(root), state)
    write_json(root / RELEASE_FILE,
               {'project': state['project'], 'finalized_at': state['finalized_at'],
                'artifacts': state['artifacts'], 'checks': state['checks'],
                'notice': 'Documentation gate only. No device installation, manufacturing fitness, or publication permission implied.'})
    print('FINALIZED: three hash-bound checks passed. Publishing or destructive actions still require owner approval.')


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    init = sub.add_parser('init')
    init.add_argument('--project', required=True)
    init.add_argument('--artifact', action='append', help='Relative file path; repeat for each file')
    sub.add_parser('resnapshot').add_argument('--root', default='.')
    rec = sub.add_parser('record')
    rec.add_argument('--check', required=True, type=int, choices=(1, 2, 3))
    rec.add_argument('--method', required=True)
    rec.add_argument('--reviewer', required=True)
    rec.add_argument('--evidence', required=True)
    rec.add_argument('--independence', default='')
    sub.add_parser('status').add_argument('--root', default='.')
    sub.add_parser('finalize').add_argument('--root', default='.')
    for command in (init, rec):
        command.add_argument('--root', default='.', help='Project root (absolute or relative)')
    args = p.parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print('ERROR: Project directory missing', file=sys.stderr)
        return 2
    try:
        {'init': cmd_init, 'resnapshot': cmd_resnapshot, 'record': cmd_record,
         'status': cmd_status, 'finalize': cmd_finalize}[args.command](args, root)
        return 0
    except (GateError, OSError, ValueError, KeyError) as exc:
        print(f'BLOCKED: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
