# v0.1.1 source publication retry — 2026-10-20

Scope: publish the verified conversation ZIP to a setup branch and draft PR in
`Craftageddon/Toolkit`. This is a source publication, not an application deployment.
Reviewer: Codex. V3 uses an independent Git transport and fresh object inspection,
not a second human reviewer. Exact commit and post-publication results belong in
the draft PR and the external verification report, avoiding a self-referential
commit hash in this document.

## V1 — source and requirements review: PASS

| Acceptance criterion | Evidence |
| --- | --- |
| Use the supplied v0.1.1 source | ZIP SHA-256 `67feb4f05c27059cc43b17551ca270852704a989924b8c360fb5a94abaac4b9a`; archive CRC and all 30 embedded file hashes pass |
| Publish only reviewed source | All 30 files match the original publisher allowlist; six skill files and runtime source retained byte for byte |
| Preserve existing main files | Baseline `5005f538743234824227c41e485ca6cf5c528bdf`; LICENSE unchanged; original README heading and introduction retained |
| Use a setup branch and draft PR | `setup/craftageddon-ai-toolchain-v0.1.1`; branch creation succeeded after permissions update; main is not a publication target |
| Exclude generated and private data | Explicit file list; no ZIP, caches, evidence state, credentials, or private project data staged; source inspection and credential-pattern scan performed |
| Document accurate status | Publication notes distinguish historical 403 failures from this retry; original ZIP report retained as historical evidence |
| Respect scope | No skill installation, Windows app deployment, Blender/AutoCAD execution, or Android roadmap implementation |

Publication changes are documentation updates, preservation of the existing README,
this report, and a regenerated `SHA256SUMS.txt`. The manifest covers every committed
file except itself. The original ZIP manifest remains in the immutable intake copy.

## V2 — automated technical checks: PASS for offline source

- CPython 3.12.14: compilation of `autocad`, `scripts`, `blender`, and `tests` passed.
- `python -m unittest discover -s tests -v`: 19 tests, zero failures.
- Tests cover verification sequencing, evidence/artifact mutation, early-finalization
  rejection, constrained CAD generation, overwrite rejection, skill structure,
  Android scope, and deterministic archive creation.
- Both PowerShell scripts parse successfully; neither installer nor publisher was executed.
- Git staged whitespace validation and final source/manifest comparison are required
  before upload. The draft PR records final results.
- GitHub Actions adds Python 3.11/3.13 checks; results must be read from the actual
  commit runs and recorded in the PR, not inferred from workflow presence.

## V3 — independent remote commit/file validation: recorded after upload

After the connector writes the commit, use a separate Git client to fetch the
remote setup branch into a fresh repository. Verify its exact commit ID, parent,
complete file set, modes, and every file's SHA-256 against the reviewed local
snapshot. Compare the remote `main` reference with the baseline; confirm LICENSE
is identical and README retains its original introduction. Independently check the
draft PR base/head and changed-file list. Record timestamp and observed results
in the draft PR and external verification report. A successful write response
alone is insufficient for V3.

## Boundaries and review

All three gates apply only to this source-publication scope. Live Codex skill
discovery, Blender MCP, AutoCAD import, hardware functionality, and Android remain
unverified. The PR remains draft for owner review and is not merged automatically.
The bundled PowerShell publisher is an initial-publication helper; its fixed branch
already exists, so later updates require a separate reviewed update branch.
