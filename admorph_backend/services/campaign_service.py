"""
Campaign management service
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from ..models.campaigns import CampaignConfig, CampaignResult, CampaignEvolution
from ..models.ads import AdVariantMorph


class CampaignService:
    """Service for campaign management"""
    
    def __init__(self):
        # In-memory storage for demo
        self.campaigns_storage = {}
        self.launch_jobs = {}
        self.optimization_jobs = {}
    
    async def launch_campaign_async(self, job_id: str, approved_variants: List[Dict[str, Any]], business_profile: Dict[str, Any]):
        """Launch campaign with approved variants (async)"""
        try:
            campaign_id = str(uuid.uuid4())
            
            # Convert variant dicts to objects
            variants = [AdVariantMorph.from_dict(v) if isinstance(v, dict) else v for v in approved_variants]
            
            # Create campaign result
            campaign = CampaignResult(
                campaign_id=campaign_id,
                meta_campaign_id=f"meta_{campaign_id}",
                business_id=business_profile.get("business_id", "unknown"),
                status="active",
                variants_published=variants,
                created_at=datetime.now().isoformat(),
                launched_at=datetime.now().isoformat()
            )
            
            self.campaigns_storage[campaign_id] = campaign
            
            self.launch_jobs[job_id] = {
                "status": "completed",
                "campaign_id": campaign_id,
                "result": campaign.to_dict(),
                "completed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.launch_jobs[job_id] = {
                "status": "failed",
                "error": str(e),
                "completed_at": datetime.now().isoformat()
            }
    
    async def get_campaign(self, campaign_id: str) -> Optional[CampaignResult]:
        """Get campaign details"""
        return self.campaigns_storage.get(campaign_id)
    
    async def pause_campaign(self, campaign_id: str) -> Optional[CampaignResult]:
        """Pause active campaign"""
        campaign = self.campaigns_storage.get(campaign_id)
        if not campaign:
            return None
        
        campaign.status = "paused"
        campaign.paused_at = datetime.now().isoformat()
        
        return campaign
    
    async def resume_campaign(self, campaign_id: str) -> Optional[CampaignResult]:
        """Resume paused campaign"""
        campaign = self.campaigns_storage.get(campaign_id)
        if not campaign:
            return None
        
        campaign.status = "active"
        campaign.paused_at = None
        
        return campaign
    
    async def get_performance_metrics(self, campaign_id: str) -> Optional[Dict[str, Any]]:
        """Get campaign performance metrics"""
        campaign = self.campaigns_storage.get(campaign_id)
        if not campaign:
            return None
        
        # Mock performance data
        return {
            "campaign_id": campaign_id,
            "impressions": 15000,
            "clicks": 450,
            "ctr": 0.03,
            "conversions": 23,
            "conversion_rate": 0.051,
            "spend": 125.50,
            "cost_per_click": 0.28,
            "cost_per_conversion": 5.46,
            "return_on_ad_spend": 3.2,
            "last_updated": datetime.now().isoformat()
        }
    
    async def get_business_campaigns(self, business_id: str) -> List[CampaignResult]:
        """Get all campaigns for a business"""
        campaigns = [
            campaign for campaign in self.campaigns_storage.values()
            if campaign.business_id == business_id
        ]
        return campaigns
    
    async def delete_campaign(self, campaign_id: str) -> bool:
        """Delete campaign"""
        if campaign_id in self.campaigns_storage:
            del self.campaigns_storage[campaign_id]
            return True
        return False
    
    async def optimize_campaign_async(self, job_id: str, campaign_id: str, optimization_request: Dict[str, Any]):
        """Start campaign optimization (async)"""
        try:
            campaign = self.campaigns_storage.get(campaign_id)
            if not campaign:
                raise ValueError("Campaign not found")
            
            # Mock optimization process
            evolution = CampaignEvolution(
                campaign_id=campaign_id,
                evolution_cycle_id=str(uuid.uuid4()),
                started_at=datetime.now().isoformat(),
                mutations_created=3,
                performance_improvements=[
                    {
                        "variant_id": "var_1",
                        "improvement_type": "headline_optimization",
                        "improvement_score": 0.15,
                        "timestamp": datetime.now().isoformat()
                    }
                ],
                trend_alignments=[
                    {
                        "trend": "mobile_first_design",
                        "alignment_score": 0.8,
                        "timestamp": datetime.now().isoformat()
                    }
                ]
            )
            
            evolution.complete_cycle()
            
            self.optimization_jobs[job_id] = {
                "status": "completed",
                "result": evolution.to_dict(),
                "completed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.optimization_jobs[job_id] = {
                "status": "failed",
                "error": str(e),
                "completed_at": datetime.now().isoformat()
            }
