#Requires -RunAsAdministrator
<#
.SYNOPSIS
  Installation one-touch - SGRH Pro Fingerprint Bridge (Windows)
.DESCRIPTION
  Installe le bridge ZK-9500, configure la cle API, demarre au logon,
  regle le pare-feu localhost et lance le service immediatement.
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

function Write-Step {
  param([string]$Message)
  Write-Host ""
  Write-Host "==> $Message" -ForegroundColor Cyan
}

function Assert-Payload {
  if (-not (Test-Path (Join-Path $Payload "FingerprintBridge.dll"))) {
    throw "Payload introuvable. Lance d'abord Build-Payload.ps1 (dossier installer\payload)."
  }
}

function Stop-OldBridge {
  Write-Step "Arret des instances bridge existantes"
  Get-Process -Name "FingerprintBridge","dotnet" -ErrorAction SilentlyContinue | Where-Object {
    try {
      $_.Path -and ($_.Path -like "*FingerprintBridge*" -or $_.Path -like "*SGRH Pro*")
    } catch {
      $false
    }
  } | Stop-Process -Force -ErrorAction SilentlyContinue

  Get-Process -Name "FingerprintBridge" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue

  $prevEap = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | ForEach-Object {
    try {
      Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
    } catch {
    }
  }
  $ErrorActionPreference = $prevEap
  Start-Sleep -Seconds 1
}

