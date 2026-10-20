#!/usr/bin/env python3
"""Generate reviewable *offline* AutoLISP from a tightly constrained 2D JSON format.

The resulting script only defines a CFIMPORT command. It does not run on load.
Requires a disposable millimeter drawing; never use unreviewed on a production DWG.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import sys

LAYER_MAP = {'CUT': ('CG_CUT', 1), 'HOLES': ('CG_HOLES', 1),
             'REFERENCE': ('CG_REFERENCE', 4)}


class PatternError(Exception):
    pass


def number(value):
    if type(value) not in (int, float) or not math.isfinite(value) or abs(value) > 1_000_000:
        raise PatternError('Coordinates/radius must be finite real numbers within 1,000,000 mm')
    if value != 0 and abs(value) < 1e-8:
        raise PatternError('Values smaller than 0.00000001 mm not supported')
    rounded = f'{value:.9f}'.rstrip('0').rstrip('.')
    if rounded in ('', '-0'):
        rounded = '0'
    return rounded + '.0' if '.' not in rounded else rounded


def pt(value):
    if not isinstance(value, list) or len(value) != 2:
        raise PatternError('Point must be [x,y]')
    return tuple(float(number(v)) for v in value)


def point_expr(value, group):
    x, y = pt(value)
    return f'(cons {group} (list {number(x)} {number(y)} 0.0))'


def lwpoint_expr(value):
    x, y = pt(value)
    return f'(cons 10 (list {number(x)} {number(y)}))'


def add_entity(ent):
    if not isinstance(ent, dict):
        raise PatternError('Entity must be a JSON object')
    typ = ent.get('type')
    layer = ent.get('layer')
    if layer not in LAYER_MAP:
        raise PatternError(f'Layer must be one of {sorted(LAYER_MAP)}')
    layer_name = LAYER_MAP[layer][0]
    if typ == 'circle':
        if set(ent) != {'type','layer','center','radius'}:
            raise PatternError('Circle keys are type, layer, center, radius')
        radius = ent['radius']
        if type(radius) not in (float, int) or radius <= 0:
            raise PatternError('Circle radius must be positive')
        return f'''  (if (not (entmake (list (cons 0 "CIRCLE") (cons 8 "{layer_name}") {point_expr(ent['center'],10)} (cons 40 {number(radius)})))) (setq errors (+ errors 1)))'''
    if typ == 'line':
        if set(ent) != {'type','layer','start','end'}:
            raise PatternError('Line keys are type, layer, start, end')
        if pt(ent['start']) == pt(ent['end']):
            raise PatternError('Zero-length lines prohibited')
        return f'''  (if (not (entmake (list (cons 0 "LINE") (cons 8 "{layer_name}") {point_expr(ent['start'],10)} {point_expr(ent['end'],11)}))) (setq errors (+ errors 1)))'''
    if typ == 'polyline':
        if set(ent) != {'type','layer','closed','points'}:
            raise PatternError('Polyline keys are type, layer, closed, points')
        closed = ent['closed']
        points = ent['points']
        if type(closed) is not bool or not isinstance(points, list) or not 2 <= len(points) <= 20000:
            raise PatternError('Polyline requires bool closed and 2..20000 points')
        xy = [pt(p) for p in points]
        if (closed and len(xy) < 3) or len(set(xy)) != len(xy):
            raise PatternError('Polyline requires distinct points (and 3+ when closed)')
        if any(xy[i] == xy[(i+1)%len(xy)] for i in range(len(xy) if closed else len(xy)-1)):
            raise PatternError('Polyline contains zero-length edge')
        if closed and abs(sum(xy[i][0]*xy[(i+1)%len(xy)][1] - xy[(i+1)%len(xy)][0]*xy[i][1] for i in range(len(xy)))) < 1e-9:
            raise PatternError('Closed polyline has zero area')
        coords = '\n'.join(f'    {lwpoint_expr(p)}' for p in points)
        return f'''  (if (not (entmake (list (cons 0 "LWPOLYLINE") (cons 100 "AcDbEntity") (cons 8 "{layer_name}") (cons 100 "AcDbPolyline") (cons 90 {len(points)}) (cons 70 {1 if closed else 0})\n{coords}))) (setq errors (+ errors 1)))'''
    raise PatternError('Allowed types: circle, line, polyline')


def generate(data):
    if not isinstance(data, dict) or set(data) != {'name','units','entities'}:
        raise PatternError('Required top-level JSON keys: name, units, entities')
    if data['units'] != 'mm' or not isinstance(data['name'], str) or not (1 <= len(data['name']) <= 120):
        raise PatternError('Only named patterns in mm are supported')
    ents = data['entities']
    if not isinstance(ents, list) or not 1 <= len(ents) <= 20000:
        raise PatternError('Provide 1..20000 entities')
    entity_lines = '\n'.join(add_entity(ent) for ent in ents)
    layers = '\n'.join(f'''      (if (not (tblsearch "LAYER" "{name}"))
        (if (not (entmake (list (cons 0 "LAYER") (cons 100 "AcDbSymbolTableRecord") (cons 100 "AcDbLayerTableRecord") (cons 2 "{name}") (cons 70 0) (cons 62 {color}) (cons 6 "Continuous")))) (setq errors (+ errors 1)))
        (if (or (/= (abs (cdr (assoc 62 (tblsearch "LAYER" "{name}")))) {color})
                (assoc 420 (tblsearch "LAYER" "{name}")))
          (setq errors (+ errors 1))))'''
                        for name, color in LAYER_MAP.values())
    return f''';;; Craftageddon restricted 2D import. Review before APPLOAD. Millimeter drawing ONLY.
;;; Generated data: {len(ents)} entities. Command: CFIMPORT (not auto executed).
(defun c:CFIMPORT (/ errors oldunits)
  (setq errors 0)
  (setq oldunits (getvar "INSUNITS"))
  (if (/= oldunits 4)
    (princ "\\nWARNING: Drawing INSUNITS is not millimeters. No changes made; set to mm manually.")
    (progn
{layers}
      (if (= errors 0)
        (progn
{entity_lines}
          (if (= errors 0) (princ "\\nCFIMPORT completed.") (princ (strcat "\\nCFIMPORT entity errors: " (itoa errors))))
        )
        (princ "\\nCFIMPORT stopped: expected CUT/HOLES red and REFERENCE cyan layers could not be created or colors conflict.")
      )
    )
  )
  (princ)
)
(princ "\\nCFIMPORT loaded. Type CFIMPORT in a disposable mm drawing to run.")
(princ)
'''


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='Restricted JSON pattern')
    parser.add_argument('output', type=Path, help='LISP output path (.lsp)')
    args = parser.parse_args(argv)
    if args.output.suffix.lower() != '.lsp':
        parser.error('Output must end with .lsp')
    if args.output.exists():
        parser.error('Refusing to overwrite existing file')
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'))
        content = generate(data)
        args.output.write_text(content, encoding='utf-8', newline='\n')
    except (PatternError, OSError, ValueError, TypeError) as exc:
        print(f'BLOCKED: {exc}', file=sys.stderr)
        return 2
    print(f'Generated {args.output} (NOT installed or AutoCAD-tested)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
