"""
Agent interaction API routes (chat, voice, etc.)
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, Optional
import uuid
from datetime import datetime

from ...services.agent_service import AgentService
from ...services.voice_service import VoiceService

router = APIRouter()
agent_service = AgentService()
voice_service = VoiceService()


@router.post("/chat", response_model=Dict[str, Any])
async def send_chat_message(message_data: Dict[str, Any]):
    """Send message to chat agent"""
    try:
        message = message_data.get("message", "")
        session_id = message_data.get("sessionId")
        
        if not message:
            raise HTTPException(status_code=400, detail="Message is required")
        
        # Generate session ID if not provided
        if not session_id:
            session_id = str(uuid.uuid4())
        
        response = await agent_service.process_chat_message(message, session_id)
        
        return {
            "response": response,
            "sessionId": session_id,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/voice/narrate", response_model=Dict[str, Any])
async def get_voice_narration(
    background_tasks: BackgroundTasks,
    narration_request: Dict[str, Any]
):
    """Generate voice narration for text"""
    try:
        text = narration_request.get("text", "")
        voice = narration_request.get("voice", "default")
        
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        # Generate audio in background
        job_id = str(uuid.uuid4())
        background_tasks.add_task(
            voice_service.generate_narration_async,
            job_id,
            text,
            voice
        )
        
        return {
            "job_id": job_id,
            "status": "processing",
            "message": "Voice narration generation started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/voice/narration/{job_id}")
async def get_narration_status(job_id: str):
    """Get voice narration job status"""
    try:
        result = await voice_service.get_narration_status(job_id)
        if not result:
            raise HTTPException(status_code=404, detail="Job not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/business/onboard", response_model=Dict[str, Any])
async def start_business_onboarding(onboarding_data: Dict[str, Any]):
    """Start voice-powered business onboarding"""
    try:
        session_id = str(uuid.uuid4())
        initial_data = onboarding_data.get("initialData", {})
        
        result = await agent_service.start_onboarding(session_id, initial_data)
        
        return {
            "sessionId": session_id,
            "stage": result.get("stage", "introduction"),
            "message": result.get("message", ""),
            "questions": result.get("questions", []),
            "progress": result.get("progress", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/business/onboard/{session_id}/respond")
async def respond_to_onboarding(session_id: str, response_data: Dict[str, Any]):
    """Respond to onboarding questions"""
    try:
        response = response_data.get("response", "")
        
        if not response:
            raise HTTPException(status_code=400, detail="Response is required")
        
        result = await agent_service.process_onboarding_response(session_id, response)
        
        return {
            "sessionId": session_id,
            "stage": result.get("stage", ""),
            "message": result.get("message", ""),
            "questions": result.get("questions", []),
            "progress": result.get("progress", 0),
            "completed": result.get("completed", False),
            "businessProfile": result.get("businessProfile")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/business/onboard/{session_id}/status")
async def get_onboarding_status(session_id: str):
    """Get onboarding session status"""
    try:
        result = await agent_service.get_onboarding_status(session_id)
        if not result:
            raise HTTPException(status_code=404, detail="Session not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze/business", response_model=Dict[str, Any])
async def analyze_business(
    background_tasks: BackgroundTasks,
    analysis_request: Dict[str, Any]
):
    """Analyze business and generate insights"""
    try:
        business_data = analysis_request.get("businessData", {})
        
        if not business_data:
            raise HTTPException(status_code=400, detail="Business data is required")
        
        job_id = str(uuid.uuid4())
        background_tasks.add_task(
            agent_service.analyze_business_async,
            job_id,
            business_data
        )
        
        return {
            "job_id": job_id,
            "status": "started",
            "message": "Business analysis started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analyze/business/{job_id}")
async def get_business_analysis(job_id: str):
    """Get business analysis results"""
    try:
        result = await agent_service.get_analysis_result(job_id)
        if not result:
            raise HTTPException(status_code=404, detail="Analysis not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_agent_stats():
    """Get agent performance statistics"""
    try:
        stats = await agent_service.get_agent_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