function Copy-Payload {
  Write-Step "Copie des fichiers vers $InstallDir"
  Stop-OldBridge

  New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
  New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

  # Nettoyage cible (DLL souvent verrouillees si reinstall)
  $prevEap = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  if (Test-Path $InstallDir) {
    Get-ChildItem -Path $InstallDir -Force -ErrorAction SilentlyContinue | ForEach-Object {
      try {
        Remove-Item $_.FullName -Recurse -Force -ErrorAction Stop
      } catch {
        # Fichier verrouille: renommer pour liberer le chemin
        try {
          $bak = $_.FullName + ".old_" + (Get-Date -Format "HHmmss")
          Rename-Item $_.FullName $bak -Force -ErrorAction SilentlyContinue
        } catch {
        }
      }
    }
  }
  $ErrorActionPreference = $prevEap

  # Copie robuste (exclut projets SDK inutiles)
  & robocopy $Payload $InstallDir /E /R:3 /W:1 /NFL /NDL /NJH /NJS `
    /XD BiometricFinEnrolmentVerificationZkteco bridge standalone RegisterTool obj bin
  $rc = $LASTEXITCODE
  # robocopy: 0-7 = succes partiel/ok, >=8 = erreur
  if ($rc -ge 8) {
    throw "Echec copie payload (robocopy code $rc)."
  }

  if (-not (Test-Path (Join-Path $InstallDir "FingerprintBridge.dll")) -and
      -not (Test-Path (Join-Path $InstallDir "FingerprintBridge.exe"))) {
    throw "Copie incomplete: FingerprintBridge.exe/dll introuvable dans $InstallDir"
  }
}

function Install-ZkSdkFiles {
  Write-Step "Integration SDK ZKTeco"
  $targets = @()
  $candidates = @()

  if (Test-Path $VendorZk) {
    $candidates += Get-ChildItem $VendorZk -File -ErrorAction SilentlyContinue
  }

  foreach ($name in @("libzkfpcsharp.dll", "libzkfp.dll", "zkfp.dll", "libzkfpadapter.dll")) {
    $sys = Join-Path $env:windir "SysWOW64\$name"
    if (Test-Path $sys) {
      $candidates += Get-Item $sys
    }
  }

  $copied = 0
  foreach ($f in ($candidates | Sort-Object FullName -Unique)) {
    if ($f.Extension -notin @(".dll", ".so")) {
      continue
    }
    Copy-Item $f.FullName -Destination (Join-Path $InstallDir $f.Name) -Force
    $wow = Join-Path $env:windir "SysWOW64\$($f.Name)"
    if (-not (Test-Path $wow)) {
      try {
        Copy-Item $f.FullName -Destination $wow -Force
      } catch {
      }
    }
    $copied++
    $targets += $f.Name
  }

  if ($copied -eq 0) {
    Write-Host "  [!] Aucune DLL ZK trouvee dans vendor\zk ni SysWOW64." -ForegroundColor Yellow
    Write-Host "      Place les DLL du SDK ZKFinger dans: $VendorZk" -ForegroundColor Yellow
    Write-Host "      Puis relance Setup-SgrhBridge.ps1" -ForegroundColor Yellow
    return $false
  }

  Write-Host "  DLL ZK copiees: $($targets -join ', ')" -ForegroundColor Green
  return $true
}

function Write-Config {
  Write-Step "Configuration bridge (cle API + port)"
  $cfg = [ordered]@{
    apiKey      = $ApiKey
    port        = $Port
    forceDevice = $true
    allowMock   = $false
    installDir  = $InstallDir
    installedAt = (Get-Date).ToString("o")
    laravelHint = "BIOMETRIC_BRIDGE_URL=http://127.0.0.1:$Port ; BIOMETRIC_BRIDGE_API_KEY=$ApiKey"
  }
  ($cfg | ConvertTo-Json -Depth 4) | Set-Content -Path $ConfigPath -Encoding UTF8

  [Environment]::SetEnvironmentVariable("FINGERPRINT_BRIDGE_API_KEY", $ApiKey, "Machine")
  [Environment]::SetEnvironmentVariable("FINGERPRINT_BRIDGE_FORCE_DEVICE", "1", "Machine")
  [Environment]::SetEnvironmentVariable("FINGERPRINT_BRIDGE_ALLOW_MOCK", "0", "Machine")
  [Environment]::SetEnvironmentVariable("FINGERPRINT_BRIDGE_PORT", "$Port", "Machine")

  $env:FINGERPRINT_BRIDGE_API_KEY = $ApiKey
  $env:FINGERPRINT_BRIDGE_FORCE_DEVICE = "1"
  $env:FINGERPRINT_BRIDGE_ALLOW_MOCK = "0"

  $appData = Join-Path $env:ProgramData "FingerprintBridge"
  New-Item -ItemType Directory -Force -Path $appData | Out-Null
}

function Write-ProtocolHandler {
  Write-Step "Enregistrement protocole web sgrhbridge:// (lancement depuis le site)"
  $exe = Join-Path $InstallDir "FingerprintBridge.exe"
  if (-not (Test-Path $exe)) {
    Write-Host "  [!] FingerprintBridge.exe introuvable - protocole non enregistre." -ForegroundColor Yellow
    return
  }

  $command = '"' + $exe + '" --headless --from-web "%1"'

  foreach ($root in @("HKLM:\SOFTWARE\Classes\sgrhbridge", "HKLM:\SOFTWARE\Classes\sgrh-fingerprint")) {
    New-Item -Path $root -Force | Out-Null
    Set-ItemProperty -Path $root -Name "(default)" -Value "URL:SGRH Fingerprint Bridge" -Force
    New-ItemProperty -Path $root -Name "URL Protocol" -Value "" -PropertyType String -Force -ErrorAction SilentlyContinue | Out-Null
    if (-not (Get-ItemProperty -Path $root -Name "URL Protocol" -ErrorAction SilentlyContinue)) {
      New-ItemProperty -Path $root -Name "URL Protocol" -Value "" -PropertyType String -Force | Out-Null
    } else {
      Set-ItemProperty -Path $root -Name "URL Protocol" -Value "" -Force
    }

    $iconPath = Join-Path $root "DefaultIcon"
    New-Item -Path $iconPath -Force | Out-Null
    Set-ItemProperty -Path $iconPath -Name "(default)" -Value ('"' + $exe + '",0') -Force

    $cmdPath = Join-Path $root "shell\open\command"
    New-Item -Path $cmdPath -Force | Out-Null
    Set-ItemProperty -Path $cmdPath -Name "(default)" -Value $command -Force
  }

  [Environment]::SetEnvironmentVariable("SGRH_BRIDGE_PROTOCOL", "sgrhbridge", "Machine")
  Write-Host "  Protocoles: sgrhbridge:// et sgrh-fingerprint://" -ForegroundColor Green
}

function Write-Launcher {
  Write-Step "Creation du lanceur headless"
  $launcher = Join-Path $InstallDir $LauncherName

  $cmdLines = @(
    "@echo off",
    "setlocal",
    "set FINGERPRINT_BRIDGE_API_KEY=$ApiKey",
    "set FINGERPRINT_BRIDGE_FORCE_DEVICE=1",
    "set FINGERPRINT_BRIDGE_ALLOW_MOCK=0",
    ('cd /d "' + $InstallDir + '"'),
    'if exist "FingerprintBridge.exe" (',
    '  start "SGRH Fingerprint Bridge" /MIN FingerprintBridge.exe --headless',
    ") else (",
    '  start "SGRH Fingerprint Bridge" /MIN dotnet FingerprintBridge.dll --headless',
    ")",
    "endlocal"
  )
  Set-Content -Path $launcher -Value ($cmdLines -join "`r`n") -Encoding ASCII

  $wsh = New-Object -ComObject WScript.Shell
  $startup = [Environment]::GetFolderPath("CommonStartup")
  $desk = [Environment]::GetFolderPath("CommonDesktopDirectory")
  $startMenu = Join-Path $env:ProgramData "Microsoft\Windows\Start Menu\Programs\SGRH Pro"
  New-Item -ItemType Directory -Force -Path $startMenu | Out-Null

  $shortcuts = @(
    @{ Path = (Join-Path $startup "SGRH Fingerprint Bridge.lnk"); Desc = "Demarrage auto" },
    @{ Path = (Join-Path $startMenu "Demarrer Fingerprint Bridge.lnk"); Desc = "Lancer le bridge" },
    @{ Path = (Join-Path $desk "SGRH Fingerprint Bridge.lnk"); Desc = "Lancer le bridge" }
  )

  foreach ($pair in $shortcuts) {
    $sc = $wsh.CreateShortcut($pair.Path)
    $sc.TargetPath = $launcher
    $sc.WorkingDirectory = $InstallDir
    $sc.Description = "SGRH Pro - Bridge biometrique ZK-9500 ($($pair.Desc))"
    $sc.Save()
  }

  # schtasks /Delete echoue si la tache n'existe pas -> ne pas stopper l'install
  $prevEap = $ErrorActionPreference
  $ErrorActionPreference = "Continue"
  cmd /c "schtasks /Delete /TN `"$TaskName`" /F >nul 2>&1"
  cmd /c "schtasks /Create /TN `"$TaskName`" /SC ONLOGON /RL HIGHEST /TR `"\"$launcher\"`" /F >nul 2>&1"
  $taskOk = ($LASTEXITCODE -eq 0)
  $ErrorActionPreference = $prevEap
  if ($taskOk) {
    Write-Host "  Tache planifiee: $TaskName" -ForegroundColor Green
  } else {
    Write-Host "  [!] Tache planifiee non creee (raccourci Startup suffit)." -ForegroundColor Yellow
  }
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
  if ($NoStart) {
    return
  }
  Write-Step "Demarrage du bridge"
  Stop-OldBridge
  $launcher = Join-Path $InstallDir $LauncherName
  Start-Process -FilePath $launcher -WorkingDirectory $InstallDir
  Start-Sleep -Seconds 3
  try {
    $status = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/status" -TimeoutSec 5
    Write-Host ("  Bridge OK: " + ($status | ConvertTo-Json -Compress)) -ForegroundColor Green
  } catch {
    Write-Host ("  Bridge demarre mais /status pas encore joignable: " + $_.Exception.Message) -ForegroundColor Yellow
    Write-Host "  Verifie le lecteur ZK-9500 et les DLL SDK." -ForegroundColor Yellow
  }
}

function Write-Uninstaller {
  $un = Join-Path $InstallDir "UnSetup-SgrhBridge.ps1"
  Copy-Item (Join-Path $Root "UnSetup-SgrhBridge.ps1") $un -Force -ErrorAction SilentlyContinue
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

