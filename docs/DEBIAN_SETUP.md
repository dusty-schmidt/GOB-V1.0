# G-O-B Development Setup Guide for Debian Systems

This guide will walk you through setting up your development environment for the g-o-b project on Debian-based Linux systems.

## Prerequisites

- Debian-based Linux system (Ubuntu, Debian, etc.)
- Internet connection
- Terminal access with sudo privileges

## 1️⃣ Install Git on Debian

```bash
# Update package list
sudo apt update

# Install Git
sudo apt install git -y

# Configure Git with your credentials
git config --global user.name "dusty-schmidt"
git config --global user.email "dustin.schmidt.86@proton.me"

# Verify installation
git --version
```

## 2️⃣ Install Docker on Debian

```bash
# Install prerequisites
sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release -y

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package list with Docker repo
sudo apt update

# Install Docker CE
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y

# Add your user to docker group (to run Docker without sudo)
sudo usermod -aG docker $USER

# Enable Docker service
sudo systemctl enable docker
sudo systemctl start docker

# Verify Docker installation
docker --version

# Note: You'll need to log out and back in (or restart) for the group change to take effect
```

## 3️⃣ Set up GitHub Authentication

### Option A: SSH Keys (Recommended)

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "dustin.schmidt.86@proton.me"

# Start ssh-agent
eval "$(ssh-agent -s)"

# Add SSH key to agent
ssh-add ~/.ssh/id_ed25519

# Display public key (copy this to GitHub)
cat ~/.ssh/id_ed25519.pub
```

**Then on GitHub:**
1. Go to GitHub.com → Settings → SSH and GPG keys
2. Click "New SSH key"
3. Paste the public key content
4. Give it a title like "Debian Home Computer"

### Option B: Personal Access Token
- Use your existing GitHub personal access token
- Git will prompt for username/token when you push

## 4️⃣ Clone Your Repository

```bash
# Create a development directory
mkdir -p ~/Development
cd ~/Development

# Clone with SSH (if you set up SSH keys)
git clone git@github.com:dusty-schmidt/g-o-b.git

# OR clone with HTTPS (if using personal access token)
git clone https://github.com/dusty-schmidt/g-o-b.git

# Enter the project directory
cd g-o-b

# Verify you're on the main branch
git branch -a
git status
```

## 5️⃣ Build and Run Development Container

```bash
# Make sure you're in the project directory
cd ~/Development/g-o-b

# Build the Docker image
docker build -t g-o-b-dev -f DockerfileLocal .

# Run the container with bind mount for live development
docker run -d \
  --name g-o-b-dev \
  -p 50080:80 \
  -p 50022:22 \
  -v "$(pwd):/a0" \
  g-o-b-dev

# Check if it's running
docker ps

# View logs
docker logs g-o-b-dev --tail 20
```

## 6️⃣ Verify Setup

```bash
# 1. Check that the web UI is accessible
curl -I http://localhost:50080

# 2. Open in browser: http://localhost:50080

# 3. Create a test file to verify live changes
echo "# Linux Development Test" > linux-test.md

# 4. Test Git workflow
git add linux-test.md
git commit -m "Test commit from Linux development setup"
git push

# 5. Pull changes from other machines
git pull
```

## 🚀 Daily Development Workflow

### Starting Development Session
```bash
cd ~/Development/g-o-b
docker start g-o-b-dev
# Access at http://localhost:50080
```

### Making Changes
1. Edit files in your local directory
2. Changes are immediately reflected in the running container
3. Test your changes at http://localhost:50080

### Committing Changes
```bash
git add .
git commit -m "Description of your changes"
git push
```

### Syncing with Other Machines
```bash
git pull
# Container automatically uses updated files
```

### Stopping Development
```bash
docker stop g-o-b-dev
```

## 🔧 Useful Commands

### Container Management
```bash
# View running containers
docker ps

# View all containers
docker ps -a

# View container logs
docker logs g-o-b-dev

# Follow logs in real-time
docker logs -f g-o-b-dev

# Execute commands inside container
docker exec -it g-o-b-dev bash

# Stop container
docker stop g-o-b-dev

# Start container
docker start g-o-b-dev

# Remove container (will need to recreate)
docker rm g-o-b-dev
```

### Rebuild Container (if needed)
```bash
docker stop g-o-b-dev
docker rm g-o-b-dev
docker build -t g-o-b-dev -f DockerfileLocal .
docker run -d --name g-o-b-dev -p 50080:80 -p 50022:22 -v "$(pwd):/a0" g-o-b-dev
```

### Git Commands
```bash
# Check status
git status

# View commit history
git log --oneline -10

# Check what branch you're on
git branch

# Pull latest changes
git pull

# Push your changes
git push
```

## 📁 Directory Structure

Your development setup will be located at:
- **Project Directory**: `~/Development/g-o-b/`
- **Access URL**: http://localhost:50080
- **SSH Access**: localhost:50022 (if needed)

## 🌐 Multi-Computer Development

This setup allows you to work seamlessly across multiple machines:

1. **Consistent Environment**: Same Docker container on all machines
2. **Synchronized Code**: Git keeps all machines in sync
3. **Same Access Points**: Always use port 50080 for web UI
4. **Live Development**: File changes are immediately visible

## 🔍 Troubleshooting

### Docker Permission Issues
If you get permission errors with Docker:
```bash
# Make sure you're in the docker group
groups $USER

# If not in docker group, add yourself and restart
sudo usermod -aG docker $USER
# Then log out and back in, or restart
```

### Container Won't Start
```bash
# Check if port is already in use
sudo netstat -tulpn | grep :50080

# Remove and recreate container
docker rm -f g-o-b-dev
docker run -d --name g-o-b-dev -p 50080:80 -p 50022:22 -v "$(pwd):/a0" g-o-b-dev
```

### Git Authentication Issues
```bash
# Test SSH connection to GitHub
ssh -T git@github.com

# If using HTTPS, make sure you have a valid personal access token
```

## 📝 Notes

- The bind mount (`-v "$(pwd):/a0"`) enables live development
- Changes to files are immediately reflected in the running container
- Container rebuild is only needed when Docker configuration changes
- Use the same Git workflow on all machines for consistency
- Web UI is accessible at http://localhost:50080 on all machines

---

**Created**: 2025-09-05  
**Project**: g-o-b (Agent Zero Fork)  
**Repository**: https://github.com/dusty-schmidt/g-o-b
