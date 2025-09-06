#!/bin/bash
# GOB Container Status & Management

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
GRAY='\033[0;37m'
NC='\033[0m'

echo -e "${GREEN}🤖 GOB Container Status${NC}"

# Check if container exists and is running
container_info=$(docker ps -a --filter "name=g-o-b" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}")
if [ -n "$container_info" ]; then
    echo -e "\n${CYAN}📦 Container Info:${NC}"
    echo "$container_info"
    
    # Check if it's running
    running=$(docker ps --filter "name=g-o-b" --format "{{.Names}}")
    if [ -n "$running" ]; then
        echo -e "\n${GREEN}✅ GOB is RUNNING${NC}"
        echo -e "${CYAN}🌐 Web UI: http://localhost:50080${NC}"
        echo -e "${CYAN}🔧 SSH: localhost:50022${NC}"
        
        echo -e "\n${YELLOW}📊 Quick Actions:${NC}"
        echo -e "${GRAY}  Logs: docker logs -f g-o-b${NC}"
        echo -e "${GRAY}  Stop: docker stop g-o-b${NC}"
        echo -e "${GRAY}  Restart: docker restart g-o-b${NC}"
    else
        echo -e "\n${RED}❌ GOB is STOPPED${NC}"
        echo -e "${YELLOW}🚀 Start with: ./scripts/linux/run-gob-docker.sh${NC}"
    fi
else
    echo -e "\n${RED}❌ GOB container not found${NC}"
    echo -e "${YELLOW}🚀 Create with: ./scripts/linux/run-gob-docker.sh${NC}"
fi

# Show all Docker containers for reference
echo -e "\n${MAGENTA}🐳 All Docker Containers:${NC}"
docker ps -a --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
