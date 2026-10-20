"""All checks are offline. They DO NOT prove Blender/AutoCAD runtime behavior."""
import importlib.util
import hashlib
import zipfile
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
VERIFY = ROOT / 'scripts' / 'triple_verify.py'
GEN = ROOT / 'autocad' / 'generate_lisp.py'


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

cad = load_module(GEN, 'craftageddon_gen_lisp')
packer = load_module(ROOT / 'scripts' / 'build_release_zip.py', 'craftageddon_zip')


class VerificationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'work.txt').write_text('source version one', encoding='utf-8')
        (self.root / 'verification' / 'evidence').mkdir(parents=True)

    def cmd(self, *args, ok=True):
        result = subprocess.run([sys.executable, str(VERIFY), *args, '--root', str(self.root)],
                                capture_output=True, text=True)
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return result

    def init(self):
        self.cmd('init', '--project', 'Sample', '--artifact', 'work.txt')

    def evidence(self, number, extra='Tested against an independently prepared checklist.'):
        f = self.root / 'verification' / 'evidence' / f'v{number}.txt'
        f.write_text(f'CHECK: V{number}\nRESULT: PASS\nObservations: The reviewed output met the expectations. {extra}\n', encoding='utf-8')
        return f'verification/evidence/v{number}.txt'

    def record(self, number, method=None, ok=True):
        return self.cmd('record', '--check', str(number), '--method', method or f'method-{number}',
                        '--reviewer', 'Inspector A', '--evidence', self.evidence(number),
                        *(['--independence', 'Clean-session separate method and inspection'] if number == 3 else []), ok=ok)

    def test_full_three_stage_flow(self):
        self.init()
        self.record(1)
        self.record(2)
        self.record(3)
        self.cmd('finalize')
        self.assertEqual(json.loads((self.root / 'verification' / 'state.json').read_text())['status'], 'FINALIZED')
        self.assertTrue((self.root / 'verification' / 'release.json').exists())

    def test_cannot_finalize_early(self):
        self.init()
        self.record(1)
        self.cmd('finalize', ok=False)

    def test_sequential_enforced(self):
        self.init()
        self.record(2, ok=False)

    def test_distinct_methods_enforced(self):
        self.init()
        self.record(1, method='identical')
        self.record(2, method='identical', ok=False)

    def test_missing_pass_marker_rejected(self):
        self.init()
        path = self.evidence(1)
        (self.root / path).write_text('CHECK: V1\nRESULT: BLOCKED\n' + 'Untested '*20, encoding='utf-8')
        self.cmd('record', '--check', '1', '--method', 'review-one', '--reviewer', 'Inspector A', '--evidence', path, ok=False)

    def test_changed_artifact_blocks_status_and_finalize(self):
        self.init()
        self.record(1)
        (self.root / 'work.txt').write_text('changed after review')
        self.cmd('status', ok=False)
        self.cmd('finalize', ok=False)
        self.cmd('resnapshot')
        self.assertEqual(json.loads((self.root / 'verification' / 'state.json').read_text())['checks'], {})

    def test_changed_evidence_blocks(self):
        self.init()
        self.record(1)
        (self.root / self.evidence(1)).write_text('CHECK: V1\nRESULT: PASS\n' + 'mutated '*15)
        self.cmd('status', ok=False)

    def test_escape_path_rejected(self):
        self.cmd('init', '--project', 'Escape', '--artifact', '../outside.txt', ok=False)

    def test_no_existing_state_overwrite(self):
        self.init()
        self.cmd('init', '--project', 'Again', '--artifact', 'work.txt', ok=False)


