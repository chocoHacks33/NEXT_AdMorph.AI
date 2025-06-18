# Product Requirements Document: AdMorph.AI Frontend-Backend Integration

## Introduction/Overview

This PRD outlines the integration of the AdMorph.AI React frontend with the Python FastAPI backend to enable a seamless voice-to-ad-generation workflow. The integration will connect the existing frontend components with the agentic AI backend services, enabling users to complete the entire journey from voice consultation to ad generation through a unified interface, with production deployment to AWS.

**Problem**: Currently, the AdMorph.AI frontend and backend operate as separate systems with no communication layer, preventing users from experiencing the complete AI-powered advertising workflow.

**Goal**: Create a fully integrated system where users can seamlessly move from voice consultation to ad generation with real-time progress updates and production-ready AWS deployment.

## Goals

1. **Enable Core User Flow**: Voice consultation → demographics analysis → ad generation → review
2. **Real-time Communication**: Implement WebSocket connections for live progress updates
3. **Production Readiness**: Ensure the integrated system is deployable to AWS with proper scalability
4. **Seamless User Experience**: Hide backend complexity while providing clear progress indicators
5. **Error Resilience**: Implement robust error handling for AI agent failures and timeouts
6. **Session Management**: Establish secure and efficient user session handling

## User Stories

### Primary User Stories
1. **As a business owner**, I want to speak my business requirements into the voice interface so that the AI can understand my advertising needs without manual form filling.

2. **As a marketing director**, I want to see real-time progress as the AI generates my ads so that I know the system is working and can estimate completion time.

3. **As a user**, I want the system to automatically analyze demographics and generate targeted ads based on my voice consultation so that I don't need to manually configure audience targeting.

4. **As a business user**, I want to review and approve generated ads through an intuitive interface so that I maintain control over my advertising content.

### Secondary User Stories
5. **As a system administrator**, I want the application deployed on AWS with proper monitoring so that it can handle production traffic reliably.

6. **As a user**, I want my session data preserved during the ad generation process so that I don't lose progress if there are temporary connection issues.

## Functional Requirements

### Core Integration Requirements
1. **The system MUST connect the voice-interface.tsx component to the AdMorphVoiceAgent backend service**
   - Voice input should be processed by the backend AI agent
   - Business profile data should be extracted and stored
   - Frontend should receive structured business profile response

2. **The system MUST integrate the processing-panel.tsx with backend generation services**
   - Display real-time progress of demographics analysis
   - Show ad generation status for each demographic segment
   - Update UI dynamically as backend processes complete

3. **The system MUST implement WebSocket communication for real-time updates**
   - Establish WebSocket connection on voice consultation start
   - Broadcast progress updates for each AI agent step
   - Handle connection drops and reconnection gracefully

4. **The system MUST integrate ad-gallery.tsx with backend ad variants**
   - Display generated ads from backend AdVariantMorph objects
   - Send swipe decisions (approve/reject/regenerate) to backend
   - Support ad regeneration with feedback loop

### API Integration Requirements
5. **The system MUST implement a production FastAPI backend service**
   - Use the production FastAPI server (admorph_backend/api/main.py) over simple_server.py for scalability
   - Implement proper error handling and timeout management
   - Include comprehensive API documentation and health checks

6. **The system MUST handle session management securely**
   - Generate unique session IDs for each user consultation
   - Persist business profiles and generated ads per session
   - Implement session timeout and cleanup mechanisms

7. **The system MUST implement proper error handling**
   - Display user-friendly error messages for AI agent failures
   - Provide retry mechanisms for failed operations
   - Log detailed errors for debugging while showing simplified messages to users

### Data Flow Requirements
8. **The system MUST maintain data consistency throughout the workflow**
   - Business profile data from voice consultation should flow to demographics analysis
   - Demographic segments should be used for targeted ad generation
   - Generated ads should retain connection to their source demographics

9. **The system MUST implement proper loading states**
   - Show appropriate loading indicators during AI processing
   - Provide estimated time remaining when possible
   - Allow users to cancel long-running operations

### AWS Deployment Requirements
10. **The system MUST be deployable to AWS with production configurations**
    - Containerized deployment using Docker and AWS ECS/Fargate
    - Environment-specific configuration management
    - Proper secrets management for API keys (OpenAI, Meta)
    - Load balancing and auto-scaling capabilities

## Non-Goals (Out of Scope)

1. **Autonomous Evolution System**: The advanced ad mutation and evolution features will remain backend-only for this integration phase
2. **Meta Campaign Publishing**: Direct Meta API campaign creation will not be included in the initial integration
3. **Advanced Analytics Dashboard**: Complex performance analytics will be implemented in a future phase
4. **Multi-user Collaboration**: Team features and multi-user campaign management are out of scope
5. **Mobile App Integration**: Focus is on web application only
6. **Real-time Voice Streaming**: Voice processing will be request-response based, not streaming

