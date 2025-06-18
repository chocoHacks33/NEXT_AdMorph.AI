"""
Business profile management API routes
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

from ...models.business import BusinessProfile, BusinessInsights
from ...services.business_service import BusinessService

router = APIRouter()
business_service = BusinessService()


@router.post("/profile", response_model=Dict[str, Any])
async def create_business_profile(profile_data: Dict[str, Any]):
    """Create new business profile"""
    try:
        # Add required fields if missing
        if "business_id" not in profile_data:
            profile_data["business_id"] = str(uuid.uuid4())
        if "created_at" not in profile_data:
            profile_data["created_at"] = datetime.now().isoformat()
        
        profile = await business_service.create_profile(profile_data)
        return profile.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{business_id}", response_model=Dict[str, Any])
async def get_business_profile(business_id: str):
    """Get business profile by ID"""
    try:
        profile = await business_service.get_profile(business_id)
        if not profile:
            raise HTTPException(status_code=404, detail="Business profile not found")
        return profile.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{business_id}", response_model=Dict[str, Any])
async def update_business_profile(business_id: str, profile_data: Dict[str, Any]):
    """Update business profile"""
    try:
        profile_data["updated_at"] = datetime.now().isoformat()
        profile = await business_service.update_profile(business_id, profile_data)
        if not profile:
            raise HTTPException(status_code=404, detail="Business profile not found")
        return profile.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{business_id}")
async def delete_business_profile(business_id: str):
    """Delete business profile"""
    try:
        success = await business_service.delete_profile(business_id)
        if not success:
            raise HTTPException(status_code=404, detail="Business profile not found")
        return {"message": "Business profile deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{business_id}/insights", response_model=Dict[str, Any])
async def get_business_insights(business_id: str):
    """Get AI-generated business insights"""
    try:
        insights = await business_service.get_insights(business_id)
        if not insights:
            raise HTTPException(status_code=404, detail="Business insights not found")
        return insights.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
