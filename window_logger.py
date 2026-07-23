"""
Window activity logger module for tracking active windows and applications
"""
import threading
import time
from datetime import datetime
import win32gui
import win32process
import psutil
import config


class WindowLogger:
    """Monitors and logs active window changes"""
    
    def __init__(self, log_file=None, check_interval=None):
        self.log_file = log_file or config.WINDOW_LOG_FILE
        self.check_interval = check_interval or config.WINDOW_CHECK_INTERVAL
        self.current_window = None
        self.running = False
        self.thread = None
        
    def get_active_window_info(self):
        """Get information about the currently active window"""
        try:
            # Get the active window handle
            hwnd = win32gui.GetForegroundWindow()
            
            # Get window title
            window_title = win32gui.GetWindowText(hwnd)
            
            # Get process ID
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            
            # Get process name
            try:
                process = psutil.Process(pid)
                process_name = process.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process_name = "Unknown"
            
            return {
                'title': window_title,
                'process': process_name,
                'pid': pid
            }
        except Exception as e:
            return None
    
    def log_window_change(self, window_info):
        """Log window change to file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = (
            f"[{timestamp}] Window changed - "
            f"Title: {window_info['title']} | "
            f"Process: {window_info['process']} | "
            f"PID: {window_info['pid']}\n"
        )
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            window_info = self.get_active_window_info()
            
            if window_info:
                # Check if window has changed
                window_key = f"{window_info['title']}|{window_info['process']}"
                
                if window_key != self.current_window:
                    self.current_window = window_key
                    self.log_window_change(window_info)
            
            time.sleep(self.check_interval)
    
    def start(self):
        """Start the window logger"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.thread.start()
        print(f"[WindowLogger] Started logging to {self.log_file}")
    
    def stop(self):
        """Stop the window logger"""
        if not self.running:
            return
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("[WindowLogger] Stopped")