## Design Considerations

### Frontend Architecture
- **Service Layer**: Implement `lib/api-client.ts` for centralized backend communication
- **State Management**: Use React Context or Zustand for session and workflow state
- **Error Boundaries**: Implement React error boundaries for graceful error handling
- **Loading States**: Consistent loading UI patterns across all integration points

### WebSocket Integration
- **Connection Management**: Automatic reconnection with exponential backoff
- **Message Types**: Structured message types for different update categories (voice_progress, generation_progress, error_alerts)
- **Fallback Strategy**: HTTP polling fallback if WebSocket connection fails

### API Design
- **RESTful Endpoints**: Follow REST conventions for CRUD operations
- **WebSocket Events**: Real-time updates for long-running AI processes
- **Response Format**: Consistent JSON response structure with proper error codes

## Technical Considerations

### Backend API Selection
- **Recommendation**: Use production FastAPI backend (`admorph_backend/api/main.py`) for scalability and features
- **Performance**: FastAPI provides async capabilities needed for AI agent orchestration
- **Documentation**: Built-in OpenAPI documentation for frontend development

### Session Management Strategy
- **JWT Tokens**: Use JSON Web Tokens for stateless session management
- **Redis Cache**: Session data caching for improved performance
- **Database Storage**: Persistent storage for business profiles and generated ads

### Error Handling Strategy
- **Timeout Management**: 30-second timeout for voice processing, 60-second timeout for ad generation
- **Retry Logic**: Exponential backoff for transient failures
- **Circuit Breaker**: Prevent cascade failures in AI agent chain

### AWS Deployment Architecture
- **Frontend**: Deploy React app to AWS S3 + CloudFront CDN
- **Backend**: Deploy FastAPI to AWS ECS Fargate with Application Load Balancer
- **Database**: AWS RDS PostgreSQL for persistent data storage
- **Cache**: AWS ElastiCache Redis for session management
- **Secrets**: AWS Secrets Manager for API key management
- **Monitoring**: AWS CloudWatch for logging and monitoring

## Success Metrics

### Functional Success Metrics
1. **Complete Workflow Success Rate**: >95% of voice consultations successfully generate ads
2. **Real-time Update Latency**: WebSocket updates delivered within 500ms
3. **Session Persistence**: 99% session data retention during workflow
4. **Error Recovery**: <5% of users experience unrecoverable errors

### Performance Success Metrics
1. **Voice Processing Time**: <30 seconds for business profile extraction
2. **Ad Generation Time**: <60 seconds for complete demographic analysis and ad generation
3. **Frontend Load Time**: <3 seconds initial page load
4. **API Response Time**: <2 seconds for non-AI endpoints

### Production Readiness Metrics
1. **AWS Deployment Success**: Successful deployment with zero-downtime updates
2. **Scalability**: Handle 100+ concurrent users without degradation
3. **Uptime**: 99.9% availability in production environment
4. **Security**: Pass security audit for API key management and data handling

## Implementation Phases

### Phase 1: Core API Integration (Week 1-2)
- Implement API client service layer
- Connect voice-interface.tsx to AdMorphVoiceAgent
- Basic error handling and loading states

### Phase 2: Real-time Communication (Week 2-3)
- Implement WebSocket connections
- Integrate processing-panel.tsx with real-time updates
- Connect ad generation workflow

### Phase 3: Ad Review Integration (Week 3-4)
- Integrate ad-gallery.tsx with backend ad variants
- Implement swipe decision handling
- Add ad regeneration capabilities

### Phase 4: AWS Deployment (Week 4-5)
- Set up AWS infrastructure
- Configure production deployment pipeline
- Implement monitoring and logging

## Open Questions

1. **AI Agent Timeout Handling**: What should be the maximum timeout for voice consultation and ad generation processes?

2. **Session Data Retention**: How long should session data be retained for incomplete workflows?

3. **AWS Region Selection**: Which AWS region should be used for deployment to optimize for your target users?

4. **Scaling Thresholds**: What are the expected concurrent user limits for initial production deployment?

5. **Monitoring Requirements**: What specific metrics and alerts are needed for production monitoring?

6. **Backup Strategy**: What backup and disaster recovery requirements exist for the production system?

7. **API Rate Limiting**: Should there be rate limiting on API endpoints to prevent abuse?

8. **Data Privacy**: Are there specific data privacy requirements for storing business profiles and generated ads? 