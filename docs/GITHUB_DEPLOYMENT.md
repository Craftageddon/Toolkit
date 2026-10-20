# Publish using a write-enabled local Git client

## v0.1.2 follow-up

The original v0.1.1 checkpoint is preserved in PR #1. The v0.1.2 fixes use
`setup/toolchain-hardening-v0.1.2` and a separate dependent draft PR; see
`HARDENING_v0.1.2.md`. The publisher now refuses differing existing files before
copying any source and stages only its explicit source list. It does not replace
the repository LICENSE. Reconcile existing-file changes manually on a review
branch. Its fixed initial-publication branch already exists after publication;
do not rerun it for routine updates. The steps below describe the original setup
workflow; local installation remains outside the current source-only work.

## Historical GitHub integration blocker

The original ZIP recorded two refused writes (`create_branch`, `create_file`): **403 Resource not accessible by integration**. After the permissions update, creating the setup branch succeeded and an independent Git read confirmed it. The draft PR records the exact source commit and verification outcomes. See `PUBLICATION_RETRY_2026-10-20.md`. Do not rerun the initial-publication script against an already published branch; use a reviewed update branch based on current main.

## Local release path (Windows)

1. Install Git for Windows from https://git-scm.com/download/win (if not already installed).
2. Authenticate in Git Credential Manager or GitHub CLI using the correct `Craftageddon` GitHub account. Never paste a token in ChatGPT or embed it in script files.
3. Extract the *entire* toolkit ZIP, including the `.github` directory, to a versioned folder under `%USERPROFILE%\Desktop\Chat GPT Saved Files\Craftageddon AI Toolchain\v0.1.1`.
4. Inspect `scripts/publish_to_github.ps1` and its allowlist. Start with a preview:

   ```powershell
   powershell -NoProfile -File .\scripts\publish_to_github.ps1 -WhatIf
   ```

5. Publish a **new branch**, not `main`:

   ```powershell
   powershell -NoProfile -File .\scripts\publish_to_github.ps1
   ```

6. Open the printed GitHub comparison URL, create a PR and review the changed file list. Wait for `Toolkit offline tests` to pass on both Python versions.
7. Merge the PR when V1/V2/V3 evidence exists for repository publication. The workflow does not certify runtime apps or hardware.
8. In each target Codex project, copy `AGENTS.md` and run the skill installer in `-WhatIf` mode before applying. Restart Codex and verify discovery manually.

## Permissions alternative

Re-authorize or reinstall the GitHub integration with access to `Craftageddon/Toolkit` and the required **Contents: read/write** and branch operations, if supported by the integration. Installing an app on an account is not the same as authorizing its write scopes. Then re-test in a separate safe branch.

## Explicit exclusions

The publisher copies only known source files; it will never push other folders under your local desktop, OneDrive content, `.env`, credentials, or hidden `.git` state.
