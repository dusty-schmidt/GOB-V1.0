# GOB Maintenance Script
Write-Host "🧹 GOB Maintenance Utility" -ForegroundColor Green

Write-Host "`n📊 System Status:" -ForegroundColor Cyan
.\gob-status.ps1

Write-Host "`n🧹 Cleanup Options:" -ForegroundColor Yellow
Write-Host "1. Clean Docker resources (safe)" -ForegroundColor White
Write-Host "2. Remove temporary files" -ForegroundColor White  
Write-Host "3. Check for large files" -ForegroundColor White
Write-Host "4. Update documentation dates" -ForegroundColor White
Write-Host "5. Full system check" -ForegroundColor White
Write-Host "0. Exit" -ForegroundColor Gray

$choice = Read-Host "`nSelect option (0-5)"

switch ($choice) {
    "1" {
        Write-Host "🗑️ Running Docker cleanup..." -ForegroundColor Yellow
        .\docker-cleanup.ps1
    }
    "2" {
        Write-Host "🗑️ Removing temporary files..." -ForegroundColor Yellow
        Get-ChildItem -Recurse -Force | Where-Object {
            $_.Name -match "\.(tmp|temp|log|bak)$" -or 
            $_.Name -eq ".DS_Store" -or 
            $_.Name -eq "Thumbs.db"
        } | Remove-Item -Force -Verbose
    }
    "3" {
        Write-Host "📊 Large files (>50MB):" -ForegroundColor Cyan
        Get-ChildItem -Recurse | Where-Object {$_.Length -gt 50MB} | 
        Select-Object Name, @{Name="Size(MB)";Expression={[math]::Round($_.Length/1MB,2)}}, FullName
    }
    "4" {
        Write-Host "📝 Updating documentation timestamps..." -ForegroundColor Yellow
        $date = Get-Date -Format "yyyy-MM-dd"
        # Update README.md
        (Get-Content README.md) -replace "Last Updated.*", "**Last Updated**: $date" | Set-Content README.md
        Write-Host "✅ Documentation updated" -ForegroundColor Green
    }
    "5" {
        Write-Host "🔍 Full system check..." -ForegroundColor Cyan
        Write-Host "`nDocker Status:"
        docker version --format "Client: {{.Client.Version}}, Server: {{.Server.Version}}"
        Write-Host "`nGOB Status:"
        .\gob-status.ps1
        Write-Host "`nDisk Usage:"
        docker system df
        Write-Host "`nGit Status:"
        git status --porcelain
    }
    "0" {
        Write-Host "👋 Maintenance complete" -ForegroundColor Gray
    }
    default {
        Write-Host "❌ Invalid option" -ForegroundColor Red
    }
}
