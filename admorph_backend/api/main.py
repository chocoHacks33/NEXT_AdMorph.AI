"""
FastAPI application factory and configuration
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from typing import Dict, Any

from .routes import ads_router, business_router, demographics_router, campaigns_router, agents_router
from .routes.products import router as products_router
from .websockets import router as websocket_router
from ..config.settings import get_settings


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    settings = get_settings()
    
    app = FastAPI(
        title="AdMorph.AI Agentic Backend",
        description="AI-powered advertising framework with intelligent campaign management",
        version="1.0.0",
        docs_url="/docs" if settings.environment == "development" else None,
        redoc_url="/redoc" if settings.environment == "development" else None
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(business_router, prefix="/api/business", tags=["business"])
    app.include_router(demographics_router, prefix="/api/demographics", tags=["demographics"])
    app.include_router(ads_router, prefix="/api/ads", tags=["ads"])
    app.include_router(campaigns_router, prefix="/api/campaigns", tags=["campaigns"])
    app.include_router(agents_router, prefix="/api/agents", tags=["agents"])
    app.include_router(products_router)  # Products router has its own prefix
    app.include_router(websocket_router, prefix="/ws")
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": str(exc) if settings.environment == "development" else "An error occurred"
            }
        )
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "service": "AdMorph.AI Agentic Backend",
            "version": "1.0.0",
            "environment": settings.environment
        }
    
    # Root endpoint
    @app.get("/")
    async def root():
        return {
            "message": "AdMorph.AI Agentic Backend",
            "version": "1.0.0",
            "docs": "/docs" if settings.environment == "development" else "Documentation not available in production"
        }
    
    return app


def run_server():
    """Run the FastAPI server"""
    settings = get_settings()
    
    uvicorn.run(
        "admorph_backend.api.main:create_app",
        factory=True,
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
        log_level=settings.log_level.lower()
    )


if __name__ == "__main__":
    run_server()
