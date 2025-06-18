# Product Requirements Document: AdMorph.AI Frontend-Backend Integration

## Introduction/Overview

This PRD outlines the integration of the AdMorph.AI React frontend with the Python FastAPI backend to enable a seamless voice-to-ad-generation workflow with marketplace simulation. The integration will connect the existing frontend components with the agentic AI backend services, enabling users to complete the entire journey from voice consultation to ad generation, campaign launch, and marketplace simulation through a unified interface, with production deployment to AWS.

**Problem**: Currently, the AdMorph.AI frontend and backend operate as separate systems with no communication layer, preventing users from experiencing the complete AI-powered advertising workflow and seeing how their ads perform in realistic marketplace environments.

**Goal**: Create a fully integrated system where users can seamlessly move from voice consultation to ad generation, campaign launch, and marketplace simulation with real-time progress updates and production-ready AWS deployment.

## Goals

1. **Enable Core User Flow**: Voice consultation → demographics analysis → ad generation → review → campaign launch → marketplace simulation
2. **Real-time Communication**: Implement WebSocket connections for live progress updates
3. **Marketplace Simulation**: Integrate Shadow Shelf Emporium to demonstrate ad performance in realistic e-commerce environment
4. **Production Readiness**: Ensure the integrated system is deployable to AWS with proper scalability
5. **Seamless User Experience**: Hide backend complexity while providing clear progress indicators and realistic ad placement demonstration
6. **Error Resilience**: Implement robust error handling for AI agent failures and timeouts
7. **Session Management**: Establish secure and efficient user session handling

## User Stories

### Primary User Stories
1. **As a business owner**, I want to speak my business requirements into the voice interface so that the AI can understand my advertising needs without manual form filling.

2. **As a marketing director**, I want to see real-time progress as the AI generates my ads so that I know the system is working and can estimate completion time.

3. **As a user**, I want the system to automatically analyze demographics and generate targeted ads based on my voice consultation so that I don't need to manually configure audience targeting.

4. **As a business user**, I want to review and approve generated ads through an intuitive interface so that I maintain control over my advertising content.

5. **As a marketing professional**, I want to launch my approved ads into a simulated campaign so that I can see how the campaign activation process works.

6. **As a user**, I want to see my generated ads displayed in a realistic marketplace environment so that I can understand how my advertisements will appear to actual customers in e-commerce contexts.

7. **As a business owner**, I want to navigate through the marketplace simulation to see my ads integrated naturally with relevant products so that I can evaluate ad placement effectiveness.

### Secondary User Stories
8. **As a system administrator**, I want the application deployed on AWS with proper monitoring so that it can handle production traffic reliably.

9. **As a user**, I want my session data preserved during the ad generation and simulation process so that I don't lose progress if there are temporary connection issues.

10. **As a marketing analyst**, I want to see my ads displayed in different product categories within the marketplace simulation so that I can assess cross-category appeal and placement strategies.

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

### Marketplace Simulation Requirements
5. **The system MUST integrate the Shadow Shelf Emporium marketplace simulation**
   - Embed the existing Shadow Shelf Emporium React application as a simulation module
   - Launch marketplace simulation after successful campaign creation
   - Display generated ads contextually within the marketplace interface

6. **The system MUST implement ad placement integration within marketplace products**
   - Inject generated campaign ads as sponsored product listings
   - Display ads in relevant product categories based on business profile demographics
   - Implement realistic ad placement algorithms (sponsored sections, between organic products)

7. **The system MUST provide seamless transition from campaign launch to marketplace simulation**
   - Add "View in Marketplace" action after campaign approval
   - Preserve session context when entering marketplace simulation
   - Implement clear navigation between AdMorph interface and marketplace simulation

8. **The system MUST simulate realistic marketplace ad interactions**
   - Enable ad clicking/interaction within the marketplace simulation
   - Track simulated engagement metrics (views, clicks, interactions)
   - Display engagement data back to user in campaign performance summary

### Enhanced Campaign Workflow Requirements
9. **The system MUST implement campaign launch functionality**
   - Add campaign launch step after ad approval in ad-gallery.tsx
   - Generate unique campaign IDs for tracking and simulation
   - Store campaign metadata (target demographics, selected ads, launch timestamp)

10. **The system MUST provide campaign management interface**
    - Display active/launched campaigns in user dashboard
    - Allow users to access marketplace simulation for any launched campaign
    - Implement campaign status tracking (draft, launched, simulated)

