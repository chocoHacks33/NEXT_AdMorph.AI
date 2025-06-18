#!/bin/bash

# AdMorph.AI Full Stack Startup Script
# This script starts both the agentic backend and Next.js frontend

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

# Check if backend repository exists
BACKEND_DIR="../admorph-agentic-backend"
if [ ! -d "$BACKEND_DIR" ]; then
    log_error "Backend repository not found at $BACKEND_DIR"
    log_info "Please clone the agentic backend repository:"
    log_info "git clone <backend-repo-url> ../admorph-agentic-backend"
    exit 1
fi

# Check if environment file exists
if [ ! -f ".env.local" ]; then
    log_warning "No .env.local file found"
    log_info "Creating .env.local from template..."
    cp .env.integration.example .env.local
    log_warning "Please edit .env.local with your API keys before continuing"
    exit 1
fi

log_info "🚀 Starting AdMorph.AI Full Stack..."

# Start backend services
log_info "Starting agentic backend services..."
cd "$BACKEND_DIR"

# Check if backend is already running
if curl -f http://localhost:8000/health &> /dev/null; then
    log_success "Backend is already running"
else
    log_info "Starting backend with Docker Compose..."
    docker-compose up -d
    
    # Wait for backend to be ready
    log_info "Waiting for backend to be ready..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost:8000/health &> /dev/null; then
            log_success "Backend is ready!"
            break
        fi
        
        log_info "Attempt $attempt/$max_attempts - waiting for backend..."
        sleep 5
        ((attempt++))
    done
    
    if [ $attempt -gt $max_attempts ]; then
        log_error "Backend failed to start within expected time"
        log_info "Check backend logs: cd $BACKEND_DIR && docker-compose logs"
        exit 1
    fi
fi

# Return to frontend directory
cd - > /dev/null

# Install frontend dependencies if needed
if [ ! -d "node_modules" ]; then
    log_info "Installing frontend dependencies..."
    npm install
fi

# Start frontend
log_info "Starting Next.js frontend..."
log_success "🎉 AdMorph.AI is starting up!"
echo
echo "📊 Services:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Health Check: http://localhost:8000/health"
echo
echo "🛑 To stop all services:"
echo "   Frontend: Ctrl+C"
echo "   Backend: cd $BACKEND_DIR && docker-compose down"
echo

# Start the frontend development server
npm run dev
