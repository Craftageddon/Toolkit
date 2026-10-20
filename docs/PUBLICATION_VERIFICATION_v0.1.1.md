> Historical report from the original ZIP. Its blocked-publication status describes the earlier attempt. For the permissions retry, see `PUBLICATION_RETRY_2026-10-20.md` and the draft PR.

# Publication verification, v0.1.1

Date: 2026-10-20
Status: **GITHUB PUBLICATION BLOCKED; LOCAL SOURCE VERIFIED**

## V1: requirements / security review â€” PASS for source package

- Correct destination repo: `Craftageddon/Toolkit` (explicitly user-supplied).
- Six Codex skills, AGENTS.md, README, setup guidance, version history, restricted AutoCAD generator, Blender smoke test and evidence-oriented triple-verification policy present.
- Publisher uses a strictly enumerated list of 30 files, verifies approved GitHub remote, creates only a review branch, never uses force-push, and supports `-WhatIf` preview.
- `.github/workflows/toolkit-ci.yml` runs offline tests on CPython 3.11 and 3.13 with read-only contents permissions.
- No production drawings, credentials, device firmware, customer data, or secrets were intentionally included.

## V2: technical / functional check â€” PASS for offline Python features

- `python -m compileall -q autocad scripts blender tests`: PASS.
- `python -m unittest discover -s tests -v`: PASS (19 tests, 0 failures).
- No claim of running PowerShell on Windows or executing Blender/AutoCAD.

## V3: independent local packaging/Git validation â€” PASS for source-stage only

- Parsed publication allowlist independently: 30 source files.
- Copied to a fresh isolated directory; initialized a local Git repository, checked staged diff whitespace with `git diff --cached --check`, and successfully committed 30 tracked files.
- This is an independent Git staging rehearsal, **not** an actual push or GitHub CI result.

## Blocked external steps

- GitHub GitHub integration `get_repo` and `fetch_file` succeeded, but `create_branch` on `setup/craftageddon-ai-toolchain-v0.1.1` returned HTTP 403 `Resource not accessible by integration`.
- `create_file` of `.gitignore` on main also returned HTTP 403 `Resource not accessible by integration`. It was not created.
- No files were uploaded or changed in the GitHub repository.
- PowerShell script was inspected but not executed in Windows. Blender MCP, AutoCAD, and Codex local installation remain unverified.

**Gate interpretation:** V1/V2/V3 above apply to the *local source artifact*. Remote deployment and application integrations are **NOT FINALIZED** and require separate V1/V2/V3 evidence when GitHub write authorization is fixed.
