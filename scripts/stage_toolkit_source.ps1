# Offline staging helper. Preflight every path; never replace an existing file.
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $true)][string]$SourceRoot,
    [Parameter(Mandatory = $true)][string]$DestinationRoot,
    [Parameter(Mandatory = $true)][string[]]$Paths
)
$ErrorActionPreference = 'Stop'
$sourceBase = (Resolve-Path -LiteralPath $SourceRoot).Path
$destinationBase = (Resolve-Path -LiteralPath $DestinationRoot).Path
$seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
$plan = @()
foreach ($rel in $Paths) {
    $parts = $rel -split '[/\\]'
    if ([IO.Path]::IsPathRooted($rel) -or $rel.Contains(':') -or
        ($parts | Where-Object { $_ -in @('', '.', '..') }) -or -not $seen.Add($rel.Replace('\', '/'))) {
        throw "Unsafe or duplicate source path: $rel"
    }
    $local = Join-Path $sourceBase ($parts -join [IO.Path]::DirectorySeparatorChar)
    $target = Join-Path $destinationBase ($parts -join [IO.Path]::DirectorySeparatorChar)
    foreach ($base in @($sourceBase, $destinationBase)) {
        $cursor = $base
        foreach ($part in @('') + $parts) {
            if ($part) { $cursor = Join-Path $cursor $part }
            if (Test-Path -LiteralPath $cursor) {
                $item = Get-Item -LiteralPath $cursor -Force
                if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
                    throw "Linked source/destination path is not allowed: $cursor"
                }
                if ($cursor -ne $local -and $cursor -ne $target -and -not $item.PSIsContainer) {
                    throw "Parent is not a directory: $cursor"
                }
            }
        }
    }
    if (-not (Test-Path -LiteralPath $local -PathType Leaf)) { throw "Missing source: $rel" }
    $exists = Test-Path -LiteralPath $target
    if ($exists -and (-not (Test-Path -LiteralPath $target -PathType Leaf) -or
        (Get-FileHash -LiteralPath $local -Algorithm SHA256).Hash -ne
        (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash)) {
        throw "Existing repository file differs: $rel. Reconcile it on a review branch; no files were copied."
    }
    $plan += [pscustomobject]@{ Relative = $rel; Source = $local; Target = $target; Exists = $exists }
}
foreach ($entry in $plan) {
    if (-not $entry.Exists -and $PSCmdlet.ShouldProcess($entry.Target, 'Copy new toolkit source without overwrite')) {
        $parent = Split-Path -Parent $entry.Target
        if (-not (Test-Path -LiteralPath $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
        [IO.File]::Copy($entry.Source, $entry.Target, $false)
    }
}
Write-Host "Preflight passed for $($plan.Count) source paths; existing identical files preserved."
