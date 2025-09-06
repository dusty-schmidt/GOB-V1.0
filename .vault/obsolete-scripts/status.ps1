# Universal GOB Status Checker - Auto-detects platform
$ErrorActionPreference = "SilentlyContinue"

Write-Host "🔍 GOB Universal Status Checker" -ForegroundColor Green

# Detect platform and run appropriate script
if ($IsWindows -or $env:OS -eq "Windows_NT" -or !$PSVersionTable.Platform) {
    Write-Host "🖥️ Windows detected" -ForegroundColor Cyan
    if (Test-Path "scripts\windows\gob-status.ps1") {
        & "scripts\windows\gob-status.ps1"
    } else {
        Write-Host "❌ Windows status script not found" -ForegroundColor Red
    }
} elseif ($IsLinux -or $IsMacOS) {
    Write-Host "🐧 Linux/Unix detected" -ForegroundColor Cyan
    if (Test-Path "scripts/linux/gob-status.sh") {
        chmod +x "scripts/linux/gob-status.sh"
        & "scripts/linux/gob-status.sh"
    } else {
        Write-Host "❌ Linux status script not found" -ForegroundColor Red
    }
}
