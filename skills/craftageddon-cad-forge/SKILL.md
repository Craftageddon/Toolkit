---
name: craftageddon-cad-forge
description: Generate and validate precise Craftageddon 2D patterns and CAD exports. Use for centerline tracing, DXF/SVG/PDF, AutoCAD layers, units, dimensions, cut lines, and hole layouts.
---

# Craftageddon CAD Forge

Use for production-quality pattern geometry, not image-only mockups.

## Workflow
1. Identify reference files and model-space units explicitly (default millimeters; never silently infer scale).
2. Detect and trace **centerlines** for original strokes, smooth contours, and uniform circular holes. Preserve original geometry and maintain separate originals.
3. Create closed cut contours; verify no duplicate, dangling, self-intersecting, or degenerate segments. Validate curve fidelity and uniform holes.
4. Use **ACI Color 1 red** for main/cut geometry and holes; **ACI Color 4 cyan** for auxiliary/internal construction/reference. Keep layers meaningful and clean.
5. Minimize sheet waste but **never split parts** merely to nest them. Prefer 24 x 36 inch layout where requested. Keep scale constant.
6. Export files in requested formats: DXF mm model space, SVG physical units, actual-size PDF with tiled pages if necessary, and PNG previews within specified pixel/size limits. Do not claim native DWG without verified AutoCAD export.
7. Provide a geometry audit: bounds, hole diameter/count, layer/color map, overlaps, units, print calibration rulers.
8. Perform V1, V2, and V3 independently; include actual target-app DXF/DWG check when available. If not available, mark blocked.

## Special checks
- Precision and machining/laser compatibility outweigh visual likeness.
- Distinguish engrave fill versus cut contour in exports.
- If scanned or photographed source lacks a reference dimension, hold scale as provisional.
- For automated AutoCAD geometry use the restricted `autocad/generate_lisp.py` workflow as a starting point and review generated LISP before loading into disposable test drawings.
