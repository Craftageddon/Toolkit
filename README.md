# Toolkit
Base Toolkit for Craftageddon.

# Craftageddon AI Toolchain v0.1.3 (starter package)

This update fixes AutoCAD 2026 layer/polyline record creation and keeps the checked-in example synchronized with the generator. The corrected source and example are byte-identical to those used in the recorded native AutoCAD test: an 80 x 50 mm panel, two diameter-4 mm holes, red cut/hole layers, and a cyan reference line. DWG/DXF save/reopen and a separate DXF parser passed for that sample. This is bounded integration evidence, not general production or fabrication certification. See `docs/AUTOCAD_IMPORT_FIX_v0.1.3.md` for exact scope and known limitations. Earlier publication checkpoints remain preserved in Git history.

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
1. Extract the ZIP under your Desktop `Chat GPT Saved Files\Craftageddon AI Toolchain\v0.1.3` folder, or another reviewed folder. `%USERPROFILE%` means the current Windows account. Do not assume a specific username.
2. Open PowerShell in the extracted folder. Review `scripts/install_codex_skills.ps1` before execution.
3. Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install_codex_skills.ps1 -WhatIf` to preview; run without `-WhatIf` only after review.
4. The installer **only copies six skill directories and their bundled helpers** into `$HOME\.codex\skills` (refuses to overwrite), and does not touch projects, AutoCAD or Blender. Restart Codex to reload skills. Installer integration tests use disposable directories; they do not install into your real user profile.
5. Copy this `AGENTS.md` to the root of each project after reviewing it.
6. Test in a Python 3.10+ environment: `python -m unittest discover -s tests -v`. Offline tests do not replace target-application tests.
7. Generate your own AutoLISP from `autocad/examples/simple_pattern.json` with `python autocad/generate_lisp.py autocad/examples/simple_pattern.json autocad/examples/pattern_review.lsp` (pick an unused output file), review it, and load only into a disposable millimeter drawing. The corrected sample has recorded AutoCAD 2026 import/export verification; every new pattern still needs its own checks. Run CFIMPORT only once per empty test drawing because it appends geometry.
8. See `docs/SETUP_GUIDE.md`, `docs/PHASE_STATUS.md`, and `docs/VERIFICATION_POLICY.md` before any plugin connection or hardware task.

## Verification usage
The installed `craftageddon-release-qa` skill is self-contained. Its helper lives
at `scripts/triple_verify.py` **inside that skill's folder**. Resolve the helper
relative to the loaded `SKILL.md`, invoke it by absolute path, and pass the real
project directory with `--root`. You can run it from an unrelated working
directory without a Toolkit checkout or third-party Python packages.

For example (replace both absolute paths with your actual locations):

```text
python "<installed-skill-directory>/scripts/triple_verify.py" init --root "<project-directory>" --project "Demo" --artifact README.md
python "<installed-skill-directory>/scripts/triple_verify.py" status --root "<project-directory>"
```

The installer still skips existing skill directories without overwriting them.
Existing installations do not acquire this helper automatically: back up and
review an explicit skill replacement separately. A checklist-only request does
not need tracker initialization; leave unperformed gates NOT RUN.

The repository's top-level CLI remains available for Toolkit users:

From the Toolkit source directory:

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
- The initial releases did not verify local applications. This update carries bounded AutoCAD 2026 sample evidence only; it does not certify Blender or AYN Thor workflows.
- SharePoint/OneDrive authorization, local app installations and hardware-based V3 testing remain pending.
- Android 16/LineageOS scope is reference-only; only tool planning is included.

**Status: STARTER PACKAGE / BOUNDED AUTOCAD SAMPLE VERIFIED. Not a production release.**

### Updating a tracked artifact

After editing a tracked deliverable, use `python scripts/triple_verify.py resnapshot --root .`, which archives the previous gate state and resets all three checks. Do not treat earlier evidence as current. This protects against a passing test for an obsolete file.

### Scope of initial testing

Offline tests, manifest validation, archive checks, and target-application tests are distinct evidence. The recorded AutoCAD sample checks apply only to the byte-identical corrected source/example described above. They do not verify arbitrary drawings, general Windows setup, Blender MCP operation, or device testing.


## Publish this toolkit to your existing GitHub repository

The repo source is organized at this folder's root. A GitHub Actions CI workflow is provided in `.github/workflows/toolkit-ci.yml`. **Do not publish `.env`, passwords, local project source, or private customer data.**

On your own Windows PC with `git` authenticated to your `Craftageddon` GitHub account:

```powershell
powershell -NoProfile -File .\scripts\publish_to_github.ps1 -WhatIf
powershell -NoProfile -File .\scripts\publish_to_github.ps1
```

The script checks the expected remote, clones to a new temporary working directory, creates a dedicated `setup/toolchain-hardening-v0.1.2` branch, and stages only the reviewed source list. If any existing file differs, it stops before copying any files; reconcile changes manually on a review branch. It never replaces existing repository files. The fixed branch already exists after publication, so do not rerun this initial-publication helper for routine updates. Review the PR after CI passes. **The network publisher has not run on your computer.** Its offline staging helper is tested independently. See `docs/GITHUB_DEPLOYMENT.md`.

## Build a release archive

Run `python scripts/build_release_zip.py --output ../Craftageddon_AI_Toolchain_v0.1.3.zip` from the source root. The ZIP and SHA-256 sidecar must be new paths outside the source tree. An existing `SHA256SUMS.txt` is treated as a reviewed file allowlist: each listed file must match its hash, unlisted files are omitted, and exactly one fresh internal manifest is written. Update the source manifest after reviewing edits before building. `.gitattributes` keeps source line endings consistent across platforms.

For a source folder without a manifest, conventional generated/private paths are excluded. That fallback does not detect credentials embedded in ordinary source files; review every release input. Partial archives are removed if a write fails, and pre-existing archives or sidecars are preserved.
