import time
import platform
import logging
from logging.handlers import RotatingFileHandler
import json

LOG_FILE = "localshield.log"

# Setup logging
logger = logging.getLogger("LocalShield")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class StatsManager:
    def __init__(self):
        self.start_time = time.time()
        self.last_io = self._get_network_io()

    def _get_network_io(self):
        """
        Gets bytes sent/received.
        On Linux: /proc/net/dev
        On others: simulated or using psutil-like logic (simplified for this script)
        """
        if platform.system() == "Linux":
            try:
                with open("/proc/net/dev", "r") as f:
                    lines = f.readlines()
                    # Just sum all interfaces for simplicity
                    sent, recv = 0, 0
                    for line in lines[2:]:
                        parts = line.split()
                        if len(parts) > 9:
                            recv += int(parts[1])
                            sent += int(parts[9])
                    return {"sent": sent, "recv": recv}
            except Exception:
                pass
        
        # Fallback for Windows/macOS (requires psutil for real data, 
        # but let's provide a skeleton that could be filled or used with psutil)
        try:
            import psutil
            io = psutil.net_io_counters()
            return {"sent": io.bytes_sent, "recv": io.bytes_recv}
        except ImportError:
            return {"sent": 0, "recv": 0}

    def get_stats(self):
        current_io = self._get_network_io()
        sent_speed = current_io["sent"] - self.last_io["sent"]
        recv_speed = current_io["recv"] - self.last_io["recv"]
        self.last_io = current_io

        return {
            "uptime": int(time.time() - self.start_time),
            "upload_speed": sent_speed,  # Bytes/sec (if called every second)
            "download_speed": recv_speed,
            "total_sent": current_io["sent"],
            "total_recv": current_io["recv"]
        }

def log_event(message, level="info"):
    if level == "info":
        logger.info(message)
    elif level == "error":
        logger.error(message)
    elif level == "warning":
        logger.warning(message)

if __name__ == "__main__":
    sm = StatsManager()
    while True:
        print(json.dumps(sm.get_stats(), indent=2))
        time.sleep(1)
