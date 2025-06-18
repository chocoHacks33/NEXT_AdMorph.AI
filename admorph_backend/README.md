# AdMorph.AI Agentic Backend

A production-ready agentic advertising framework that provides AI-powered ad generation, demographic targeting, performance optimization, and automated campaign management.

## 🏗️ Architecture

The AdMorph.AI backend is built with a modular, scalable architecture:

```
admorph_backend/
├── api/                    # FastAPI routes and WebSocket handlers
├── core/                   # AI agents and agentic logic
├── models/                 # Data models and schemas
├── services/               # Business logic and external integrations
├── config/                 # Configuration management
├── utils/                  # Utility functions and helpers
├── requirements.txt        # Python dependencies
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-service deployment
└── .env.example          # Environment template
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key
- (Optional) Meta Marketing API credentials
- (Optional) Docker and Docker Compose

### Local Development

1. **Clone and setup**
   ```bash
   cd admorph_backend
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**
   ```bash
   python -m admorph_backend.api.main
   ```

4. **Access the API**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Health: http://localhost:8000/health

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Services available**
   - Backend API: http://localhost:8000
   - Redis: localhost:6379
   - PostgreSQL: localhost:5432

## 📡 API Endpoints

### Business Management
- `POST /api/business/profile` - Create business profile
- `GET /api/business/{business_id}` - Get business profile
- `PUT /api/business/{business_id}` - Update business profile

### Demographics Analysis
- `POST /api/demographics/analyze` - Analyze business and create segments
- `GET /api/demographics/{business_id}` - Get demographic segments

### Ad Management
- `GET /api/ads/` - List all ads
- `POST /api/ads/` - Create new ad
- `GET /api/ads/{ad_id}` - Get specific ad
- `PUT /api/ads/{ad_id}` - Update ad
- `DELETE /api/ads/{ad_id}` - Delete ad
- `POST /api/ads/generate` - Generate ad variants
- `POST /api/ads/{ad_id}/approve` - Approve ad
- `POST /api/ads/{ad_id}/reject` - Reject ad
- `POST /api/ads/{ad_id}/regenerate` - Regenerate ad

### Campaign Management
- `POST /api/campaigns/launch` - Launch campaign
- `GET /api/campaigns/{campaign_id}` - Get campaign details
- `POST /api/campaigns/{campaign_id}/pause` - Pause campaign
- `GET /api/campaigns/{campaign_id}/performance` - Get performance metrics

### Agent Interactions
- `POST /api/agents/chat` - Send chat message
- `POST /api/agents/voice/narrate` - Generate voice narration
- `POST /api/agents/business/onboard` - Start business onboarding
- `POST /api/agents/analyze/business` - Analyze business

### WebSocket Endpoints
- `ws://localhost:8000/ws/generation` - Real-time ad generation updates
- `ws://localhost:8000/ws/performance` - Live campaign metrics
- `ws://localhost:8000/ws/chat/{session_id}` - Chat interactions

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | Yes | - |
| `META_ACCESS_TOKEN` | Meta Marketing API token | No | - |
| `META_APP_ID` | Meta app ID | No | - |
| `META_APP_SECRET` | Meta app secret | No | - |
| `META_AD_ACCOUNT_ID` | Meta ad account ID | No | - |
| `ADMORPH_ENVIRONMENT` | Environment (development/production) | No | development |
| `ADMORPH_HOST` | Server host | No | 0.0.0.0 |
| `ADMORPH_PORT` | Server port | No | 8000 |
| `DATABASE_URL` | PostgreSQL connection string | No | - |
| `REDIS_URL` | Redis connection string | No | - |

### OpenAI Configuration

The system requires OpenAI GPT-4 access for:
- Business analysis and demographic segmentation
- Ad copy generation and optimization
- Trend analysis and mutation recommendations
- Voice-powered onboarding conversations

### Meta API Configuration (Optional)

For campaign publishing to Facebook/Instagram:
- Create a Meta Developer App
- Get Marketing API access
- Configure ad account permissions
- Add credentials to environment variables

## 🧬 Agentic System

### Core Agents

1. **DemographicAnalysisAgent**
   - Analyzes business profiles
   - Maps to real Meta demographic data
   - Creates targeted audience segments

2. **AdGenerationAgent**
   - Generates compelling ad variants
   - Follows Ogilvy's advertising principles
   - Optimizes for demographic segments

3. **EvolutionOrchestrator**
   - Monitors ad performance
   - Triggers mutations based on metrics
   - Manages A/B testing cycles

4. **VoiceAgent**
   - Handles conversational onboarding
   - Extracts business requirements
   - Guides campaign setup

### Data Flow

```
Business Input → Demographic Analysis → Ad Generation → Review → Publishing → Evolution
```

## 🔌 Integration with Next.js Frontend

### API Compatibility

The backend API is designed to match the expected interface from the Next.js frontend:

```typescript
// Frontend service calls
const ads = await adService.getAds();
const job = await processingService.startProcessing(adId);
const metrics = await analyticsService.getPerformanceMetrics();
const response = await agentService.sendChatMessage(message);
```

### WebSocket Integration

```typescript
// Real-time updates
const wsClient = createWebSocketClient('/generation');
wsClient.connect((data) => {
  if (data.type === 'generation_complete') {
    updateAdsList(data.ads);
  }
});
```

## 📊 Monitoring and Logging

### Health Checks
- `/health` - Service health status
- `/metrics` - Prometheus metrics (if enabled)

### Logging
- Structured JSON logging
- Configurable log levels
- Request/response tracking
- Agent execution monitoring

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
   ```bash
   export ADMORPH_ENVIRONMENT=production
   export ADMORPH_LOG_LEVEL=WARNING
   # Set all required API keys
   ```

2. **Database Migration** (if using PostgreSQL)
   ```bash
   alembic upgrade head
   ```

3. **Run with Gunicorn**
   ```bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker admorph_backend.api.main:create_app
   ```

### Docker Production

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=admorph_backend

# Run specific test file
pytest tests/test_agents.py
```

## 📈 Performance

### Optimization Features
- Async/await throughout
- Connection pooling for external APIs
- Background job processing with Celery
- Redis caching for demographic data
- Rate limiting and request throttling

### Scaling Considerations
- Horizontal scaling with multiple workers
- Database connection pooling
- Redis for session management
- Load balancing for high availability

## 🔒 Security

### API Security
- CORS configuration
- Rate limiting
- Input validation with Pydantic
- Environment-based configuration

### Production Security
- JWT authentication (configurable)
- HTTPS enforcement
- API key rotation
- Audit logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is proprietary software developed for AdMorph.AI.

## 📞 Support

For technical support or questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation and API specs

## 📚 Additional Resources

- [API Documentation](http://localhost:8000/docs) (when running)
- [Framework Analysis](../FRAMEWORK_ANALYSIS.md)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Meta Marketing API Documentation](https://developers.facebook.com/docs/marketing-apis)
