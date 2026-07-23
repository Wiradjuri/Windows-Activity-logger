"""
Log Viewer - Simple utility to view and analyze logs
"""
import sys
from pathlib import Path
import config
from utils import print_log_statistics


def view_log(log_file, lines=50):
    """View the last N lines of a log file"""
    if not log_file.exists():
        print(f"Log file not found: {log_file}")
        return
    
    print(f"\n{'=' * 60}")
    print(f"Viewing last {lines} lines of: {log_file.name}")
    print('=' * 60 + '\n')
    
    try:
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            all_lines = f.readlines()
            last_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
            print(''.join(last_lines))
    except Exception as e:
        print(f"Error reading log file: {e}")


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Windows Activity Logger - Log Viewer")
        print("=" * 60)
        print("\nUsage:")
        print("  python view_logs.py [log_type] [optional: number of lines]")
        print("\nLog types:")
        print("  keystrokes  - View keyboard events")
        print("  mouse       - View mouse events")
        print("  windows     - View window changes")
        print("  activity    - View system activity")
        print("  stats       - View log statistics")
        print("\nExamples:")
        print("  python view_logs.py keystrokes")
        print("  python view_logs.py windows 100")
        print("  python view_logs.py stats")
        return
    
    log_type = sys.argv[1].lower()
    lines = int(sys.argv[2]) if len(sys.argv) > 2 else 50
    
    log_files = {
        'keystrokes': config.KEYLOG_FILE,
        'mouse': config.MOUSE_LOG_FILE,
        'windows': config.WINDOW_LOG_FILE,
        'activity': config.ACTIVITY_LOG_FILE
    }
    
    if log_type == 'stats':
        print_log_statistics()
    elif log_type in log_files:
        view_log(log_files[log_type], lines)
    else:
        print(f"Unknown log type: {log_type}")
        print("Valid options: keystrokes, mouse, windows, activity, stats")


if __name__ == "__main__":
    main()
