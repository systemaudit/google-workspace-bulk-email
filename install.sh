#!/bin/bash

# Google Workspace Bulk Email Creator - Linux/VPS Installer
# https://github.com/systemaudit/google-workspace-bulk-email

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Header
clear
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  Google Workspace Bulk Email Creator Setup${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Check OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo -e "${GREEN}✓ Linux detected${NC}"
else
    echo -e "${YELLOW}⚠ This installer is designed for Linux/VPS${NC}"
    echo "For other OS, please use the appropriate installer"
    exit 1
fi

# Check Python
echo -e "\n${YELLOW}Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
    
    # Check version
    REQUIRED_VERSION="3.6"
    if python3 -c "import sys; exit(0 if sys.version_info >= (3,6) else 1)"; then
        echo -e "${GREEN}✓ Python version is compatible${NC}"
    else
        echo -e "${RED}✗ Python 3.6+ required${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ Python 3 not found${NC}"
    echo ""
    echo "Installing Python 3..."
    
    # Detect package manager
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y python3 python3-pip python3-venv
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3 python3-pip
    else
        echo -e "${RED}Unable to install Python automatically${NC}"
        echo "Please install Python 3.6+ manually"
        exit 1
    fi
fi

# Check pip
echo -e "\n${YELLOW}Checking pip installation...${NC}"
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓ pip3 found${NC}"
else
    echo -e "${YELLOW}Installing pip3...${NC}"
    python3 -m ensurepip --default-pip 2>/dev/null || {
        curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        python3 get-pip.py
        rm get-pip.py
    }
fi

# Create virtual environment
echo -e "\n${YELLOW}Creating virtual environment...${NC}"
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists${NC}"
    read -p "Do you want to recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo -e "${GREEN}✓ Virtual environment recreated${NC}"
    fi
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "\n${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install requirements
echo -e "\n${YELLOW}Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Create config files if not exists
echo -e "\n${YELLOW}Setting up configuration files...${NC}"

# domain.txt
if [ ! -f "domain.txt" ]; then
    echo -e "${YELLOW}Creating domain.txt...${NC}"
    read -p "Enter your Google Workspace domain (e.g., company.com): " domain
    echo "$domain" > domain.txt
    echo -e "${GREEN}✓ domain.txt created${NC}"
else
    echo -e "${GREEN}✓ domain.txt already exists${NC}"
fi

# password.txt
if [ ! -f "password.txt" ]; then
    echo "Email123@" > password.txt
    echo -e "${GREEN}✓ password.txt created with default password${NC}"
else
    echo -e "${GREEN}✓ password.txt already exists${NC}"
fi

# nama.txt
if [ ! -f "nama.txt" ]; then
    cat > nama.txt << 'EOF'
# Name database for email generation
# Format: DEPAN (first names) or BELAKANG (last names) followed by names

DEPAN Andi Budi Citra Dewi Eko Fitri Galih Hani Indra Joko Kartika Lestari Maya Novi Oki Putri Rina Sari Tari Umar Vina Wulan Yuni Zaki
BELAKANG Pratama Sari Putra Dewi Santoso Lestari Wijaya Rahayu Setiawan Wati Kusuma Anggraini Nugroho Safitri Permana
EOF
    echo -e "${GREEN}✓ nama.txt created with default names${NC}"
else
    echo -e "${GREEN}✓ nama.txt already exists${NC}"
fi

# Create run script
echo -e "\n${YELLOW}Creating run script...${NC}"
cat > run.sh << 'EOF'
#!/bin/bash
# Activate virtual environment and run the bot
source venv/bin/activate
python3 bot.py
EOF
chmod +x run.sh
echo -e "${GREEN}✓ run.sh created${NC}"

# Summary
echo -e "\n${BLUE}================================================${NC}"
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""
echo -e "To run the application:"
echo -e "  ${YELLOW}./run.sh${NC}"
echo ""
echo -e "Or manually:"
echo -e "  ${YELLOW}source venv/bin/activate${NC}"
echo -e "  ${YELLOW}python3 bot.py${NC}"
echo ""
echo -e "Configuration files:"
echo -e "  • domain.txt   - Your Google Workspace domain"
echo -e "  • password.txt - Default password for new accounts"
echo -e "  • nama.txt     - Name database"
echo ""
echo -e "${YELLOW}Note: You'll need to set up OAuth2 on first run${NC}"
echo -e "${BLUE}================================================${NC}"
