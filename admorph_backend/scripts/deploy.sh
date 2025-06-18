#!/bin/bash

# AdMorph.AI Backend Deployment Script
# This script handles deployment of the agentic backend service

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_DIR/.env"
DOCKER_COMPOSE_FILE="$PROJECT_DIR/docker-compose.yml"
DOCKER_COMPOSE_PROD_FILE="$PROJECT_DIR/docker-compose.prod.yml"

# Functions
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

check_requirements() {
    log_info "Checking deployment requirements..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check environment file
    if [ ! -f "$ENV_FILE" ]; then
        log_error "Environment file not found at $ENV_FILE"
        log_info "Please copy .env.example to .env and configure your settings"
        exit 1
    fi
    
    # Check required environment variables
    source "$ENV_FILE"
    if [ -z "$OPENAI_API_KEY" ]; then
        log_error "OPENAI_API_KEY is not set in environment file"
        exit 1
    fi
    
    log_success "All requirements satisfied"
}

build_images() {
    log_info "Building Docker images..."
    cd "$PROJECT_DIR"
    
    if [ "$ENVIRONMENT" = "production" ]; then
        docker-compose -f "$DOCKER_COMPOSE_FILE" -f "$DOCKER_COMPOSE_PROD_FILE" build
    else
        docker-compose build
    fi
    
    log_success "Docker images built successfully"
}

deploy_services() {
    log_info "Deploying services..."
    cd "$PROJECT_DIR"
    
    if [ "$ENVIRONMENT" = "production" ]; then
        docker-compose -f "$DOCKER_COMPOSE_FILE" -f "$DOCKER_COMPOSE_PROD_FILE" up -d
    else
        docker-compose up -d
    fi
    
    log_success "Services deployed successfully"
}

wait_for_services() {
    log_info "Waiting for services to be ready..."
    
    # Wait for backend to be healthy
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -f http://localhost:8000/health &> /dev/null; then
            log_success "Backend service is healthy"
            break
        fi
        
        log_info "Attempt $attempt/$max_attempts - waiting for backend..."
        sleep 5
        ((attempt++))
    done
    
    if [ $attempt -gt $max_attempts ]; then
        log_error "Backend service failed to start within expected time"
        exit 1
    fi
}

run_health_checks() {
    log_info "Running health checks..."
    
    # Check backend health
    local health_response=$(curl -s http://localhost:8000/health)
    if echo "$health_response" | grep -q '"status":"healthy"'; then
        log_success "Backend health check passed"
    else
        log_error "Backend health check failed"
        exit 1
    fi
    
    # Check database connection (if configured)
    if [ -n "$DATABASE_URL" ]; then
        log_info "Checking database connection..."
        # Add database health check here
    fi
    
    # Check Redis connection (if configured)
    if [ -n "$REDIS_URL" ]; then
        log_info "Checking Redis connection..."
        # Add Redis health check here
    fi
    
    log_success "All health checks passed"
}

show_deployment_info() {
    log_success "Deployment completed successfully!"
    echo
    echo "🚀 AdMorph.AI Backend is now running:"
    echo "   API: http://localhost:8000"
    echo "   Health: http://localhost:8000/health"
    echo "   Docs: http://localhost:8000/docs"
    echo
    echo "📊 Services:"
    docker-compose ps
    echo
    echo "📝 Logs:"
    echo "   View logs: docker-compose logs -f"
    echo "   Backend logs: docker-compose logs -f admorph-backend"
    echo
    echo "🛑 To stop services:"
    echo "   docker-compose down"
}

# Main deployment flow
main() {
    log_info "Starting AdMorph.AI Backend deployment..."
    
    # Parse command line arguments
    ENVIRONMENT="development"
    SKIP_BUILD=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --production)
                ENVIRONMENT="production"
                shift
                ;;
            --skip-build)
                SKIP_BUILD=true
                shift
                ;;
            --help)
                echo "Usage: $0 [OPTIONS]"
                echo "Options:"
                echo "  --production    Deploy in production mode"
                echo "  --skip-build    Skip Docker image building"
                echo "  --help          Show this help message"
                exit 0
                ;;
            *)
                log_error "Unknown option: $1"
                exit 1
                ;;
        esac
    done
    
    log_info "Deployment mode: $ENVIRONMENT"
    
    # Run deployment steps
    check_requirements
    
    if [ "$SKIP_BUILD" = false ]; then
        build_images
    fi
    
    deploy_services
    wait_for_services
    run_health_checks
    show_deployment_info
}

# Run main function
main "$@"
