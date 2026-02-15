"""
Activity logger module for tracking system and application activity
"""
import threading
import time
from datetime import datetime
import psutil
import config


class ActivityLogger:
    """Monitors and logs system activity"""
    
    def __init__(self, log_file=None, check_interval=60):
        self.log_file = log_file or config.ACTIVITY_LOG_FILE
        self.check_interval = check_interval
        self.running = False
        self.thread = None
        
    def get_system_info(self):
        """Get current system activity information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Get top processes by CPU usage
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage and get top 5
            top_processes = sorted(
                processes, 
                key=lambda x: x['cpu_percent'] if x['cpu_percent'] else 0, 
                reverse=True
            )[:5]
            
            return {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': memory.available / (1024**3),
                'disk_percent': disk.percent,
                'top_processes': top_processes
            }
        except Exception as e:
            return None
    
    def log_activity(self, activity_info):
        """Log system activity to file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_entry = (
            f"\n[{timestamp}] System Activity Report\n"
            f"CPU Usage: {activity_info['cpu_percent']}%\n"
            f"Memory Usage: {activity_info['memory_percent']}%\n"
            f"Memory Available: {activity_info['memory_available_gb']:.2f} GB\n"
            f"Disk Usage: {activity_info['disk_percent']}%\n"
            f"Top Processes:\n"
        )
        
        for i, proc in enumerate(activity_info['top_processes'], 1):
            log_entry += (
                f"  {i}. {proc['name']} (PID: {proc['pid']}) - "
                f"CPU: {proc['cpu_percent']}%\n"
            )
        
        log_entry += "-" * 50 + "\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def monitor_loop(self):
        """Main monitoring loop"""
        while self.running:
            activity_info = self.get_system_info()
            
            if activity_info:
                self.log_activity(activity_info)
            
            time.sleep(self.check_interval)
    
    def start(self):
        """Start the activity logger"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.thread.start()
        print(f"[ActivityLogger] Started logging to {self.log_file}")
    
    def stop(self):
        """Stop the activity logger"""
        if not self.running:
            return
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("[ActivityLogger] Stopped")
