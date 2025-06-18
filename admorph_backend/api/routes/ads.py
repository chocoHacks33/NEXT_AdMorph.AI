"""
Ad management API routes
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, BackgroundTasks
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

# Temporarily comment out complex imports to get server running
# from ...models.ads import AdVariant, AdVariantMorph, EngagementMetrics
# from ...models.business import BusinessProfile
# from ...models.demographics import DemographicSegment
# from ...services.ad_service import AdService
# from ...services.generation_service import GenerationService

# Simple mock data classes for now
class MockAdVariant:
    def __init__(self, **kwargs):
        self.variant_id = kwargs.get('variant_id', 'mock-id')
        self.headline = kwargs.get('headline', 'Mock Headline')
        self.body = kwargs.get('body', 'Mock Body')
        self.image_url = kwargs.get('image_url', '')
        self.swipe_status = kwargs.get('swipe_status', 'pending')
        self.is_published = kwargs.get('is_published', False)
        self.created_at = kwargs.get('created_at', datetime.now().isoformat())

router = APIRouter()
# Mock services for now
# ad_service = AdService()
# generation_service = GenerationService()


# Response models matching Next.js expectations
class AdResponse:
    def __init__(self, variant: MockAdVariant):
        self.id = variant.variant_id
        self.title = variant.headline
        self.description = variant.body
        self.imageUrl = variant.image_url
        self.status = self._map_status(variant.swipe_status, variant.is_published)
        self.createdAt = variant.created_at or datetime.now().isoformat()
        self.updatedAt = variant.created_at or datetime.now().isoformat()
    
    def _map_status(self, swipe_status: str, is_published: bool) -> str:
        if is_published:
            return "completed"
        elif swipe_status == "pending":
            return "draft"
        elif swipe_status == "approved":
            return "processing"
        else:
            return "failed"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "imageUrl": self.imageUrl,
            "status": self.status,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt
        }


@router.get("/", response_model=List[Dict[str, Any]])
async def get_ads(business_id: Optional[str] = None):
    """Get all ads or ads for specific business"""
    try:
        # Mock data for now
        mock_variants = [
            MockAdVariant(
                variant_id="1",
                headline="Boost Your Team's Productivity",
                body="Transform your remote team with AI-powered collaboration tools",
                image_url="/placeholder.svg?height=400&width=600"
            ),
            MockAdVariant(
                variant_id="2", 
                headline="Scale Your Business Faster",
                body="Join thousands of businesses using our platform to grow",
                image_url="/placeholder.svg?height=400&width=600"
            )
        ]
        return [AdResponse(variant).to_dict() for variant in mock_variants]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{ad_id}", response_model=Dict[str, Any])
async def get_ad(ad_id: str):
    """Get specific ad by ID"""
    try:
        # Mock single ad
        mock_variant = MockAdVariant(
            variant_id=ad_id,
            headline="Boost Your Team's Productivity",
            body="Transform your remote team with AI-powered collaboration tools",
            image_url="/placeholder.svg?height=400&width=600"
        )
        return AdResponse(mock_variant).to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=Dict[str, Any])
async def create_ad(ad_data: Dict[str, Any]):
    """Create new ad variant"""
    try:
        # Convert from Next.js format to internal format
        variant_data = {
            "variant_id": str(uuid.uuid4()),
            "headline": ad_data.get("title", ""),
            "body": ad_data.get("description", ""),
            "cta": ad_data.get("cta", "Learn More"),
            "image_url": ad_data.get("imageUrl", ""),
            "aesthetic_score": 0.8,
            "ogilvy_score": 0.8,
            "emotional_impact": 0.8,
            "format_type": "social",
            "created_at": datetime.now().isoformat()
        }
        
        variant = await ad_service.create_ad(variant_data)
        return AdResponse(variant).to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{ad_id}", response_model=Dict[str, Any])
async def update_ad(ad_id: str, ad_data: Dict[str, Any]):
    """Update existing ad"""
    try:
        variant = await ad_service.update_ad(ad_id, ad_data)
        if not variant:
            raise HTTPException(status_code=404, detail="Ad not found")
        return AdResponse(variant).to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{ad_id}")
async def delete_ad(ad_id: str):
    """Delete ad"""
    try:
        success = await ad_service.delete_ad(ad_id)
        if not success:
            raise HTTPException(status_code=404, detail="Ad not found")
        return {"message": "Ad deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{ad_id}/assets", response_model=List[str])
async def upload_ad_assets(ad_id: str, files: List[UploadFile] = File(...)):
    """Upload assets for ad"""
    try:
        urls = await ad_service.upload_assets(ad_id, files)
        return urls
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate", response_model=Dict[str, Any])
async def generate_ads(
    background_tasks: BackgroundTasks,
    generation_request: Dict[str, Any]
):
    """Generate ad variants for business and demographics"""
    try:
        # Start generation in background
        job_id = str(uuid.uuid4())
        background_tasks.add_task(
            generation_service.generate_ads_async,
            job_id,
            generation_request
        )
        
        return {
            "job_id": job_id,
            "status": "started",
            "message": "Ad generation started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{ad_id}/approve")
async def approve_ad(ad_id: str):
    """Approve ad for campaign launch"""
    try:
        variant = await ad_service.approve_ad(ad_id)
        if not variant:
            raise HTTPException(status_code=404, detail="Ad not found")
        return {"message": "Ad approved successfully", "ad": AdResponse(variant).to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{ad_id}/reject")
async def reject_ad(ad_id: str, feedback: Optional[Dict[str, Any]] = None):
    """Reject ad variant"""
    try:
        variant = await ad_service.reject_ad(ad_id, feedback)
        if not variant:
            raise HTTPException(status_code=404, detail="Ad not found")
        return {"message": "Ad rejected", "ad": AdResponse(variant).to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{ad_id}/regenerate")
async def regenerate_ad(
    ad_id: str, 
    background_tasks: BackgroundTasks,
    regeneration_request: Optional[Dict[str, Any]] = None
):
    """Request ad regeneration"""
    try:
        job_id = str(uuid.uuid4())
        background_tasks.add_task(
            generation_service.regenerate_ad_async,
            job_id,
            ad_id,
            regeneration_request
        )
        
        return {
            "job_id": job_id,
            "status": "started",
            "message": "Ad regeneration started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
