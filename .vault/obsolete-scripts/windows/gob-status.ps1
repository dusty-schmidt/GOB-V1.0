# GOB Container Status & Management
Write-Host "🤖 GOB Container Status" -ForegroundColor Green

# Check if container exists and is running
$container = docker ps -a --filter "name=g-o-b" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
if ($container) {
    Write-Host "`n📦 Container Info:" -ForegroundColor Cyan
    Write-Host $container
    
    # Check if it's running
    $running = docker ps --filter "name=g-o-b" --format "{{.Names}}"
    if ($running) {
        Write-Host "`n✅ GOB is RUNNING" -ForegroundColor Green
        Write-Host "🌐 Web UI: http://localhost:8080" -ForegroundColor Cyan
        Write-Host "🔧 SSH: localhost:2222" -ForegroundColor Cyan
        
        Write-Host "`n📊 Quick Actions:" -ForegroundColor Yellow
        Write-Host "  Logs: docker logs -f g-o-b" -ForegroundColor Gray
        Write-Host "  Stop: docker stop g-o-b" -ForegroundColor Gray
        Write-Host "  Restart: docker restart g-o-b" -ForegroundColor Gray
    } else {
        Write-Host "`n❌ GOB is STOPPED" -ForegroundColor Red
        Write-Host "🚀 Start with: .\run-gob-docker.ps1" -ForegroundColor Yellow
    }
} else {
    Write-Host "`n❌ GOB container not found" -ForegroundColor Red
    Write-Host "🚀 Create with: .\run-gob-docker.ps1" -ForegroundColor Yellow
}

# Show all Docker containers for reference
Write-Host "`n🐳 All Docker Containers:" -ForegroundColor Magenta
docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
