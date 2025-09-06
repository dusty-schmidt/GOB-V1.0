# Docker Cleanup Script
Write-Host "🧹 Docker Cleanup Utility" -ForegroundColor Green

Write-Host "`n📊 Current Docker Usage:" -ForegroundColor Cyan
docker system df

Write-Host "`n🔍 All Containers:" -ForegroundColor Yellow
docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.CreatedAt}}"

Write-Host "`n🎯 Safe Cleanup Options:" -ForegroundColor Magenta
Write-Host "1. Remove stopped containers (keeps GOB if running)" -ForegroundColor White
Write-Host "2. Remove unused images (keeps active images)" -ForegroundColor White
Write-Host "3. Remove unused volumes" -ForegroundColor White
Write-Host "4. Full cleanup (CAUTION: stops and removes everything)" -ForegroundColor Red
Write-Host "5. Just show what would be cleaned" -ForegroundColor Gray
Write-Host "0. Exit" -ForegroundColor Gray

$choice = Read-Host "`nSelect option (0-5)"

switch ($choice) {
    "1" {
        Write-Host "🗑️ Removing stopped containers..." -ForegroundColor Yellow
        docker container prune -f
    }
    "2" {
        Write-Host "🗑️ Removing unused images..." -ForegroundColor Yellow
        docker image prune -f
    }
    "3" {
        Write-Host "🗑️ Removing unused volumes..." -ForegroundColor Yellow
        docker volume prune -f
    }
    "4" {
        Write-Host "⚠️ FULL CLEANUP - This will stop GOB!" -ForegroundColor Red
        $confirm = Read-Host "Are you sure? (type 'YES' to confirm)"
        if ($confirm -eq "YES") {
            docker stop $(docker ps -aq) 2>$null
            docker system prune -af --volumes
            Write-Host "✅ Full cleanup complete" -ForegroundColor Green
        } else {
            Write-Host "❌ Cleanup cancelled" -ForegroundColor Yellow
        }
    }
    "5" {
        Write-Host "👀 Dry run - what would be cleaned:" -ForegroundColor Cyan
        Write-Host "`nStopped containers:"
        docker ps -a --filter "status=exited" --format "{{.Names}} ({{.Image}})"
        Write-Host "`nUnused images:"
        docker images --filter "dangling=true" --format "{{.Repository}}:{{.Tag}} ({{.Size}})"
        Write-Host "`nUnused volumes:"
        docker volume ls --filter "dangling=true" --format "{{.Name}}"
    }
    "0" {
        Write-Host "👋 Cleanup cancelled" -ForegroundColor Gray
    }
    default {
        Write-Host "❌ Invalid option" -ForegroundColor Red
    }
}

Write-Host "`n📊 Current Docker Usage After Cleanup:" -ForegroundColor Cyan
docker system df
