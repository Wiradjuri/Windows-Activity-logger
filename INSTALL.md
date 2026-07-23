# Windows Activity Logger - Installation and Usage Guide

## Quick Start

### 1. Initial Setup

Run the setup script as Administrator:
```cmd
setup.bat
```

This will:
- Check Python installation
- Install all required dependencies
- Create necessary directories

### 2. Running the Logger

#### Option A: Using the Run Script
```cmd
run.bat
```

#### Option B: Direct Python Execution
```cmd
python main.py
```

**Note**: Both methods require Administrator privileges for full functionality.

## Detailed Installation Steps

### Prerequisites

1. **Windows 11 Pro** or higher
2. **Python 3.8+** installed and added to PATH
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
3. **Administrator access** to your system

### Manual Installation

If you prefer manual setup:

1. Open Command Prompt as Administrator

2. Navigate to the project directory:
```cmd
cd path\to\Windows-Activity-logger
```

3. Install dependencies:
```cmd
pip install -r requirements.txt
```

4. Create log directories:
```cmd
mkdir logs
mkdir config
```

## Running at System Startup

To automatically start the logger when Windows boots:

### Method 1: Task Scheduler (Recommended)

1. Open **Task Scheduler** (search in Start Menu)
2. Click "Create Task" (not "Create Basic Task")
3. **General Tab**:
   - Name: `Windows Activity Logger`
   - Description: `Monitors system for unauthorized access`
   - Check "Run with highest privileges"
   - Configure for: Windows 11

4. **Triggers Tab**:
   - Click "New"
   - Begin the task: "At log on"
   - Settings: "Specific user" (your account)

5. **Actions Tab**:
   - Click "New"
   - Action: "Start a program"
   - Program/script: `python.exe`
   - Add arguments: `main.py`
   - Start in: `C:\path\to\Windows-Activity-logger`

6. **Conditions Tab**:
   - Uncheck "Start the task only if the computer is on AC power"

7. **Settings Tab**:
   - Check "Allow task to be run on demand"
   - Check "Run task as soon as possible after a scheduled start is missed"

8. Click "OK" and enter your password if prompted

### Method 2: Startup Folder

1. Press `Win + R`
2. Type: `shell:startup`
3. Create a shortcut to `run.bat` in this folder
4. Right-click the shortcut → Properties → Advanced
5. Check "Run as administrator"

**Note**: This method may require UAC approval each time.

## Monitoring the Logger

### View Real-Time Logs

While the logger is running, you can view logs in real-time:

```cmd
# In a separate command prompt
cd logs
type keystrokes.log
type windows.log
type activity.log
type mouse.log
```

### Check Log Statistics

```cmd
python utils.py
```

This displays:
- Log file sizes
- Number of entries
- Last modification times

## Configuration

Edit `config.py` to customize behavior:

### Log File Locations
```python
KEYLOG_FILE = LOGS_DIR / "keystrokes.log"
ACTIVITY_LOG_FILE = LOGS_DIR / "activity.log"
WINDOW_LOG_FILE = LOGS_DIR / "windows.log"
MOUSE_LOG_FILE = LOGS_DIR / "mouse.log"
```

### Monitoring Intervals
```python
LOG_INTERVAL = 60  # seconds - system activity logging interval
WINDOW_CHECK_INTERVAL = 1  # seconds - window change check interval
```

### Log Management
```python
LOG_RETENTION_DAYS = 30  # days to keep logs before auto-deletion
MAX_LOG_SIZE_MB = 100  # maximum log file size before rotation
```

## Security Best Practices

1. **Protect Log Files**:
   - Set restrictive NTFS permissions on the `logs` folder
   - Only your user account should have read/write access

2. **Secure the Application**:
   - Keep the application directory secure
   - Don't share logs with unauthorized parties

3. **Regular Maintenance**:
   - Review logs regularly for unauthorized access
   - Archive old logs to external storage
   - Clean up logs that are no longer needed

4. **Encryption** (Optional):
   - Consider encrypting the `logs` folder using Windows EFS
   - Use BitLocker for full disk encryption

## Troubleshooting

### "Access Denied" Errors

**Solution**: Run as Administrator
- Right-click Command Prompt → "Run as Administrator"
- Or right-click `run.bat` → "Run as Administrator"

### "Module not found" Errors

**Solution**: Reinstall dependencies
```cmd
pip install -r requirements.txt --force-reinstall
```

### Python Not Found

**Solution**: Add Python to PATH
1. Find Python installation location (usually `C:\Python3X\`)
2. Add to System PATH environment variable
3. Restart Command Prompt

### High CPU Usage

**Solution**: Adjust monitoring intervals in `config.py`
```python
LOG_INTERVAL = 120  # Increase from 60 to 120 seconds
WINDOW_CHECK_INTERVAL = 2  # Increase from 1 to 2 seconds
```

### Logs Growing Too Large

**Solution**: Enable automatic rotation
```python
MAX_LOG_SIZE_MB = 50  # Reduce from 100 to 50 MB
```

Then run:
```cmd
python utils.py
```

## Stopping the Logger

### Graceful Shutdown
Press `Ctrl+C` in the Command Prompt window

### Force Stop
1. Open Task Manager (`Ctrl+Shift+Esc`)
2. Find "Python" process
3. Right-click → End Task

**Note**: Force stopping may result in data loss from buffered events.

## Viewing Logs

### Using Notepad
```cmd
notepad logs\keystrokes.log
```

### Using PowerShell (with filtering)
```powershell
# View last 50 lines
Get-Content logs\keystrokes.log -Tail 50

# Search for specific content
Select-String -Path logs\windows.log -Pattern "chrome.exe"
```

### Using Log Viewer Tools
- Baretail: https://www.baremetalsoft.com/baretail/
- Notepad++: https://notepad-plus-plus.org/
- Visual Studio Code

## Uninstallation

1. Stop the logger (press `Ctrl+C`)
2. Remove from Task Scheduler (if configured)
3. Delete the application directory
4. Optionally, remove Python packages:
```cmd
pip uninstall pynput psutil pywin32 cryptography
```

## Legal Compliance

**Important**: Before using this software:

1. Ensure you own the computer you're monitoring
2. Check local laws regarding monitoring and logging
3. Do not use on employer-owned devices without permission
4. Do not share or distribute logs containing personal information
5. Comply with data protection regulations (GDPR, CCPA, etc.)

## Support

For issues or questions:
1. Check this documentation
2. Review the README.md
3. Check the GitHub repository issues
4. Ensure you're using the latest version

## Updates

To update to the latest version:
```cmd
git pull origin main
pip install -r requirements.txt --upgrade
```

---

**Remember**: This tool is for personal security monitoring only. Use responsibly and legally.
