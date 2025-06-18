"""
Campaign management API routes
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any, List, Optional
import uuid

from ...models.campaigns import CampaignConfig, CampaignResult
from ...services.campaign_service import CampaignService

router = APIRouter()
campaign_service = CampaignService()


@router.post("/launch", response_model=Dict[str, Any])
async def launch_campaign(
    background_tasks: BackgroundTasks,
    launch_request: Dict[str, Any]
):
    """Launch campaign with approved ad variants"""
    try:
        approved_variants = launch_request.get("approvedVariants", [])
        business_profile = launch_request.get("businessProfile", {})
        
        if not approved_variants:
            raise HTTPException(status_code=400, detail="No approved variants provided")
        
        job_id = str(uuid.uuid4())
        background_tasks.add_task(
            campaign_service.launch_campaign_async,
            job_id,
            approved_variants,
            business_profile
        )
        
        return {
            "job_id": job_id,
            "status": "started",
            "message": "Campaign launch started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{campaign_id}", response_model=Dict[str, Any])
async def get_campaign(campaign_id: str):
    """Get campaign details"""
    try:
        campaign = await campaign_service.get_campaign(campaign_id)
        if not campaign:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return campaign.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{campaign_id}/pause")
async def pause_campaign(campaign_id: str):
    """Pause active campaign"""
    try:
        result = await campaign_service.pause_campaign(campaign_id)
        if not result:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return {"message": "Campaign paused successfully", "campaign": result.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{campaign_id}/resume")
async def resume_campaign(campaign_id: str):
    """Resume paused campaign"""
    try:
        result = await campaign_service.resume_campaign(campaign_id)
        if not result:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return {"message": "Campaign resumed successfully", "campaign": result.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{campaign_id}/performance", response_model=Dict[str, Any])
async def get_campaign_performance(campaign_id: str):
    """Get campaign performance metrics"""
    try:
        performance = await campaign_service.get_performance_metrics(campaign_id)
        if not performance:
            raise HTTPException(status_code=404, detail="Performance data not found")
        return performance
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/business/{business_id}", response_model=List[Dict[str, Any]])
async def get_business_campaigns(business_id: str):
    """Get all campaigns for a business"""
    try:
        campaigns = await campaign_service.get_business_campaigns(business_id)
        return [campaign.to_dict() for campaign in campaigns]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{campaign_id}")
async def delete_campaign(campaign_id: str):
    """Delete campaign"""
    try:
        success = await campaign_service.delete_campaign(campaign_id)
        if not success:
            raise HTTPException(status_code=404, detail="Campaign not found")
        return {"message": "Campaign deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{campaign_id}/optimize")
async def optimize_campaign(
    campaign_id: str,
    background_tasks: BackgroundTasks,
    optimization_request: Optional[Dict[str, Any]] = None
):
    """Start campaign optimization"""
    try:
        job_id = str(uuid.uuid4())
        background_tasks.add_task(
            campaign_service.optimize_campaign_async,
            job_id,
            campaign_id,
            optimization_request or {}
        )
        
        return {
            "job_id": job_id,
            "status": "started",
            "message": "Campaign optimization started"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
