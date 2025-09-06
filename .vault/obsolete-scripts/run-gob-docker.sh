#!/bin/bash
# GOB Docker Container Runner for Linux

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# Stop and remove existing container if it exists
echo -e "${YELLOW}🛑 Stopping existing GOB container...${NC}"
docker stop g-o-b 2>/dev/null || true
docker rm g-o-b 2>/dev/null || true

# Run the GOB container
echo -e "${GREEN}🚀 Starting GOB Docker container...${NC}"
docker run -d \
  --name g-o-b \
  -p 50080:80 \
  -p 50022:22 \
  --restart unless-stopped \
  -v "$(pwd):/gob" \
  --env-file .env \
  g-o-b:latest

# Check if container started successfully
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ GOB container started successfully!${NC}"
    echo -e "${CYAN}🌐 Web UI: http://localhost:50080${NC}"
    echo -e "${CYAN}🔧 SSH: localhost:50022${NC}"  
    echo -e "${CYAN}📋 Container name: g-o-b${NC}"
    echo ""
    echo -e "${GRAY}To view logs: docker logs g-o-b${NC}"
    echo -e "${GRAY}To stop: docker stop g-o-b${NC}"
    
    # Optionally open browser
    read -p "Open GOB web interface in browser? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if command -v xdg-open > /dev/null; then
            xdg-open "http://localhost:50080"
        elif command -v open > /dev/null; then
            open "http://localhost:50080"  # macOS
        else
            echo -e "${YELLOW}Please open http://localhost:50080 in your browser${NC}"
        fi
    fi
else
    echo -e "${RED}❌ Failed to start GOB container${NC}"
    exit 1
fi
