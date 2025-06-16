#!/bin/bash
# Quick installer for Google Workspace Bulk Email Creator
# This script clones the repo and runs the installer

set -e

echo "=========================================="
echo "Google Workspace Bulk Email Creator"
echo "Quick Installer"
echo "=========================================="
echo ""

# Clone repository
if [ -d "google-workspace-bulk-email" ]; then
    echo "Directory already exists. Updating..."
    cd google-workspace-bulk-email
    git pull
else
    echo "Cloning repository..."
    git clone https://github.com/systemaudit/google-workspace-bulk-email.git
    cd google-workspace-bulk-email
fi

# Make installer executable
chmod +x install.sh

# Run installer
./install.sh
