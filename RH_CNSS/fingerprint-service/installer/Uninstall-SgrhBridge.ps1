#Requires -RunAsAdministrator
<#
.SYNOPSIS
  Désinstalle SGRH Fingerprint Bridge
#>
$ErrorActionPreference = "Continue"
$InstallDir = "$env:ProgramFiles\SGRH Pro\FingerprintBridge"
$TaskName = "SGRH Fingerprint Bridge"
$Port = 5002

Write-Host "Désinstallation SGRH Fingerprint Bridge..." -ForegroundColor Cyan

Get-Process -Name "FingerprintBridge" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
schtasks /Delete /TN $TaskName /F 2>$null | Out-Null
netsh advfirewall firewall delete rule name="SGRH Fingerprint Bridge $Port" 2>$null | Out-Null

Remove-Item "HKLM:\SOFTWARE\Classes\sgrhbridge" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "HKLM:\SOFTWARE\Classes\sgrh-fingerprint" -Recurse -Force -ErrorAction SilentlyContinue

$startup = [Environment]::GetFolderPath("CommonStartup")
$desk = [Environment]::GetFolderPath("CommonDesktopDirectory")
$startMenu = Join-Path $env:ProgramData "Microsoft\Windows\Start Menu\Programs\SGRH Pro"
Remove-Item (Join-Path $startup "SGRH Fingerprint Bridge.lnk") -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $desk "SGRH Fingerprint Bridge.lnk") -Force -ErrorAction SilentlyContinue
Remove-Item $startMenu -Recurse -Force -ErrorAction SilentlyContinue

[Environment]::SetEnvironmentVariable("FINGERPRINT_BRIDGE_API_KEY", $null, "Machine")
[Environment]::SetEnvironmentVariable("FINGERPRINT_BRIDGE_FORCE_DEVICE", $null, "Machine")
[Environment]::SetEnvironmentVariable("FINGERPRINT_BRIDGE_ALLOW_MOCK", $null, "Machine")
[Environment]::SetEnvironmentVariable("FINGERPRINT_BRIDGE_PORT", $null, "Machine")
[Environment]::SetEnvironmentVariable("SGRH_BRIDGE_PROTOCOL", $null, "Machine")

if (Test-Path $InstallDir) {
  Remove-Item $InstallDir -Recurse -Force -ErrorAction SilentlyContinue
}

Write-Host "Terminé." -ForegroundColor Green
