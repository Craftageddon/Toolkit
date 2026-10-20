# Changelog

## v0.1.2 (2026-10-20) - Packaging and publishing fixes
- Rebuild archives with exactly one internal checksum manifest; enforce a present source manifest as a checksum-validated allowlist.
- Exclude conventional generated/private paths, reject unsafe manifest paths, preserve existing outputs, and remove partial archives on failure.
- Preflight all publication paths and stop on existing-file conflicts before copying; stage only the explicit reviewed list.
- Include current publication documentation and manifest in the publisher source list; preserve the v0.1.1 checkpoint on its branch.
- Add regression tests, PowerShell 7 CI on Windows, consistent source line endings, and the required V3 independence argument in the README example.

## v0.1.1 publication retry (2026-10-20)
- Imported the checksum-verified conversation ZIP on a setup branch.
- Preserved the existing main license and README introduction.
- Added publication evidence and distinguished historical access failures from the permissions retry.
- Runtime source is unchanged; no local skill installation or Android implementation.

## v0.1.1 (2026-10-20) - GitHub-ready, not installed
- Added GitHub Actions Python test workflow, security notes and ignore list.
- Added explicit safe local Git publishing script and documented blocked GitHub integration writes.
- Retained six skills, triple-verification, CAD prototype and Blender smoke test.
- No claims of production readiness or successful Windows/Blender/AutoCAD installs.

## v0.1.0 (2026-10-20) - Offline starter
- Initial toolkit source; 19 offline unit tests passed.
