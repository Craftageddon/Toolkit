---
name: craftageddon-3d-print-engineer
description: Design and verify physically printable Craftageddon 3D assemblies for the Creality K1 Max. Use for STL/3MF parts, mechanical joints, tolerances, splitting, printable props, and assembly manuals.
---

# Craftageddon 3D Print Engineer

## Delivery sequence
1. Gather target outer dimensions, load case, material, printer, nozzle, desired print orientation and moving-part requirements. K1 Max nominal build volume is **300 x 300 x 300 mm**, but verify actual printable envelope and clearance in slicer.
2. Design each physical component separately and assign stable part IDs. Never use an attractive exploded view as proof of functional assembly.
3. Specify mechanically realizable connections: locating pins, dovetails, screws, inserts, snap-fit clips, pivots, bearings or keyed shafts as appropriate; demonstrate tool access and load direction.
4. Define tolerances by material and printer calibration rather than assuming universal values. Create small tolerance coupons for moving or mating surfaces.
5. Check manifoldness, minimum wall thickness, overhang/support strategy, trapped volumes, clearances, materials, part count and printer fit. Split oversized pieces at strong, reachable joints.
6. Provide assembly order, fastener/BOM, orientation labels, cutaway/clearance views and editable source model.
7. Export individually named STL/3MF parts; specify mm units and compare slicer dimensions against CAD.
8. V1: requirements and kinematics review. V2: computational mesh/fit/build checks. V3: independently simulate assembled motion and physically print/test when functional claims require it. Label unprinted as **not physically verified**.

## Craftageddon-specific reference
- Existing examples: mechanical lotus, fantasy dice towers, K1 Max deck boxes, relief mug shells and shoulder armor decorations.
- Honor real components (Rockler 16 oz insert or other hardware) by confirmed measurements, not image estimation.
