# Publish only reviewed Craftageddon toolkit source to a new review branch.
# Requires locally installed and authenticated Git. Never pushes main or force-pushes.
[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium')]
param(
    [string]$Remote = 'https://github.com/Craftageddon/Toolkit.git',
    [string]$Branch = 'setup/toolchain-hardening-v0.1.2'
)
$ErrorActionPreference = 'Stop'
$sourceRoot = (Resolve-Path -LiteralPath (Split-Path -Parent $PSScriptRoot)).Path
$allowedFiles = @(
    '.gitattributes', '.gitignore', 'AGENTS.md', 'CHANGELOG.md', 'README.md', 'SECURITY.md', 'SHA256SUMS.txt',
    '.github/workflows/toolkit-ci.yml',
    'autocad/generate_lisp.py',
    'autocad/examples/simple_pattern.json', 'autocad/examples/simple_pattern_preview.lsp',
    'blender/smoke_scene.py',
    'docs/GITHUB_DEPLOYMENT.md', 'docs/OFFLINE_QA_SCOPE.md', 'docs/PHASE_STATUS.md',
    'docs/SETUP_GUIDE.md', 'docs/VERIFICATION_POLICY.md',
    'docs/PUBLICATION_VERIFICATION_v0.1.1.md',
    'docs/PUBLICATION_RETRY_2026-10-20.md', 'docs/HARDENING_v0.1.2.md',
    'docs/AUTOCAD_IMPORT_FIX_v0.1.3.md',
    'scripts/build_release_zip.py', 'scripts/install_codex_skills.ps1',
    'scripts/publish_to_github.ps1', 'scripts/triple_verify.py', 'scripts/stage_toolkit_source.ps1',
    'tests/test_toolchain.py', 'tests/test_hardening.py', 'tests/test_skill_packaging.py',
    'templates/Project_Template/README.md', 'templates/Project_Template/REQUIREMENTS.md',
    'templates/Project_Template/CHANGELOG.md',
    'skills/craftageddon-cad-forge/SKILL.md',
    'skills/craftageddon-3d-print-engineer/SKILL.md',
    'skills/craftageddon-leather-pattern-engineer/SKILL.md',
    'skills/craftageddon-ember-steel-ui/SKILL.md',
    'skills/craftageddon-android-lineageos-engineer/SKILL.md',
    'skills/craftageddon-release-qa/SKILL.md',
    'skills/craftageddon-release-qa/scripts/triple_verify.py'
)
if ($Remote -ne 'https://github.com/Craftageddon/Toolkit.git') {
    throw 'Remote must be the approved Craftageddon/Toolkit HTTPS URL.'
}
if ($Branch -ne 'setup/toolchain-hardening-v0.1.2') {
    throw 'Branch must be the approved review branch.'
}
foreach ($rel in $allowedFiles) {
    $local = Join-Path $sourceRoot ($rel.Replace('/', [IO.Path]::DirectorySeparatorChar))
    if (-not (Test-Path -LiteralPath $local -PathType Leaf)) { throw "Missing required source: $rel" }
}
Write-Host "Verified allowlist: $($allowedFiles.Count) source files"
Write-Host "Source: $sourceRoot"
Write-Host "Repository: $Remote"
Write-Host "Branch: $Branch"
if (-not $PSCmdlet.ShouldProcess($Remote, "Clone, stage approved files, and push $Branch")) {
    Write-Host 'Preview only. No remote or local Git changes were performed.'
    $allowedFiles | ForEach-Object { Write-Host "  $_" }
    return
}
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw 'Git for Windows is not installed or in PATH.' }
$workDir = Join-Path ([IO.Path]::GetTempPath()) ('Craftageddon_Toolkit_Publish_' + [guid]::NewGuid().ToString('N'))
if (Test-Path $workDir) { throw 'Unexpected staging path collision' }
New-Item -ItemType Directory -Path $workDir -ErrorAction Stop | Out-Null
Write-Host "Temporary Git clone: $workDir"
& git clone -- "$Remote" "$workDir"
if ($LASTEXITCODE -ne 0) { throw 'Clone failed. Check network and account access.' }
Push-Location $workDir
try {
    $origin = (& git remote get-url origin).Trim()
    if ($LASTEXITCODE -ne 0 -or $origin -ne $Remote) { throw 'Refusing to publish to unexpected remote' }
    & git switch -c "$Branch"
    if ($LASTEXITCODE -ne 0) { throw 'Unable to create review branch; it may already exist.' }
    & (Join-Path $sourceRoot 'scripts/stage_toolkit_source.ps1') -SourceRoot $sourceRoot -DestinationRoot $workDir -Paths $allowedFiles
    & git add -- $allowedFiles
    if ($LASTEXITCODE -ne 0) { throw 'Unable to stage source files.' }
    & git diff --cached --check
    if ($LASTEXITCODE -ne 0) { throw 'Whitespace or patch validation failed.' }
    & git diff --cached --stat
    & git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) { throw 'No content changes to publish.' }
    if ($LASTEXITCODE -ne 1) { throw 'Could not inspect staged differences.' }
    & git commit -m 'fix: harden Craftageddon toolkit packaging and source staging'
    if ($LASTEXITCODE -ne 0) { throw 'Commit failed. Configure Git author name and email.' }
    & git push --set-upstream origin "$Branch"
    if ($LASTEXITCODE -ne 0) { throw 'Push failed. Review credentials and repository write rights.' }
    Write-Host 'Branch pushed. Open a PR and review it before merging:'
    Write-Host 'https://github.com/Craftageddon/Toolkit/compare/main...setup/toolchain-hardening-v0.1.2'
} finally {
    Pop-Location
    Write-Host "Staging copy retained for review: $workDir"
}
