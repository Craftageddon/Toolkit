# Craftageddon AI Development Rules (toolchain v0.1.4)

Applies to this repository and is intended to be copied into each Craftageddon project.

## Development contract
- Make real, inspectable, reproducible files, not just screenshots or claims of success.
- Preserve existing designs and source files. Do not destructively overwrite without an explicit owner-approved backup/restore plan.
- Put all new local work under `%USERPROFILE%\Desktop\Chat GPT Saved Files` when Windows filesystem access permits; use project/name/version directories. Never claim the local path was written if it was not.
- Prefer working on a branch; do not push to a remote or alter release channels without the owner's approval.
- Determine exact requirements and intended units, manufacturing process, and acceptance criteria before implementation.
- Maintain project changelog, source-of-truth links, build instructions, tests, and artifact manifest. Label WIP versus verified work.
- Use human-readable deterministic names; no silent last-minute renaming, file scaling, or resolution changes.
- Do not infer that generated CAD or 3D geometry is physically functional based solely on appearance.
- Treat account connections, plugin installs, hardware firmware, device flashes, network access, and destructive commands as approval-gated.
- Work locally and offline by default for EmberChat; never add telemetry, cloud dependencies, or keys unless explicitly authorized.

## Triple Verification: mandatory gate
1. **Requirements/Design Check (V1)**: compare requested functionality, dimensions, design, formats, and constraints against an itemized acceptance matrix.
2. **Technical/Functional Check (V2)**: test with suitable automated and in-application checks; provide evidence, errors, and logs.
3. **Independent Final Check (V3)**: validate using a distinct method/reviewer and end-to-end workflow. Check output files and real-world assembly or device operation when applicable.

These are three **separate, recorded checks**. Preserve evidence path, reviewer/method, date/time, and results for each. Invalidate affected checks whenever deliverables change. No 'FINAL', 'PRODUCTION READY', or 'COMPLETED' label if any check is pending, failed, or untestable. If hardware or a named app is unavailable, explicitly mark its validation **BLOCKED / NOT VERIFIED**, not PASS. See `docs/VERIFICATION_POLICY.md` and `scripts/triple_verify.py`.

## High-risk project protections
- **Android 16 / AYN Thor**: the Craftageddon Ember and Dark Steel Rework Revision 1.1 (2026-10-19), including 103 work packages, is REFERENCE ONLY. Do not implement it without specific fresh authorization. Before any future ROM deployment, require tested backups, recovery image, model identification, restore process and explicit flashing consent.
- **AutoCAD 2026**: drawing units and reference planes must be explicit; never load generated scripts into production drawings first. Validate DXF geometry; test on a disposable copy.
- **Blender**: generated Python via MCP can alter/delete data. Prefer sandboxed sessions, minimal permissions, allowlist working directories, and no sensitive files in the test environment.
- **K1 Max printing**: check build volume, material shrinkage, joints, print orientation, tolerances, watertight meshes and physical fit separately.
- **Leather patterns**: require real scale; avoid converting toolpaths to raster; red (ACI 1) main contours/holes, cyan (ACI 4) auxiliary/reference where applicable.

## Expected release bundle
`README.md`, `CHANGELOG.md`, source projects, export files, artifact checksum list, requirements matrix, V1/V2/V3 evidence, test instructions, unresolved limitations, and explicit status.
