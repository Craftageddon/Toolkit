# AutoCAD 2026 import fix — v0.1.3

## Problem and change

The original v0.1.2 generated sample loaded, but CFIMPORT failed to create the expected CG layers and stopped with zero model-space geometry. The corrected generator adds AcDbSymbolTableRecord / AcDbLayerTableRecord fields to layer records and AcDbEntity / AcDbPolyline fields to lightweight polyline records. The combined change passed the native test; individual fields were not tested in isolation.

The regenerated example is kept byte-identical to generator output by a regression test. Additional tests verify subclass marker ordering. SHA256SUMS.txt must be refreshed after reviewed changes: PR #3's original CI failure at 591bc10fde624cce1f0d278dfee6ee0cda544be2 was `Source checksum mismatch: autocad/generate_lisp.py`, not a reason to disable the integrity test.

## Recorded target-application evidence (2026-10-20)

Source comparison binds this revision's generator and sample to the previously tested local correction. They are byte-identical to the actual tested files; this comparison does not claim a new application run for unrelated documentation changes.

| Check | Observed result |
|---|---|
| Application | Autodesk AutoCAD 2026 (25.1) |
| Starting drawing | Empty disposable Drawing1, original inch units preserved in a separate blank DWG |
| Test units | INSUNITS=4 (mm), MEASUREMENT=1 |
| Geometry | Exactly 4 native model-space entities, Z=0 |
| Outline | Closed 80 x 50 mm polyline, area 4000 mm², perimeter 260 mm, zero bulges |
| Holes | Two circles at (10,10) and (70,10), radius 2 mm |
| Reference | Line from (40,0) to (40,50), length 50 mm |
| Colors | CG_CUT and CG_HOLES ACI 1 red; CG_REFERENCE ACI 4 cyan; geometry ByLayer |
| Persistence | DWG and DXF separately closed/reopened in native AutoCAD; dimensions and layers matched |
| Independent method | Separate Python ASCII-DXF group-code parser and direct geometry arithmetic, using neither generator nor AutoCAD API |
| File integrity | SHA-256 unchanged before/after native reopen; blank baseline remained empty in original inch units |

Recorded native sample hashes (evidence fingerprints, not additional release assets):

- DWG: `3aeee2a94c43c0cb32448f626c046b7c619244caab83fb9a309add305b0f0af6`
- DXF: `c63dde53a446d7e4c3052582b33009d5d4e53e2298fa9f02b197971cb70a4392`
- Blank baseline DWG: `2487d34260ec824871d84475f33b12638c9473a3503f052533891a084153a82a`

No production drawing received commands or mutations. No global settings, startup loaders, trust paths, security controls, firmware, Android code or installations were changed. Native files and machine-specific logs are retained locally and deliberately excluded from the source package.

## Verification gates and release boundary

- V1: review exact source, mm sample requirements, generated records, allowlist, hashes and preserved prior files.
- V2: run the entire offline suite and package checks. Target-application evidence above applies only when generator/example bytes match the tested files. CI itself does not run AutoCAD.
- V3: independently parse exported DXF, reopen persisted native files, and compare archive contents with reviewed source. For publication, independently fetch the uploaded commit/files and confirm GitHub CI on that exact revision. Remote CI/commit checks are pending until the updated branch is actually uploaded; local test results do not imply those checks passed.

Keep the PR in draft until the update and remote checks are complete. A local release candidate is not a published release. Retain v0.1.2 and use a new v0.1.3 tag only after review/merge and release approval. Never add generated ZIPs, credentials, caches or unrelated local project files to the branch.

## Reproduce the sample

Generate the LISP to a new path with `python autocad/generate_lisp.py autocad/examples/simple_pattern.json autocad/examples/pattern_review.lsp`. Review it; create an empty disposable mm drawing; LOAD/APPLOAD that file; run CFIMPORT once. Inspect units, geometry and colors; export/reopen and validate both exchange and native outputs before use. CFIMPORT appends geometry: a second invocation duplicates it. General self-intersection detection for arbitrary input is not provided.

A long inline SendCommand submission caused an access violation during the test; its precise cause was not established. Loading the reviewed LISP file worked. Prefer the file-load workflow. The sample is bounded integration evidence, not manufacturing approval or certification of arbitrary AutoCAD projects. Roll back source by using the retained v0.1.2 tag/checkpoint; restore local geometry from the blank backup rather than rerunning into an existing drawing.
