@echo off
REM Google Workspace Bulk Email Creator - Windows Batch Installer
REM https://github.com/systemaudit/google-workspace-bulk-email

cls
echo ================================================
echo   Google Workspace Bulk Email Creator Setup
echo   Windows Installation (Batch)
echo ================================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Python not found!
        echo.
        echo Please install Python 3.6+ from:
        echo https://www.python.org/downloads/
        echo.
        echo Make sure to check "Add Python to PATH" during installation!
        echo.
        pause
        exit /b 1
    ) else (
        set PYTHON=python3
        set PIP=pip3
    )
) else (
    set PYTHON=python
    set PIP=pip
)

%PYTHON% --version
echo Python found!
echo.

REM Check pip
echo Checking pip installation...
%PIP% --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pip...
    %PYTHON% -m ensurepip --default-pip
)

REM Create virtual environment
echo.
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
    choice /C YN /M "Do you want to recreate it?"
    if errorlevel 2 goto :skip_venv
    rmdir /s /q venv
)
%PYTHON% -m venv venv
echo Virtual environment created!
:skip_venv

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo.
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Dependencies installed!

REM Create config files
echo.
echo Setting up configuration files...

REM domain.txt
if not exist domain.txt (
    echo.
    set /p domain="Enter your Google Workspace domain (e.g., company.com): "
    echo %domain%>domain.txt
    echo domain.txt created!
) else (
    echo domain.txt already exists
)

REM password.txt
if not exist password.txt (
    echo Email123@>password.txt
    echo password.txt created with default password
) else (
    echo password.txt already exists
)

REM nama.txt
if not exist nama.txt (
    (
    echo # Name database for email generation
    echo # Format: DEPAN ^(first names^) or BELAKANG ^(last names^) followed by names
    echo.
    echo DEPAN Andi Budi Citra Dewi Eko Fitri Galih Hani Indra Joko Kartika Lestari Maya Novi Oki Putri Rina Sari Tari Umar Vina Wulan Yuni Zaki
    echo BELAKANG Pratama Sari Putra Dewi Santoso Lestari Wijaya Rahayu Setiawan Wati Kusuma Anggraini Nugroho Safitri Permana
    ) > nama.txt
    echo nama.txt created with default names
) else (
    echo nama.txt already exists
)

REM Create run.bat if not exists
if not exist run.bat (
    (
    echo @echo off
    echo call venv\Scripts\activate.bat
    echo python bot.py
    echo pause
    ) > run.bat
    echo run.bat created!
)

REM Summary
echo.
echo ================================================
echo Installation Complete!
echo ================================================
echo.
echo To run the application:
echo   - Double-click: run.bat
echo   - Or run: venv\Scripts\activate then python bot.py
echo.
echo Configuration files:
echo   - domain.txt   : Your Google Workspace domain
echo   - password.txt : Default password for new accounts
echo   - nama.txt     : Name database
echo.
echo Note: You'll need to set up OAuth2 on first run
echo ================================================
echo.
pause
