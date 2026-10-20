# Offline checks versus real integrations

## V1: requirements and content review
The distribution package must contain the six agreed Codex skills, AGENTS.md, versioned project template, integration guide, Android reference-only protections, and three-check verification policy. This check concerns the **toolkit distribution**, not manufacturing or physical device functionality.

## V2: functional offline test
The Python unit tests must pass for evidence/manifest integrity, sequential verification, changed-file invalidation, restricted CAD JSON-to-AutoLISP generation, and archive repeatability. The sample AutoLISP is generated but **not run inside AutoCAD**. The Blender smoke script is included but **not run inside Blender**.

## V3: independent archive inspection
The final packaged ZIP must open without errors. Independently re-read every entry against the embedded SHA-256 manifest and cross-check each extracted file's hash against the original source tree, plus verify the ZIP sidecar hash.

## Explicitly excluded from offline verification
No GitHub repo edits; no local Codex skill install; no PowerShell execution on Windows; no Blender MCP connection; no AutoCAD 2026 live tests; no Microsoft tenant connection; no Android device or firmware tests. All remain PENDING or BLOCKED until approved and performed. No production or firmware-release claims are made.
