"""
Utility functions for log management
"""
import os
from datetime import datetime, timedelta
from pathlib import Path
import config


def rotate_logs():
    """Rotate log files if they exceed maximum size"""
    for log_file in [config.KEYLOG_FILE, config.MOUSE_LOG_FILE,
                    config.WINDOW_LOG_FILE, config.ACTIVITY_LOG_FILE]:
        if log_file.exists():
            size_mb = log_file.stat().st_size / (1024 * 1024)
            
            if size_mb > config.MAX_LOG_SIZE_MB:
                # Create rotated filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                rotated_name = log_file.stem + f"_{timestamp}" + log_file.suffix
                rotated_file = log_file.parent / rotated_name
                
                # Rename current log file
                log_file.rename(rotated_file)
                print(f"Rotated {log_file.name} to {rotated_name}")


def cleanup_old_logs():
    """Delete logs older than retention period"""
    cutoff_date = datetime.now() - timedelta(days=config.LOG_RETENTION_DAYS)
    
    for log_file in config.LOGS_DIR.glob("*.log"):
        if log_file.exists():
            modified_time = datetime.fromtimestamp(log_file.stat().st_mtime)
            
            if modified_time < cutoff_date:
                log_file.unlink()
                print(f"Deleted old log: {log_file.name}")


def get_log_statistics():
    """Get statistics about log files"""
    stats = {}
    
    for log_file in [config.KEYLOG_FILE, config.MOUSE_LOG_FILE,
                    config.WINDOW_LOG_FILE, config.ACTIVITY_LOG_FILE]:
        if log_file.exists():
            size_mb = log_file.stat().st_size / (1024 * 1024)
            modified = datetime.fromtimestamp(log_file.stat().st_mtime)
            
            # Count lines in file
            with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
                line_count = sum(1 for _ in f)
            
            stats[log_file.name] = {
                'size_mb': round(size_mb, 2),
                'lines': line_count,
                'last_modified': modified.strftime("%Y-%m-%d %H:%M:%S")
            }
    
    return stats


def print_log_statistics():
    """Print log file statistics"""
    stats = get_log_statistics()
    
    print("\n" + "=" * 60)
    print("Log File Statistics")
    print("=" * 60)
    
    for filename, data in stats.items():
        print(f"\n{filename}:")
        print(f"  Size: {data['size_mb']} MB")
        print(f"  Lines: {data['lines']:,}")
        print(f"  Last Modified: {data['last_modified']}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    # When run directly, print statistics
    print_log_statistics()
