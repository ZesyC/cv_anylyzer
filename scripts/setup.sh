#!/bin/bash
# Auto-fix and setup script for CV Analyzer

set -e  # Exit on error

echo " CV Analyzer - Auto Setup & Fix Script"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN} $1${NC}"
}

print_error() {
    echo -e "${RED} $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ  $1${NC}"
}

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    print_error "Please run this script from the cv-analyzer/ directory"
    exit 1
fi

print_info "Step 1/4: Checking Python..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
print_success "Found $PYTHON_VERSION"

print_info "Step 2/4: Checking Node.js..."
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed."
    print_info "Please install from: https://nodejs.org/"
    print_info "You can continue with backend only, but frontend won't work."
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    SKIP_FRONTEND=true
else
    NODE_VERSION=$(node --version)
    print_success "Found Node.js $NODE_VERSION"
    SKIP_FRONTEND=false
fi

echo ""
print_info "Step 3/4: Setting up Backend..."

cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_success "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
print_info "Installing Python dependencies..."
pip install --upgrade pip > /dev/null
pip install -r requirements.txt
print_success "Python dependencies installed"

cd ..

if [ "$SKIP_FRONTEND" = false ]; then
    echo ""
    print_info "Step 4/4: Setting up Frontend..."
    
    cd frontend
    
    # Install npm dependencies
    print_info "Installing Node.js dependencies (this may take a few minutes)..."
    npm install
    print_success "Node.js dependencies installed"
    
    cd ..
else
    print_info "Step 4/4: Skipping frontend setup (Node.js not available)"
fi

echo ""
echo "========================================"
print_success "Setup Complete!"
echo "========================================"
echo ""
echo " Next Steps:"
echo ""
echo "1.  Start Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""
if [ "$SKIP_FRONTEND" = false ]; then
    echo "2.  Start Frontend (Terminal 2):"
    echo "   cd frontend"
    echo "   npm run dev"
    echo ""
    echo "3.  Open http://localhost:5173 in your browser"
else
    echo "  Frontend not set up. Install Node.js and run this script again."
fi
echo ""
print_success "All errors should be fixed now!"
