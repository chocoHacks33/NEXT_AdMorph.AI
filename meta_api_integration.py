"""
Meta Marketing API Integration for AdMorph.AI
Handles publishing approved ads to Facebook/Instagram platforms
"""

import os
import json
import asyncio
import requests
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import uuid
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.adimage import AdImage
from dotenv import load_dotenv

from admorph_core import AdVariantMorph, BusinessProfile, DemographicSegment

# Load environment variables
load_dotenv()

@dataclass
class MetaCampaignConfig:
    """Configuration for Meta campaign creation"""
    campaign_name: str
    objective: str  # 'CONVERSIONS', 'TRAFFIC', 'AWARENESS', 'LEAD_GENERATION'
    budget_amount: int  # Daily budget in cents
    bid_strategy: str = 'LOWEST_COST_WITHOUT_CAP'
    status: str = 'PAUSED'  # Start paused for review

@dataclass
class MetaAdSetConfig:
    """Configuration for Meta ad set creation"""
    name: str
    targeting: Dict[str, Any]
    billing_event: str = 'IMPRESSIONS'
    optimization_goal: str = 'REACH'
    bid_amount: Optional[int] = None
    daily_budget: int = 1000  # In cents

@dataclass
class MetaAdConfig:
    """Configuration for Meta ad creation"""
    name: str
    creative_id: str
    status: str = 'PAUSED'

