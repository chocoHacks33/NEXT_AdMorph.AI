#!/bin/bash

# =============================================================================
# 🚀 AdMorph.AI Full Stack Startup Script
# =============================================================================
# This script starts the complete AdMorph.AI platform with all integrated features
# =============================================================================

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}$1${NC}"
}

# Main startup function
main() {
    print_header "🤖 AdMorph.AI Full Stack Integration Startup"
    print_header "=============================================="
    echo ""
    
    # Check if we're in the right directory
    if [ ! -f "package.json" ] || [ ! -d "admorph_backend" ]; then
        print_error "Please run this script from the NEXT_AdMorph.AI root directory"
        exit 1
    fi
    
    # Check for required files
    print_status "Checking required files..."
    
    if [ ! -f ".env.local" ]; then
        print_warning ".env.local not found. Creating from template..."
        cp .env.example .env.local
        print_warning "Please edit .env.local and add your OpenAI API key before continuing"
        print_warning "Minimum required: OPENAI_API_KEY=your_key_here"
        echo ""
        read -p "Press Enter after you've updated .env.local with your API keys..."
    fi
    
    if [ ! -f "docker-compose.integration.yml" ]; then
        print_error "docker-compose.integration.yml not found!"
        exit 1
    fi
    
    print_success "All required files found"
    echo ""
    
    # Check Docker
    print_status "Checking Docker..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    print_success "Docker and Docker Compose are available"
    echo ""
    
    # Check if containers are already running
    print_status "Checking for existing containers..."
    if docker-compose -f docker-compose.integration.yml ps | grep -q "Up"; then
        print_warning "Some containers are already running"
        read -p "Do you want to stop and restart them? (y/N): " restart_choice
        if [[ $restart_choice =~ ^[Yy]$ ]]; then
            print_status "Stopping existing containers..."
            docker-compose -f docker-compose.integration.yml down
        else
            print_status "Keeping existing containers running"
            show_status
            exit 0
        fi
    fi
    
    # Build and start services
    print_header "🏗️  Building and Starting Services"
    print_header "=================================="
    echo ""
    
    print_status "Building Docker images (this may take a few minutes)..."
    docker-compose -f docker-compose.integration.yml build
    
    print_status "Starting all services..."
    docker-compose -f docker-compose.integration.yml up -d
    
    # Wait for services to be healthy
    print_status "Waiting for services to be ready..."
    echo ""
    
    # Wait for database
    print_status "⏳ Waiting for PostgreSQL..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if docker-compose -f docker-compose.integration.yml exec -T postgres pg_isready -U admorph &>/dev/null; then
            print_success "✅ PostgreSQL is ready"
            break
        fi
        sleep 2
        timeout=$((timeout-2))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "❌ PostgreSQL failed to start within 60 seconds"
        show_logs
        exit 1
    fi
    
    # Wait for Redis
    print_status "⏳ Waiting for Redis..."
    timeout=30
    while [ $timeout -gt 0 ]; do
        if docker-compose -f docker-compose.integration.yml exec -T redis redis-cli ping &>/dev/null; then
            print_success "✅ Redis is ready"
            break
        fi
        sleep 2
        timeout=$((timeout-2))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "❌ Redis failed to start within 30 seconds"
        show_logs
        exit 1
    fi
    
    # Wait for backend
    print_status "⏳ Waiting for Backend API..."
    timeout=120
    while [ $timeout -gt 0 ]; do
        if curl -s http://localhost:8000/health &>/dev/null; then
            print_success "✅ Backend API is ready"
            break
        fi
        sleep 3
        timeout=$((timeout-3))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "❌ Backend API failed to start within 120 seconds"
        show_logs
        exit 1
    fi
    
    # Wait for frontend
    print_status "⏳ Waiting for Frontend..."
    timeout=60
    while [ $timeout -gt 0 ]; do
        if curl -s http://localhost:3000 &>/dev/null; then
            print_success "✅ Frontend is ready"
            break
        fi
        sleep 3
        timeout=$((timeout-3))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "❌ Frontend failed to start within 60 seconds"
        show_logs
        exit 1
    fi
    
    # Success!
    echo ""
    print_header "🎉 AdMorph.AI Full Stack is Ready!"
    print_header "=================================="
    echo ""
    
    show_status
    
    echo ""
    print_header "📚 Quick Start Guide"
    print_header "==================="
    echo ""
    echo "1. 🎤 Voice Onboarding: Use the voice interface to create business profiles"
    echo "2. 🎨 Ad Generation: Generate AI-powered ad variants for different demographics"
    echo "3. 🛍️  E-commerce: Personalize product listings with GPT-4.1"
    echo "4. 📊 Analytics: Monitor performance and A/B test results"
    echo "5. 🤖 Agents: Chat with AI agents for business insights"
    echo ""
    
    print_status "To stop all services: docker-compose -f docker-compose.integration.yml down"
    print_status "To view logs: docker-compose -f docker-compose.integration.yml logs -f"
    echo ""
}

# Function to show current status
show_status() {
    print_header "🌐 Service Status"
    print_header "================"
    echo ""
    echo "🎨 Frontend:     http://localhost:3000"
    echo "🤖 Backend API:  http://localhost:8000"
    echo "📚 API Docs:     http://localhost:8000/docs"
    echo "💾 PostgreSQL:   localhost:5432"
    echo "🔄 Redis:        localhost:6379"
    echo ""
    
    # Show container status
    print_status "Container Status:"
    docker-compose -f docker-compose.integration.yml ps
}

# Function to show logs if something fails
show_logs() {
    print_error "Something went wrong. Here are the recent logs:"
    echo ""
    docker-compose -f docker-compose.integration.yml logs --tail=20
    echo ""
    print_status "For full logs: docker-compose -f docker-compose.integration.yml logs -f"
}

# Handle script arguments
case "${1:-}" in
    "status")
        show_status
        ;;
    "logs")
        docker-compose -f docker-compose.integration.yml logs -f
        ;;
    "stop")
        print_status "Stopping all services..."
        docker-compose -f docker-compose.integration.yml down
        print_success "All services stopped"
        ;;
    "restart")
        print_status "Restarting all services..."
        docker-compose -f docker-compose.integration.yml down
        docker-compose -f docker-compose.integration.yml up -d
        print_success "All services restarted"
        ;;
    *)
        main
        ;;
esac
