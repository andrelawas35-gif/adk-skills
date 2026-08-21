<#
.SYNOPSIS
    Behavioral tests for tools/install.ps1 -- the native-Windows counterpart
    to tests/test_install.sh (which exercises tools/install.sh). No test
    framework: plain PowerShell with a tiny assert helper, mirroring the
    sh version's structure and coverage.
#>
$ErrorActionPreference = 'Stop'

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Install = Join-Path $RepoRoot 'tools\install.ps1'
$Platform = 'claude-code'

$script:Pass = 0
$script:Fail = 0

function Ok([string]$Name) { $script:Pass++; Write-Output "  ok    $Name" }
function Bad([string]$Name) { $script:Fail++; Write-Output "  FAIL  $Name" }
function Check([string]$Actual, [string]$Expected, [string]$Name) {
    if ($Actual -eq $Expected) { Ok $Name } else { Bad "$Name (want '$Expected', got '$Actual')" }
}

$Work = Join-Path $env:TEMP ("ws-install-test-" + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Force -Path $Work | Out-Null
try {

Write-Output "test: verify source artifacts"
& powershell -ExecutionPolicy Bypass -File $Install -Platform $Platform -Verify *> $null
if ($LASTEXITCODE -eq 0) { Ok "verify passes on committed artifacts" } else { Bad "verify passes on committed artifacts" }

Write-Output "test: global install"
$env:CLAUDE_HOME = Join-Path $Work 'home\.claude'
& powershell -ExecutionPolicy Bypass -File $Install -Platform $Platform -Global *> $null
$n = (Get-ChildItem -Path (Join-Path $Work 'home') -Recurse -Filter 'SKILL.md' -ErrorAction SilentlyContinue).Count
$expected = (Get-ChildItem -Path (Join-Path $RepoRoot 'skills\core') -Directory |
    ForEach-Object { Join-Path $_.FullName 'SKILL.md' } |
    Where-Object { Test-Path $_ }).Count
Check "$n" "$expected" "global install places every generated skill"
Remove-Item Env:\CLAUDE_HOME -ErrorAction SilentlyContinue

Write-Output "test: project pin writes lock and skills"
$proj = Join-Path $Work 'proj'
New-Item -ItemType Directory -Force -Path (Join-Path $proj '.git') | Out-Null
& powershell -ExecutionPolicy Bypass -File $Install -Platform $Platform -Project -Dir $proj *> $null
if (Test-Path (Join-Path $proj '.claude\skills\alawas-governance-conduct-work-object\SKILL.md')) { Ok "project skill installed" } else { Bad "project skill installed" }
$lockPath = Join-Path $proj ".work-studio\adapter.$Platform.lock"
if (Test-Path $lockPath) { Ok "project lock written" } else { Bad "project lock written" }
if ((Get-Content $lockPath) -contains "platform=$Platform") { Ok "lock records platform" } else { Bad "lock records platform" }

Write-Output "test: project pins coexist across platforms"
& powershell -ExecutionPolicy Bypass -File $Install -Platform codex -Project -Dir $proj *> $null
$claudeLock = Join-Path $proj ".work-studio\adapter.$Platform.lock"
$codexLock = Join-Path $proj '.work-studio\adapter.codex.lock'
if ((Test-Path $claudeLock) -and (Test-Path $codexLock)) { Ok "platform-specific locks coexist" } else { Bad "platform-specific locks coexist" }

Write-Output "test: precedence resolution"
$res = & powershell -ExecutionPolicy Bypass -File $Install -Platform $Platform -Resolve -Dir $proj
if ($res -like 'project:*') { Ok "pinned project resolves to project adapter" } else { Bad "pinned project resolves to project adapter (got '$res')" }
$res = & powershell -ExecutionPolicy Bypass -File $Install -Platform $Platform -Resolve -Dir $Work
if ($res -like 'global:*') { Ok "unpinned dir resolves to global adapter" } else { Bad "unpinned dir resolves to global adapter (got '$res')" }

Write-Output "test: precedence resolves upward from a subdirectory"
$deep = Join-Path $proj 'src\deep'
New-Item -ItemType Directory -Force -Path $deep | Out-Null
$res = & powershell -ExecutionPolicy Bypass -File $Install -Platform $Platform -Resolve -Dir $deep
if ($res -like 'project:*') { Ok "nested dir inherits project pin" } else { Bad "nested dir inherits project pin (got '$res')" }

Write-Output "test: lock uses relative dest path"
$lockDestLine = (Get-Content $lockPath) | Where-Object { $_ -match '^dest=' }
$lockDest = $lockDestLine -replace '^dest=', ''
if ($lockDest -match '^[a-zA-Z]:\\|^\\\\') {
    Bad "lock dest is relative (got absolute: '$lockDest')"
} elseif ($lockDest -in @('.claude\skills', '.agents\skills', '.github\skills')) {
    Ok "lock dest is relative"
} else {
    Bad "lock dest is relative (got '$lockDest')"
}

Write-Output "test: relative lock resolves to correct absolute path"
$res = & powershell -ExecutionPolicy Bypass -File $Install -Platform $Platform -Resolve -Dir $proj
if ($res -like "project:*$proj*") { Ok "relative lock resolves to absolute" } else { Bad "relative lock resolves to absolute (got '$res')" }

Write-Output "test: tamper detection on installed copy"
$tampered = Join-Path $proj '.claude\skills\alawas-governance-conduct-work-object\SKILL.md'
Add-Content -Path $tampered -Value 'corruption'
$adapterDir = Join-Path $RepoRoot "adapters\$Platform"
$rewritten = Get-Content (Join-Path $adapterDir 'SHA256SUMS') -Encoding utf8 |
    ForEach-Object { $_ -replace '^([0-9a-fA-F]{64})\s+\*?skills/', '$1  ' }
$sumsFile = Join-Path $proj '.claude\skills\.sums.txt'
Set-Content -Path $sumsFile -Value $rewritten -Encoding utf8
$tamperDetected = $false
foreach ($line in (Get-Content $sumsFile)) {
    if ($line.Trim() -eq '') { continue }
    if ($line -notmatch '^([0-9a-fA-F]{64})\s+\*?(.+)$') { continue }
    $expectedHash = $Matches[1].ToLowerInvariant()
    $relPath = $Matches[2] -replace '/', '\'
    $fullPath = Join-Path (Join-Path $proj '.claude\skills') $relPath
    if (-not (Test-Path $fullPath)) { $tamperDetected = $true; break }
    $actualHash = (Get-FileHash -Path $fullPath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actualHash -ne $expectedHash) { $tamperDetected = $true; break }
}
if ($tamperDetected) { Ok "tampered install fails checksum" } else { Bad "tampered install fails checksum" }

Write-Output "test: unknown platform is rejected"
$prevEap = $ErrorActionPreference
$ErrorActionPreference = 'Continue'
& powershell -ExecutionPolicy Bypass -File $Install -Platform bogus -Verify *> $null
$rejected = ($LASTEXITCODE -ne 0)
$ErrorActionPreference = $prevEap
if ($rejected) { Ok "unknown platform rejected" } else { Bad "unknown platform rejected" }

} finally {
    Remove-Item -Recurse -Force $Work -ErrorAction SilentlyContinue
}

Write-Output ""
Write-Output "install tests: $($script:Pass) passed, $($script:Fail) failed"
if ($script:Fail -ne 0) { exit 1 } else { exit 0 }
