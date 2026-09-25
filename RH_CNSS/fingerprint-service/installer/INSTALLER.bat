@echo off
:: ============================================================
::  SGRH Pro — Installation ONE-TOUCH Fingerprint Bridge
::  Double-clic = installation complete (UAC requis)
:: ============================================================
cd /d "%~dp0"
title SGRH Pro — Installation Bridge ZK-9500

net session >nul 2>&1
if %errorlevel% NEQ 0 (
  echo Elevation administrateur requise...
  powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
  exit /b
)

echo.
echo  ============================================
echo   SGRH Pro — Bridge biométrique (one-touch)
echo  ============================================
echo.

if not exist "%~dp0payload\FingerprintBridge.dll" (
  echo [1/2] Construction du payload...
  powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Build-Payload.ps1"
  if errorlevel 1 (
    echo ECHEC build payload.
    pause
    exit /b 1
  )
)

echo [2/2] Installation...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0Install-SgrhBridge.ps1"
if errorlevel 1 (
  echo ECHEC installation.
  pause
  exit /b 1
)

echo.
echo Ouvre http://127.0.0.1:5002/status pour verifier.
echo.
pause
