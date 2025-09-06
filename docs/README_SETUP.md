# GOBV1 - Legacy Setup Documentation (ARCHIVED)


## Original Documentation:

# GOB (General Orchestrator Bot) - Setup Documentation

## 🚀 **Quick Start**

### **On Windows:**
```powershell
# 2. Open PowerShell in project directory
cd C:\Users\JANET\dusty\g-o-b

# 3. Start GOB

# 4. Open browser to http://localhost:8080
```

### **Check Status:**
```powershell
.\gob-status.ps1
```

## 📚 **Documentation Index**

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **[WINDOWS_SETUP.md](WINDOWS_SETUP.md)** | 🖥️ Complete Windows setup guide | **Start here** for Windows users |
| This README | 🎯 Quick reference and navigation | Finding the right documentation |

## 🎯 **Essential Information**

### **Access Points:**
- **Web UI**: http://localhost:8080
- **SSH**: `ssh root@localhost -p 2222`

### **Key Scripts:**
- `.\gob-status.ps1` - Check container status  

### **Auto-Start:**

## 🛠️ **Common Tasks**

### **Daily Development:**
```powershell
# Start working
.\gob-status.ps1          # Check if running

# Make code changes in your editor
# Changes are live-mounted, restart to apply:

# View logs
```

### **Troubleshooting:**
```powershell

# Check container status
.\gob-status.ps1

# Clean up resources

# Full restart
```

## 🔧 **Configuration Files**

| File | Purpose |
|------|---------|
| `.env` | Environment variables and API keys |

## 📂 **Project Structure**

```
g-o-b/
├── README_SETUP.md          # This file - setup navigation
├── WINDOWS_SETUP.md         # Complete Windows guide
├── gob-status.ps1           # Status checker
├── .env                     # Configuration
    ├── base/                # Base image files
    └── run/                 # Runtime configuration
```

## 🆘 **Getting Help**

### **If Something's Not Working:**
1. 📖 **Read**: [WINDOWS_SETUP.md](WINDOWS_SETUP.md) troubleshooting section
2. 🔍 **Check**: Run `.\gob-status.ps1` for current status

### **Quick Diagnostics:**
```powershell

# Is GOB container running?

# Are the ports available?
netstat -ano | Select-String ":8080|:2222"

# What's in the logs?
```

## 🎉 **You're All Set!**

If GOB is running and accessible at http://localhost:8080, you're ready to go!

For detailed setup, configuration, and troubleshooting, see **[WINDOWS_SETUP.md](WINDOWS_SETUP.md)**.

---

**Version**: Custom GOB build  
**Last Updated**: 2025-09-05
