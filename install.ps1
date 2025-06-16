# Google Workspace Bulk Email Creator - Windows Installer
# https://github.com/systemaudit/google-workspace-bulk-email
# Run as: powershell -ExecutionPolicy Bypass -File install.ps1

# Check if running as administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script requires Administrator privileges for best results" -ForegroundColor Yellow
    Write-Host "Some features may not work without admin rights" -ForegroundColor Yellow
    Write-Host ""
}

# Header
Clear-Host
Write-Host "================================================" -ForegroundColor Blue
Write-Host "  Google Workspace Bulk Email Creator Setup" -ForegroundColor Blue
Write-Host "  Windows Installation" -ForegroundColor Blue
Write-Host "================================================" -ForegroundColor Blue
Write-Host ""

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
$python3 = Get-Command python3 -ErrorAction SilentlyContinue

if ($python3) {
    $pythonCmd = "python3"
    $pipCmd = "pip3"
} elseif ($python) {
    $pythonCmd = "python"
    $pipCmd = "pip"
} else {
    Write-Host "✗ Python not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Would you like to download Python? (Y/N): " -ForegroundColor Yellow -NoNewline
    $response = Read-Host
    
    if ($response -eq 'Y' -or $response -eq 'y') {
        Write-Host "Opening Python download page..." -ForegroundColor Green
        Start-Process "https://www.python.org/downloads/"
        Write-Host ""
        Write-Host "Please install Python and run this script again" -ForegroundColor Yellow
        Write-Host "Make sure to check 'Add Python to PATH' during installation!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit
    } else {
        Write-Host "Please install Python 3.6+ manually" -ForegroundColor Red
        exit
    }
}

# Check Python version
$version = & $pythonCmd --version 2>&1
Write-Host "✓ $version found" -ForegroundColor Green

# Check pip
Write-Host ""
Write-Host "Checking pip installation..." -ForegroundColor Yellow
try {
    $pipVersion = & $pipCmd --version 2>&1
    Write-Host "✓ pip found" -ForegroundColor Green
} catch {
    Write-Host "Installing pip..." -ForegroundColor Yellow
    & $pythonCmd -m ensurepip --default-pip
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists" -ForegroundColor Yellow
    $response = Read-Host "Do you want to recreate it? (Y/N)"
    if ($response -eq 'Y' -or $response -eq 'y') {
        Remove-Item -Recurse -Force venv
        & $pythonCmd -m venv venv
        Write-Host "✓ Virtual environment recreated" -ForegroundColor Green
    }
} else {
    & $pythonCmd -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Install requirements
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
& python -m pip install --upgrade pip
& pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Create config files
Write-Host ""
Write-Host "Setting up configuration files..." -ForegroundColor Yellow

# domain.txt
if (-not (Test-Path "domain.txt")) {
    Write-Host "Creating domain.txt..." -ForegroundColor Yellow
    $domain = Read-Host "Enter your Google Workspace domain (e.g., company.com)"
    Set-Content -Path "domain.txt" -Value $domain
    Write-Host "✓ domain.txt created" -ForegroundColor Green
} else {
    Write-Host "✓ domain.txt already exists" -ForegroundColor Green
}

# password.txt
if (-not (Test-Path "password.txt")) {
    Set-Content -Path "password.txt" -Value "Email123@"
    Write-Host "✓ password.txt created with default password" -ForegroundColor Green
} else {
    Write-Host "✓ password.txt already exists" -ForegroundColor Green
}

# nama.txt
if (-not (Test-Path "nama.txt")) {
    $namaContent = @"
# Name database for email generation
# Format: DEPAN (first names) or BELAKANG (last names) followed by names

DEPAN Andi Budi Citra Dewi Eko Fitri Galih Hani Indra Joko Kartika Lestari Maya Novi Oki Putri Rina Sari Tari Umar Vina Wulan Yuni Zaki
BELAKANG Pratama Sari Putra Dewi Santoso Lestari Wijaya Rahayu Setiawan Wati Kusuma Anggraini Nugroho Safitri Permana
"@
    Set-Content -Path "nama.txt" -Value $namaContent
    Write-Host "✓ nama.txt created with default names" -ForegroundColor Green
} else {
    Write-Host "✓ nama.txt already exists" -ForegroundColor Green
}

# Create run script
Write-Host ""
Write-Host "Creating run script..." -ForegroundColor Yellow
$runBat = @"
@echo off
call venv\Scripts\activate.bat
python bot.py
pause
"@
Set-Content -Path "run.bat" -Value $runBat
Write-Host "✓ run.bat created" -ForegroundColor Green

# Create PowerShell run script
$runPs1 = @"
# Activate virtual environment and run the bot
& "venv\Scripts\Activate.ps1"
python bot.py
Read-Host "Press Enter to exit"
"@
Set-Content -Path "run.ps1" -Value $runPs1
Write-Host "✓ run.ps1 created" -ForegroundColor Green

# Summary
Write-Host ""
Write-Host "================================================" -ForegroundColor Blue
Write-Host "✅ Installation Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Blue
Write-Host ""
Write-Host "To run the application:" -ForegroundColor White
Write-Host "  Option 1: Double-click run.bat" -ForegroundColor Yellow
Write-Host "  Option 2: PowerShell: .\run.ps1" -ForegroundColor Yellow
Write-Host "  Option 3: Manual:" -ForegroundColor Yellow
Write-Host "    venv\Scripts\activate" -ForegroundColor Gray
Write-Host "    python bot.py" -ForegroundColor Gray
Write-Host ""
Write-Host "Configuration files:" -ForegroundColor White
Write-Host "  • domain.txt   - Your Google Workspace domain" -ForegroundColor Gray
Write-Host "  • password.txt - Default password for new accounts" -ForegroundColor Gray
Write-Host "  • nama.txt     - Name database" -ForegroundColor Gray
Write-Host ""
Write-Host "Note: You'll need to set up OAuth2 on first run" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Blue
Write-Host ""
Read-Host "Press Enter to exit"
