"""
Business profile management service
"""

from typing import Optional, Dict, Any
from datetime import datetime

from ..models.business import BusinessProfile, BusinessInsights


class BusinessService:
    """Service for managing business profiles"""
    
    def __init__(self):
        # In-memory storage for demo - replace with database in production
        self.profiles_storage = {}
        self.insights_storage = {}
    
    async def create_profile(self, profile_data: Dict[str, Any]) -> BusinessProfile:
        """Create new business profile"""
        profile = BusinessProfile.from_dict(profile_data)
        
        if not profile.validate():
            raise ValueError("Invalid business profile data")
        
        self.profiles_storage[profile.business_id] = profile
        return profile
    
    async def get_profile(self, business_id: str) -> Optional[BusinessProfile]:
        """Get business profile by ID"""
        return self.profiles_storage.get(business_id)
    
    async def update_profile(self, business_id: str, profile_data: Dict[str, Any]) -> Optional[BusinessProfile]:
        """Update business profile"""
        if business_id not in self.profiles_storage:
            return None
        
        profile = self.profiles_storage[business_id]
        
        # Update fields
        for key, value in profile_data.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        return profile
    
    async def delete_profile(self, business_id: str) -> bool:
        """Delete business profile"""
        if business_id in self.profiles_storage:
            del self.profiles_storage[business_id]
            # Also delete associated insights
            if business_id in self.insights_storage:
                del self.insights_storage[business_id]
            return True
        return False
    
    async def get_insights(self, business_id: str) -> Optional[BusinessInsights]:
        """Get AI-generated business insights"""
        return self.insights_storage.get(business_id)
    
    async def generate_insights(self, business_id: str) -> Optional[BusinessInsights]:
        """Generate AI insights for business"""
        profile = self.profiles_storage.get(business_id)
        if not profile:
            return None
        
        # Mock AI-generated insights - in production, use OpenAI
        insights = BusinessInsights(
            business_id=business_id,
            industry_analysis=f"The {profile.industry} industry shows strong growth potential with increasing digital adoption.",
            target_market_analysis=f"Your target audience of {profile.target_audience.get('description', 'general consumers')} represents a valuable market segment.",
            competitive_advantages=[
                "Strong brand positioning",
                "Innovative product features",
                "Excellent customer service"
            ],
            recommended_strategies=[
                "Focus on digital marketing channels",
                "Leverage social media engagement",
                "Implement customer retention programs"
            ],
            risk_factors=[
                "Market competition",
                "Economic uncertainty",
                "Technology disruption"
            ],
            growth_opportunities=[
                "Expand to new geographic markets",
                "Develop complementary products",
                "Strategic partnerships"
            ],
            generated_at=datetime.now().isoformat(),
            confidence_score=0.85
        )
        
        self.insights_storage[business_id] = insights
        return insights
