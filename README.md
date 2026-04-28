# 🛡️ LocalShield VPN

LocalShield is a high-performance, decentralized, and 100% free VPN application for Windows, macOS, and Linux. Built with **WireGuard**, **Python**, and **Tauri**, it puts the user in total control of their privacy.

---

## 🚀 How to Use (For End-Users)

If you have downloaded the finished `.exe`, `.dmg`, or `.deb` installer from GitHub:
1.  **Install WireGuard**: Ensure the official WireGuard client is installed on your system ([Download here](https://www.wireguard.com/install/)).
2.  **Launch LocalShield**: Run the application.
3.  **Setup Exit Node**: LocalShield is a "Bring Your Own Server" (BYOS) VPN. You will need a WireGuard peer config (`.conf`) to connect. (See the "Self-Hosting" section below).
4.  **Import & Connect**: Import your config and click **Connect**.

---

## 🛠️ Development Setup (For Developers)

To build, modify, or run LocalShield from source, follow these steps:

### 1. Prerequisites
- **Python 3.11+**: Ensure it's added to your PATH.
- **Node.js 20+**: For the React frontend.
- **Rust & Cargo**: Required for Tauri. [Install Rust](https://www.rust-lang.org/tools/install).
- **C++ Build Tools (Windows Only)**: Install [Visual Studio Build Tools](https://aka.ms/vs/17/release/vs_BuildTools.exe) and select the **"Desktop development with C++"** workload.

### 2. Local Installation
Run the automated installer for your OS:
- **Windows**: `.\install.ps1`
- **Linux/macOS**: `bash install.sh`

### 3. Run in Dev Mode
```powershell
cd src/frontend
npm install
npm run tauri dev
```

---

## 🌐 Self-Hosting Your VPN Server (Exit Node)

For maximum privacy, we recommend hosting your own exit node on **Oracle Cloud (Always Free Tier)**.

### 1. Create a VPS
- Sign up for [Oracle Cloud](https://www.oracle.com/cloud/free/).
- Create a **"VM.Standard.A1.Flex"** (ARM) or **"VM.Standard.E2.1.Micro"** instance.
- Select **Ubuntu 22.04** as the image.

### 2. Automated WireGuard Install
SSH into your new server and run:
```bash
wget https://git.io/wireguard -O wireguard-install.sh && bash wireguard-install.sh
```
- Follow the prompts to create a client (e.g., `client1`).
- The script will generate a `.conf` file.

### 3. Import to LocalShield
- Copy the content of the `.conf` file from your server.
- In LocalShield, go to **Peers > Import .conf** and paste the configuration.
- Click **Connect** to secure your traffic!

---

## 🤖 Automated Deployment (GitHub Actions)

This project is pre-configured with a GitHub Action to build and release binaries automatically.
1.  Push this code to your GitHub repository.
2.  Go to **Actions** to see the build progress.
3.  Once finished, your installers will be available in the **Releases** section of your repo.

---

## 🔒 Security Features
- **Zero-Logs**: No data ever leaves your machine.
- **OS Keychain**: Private keys are stored in your system's secure vault.
- **Kill Switch**: Blocks all traffic if the tunnel drops (configurable in Settings).
- **DNS-over-HTTPS**: Prevents DNS leaks by routing queries through Cloudflare/Google.

*LocalShield is open-source and free forever.*
