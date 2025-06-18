"""
API route modules
"""

from fastapi import APIRouter

# Create a main router that combines all routes
router = APIRouter()

# Import individual routers (we'll fix imports in each file)
try:
    from .ads import router as ads_router
    router.include_router(ads_router, prefix="/ads", tags=["ads"])
except ImportError as e:
    print(f"Warning: Could not import ads router: {e}")

try:
    from .business import router as business_router
    router.include_router(business_router, prefix="/business", tags=["business"])
except ImportError as e:
    print(f"Warning: Could not import business router: {e}")

try:
    from .demographics import router as demographics_router
    router.include_router(demographics_router, prefix="/demographics", tags=["demographics"])
except ImportError as e:
    print(f"Warning: Could not import demographics router: {e}")

try:
    from .campaigns import router as campaigns_router
    router.include_router(campaigns_router, prefix="/campaigns", tags=["campaigns"])
except ImportError as e:
    print(f"Warning: Could not import campaigns router: {e}")

try:
    from .agents import router as agents_router
    router.include_router(agents_router, prefix="/agents", tags=["agents"])
except ImportError as e:
    print(f"Warning: Could not import agents router: {e}")

__all__ = ["router"]
