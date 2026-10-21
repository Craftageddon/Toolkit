# Installs the six reviewed skill directories, including bundled helpers. No overwrite, network, or app configuration.
[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium')]
param([string]$Destination = (Join-Path $HOME '.codex\skills'))
$ErrorActionPreference = 'Stop'
$packageRoot = Split-Path -Parent $PSScriptRoot
$source = Join-Path $packageRoot 'skills'
if (-not (Test-Path -LiteralPath $source -PathType Container)) { throw 'Skills source missing' }
$skills = @(
  'craftageddon-cad-forge', 'craftageddon-3d-print-engineer',
  'craftageddon-leather-pattern-engineer', 'craftageddon-ember-steel-ui',
  'craftageddon-android-lineageos-engineer', 'craftageddon-release-qa'
)
foreach ($name in $skills) {
  $from = Join-Path $source $name
  $to = Join-Path $Destination $name
  if (-not (Test-Path -LiteralPath (Join-Path $from 'SKILL.md') -PathType Leaf)) { throw "Skill missing: $name" }
  if (Test-Path -LiteralPath $to) { Write-Warning "Already exists, skipping without overwrite: $to"; continue }
  if ($PSCmdlet.ShouldProcess($to, "Copy verified skill '$name'")) {
    if (-not (Test-Path -LiteralPath $Destination)) {
      New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    }
    Copy-Item -LiteralPath $from -Destination $to -Recurse -ErrorAction Stop
    Write-Host "Installed: $name"
  }
}
Write-Host 'Restart Codex to pick up new skills. This script never touches Blender/AutoCAD/Android.'
