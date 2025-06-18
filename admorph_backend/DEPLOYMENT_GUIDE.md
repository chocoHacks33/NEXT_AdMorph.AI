# AdMorph.AI Backend Deployment Guide

This guide provides comprehensive instructions for deploying the AdMorph.AI agentic backend in various environments.

## 🚀 Quick Start

### Automated Setup

```bash
# Clone and setup
git clone <repository-url>
cd admorph_backend

# Run setup script
./scripts/setup.sh

# Deploy with Docker
./scripts/deploy.sh
```

### Manual Setup

```bash
# 1. Environment setup
cp .env.example .env
# Edit .env with your API keys

# 2. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Run the server
python -m admorph_backend.api.main
```

## 🔧 Environment Configuration

### Required Environment Variables

```env
# OpenAI API (Required)
OPENAI_API_KEY=sk-your-openai-key-here

# Server Configuration
ADMORPH_ENVIRONMENT=development
ADMORPH_HOST=0.0.0.0
ADMORPH_PORT=8000
ADMORPH_LOG_LEVEL=INFO

# CORS Settings
ADMORPH_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Optional Configuration

```env
# Meta Marketing API (for campaign publishing)
META_ACCESS_TOKEN=your-meta-token
META_APP_ID=your-app-id
META_APP_SECRET=your-app-secret
META_AD_ACCOUNT_ID=your-account-id

# Database (PostgreSQL)
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/admorph

# Redis (for caching and job queue)
REDIS_URL=redis://localhost:6379/0

# File Upload Settings
ADMORPH_UPLOAD_DIR=uploads
ADMORPH_MAX_FILE_SIZE=10485760

# Performance Settings
ADMORPH_MAX_CONCURRENT_JOBS=10
ADMORPH_JOB_TIMEOUT=300
```

## 🐳 Docker Deployment

### Development Deployment

```bash
# Build and run all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f admorph-backend
```

### Production Deployment

```bash
# Create production environment file
cp .env.example .env.prod
# Configure production settings

# Deploy with production configuration
ADMORPH_ENVIRONMENT=production ./scripts/deploy.sh --production

# Or manually with docker-compose
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Docker Services

The deployment includes:

- **admorph-backend**: Main FastAPI application
- **postgres**: PostgreSQL database
- **redis**: Redis for caching and job queue
- **celery-worker**: Background job processing
- **celery-beat**: Scheduled task management

## ☁️ Cloud Deployment

### AWS Deployment

#### Using AWS ECS

1. **Build and push Docker image**
   ```bash
   # Build image
   docker build -t admorph-backend .
   
   # Tag for ECR
   docker tag admorph-backend:latest <account-id>.dkr.ecr.<region>.amazonaws.com/admorph-backend:latest
   
   # Push to ECR
   docker push <account-id>.dkr.ecr.<region>.amazonaws.com/admorph-backend:latest
   ```

2. **Create ECS Task Definition**
   ```json
   {
     "family": "admorph-backend",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "512",
     "memory": "1024",
     "containerDefinitions": [
       {
         "name": "admorph-backend",
         "image": "<account-id>.dkr.ecr.<region>.amazonaws.com/admorph-backend:latest",
         "portMappings": [
           {
             "containerPort": 8000,
             "protocol": "tcp"
           }
         ],
         "environment": [
           {
             "name": "ADMORPH_ENVIRONMENT",
             "value": "production"
           }
         ],
         "secrets": [
           {
             "name": "OPENAI_API_KEY",
             "valueFrom": "arn:aws:secretsmanager:region:account:secret:openai-api-key"
           }
         ]
       }
     ]
   }
   ```

3. **Create ECS Service**
   ```bash
   aws ecs create-service \
     --cluster admorph-cluster \
     --service-name admorph-backend \
     --task-definition admorph-backend \
     --desired-count 2 \
     --launch-type FARGATE
   ```

#### Using AWS Lambda (Serverless)

```bash
# Install serverless framework
npm install -g serverless

# Deploy with serverless
serverless deploy --stage production
```

