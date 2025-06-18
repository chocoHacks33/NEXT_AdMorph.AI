"""
Ad management service
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from ..models.ads import AdVariantMorph
from ..models.demographics import DemographicSegment


class AdService:
    """Service for managing ad variants"""
    
    def __init__(self):
        # In-memory storage for demo - replace with database in production
        self.ads_storage = {}
    
    async def get_ads(self, business_id: Optional[str] = None) -> List[AdVariantMorph]:
        """Get all ads or ads for specific business"""
        ads = list(self.ads_storage.values())
        
        if business_id:
            # Filter by business_id if provided
            ads = [ad for ad in ads if hasattr(ad, 'business_id') and ad.business_id == business_id]
        
        return ads
    
    async def get_ad(self, ad_id: str) -> Optional[AdVariantMorph]:
        """Get specific ad by ID"""
        return self.ads_storage.get(ad_id)
    
    async def create_ad(self, ad_data: Dict[str, Any]) -> AdVariantMorph:
        """Create new ad variant"""
        # Create a basic demographic segment if not provided
        if "demographic_segment" not in ad_data:
            ad_data["demographic_segment"] = DemographicSegment(
                segment_id="default",
                name="General Audience",
                age_range=(18, 65),
                gender="all",
                interests=[],
                behaviors=[],
                location="United States",
                income_level="Middle",
                education="High School",
                meta_targeting_spec={}
            )
        
        # Set default values for required fields
        ad_data.setdefault("generation_strategy", "manual")
        ad_data.setdefault("mutation_history", [])
        ad_data.setdefault("performance_score", 0.0)
        ad_data.setdefault("trend_alignment", 0.0)
        ad_data.setdefault("swipe_status", "pending")
        ad_data.setdefault("is_published", False)
        
        variant = AdVariantMorph(**ad_data)
        self.ads_storage[variant.variant_id] = variant
        
        return variant
    
    async def update_ad(self, ad_id: str, ad_data: Dict[str, Any]) -> Optional[AdVariantMorph]:
        """Update existing ad"""
        if ad_id not in self.ads_storage:
            return None
        
        variant = self.ads_storage[ad_id]
        
        # Update fields
        for key, value in ad_data.items():
            if hasattr(variant, key):
                setattr(variant, key, value)
        
        return variant
    
    async def delete_ad(self, ad_id: str) -> bool:
        """Delete ad"""
        if ad_id in self.ads_storage:
            del self.ads_storage[ad_id]
            return True
        return False
    
    async def upload_assets(self, ad_id: str, files: List[Any]) -> List[str]:
        """Upload assets for ad"""
        # Mock implementation - in production, upload to cloud storage
        urls = []
        for i, file in enumerate(files):
            url = f"https://storage.admorph.ai/ads/{ad_id}/asset_{i}.jpg"
            urls.append(url)
        
        # Update ad with image URLs
        if ad_id in self.ads_storage:
            variant = self.ads_storage[ad_id]
            if urls:
                variant.image_url = urls[0]  # Use first uploaded image
        
        return urls
    
    async def approve_ad(self, ad_id: str) -> Optional[AdVariantMorph]:
        """Approve ad for campaign launch"""
        if ad_id not in self.ads_storage:
            return None
        
        variant = self.ads_storage[ad_id]
        variant.swipe_status = "approved"
        
        return variant
    
    async def reject_ad(self, ad_id: str, feedback: Optional[Dict[str, Any]] = None) -> Optional[AdVariantMorph]:
        """Reject ad variant"""
        if ad_id not in self.ads_storage:
            return None
        
        variant = self.ads_storage[ad_id]
        variant.swipe_status = "rejected"
        
        # Store feedback in mutation history
        if feedback:
            variant.add_mutation("rejection", feedback, "User feedback")
        
        return variant
