# Changelog

## Unreleased - standalone release-QA skill packaging
- Include a byte-identical copy of the canonical verification helper inside the release-QA skill so fresh installations work outside the Toolkit checkout.
- Explain skill-relative helper resolution and explicit project roots; leave checklist-only gates unrun.
- Add isolated helper lifecycle and PowerShell installer tests, including preview and preservation of existing skills.
- Extend the reviewed source manifest and publisher allowlist; retain the published v0.1.3 release and installer no-overwrite behavior.

## v0.1.3 (2026-10-20) - AutoCAD 2026 import fix
- Add explicit symbol-table/layer and entity/polyline subclass markers to generated records.
- Regenerate the reviewable example; add record-order and example-synchronization regression tests.
- Refresh the reviewed source checksums without weakening the archive integrity gate.
- Document bounded native AutoCAD import, dimensions, DWG/DXF reopen, independent parser evidence and unchanged-file hashes.
- Preserve prior release checkpoints; no installer, Android, production-drawing or global application-setting changes.

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
