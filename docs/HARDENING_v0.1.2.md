# v0.1.2 source fixes and verification scope

The v0.1.1 source publication is preserved at commit
`8103086b6a6ec95fe8da6c015134875fc98b1bc0` and draft PR #1. This follow-up
uses `setup/toolchain-hardening-v0.1.2` and a separate draft PR targeting that
checkpoint branch. Review/merge PR #1 before retargeting the follow-up to main.
Neither PR is merged automatically.

## Requirements and acceptance criteria (V1)

| Observed problem | Required behavior | Verification |
| --- | --- | --- |
| Rebuilding from a folder containing SHA256SUMS writes the manifest twice | Exactly one internal manifest, each entry matches archived bytes, no duplicate ZIP names | Archive round-trip and real repository archive regression tests |
| Unreviewed/generated files can enter an archive | A present source manifest is a strict allowlist; reject changed/missing/unsafe entries; omit unlisted files | Unlisted-file, stale-hash, traversal, private-path and symlink tests |
| Output failures can leave a partial archive | Preserve existing ZIP/sidecar; preflight inputs; remove newly created partial outputs on failure | Collision and simulated write-failure regression tests |
| Publisher copies over existing files | Preflight every path and fail on any differing existing file before any copy; preserve identical files | Actual PowerShell staging-helper tests on disposable folders |
| Publication list misses later documentation/checksums | Explicit source list matches the reviewed manifest, excluding the repository's existing LICENSE | Repository-manifest/publisher integration test |
| README V3 recording example omits required independence | Include the actual required CLI argument | Source inspection and existing verifier workflow tests |
| Windows checkout can alter bytes represented by checksums | Enforce LF for text source with .gitattributes | Windows CI repository archive regression test |

The source manifest excludes only itself. The archive regenerates that one
manifest rather than embedding the input manifest as source. When no input
manifest exists, conventional private/generated paths are omitted; that mode
does not recognize arbitrary secrets inside ordinary source. Manifest files
and source must be reviewed together. These scripts are not a security boundary
against someone who can edit the source or manifest.

The offline staging helper does not overwrite files. It rejects unsafe/linked
paths and preflights conflicts. A later I/O failure can leave newly copied files
in the disposable clone; the clone is retained for inspection, and no push occurs
unless staging and subsequent Git checks succeed. The fixed publication branch
must not already exist; routine updates use a separately reviewed branch.

## V2 — required automated evidence

Run Python compilation and the full unit suite, including the new archive and
PowerShell staging regressions. CI runs Python 3.11/3.13 on Ubuntu and Python 3.13
with PowerShell 7 on Windows. Legacy Windows PowerShell 5 script execution was
blocked by the local execution policy and is not claimed as verified; no policy
was changed. Symlink tests may be skipped on a host that
cannot create unprivileged symlinks; record that limitation, and use Ubuntu CI
for the actual symlink test. Tests never install skills or invoke network publishing.

## V3 — distinct final validation

After connector publication, independently fetch the exact remote commit with
Git into a fresh checkout. Compare the entire file set, modes and every SHA-256
with the reviewed local snapshot. Build the release twice from that fresh source,
independently inspect ZIP names/CRC/hashes and compare both archives. Confirm the
v0.1.1 checkpoint and main references remain unchanged. Record exact commit IDs,
CI results, timestamps and outcomes in the follow-up PR and external evidence.

Prior v0.1.1 gate approvals do not apply to these changed files. The follow-up PR
records fresh V1/V2/V3 evidence. No production readiness, app integration, Windows
installation, Blender/AutoCAD operation or Android implementation is claimed.
