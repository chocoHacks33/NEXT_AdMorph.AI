# 🤖 AdMorph.AI Agentic Backend Integration

## 🎯 Overview

This document explains how to integrate the AdMorph.AI agentic backend with this Next.js frontend application. The agentic backend provides AI-powered advertising capabilities including voice onboarding, demographic analysis, intelligent ad generation, and autonomous campaign optimization.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FULL STACK ARCHITECTURE                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📱 NEXT.JS FRONTEND (Port 3000)                           │
│  ├─ React Components                                       │
│  ├─ API Client (configured for backend)                    │
│  ├─ WebSocket Client (real-time updates)                   │
│  └─ UI/UX for ad management and review                     │
│                                                             │
│  🤖 AGENTIC BACKEND (Port 8000)                            │
│  ├─ FastAPI Service                                        │
│  ├─ AI Agents (Voice, Generation, Evolution)               │
│  ├─ Real Meta Data Integration                              │
│  ├─ WebSocket for real-time updates                        │
│  └─ Docker deployment ready                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

1. **Backend Repository**: Clone the agentic backend repository
2. **Docker**: Ensure Docker and Docker Compose are installed
3. **API Keys**: OpenAI API key (required), Meta API credentials (optional)

### Setup Steps

1. **Clone the backend repository** (parallel to this frontend repo):
   ```bash
   cd ..
   git clone <agentic-backend-repo-url> admorph-agentic-backend
   cd NEXT_AdMorph.AI
   ```

2. **Configure environment**:
   ```bash
   cp .env.integration.example .env.local
   # Edit .env.local with your API keys
   ```

3. **Start the full stack**:
   ```bash
   ./scripts/start-fullstack.sh
   ```

4. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

Add these to your `.env.local`:

```env
# Backend Connection
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws

# AI Services (Required)
OPENAI_API_KEY=your_openai_key_here

# Meta API (Optional - for campaign publishing)
META_ACCESS_TOKEN=your_meta_token
META_APP_ID=your_app_id
META_APP_SECRET=your_app_secret
META_AD_ACCOUNT_ID=your_account_id
```

### API Client Configuration

The existing API client in `lib/api.ts` is already configured to work with the agentic backend. No changes needed!

## 🤖 Agentic Features Available

### 1. **Voice-Powered Onboarding**
- Natural language business profile creation
- AI-guided questionnaire
- Automatic industry analysis

### 2. **Intelligent Demographic Analysis**
- Real Meta API data (1200+ categories)
- AI-powered audience segmentation
- Behavioral targeting recommendations

### 3. **AI Ad Generation**
- GPT-4 powered ad creation
- Ogilvy advertising principles
- Multiple variants per demographic segment

### 4. **Autonomous Evolution**
- Performance-based ad optimization
- Automatic A/B testing
- Trend-aligned mutations

### 5. **Real-Time Monitoring**
- Live campaign performance metrics
- WebSocket updates for generation progress
- Instant optimization notifications

## 📡 API Integration

### Existing Services Work Automatically

Your existing services in `lib/services.ts` work seamlessly:

```typescript
// Ad Management - Already works!
const ads = await adService.getAds();
const newAd = await adService.createAd(adData);

// Processing - AI generation ready!
const job = await processingService.startProcessing(adId);

// Analytics - Real-time metrics!
const metrics = await analyticsService.getPerformanceMetrics();

// Agent Interaction - Voice and chat!
const response = await agentService.sendChatMessage(message);
```

### New Agentic Capabilities

Additional endpoints now available:

```typescript
// Business Onboarding
POST /api/agents/business/onboard
POST /api/agents/business/onboard/{sessionId}/respond

// Demographic Analysis
POST /api/demographics/analyze
GET /api/demographics/{businessId}

// Campaign Management
POST /api/campaigns/launch
GET /api/campaigns/{campaignId}/performance

// Voice Narration
POST /api/agents/voice/narrate
```

### WebSocket Real-Time Updates