class AutoCADGeneratorTests(unittest.TestCase):
    def test_example_generates_expected_types_and_layers(self):
        data = json.loads((ROOT / 'autocad' / 'examples' / 'simple_pattern.json').read_text())
        value = cad.generate(data)
        for name in ('CG_CUT', 'CG_HOLES', 'CG_REFERENCE'):
            self.assertIn(name, value)
        self.assertIn('LWPOLYLINE', value)
        self.assertEqual(value.count('(cons 0 "CIRCLE")'), 2)
        self.assertIn('oldunits 4', value)
        self.assertIn('(defun c:CFIMPORT', value)

    def test_layer_records_include_subclass_markers_in_order(self):
        sample = json.loads((ROOT / 'autocad' / 'examples' / 'simple_pattern.json').read_text())
        generated = cad.generate(sample)
        layer_records = [line for line in generated.splitlines() if '(cons 0 "LAYER")' in line]
        self.assertEqual(len(layer_records), 3)
        for record in layer_records:
            markers = ['(cons 0 "LAYER")', '(cons 100 "AcDbSymbolTableRecord")',
                       '(cons 100 "AcDbLayerTableRecord")', '(cons 2 ']
            positions = [record.index(marker) for marker in markers]
            self.assertEqual(positions, sorted(positions))

    def test_polyline_records_include_subclass_markers_in_order(self):
        entity = {'type': 'polyline', 'layer': 'CUT', 'closed': True,
                  'points': [[0, 0], [80, 0], [80, 50], [0, 50]]}
        record = cad.add_entity(entity)
        markers = ['(cons 0 "LWPOLYLINE")', '(cons 100 "AcDbEntity")',
                   '(cons 8 "CG_CUT")', '(cons 100 "AcDbPolyline")', '(cons 90 4)']
        positions = [record.index(marker) for marker in markers]
        self.assertEqual(positions, sorted(positions))

    def test_checked_in_example_matches_generator(self):
        sample = json.loads((ROOT / 'autocad' / 'examples' / 'simple_pattern.json').read_text())
        expected = cad.generate(sample).encode('utf-8')
        self.assertEqual((ROOT / 'autocad' / 'examples' / 'simple_pattern_preview.lsp').read_bytes(), expected)

    def test_lisp_parentheses_are_balanced(self):
        sample = json.loads((ROOT / 'autocad' / 'examples' / 'simple_pattern.json').read_text())
        data = cad.generate(sample)
        depth = 0
        in_string = False
        escaped = False
        for line in data.splitlines():
            if line.lstrip().startswith(';'):
                continue
            for char in line:
                if escaped:
                    escaped = False
                elif char == '\\' and in_string:
                    escaped = True
                elif char == '"':
                    in_string = not in_string
                elif not in_string and char == '(':
                    depth += 1
                elif not in_string and char == ')':
                    depth -= 1
                    self.assertGreaterEqual(depth, 0)
        self.assertEqual(depth, 0)

    def test_lisp_injection_rejected(self):
        with self.assertRaises(cad.PatternError):
            cad.generate({'name':'Bad', 'units':'mm', 'entities':[{'type':'line','layer':'CUT") (command "_erase"','start':[0,0],'end':[1,1]}]})

    def test_nonfinite_number_rejected(self):
        with self.assertRaises(cad.PatternError):
            cad.number(float('nan'))
        with self.assertRaises(cad.PatternError):
            cad.number(float('inf'))

    def test_zero_length_rejected(self):
        with self.assertRaises(cad.PatternError):
            cad.add_entity({'type':'line','layer':'CUT','start':[2,2],'end':[2,2]})

    def test_unknown_keys_rejected(self):
        with self.assertRaises(cad.PatternError):
            cad.add_entity({'type':'circle','layer':'HOLES','radius':1,'center':[0,0],'eval':'evil'})

    def test_no_output_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            dest = Path(folder) / 'existing.lsp'
            dest.write_text('KEEP ORIGINAL')
            proc = subprocess.run([sys.executable,str(GEN),str(ROOT / 'autocad' / 'examples' / 'simple_pattern.json'), str(dest)], capture_output=True,text=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertEqual(dest.read_text(), 'KEEP ORIGINAL')


class StructureTests(unittest.TestCase):
    def test_all_skills_have_frontmatter_and_required_gates(self):
        skills = sorted((ROOT / 'skills').glob('*/SKILL.md'))
        self.assertEqual(len(skills), 6)
        for file in skills:
            content = file.read_text(encoding='utf-8')
            self.assertTrue(content.startswith('---\n'), file)
            self.assertIn('\nname:', content)
            self.assertIn('\ndescription:', content)
            for marker in ('V1', 'V2', 'V3'):
                self.assertIn(marker, content, file)

    def test_no_Android_implementation_claim(self):
        doc = (ROOT / 'skills' / 'craftageddon-android-lineageos-engineer' / 'SKILL.md').read_text()
        self.assertIn('reference-only', doc.lower())
        self.assertIn('HARD STOP', doc)


class ArchiveTests(unittest.TestCase):
    def test_archive_checksum_and_determinism(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'source'
            root.mkdir()
            (root / 'a.txt').write_text('A', encoding='utf-8')
            (root / 'b.txt').write_text('B', encoding='utf-8')
            first = Path(folder) / 'one.zip'
            second = Path(folder) / 'two.zip'
            self.assertEqual(packer.build(root, first), 2)
            self.assertEqual(packer.build(root, second), 2)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as z:
                self.assertIsNone(z.testzip())
                manifest = z.read('source/SHA256SUMS.txt').decode()
                self.assertIn(hashlib.sha256(b'A').hexdigest(), manifest)
                self.assertIn(hashlib.sha256(b'B').hexdigest(), manifest)


if __name__ == '__main__':
    unittest.main()