### API Integration Requirements
11. **The system MUST implement a production FastAPI backend service**
    - Use the production FastAPI server (admorph_backend/api/main.py) over simple_server.py for scalability
    - Implement proper error handling and timeout management
    - Include comprehensive API documentation and health checks

12. **The system MUST handle session management securely**
    - Generate unique session IDs for each user consultation
    - Persist business profiles, generated ads, and campaign data per session
    - Implement session timeout and cleanup mechanisms

13. **The system MUST implement proper error handling**
    - Display user-friendly error messages for AI agent failures
    - Provide retry mechanisms for failed operations
    - Log detailed errors for debugging while showing simplified messages to users

### Data Flow Requirements
14. **The system MUST maintain data consistency throughout the extended workflow**
    - Business profile data from voice consultation should flow to demographics analysis
    - Demographic segments should be used for targeted ad generation
    - Generated ads should retain connection to their source demographics
    - Campaign data should connect ads to their marketplace placement context

15. **The system MUST implement proper loading states**
    - Show appropriate loading indicators during AI processing
    - Provide estimated time remaining when possible
    - Allow users to cancel long-running operations
    - Display marketplace simulation loading states

### AWS Deployment Requirements
16. **The system MUST be deployable to AWS with production configurations**
    - Containerized deployment using Docker and AWS ECS/Fargate
    - Environment-specific configuration management
    - Proper secrets management for API keys (OpenAI, Meta)
    - Load balancing and auto-scaling capabilities

## Non-Goals (Out of Scope)

1. **Autonomous Evolution System**: The advanced ad mutation and evolution features will remain backend-only for this integration phase
2. **Real Meta Campaign Publishing**: Direct Meta API campaign creation will not be included in the initial integration
3. **Advanced Analytics Dashboard**: Complex performance analytics will be implemented in a future phase
4. **Multi-user Collaboration**: Team features and multi-user campaign management are out of scope
5. **Mobile App Integration**: Focus is on web application only
6. **Real-time Voice Streaming**: Voice processing will be request-response based, not streaming
7. **Real E-commerce Integration**: The marketplace simulation will not connect to actual e-commerce platforms or real product data
8. **Actual Purchase Transactions**: The marketplace simulation will not process real financial transactions
9. **Multi-marketplace Simulation**: Initial implementation will focus on the single Shadow Shelf Emporium marketplace

## Design Considerations

### Frontend Architecture
- **Service Layer**: Implement `lib/api-client.ts` for centralized backend communication
- **State Management**: Use React Context or Zustand for session, workflow, and marketplace state
- **Error Boundaries**: Implement React error boundaries for graceful error handling
- **Loading States**: Consistent loading UI patterns across all integration points
- **Route Management**: Implement proper routing for marketplace simulation integration

### Marketplace Integration Architecture
- **Module Integration**: Embed Shadow Shelf Emporium as a React component within AdMorph interface
- **State Sharing**: Share campaign and ad data between AdMorph and marketplace contexts
- **Navigation Design**: Seamless transitions between ad creation and marketplace simulation
- **Data Injection**: Dynamic injection of generated ads into marketplace product listings

### WebSocket Integration
- **Connection Management**: Automatic reconnection with exponential backoff
- **Message Types**: Structured message types for different update categories (voice_progress, generation_progress, campaign_launch, simulation_ready, error_alerts)
- **Fallback Strategy**: HTTP polling fallback if WebSocket connection fails

### API Design
- **RESTful Endpoints**: Follow REST conventions for CRUD operations
- **WebSocket Events**: Real-time updates for long-running AI processes and simulation state
- **Response Format**: Consistent JSON response structure with proper error codes
- **Campaign Endpoints**: New endpoints for campaign management and marketplace simulation data

## Technical Considerations

### Backend API Selection
- **Recommendation**: Use production FastAPI backend (`admorph_backend/api/main.py`) for scalability and features
- **Performance**: FastAPI provides async capabilities needed for AI agent orchestration
- **Documentation**: Built-in OpenAPI documentation for frontend development

### Session Management Strategy
- **JWT Tokens**: Use JSON Web Tokens for stateless session management
- **Redis Cache**: Session data caching for improved performance
- **Database Storage**: Persistent storage for business profiles, generated ads, and campaign data

### Marketplace Integration Strategy
- **Component Composition**: Integrate Shadow Shelf Emporium as a React component within AdMorph
- **Shared Dependencies**: Resolve potential dependency conflicts between AdMorph and marketplace UI libraries
- **State Synchronization**: Implement state synchronization between AdMorph campaign data and marketplace simulation

