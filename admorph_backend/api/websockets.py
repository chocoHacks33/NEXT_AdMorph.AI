"""
WebSocket handlers for real-time communication
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import asyncio
from datetime import datetime

router = APIRouter()


class WebSocketManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {
            "generation": [],
            "performance": [],
            "chat": {}
        }
    
    async def connect(self, websocket: WebSocket, connection_type: str, session_id: str = None):
        """Connect a WebSocket"""
        await websocket.accept()
        
        if connection_type == "chat" and session_id:
            if session_id not in self.active_connections["chat"]:
                self.active_connections["chat"][session_id] = []
            self.active_connections["chat"][session_id].append(websocket)
        else:
            self.active_connections[connection_type].append(websocket)
    
    def disconnect(self, websocket: WebSocket, connection_type: str, session_id: str = None):
        """Disconnect a WebSocket"""
        if connection_type == "chat" and session_id:
            if session_id in self.active_connections["chat"]:
                if websocket in self.active_connections["chat"][session_id]:
                    self.active_connections["chat"][session_id].remove(websocket)
        else:
            if websocket in self.active_connections[connection_type]:
                self.active_connections[connection_type].remove(websocket)
    
    async def send_personal_message(self, message: str, websocket: WebSocket):
        """Send message to specific WebSocket"""
        try:
            await websocket.send_text(message)
        except:
            pass  # Connection might be closed
    
    async def broadcast_to_type(self, message: str, connection_type: str):
        """Broadcast message to all connections of a type"""
        connections = self.active_connections.get(connection_type, [])
        for connection in connections:
            try:
                await connection.send_text(message)
            except:
                # Remove dead connections
                connections.remove(connection)
    
    async def send_to_session(self, message: str, session_id: str):
        """Send message to specific chat session"""
        if session_id in self.active_connections["chat"]:
            for connection in self.active_connections["chat"][session_id]:
                try:
                    await connection.send_text(message)
                except:
                    pass


websocket_manager = WebSocketManager()


@router.websocket("/generation")
async def websocket_generation(websocket: WebSocket):
    """WebSocket endpoint for real-time ad generation updates"""
    await websocket_manager.connect(websocket, "generation")
    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Echo back for demo purposes
            response = {
                "type": "generation_status",
                "message": "Generation system is active",
                "timestamp": datetime.now().isoformat()
            }
            await websocket_manager.send_personal_message(json.dumps(response), websocket)
            
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, "generation")


@router.websocket("/performance")
async def websocket_performance(websocket: WebSocket):
    """WebSocket endpoint for real-time performance metrics"""
    await websocket_manager.connect(websocket, "performance")
    try:
        while True:
            # Send mock performance updates every 30 seconds
            await asyncio.sleep(30)
            
            performance_update = {
                "type": "metrics_update",
                "metrics": {
                    "impressions": 1500,
                    "clicks": 45,
                    "ctr": 0.03,
                    "conversions": 3,
                    "spend": 12.50
                },
                "timestamp": datetime.now().isoformat()
            }
            
            await websocket_manager.send_personal_message(
                json.dumps(performance_update), 
                websocket
            )
            
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, "performance")


@router.websocket("/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for chat interactions"""
    await websocket_manager.connect(websocket, "chat", session_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Echo the message back with AI response
            response = {
                "type": "chat_message",
                "session_id": session_id,
                "user_message": message_data.get("message", ""),
                "ai_response": "I understand your request. Let me help you with that.",
                "timestamp": datetime.now().isoformat()
            }
            
            await websocket_manager.send_to_session(json.dumps(response), session_id)
            
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket, "chat", session_id)


# Helper functions for broadcasting updates
async def broadcast_generation_update(job_id: str, status: str, progress: int = None, result: dict = None):
    """Broadcast generation update to all connected clients"""
    message = {
        "type": "generation_update",
        "job_id": job_id,
        "status": status,
        "progress": progress,
        "result": result,
        "timestamp": datetime.now().isoformat()
    }
    
    await websocket_manager.broadcast_to_type(json.dumps(message), "generation")


async def broadcast_performance_update(campaign_id: str, metrics: dict):
    """Broadcast performance update to all connected clients"""
    message = {
        "type": "performance_update",
        "campaign_id": campaign_id,
        "metrics": metrics,
        "timestamp": datetime.now().isoformat()
    }
    
    await websocket_manager.broadcast_to_type(json.dumps(message), "performance")
