"""Blender local smoke test. Run on disposable session only.

Example from project directory:
blender --background --factory-startup --python blender/smoke_scene.py -- --output ./test_outputs/cube.blend

Creates 20 mm cube and saves ONLY to a new, explicitly specified filepath.
No MCP installation or integration implied by this script.
"""
import argparse
from pathlib import Path
import sys

import bpy


def main():
    args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    cfg = parser.parse_args(args)
    output = Path(cfg.output).expanduser().resolve()
    if output.suffix != '.blend' or output.exists() or not output.parent.is_dir():
        raise RuntimeError('Expected unused *.blend path inside an existing disposable folder')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    bpy.context.scene.unit_settings.system = 'METRIC'
    bpy.context.scene.unit_settings.scale_length = 1.0
    bpy.ops.mesh.primitive_cube_add(size=0.02)
    cube = bpy.context.object
    cube.name = 'Craftageddon_Test_Cube_20mm'
    bpy.context.view_layer.update()
    dims = tuple(cube.dimensions)
    if any(abs(d - 0.02) > 1e-6 for d in dims):
        raise RuntimeError(f'Unexpected dimensions: {dims}')
    bpy.ops.wm.save_as_mainfile(filepath=str(output))
    print(f'SMOKE PASS: version={bpy.app.version_string}; cube_dimensions_m={dims}; path={output}')


if __name__ == '__main__':
    main()
