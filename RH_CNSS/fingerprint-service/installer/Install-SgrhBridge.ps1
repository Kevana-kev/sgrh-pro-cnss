#Requires -RunAsAdministrator
<#
.SYNOPSIS
  Installation one-touch — SGRH Pro Fingerprint Bridge (Windows)
.DESCRIPTION
  Installe le bridge ZK-9500, configure la clé API, démarre au logon,
  règle le pare-feu localhost et lance le service immédiatement.
#>
[CmdletBinding()]
param(
  [string]$InstallDir = "$env:ProgramFiles\SGRH Pro\FingerprintBridge",
  [string]$ApiKey = "local-secret-key",
  [int]$Port = 5002,
  [switch]$NoStart
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Payload = Join-Path $Root "payload"
$VendorZk = Join-Path $Root "vendor\zk"
$LogDir = Join-Path $env:ProgramData "SGRH Pro\FingerprintBridge"
$ConfigPath = Join-Path $LogDir "bridge.config.json"
$TaskName = "SGRH Fingerprint Bridge"
$LauncherName = "Start-SgrhBridge.cmd"

function Write-Step($msg) {
  Write-Host ""
  Write-Host "==> $msg" -ForegroundColor Cyan
}

function Assert-Payload {
  if (-not (Test-Path (Join-Path $Payload "FingerprintBridge.dll"))) {
    throw "Payload introuvable. Lance d'abord Build-Payload.ps1 (dossier installer\payload)."
  }
}

function Copy-Payload {
  Write-Step "Copie des fichiers vers $InstallDir"
  New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
  New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
  Copy-Item -Path (Join-Path $Payload "*") -Destination $InstallDir -Recurse -Force
}

function Install-ZkSdkFiles {
  Write-Step "Intégration SDK ZKTeco"
  $targets = @()
  $candidates = @()

  if (Test-Path $VendorZk) {
    $candidates += Get-ChildItem $VendorZk -File -ErrorAction SilentlyContinue
  }

  foreach ($name in @(
      "libzkfpcsharp.dll",
      "libzkfp.dll",
      "zkfp.dll",
      "libzkfpadapter.dll"
    )) {
    $sys = Join-Path $env:windir "SysWOW64\$name"
    if (Test-Path $sys) { $candidates += Get-Item $sys }
  }

  $copied = 0
  foreach ($f in ($candidates | Sort-Object FullName -Unique)) {
    if ($f.Extension -notin ".dll", ".so") { continue }
    Copy-Item $f.FullName -Destination (Join-Path $InstallDir $f.Name) -Force
    # Aussi en SysWOW64 si absents (nécessaire à certains loaders)
    $wow = Join-Path $env:windir "SysWOW64\$($f.Name)"
    if (-not (Test-Path $wow)) {
      try { Copy-Item $f.FullName -Destination $wow -Force; } catch { }
    }
    $copied++
    $targets += $f.Name
  }

  if ($copied -eq 0) {
    Write-Host "  [!] Aucune DLL ZK trouvée dans vendor\zk ni SysWOW64." -ForegroundColor Yellow
    Write-Host "      Place les DLL du SDK ZKFinger dans: $VendorZk" -ForegroundColor Yellow
    Write-Host "      Puis relance Install-SgrhBridge.ps1" -ForegroundColor Yellow
    $missing = $true
  } else {
    Write-Host "  DLL ZK copiées: $($targets -join ', ')" -ForegroundColor Green
    $missing = $false
  }
  return -not $missing
}

function Write-Config {
  Write-Step "Configuration bridge (clé API + port)"
  $cfg = [ordered]@{
    apiKey            = $ApiKey
    port              = $Port
    forceDevice       = $true
    allowMock         = $false
    installDir        = $InstallDir
    installedAt       = (Get-Date).ToString("o")
    laravelHint       = "BIOMETRIC_BRIDGE_URL=http://127.0.0.1:$Port ; BIOMETRIC_BRIDGE_API_KEY=$ApiKey"
  }
  ($cfg | ConvertTo-Json -Depth 4) | Set-Content -Path $ConfigPath -Encoding UTF8

  # Clé lisible aussi en env machine (pour tous les users)
  [Environment]::SetEnvironmentVariable("FINGERPRINT_BRIDGE_API_KEY", $ApiKey, "Machine")
  [Environment]::SetEnvironmentVariable("FINGERPRINT_BRIDGE_FORCE_DEVICE", "1", "Machine")
  [Environment]::SetEnvironmentVariable("FINGERPRINT_BRIDGE_ALLOW_MOCK", "0", "Machine")
  [Environment]::SetEnvironmentVariable("FINGERPRINT_BRIDGE_PORT", "$Port", "Machine")

  $env:FINGERPRINT_BRIDGE_API_KEY = $ApiKey
  $env:FINGERPRINT_BRIDGE_FORCE_DEVICE = "1"
  $env:FINGERPRINT_BRIDGE_ALLOW_MOCK = "0"

  # Stockage DPAPI LocalMachine attendu par HeadlessBridge (key.bin)
  $appData = Join-Path $env:ProgramData "FingerprintBridge"
  New-Item -ItemType Directory -Force -Path $appData | Out-Null
  # Headless utilise %AppData% utilisateur — on crée aussi un lanceur qui set l'env
}

function Write-ProtocolHandler {
  Write-Step "Enregistrement protocole web sgrhbridge:// (lancement depuis le site)"
  $exe = Join-Path $InstallDir "FingerprintBridge.exe"
  if (-not (Test-Path $exe)) {
    Write-Host "  [!] FingerprintBridge.exe introuvable — protocole non enregistré." -ForegroundColor Yellow
    return
  }

  # Commande : démarrage headless silencieux depuis Chrome/Edge
  $command = "`"$exe`" --headless --from-web `"%1`""

  foreach ($root in @(
      "HKLM:\SOFTWARE\Classes\sgrhbridge",
      "HKLM:\SOFTWARE\Classes\sgrh-fingerprint"
    )) {
    New-Item -Path $root -Force | Out-Null
    New-ItemProperty -Path $root -Name "(Default)" -Value "URL:SGRH Fingerprint Bridge" -PropertyType String -Force | Out-Null
    New-ItemProperty -Path $root -Name "URL Protocol" -Value "" -PropertyType String -Force | Out-Null
    New-Item -Path "$root\DefaultIcon" -Force | Out-Null
    New-ItemProperty -Path "$root\DefaultIcon" -Name "(Default)" -Value "`"$exe`",0" -PropertyType String -Force | Out-Null
    New-Item -Path "$root\shell\open\command" -Force | Out-Null
    New-ItemProperty -Path "$root\shell\open\command" -Name "(Default)" -Value $command -PropertyType String -Force | Out-Null
  }

  [Environment]::SetEnvironmentVariable("SGRH_BRIDGE_PROTOCOL", "sgrhbridge", "Machine")
  Write-Host "  Protocoles: sgrhbridge:// et sgrh-fingerprint://" -ForegroundColor Green
}

function Write-Launcher {
  Write-Step "Création du lanceur headless"
  $launcher = Join-Path $InstallDir $LauncherName
  $dotnetHost = Join-Path $InstallDir "FingerprintBridge.exe"
  if (-not (Test-Path $dotnetHost)) {
    # self-contained publish produces FingerprintBridge.exe
    $dotnetHost = "dotnet"
    $argsLine = "`"$InstallDir\FingerprintBridge.dll`" --headless"
  } else {
    $argsLine = "--headless"
  }

  $cmd = @"
@echo off
setlocal
set FINGERPRINT_BRIDGE_API_KEY=$ApiKey
set FINGERPRINT_BRIDGE_FORCE_DEVICE=1
set FINGERPRINT_BRIDGE_ALLOW_MOCK=0
cd /d "$InstallDir"
if exist "FingerprintBridge.exe" (
  start "SGRH Fingerprint Bridge" /MIN FingerprintBridge.exe --headless
) else (
  start "SGRH Fingerprint Bridge" /MIN dotnet FingerprintBridge.dll --headless
)
endlocal
"@
  Set-Content -Path $launcher -Value $cmd -Encoding ASCII

  # Raccourcis
  $wsh = New-Object -ComObject WScript.Shell
  $startup = [Environment]::GetFolderPath("CommonStartup")
  $desk = [Environment]::GetFolderPath("CommonDesktopDirectory")
  $startMenu = Join-Path $env:ProgramData "Microsoft\Windows\Start Menu\Programs\SGRH Pro"
  New-Item -ItemType Directory -Force -Path $startMenu | Out-Null

  foreach ($pair in @(
      @{ Path = (Join-Path $startup "SGRH Fingerprint Bridge.lnk"); Desc = "Démarrage auto" },
      @{ Path = (Join-Path $startMenu "Démarrer Fingerprint Bridge.lnk"); Desc = "Lancer le bridge" },
      @{ Path = (Join-Path $desk "SGRH Fingerprint Bridge.lnk"); Desc = "Lancer le bridge" }
    )) {
    $sc = $wsh.CreateShortcut($pair.Path)
    $sc.TargetPath = $launcher
    $sc.WorkingDirectory = $InstallDir
    $sc.Description = "SGRH Pro — Bridge biométrique ZK-9500 ($($pair.Desc))"
    $sc.Save()
  }

  # Tâche planifiée (filet de sécurité si startup échoue)
  schtasks /Delete /TN $TaskName /F 2>$null | Out-Null
  schtasks /Create /TN $TaskName /SC ONLOGON /RL HIGHEST /TR "`"$launcher`"" /F | Out-Null
  Write-Host "  Tâche planifiée: $TaskName" -ForegroundColor Green
}

function Set-FirewallRule {
  Write-Step "Règle pare-feu locale (port $Port)"
  $rule = "SGRH Fingerprint Bridge $Port"
  netsh advfirewall firewall delete rule name="$rule" 2>$null | Out-Null
  netsh advfirewall firewall add rule name="$rule" dir=in action=allow protocol=TCP localport=$Port profile=any | Out-Null
}

function Stop-OldBridge {
  Get-Process -Name "FingerprintBridge" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
  Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | ForEach-Object {
    try { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue } catch {}
  }
}

function Start-Bridge {
  if ($NoStart) { return }
  Write-Step "Démarrage du bridge"
  Stop-OldBridge
  $launcher = Join-Path $InstallDir $LauncherName
  Start-Process -FilePath $launcher -WorkingDirectory $InstallDir
  Start-Sleep -Seconds 3
  try {
    $status = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/status" -TimeoutSec 5
    Write-Host "  Bridge OK: $($status | ConvertTo-Json -Compress)" -ForegroundColor Green
  } catch {
    Write-Host "  Bridge démarré mais /status pas encore joignable: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host "  Vérifie le lecteur ZK-9500 et les DLL SDK." -ForegroundColor Yellow
  }
}

function Write-Uninstaller {
  $un = Join-Path $InstallDir "Uninstall-SgrhBridge.ps1"
  Copy-Item (Join-Path $Root "Uninstall-SgrhBridge.ps1") $un -Force -ErrorAction SilentlyContinue
}

# ── Main ─────────────────────────────────────────────────
Write-Host "============================================" -ForegroundColor Green
Write-Host " SGRH Pro — Installation Fingerprint Bridge" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green

Assert-Payload
Copy-Payload
$zkOk = Install-ZkSdkFiles
Write-Config
Write-Launcher
Write-ProtocolHandler
Set-FirewallRule
Write-Uninstaller
Start-Bridge

Write-Host ""
Write-Host "INSTALLATION TERMINÉE" -ForegroundColor Green
Write-Host "  Dossier     : $InstallDir"
Write-Host "  Config      : $ConfigPath"
Write-Host "  API Key     : $ApiKey"
Write-Host "  URL bridge  : http://127.0.0.1:$Port"
Write-Host "  Protocole   : sgrhbridge://start  (clic Empreinte sur le site web)"
Write-Host "  Laravel .env: BIOMETRIC_BRIDGE_API_KEY=$ApiKey"
if (-not $zkOk) {
  Write-Host ""
  Write-Host "ACTION REQUISE: copie les DLL ZKFinger dans:" -ForegroundColor Yellow
  Write-Host "  $VendorZk" -ForegroundColor Yellow
  Write-Host "  puis relance cet installateur." -ForegroundColor Yellow
}
Write-Host ""
