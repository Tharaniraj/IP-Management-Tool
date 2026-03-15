# IP Management Tool - Quick Start Guide

**Start your web application in seconds with automatic setup!**

## 🚀 Quick Start (Choose Your OS)

### Windows

#### Option 1: Simple Batch Script (Recommended)
```bash
double-click START.bat
```

**Or** open PowerShell and run:
```powershell
.\START.bat
```

#### Option 2: PowerShell Script (More Modern)
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteS igned -Scope CurrentUser
.\START.ps1
```

### Linux / Mac

```bash
chmod +x START.sh
./START.sh
```

## ⏱️ First Run (2-3 minutes)
- Creates virtual environment
- Installs Flask and dependencies
- Starts web server

## ⏱️ Subsequent Runs (5 seconds)
- Activates existing environment
- Starts server immediately

## 🌐 Access Your Application

After the script completes, you'll see:

```
============================================================
IP MANAGEMENT TOOL - WEB VERSION - STARTUP
============================================================

✓ Flask server ready

ACCESS THE APPLICATION:
  Local:        http://localhost:5000
  From LAN:     http://192.168.1.100:5000
  Hostname:     YOUR-COMPUTER-NAME

Press Ctrl+C to stop the server
============================================================
```

### Local Access
- **Browser**: Open http://localhost:5000

### Access from Other Computers on Network
1. Use the IP shown in startup output
2. Open http://192.168.x.x:5000 (replace with your IP)
3. Both computers must be on **same network**

## 📋 What Each Script Does

### START.bat (Windows - Batch)
```
1. Checks if Python is installed
2. Creates .venv folder (first run only)
3. Activates virtual environment
4. Installs requirements.txt packages
5. Creates /data and /logs directories
6. Starts Flask server on port 5000
```

**Pros:**
- Simple double-click execution
- No PowerShell policy issues
- Works with all Windows versions

**Cons:**
- Less detailed output
- Limited error messages

---

### START.ps1 (Windows - PowerShell)
```
1. Checks if Python is installed
2. Creates .venv folder (first run only)
3. Activates virtual environment
4. Installs requirements.txt packages
5. Creates /data and /logs directories
6. Shows local IP address
7. Starts Flask server on port 5000
```

**Pros:**
- Modern Windows script
- Colorized output
- Shows your local IP automatically
- Better error messages

**Cons:**
- Requires PowerShell execution policy change
- First time setup is more involved

**If you get execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then run: `.\START.ps1`

---

### START.sh (Linux/Mac - Bash)
```
1. Checks if Python 3 is installed
2. Creates .venv folder (first run only)
3. Activates virtual environment
4. Installs requirements.txt packages
5. Creates /data and /logs directories
6. Shows local IP address
7. Starts Flask server on port 5000
```

**Pros:**
- Cross-platform (Linux, Mac, BSD)
- Colorized output
- Automatic IP detection

**Cons:**
- Requires chmod +x on first use
- Linux-specific paths

**First time only:**
```bash
chmod +x START.sh
```

---

## 🔧 Manual Setup (Advanced)

If scripts don't work, do this manually:

```bash
# 1. Navigate to project directory
cd c:\Users\User\OneDrive\Documents\GitHub\IP-Management-Tool

# 2. Create virtual environment
python -m venv .venv

# 3. Activate it
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create directories
mkdir data\backups logs

# 6. Run the app
python app.py
```

## 🌍 Network Access

### Find Your Server IP

**Windows:**
```powershell
ipconfig
```
Look for "IPv4 Address" under your network adapter

**Linux/Mac:**
```bash
hostname -I
```

### Allow Firewall Access

**Windows Defender Firewall:**
1. Search "Windows Defender Firewall"
2. Click "Allow an app through firewall"
3. Click "Change settings"
4. Click "Allow another app"
5. Browse → Select `python.exe`
6. Click "Add"
7. ✓ Check both Private & Public
8. Click "OK"

**Allow Other Apps:**
Also add Flask if needed:
- Search for python installation folder
- Add all python.exe instances

## ✅ Verify it Works

After startup completes:

1. **Open browser**: http://localhost:5000
2. **Should see**: IP Management Tool web interface
3. **Try adding**: Click ➕ Add, enter test IP like 192.168.1.1
4. **From another PC**: http://YOUR-SERVER-IP:5000

## 🛑 Stop the Server

Press `Ctrl+C` in the terminal

## 📁 Project Structure

After first run, your folder will have:

```
IP-Management-Tool/
├── START.bat          ← Click this (Windows)
├── START.ps1          ← Or this (Windows modern)
├── START.sh           ← Or this (Linux/Mac)
├── app.py             ← Flask server
├── requirements.txt   ← Dependencies
├── .venv/             ← Virtual env (created auto)
├── data/
│   ├── ip_data.json   ← Your data
│   └── backups/       ← Automatic backups
├── logs/              ← App logs
├── modules/           ← Core functionality
├── templates/
│   └── index.html     ← Web interface
└── static/
    ├── css/style.css
    └── js/app.js
```

## 🚀 Production Deployment

For hosting on a server:

```bash
# Install Gunicorn (production server)
pip install gunicorn

# Run with multiple workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

Then access: http://server-ip:5000

## 📞 Troubleshooting

### Script doesn't execute
- **Windows**: Try double-clicking START.bat instead
- **Linux**: Make sure you ran `chmod +x START.sh`
- **Mac**: Same as Linux

### "Python not found"
- Install Python from https://www.python.org/
- **Important**: Check ✓ "Add Python to PATH" during installation
- Restart terminal/command prompt
- Try again

### "Port 5000 already in use"
- Another app is using port 5000
- Either close that app, or edit app.py:
  - Line: `app.run(host='0.0.0.0', port=5000, debug=False)`
  - Change `5000` to `5001` or `8000`

### "Permission denied" (Mac/Linux)
```bash
chmod +x START.sh
./START.sh
```

### Can't connect from other computer
- Both computers on same network?
- Firewall blocking port 5000? (See above)
- Using correct IP address?
- Try: http://YOUR-IP:5000 (not hostname)

## 📊 Ports Used

- **Flask**: Port 5000 (default)
- **Change port**: Edit app.py line with `port=5000`

## 🔐 Security Notes

- Application runs on unencrypted HTTP (fine for LAN)
- No authentication (assumes trusted network)
- All data stored locally in JSON format
- Backups created automatically
- To add HTTPS: See WEB_VERSION.md

## 📖 More Information

- Full setup guide: [WEB_VERSION.md](WEB_VERSION.md)
- Desktop version: `python Main.py`
- API documentation: See app.py routes

## ⚡ Tips

- **Keep terminal open** - closing it stops the server
- **Minimize, don't close** - if you need the server running
- **Both data sources** - Desktop and Web versions share the same data file
- **Don't run both** - Running desktop + web together can cause conflicts

---

**Questions?** Check [WEB_VERSION.md](WEB_VERSION.md) for detailed documentation.

**Ready to start?** Double-click START.bat (Windows) or run ./START.sh (Linux/Mac)
