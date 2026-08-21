<#
.SYNOPSIS
    Andrelawas Work Studio — dependency-free adapter installer (Windows/PowerShell).

.DESCRIPTION
    Installs committed, checksummed adapter artifacts into a platform's skills
    directory. Requires NO Python at runtime and no external SHA-256 tool —
    only Windows PowerShell 5.1+ (Get-FileHash is built in). This is the
    native-Windows counterpart to tools/install.sh; both read the same
    adapters/<platform>/SHA256SUMS files and enforce the same precedence rule.

.PARAMETER Platform
    codex | claude-code | github-copilot

.PARAMETER Global
    Install the global bootstrap adapter for -Platform.

.PARAMETER Project
    Pin the adapter to a project directory. Combine with -Dir (default: .).

.PARAMETER Verify
    Verify source artifacts only; do not install.

.PARAMETER Resolve
    Print which install (project pin or global) wins for -Dir (default: .).

.PARAMETER Dir
    Target directory for -Project or -Resolve. Defaults to the current directory.

.PARAMETER Dest
    Override the install directory entirely.

.PARAMETER DryRun
    Show what would happen without writing.

.EXAMPLE
    tools/install.ps1 -Platform claude-code -Global

.EXAMPLE
    tools/install.ps1 -Platform codex -Project -Dir .

.EXAMPLE
    tools/install.ps1 -Platform codex -Resolve -Dir .
#>
[CmdletBinding(DefaultParameterSetName = 'Global')]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet('codex', 'claude-code', 'github-copilot')]
    [string]$Platform,

    [Parameter(ParameterSetName = 'Global', Mandatory = $true)]
    [switch]$Global,

    [Parameter(ParameterSetName = 'Project', Mandatory = $true)]
    [switch]$Project,

    [Parameter(ParameterSetName = 'Verify', Mandatory = $true)]
    [switch]$Verify,

    [Parameter(ParameterSetName = 'Resolve', Mandatory = $true)]
    [switch]$Resolve,

    [Parameter(ParameterSetName = 'Project')]
    [Parameter(ParameterSetName = 'Resolve')]
    [string]$Dir = '.',

    [string]$Dest,

    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

function Die {
    param([string]$Message)
    Write-Error "install.ps1: $Message"
    exit 1
}

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

function Get-GlobalDir {
    param([string]$Platform)
    switch ($Platform) {
        'claude-code' {
            if ($env:CLAUDE_HOME) { Join-Path $env:CLAUDE_HOME 'skills' }
            else { Join-Path $env:USERPROFILE '.claude\skills' }
        }
        'codex' { Join-Path $env:USERPROFILE '.agents\skills' }
        'github-copilot' {
            if ($env:COPILOT_HOME) { Join-Path $env:COPILOT_HOME 'skills' }
            else { Join-Path $env:USERPROFILE '.copilot\skills' }
        }
        default { Die "unknown platform: $Platform" }
    }
}

function Get-ProjectSubdir {
    param([string]$Platform)
    switch ($Platform) {
        'claude-code' { '.claude\skills' }
        'codex' { '.agents\skills' }
        'github-copilot' { '.github\skills' }
        default { Die "unknown platform: $Platform" }
    }
}

# ── SHA-256 verification (native Get-FileHash, no external tool) ────────────
function Test-Sha256Sums {
    <#
    Verifies every file listed in $SumsFile (sha256sum format: "<hex>  <relpath>",
    paths using forward slashes) against its hash, resolved relative to $BaseDir.
    Throws on the first mismatch or missing file.
    #>
    param(
        [string]$SumsFile,
        [string]$BaseDir
    )
    if (-not (Test-Path $SumsFile)) {
        Die "missing $SumsFile"
    }
    foreach ($line in Get-Content -Path $SumsFile -Encoding utf8) {
        if ($line.Trim() -eq '') { continue }
        if ($line -notmatch '^([0-9a-fA-F]{64})\s+\*?(.+)$') {
            Die "malformed SHA256SUMS line: $line"
        }
        $expectedHash = $Matches[1].ToLowerInvariant()
        $relPath = $Matches[2] -replace '/', '\'
        $fullPath = Join-Path $BaseDir $relPath
        if (-not (Test-Path $fullPath)) {
            Die "checksum verification FAILED: missing file $relPath"
        }
        $actualHash = (Get-FileHash -Path $fullPath -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actualHash -ne $expectedHash) {
            Die "checksum verification FAILED: $relPath (expected $expectedHash, got $actualHash)"
        }
    }
}

function Invoke-VerifySource {
    param([string]$Src, [string]$Platform)
    Test-Sha256Sums -SumsFile (Join-Path $Src 'SHA256SUMS') -BaseDir $Src
    Write-Output "verified: $Platform adapter artifacts match SHA256SUMS"
}

