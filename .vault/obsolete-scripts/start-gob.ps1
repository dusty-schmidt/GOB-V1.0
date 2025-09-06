# Universal GOB Starter - Auto-detects platform
param(
    [switch]$Force
)

$ErrorActionPreference = "SilentlyContinue"

Write-Host "🚀 GOB Universal Starter" -ForegroundColor Green

# Detect platform and run appropriate script
if ($IsWindows -or $env:OS -eq "Windows_NT" -or !$PSVersionTable.Platform) {
    Write-Host "🖥️ Windows detected" -ForegroundColor Cyan
    if (Test-Path "scripts\windows\run-gob-docker.ps1") {
        & "scripts\windows\run-gob-docker.ps1"
    } else {
        Write-Host "❌ Windows script not found at scripts\windows\run-gob-docker.ps1" -ForegroundColor Red
        exit 1
    }
} elseif ($IsLinux -or $IsMacOS) {
    Write-Host "🐧 Linux/Unix detected" -ForegroundColor Cyan
    if (Test-Path "scripts/linux/run-gob-docker.sh") {
        chmod +x "scripts/linux/run-gob-docker.sh"
        & "scripts/linux/run-gob-docker.sh"
    } else {
        Write-Host "❌ Linux script not found at scripts/linux/run-gob-docker.sh" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "❌ Unable to detect platform" -ForegroundColor Red
    Write-Host "ℹ️ Run platform-specific scripts manually:" -ForegroundColor Yellow
    Write-Host "   Windows: scripts\windows\run-gob-docker.ps1" -ForegroundColor Gray
    Write-Host "   Linux:   scripts/linux/run-gob-docker.sh" -ForegroundColor Gray
    exit 1
}
