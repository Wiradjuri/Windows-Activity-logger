# Windows Activity Logger

A comprehensive activity monitoring and logging tool for Windows 11+ designed for personal security and unauthorized access detection.

## ⚠️ Important Legal Notice

**This tool is intended ONLY for personal use on your own computer to monitor unauthorized access.** Using this tool on computers you do not own or without explicit permission may violate privacy laws and computer fraud statutes. Always comply with local laws and regulations.

## Features

- **Keyboard Event Logging**: Captures all keyboard inputs with timestamps
- **Mouse Activity Tracking**: Logs mouse clicks and scroll events
- **Active Window Monitoring**: Tracks which applications and windows are in focus
- **System Activity Logging**: Records CPU usage, memory usage, and top processes
- **Automatic Log Rotation**: Prevents log files from growing too large
- **Session Tracking**: Records when monitoring sessions start and stop

## Requirements

- Windows 11 Pro or higher
- Python 3.8+
- Administrator privileges (required for low-level input monitoring)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Wiradjuri/Windows-Activity-logger.git
cd Windows-Activity-logger
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Logger

**Important**: Run as Administrator for full functionality:

```bash
python main.py
```

The application will start monitoring and display:
- Keyboard events → `logs/keystrokes.log`
- Mouse events → `logs/mouse.log`
- Window changes → `logs/windows.log`
- System activity → `logs/activity.log`

### Stopping the Logger

Press `Ctrl+C` to gracefully stop the logger. All buffered data will be flushed to disk.

## Configuration

Edit `config.py` to customize:

- **Log file locations**: Change where logs are stored
- **Check intervals**: Adjust monitoring frequency
- **Log retention**: Set automatic log cleanup periods
- **Max log sizes**: Configure log rotation thresholds

## Log Files

### keystrokes.log
Records all keyboard inputs with timestamps:
```
[2026-02-15 10:30:45] Key pressed: h
[2026-02-15 10:30:45] Key pressed: e
[2026-02-15 10:30:45] Key pressed: l
[2026-02-15 10:30:45] Key pressed: l
[2026-02-15 10:30:45] Key pressed: o
```

### mouse.log
Tracks mouse clicks and scroll events:
```
[2026-02-15 10:30:50] Mouse Button.left pressed at (523, 412)
[2026-02-15 10:30:51] Mouse Button.left released at (523, 412)
[2026-02-15 10:30:55] Mouse scrolled down at (600, 450)
```

### windows.log
Logs active window and application changes:
```
[2026-02-15 10:31:00] Window changed - Title: Chrome - Google | Process: chrome.exe | PID: 5432
[2026-02-15 10:31:15] Window changed - Title: main.py - Visual Studio Code | Process: Code.exe | PID: 6789
```

### activity.log
Records system resource usage and top processes:
```
[2026-02-15 10:32:00] System Activity Report
CPU Usage: 25.3%
Memory Usage: 68.2%
Memory Available: 10.45 GB
Disk Usage: 45.6%
Top Processes:
  1. chrome.exe (PID: 5432) - CPU: 12.5%
  2. Code.exe (PID: 6789) - CPU: 8.3%
```

## Security Considerations

1. **Log File Security**: Store logs in a secure location with restricted access
2. **Data Encryption**: Consider encrypting logs containing sensitive information
3. **Log Rotation**: Regularly archive or delete old logs
4. **Access Control**: Ensure only authorized users can access the application
5. **Compliance**: Ensure usage complies with all applicable laws and regulations

## Running at Startup (Optional)

To automatically start monitoring when your computer boots:

1. Create a scheduled task in Windows Task Scheduler
2. Set trigger to "At log on"
3. Set action to run `python main.py` with administrator privileges
4. Set the working directory to the application folder

## Troubleshooting

### Permission Errors
- Ensure you're running as Administrator
- Check that Python has necessary permissions

### Missing Dependencies
```bash
pip install -r requirements.txt --upgrade
```

### High CPU Usage
- Increase check intervals in `config.py`
- Disable mouse logging if not needed

## Contributing

Contributions are welcome! Please ensure any changes:
- Maintain security best practices
- Include appropriate documentation
- Follow existing code style

## License

See [LICENSE](LICENSE) file for details.

## Disclaimer

This software is provided "as is" without warranty of any kind. The authors are not responsible for any misuse or damage caused by this software. Users are solely responsible for ensuring their use complies with all applicable laws and regulations.
