import subprocess
import os
import threading
import time
import platform
from keygen import get_private_key

CONF_PATH = "wg0.conf"

class TunnelManager:
    def __init__(self):
        self.is_connected = False
        self.current_peer = None
        self._watchdog_thread = None
        self._stop_watchdog = threading.Event()

    def start(self, peer_config):
        """
        Starts the WireGuard tunnel.
        peer_config: dict with {endpoint, public_key, allowed_ips, preshared_key}
        """
        priv_key = get_private_key()
        if not priv_key:
            raise Exception("Private key not found. Run keygen first.")

        # Generate wg0.conf
        conf_content = f"""[Interface]
PrivateKey = {priv_key}
Address = 10.0.0.2/24
DNS = 127.0.0.1

[Peer]
PublicKey = {peer_config['public_key']}
Endpoint = {peer_config['endpoint']}
AllowedIPs = {peer_config['allowed_ips']}
"""
        if peer_config.get('preshared_key'):
            conf_content += f"PresharedKey = {peer_config['preshared_key']}\n"

        with open(CONF_PATH, "w") as f:
            f.write(conf_content)

        # Run wg-quick
        try:
            if platform.system() == "Windows":
                # On Windows, wg-quick might not be available directly, 
                # often uses 'wireguard /installservice' or similar.
                # Assuming 'wireguard' CLI is in path or 'wg'
                subprocess.run(["wg-quick", "up", os.path.abspath(CONF_PATH)], check=True)
            else:
                subprocess.run(["sudo", "wg-quick", "up", os.path.abspath(CONF_PATH)], check=True)
            
            self.is_connected = True
            self.current_peer = peer_config
            self._start_watchdog()
            return True
        except Exception as e:
            print(f"Failed to start tunnel: {e}")
            return False

    def stop(self):
        self._stop_watchdog.set()
        try:
            if platform.system() == "Windows":
                subprocess.run(["wg-quick", "down", os.path.abspath(CONF_PATH)], check=True)
            else:
                subprocess.run(["sudo", "wg-quick", "down", os.path.abspath(CONF_PATH)], check=True)
            self.is_connected = False
            return True
        except Exception:
            return False

    def status(self):
        # Simplified status
        latency = self._check_latency() if self.is_connected else -1
        return {
            "connected": self.is_connected,
            "peer": self.current_peer["name"] if self.current_peer else None,
            "latency": latency
        }

    def _check_latency(self):
        # Ping check
        try:
            # Ping 1.1.1.1 or the peer endpoint
            host = "1.1.1.1"
            param = "-n" if platform.system() == "Windows" else "-c"
            output = subprocess.check_output(["ping", param, "1", host]).decode()
            # Parse latency from output (simplified)
            if "time=" in output:
                return float(output.split("time=")[1].split("ms")[0])
            return 0
        except Exception:
            return -1

    def _start_watchdog(self):
        self._stop_watchdog.clear()
        self._watchdog_thread = threading.Thread(target=self._watchdog_loop, daemon=True)
        self._watchdog_thread.start()

    def _watchdog_loop(self):
        while not self._stop_watchdog.is_set():
            if self.is_connected:
                latency = self._check_latency()
                if latency == -1:
                    print("Tunnel health check failed. Reconnecting...")
                    # Logic to auto-reconnect could go here
            time.sleep(10)
