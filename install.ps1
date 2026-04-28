# LocalShield VPN Windows Installer

Write-Host "Starting LocalShield VPN installation for Windows..." -ForegroundColor Cyan

# 1. Check for Python (Try 'python', 'python3', or 'py')
$pythonCmd = ""
$testCmds = @("python", "python3", "py")

foreach ($cmd in $testCmds) {
    if (Get-Command $cmd -ErrorAction SilentlyContinue) {
        # Check if it's the Microsoft Store placeholder by checking its version output
        $version = & $cmd --version 2>$null
        if ($version -match "Python 3") {
            $pythonCmd = $cmd
            break
        }
    }
}

# If not found, try common installation paths
if ($pythonCmd -eq "") {
    $commonPaths = @(
        "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "C:\Python311\python.exe",
        "C:\Python312\python.exe"
    )
    foreach ($path in $commonPaths) {
        if (Test-Path $path) {
            $pythonCmd = $path
            break
        }
    }
}

if ($pythonCmd -ne "") {
    Write-Host "Found Python: $pythonCmd" -ForegroundColor Green
} else {
    Write-Host "Real Python not detected. Please install Python 3.11+ from python.org and ensure 'Add to PATH' is checked." -ForegroundColor Red
    exit
}

# 2. Check for Node.js
if (Get-Command npm -ErrorAction SilentlyContinue) {
    Write-Host "Found Node.js/npm." -ForegroundColor Green
} else {
    Write-Host "Node.js/npm not found. Please install Node.js from nodejs.org" -ForegroundColor Red
    exit
}

# 3. Setup Python Virtual Environment
Write-Host "Setting up Python backend..." -ForegroundColor Yellow
& $pythonCmd -m venv .venv
if (Test-Path ".\.venv\Scripts\pip.exe") {
    & ".\.venv\Scripts\python.exe" -m pip install cryptography keyring dnslib httpx fastapi uvicorn psutil pydantic
} else {
    Write-Host "Failed to create virtual environment." -ForegroundColor Red
}

# 4. Install Frontend Dependencies
Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
Set-Location -Path "src/frontend"
npm install
Set-Location -Path "../.."

# 5. Download WireGuard Installer
Write-Host "Downloading WireGuard Installer..." -ForegroundColor Yellow
$wgUrl = "https://download.wireguard.com/windows-client/wireguard-installer.exe"
$wgFile = "wireguard-installer.exe"
try {
    Invoke-WebRequest -Uri $wgUrl -OutFile $wgFile
    Write-Host "WireGuard Installer downloaded: $wgFile" -ForegroundColor Green
    Write-Host "Please run $wgFile to complete the system installation." -ForegroundColor Cyan
} catch {
    Write-Host "Failed to download WireGuard automatically. Please download it from: $wgUrl" -ForegroundColor Red
}

Write-Host "`nInstallation steps completed!" -ForegroundColor Green
Write-Host "1. Run wireguard-installer.exe (if not already installed)" -ForegroundColor White
Write-Host "2. Start the app: cd src/frontend; npm run tauri dev" -ForegroundColor Cyan
