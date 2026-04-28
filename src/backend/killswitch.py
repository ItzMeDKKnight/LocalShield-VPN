import os
import sys
import subprocess
import platform

class KillSwitch:
    def __init__(self):
        self.os_type = platform.system()

    def enable(self):
        """
        Blocks all traffic except to the VPN endpoint and local loopback.
        """
        if self.os_type == "Windows":
            self._enable_windows()
        elif self.os_type == "Linux":
            self._enable_linux()
        elif self.os_type == "Darwin":
            self._enable_macos()

    def disable(self):
        """
        Restores normal networking.
        """
        if self.os_type == "Windows":
            self._disable_windows()
        elif self.os_type == "Linux":
            self._disable_linux()
        elif self.os_type == "Darwin":
            self._disable_macos()

    def _enable_windows(self):
        # Using netsh as a reliable alternative to complex WFP ctypes
        # Block all outbound traffic by default
        subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "firewallpolicy", "blockoutbound,allowinbound"], check=True)
        # Allow loopback
        subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", "name=LocalShield-Loopback", "dir=out", "action=allow", "remoteip=127.0.0.1"], check=True)
        # Allow WireGuard (UDP 51820 by default, should be dynamic)
        subprocess.run(["netsh", "advfirewall", "firewall", "add", "rule", "name=LocalShield-VPN", "dir=out", "action=allow", "protocol=UDP", "remoteport=51820"], check=True)

    def _disable_windows(self):
        subprocess.run(["netsh", "advfirewall", "set", "allprofiles", "firewallpolicy", "allowoutbound,allowinbound"], check=True)
        subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", "name=LocalShield-Loopback"], check=False)
        subprocess.run(["netsh", "advfirewall", "firewall", "delete", "rule", "name=LocalShield-VPN"], check=False)

    def _enable_linux(self):
        # iptables rules
        subprocess.run(["iptables", "-P", "OUTPUT", "DROP"], check=True)
        subprocess.run(["iptables", "-A", "OUTPUT", "-o", "lo", "-j", "ACCEPT"], check=True)
        subprocess.run(["iptables", "-A", "OUTPUT", "-o", "wg0", "-j", "ACCEPT"], check=True)
        # Allow connection to VPN endpoint (port 51820)
        subprocess.run(["iptables", "-A", "OUTPUT", "-p", "udp", "--dport", "51820", "-j", "ACCEPT"], check=True)

    def _disable_linux(self):
        subprocess.run(["iptables", "-P", "OUTPUT", "ACCEPT"], check=True)
        subprocess.run(["iptables", "-F", "OUTPUT"], check=True)

    def _enable_macos(self):
        # pfctl rules
        rules = "block drop out all\npass out on lo0 all\npass out on utun0 all\n"
        with open("/tmp/ls_pf.conf", "w") as f:
            f.write(rules)
        subprocess.run(["pfctl", "-e", "-f", "/tmp/ls_pf.conf"], check=True)

    def _disable_macos(self):
        subprocess.run(["pfctl", "-d"], check=True)

if __name__ == "__main__":
    ks = KillSwitch()
    if len(sys.argv) > 1:
        if sys.argv[1] == "on":
            ks.enable()
        else:
            ks.disable()
