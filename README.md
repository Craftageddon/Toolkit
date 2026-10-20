# Toolkit
Base Toolkit for Craftageddon.

# Craftageddon AI Toolchain v0.1.2 (starter package)

This is an **offline-tested, GitHub-ready toolkit**. It has not been installed on your Windows PC or connected to Blender/AutoCAD. The v0.1.1 source checkpoint is preserved on `setup/craftageddon-ai-toolchain-v0.1.1`. Packaging and publishing fixes are tracked on `setup/toolchain-hardening-v0.1.2`; see its draft PR for the exact commit, three verification gates, and CI results. See `docs/HARDENING_v0.1.2.md` for this follow-up scope.

## Included
- `AGENTS.md` global project rules and **mandatory three-verification gate**
- Six Codex-compatible `skills/*/SKILL.md` with project-specific constraints
- `scripts/triple_verify.py` evidence-based release gate with artifact integrity fingerprints
- `autocad/generate_lisp.py` restricted JSON-to-AutoLISP generator for 2D drafting (no remote execution); reviewable example .lsp
- `scripts/install_codex_skills.ps1` conservative Windows installer: copies skills, backs off on conflicts
- Setup notes for GitHub, Blender MCP, AutoCAD, Figma, SharePoint, and AYN Thor
- Blender offline smoke-test source (requires an actual Blender run for validation)
- Python unit tests and examples
- `scripts/build_release_zip.py` deterministic release ZIP builder with SHA-256 file manifest

## Windows setup
1. Extract the ZIP under your Desktop `Chat GPT Saved Files\Craftageddon AI Toolchain\v0.1.2` folder, or another reviewed folder. `%USERPROFILE%` means the current Windows account. Do not assume a specific username.
2. Open PowerShell in the extracted folder. Review `scripts/install_codex_skills.ps1` before execution.
3. Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install_codex_skills.ps1 -WhatIf` to preview; run without `-WhatIf` only after review.
4. The installer **only copies six skills** into `$HOME\.codex\skills` (refuses to overwrite), and does not touch projects, AutoCAD or Blender. Restart Codex to reload skills. The PowerShell installer has not been executed on your PC.
5. Copy this `AGENTS.md` to the root of each project after reviewing it.
6. Test in a Python 3.10+ environment: `python -m unittest discover -s tests -v`. Offline tests do not replace target-application tests.
7. Generate your own AutoLISP from `autocad/examples/simple_pattern.json` with `python autocad/generate_lisp.py autocad/examples/simple_pattern.json autocad/examples/pattern_review.lsp` (pick an unused output file), review it, and load only into a disposable millimeter drawing. AutoCAD integration is **not** verified yet.
8. See `docs/SETUP_GUIDE.md`, `docs/PHASE_STATUS.md`, and `docs/VERIFICATION_POLICY.md` before any plugin connection or hardware task.

## Verification usage
From any project directory (example using Python from toolkit path):

```powershell
python scripts/triple_verify.py init --root . --project "Demo" --artifact README.md
python scripts/triple_verify.py status --root .
```

Then create three separate, genuinely checked evidence files. Record sequentially:

```powershell
python scripts/triple_verify.py record --root . --check 1 --method "requirements-matrix" --reviewer "reviewer" --evidence verification/evidence/v1.txt
python scripts/triple_verify.py record --root . --check 2 --method "automated-tests" --reviewer "reviewer" --evidence verification/evidence/v2.txt
python scripts/triple_verify.py record --root . --check 3 --method "independent-app-or-physical-check" --reviewer "reviewer" --evidence verification/evidence/v3.txt --independence "Different tool or independent end-to-end check; describe the actual method here"
python scripts/triple_verify.py status --root .
python scripts/triple_verify.py finalize --root .  # eligible only when all 3 are valid
```

The verifier checks that evidence exists, is marked `CHECK: Vn` / `RESULT: PASS`, checksums have not changed, methods differ, gates are sequential, and artifact hashes still match. Evidence must be genuine, substantive, and saved under `verification/evidence/`. It cannot judge whether a real-world fit or manual review was honest: those require real evidence. Do not self-certify tests that have not happened.

## Current known blockers
- The original ZIP recorded HTTP 403 GitHub write failures. On this retry, linked GitHub branch creation succeeded and an independent Git read confirmed the branch. Source commit, draft PR, and CI evidence are recorded separately in the publication PR; the old report is historical.
- Local desktop, Blender 5.2.2, AutoCAD 2026, and AYN Thor were not accessed, installed to, or tested.
- SharePoint/OneDrive authorization, local app installations and hardware-based V3 testing remain pending.
- Android 16/LineageOS scope is reference-only; only tool planning is included.

**Status: STARTER PACKAGE / LOCAL INTEGRATION PENDING. Not a production release.**

### Updating a tracked artifact

After editing a tracked deliverable, use `python scripts/triple_verify.py resnapshot --root .`, which archives the previous gate state and resets all three checks. Do not treat earlier evidence as current. This protects against a passing test for an obsolete file.

### Scope of initial testing

The package can pass offline Python tests, file-manifest validation, and archive round-trip verification. **It cannot legitimately claim Windows install, Blender MCP operation, AutoCAD drawing import, or device testing** until each is actually performed and recorded. Those phases remain **PENDING**, not finalized.


## Publish this toolkit to your existing GitHub repository

The repo source is organized at this folder's root. A GitHub Actions CI workflow is provided in `.github/workflows/toolkit-ci.yml`. **Do not publish `.env`, passwords, local project source, or private customer data.**

On your own Windows PC with `git` authenticated to your `Craftageddon` GitHub account:

```powershell
powershell -NoProfile -File .\scripts\publish_to_github.ps1 -WhatIf
powershell -NoProfile -File .\scripts\publish_to_github.ps1
```

The script checks the expected remote, clones to a new temporary working directory, creates a dedicated `setup/toolchain-hardening-v0.1.2` branch, and stages only the reviewed source list. If any existing file differs, it stops before copying any files; reconcile changes manually on a review branch. It never replaces existing repository files. The fixed branch already exists after publication, so do not rerun this initial-publication helper for routine updates. Review the PR after CI passes. **The network publisher has not run on your computer.** Its offline staging helper is tested independently. See `docs/GITHUB_DEPLOYMENT.md`.

## Build a release archive

Run `python scripts/build_release_zip.py --output ../Craftageddon_AI_Toolchain_v0.1.2.zip` from the source root. The ZIP and SHA-256 sidecar must be new paths outside the source tree. An existing `SHA256SUMS.txt` is treated as a reviewed file allowlist: each listed file must match its hash, unlisted files are omitted, and exactly one fresh internal manifest is written. Update the source manifest after reviewing edits before building. `.gitattributes` keeps source line endings consistent across platforms.

For a source folder without a manifest, conventional generated/private paths are excluded. That fallback does not detect credentials embedded in ordinary source files; review every release input. Partial archives are removed if a write fails, and pre-existing archives or sidecars are preserved.
