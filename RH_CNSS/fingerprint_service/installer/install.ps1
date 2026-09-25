<#
Install the FingerprintBridge distribution on a target machine.

Usage:
  .\install.ps1 -ZipPath 'C:\path\to\FingerprintBridge-202603251200.zip' -InstallDir 'C:\Program Files\FingerprintBridge' -CreateStartupShortcut

Options:
  -ZipPath : path to the distribution ZIP (defaults to the newest zip in ../dist)
  -InstallDir : installation folder (defaults to %ProgramFiles%\FingerprintBridge)
  -CreateStartupShortcut : create a shortcut in the current user's Startup folder to auto-run at login
  -SdkShare : optional UNC path where vendor DLLs can be copied from (e.g. \\share\sdk)
    -ProvisioningToken : optional one-time provisioning token to exchange for device credentials
    -ServerUrl : required when using -ProvisioningToken, the backend server URL (e.g. http://server:8000)
    -DeviceName : optional device name to send during provisioning (defaults to machine name)
#>

param(
    [string]$ZipPath = '',
    [string]$InstallDir = "$env:ProgramFiles\FingerprintBridge",
    [switch]$CreateStartupShortcut,
    [string]$SdkShare = ''
        , [string]$ProvisioningToken = ''
        , [string]$ServerUrl = ''
        , [string]$DeviceName = $env:COMPUTERNAME
        , [switch]$InstallAsService
        , [string]$ServiceName = 'FingerprintBridge'
)

Set-StrictMode -Version Latest

if (-not $ZipPath) {
    # pick newest zip in dist
    $distDir = Join-Path (Resolve-Path ..\..\).Path 'fingerprint_service\dist'
    if (-not (Test-Path $distDir)) { Write-Error "dist folder not found: $distDir"; exit 1 }
    $zips = Get-ChildItem -Path $distDir -Filter 'FingerprintBridge-*.zip' | Sort-Object LastWriteTime -Descending
    if (-not $zips) { Write-Error "No distribution zip found in $distDir"; exit 1 }
    $ZipPath = $zips[0].FullName
}

Write-Host "Using ZIP: $ZipPath"
Write-Host "Install dir: $InstallDir"

if (-not (Test-Path $ZipPath)) { Write-Error "Zip not found: $ZipPath"; exit 1 }

if (-not (Test-Path $InstallDir)) { New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null }

Write-Host "Extracting..."
Expand-Archive -Path $ZipPath -DestinationPath $InstallDir -Force

if ($SdkShare) {
    Write-Host "Copying SDK files from share: $SdkShare"
    try {
        Get-ChildItem -Path $SdkShare -File | ForEach-Object { Copy-Item $_.FullName -Destination $InstallDir -Force }
    } catch {
        Write-Warning "Failed to copy from share: $_"
    }
}

# Optionally create a startup shortcut for the current user
if ($CreateStartupShortcut) {
    $wsh = New-Object -ComObject WScript.Shell
    $startup = [Environment]::GetFolderPath('Startup')
    $exe = Get-ChildItem -Path $InstallDir -Filter '*.exe' | Select-Object -First 1
    if ($exe) {
        $lnkPath = Join-Path $startup 'FingerprintBridge.lnk'
        $shortcut = $wsh.CreateShortcut($lnkPath)
        $shortcut.TargetPath = $exe.FullName
        $shortcut.WorkingDirectory = $InstallDir
        $shortcut.Save()
        Write-Host "Startup shortcut created: $lnkPath"
    } else {
        Write-Warning "No executable found in $InstallDir to create a shortcut."
    }
}

# If requested, create a Windows Service that runs the bridge headless
if ($InstallAsService) {
    $exe = Get-ChildItem -Path $InstallDir -Filter '*.exe' | Select-Object -First 1
    if (-not $exe) {
        Write-Warning "No executable found in $InstallDir - cannot create service."
    } else {
        try {
            $svc = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
            if ($svc) {
                Write-Host "Service '$ServiceName' already exists. Attempting to stop and remove it."
                try { Stop-Service -Name $ServiceName -Force -ErrorAction SilentlyContinue } catch { }
                try { sc.exe delete $ServiceName | Out-Null } catch { }
                Start-Sleep -Seconds 1
            }

            $binary = "`"$($exe.FullName)`" --headless"
            Write-Host "Creating service '$ServiceName' -> $binary"
            New-Service -Name $ServiceName -BinaryPathName $binary -DisplayName $ServiceName -StartupType Automatic -ErrorAction Stop
            Write-Host "Service '$ServiceName' created. Starting service..."
            Start-Service -Name $ServiceName -ErrorAction Stop
            Write-Host "Service started."
        } catch {
            Write-Warning "Failed to create/start service '$ServiceName': $_"
        }
    }
}

Write-Host "Installation complete. Launch the application from: $InstallDir"
Write-Host "Remember to configure the server via POST /configure-server with the local API key (see INSTALL_SDK.md)."

# If a provisioning token is provided, attempt zero-touch provisioning:
if ($ProvisioningToken -and $ServerUrl) {
    Write-Host "Attempting zero-touch provisioning against $ServerUrl..."

    $exe = Get-ChildItem -Path $InstallDir -Filter '*.exe' | Select-Object -First 1
    if (-not $exe) {
        Write-Warning "No executable found in $InstallDir - cannot start bridge for provisioning."
    } else {
        $procName = [System.IO.Path]::GetFileNameWithoutExtension($exe.Name)
        if ($InstallAsService) {
            # If installed as a service, start the service (already attempted above)
            try {
                $svc = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
                if ($svc.Status -ne 'Running') { Start-Service -Name $ServiceName -ErrorAction SilentlyContinue }
                Write-Host "Bridge running as service: $ServiceName"
            } catch {
                Write-Warning "Could not start service $ServiceName: $_"
            }
        } else {
            $proc = Get-Process -Name $procName -ErrorAction SilentlyContinue
            if (-not $proc) {
                Write-Host "Starting bridge: $($exe.FullName)"
                Start-Process -FilePath $exe.FullName -WorkingDirectory $InstallDir | Out-Null
            } else {
                Write-Host "Bridge already running (process: $procName)."
            }
        }

        # Wait for local API to become available
        $maxWait = 30
        $waited = 0
        $statusOk = $false
        while ($waited -lt $maxWait) {
            try {
                $resp = Invoke-RestMethod -Uri 'http://localhost:5002/status' -Method Get -ErrorAction Stop
                if ($resp -and $resp.status -eq 'ok') { $statusOk = $true; break }
            } catch { }
            Start-Sleep -Seconds 1
            $waited++
        }

        if (-not $statusOk) {
            Write-Warning "Local bridge did not respond at http://localhost:5002 within $maxWait seconds. Provisioning skipped."
        } else {
            # Try to read local API key from AppData (DPAPI CurrentUser)
            $keyPath = Join-Path $env:APPDATA 'FingerprintBridge\key.bin'
            $apiKey = $null
            if (Test-Path $keyPath) {
                try {
                    $protectedBytes = [System.IO.File]::ReadAllBytes($keyPath)
                    $entropy = [System.Text.Encoding]::UTF8.GetBytes('FingerprintBridgeEntropy_v1')
                    $unprotected = [System.Security.Cryptography.ProtectedData]::Unprotect($protectedBytes, $entropy, [System.Security.Cryptography.DataProtectionScope]::LocalMachine)
                    $apiKey = [System.Text.Encoding]::UTF8.GetString($unprotected)
                    Write-Host "Recovered local API key from secure storage."
                } catch {
                    Write-Warning "Failed to unprotect local API key: $_"
                    $apiKey = $null
                }
            }

            # Fallback: attempt pair endpoint to obtain API key (will show approval UI)
            if (-not $apiKey) {
                Write-Host "Attempting pairing fallback to obtain API key (user approval may be required)."
                try {
                    $pairBody = @{ appName = 'Installer' } | ConvertTo-Json
                    $pairRes = Invoke-RestMethod -Uri 'http://localhost:5002/pair' -Method Post -Body $pairBody -ContentType 'application/json' -ErrorAction Stop
                    if ($pairRes -and $pairRes.apiKey) { $apiKey = $pairRes.apiKey; Write-Host 'Pairing returned API key.' }
                } catch {
                    Write-Warning "Pairing fallback failed: $_"
                }
            }

            if (-not $apiKey) {
                Write-Warning "Could not obtain local API key; provisioning aborted."
            } else {
                try {
                    $payload = @{ serverUrl = $ServerUrl; provisioningToken = $ProvisioningToken; name = $DeviceName; deviceUrl = 'http://localhost:5002' } | ConvertTo-Json
                    $headers = @{ 'X-API-KEY' = $apiKey }
                    Write-Host "Calling bridge configure-server to exchange provisioning token..."
                    $res = Invoke-RestMethod -Uri 'http://localhost:5002/configure-server' -Method Post -Headers $headers -Body $payload -ContentType 'application/json' -ErrorAction Stop
                    Write-Host "Provisioning response: $($res | ConvertTo-Json -Depth 5)"
                } catch {
                    Write-Warning "Provisioning call failed: $_"
                }
            }
        }
    }
}
