# 🔗 AdMorph.AI Integration Plan

## 📊 Current State Analysis

### ✅ What's Already Compatible:
- **API Endpoints**: Our FastAPI backend provides all endpoints the Next.js frontend expects
- **Data Models**: TypeScript interfaces match our Python models
- **WebSocket**: Real-time communication already implemented
- **Environment Config**: Frontend already configured for `localhost:8000`

### 🎯 Integration Strategy: Microservices Architecture

**Recommended Approach**: Keep repositories separate but connected

```
┌─────────────────────────────────────────────────────────────┐
│                    INTEGRATION ARCHITECTURE                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📱 NEXT.JS FRONTEND                                        │
│  ├─ Repository: chocoHacks33/NEXT_AdMorph.AI               │
│  ├─ Port: 3000                                             │
│  ├─ API Client: Configured for localhost:8000              │
│  └─ WebSocket: Configured for ws://localhost:8000          │
│                                                             │
│  🤖 AGENTIC BACKEND                                         │
│  ├─ Repository: Your agentic framework repo                │
│  ├─ Port: 8000                                             │
│  ├─ FastAPI Service: All endpoints implemented             │
│  └─ WebSocket: Real-time updates ready                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Step-by-Step Integration

### Step 1: Update Next.js Repository (Minimal Changes)

Add these files to the Next.js repo:

#### 1. `docker-compose.integration.yml`
```yaml
version: '3.8'
services:
  frontend:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000/api
      - NEXT_PUBLIC_WS_URL=ws://backend:8000/ws
    depends_on:
      - backend

  backend:
    image: admorph-backend:latest
    ports:
      - "8000:8000"
    environment:
      - ADMORPH_ENVIRONMENT=production
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./backend-config:/app/config
```

#### 2. `.env.example` (Update)
```env
# AdMorph.AI Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws

# Backend Configuration (for development)
OPENAI_API_KEY=your_openai_key_here
META_ACCESS_TOKEN=your_meta_token_here
```

#### 3. `scripts/start-full-stack.sh`
```bash
#!/bin/bash
echo "🚀 Starting AdMorph.AI Full Stack..."

# Start backend
echo "Starting agentic backend..."
cd ../admorph-backend
docker-compose up -d

# Wait for backend to be ready
echo "Waiting for backend to be ready..."
while ! curl -f http://localhost:8000/health; do
  sleep 2
done

# Start frontend
echo "Starting Next.js frontend..."
cd ../NEXT_AdMorph.AI
npm run dev

echo "✅ AdMorph.AI is running!"
echo "Frontend: http://localhost:3000"
echo "Backend API: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
```

### Step 2: Backend Repository Setup

Your agentic backend repository should have:

#### Repository Structure:
```
admorph-agentic-backend/
├── admorph_backend/          # FastAPI service
├── docker-compose.yml        # Backend deployment
├── README.md                 # Educational documentation
├── INTEGRATION_GUIDE.md      # Integration instructions
└── scripts/
    ├── setup.sh             # Environment setup
    └── deploy.sh            # Deployment script
```

## 🔧 API Endpoint Mapping

### ✅ Already Implemented and Compatible:

| Frontend Expectation | Backend Implementation | Status |
|----------------------|------------------------|---------|
| `GET /ads` | `GET /api/ads/` | ✅ Ready |
| `POST /ads` | `POST /api/ads/` | ✅ Ready |
| `PUT /ads/{id}` | `PUT /api/ads/{id}` | ✅ Ready |
| `DELETE /ads/{id}` | `DELETE /api/ads/{id}` | ✅ Ready |
| `POST /processing/start` | `POST /api/ads/generate` | ✅ Ready |
| `GET /processing/jobs/{id}` | `GET /api/processing/jobs/{id}` | ✅ Ready |
| `POST /agents/chat` | `POST /api/agents/chat` | ✅ Ready |
| `POST /agents/voice/narrate` | `POST /api/agents/voice/narrate` | ✅ Ready |
| `WS /processing` | `WS /ws/generation` | ✅ Ready |
| `WS /agents/chat/{id}` | `WS /ws/chat/{id}` | ✅ Ready |

## 🎯 Deployment Options

### Option 1: Development Setup (Recommended for now)

1. **Clone both repositories**:
   ```bash
   git clone https://github.com/chocoHacks33/NEXT_AdMorph.AI.git
   git clone <your-agentic-backend-repo> admorph-backend
   ```

2. **Start backend**:
   ```bash
   cd admorph-backend
   ./scripts/setup.sh
   ./scripts/deploy.sh
   ```

3. **Start frontend**:
   ```bash
   cd NEXT_AdMorph.AI
   npm install
   npm run dev
   ```

### Option 2: Docker Compose (Production)

Create a `docker-compose.fullstack.yml` that orchestrates both services:

```yaml
version: '3.8'
services:
  frontend:
    build: ./NEXT_AdMorph.AI
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000/api
      - NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
    depends_on:
      - backend

  backend:
    build: ./admorph-backend
    ports:
      - "8000:8000"
    environment:
      - ADMORPH_ENVIRONMENT=production
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./uploads:/app/uploads
```

## 📋 Integration Checklist

### For Next.js Repository:
- [ ] Add environment configuration for backend connection
- [ ] Add Docker compose for full-stack deployment
- [ ] Add startup scripts for development
- [ ] Update README with integration instructions

### For Backend Repository:
- [ ] Ensure all API endpoints match frontend expectations
- [ ] Add CORS configuration for frontend domain
- [ ] Add health check endpoints
- [ ] Add deployment documentation

### For Development Team:
- [ ] Set up development environment with both repos
- [ ] Test API connectivity between frontend and backend
- [ ] Verify WebSocket connections work
- [ ] Test full ad generation workflow
- [ ] Verify real-time updates function

## 🎉 Expected Result

After integration:

1. **Frontend** (localhost:3000): Full UI with all components working
2. **Backend** (localhost:8000): Agentic framework providing AI services
3. **Real-time Features**: WebSocket connections for live updates
4. **AI Capabilities**: Voice onboarding, demographic analysis, ad generation
5. **Performance Monitoring**: Live campaign metrics and optimization

## 🚀 Next Steps

1. **Create backend repository** with the agentic framework
2. **Add integration files** to Next.js repository
3. **Test connectivity** between frontend and backend
4. **Deploy to staging** environment for team testing
5. **Production deployment** when ready

This approach keeps the codebases clean while enabling full integration of the agentic capabilities with the existing UI/UX work.