class MetaMarketingAPIClient:
    """Client for Meta Marketing API operations"""
    
    def __init__(self):
        self.access_token = os.getenv("META_ACCESS_TOKEN")
        self.app_id = os.getenv("META_APP_ID")
        self.app_secret = os.getenv("META_APP_SECRET")
        self.ad_account_id = os.getenv("META_AD_ACCOUNT_ID")
        
        if not all([self.access_token, self.app_id, self.app_secret, self.ad_account_id]):
            raise ValueError("Missing required Meta API credentials in environment variables")
        
        # Initialize Facebook Ads API
        FacebookAdsApi.init(self.app_id, self.app_secret, self.access_token)
        self.ad_account = AdAccount(f"act_{self.ad_account_id}")
    
    async def publish_campaign(self, variants: List[AdVariantMorph], business_profile: BusinessProfile) -> Dict[str, Any]:
        """Publish a complete campaign with multiple ad variants"""
        
        try:
            # Create campaign
            campaign_config = self._create_campaign_config(business_profile)
            campaign = await self._create_campaign(campaign_config)
            
            # Group variants by demographic segment
            segment_groups = self._group_variants_by_segment(variants)
            
            # Create ad sets and ads for each segment
            published_ads = []
            for segment_id, segment_variants in segment_groups.items():
                adset_result = await self._create_adset_for_segment(
                    campaign['id'], 
                    segment_variants[0].demographic_segment,
                    business_profile
                )
                
                for variant in segment_variants:
                    ad_result = await self._create_ad_from_variant(
                        adset_result['id'],
                        variant,
                        business_profile
                    )
                    published_ads.append(ad_result)
            
            return {
                "success": True,
                "campaign_id": campaign['id'],
                "campaign_name": campaign_config.campaign_name,
                "total_ads": len(published_ads),
                "published_ads": published_ads,
                "estimated_reach": await self._estimate_campaign_reach(campaign['id']),
                "created_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__
            }
    
    def _create_campaign_config(self, business_profile: BusinessProfile) -> MetaCampaignConfig:
        """Create campaign configuration based on business profile"""
        
        # Map business goals to Meta objectives
        objective_mapping = {
            "sales": "CONVERSIONS",
            "leads": "LEAD_GENERATION", 
            "awareness": "REACH",
            "traffic": "LINK_CLICKS",
            "app_installs": "APP_INSTALLS"
        }
        
        objective = objective_mapping.get(business_profile.target_engagement, "CONVERSIONS")
        
        # Calculate daily budget (convert monthly to daily, in cents)
        daily_budget_cents = int((business_profile.monthly_budget / 30) * 100)
        
        return MetaCampaignConfig(
            campaign_name=f"{business_profile.business_name}_AdMorph_{datetime.now().strftime('%Y%m%d')}",
            objective=objective,
            budget_amount=daily_budget_cents,
            status="PAUSED"  # Start paused for review
        )
    
    async def _create_campaign(self, config: MetaCampaignConfig) -> Dict[str, Any]:
        """Create Meta campaign"""
        
        campaign_data = {
            Campaign.Field.name: config.campaign_name,
            Campaign.Field.objective: config.objective,
            Campaign.Field.status: config.status,
            Campaign.Field.daily_budget: config.budget_amount,
            Campaign.Field.bid_strategy: config.bid_strategy
        }
        
        try:
            campaign = self.ad_account.create_campaign(fields=[], params=campaign_data)
            return {
                "id": campaign['id'],
                "name": config.campaign_name,
                "objective": config.objective,
                "status": config.status
            }
        except Exception as e:
            raise Exception(f"Failed to create campaign: {str(e)}")
    
    def _group_variants_by_segment(self, variants: List[AdVariantMorph]) -> Dict[str, List[AdVariantMorph]]:
        """Group ad variants by demographic segment"""
        
        groups = {}
        for variant in variants:
            segment_id = variant.demographic_segment.segment_id
            if segment_id not in groups:
                groups[segment_id] = []
            groups[segment_id].append(variant)
        
        return groups
    
    async def _create_adset_for_segment(self, campaign_id: str, segment: DemographicSegment, business_profile: BusinessProfile) -> Dict[str, Any]:
        """Create ad set for a specific demographic segment"""
        
        # Build targeting specification
        targeting = self._build_targeting_spec(segment)
        
        # Calculate budget allocation per segment
        daily_budget_cents = int((business_profile.monthly_budget / 30) * 100)
        
        adset_data = {
            AdSet.Field.name: f"{segment.name}_AdSet",
            AdSet.Field.campaign_id: campaign_id,
            AdSet.Field.daily_budget: daily_budget_cents,
            AdSet.Field.billing_event: 'IMPRESSIONS',
            AdSet.Field.optimization_goal: 'REACH',
            AdSet.Field.targeting: targeting,
            AdSet.Field.status: 'PAUSED'
        }
        
        try:
            adset = self.ad_account.create_ad_set(fields=[], params=adset_data)
            return {
                "id": adset['id'],
                "name": f"{segment.name}_AdSet",
                "targeting": targeting
            }
        except Exception as e:
            raise Exception(f"Failed to create ad set for segment {segment.name}: {str(e)}")
    
    def _build_targeting_spec(self, segment: DemographicSegment) -> Dict[str, Any]:
        """Build Meta targeting specification from demographic segment"""
        
        targeting = {
            "age_min": segment.age_range[0],
            "age_max": segment.age_range[1],
            "geo_locations": {
                "countries": ["US"]  # Default to US, could be configurable
            }
        }
        
        # Add gender targeting if specified
        if segment.gender != "all":
            targeting["genders"] = [1] if segment.gender == "male" else [2]
        
        # Add interest targeting
        if segment.interests:
            # In production, you'd map interests to Meta's interest IDs
            targeting["interests"] = [{"name": interest} for interest in segment.interests[:5]]
        
        # Add behavior targeting
        if segment.behaviors:
            # In production, you'd map behaviors to Meta's behavior IDs
            targeting["behaviors"] = [{"name": behavior} for behavior in segment.behaviors[:3]]
        
        return targeting
    
    async def _create_ad_from_variant(self, adset_id: str, variant: AdVariantMorph, business_profile: BusinessProfile) -> Dict[str, Any]:
        """Create Meta ad from AdMorph variant"""
        
        try:
            # Create ad creative
            creative = await self._create_ad_creative(variant, business_profile)
            
            # Create the ad
            ad_data = {
                Ad.Field.name: f"{variant.headline[:50]}_Ad",
                Ad.Field.adset_id: adset_id,
                Ad.Field.creative: {'creative_id': creative['id']},
                Ad.Field.status: 'PAUSED'
            }
            
            ad = self.ad_account.create_ad(fields=[], params=ad_data)
            
            # Update variant with Meta campaign info
            variant.meta_campaign_id = ad['id']
            variant.is_published = True
            
            return {
                "id": ad['id'],
                "name": ad_data[Ad.Field.name],
                "variant_id": variant.variant_id,
                "creative_id": creative['id'],
                "status": "PAUSED"
            }
            
        except Exception as e:
            raise Exception(f"Failed to create ad from variant {variant.variant_id}: {str(e)}")
    
    async def _create_ad_creative(self, variant: AdVariantMorph, business_profile: BusinessProfile) -> Dict[str, Any]:
        """Create ad creative from variant"""
        
        # For demo purposes, use a placeholder image
        # In production, you'd upload the actual generated image
        image_hash = await self._upload_placeholder_image()
        
        creative_data = {
            AdCreative.Field.name: f"{variant.headline}_Creative",
            AdCreative.Field.object_story_spec: {
                "page_id": "YOUR_PAGE_ID",  # Would be configured per business
                "link_data": {
                    "image_hash": image_hash,
                    "link": "https://your-landing-page.com",  # Would be business-specific
                    "message": variant.body,
                    "name": variant.headline,
                    "call_to_action": {
                        "type": self._map_cta_to_meta(variant.cta)
                    }
                }
            }
        }
        
        try:
            creative = self.ad_account.create_ad_creative(fields=[], params=creative_data)
            return {
                "id": creative['id'],
                "name": creative_data[AdCreative.Field.name]
            }
        except Exception as e:
            raise Exception(f"Failed to create ad creative: {str(e)}")
    
    async def _upload_placeholder_image(self) -> str:
        """Upload placeholder image and return hash"""
        
        # Create a simple placeholder image
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # Create image
        img = Image.new('RGB', (1200, 628), color='#4CAF50')
        draw = ImageDraw.Draw(img)
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        text = "AdMorph.AI Generated Ad"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (1200 - text_width) // 2
        y = (628 - text_height) // 2
        draw.text((x, y), text, fill='white', font=font)
        
        # Save to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Upload to Meta
        try:
            image = self.ad_account.create_ad_image(fields=[], params={'bytes': img_bytes.getvalue()})
            return image['hash']
        except Exception as e:
            # Return a default hash if upload fails
            return "placeholder_hash"
    
    def _map_cta_to_meta(self, cta: str) -> str:
        """Map AdMorph CTA to Meta CTA types"""
        
        cta_mapping = {
            "Learn More": "LEARN_MORE",
            "Sign Up": "SIGN_UP", 
            "Get Started": "SIGN_UP",
            "Buy Now": "SHOP_NOW",
            "Download": "DOWNLOAD",
            "Contact Us": "CONTACT_US",
            "Get Quote": "CONTACT_US"
        }
        
        return cta_mapping.get(cta, "LEARN_MORE")
    
    async def _estimate_campaign_reach(self, campaign_id: str) -> Dict[str, Any]:
        """Estimate campaign reach using Meta's delivery insights"""
        
        # Simplified reach estimation
        # In production, use Meta's reach estimation API
        return {
            "estimated_daily_reach": 10000,
            "estimated_monthly_reach": 300000,
            "confidence": "medium"
        }
    
    async def get_campaign_performance(self, campaign_id: str) -> Dict[str, Any]:
        """Get real-time campaign performance metrics"""
        
        try:
            campaign = Campaign(campaign_id)
            insights = campaign.get_insights(fields=[
                'impressions',
                'clicks',
                'ctr',
                'spend',
                'conversions',
                'cost_per_conversion'
            ])
            
            if insights:
                return insights[0]
            else:
                return {"error": "No insights available yet"}
                
        except Exception as e:
            return {"error": f"Failed to get performance data: {str(e)}"}
    
    async def pause_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Pause a running campaign"""
        
        try:
            campaign = Campaign(campaign_id)
            campaign.update(params={Campaign.Field.status: 'PAUSED'})
            return {"success": True, "status": "PAUSED"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def resume_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Resume a paused campaign"""
        
        try:
            campaign = Campaign(campaign_id)
            campaign.update(params={Campaign.Field.status: 'ACTIVE'})
            return {"success": True, "status": "ACTIVE"}
        except Exception as e:
            return {"success": False, "error": str(e)}

