import sqlite3
import os
import json
from cryptography.fernet import Fernet
import keyring

SERVICE_NAME = "LocalShieldVPN"
DB_KEY_ACCOUNT = "db_encryption_key"
DB_PATH = "peers.db"

def get_or_create_db_key():
    """
    Retrieves the DB encryption key from the keychain or generates a new one.
    """
    key = keyring.get_password(SERVICE_NAME, DB_KEY_ACCOUNT)
    if not key:
        key = Fernet.generate_key().decode()
        keyring.set_password(SERVICE_NAME, DB_KEY_ACCOUNT, key)
    return key.encode()

class PeerManager:
    def __init__(self):
        self.key = get_or_create_db_key()
        self.fernet = Fernet(self.key)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS peers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                public_key TEXT NOT NULL,
                preshared_key TEXT,
                allowed_ips TEXT DEFAULT '0.0.0.0/0, ::/0',
                is_active INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

    def add_peer(self, name, endpoint, public_key, preshared_key=None, allowed_ips='0.0.0.0/0, ::/0'):
        # Encrypt sensitive data if needed, but since we are encrypting the whole DB file 
        # (simulated here by encrypting fields), we'll encrypt public/preshared keys.
        enc_public_key = self.fernet.encrypt(public_key.encode()).decode()
        enc_psk = self.fernet.encrypt(preshared_key.encode()).decode() if preshared_key else None
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO peers (name, endpoint, public_key, preshared_key, allowed_ips)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, endpoint, enc_public_key, enc_psk, allowed_ips))
        conn.commit()
        conn.close()

    def get_peers(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, endpoint, public_key, preshared_key, allowed_ips, is_active FROM peers')
        rows = cursor.fetchall()
        conn.close()

        peers = []
        for row in rows:
            try:
                dec_public_key = self.fernet.decrypt(row[3].encode()).decode()
                dec_psk = self.fernet.decrypt(row[4].encode()).decode() if row[4] else None
            except Exception:
                # Key might have changed or data corrupted
                dec_public_key = "[DECRYPTION ERROR]"
                dec_psk = None

            peers.append({
                "id": row[0],
                "name": row[1],
                "endpoint": row[2],
                "public_key": dec_public_key,
                "preshared_key": dec_psk,
                "allowed_ips": row[5],
                "is_active": bool(row[6])
            })
        return peers

    def delete_peer(self, peer_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM peers WHERE id = ?', (peer_id,))
        conn.commit()
        conn.close()

    def import_conf(self, conf_content):
        """
        Parses a WireGuard .conf file and adds it as a peer.
        """
        # Simple parser for [Peer] section
        lines = conf_content.splitlines()
        peer_data = {}
        for line in lines:
            line = line.strip()
            if line.startswith("PublicKey"):
                peer_data['public_key'] = line.split("=")[1].strip()
            elif line.startswith("Endpoint"):
                peer_data['endpoint'] = line.split("=")[1].strip()
            elif line.startswith("AllowedIPs"):
                peer_data['allowed_ips'] = line.split("=")[1].strip()
            elif line.startswith("PresharedKey"):
                peer_data['preshared_key'] = line.split("=")[1].strip()
        
        if 'public_key' in peer_data and 'endpoint' in peer_data:
            name = peer_data['endpoint'].split(":")[0]
            self.add_peer(name, peer_data['endpoint'], peer_data['public_key'], 
                          peer_data.get('preshared_key'), peer_data.get('allowed_ips', '0.0.0.0/0, ::/0'))
            return True
        return False
