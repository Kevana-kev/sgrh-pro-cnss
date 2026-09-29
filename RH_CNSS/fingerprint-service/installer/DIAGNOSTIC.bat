@echo off
:: Diagnostic rapide du bridge sur ce PC
cd /d "%~dp0"
title SGRH Pro - Diagnostic Bridge
echo.
echo === Diagnostic Fingerprint Bridge ===
echo.

echo [1] Processus FingerprintBridge :
tasklist /FI "IMAGENAME eq FingerprintBridge.exe" 2>nul | find /I "FingerprintBridge.exe" >nul
if errorlevel 1 (
  echo    NON DEMARRE
  echo    Lancement...
  if exist "%LOCALAPPDATA%\SGRH Pro\FingerprintBridge\Start-SgrhBridge.cmd" (
    call "%LOCALAPPDATA%\SGRH Pro\FingerprintBridge\Start-SgrhBridge.cmd"
  ) else if exist "%~dp0payload\FingerprintBridge.exe" (
    start "" /MIN "%~dp0payload\FingerprintBridge.exe" --headless
  ) else (
    echo    Introuvable. Relancez INSTALLER.bat
  )
  timeout /t 3 >nul
) else (
  echo    OK - en cours
)

echo.
echo [2] Test http://127.0.0.1:5002/status
powershell -NoProfile -Command "try { (Invoke-RestMethod 'http://127.0.0.1:5002/status' -TimeoutSec 3 | ConvertTo-Json -Compress) } catch { Write-Host 'ECHEC:' $_.Exception.Message }"

echo.
echo [3] Protocoles URL :
reg query "HKLM\SOFTWARE\Classes\sgrhbridge\shell\open\command" 2>nul
if errorlevel 1 echo    sgrhbridge:// NON enregistre - relancez INSTALLER.bat en admin

echo.
echo [4] DLL ZK :
if exist "%LOCALAPPDATA%\SGRH Pro\FingerprintBridge\libzkfpcsharp.dll" (
  echo    libzkfpcsharp.dll OK dans LocalAppData
) else if exist "%~dp0payload\libzkfpcsharp.dll" (
  echo    libzkfpcsharp.dll OK dans payload
) else if exist "%WINDIR%\SysWOW64\libzkfpcsharp.dll" (
  echo    libzkfpcsharp.dll OK dans SysWOW64
) else (
  echo    MANQUANTE - copiez vendor\zk\*.dll puis reinstallez
)

echo.
echo Sur le site Railway, ouvrez la page DEPUIS CE PC.
echo Chrome peut demander d'ouvrir FingerprintBridge : Autoriser.
echo.
pause
