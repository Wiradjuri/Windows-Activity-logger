"""
Main Windows Activity Logger Application
Monitors keyboard, mouse, windows, and system activity for personal security monitoring.

WARNING: This tool is intended for personal use only on your own computer.
Unauthorized use on other systems may violate privacy laws.
"""
import signal
import sys
import time
from datetime import datetime

from keylogger import KeyLogger
from mouse_logger import MouseLogger
from window_logger import WindowLogger
from activity_logger import ActivityLogger
import config


class ActivityMonitor:
    """Main application class that coordinates all logging modules"""
    
    def __init__(self):
        self.keylogger = KeyLogger()
        self.mouse_logger = MouseLogger()
        self.window_logger = WindowLogger()
        self.activity_logger = ActivityLogger(log_interval=config.LOG_INTERVAL)
        self.running = False
        
    def start(self):
        """Start all logging modules"""
        print("=" * 60)
        print("Windows Activity Logger - Starting")
        print("=" * 60)
        print(f"Log directory: {config.LOGS_DIR}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print("Monitoring:")
        print("  - Keyboard events")
        print("  - Mouse events")
        print("  - Active windows")
        print("  - System activity")
        print()
        print("Press Ctrl+C to stop monitoring")
        print("=" * 60)
        print()
        
        self.running = True
        
        # Start all loggers
        self.keylogger.start()
        self.mouse_logger.start()
        self.window_logger.start()
        self.activity_logger.start()
        
        # Log session start
        self._log_session_event("SESSION_START")
    
    def stop(self):
        """Stop all logging modules"""
        if not self.running:
            return
        
        print("\n" + "=" * 60)
        print("Windows Activity Logger - Stopping")
        print("=" * 60)
        
        self.running = False
        
        # Stop all loggers
        self.keylogger.stop()
        self.mouse_logger.stop()
        self.window_logger.stop()
        self.activity_logger.stop()
        
        # Log session end
        self._log_session_event("SESSION_END")
        
        print(f"Stopped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Logs saved to: {config.LOGS_DIR}")
        print("=" * 60)
    
    def _log_session_event(self, event_type):
        """Log session start/end events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event_log = f"\n{'=' * 60}\n[{timestamp}] {event_type}\n{'=' * 60}\n\n"
        
        # Write to all log files
        for log_file in [config.KEYLOG_FILE, config.MOUSE_LOG_FILE, 
                        config.WINDOW_LOG_FILE, config.ACTIVITY_LOG_FILE]:
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(event_log)
    
    def run(self):
        """Main run loop"""
        try:
            self.start()
            
            # Keep the program running
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\nReceived interrupt signal...")
        except Exception as e:
            print(f"\nError occurred: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.stop()


def signal_handler(signum, frame):
    """Handle termination signals"""
    print("\n\nReceived termination signal...")
    sys.exit(0)


def main():
    """Main entry point"""
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create and run the monitor
    monitor = ActivityMonitor()
    monitor.run()


if __name__ == "__main__":
    main()
