"""
Mouse activity logger module for tracking mouse events
"""
import threading
from datetime import datetime
from pynput import mouse
import config


class MouseLogger:
    """Captures and logs mouse events"""
    
    def __init__(self, log_file=None):
        self.log_file = log_file or config.MOUSE_LOG_FILE
        self.buffer = []
        self.lock = threading.Lock()
        self.running = False
        self.listener = None
        
    def on_click(self, x, y, button, pressed):
        """Handle mouse click events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        action = "pressed" if pressed else "released"
        
        with self.lock:
            self.buffer.append(
                f"[{timestamp}] Mouse {button} {action} at ({x}, {y})\n"
            )
            
            # Auto-flush buffer if it gets too large
            if len(self.buffer) > 50:
                self._flush_buffer()
    
    def on_scroll(self, x, y, dx, dy):
        """Handle mouse scroll events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        direction = "down" if dy < 0 else "up"
        
        with self.lock:
            self.buffer.append(
                f"[{timestamp}] Mouse scrolled {direction} at ({x}, {y})\n"
            )
            
            # Auto-flush buffer if it gets too large
            if len(self.buffer) > 50:
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
        """Start the mouse logger"""
        if self.running:
            return
        
        self.running = True
        self.listener = mouse.Listener(
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )
        self.listener.start()
        print(f"[MouseLogger] Started logging to {self.log_file}")
    
    def stop(self):
        """Stop the mouse logger"""
        if not self.running:
            return
        
        self.running = False
        if self.listener:
            self.listener.stop()
        
        # Flush remaining buffer
        self.flush()
        print("[MouseLogger] Stopped")