### Google Cloud Platform

#### Using Cloud Run

```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT-ID/admorph-backend
gcloud run deploy --image gcr.io/PROJECT-ID/admorph-backend --platform managed
```

### Azure Container Instances

```bash
# Create resource group
az group create --name admorph-rg --location eastus

# Deploy container
az container create \
  --resource-group admorph-rg \
  --name admorph-backend \
  --image admorph-backend:latest \
  --ports 8000 \
  --environment-variables ADMORPH_ENVIRONMENT=production
```

## 🔒 Production Security

### Environment Security

```env
# Production security settings
ADMORPH_ENVIRONMENT=production
ADMORPH_LOG_LEVEL=WARNING
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Disable debug features
ADMORPH_ENABLE_DOCS=false
ADMORPH_ENABLE_METRICS=true
```

### SSL/TLS Configuration

```nginx
# Nginx configuration for HTTPS
server {
    listen 443 ssl;
    server_name api.admorph.ai;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # WebSocket support
    location /ws/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### API Key Management

```bash
# Use environment variables or secret management
export OPENAI_API_KEY=$(aws secretsmanager get-secret-value --secret-id openai-key --query SecretString --output text)
export META_ACCESS_TOKEN=$(aws secretsmanager get-secret-value --secret-id meta-token --query SecretString --output text)
```

## 📊 Monitoring and Logging

### Health Checks

```bash
# Basic health check
curl http://localhost:8000/health

# Detailed health check with metrics
curl http://localhost:8000/metrics
```

### Logging Configuration

```python
# Production logging setup
import logging
import structlog

logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.INFO,
)

structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
```

### Prometheus Metrics

```python
# Metrics endpoint configuration
from prometheus_client import Counter, Histogram, generate_latest

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type="text/plain")
```

## 🔄 CI/CD Pipeline

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy AdMorph Backend

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest
      
      - name: Run tests
        run: pytest
      
      - name: Build Docker image
        run: docker build -t admorph-backend .
      
      - name: Deploy to production
        run: ./scripts/deploy.sh --production
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          META_ACCESS_TOKEN: ${{ secrets.META_ACCESS_TOKEN }}
```

## 🧪 Testing Deployment

### Automated Testing

```bash
# Run deployment tests
./scripts/test-deployment.sh

# Manual API testing
curl -X POST http://localhost:8000/api/ads/generate \
  -H "Content-Type: application/json" \
  -d '{"businessId": "test", "segments": []}'
```

### Load Testing

```bash
# Install artillery
npm install -g artillery

# Run load tests
artillery run load-test.yml
```

## 🚨 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port 8000
   lsof -i :8000
   # Kill the process
   kill -9 <PID>
   ```

2. **Docker Build Fails**
   ```bash
   # Clean Docker cache
   docker system prune -a
   # Rebuild without cache
   docker-compose build --no-cache
   ```

3. **OpenAI API Errors**
   ```bash
   # Test API key
   curl https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
   ```

4. **Database Connection Issues**
   ```bash
   # Check PostgreSQL connection
   docker-compose exec postgres psql -U admorph -d admorph -c "SELECT 1;"
   ```

### Log Analysis

```bash
# View application logs
docker-compose logs -f admorph-backend

# View specific service logs
docker-compose logs postgres
docker-compose logs redis

# Follow logs in real-time
tail -f logs/admorph-backend.log
```

## 📈 Scaling

### Horizontal Scaling

```yaml
# docker-compose.scale.yml
version: '3.8'
services:
  admorph-backend:
    deploy:
      replicas: 3
    ports:
      - "8000-8002:8000"
```

### Load Balancing

```nginx
# Nginx load balancer
upstream admorph_backend {
    server localhost:8000;
    server localhost:8001;
    server localhost:8002;
}

server {
    listen 80;
    location / {
        proxy_pass http://admorph_backend;
    }
}
```

This deployment guide ensures reliable, scalable deployment of the AdMorph.AI agentic backend across various environments and platforms.