### Error Handling Strategy
- **Timeout Management**: 30-second timeout for voice processing, 60-second timeout for ad generation, 10-second timeout for marketplace simulation setup
- **Retry Logic**: Exponential backoff for transient failures
- **Circuit Breaker**: Prevent cascade failures in AI agent chain and marketplace simulation

### AWS Deployment Architecture
- **Frontend**: Deploy React app to AWS S3 + CloudFront CDN
- **Backend**: Deploy FastAPI to AWS ECS Fargate with Application Load Balancer
- **Database**: AWS RDS PostgreSQL for persistent data storage including campaign and simulation data
- **Cache**: AWS ElastiCache Redis for session management
- **Secrets**: AWS Secrets Manager for API key management
- **Monitoring**: AWS CloudWatch for logging and monitoring

## Success Metrics

### Functional Success Metrics
1. **Complete Workflow Success Rate**: >95% of voice consultations successfully generate ads and launch campaigns
2. **Real-time Update Latency**: WebSocket updates delivered within 500ms
3. **Session Persistence**: 99% session data retention during workflow
4. **Error Recovery**: <5% of users experience unrecoverable errors
5. **Marketplace Simulation Success Rate**: >98% of launched campaigns successfully display in marketplace simulation

### Performance Success Metrics
1. **Voice Processing Time**: <30 seconds for business profile extraction
2. **Ad Generation Time**: <60 seconds for complete demographic analysis and ad generation
3. **Campaign Launch Time**: <10 seconds for campaign creation and marketplace preparation
4. **Marketplace Simulation Load Time**: <5 seconds for marketplace interface with injected ads
5. **Frontend Load Time**: <3 seconds initial page load
6. **API Response Time**: <2 seconds for non-AI endpoints

### User Experience Success Metrics
1. **Workflow Completion Rate**: >90% of users complete the full voice-to-marketplace-simulation workflow
2. **Marketplace Engagement**: Users spend >2 minutes exploring marketplace simulation
3. **Ad Placement Satisfaction**: >85% user satisfaction with ad placement realism (via feedback survey)

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
- Implement campaign creation backend endpoints

### Phase 2: Real-time Communication (Week 2-3)
- Implement WebSocket connections
- Integrate processing-panel.tsx with real-time updates
- Connect ad generation workflow
- Add campaign launch functionality to ad-gallery.tsx

### Phase 3: Marketplace Integration Setup (Week 3-4)
- Integrate Shadow Shelf Emporium as React component module
- Resolve dependency conflicts and shared UI library issues
- Implement basic marketplace simulation navigation
- Create ad injection mechanisms for marketplace product listings

### Phase 4: Ad Review and Campaign Launch Integration (Week 4-5)
- Integrate ad-gallery.tsx with backend ad variants
- Implement swipe decision handling
- Add ad regeneration capabilities
- Implement campaign launch and marketplace simulation transition

### Phase 5: Advanced Marketplace Features (Week 5-6)
- Implement realistic ad placement algorithms
- Add simulated engagement tracking
- Create campaign performance summary interface
- Implement marketplace navigation and interaction features

### Phase 6: AWS Deployment (Week 6-7)
- Set up AWS infrastructure
- Configure production deployment pipeline
- Implement monitoring and logging
- Deploy integrated system with marketplace simulation

## Open Questions

1. **AI Agent Timeout Handling**: What should be the maximum timeout for voice consultation and ad generation processes?

2. **Session Data Retention**: How long should session data be retained for incomplete workflows?

3. **AWS Region Selection**: Which AWS region should be used for deployment to optimize for your target users?

4. **Scaling Thresholds**: What are the expected concurrent user limits for initial production deployment?

5. **Monitoring Requirements**: What specific metrics and alerts are needed for production monitoring?

6. **Backup Strategy**: What backup and disaster recovery requirements exist for the production system?

7. **API Rate Limiting**: Should there be rate limiting on API endpoints to prevent abuse?

8. **Data Privacy**: Are there specific data privacy requirements for storing business profiles, generated ads, and campaign data?

9. **Marketplace Simulation Scope**: Should the marketplace simulation include all Shadow Shelf Emporium features (cart, checkout, user accounts) or focus only on product browsing and ad display?

10. **Ad Placement Algorithm**: What specific algorithms should determine where and how frequently generated ads appear in the marketplace simulation?

11. **Engagement Simulation**: Should the marketplace simulation include simulated user behavior (clicks, views, interactions) or only display ad placement?

12. **Campaign Data Persistence**: How long should campaign and simulation data be retained for user access and analysis? 