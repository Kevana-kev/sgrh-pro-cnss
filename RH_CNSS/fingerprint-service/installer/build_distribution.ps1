<#
Build a Windows distribution ZIP for the FingerprintBridge application.

Usage (run from repo root or provide -RepoRoot):
  .\build_distribution.ps1
  .\build_distribution.ps1 -RepoRoot 'C:\path\to\repo'

Preconditions:
- `dotnet` SDK must be installed and on PATH.
- Place vendor SDK DLLs into `fingerprint_service/vendor/` (not committed).
#>

param(
    [string]$RepoRoot = $(Get-Location),
    [string]$Configuration = "Release",
    [string]$Runtime = "win-x64"
)

Set-StrictMode -Version Latest

$RepoRoot = (Resolve-Path $RepoRoot).Path
Write-Host "Repo root: $RepoRoot"

$projectPath = Join-Path $RepoRoot 'fingerprint_service\APP_DESK\FingerprintBridge.csproj'
if (-not (Test-Path $projectPath)) {
    Write-Error "Project not found: $projectPath"
    exit 1
}

$publishDir = Join-Path $RepoRoot 'fingerprint_service\dist\publish'
if (Test-Path $publishDir) { Remove-Item $publishDir -Recurse -Force }
New-Item -ItemType Directory -Path $publishDir | Out-Null

Write-Host "Running dotnet publish..."
dotnet publish $projectPath -c $Configuration -r $Runtime --self-contained false -o $publishDir
if ($LASTEXITCODE -ne 0) { Write-Error "dotnet publish failed"; exit $LASTEXITCODE }

# Copy vendor DLLs (if any)
$vendorDir = Join-Path $RepoRoot 'fingerprint_service\vendor'
if (Test-Path $vendorDir) {
    Write-Host "Copying vendor files from $vendorDir"
    Get-ChildItem -Path $vendorDir -File | ForEach-Object {
        Copy-Item $_.FullName -Destination $publishDir -Force
    }
} else {
    Write-Host "No vendor directory found at $vendorDir (skip)"
}

# Add helper docs
Copy-Item (Join-Path $RepoRoot 'fingerprint_service\INSTALL_SDK.md') -Destination $publishDir -Force

# Create ZIP
$timestamp = Get-Date -Format 'yyyyMMddHHmm'
$zipPath = Join-Path $RepoRoot "fingerprint_service\dist\FingerprintBridge-$timestamp.zip"
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
Write-Host "Creating zip: $zipPath"
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory($publishDir, $zipPath)

Write-Host "Distribution created: $zipPath"
Write-Host "Next: copy the ZIP to target machines and run 'installer\install.ps1' on the target to install." 
