#!/bin/bash

# LocalShield VPN Installer
# Supported OS: Ubuntu/Debian, Fedora, macOS

echo "Starting LocalShield VPN installation..."

OS="$(uname -s)"
case "${OS}" in
    Linux*)
        if [ -f /etc/debian_version ]; then
            echo "Detected Debian/Ubuntu"
            sudo apt-get update
            sudo apt-get install -y wireguard python3-pip python3-venv libsqlite3-dev
        elif [ -f /etc/fedora-release ]; then
            echo "Detected Fedora"
            sudo dnf install -y wireguard-tools python3-pip sqlite-devel
        fi
        ;;
    Darwin*)
        echo "Detected macOS"
        brew install wireguard-tools python3
        ;;
    *)
        echo "Unsupported OS: ${OS}"
        exit 1
        ;;
esac

# Create virtual environment for backend
echo "Setting up Python backend..."
python3 -m venv .venv
source .venv/bin/activate
pip install cryptography keyring dnslib httpx fastapi uvicorn psutil pydantic

# Note: Tauri app would be pre-built as an executable or installed via npm for dev
echo "Installing frontend dependencies..."
npm install

echo "Installation complete!"
echo "To start the app in development mode, run: npm run tauri dev"
echo "To start the backend manually: source .venv/bin/activate && python src/backend/main.py"