```typescript
// Generation Progress
const wsClient = createWebSocketClient('/generation');
wsClient.connect((data) => {
  if (data.type === 'generation_progress') {
    updateProgress(data.progress);
  }
});

// Performance Metrics
const perfClient = createWebSocketClient('/performance');
perfClient.connect((data) => {
  if (data.type === 'metrics_update') {
    updateDashboard(data.metrics);
  }
});
```

## 🎨 UI Component Integration

### Enhanced Components

Your existing components gain new capabilities:

#### 1. **Voice Interface** (`components/voice-interface.tsx`)
- Now connects to real voice agent
- Natural language business onboarding
- AI-powered conversation flow

#### 2. **Processing Panel** (`components/processing-panel.tsx`)
- Real AI generation with progress updates
- Multiple demographic segments
- Intelligent variant creation

#### 3. **Ad Gallery** (`components/ad-gallery.tsx`)
- AI-generated variants with performance scores
- Ogilvy principle ratings
- Trend alignment indicators

#### 4. **Performance Dashboard** (`components/ad-performance-dashboard.tsx`)
- Real-time metrics from campaigns
- AI optimization suggestions
- Autonomous evolution tracking

## 🔄 Development Workflow

### 1. **Start Development Environment**
```bash
./scripts/start-fullstack.sh
```

### 2. **Test AI Features**
- Voice onboarding: Use voice interface component
- Ad generation: Create business profile and generate variants
- Real-time updates: Monitor WebSocket connections
- Performance tracking: View live campaign metrics

### 3. **Debug Issues**
```bash
# Check backend health
curl http://localhost:8000/health

# View backend logs
cd ../admorph-agentic-backend
docker-compose logs -f

# Test API endpoints
curl http://localhost:8000/api/ads/
```

## 🚀 Production Deployment

### Option 1: Separate Services
Deploy frontend and backend independently:

```bash
# Frontend (Vercel/Netlify)
NEXT_PUBLIC_API_URL=https://api.admorph.ai/api
NEXT_PUBLIC_WS_URL=wss://api.admorph.ai/ws

# Backend (AWS/GCP/Azure)
# Use provided Docker deployment
```

### Option 2: Full Stack Docker
Use the provided `docker-compose.integration.yml`:

```bash
docker-compose -f docker-compose.integration.yml up -d
```

## 🧪 Testing Integration

### 1. **API Connectivity Test**
```bash
# Test backend health
curl http://localhost:8000/health

# Test ad endpoints
curl http://localhost:8000/api/ads/
```

### 2. **WebSocket Test**
```javascript
// In browser console
const ws = new WebSocket('ws://localhost:8000/ws/generation');
ws.onmessage = (event) => console.log(JSON.parse(event.data));
```

### 3. **Full Workflow Test**
1. Start voice onboarding
2. Create business profile
3. Generate ad variants
4. Review in gallery
5. Launch campaign
6. Monitor performance

## 🆘 Troubleshooting

### Common Issues

1. **Backend Not Starting**
   ```bash
   cd ../admorph-agentic-backend
   docker-compose logs
   ```

2. **API Connection Failed**
   - Check `.env.local` configuration
   - Verify backend is running on port 8000
   - Check CORS settings

3. **WebSocket Connection Failed**
   - Verify WebSocket URL in environment
   - Check firewall/proxy settings
   - Ensure backend WebSocket service is running

4. **AI Generation Timeout**
   - Check OpenAI API key
   - Verify API quota and billing
   - Check backend logs for errors

### Support

- Backend Documentation: See agentic backend repository
- API Documentation: http://localhost:8000/docs
- Integration Issues: Check this document and backend logs

## 🎉 Success Criteria

Integration is successful when:

- ✅ Frontend loads at http://localhost:3000
- ✅ Backend health check returns "healthy"
- ✅ API calls return data (test with /api/ads/)
- ✅ WebSocket connections establish successfully
- ✅ Voice onboarding works end-to-end
- ✅ Ad generation creates real variants
- ✅ Real-time updates appear in UI

**You now have a fully integrated agentic advertising platform!** 🚀
