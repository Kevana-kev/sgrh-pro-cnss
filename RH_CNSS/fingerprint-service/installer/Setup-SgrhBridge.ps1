#Requires -RunAsAdministrator
<#
.SYNOPSIS
  Installation one-touch - SGRH Pro Fingerprint Bridge (Windows)
#>
[CmdletBinding()]
param(
  # LocalAppData = moins de conflits ACL / antivirus que Program Files
  [string]$InstallDir = "$env:LOCALAPPDATA\SGRH Pro\FingerprintBridge",
  [string]$ApiKey = "local-secret-key",
  [int]$Port = 5002,
  [switch]$NoStart,
  [switch]$InPlace
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Payload = Join-Path $Root "payload"
$VendorZk = Join-Path $Root "vendor\zk"
$LogDir = Join-Path $env:ProgramData "SGRH Pro\FingerprintBridge"
$ConfigPath = Join-Path $LogDir "bridge.config.json"
$TaskName = "SGRH Fingerprint Bridge"
$LauncherName = "Start-SgrhBridge.cmd"
$script:EffectiveInstallDir = $InstallDir

function Write-Step {
  param([string]$Message)
  Write-Host ""
  Write-Host "==> $Message" -ForegroundColor Cyan
}

function Assert-Payload {
  $dll = Join-Path $Payload "FingerprintBridge.dll"
  $exe = Join-Path $Payload "FingerprintBridge.exe"
  if (-not (Test-Path $dll) -and -not (Test-Path $exe)) {
    throw "Payload introuvable. Lance d'abord Build-Payload.ps1 (dossier installer\payload)."
  }
}

function Stop-OldBridge {
  Write-Step "Arret des instances bridge existantes"
  $prevEap = $ErrorActionPreference
  $ErrorActionPreference = "Continue"

  cmd /c "taskkill /F /IM FingerprintBridge.exe >nul 2>&1"
  cmd /c "taskkill /F /IM FingerprintBridge.dll >nul 2>&1"

  Get-Process -ErrorAction SilentlyContinue | ForEach-Object {
    $p = $_
    try {
      $path = $p.Path
      if ($path -and (
          $path -like "*FingerprintBridge*" -or
          $path -like "*SGRH Pro*" -or
          $path -like "*fingerprint-service*payload*"
        )) {
        Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
      }
    } catch {}
  }

  Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | ForEach-Object {
    try { Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue } catch {}
  }

  $ErrorActionPreference = $prevEap
  Start-Sleep -Seconds 3
}

function Test-BridgeBinaries {
  param([string]$Dir)
  return (Test-Path (Join-Path $Dir "FingerprintBridge.exe")) -or
         (Test-Path (Join-Path $Dir "FingerprintBridge.dll"))
}

function Copy-Payload {
  Write-Step "Preparation du dossier d'installation"
  Stop-OldBridge
  New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

  if ($InPlace) {
    $script:EffectiveInstallDir = $Payload
    Write-Host "  Mode in-place: utilisation directe de $Payload" -ForegroundColor Yellow
    return
  }

  $prevEap = $ErrorActionPreference
  $ErrorActionPreference = "Continue"

  # Deplacer l'ancienne install si presente
  if (Test-Path $script:EffectiveInstallDir) {
    $backup = "$($script:EffectiveInstallDir).bak_" + (Get-Date -Format "yyyyMMdd_HHmmss")
    try {
      Move-Item -Path $script:EffectiveInstallDir -Destination $backup -Force -ErrorAction Stop
      Write-Host "  Ancienne install deplacee" -ForegroundColor DarkGray
    } catch {
      try { Remove-Item $script:EffectiveInstallDir -Recurse -Force -ErrorAction SilentlyContinue } catch {}
    }
  }

  New-Item -ItemType Directory -Force -Path $script:EffectiveInstallDir | Out-Null
  Get-ChildItem -Path $Payload -Recurse -File -ErrorAction SilentlyContinue | Unblock-File -ErrorAction SilentlyContinue

  # Etape 1: staging dans %TEMP% (evite locks Program Files)
  $stage = Join-Path $env:TEMP ("sgrh-bridge-stage-" + [guid]::NewGuid().ToString("N").Substring(0, 8))
  New-Item -ItemType Directory -Force -Path $stage | Out-Null

  Write-Host "  Staging: $stage" -ForegroundColor DarkGray
  & robocopy $Payload $stage /E /R:0 /W:0 /NFL /NDL /NJH /NJS `
    /XD BiometricFinEnrolmentVerificationZkteco bridge standalone RegisterTool obj bin `
    /XF libzkfpcsharp.dll libzkfp.dll zkfp.dll libzkfpadapter.dll *.pdb | Out-Null
  $rc1 = $LASTEXITCODE

  # Etape 2: staging -> install
  & robocopy $stage $script:EffectiveInstallDir /E /R:1 /W:1 /NFL /NDL /NJH /NJS | Out-Null
  $rc2 = $LASTEXITCODE

  try { Remove-Item $stage -Recurse -Force -ErrorAction SilentlyContinue } catch {}

  $ErrorActionPreference = $prevEap

  if (Test-BridgeBinaries $script:EffectiveInstallDir) {
    if ($rc1 -ge 8 -or $rc2 -ge 8) {
      Write-Host "  Copie partielle OK (binaires presents)." -ForegroundColor Yellow
    }
    return
  }

  # Fallback ultime: installer in-place depuis payload (fichiers deja la)
  Write-Host "  Copie impossible (fichiers verrouilles). Fallback in-place payload." -ForegroundColor Yellow
  $script:EffectiveInstallDir = $Payload
  if (-not (Test-BridgeBinaries $script:EffectiveInstallDir)) {
    throw "Impossible d'installer: FingerprintBridge.exe/dll inaccessibles (ferme le bridge / antivirus)."
  }
}

function Install-ZkSdkFiles {
  Write-Step "Integration SDK ZKTeco"
  $dir = $script:EffectiveInstallDir
  $targets = @()
  $searchDirs = @($VendorZk, $Payload, (Join-Path $env:windir "SysWOW64"), $dir)

  foreach ($name in @("libzkfpcsharp.dll", "libzkfp.dll", "zkfp.dll", "libzkfpadapter.dll")) {
    $dest = Join-Path $dir $name
    if (Test-Path $dest) {
      $targets += "$name (ok)"
      continue
    }

    $srcFile = $null
    foreach ($d in $searchDirs) {
      $candidate = Join-Path $d $name
      if ((Test-Path $candidate) -and ($candidate -ne $dest)) {
        $srcFile = $candidate
        break
      }
    }
    if (-not $srcFile) { continue }

    try {
      Unblock-File -Path $srcFile -ErrorAction SilentlyContinue
      Copy-Item -LiteralPath $srcFile -Destination $dest -Force -ErrorAction Stop
      $targets += $name
    } catch {
      Write-Host ("  [!] $name non copie: " + $_.Exception.Message) -ForegroundColor Yellow
    }
  }

  if ($targets.Count -eq 0) {
    Write-Host "  [!] Aucune DLL ZK trouvee. Place-les dans: $VendorZk" -ForegroundColor Yellow
    return $false
  }

  Write-Host "  DLL ZK: $($targets -join ', ')" -ForegroundColor Green
  return $true
}

function Write-Config {
  Write-Step "Configuration bridge (cle API + port)"
  $dir = $script:EffectiveInstallDir
  $cfg = [ordered]@{
    apiKey      = $ApiKey
    port        = $Port
    forceDevice = $true
    allowMock   = $false
    installDir  = $dir
    installedAt = (Get-Date).ToString("o")
    laravelHint = "BIOMETRIC_BRIDGE_URL=http://127.0.0.1:$Port ; BIOMETRIC_BRIDGE_API_KEY=$ApiKey"
  }
  ($cfg | ConvertTo-Json -Depth 4) | Set-Content -Path $ConfigPath -Encoding UTF8

  [Environment]::SetEnvironmentVariable("FINGERPRINT_BRIDGE_API_KEY", $ApiKey, "Machine")
  [Environment]::SetEnvironmentVariable("FINGERPRINT_BRIDGE_FORCE_DEVICE", "1", "Machine")
  [Environment]::SetEnvironmentVariable("FINGERPRINT_BRIDGE_ALLOW_MOCK", "0", "Machine")
  [Environment]::SetEnvironmentVariable("FINGERPRINT_BRIDGE_PORT", "$Port", "Machine")
  [Environment]::SetEnvironmentVariable("SGRH_BRIDGE_INSTALL_DIR", $dir, "Machine")

  $env:FINGERPRINT_BRIDGE_API_KEY = $ApiKey
  $env:FINGERPRINT_BRIDGE_FORCE_DEVICE = "1"
  $env:FINGERPRINT_BRIDGE_ALLOW_MOCK = "0"

  New-Item -ItemType Directory -Force -Path (Join-Path $env:ProgramData "FingerprintBridge") | Out-Null
}

function Write-ProtocolHandler {
  Write-Step "Enregistrement protocole web sgrhbridge://"
  $dir = $script:EffectiveInstallDir
  $exe = Join-Path $dir "FingerprintBridge.exe"
  if (-not (Test-Path $exe)) {
    Write-Host "  [!] FingerprintBridge.exe introuvable - protocole non enregistre." -ForegroundColor Yellow
    return
  }

  $command = '"' + $exe + '" --headless --from-web "%1"'

  foreach ($root in @("HKLM:\SOFTWARE\Classes\sgrhbridge", "HKLM:\SOFTWARE\Classes\sgrh-fingerprint")) {
    New-Item -Path $root -Force | Out-Null
    Set-ItemProperty -Path $root -Name "(default)" -Value "URL:SGRH Fingerprint Bridge" -Force
    if (-not (Get-ItemProperty -Path $root -Name "URL Protocol" -ErrorAction SilentlyContinue)) {
      New-ItemProperty -Path $root -Name "URL Protocol" -Value "" -PropertyType String -Force | Out-Null
    } else {
      Set-ItemProperty -Path $root -Name "URL Protocol" -Value "" -Force
    }
    New-Item -Path (Join-Path $root "DefaultIcon") -Force | Out-Null
    Set-ItemProperty -Path (Join-Path $root "DefaultIcon") -Name "(default)" -Value ('"' + $exe + '",0') -Force
    New-Item -Path (Join-Path $root "shell\open\command") -Force | Out-Null
    Set-ItemProperty -Path (Join-Path $root "shell\open\command") -Name "(default)" -Value $command -Force
  }

  [Environment]::SetEnvironmentVariable("SGRH_BRIDGE_PROTOCOL", "sgrhbridge", "Machine")
  Write-Host "  Protocoles OK -> $exe" -ForegroundColor Green
}

function Write-Launcher {
  Write-Step "Creation du lanceur headless"
  $dir = $script:EffectiveInstallDir
  $launcher = Join-Path $dir $LauncherName

  $cmdLines = @(
    "@echo off",
    "setlocal",
    "set FINGERPRINT_BRIDGE_API_KEY=$ApiKey",
    "set FINGERPRINT_BRIDGE_FORCE_DEVICE=1",
    "set FINGERPRINT_BRIDGE_ALLOW_MOCK=0",
    ('cd /d "' + $dir + '"'),
    'if exist "FingerprintBridge.exe" (',
    '  start "SGRH Fingerprint Bridge" /MIN FingerprintBridge.exe --headless',
    ") else (",
    '  start "SGRH Fingerprint Bridge" /MIN dotnet FingerprintBridge.dll --headless',
    ")",
    "endlocal"
  )
  Set-Content -Path $launcher -Value ($cmdLines -join "`r`n") -Encoding ASCII

  $wsh = New-Object -ComObject WScript.Shell
  $startup = [Environment]::GetFolderPath("Startup")
  $desk = [Environment]::GetFolderPath("Desktop")
  $startMenu = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs\SGRH Pro"
  New-Item -ItemType Directory -Force -Path $startMenu | Out-Null

  foreach ($pair in @(
      @{ Path = (Join-Path $startup "SGRH Fingerprint Bridge.lnk"); Desc = "Demarrage auto" },
      @{ Path = (Join-Path $startMenu "Demarrer Fingerprint Bridge.lnk"); Desc = "Lancer" },
      @{ Path = (Join-Path $desk "SGRH Fingerprint Bridge.lnk"); Desc = "Bureau" }
    )) {
    $sc = $wsh.CreateShortcut($pair.Path)
    $sc.TargetPath = $launcher
    $sc.WorkingDirectory = $dir
    $sc.Description = "SGRH Pro Bridge ZK-9500 ($($pair.Desc))"
    $sc.Save()
  }

  $prevEap = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  cmd /c "schtasks /Delete /TN `"$TaskName`" /F >nul 2>&1"
  cmd /c "schtasks /Create /TN `"$TaskName`" /SC ONLOGON /RL LIMITED /TR `"\"$launcher\"`" /F >nul 2>&1"
  $ErrorActionPreference = $prevEap
  Write-Host "  Lanceur: $launcher" -ForegroundColor Green
}

function Set-FirewallRule {
  Write-Step "Regle pare-feu locale (port $Port)"
  $rule = "SGRH Fingerprint Bridge $Port"
  $prevEap = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  cmd /c "netsh advfirewall firewall delete rule name=`"$rule`" >nul 2>&1"
  cmd /c "netsh advfirewall firewall add rule name=`"$rule`" dir=in action=allow protocol=TCP localport=$Port profile=any >nul 2>&1"
  $ErrorActionPreference = $prevEap
}

function Start-Bridge {
  if ($NoStart) { return }
  Write-Step "Demarrage du bridge"
  Stop-OldBridge
  $launcher = Join-Path $script:EffectiveInstallDir $LauncherName
  if (-not (Test-Path $launcher)) {
    Write-Host "  Lanceur introuvable." -ForegroundColor Yellow
    return
  }
  Start-Process -FilePath $launcher -WorkingDirectory $script:EffectiveInstallDir
  Start-Sleep -Seconds 4
  try {
    $status = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/status" -TimeoutSec 5
    Write-Host ("  Bridge OK: " + ($status | ConvertTo-Json -Compress)) -ForegroundColor Green
  } catch {
    Write-Host ("  Bridge demarre mais /status pas joignable: " + $_.Exception.Message) -ForegroundColor Yellow
  }
}

function Write-Uninstaller {
  $src = Join-Path $Root "Uninstall-SgrhBridge.ps1"
  $dst = Join-Path $script:EffectiveInstallDir "Uninstall-SgrhBridge.ps1"
  if ((Test-Path $src) -and ($script:EffectiveInstallDir -ne $Payload)) {
    Copy-Item $src $dst -Force -ErrorAction SilentlyContinue
  }
}

Write-Host "============================================" -ForegroundColor Green
Write-Host " SGRH Pro - Installation Fingerprint Bridge" -ForegroundColor Green
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
Write-Host "INSTALLATION TERMINEE" -ForegroundColor Green
Write-Host "  Dossier     : $($script:EffectiveInstallDir)"
Write-Host "  Config      : $ConfigPath"
Write-Host "  API Key     : $ApiKey"
Write-Host "  URL bridge  : http://127.0.0.1:$Port"
Write-Host "  Protocole   : sgrhbridge://start"
if (-not $zkOk) {
  Write-Host ""
  Write-Host "ACTION REQUISE: DLL ZK dans $VendorZk puis relancer." -ForegroundColor Yellow
}
Write-Host ""
