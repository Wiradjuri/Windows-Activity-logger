"""
Configuration settings for Windows Activity Logger
"""
import os
from pathlib import Path

# Directory paths
BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR / "logs"
CONFIG_DIR = BASE_DIR / "config"

# Create directories if they don't exist
LOGS_DIR.mkdir(exist_ok=True)
CONFIG_DIR.mkdir(exist_ok=True)

# Log file settings
KEYLOG_FILE = LOGS_DIR / "keystrokes.log"
ACTIVITY_LOG_FILE = LOGS_DIR / "activity.log"
WINDOW_LOG_FILE = LOGS_DIR / "windows.log"
MOUSE_LOG_FILE = LOGS_DIR / "mouse.log"

# Logging settings
LOG_INTERVAL = 60  # seconds - how often to log system activity
WINDOW_CHECK_INTERVAL = 1  # seconds - how often to check active window

# Security settings
LOG_RETENTION_DAYS = 30  # days to keep logs before auto-deletion
MAX_LOG_SIZE_MB = 100  # maximum log file size in MB before rotation
