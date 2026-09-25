<#
.SYNOPSIS
  Cree une archive ZIP prete a deployer sur les PC CNSS (one-touch).
#>
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$OutZip = Join-Path (Split-Path $Root -Parent) ("SGRH-FingerprintBridge-Setup-" + (Get-Date -Format "yyyyMMdd") + ".zip")

if (-not (Test-Path (Join-Path $Root "payload\FingerprintBridge.exe"))) {
  & (Join-Path $Root "Build-Payload.ps1")
}

if (-not (Test-Path (Join-Path $Root "vendor\zk\libzkfpcsharp.dll"))) {
  Write-Warning "vendor\zk sans libzkfpcsharp.dll - le scan echouera sur les PC cibles."
}

if (Test-Path $OutZip) { Remove-Item $OutZip -Force }

Compress-Archive -Path @(
  (Join-Path $Root "INSTALLER.bat"),
  (Join-Path $Root "Setup-SgrhBridge.ps1"),
  (Join-Path $Root "UnSetup-SgrhBridge.ps1"),
  (Join-Path $Root "Build-Payload.ps1"),
  (Join-Path $Root "README.md"),
  (Join-Path $Root "payload"),
  (Join-Path $Root "vendor")
) -DestinationPath $OutZip -Force

Write-Host "Archive creee: $OutZip" -ForegroundColor Green
Write-Host "Sur le PC cible: dezipper puis double-cliquer INSTALLER.bat" -ForegroundColor Cyan

