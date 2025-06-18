"""
FastAPI interface layer for AdMorph.AI agentic backend
"""

from .main import create_app
from .routes import router
from .websockets import websocket_manager

__all__ = ["create_app", "router", "websocket_manager"]
