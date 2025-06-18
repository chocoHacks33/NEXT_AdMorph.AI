# 🚀 AdMorph.AI - Full-Stack Agentic Advertising Platform

## 📚 Overview: Complete AI-Powered Advertising System

AdMorph.AI is a **production-ready full-stack agentic advertising platform** that combines advanced AI backend services with a modern Next.js frontend. This project demonstrates end-to-end AI system architecture, from autonomous agent coordination to responsive user interfaces.

## 🏗️ Architecture Overview

### 🤖 Backend: Agentic AI System

The backend demonstrates a **multi-agent architecture** where specialized AI agents handle different aspects of advertising:

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENTIC WORKFLOW                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🗣️ VOICE AGENT          🎯 DEMOGRAPHIC AGENT              │
│  ├─ Natural language     ├─ Business analysis              │
│  ├─ Business onboarding  ├─ Audience segmentation          │
│  └─ Requirement extraction└─ Meta data integration         │
│                                                             │
│  ✍️ GENERATION AGENT     📊 PERFORMANCE AGENT              │
│  ├─ GPT-4 integration    ├─ Real-time monitoring           │
│  ├─ Ogilvy principles    ├─ A/B testing automation         │
│  └─ Multi-variant creation└─ ROI optimization              │
│                                                             │
│  🧬 EVOLUTION AGENT      🔄 TREND AGENT                    │
│  ├─ Performance analysis ├─ Market trend monitoring        │
│  ├─ Automatic mutations  ├─ Viral content detection        │
│  └─ Continuous improvement└─ Strategy adaptation           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 🎨 Frontend: Modern React/Next.js Interface

- **Next.js 14** with App Router
- **Real-time WebSocket** communication
- **Responsive design** with Tailwind CSS
- **Complete API integration** with backend services

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.13+** (for backend)
- **Node.js 18+** (for frontend)
- **pnpm** (recommended) or npm
- **Docker** (optional, for containerized deployment)

### Backend Setup

1. **Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install backend dependencies:**
```bash
pip install -r requirements.txt
pip install -r admorph_backend/requirements.txt
```

3. **Run backend demos:**
```bash
# Complete agentic workflow demo
python complete_admorph_demo.py

# Streamlit interface
streamlit run swipe_interface.py --server.port 8502
```

4. **Start FastAPI backend** (when import issues are fixed):
```bash
cd admorph_backend
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup (Coming Soon)

1. **Install frontend dependencies:**
```bash
pnpm install
```

2. **Copy environment variables:**
```bash
cp .env.example .env.local
```

3. **Start development server:**
```bash
pnpm dev
```

The application will be available at `http://localhost:3000`.

---
## 📱 Frontend Documentation