# ── resolve: report effective adapter (project pin beats global) ───────────
function Invoke-Resolve {
    param([string]$TargetDir, [string]$Platform)
    $current = (Resolve-Path $TargetDir).Path
    while ($true) {
        $lock = Join-Path $current ".work-studio\adapter.$Platform.lock"
        $legacyLock = Join-Path $current '.work-studio\adapter.lock'
        if (Test-Path $lock) {
            $pinnedLine = (Get-Content $lock | Where-Object { $_ -match '^dest=' }) | Select-Object -First 1
            $pinned = $pinnedLine -replace '^dest=', ''
            if ($pinned -match '^([a-zA-Z]:\\|\\\\|/)') {
                Write-Output "project:$pinned"
            } else {
                Write-Output "project:$(Join-Path $current $pinned)"
            }
            return
        }
        if (Test-Path $legacyLock) {
            $platformLine = Get-Content $legacyLock | Where-Object { $_ -eq "platform=$Platform" }
            if ($platformLine) {
                $pinnedLine = (Get-Content $legacyLock | Where-Object { $_ -match '^dest=' }) | Select-Object -First 1
                $pinned = $pinnedLine -replace '^dest=', ''
                if ($pinned -match '^([a-zA-Z]:\\|\\\\|/)') {
                    Write-Output "project:$pinned"
                } else {
                    Write-Output "project:$(Join-Path $current $pinned)"
                }
                return
            }
        }
        if (Test-Path (Join-Path $current '.git')) { break }
        $parent = Split-Path $current -Parent
        if (-not $parent -or $parent -eq $current) { break }
        $current = $parent
    }
    Write-Output "global:$(Get-GlobalDir -Platform $Platform)"
}

# ── install: verify, then copy skills into the destination ─────────────────
function Invoke-Install {
    param([string]$Src, [string]$Platform, [string]$Mode, [string]$TargetDir, [string]$Version)

    Invoke-VerifySource -Src $Src -Platform $Platform

    if ($Dest) {
        $installDest = $Dest
    } elseif ($Mode -eq 'Global') {
        $installDest = Get-GlobalDir -Platform $Platform
    } else {
        $installDest = Join-Path $TargetDir (Get-ProjectSubdir -Platform $Platform)
    }

    Write-Output "installing $Platform adapter v$Version -> $installDest"

    if ($DryRun) {
        Write-Output "(dry-run) would copy $Src\skills\* to $installDest"
        if ($Mode -eq 'Project') {
            Write-Output "(dry-run) would write $TargetDir\.work-studio\adapter.$Platform.lock"
        }
        return
    }

    New-Item -ItemType Directory -Force -Path $installDest | Out-Null

    $skillsRoot = Join-Path $Src 'skills'
    Get-ChildItem -Path $skillsRoot -Directory | ForEach-Object {
        $destSkill = Join-Path $installDest $_.Name
        if (Test-Path $destSkill) { Remove-Item -Recurse -Force $destSkill }
        Copy-Item -Recurse -Path $_.FullName -Destination $destSkill
    }

    # Verify the installed copy byte-for-byte against the source checksums.
    # SHA256SUMS paths are `skills/<name>/...`; installed paths drop the
    # `skills/` prefix.
    $rewritten = Get-Content (Join-Path $Src 'SHA256SUMS') -Encoding utf8 |
        ForEach-Object { $_ -replace '^([0-9a-fA-F]{64})\s+\*?skills/', '$1  ' }
    $sumsCheckFile = Join-Path $installDest '.work-studio-sha256sums-check.txt'
    Set-Content -Path $sumsCheckFile -Value $rewritten -Encoding utf8
    try {
        Test-Sha256Sums -SumsFile $sumsCheckFile -BaseDir $installDest
    } catch {
        Remove-Item -Force $sumsCheckFile -ErrorAction SilentlyContinue
        Die "installed copy failed verification at $installDest"
    }
    Remove-Item -Force $sumsCheckFile

    if ($Mode -eq 'Project') {
        $lockDir = Join-Path $TargetDir '.work-studio'
        New-Item -ItemType Directory -Force -Path $lockDir | Out-Null
        $destRel = Get-ProjectSubdir -Platform $Platform
        $lockPath = Join-Path $lockDir "adapter.$Platform.lock"
        @(
            '# Work Studio adapter pin -- this project overrides the global install.'
            "platform=$Platform"
            "version=$Version"
            "dest=$destRel"
        ) | Set-Content -Path $lockPath -Encoding utf8

        $legacyLock = Join-Path $lockDir 'adapter.lock'
        if (Test-Path $legacyLock) {
            $platformLine = Get-Content $legacyLock | Where-Object { $_ -eq "platform=$Platform" }
            if ($platformLine) { Remove-Item -Force $legacyLock }
        }
        Write-Output "pinned: $lockPath (project overrides global for $Platform)"
    }

    Write-Output "done."
}

# ── main ─────────────────────────────────────────────────────────────────────

$Src = Join-Path $RepoRoot "adapters\$Platform"
if (-not (Test-Path $Src -PathType Container)) {
    Die "no adapter for platform '$Platform' at $Src"
}
if (-not (Test-Path (Join-Path $Src 'SHA256SUMS'))) {
    Die "missing $Src\SHA256SUMS (run tools/generate-adapters.py)"
}

$versionFile = Join-Path $RepoRoot 'VERSION'
$Version = if (Test-Path $versionFile) { (Get-Content $versionFile -Raw).Trim() } else { '0.0.0' }

switch ($PSCmdlet.ParameterSetName) {
    'Verify' { Invoke-VerifySource -Src $Src -Platform $Platform }
    'Resolve' { Invoke-Resolve -TargetDir $Dir -Platform $Platform }
    'Global' { Invoke-Install -Src $Src -Platform $Platform -Mode 'Global' -TargetDir $Dir -Version $Version }
    'Project' { Invoke-Install -Src $Src -Platform $Platform -Mode 'Project' -TargetDir $Dir -Version $Version }
    default { Die "unhandled mode: $($PSCmdlet.ParameterSetName)" }
}
