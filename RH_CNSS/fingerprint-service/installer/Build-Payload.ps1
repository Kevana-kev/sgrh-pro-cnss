<#
.SYNOPSIS
  Compile le payload self-contained win-x86 du bridge (à lancer une fois avant distribution).
#>
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Proj = Join-Path $Root "..\APP_DESK\FingerprintBridge.csproj"
$Out = Join-Path $Root "payload"

Write-Host "Publication self-contained win-x86 → $Out" -ForegroundColor Cyan
New-Item -ItemType Directory -Force -Path $Out | Out-Null

dotnet publish $Proj `
  -c Release `
  -r win-x86 `
  --self-contained true `
  -p:PublishSingleFile=false `
  -p:IncludeNativeLibrariesForSelfExtract=true `
  -o $Out

if ($LASTEXITCODE -ne 0) { throw "dotnet publish a échoué ($LASTEXITCODE)" }

# Copier DLL ZK si présentes sur la machine de build
$vendor = Join-Path $Root "vendor\zk"
New-Item -ItemType Directory -Force -Path $vendor | Out-Null
foreach ($name in @("libzkfpcsharp.dll", "libzkfp.dll", "zkfp.dll")) {
  $src = Join-Path $env:windir "SysWOW64\$name"
  if (Test-Path $src) {
    Copy-Item $src (Join-Path $vendor $name) -Force
    Copy-Item $src (Join-Path $Out $name) -Force
    Write-Host "  + $name (depuis SysWOW64)" -ForegroundColor Green
  }
}

Write-Host "Payload prêt." -ForegroundColor Green
Get-ChildItem $Out | Select-Object Name, Length | Format-Table -AutoSize
