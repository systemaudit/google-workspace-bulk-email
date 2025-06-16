# Google Workspace Bulk Email Creator

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6%2B-brightgreen.svg)](https://www.python.org/downloads/)
[![Google API](https://img.shields.io/badge/Google%20API-Admin%20SDK-orange.svg)](https://developers.google.com/admin-sdk)

Automated bulk email account creation tool for Google Workspace (formerly G Suite) administrators. Streamline the process of creating multiple user accounts with customizable settings and comprehensive logging.

## 🚀 Features

- **Automated OAuth2 Setup** - Simplified authentication process with step-by-step guidance
- **Bulk Account Creation** - Create multiple accounts efficiently with rate limiting protection
- **Customizable Configuration** - Easy-to-edit configuration files for domains, passwords, and user names
- **Dual Mode Operation** - Automatic detection for VPS or local environment
- **Comprehensive Logging** - Detailed output files with creation results
- **Error Handling** - Robust error handling with retry mechanisms
- **Name Database** - Built-in Indonesian name database with easy customization

## 📋 Requirements

- Python 3.6 or higher
- Google Workspace administrator account
- Admin SDK API enabled in Google Cloud Console
- Network connectivity

## 🛠️ Installation

### 🐧 Linux/VPS

#### One-line Installation
```bash
git clone https://github.com/systemaudit/google-workspace-bulk-email.git && cd google-workspace-bulk-email && chmod +x install.sh && ./install.sh
```

#### Manual Installation
```bash
# Clone repository
git clone https://github.com/systemaudit/google-workspace-bulk-email.git
cd google-workspace-bulk-email

# Make installer executable
chmod +x install.sh

# Run installer
./install.sh
```

The installer will:
- Check and install Python if needed
- Create virtual environment
- Install all dependencies
- Set up configuration files
- Create run script

### 🪟 Windows

#### PowerShell Installation (Recommended)
```powershell
# Download installer
curl -O https://raw.githubusercontent.com/systemaudit/google-workspace-bulk-email/main/install.ps1

# Run installer (may need to allow execution)
powershell -ExecutionPolicy Bypass -File install.ps1
```

#### Batch File Installation
```cmd
# Download and run install.bat
# Double-click install.bat or run from command prompt
install.bat
```

#### Manual Installation
```cmd
# Clone repository
git clone https://github.com/systemaudit/google-workspace-bulk-email.git
cd google-workspace-bulk-email

# Install dependencies
pip install -r requirements.txt

# Run application
python bot.py
```

### 🐳 Docker

#### Using Docker Compose
```bash
# Clone repository
git clone https://github.com/systemaudit/google-workspace-bulk-email.git
cd google-workspace-bulk-email

# Build and run
docker-compose up --build
```

#### Using Docker directly
```bash
# Build image
docker build -t gsuite-email-generator .

# Run container
docker run -it \
  -v $(pwd)/domain.txt:/app/domain.txt \
  -v $(pwd)/password.txt:/app/password.txt \
  -v $(pwd)/nama.txt:/app/nama.txt \
  -v $(pwd)/credentials.json:/app/credentials.json \
  -v $(pwd)/token.json:/app/token.json \
  -v $(pwd)/output:/app/output \
  gsuite-email-generator
```

## ⚙️ Configuration

### Google Cloud Setup

1. Navigate to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable Admin SDK API:
   - Go to **APIs & Services** > **Library**
   - Search for "Admin SDK API"
   - Click **Enable**
4. Create OAuth2 credentials:
   - Go to **APIs & Services** > **Credentials**
   - Click **+ CREATE CREDENTIALS** > **OAuth client ID**
   - Select **Web application**
   - Add authorized redirect URI: `http://localhost:8080`
   - Download credentials JSON

### Application Configuration

The application uses the following configuration files:

- `domain.txt` - Your Google Workspace domain
- `password.txt` - Default password for new accounts
- `nama.txt` - Name database for account generation

## 📖 Usage

### Quick Start

After installation, run the application:

#### Linux/VPS
```bash
./run.sh
```

#### Windows
```cmd
run.bat
```
or
```powershell
.\run.ps1
```

#### Docker
```bash
docker-compose run gsuite-email-generator
```

### First Run

The application will:
1. Detect your environment (VPS/Local)
2. Guide through OAuth2 setup
3. Create necessary configuration files
4. Begin account creation process

### Subsequent Runs

Simply run the application and enter the number of accounts to create when prompted.

## 📁 Project Structure

```
google-workspace-bulk-email/
├── bot.py              # Main application
├── requirements.txt    # Python dependencies
├── install.sh          # Linux/VPS installer
├── install.ps1         # Windows PowerShell installer
├── install.bat         # Windows batch installer
├── run.sh              # Linux run script (created by installer)
├── run.bat             # Windows run script (created by installer)
├── run.ps1             # PowerShell run script (created by installer)
├── docker-compose.yml  # Docker compose configuration
├── Dockerfile          # Docker image definition
├── domain.txt          # Domain configuration
├── password.txt        # Default password
├── nama.txt            # Name database
├── .gitignore          # Git ignore rules
├── LICENSE             # MIT License
└── README.md           # Documentation
```

## 🔒 Security Considerations

- Never commit `credentials.json` or `token.json` to version control
- Use strong passwords for created accounts
- Regularly rotate OAuth2 credentials
- Monitor API usage to stay within quotas
- Enable 2FA on administrator accounts

## 📊 Output Format

Results are saved to `results_YYYYMMDD_HHMMSS.txt` with the following format:

```
============================================================
GOOGLE WORKSPACE BULK EMAIL CREATION RESULTS
Generated: 2024-01-15 10:30:45
Domain: company.com
============================================================

Email | Password | Full Name
------------------------------------------------------------
john.doe@company.com | Email123@ | John Doe
jane.smith@company.com | Email123@ | Jane Smith
```

## 🐛 Troubleshooting

### Common Issues

**OAuth2 Error: redirect_uri_mismatch**
- Ensure redirect URI in Google Cloud Console matches exactly: `http://localhost:8080`
- No trailing slashes or additional parameters

**API Quota Exceeded**
- Google Workspace has rate limits
- The application includes automatic delays
- Wait before retrying if quota is exceeded

**Token Expired**
- The application will automatically refresh tokens
- If refresh fails, re-authenticate by deleting `token.json`

**Permission Denied (Linux/Mac)**
- Make scripts executable: `chmod +x install.sh run.sh`

**PowerShell Execution Policy (Windows)**
- Run: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- Or use: `powershell -ExecutionPolicy Bypass -File install.ps1`

### Environment-Specific Issues

**VPS/Headless Server**
- The application automatically detects VPS environment
- Uses manual OAuth2 flow (copy-paste URLs)
- No browser required on server

**Docker Issues**
- Ensure configuration files exist before running
- Mount volumes correctly for persistent data
- Check file permissions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Workspace Admin SDK documentation
- Python Google API Client library contributors
- Open source community

## 📞 Support

For issues, questions, or contributions, please open an issue in the GitHub repository.

---

**Note**: This tool is intended for legitimate administrative use only. Ensure compliance with your organization's policies and Google Workspace terms of service.
