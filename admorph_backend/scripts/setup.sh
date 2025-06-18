#!/bin/bash

# AdMorph.AI Backend Setup Script
# This script sets up the development environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_python() {
    log_info "Checking Python installation..."
    
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed. Please install Python 3.11 or higher."
        exit 1
    fi
    
    local python_version=$(python3 --version | cut -d' ' -f2)
    local major_version=$(echo $python_version | cut -d'.' -f1)
    local minor_version=$(echo $python_version | cut -d'.' -f2)
    
    if [ "$major_version" -lt 3 ] || ([ "$major_version" -eq 3 ] && [ "$minor_version" -lt 11 ]); then
        log_error "Python 3.11 or higher is required. Found: $python_version"
        exit 1
    fi
    
    log_success "Python $python_version found"
}

setup_virtual_environment() {
    log_info "Setting up virtual environment..."
    cd "$PROJECT_DIR"
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        log_success "Virtual environment created"
    else
        log_info "Virtual environment already exists"
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    log_success "Virtual environment ready"
}

install_dependencies() {
    log_info "Installing Python dependencies..."
    cd "$PROJECT_DIR"
    
    # Ensure virtual environment is activated
    source venv/bin/activate
    
    # Install requirements
    pip install -r requirements.txt
    
    log_success "Dependencies installed"
}

setup_environment_file() {
    log_info "Setting up environment configuration..."
    cd "$PROJECT_DIR"
    
    if [ ! -f ".env" ]; then
        cp .env.example .env
        log_success "Environment file created from template"
        log_warning "Please edit .env file with your API keys and configuration"
        log_info "Required: OPENAI_API_KEY"
        log_info "Optional: META_ACCESS_TOKEN, META_APP_ID, META_APP_SECRET, META_AD_ACCOUNT_ID"
    else
        log_info "Environment file already exists"
    fi
}

create_directories() {
    log_info "Creating necessary directories..."
    cd "$PROJECT_DIR"
    
    mkdir -p uploads
    mkdir -p logs
    mkdir -p data
    
    log_success "Directories created"
}

run_tests() {
    log_info "Running basic tests..."
    cd "$PROJECT_DIR"
    
    # Ensure virtual environment is activated
    source venv/bin/activate
    
    # Run a simple import test
    python -c "
import sys
sys.path.append('.')
try:
    from admorph_backend.models.business import BusinessProfile
    from admorph_backend.config.settings import get_settings
    print('✅ Core modules import successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"
    
    log_success "Basic tests passed"
}

show_next_steps() {
    log_success "Setup completed successfully!"
    echo
    echo "🚀 Next steps:"
    echo "1. Edit .env file with your API keys:"
    echo "   nano .env"
    echo
    echo "2. Activate virtual environment:"
    echo "   source venv/bin/activate"
    echo
    echo "3. Start the development server:"
    echo "   python -m admorph_backend.api.main"
    echo
    echo "4. Or use the deployment script:"
    echo "   ./scripts/deploy.sh"
    echo
    echo "📚 Documentation:"
    echo "   README.md - Main documentation"
    echo "   INTEGRATION_GUIDE.md - Integration instructions"
    echo
    echo "🔗 URLs (when running):"
    echo "   API: http://localhost:8000"
    echo "   Docs: http://localhost:8000/docs"
    echo "   Health: http://localhost:8000/health"
}

main() {
    log_info "Setting up AdMorph.AI Backend development environment..."
    
    check_python
    setup_virtual_environment
    install_dependencies
    setup_environment_file
    create_directories
    run_tests
    show_next_steps
}

main "$@"
