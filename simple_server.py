#!/usr/bin/env python3
"""
Simple FastAPI server for AdMorph.AI - Quick start version
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import uvicorn
from datetime import datetime

# Create FastAPI app
app = FastAPI(
    title="AdMorph.AI Simple Backend",
    description="Simplified API for testing frontend integration",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock data
mock_ads = [
    {
        "id": "1",
        "title": "Boost Your Team's Productivity",
        "description": "Transform your remote team with AI-powered collaboration tools",
        "imageUrl": "/placeholder.svg?height=400&width=600",
        "status": "completed",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    },
    {
        "id": "2", 
        "title": "Scale Your Business Faster",
        "description": "Join thousands of businesses using our platform to grow",
        "imageUrl": "/placeholder.svg?height=400&width=600",
        "status": "processing",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
]

# Routes
@app.get("/")
async def root():
    return {
        "message": "AdMorph.AI Simple Backend",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AdMorph.AI Simple Backend",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/ads")
async def get_ads():
    """Get all ads"""
    return mock_ads

@app.get("/api/ads/{ad_id}")
async def get_ad(ad_id: str):
    """Get specific ad by ID"""
    for ad in mock_ads:
        if ad["id"] == ad_id:
            return ad
    raise HTTPException(status_code=404, detail="Ad not found")

@app.post("/api/ads")
async def create_ad(ad_data: Dict[str, Any]):
    """Create new ad"""
    new_ad = {
        "id": str(len(mock_ads) + 1),
        "title": ad_data.get("title", "New Ad"),
        "description": ad_data.get("description", "New ad description"),
        "imageUrl": ad_data.get("imageUrl", "/placeholder.svg?height=400&width=600"),
        "status": "processing",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
    mock_ads.append(new_ad)
    return new_ad

@app.get("/api/processing/jobs")
async def get_processing_jobs():
    """Get processing jobs"""
    return [
        {
            "id": "job-1",
            "adId": "1",
            "status": "completed",
            "progress": 100,
            "message": "Ad generation completed",
            "createdAt": datetime.now().isoformat()
        }
    ]

@app.post("/api/agents/chat")
async def send_chat_message(message_data: Dict[str, Any]):
    """Send chat message to AI agent"""
    message = message_data.get("message", "")
    return {
        "response": f"Thanks for your message: '{message}'. This is a mock response from the AI agent.",
        "sessionId": "mock-session-123"
    }

@app.get("/api/analytics/performance")
async def get_performance_metrics():
    """Get performance metrics"""
    return [
        {
            "adId": "1",
            "impressions": 1000,
            "clicks": 50,
            "conversions": 5,
            "ctr": 5.0,
            "cost": 100.0,
            "revenue": 500.0
        }
    ]

if __name__ == "__main__":
    print("🚀 Starting AdMorph.AI Simple Backend...")
    print("📡 Server will be available at: http://localhost:8001")
    print("📖 API docs at: http://localhost:8001/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)