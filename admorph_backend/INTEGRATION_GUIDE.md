# AdMorph.AI Integration Guide

This guide provides step-by-step instructions for integrating the AdMorph.AI agentic backend with the Next.js frontend application.

## 🎯 Integration Overview

The integration involves connecting the Python-based agentic backend with the TypeScript Next.js frontend through REST APIs and WebSocket connections.

### Architecture Flow
```
Next.js Frontend ↔ FastAPI Backend ↔ AI Agents ↔ External APIs (OpenAI, Meta)
```

## 🔧 Backend Setup

### 1. Environment Configuration

Create `.env` file in the backend directory:

```bash
# Copy the example environment file
cp .env.example .env

# Edit with your actual API keys
nano .env
```

Required configuration:
```env
# OpenAI (Required)
OPENAI_API_KEY=sk-your-openai-key-here

# Meta API (Optional - for campaign publishing)
META_ACCESS_TOKEN=your-meta-token
META_APP_ID=your-app-id
META_APP_SECRET=your-app-secret
META_AD_ACCOUNT_ID=your-account-id

# Server settings
ADMORPH_ENVIRONMENT=development
ADMORPH_PORT=8000
ADMORPH_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### 2. Start the Backend Service

**Option A: Direct Python**
```bash
cd admorph_backend
pip install -r requirements.txt
python -m admorph_backend.api.main
```

**Option B: Docker**
```bash
cd admorph_backend
docker-compose up --build
```

### 3. Verify Backend is Running

```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/docs
```

## 🌐 Frontend Integration

### 1. Update API Configuration

In your Next.js app, update the API configuration to point to the backend:

```typescript
// lib/config.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
const WS_BASE_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws';
```

### 2. Environment Variables

Add to your Next.js `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_WS_URL=ws://localhost:8000/ws
```

### 3. Service Integration

The existing services in your Next.js app should work with minimal changes:

```typescript
// lib/services.ts - Already compatible!
export const adService = {
  async getAds(): Promise<Ad[]> {
    const response = await apiClient.get<Ad[]>('/ads');
    return response.data;
  },
  // ... other methods work as-is
};
```

## 🔄 API Mapping

### Ad Service Mapping

| Frontend Method | Backend Endpoint | Description |
|----------------|------------------|-------------|
| `adService.getAds()` | `GET /api/ads/` | List all ads |
| `adService.createAd(data)` | `POST /api/ads/` | Create new ad |
| `adService.updateAd(id, data)` | `PUT /api/ads/{id}` | Update ad |
| `adService.deleteAd(id)` | `DELETE /api/ads/{id}` | Delete ad |
| `adService.uploadAdAssets(id, files)` | `POST /api/ads/{id}/assets` | Upload assets |

### Processing Service Mapping

| Frontend Method | Backend Endpoint | Description |
|----------------|------------------|-------------|
| `processingService.startProcessing(adId)` | `POST /api/ads/generate` | Start ad generation |
| `processingService.getJob(jobId)` | `GET /api/processing/jobs/{jobId}` | Get job status |
| `processingService.cancelProcessing(jobId)` | `POST /api/processing/jobs/{jobId}/cancel` | Cancel job |

### Agent Service Mapping

| Frontend Method | Backend Endpoint | Description |
|----------------|------------------|-------------|
| `agentService.sendChatMessage(msg)` | `POST /api/agents/chat` | Chat with AI |
| `agentService.getVoiceNarration(text)` | `POST /api/agents/voice/narrate` | Generate voice |

## 🔌 WebSocket Integration

### Real-time Ad Generation

```typescript
// In your React component
import { createWebSocketClient } from '@/lib/api';

