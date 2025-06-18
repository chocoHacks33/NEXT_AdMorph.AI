# AdMorph.AI Voice Agent Integration Plan

## Current State Analysis

### Frontend Components
- `voice-interface.tsx`: Main voice interaction UI with simulated voice commands
- `voice-agent-narrator.tsx`: Smaller component using browser SpeechSynthesis API

### Backend Services
- `voice_service.py`: Mocked voice narration service with async job processing
- `/voice/narrate` endpoint: Accepts text and returns job ID
- `/voice/narration/{job_id}` endpoint: Checks narration job status

## Planned Changes

### Frontend Modifications
1. Replace browser SpeechSynthesis with backend API calls:
   - Call `/voice/narrate` with narration text
   - Poll `/voice/narration/{job_id}` for completion
   - Play returned audio URL when ready

2. Enhance voice command processing:
   - Send voice commands to backend for processing
   - Handle responses appropriately in UI

### Backend Enhancements
1. Implement actual voice generation service:
   - Integrate with a TTS provider (AWS Polly, Google TTS, etc.)
   - Add proper audio file storage/streaming

2. Improve voice command processing:
   - Add NLP for command interpretation
   - Connect to business logic/services

## Implementation Steps

1. [ ] Create API client service for voice endpoints
2. [ ] Modify voice-interface.tsx to use backend services
3. [ ] Update voice-agent-narrator.tsx for backend integration
4. [ ] Implement proper TTS service in voice_service.py
5. [ ] Add voice command processing logic
6. [ ] Add error handling and loading states

## Recommendations

### For Development Team
1. Choose a TTS provider (AWS Polly recommended for scalability)
2. Set up proper audio file storage (S3 or similar)
3. Consider adding voice command training interface
4. Add analytics for voice interaction metrics

### For Product Team
1. Define voice command vocabulary/syntax
2. Plan voice personality/branding
3. Consider multi-language support roadmap
4. Plan accessibility features

## Future Enhancements
1. Real-time voice streaming
2. Voice profile customization
3. Context-aware voice commands
4. Voice-based ad editing
5. Multi-user voice collaboration