# Campaign Management Helper
class AdMorphCampaignManager:
    """High-level campaign management for AdMorph"""
    
    def __init__(self):
        self.meta_client = MetaMarketingAPIClient()
        self.active_campaigns = {}
    
    async def launch_approved_variants(self, approved_variants: List[AdVariantMorph], business_profile: BusinessProfile) -> Dict[str, Any]:
        """Launch campaign with approved variants"""
        
        if not approved_variants:
            return {"success": False, "error": "No approved variants to launch"}
        
        # Publish to Meta
        result = await self.meta_client.publish_campaign(approved_variants, business_profile)
        
        if result["success"]:
            # Store campaign info for monitoring
            self.active_campaigns[result["campaign_id"]] = {
                "business_profile": business_profile,
                "variants": approved_variants,
                "launch_date": datetime.now(),
                "status": "active"
            }
        
        return result
    
    async def get_all_campaign_performance(self) -> Dict[str, Any]:
        """Get performance data for all active campaigns"""
        
        performance_data = {}
        
        for campaign_id in self.active_campaigns:
            performance = await self.meta_client.get_campaign_performance(campaign_id)
            performance_data[campaign_id] = performance
        
        return performance_data
    
    async def emergency_pause_all(self) -> Dict[str, Any]:
        """Emergency pause all active campaigns"""
        
        results = {}
        
        for campaign_id in self.active_campaigns:
            result = await self.meta_client.pause_campaign(campaign_id)
            results[campaign_id] = result
        
        return results