### Table of Contents
- [Quick Start](#quick-start)
- [Environment Setup](#environment-setup)
- [Development](#development)
- [Backend Integration](#backend-integration)
- [AWS Deployment](#aws-deployment)
- [Docker Deployment](#docker-deployment)
- [Project Structure](#project-structure)
- [API Integration](#api-integration)
- [Troubleshooting](#troubleshooting)

## Quick Start

### Prerequisites
- Node.js 18+ 
- pnpm (recommended) or npm
- Docker (for containerized deployment)
- AWS CLI (for AWS deployment)

### Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd NEXT_AdMorph.AI

# Install dependencies
pnpm install

# Copy environment variables
cp .env.example .env.local

# Start development server
pnpm dev
```

The application will be available at `http://localhost:3000`.

## Environment Setup

### Environment Variables

Create a `.env.local` file in the root directory:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8001

# AWS Configuration
NEXT_PUBLIC_AWS_REGION=us-east-1
NEXT_PUBLIC_S3_BUCKET_NAME=your-bucket-name

# Environment
NEXT_PUBLIC_NODE_ENV=development

# Optional Feature Flags
NEXT_PUBLIC_VOICE_ENABLED=true
NEXT_PUBLIC_CHAT_ENABLED=true
NEXT_PUBLIC_ANALYTICS_ENABLED=true
```

### Environment Files
- `.env.local` - Local development (not committed to git)
- `.env.production` - Production environment variables
- `.env.example` - Template with all required variables

## Development

### Available Scripts

```bash
# Development
pnpm dev              # Start development server
pnpm build            # Build for production
pnpm start            # Start production server
pnpm lint             # Run ESLint
pnpm type-check       # Run TypeScript type checking

# Production builds
pnpm build:production # Build with production environment
pnpm start:production # Start with production environment

# Docker commands
pnpm docker:build     # Build Docker image
pnpm docker:run       # Run Docker container
pnpm docker:compose   # Run with docker-compose

# Analysis
pnpm analyze          # Analyze bundle size
pnpm export           # Export static files
```

### Development Workflow

1. **Start development server:**
   ```bash
   pnpm dev
   ```

2. **Make changes to components in:**
   - `components/` - Reusable UI components
   - `app/` - Pages and layouts
   - `lib/` - Utilities and services

3. **Test your changes:**
   ```bash
   pnpm lint
   pnpm type-check
   ```

4. **Build for production:**
   ```bash
   pnpm build
   ```

## Backend Integration

### API Service Layer

The application includes a complete API service layer in `lib/api.ts` and `lib/services.ts`.

### Setting Up Backend Connection

1. **Update environment variables:**
   ```env
   NEXT_PUBLIC_API_URL=https://your-backend-api.com
   NEXT_PUBLIC_WS_URL=wss://your-backend-websocket.com
   ```

2. **Backend API Endpoints Expected:**
   ```
   GET    /ads              # Get all ads
   POST   /ads              # Create new ad
   GET    /ads/:id          # Get specific ad
   PUT    /ads/:id          # Update ad
   DELETE /ads/:id          # Delete ad
   POST   /ads/:id/assets   # Upload ad assets

   GET    /processing/jobs           # Get processing jobs
   POST   /processing/start         # Start processing
   POST   /processing/jobs/:id/cancel # Cancel processing

   GET    /analytics/performance    # Get performance metrics
   GET    /analytics/performance/:id # Get ad-specific metrics

   POST   /agents/chat             # Send chat message
   POST   /agents/voice/narrate    # Get voice narration

   WebSocket /processing           # Processing updates
   WebSocket /agents/chat/:sessionId # Chat updates
   ```

3. **Backend Response Format:**
   ```typescript
   interface ApiResponse<T> {
     data: T;
     message?: string;
     error?: string;
   }
   ```

### Using the API Services

```typescript
import { adService, processingService, analyticsService, agentService } from '@/lib/services';

// Get all ads
const ads = await adService.getAds();

// Create new ad
const newAd = await adService.createAd({
  title: 'My Ad',
  description: 'Ad description'
});

// Start processing
const job = await processingService.startProcessing(adId);

// Get performance metrics
const metrics = await analyticsService.getPerformanceMetrics();

// Send chat message
const response = await agentService.sendChatMessage('Hello');
```

### WebSocket Integration

```typescript
import { processingService, agentService } from '@/lib/services';

// Processing updates
const wsClient = processingService.createProcessingWebSocket((job) => {
  console.log('Processing update:', job);
});

// Chat updates
const chatWs = agentService.createChatWebSocket(sessionId, (message) => {
  console.log('Chat message:', message);
});

// Clean up
wsClient.disconnect();
chatWs.disconnect();
```

## AWS Deployment

### Prerequisites

1. **Install AWS CLI:**
   ```bash
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install
   ```

2. **Configure AWS credentials:**
   ```bash
   aws configure
   ```

### Deployment Methods

#### Option 1: AWS Amplify (Recommended for Static/SSG)

1. **Install Amplify CLI:**
   ```bash
   npm install -g @aws-amplify/cli
   amplify configure
   ```

2. **Initialize Amplify:**
   ```bash
   amplify init
   amplify add hosting
   amplify publish
   ```

#### Option 2: AWS EC2 with CodeDeploy

1. **Create EC2 instance** (Amazon Linux 2)

2. **Install CodeDeploy agent** on EC2:
   ```bash
   sudo yum update -y
   sudo yum install -y ruby wget
   cd /home/ec2-user
   wget https://aws-codedeploy-us-east-1.s3.us-east-1.amazonaws.com/latest/install
   chmod +x ./install
   sudo ./install auto
   ```

3. **Create CodeDeploy application:**
   ```bash
   aws deploy create-application \
     --application-name AdMorph-Frontend \
     --compute-platform Server
   ```

4. **Create deployment group:**
   ```bash
   aws deploy create-deployment-group \
     --application-name AdMorph-Frontend \
     --deployment-group-name Production \
     --service-role-arn arn:aws:iam::ACCOUNT:role/CodeDeployRole \
     --ec2-tag-filters Key=Name,Value=AdMorph-Frontend,Type=KEY_AND_VALUE
   ```

5. **Deploy using provided scripts:**
   ```bash
   # The deployment will use:
   # - buildspec.yml for CodeBuild
   # - appspec.yml for CodeDeploy
   # - scripts/ directory for deployment hooks
   ```

#### Option 3: AWS ECS with Fargate

1. **Create ECR repository:**
   ```bash
   aws ecr create-repository --repository-name admorph-frontend
   ```

2. **Build and push Docker image:**
   ```bash
   # Get login token
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

   # Build image
   docker build -t admorph-frontend .

   # Tag image
   docker tag admorph-frontend:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/admorph-frontend:latest

   # Push image
   docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/admorph-frontend:latest
   ```

3. **Create ECS cluster:**
   ```bash
   aws ecs create-cluster --cluster-name admorph-cluster
   ```

4. **Create task definition** (create `task-definition.json`):
   ```json
   {
     "family": "admorph-frontend",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "256",
     "memory": "512",
     "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "admorph-frontend",
         "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/admorph-frontend:latest",
         "portMappings": [
           {
             "containerPort": 3000,
             "protocol": "tcp"
           }
         ],
         "environment": [
           {
             "name": "NEXT_PUBLIC_API_URL",
             "value": "https://your-api-domain.com"
           }
         ],
         "logConfiguration": {
           "logDriver": "awslogs",
           "options": {
             "awslogs-group": "/ecs/admorph-frontend",
             "awslogs-region": "us-east-1",
             "awslogs-stream-prefix": "ecs"
           }
         }
       }
     ]
   }
   ```

5. **Register task definition:**
   ```bash
   aws ecs register-task-definition --cli-input-json file://task-definition.json
   ```

6. **Create service:**
   ```bash
   aws ecs create-service \
     --cluster admorph-cluster \
     --service-name admorph-frontend-service \
     --task-definition admorph-frontend \
     --desired-count 1 \
     --launch-type FARGATE \
     --network-configuration "awsvpcConfiguration={subnets=[subnet-12345],securityGroups=[sg-12345],assignPublicIp=ENABLED}"
   ```

### Environment Variables for AWS

Update `.env.production`:
```env
NEXT_PUBLIC_API_URL=https://your-api-domain.com
NEXT_PUBLIC_WS_URL=wss://your-ws-domain.com
NEXT_PUBLIC_AWS_REGION=us-east-1
NEXT_PUBLIC_S3_BUCKET_NAME=your-production-bucket
NEXT_PUBLIC_NODE_ENV=production
```

## Docker Deployment

### Local Docker Development

1. **Build Docker image:**
   ```bash
   docker build -t admorph-frontend .
   ```

2. **Run container:**
   ```bash
   docker run -p 3000:3000 admorph-frontend
   ```

3. **With environment variables:**
   ```bash
   docker run -p 3000:3000 \
     -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
     -e NEXT_PUBLIC_WS_URL=ws://localhost:8001 \
     admorph-frontend
   ```

### Docker Compose

1. **Start services:**
   ```bash
   docker-compose up --build
   ```

2. **Run in background:**
   ```bash
   docker-compose up -d --build
   ```

3. **Stop services:**
   ```bash
   docker-compose down
   ```

### Docker Production Deployment

1. **Build production image:**
   ```bash
   docker build -t admorph-frontend:production .
   ```

2. **Run with production environment:**
   ```bash
   docker run -p 3000:3000 \
     --env-file .env.production \
     admorph-frontend:production
   ```

## Project Structure

```
NEXT_AdMorph.AI/
├── app/                    # Next.js app directory
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/             # React components
│   ├── ui/                # Base UI components
│   ├── ad-gallery.tsx     # Ad gallery component
│   ├── chat-interface.tsx # Chat interface
│   ├── processing-panel.tsx # Processing panel
│   ├── sidebar.tsx        # Navigation sidebar
│   ├── upload-interface.tsx # File upload
│   └── voice-*.tsx        # Voice components
├── lib/                   # Utility libraries
│   ├── api.ts            # API client
│   ├── services.ts       # Service layer
│   ├── config.ts         # Configuration
│   └── utils.ts          # Utilities
├── public/               # Static assets
├── scripts/              # Deployment scripts
│   ├── install_dependencies.sh
│   ├── start_server.sh
│   └── stop_server.sh
├── styles/               # Stylesheets
├── .env.example          # Environment template
├── .env.local           # Local environment (not committed)
├── .env.production      # Production environment
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
├── buildspec.yml        # AWS CodeBuild specification
├── appspec.yml          # AWS CodeDeploy specification
├── next.config.mjs      # Next.js configuration
├── package.json         # Dependencies and scripts
└── README.md           # This file
```

## API Integration

### Service Layer Architecture

The application uses a layered architecture:

1. **API Client (`lib/api.ts`)**: Low-level HTTP and WebSocket client
2. **Services (`lib/services.ts`)**: Business logic and data transformation
3. **Components**: UI components that consume services

### Adding New API Endpoints

1. **Add to API client:**
   ```typescript
   // lib/api.ts
   async patch<T>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
     return this.request<T>(endpoint, {
       method: 'PATCH',
       body: data ? JSON.stringify(data) : undefined,
     });
   }
   ```

2. **Add to service layer:**
   ```typescript
   // lib/services.ts
   export const newService = {
     async updatePartial(id: string, data: Partial<Entity>): Promise<Entity> {
       const response = await apiClient.patch<Entity>(`/entities/${id}`, data);
       return response.data;
     }
   };
   ```

3. **Use in components:**
   ```typescript
   import { newService } from '@/lib/services';
   
   const handleUpdate = async () => {
     const updated = await newService.updatePartial(id, { status: 'active' });
     // Handle response
   };
   ```

### Error Handling

The API client includes automatic error handling:

```typescript
try {
  const data = await adService.getAds();
} catch (error) {
  console.error('Failed to fetch ads:', error);
  // Handle error in UI
}
```

### Loading States

Implement loading states in components:

```typescript
const [loading, setLoading] = useState(false);
const [error, setError] = useState<string | null>(null);

const fetchData = async () => {
  setLoading(true);
  setError(null);
  try {
    const data = await adService.getAds();
    // Handle success
  } catch (err) {
    setError(err instanceof Error ? err.message : 'An error occurred');
  } finally {
    setLoading(false);
  }
};
```

## Troubleshooting

### Common Issues

1. **Environment variables not loading:**
   ```bash
   # Ensure variables are prefixed with NEXT_PUBLIC_
   # Restart development server after changes
   pnpm dev
   ```

2. **Build failures:**
   ```bash
   # Clear Next.js cache
   rm -rf .next
   
   # Reinstall dependencies
   rm -rf node_modules pnpm-lock.yaml
   pnpm install
   
   # Check TypeScript errors
   pnpm type-check
   ```

3. **Docker build issues:**
   ```bash
   # Clean Docker cache
   docker system prune -a
   
   # Rebuild without cache
   docker build --no-cache -t admorph-frontend .
   ```

4. **API connection issues:**
   ```bash
   # Check if backend is running
   curl http://localhost:8000/health
   
   # Verify environment variables
   echo $NEXT_PUBLIC_API_URL
   ```

5. **WebSocket connection failures:**
   ```bash
   # Check WebSocket URL format
   # Ensure ws:// for development, wss:// for production
   # Verify backend WebSocket server is running
   ```

### Development Tips

1. **Hot reload not working:**
   ```bash
   # Restart development server
   pnpm dev
   
   # Check for TypeScript errors
   pnpm type-check
   ```

2. **Styling issues:**
   ```bash
   # Ensure Tailwind classes are correct
   # Check for conflicting CSS
   # Verify component imports
   ```

3. **Component not rendering:**
   ```bash
   # Check console for errors
   # Verify component exports
   # Check for missing dependencies
   ```

### Debugging

1. **Enable debug logging:**
   ```typescript
   // Add to lib/config.ts
   export const DEBUG = process.env.NODE_ENV === 'development';
   
   // Use in components
   if (DEBUG) console.log('Debug info:', data);
   ```

2. **Network debugging:**
   ```bash
   # Check network requests in browser dev tools
   # Verify API responses
   # Check for CORS issues
   ```

3. **Performance debugging:**
   ```bash
   # Analyze bundle size
   pnpm analyze
   
   # Check for memory leaks
   # Use React DevTools Profiler
   ```

### Getting Help

1. **Check logs:**
   - Browser console for client-side errors
   - Server logs for API issues
   - Docker logs for container issues

2. **Verify configuration:**
   - Environment variables are correct
   - API endpoints are accessible
   - Network connectivity is available

3. **Test components individually:**
   - Isolate problematic components
   - Test API calls separately
   - Verify data flow

For additional support, check the component documentation in the respective files or consult the Next.js documentation.

---

## 🎓 Educational Value Summary

This project demonstrates **production-grade full-stack AI system development** with:

- ✅ **Scalable Backend**: Python FastAPI with agentic AI coordination
- ✅ **Modern Frontend**: Next.js 14 with real-time communication
- ✅ **Real-time Processing**: WebSocket and async patterns
- ✅ **AI Integration**: Multiple AI services working together
- ✅ **Production Deployment**: Docker, monitoring, security
- ✅ **Business Logic**: Real advertising domain knowledge

**Perfect for learning**: Full-stack AI system architecture, modern web development, production deployment, and business application development.
