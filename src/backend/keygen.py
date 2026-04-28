import base64
import keyring
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519

SERVICE_NAME = "LocalShieldVPN"
PRIVATE_KEY_ACCOUNT = "wg_private_key"

def generate_keypair():
    """
    Generates a WireGuard-compatible X25519 keypair.
    Returns: (private_key_b64, public_key_b64)
    """
    # Generate private key
    private_key = x25519.X25519PrivateKey.generate()
    
    # Get raw bytes for private key
    priv_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Generate public key
    public_key = private_key.public_key()
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    
    # WireGuard uses base64 encoding for keys
    priv_b64 = base64.b64encode(priv_bytes).decode('utf-8')
    pub_b64 = base64.b64encode(pub_bytes).decode('utf-8')
    
    return priv_b64, pub_b64

def save_private_key(priv_b64):
    """
    Saves the private key securely to the OS keychain.
    """
    keyring.set_password(SERVICE_NAME, PRIVATE_KEY_ACCOUNT, priv_b64)

def get_private_key():
    """
    Retrieves the private key from the OS keychain.
    """
    return keyring.get_password(SERVICE_NAME, PRIVATE_KEY_ACCOUNT)

def main():
    """
    CLI command: localshield keygen
    """
    print("Generating new WireGuard keypair...")
    priv, pub = generate_keypair()
    save_private_key(priv)
    print(f"Public Key: {pub}")
    print("Private key has been saved securely to the system keychain.")

if __name__ == "__main__":
    main()
