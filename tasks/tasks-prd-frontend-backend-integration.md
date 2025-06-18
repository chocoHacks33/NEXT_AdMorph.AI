# Task List: AdMorph.AI Frontend-Backend Integration

## Relevant Files

- `lib/api-client.ts` - Central API client for all backend communication with error handling and retry logic.
- `lib/api-client.test.ts` - Unit tests for API client functionality.
- `lib/websocket-client.ts` - WebSocket client for real-time communication with reconnection logic.
- `lib/websocket-client.test.ts` - Unit tests for WebSocket client.
- `lib/session-manager.ts` - Session management utilities for JWT tokens and user state.
- `lib/session-manager.test.ts` - Unit tests for session management.
- `lib/types/api.ts` - TypeScript interfaces for API requests and responses.
- `components/voice-interface.tsx` - Existing voice interface component (modify for backend integration).
- `components/processing-panel.tsx` - Existing processing panel component (modify for real-time updates).
- `components/ad-gallery.tsx` - Existing ad gallery component (modify for backend ad data).
- `hooks/use-api.ts` - Custom React hook for API operations with loading states.
- `hooks/use-api.test.ts` - Unit tests for API hook.
- `hooks/use-websocket.ts` - Custom React hook for WebSocket connections.
- `hooks/use-websocket.test.ts` - Unit tests for WebSocket hook.
- `contexts/SessionContext.tsx` - React context for session state management.
- `contexts/WorkflowContext.tsx` - React context for workflow state management.
- `utils/error-handler.ts` - Centralized error handling utilities.
- `utils/error-handler.test.ts` - Unit tests for error handling.
- `admorph_backend/api/routes/voice.py` - Backend API routes for voice consultation.
- `admorph_backend/api/routes/generation.py` - Backend API routes for ad generation.
- `admorph_backend/api/routes/sessions.py` - Backend API routes for session management.
- `admorph_backend/api/websockets.py` - WebSocket handlers for real-time updates.
- `docker-compose.production.yml` - Production Docker configuration.
- `aws/ecs-task-definition.json` - AWS ECS task definition for deployment.
- `aws/cloudformation.yml` - AWS infrastructure as code template.
- `.env.production` - Production environment variables template.

### Notes

- Unit tests should typically be placed alongside the code files they are testing (e.g., `api-client.tsx` and `api-client.test.tsx` in the same directory).
- Use `npx jest [optional/path/to/test/file]` to run tests. Running without a path executes all tests found by the Jest configuration.
- Backend API routes should follow RESTful conventions and include proper error handling.
- WebSocket connections should implement automatic reconnection with exponential backoff.

## Tasks

- [ ] 1.0 Implement Core API Integration Layer
  - [ ] 1.1 Create centralized API client service (`lib/api-client.ts`) with axios configuration, error handling, and retry logic
  - [ ] 1.2 Implement session management utilities (`lib/session-manager.ts`) for JWT token handling and user state persistence
  - [ ] 1.3 Define TypeScript interfaces (`lib/types/api.ts`) for all API requests and responses based on backend models
  - [ ] 1.4 Create error handling utilities (`utils/error-handler.ts`) for consistent error processing and user-friendly messages
  - [ ] 1.5 Set up React contexts (`contexts/SessionContext.tsx`, `contexts/WorkflowContext.tsx`) for global state management
  - [ ] 1.6 Write comprehensive unit tests for all API integration components

- [ ] 2.0 Establish Real-time Communication System
  - [ ] 2.1 Create WebSocket client (`lib/websocket-client.ts`) with connection management and automatic reconnection
  - [ ] 2.2 Implement WebSocket React hook (`hooks/use-websocket.ts`) for component-level WebSocket integration
  - [ ] 2.3 Design message type system for different update categories (voice_progress, generation_progress, error_alerts)
  - [ ] 2.4 Add WebSocket fallback strategy with HTTP polling for connection failures
  - [ ] 2.5 Implement backend WebSocket handlers (`admorph_backend/api/websockets.py`) for broadcasting updates
  - [ ] 2.6 Create WebSocket connection health monitoring and status indicators in UI

- [ ] 3.0 Integrate Voice Interface with Backend AI Agents
  - [ ] 3.1 Modify voice-interface.tsx to send voice input to backend AdMorphVoiceAgent via API
  - [ ] 3.2 Implement voice consultation API endpoints (`admorph_backend/api/routes/voice.py`) for business profile extraction
  - [ ] 3.3 Add real-time progress updates during voice processing using WebSocket connections
  - [ ] 3.4 Create business profile data flow from voice consultation to demographics analysis
  - [ ] 3.5 Implement error handling for voice processing failures with user-friendly messages
  - [ ] 3.6 Add loading states and progress indicators for voice consultation workflow

- [ ] 4.0 Connect Ad Generation and Review Workflow
  - [ ] 4.1 Integrate processing-panel.tsx with backend generation services for real-time demographics analysis updates
  - [ ] 4.2 Modify ad-gallery.tsx to display AdVariantMorph objects from backend with demographic segment information
  - [ ] 4.3 Implement swipe decision handling (approve/reject/regenerate) with backend API communication
  - [ ] 4.4 Create ad generation API endpoints (`admorph_backend/api/routes/generation.py`) for demographics and ad creation
  - [ ] 4.5 Add ad regeneration workflow with feedback loop integration
  - [ ] 4.6 Implement data consistency between demographics analysis and ad generation steps
  - [ ] 4.7 Add cancel operation functionality for long-running ad generation processes

- [ ] 5.0 Set Up AWS Production Deployment Infrastructure
  - [ ] 5.1 Create production Docker configuration (`docker-compose.production.yml`) for multi-service deployment
  - [ ] 5.2 Set up AWS ECS task definitions (`aws/ecs-task-definition.json`) for containerized backend deployment
  - [ ] 5.3 Configure AWS infrastructure using CloudFormation (`aws/cloudformation.yml`) including ECS, RDS, ElastiCache, S3
  - [ ] 5.4 Implement AWS Secrets Manager integration for secure API key management (OpenAI, Meta)
  - [ ] 5.5 Set up AWS Application Load Balancer with auto-scaling groups for high availability
  - [ ] 5.6 Configure CloudFront CDN for frontend static asset delivery
  - [ ] 5.7 Implement CloudWatch monitoring, logging, and alerting for production environment
  - [ ] 5.8 Create deployment pipeline with blue-green deployment strategy for zero-downtime updates 