const GenerationComponent = () => {
  useEffect(() => {
    const wsClient = createWebSocketClient('/generation');
    
    wsClient.connect(
      (data) => {
        if (data.type === 'generation_progress') {
          setProgress(data.progress);
        } else if (data.type === 'generation_complete') {
          setAds(data.ads);
        }
      },
      (error) => console.error('WebSocket error:', error)
    );

    return () => wsClient.disconnect();
  }, []);
};
```

### Live Performance Metrics

```typescript
// Real-time campaign performance
const PerformanceComponent = () => {
  useEffect(() => {
    const wsClient = createWebSocketClient('/performance');
    
    wsClient.connect((data) => {
      if (data.type === 'metrics_update') {
        updateMetrics(data.metrics);
      }
    });

    return () => wsClient.disconnect();
  }, []);
};
```

## 🎨 UI Component Integration

### Ad Gallery Component

The existing ad gallery component works seamlessly:

```typescript
// components/ad-gallery.tsx - No changes needed!
const AdGallery = () => {
  const [ads, setAds] = useState<Ad[]>([]);

  useEffect(() => {
    adService.getAds().then(setAds);
  }, []);

  // Component renders ads from backend
};
```

### Processing Panel Integration

```typescript
// components/processing-panel.tsx
const ProcessingPanel = () => {
  const startGeneration = async (businessData: any) => {
    // This now calls the agentic backend
    const job = await processingService.startProcessing(businessData.id, {
      generateAds: true,
      segments: businessData.segments
    });
    
    // Monitor job progress via WebSocket
    monitorJob(job.id);
  };
};
```

## 🤖 Agentic Features Integration

### Business Onboarding

```typescript
// New agentic onboarding flow
const OnboardingComponent = () => {
  const [session, setSession] = useState(null);

  const startOnboarding = async () => {
    const response = await agentService.startBusinessOnboarding({
      initialData: { industry: 'technology' }
    });
    setSession(response);
  };

  const respondToAgent = async (response: string) => {
    const result = await agentService.respondToOnboarding(
      session.sessionId, 
      { response }
    );
    setSession(result);
  };
};
```

### Demographic Analysis

```typescript
// Automatic demographic analysis
const DemographicsComponent = () => {
  const analyzeBusiness = async (businessProfile: BusinessProfile) => {
    const job = await agentService.analyzeBusiness({
      businessData: businessProfile
    });
    
    // Poll for results or use WebSocket
    const segments = await pollForResults(job.job_id);
    return segments;
  };
};
```

## 🔄 Data Flow Examples

### Complete Ad Generation Flow

```typescript
const AdGenerationFlow = () => {
  // 1. Business onboarding (voice-powered)
  const businessProfile = await onboardBusiness();
  
  // 2. Demographic analysis (AI-powered)
  const segments = await analyzeDemographics(businessProfile);
  
  // 3. Ad generation (multi-variant)
  const generationJob = await generateAds(businessProfile, segments);
  
  // 4. Real-time monitoring
  monitorGeneration(generationJob.job_id);
  
  // 5. Review interface (Tinder-style)
  const approvedAds = await reviewAds(generatedAds);
  
  // 6. Campaign launch
  const campaign = await launchCampaign(approvedAds);
  
  // 7. Performance monitoring
  monitorPerformance(campaign.id);
};
```

## 🚨 Error Handling

### API Error Handling

```typescript
// Enhanced error handling for agentic features
const handleAgentError = (error: any) => {
  if (error.status === 429) {
    // Rate limiting - show user-friendly message
    showNotification('AI is processing many requests. Please wait...');
  } else if (error.status === 503) {
    // Service unavailable - fallback to manual mode
    enableManualMode();
  } else {
    // Generic error
    showError('An error occurred. Please try again.');
  }
};
```

### WebSocket Reconnection

```typescript
// Automatic reconnection for real-time features
const createResilientWebSocket = (endpoint: string) => {
  const wsClient = createWebSocketClient(endpoint);
  
  wsClient.connect(
    onMessage,
    (error) => {
      console.error('WebSocket error:', error);
      // Attempt reconnection after delay
      setTimeout(() => wsClient.connect(onMessage), 5000);
    }
  );
  
  return wsClient;
};
```

## 🧪 Testing Integration

### API Testing

```bash
# Test backend endpoints
curl -X POST http://localhost:8000/api/ads/generate \
  -H "Content-Type: application/json" \
  -d '{"businessId": "test", "segments": []}'
```

### Frontend Testing

```typescript
// Test agentic features
describe('Agentic Integration', () => {
  it('should generate ads using AI agents', async () => {
    const result = await adService.generateAds(mockBusinessProfile);
    expect(result.job_id).toBeDefined();
  });

  it('should handle real-time updates', async () => {
    const wsClient = createWebSocketClient('/generation');
    // Test WebSocket functionality
  });
});
```

## 🚀 Deployment Integration

### Production Setup

1. **Backend Deployment**
   ```bash
   # Deploy backend service
   docker-compose -f docker-compose.prod.yml up -d
   ```

2. **Frontend Environment**
   ```env
   NEXT_PUBLIC_API_URL=https://api.admorph.ai/api
   NEXT_PUBLIC_WS_URL=wss://api.admorph.ai/ws
   ```

3. **Load Balancing**
   - Configure load balancer for backend API
   - Enable WebSocket support in proxy
   - Set up health checks

## ✅ Integration Checklist

- [ ] Backend service running on port 8000
- [ ] OpenAI API key configured
- [ ] Frontend API URLs updated
- [ ] WebSocket connections working
- [ ] Ad generation flow tested
- [ ] Real-time updates functioning
- [ ] Error handling implemented
- [ ] Performance monitoring active
- [ ] Production deployment ready

## 🆘 Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check `ADMORPH_ALLOWED_ORIGINS` in backend
   - Verify frontend URL matches allowed origins

2. **WebSocket Connection Failed**
   - Ensure WebSocket URL is correct
   - Check firewall/proxy settings

3. **AI Generation Timeout**
   - Increase `ADMORPH_JOB_TIMEOUT` setting
   - Check OpenAI API key and quota

4. **Meta API Errors**
   - Verify Meta API credentials
   - Check ad account permissions

This integration guide ensures seamless connection between your Next.js frontend and the AdMorph.AI agentic backend, enabling all AI-powered advertising features.
