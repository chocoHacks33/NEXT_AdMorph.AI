"""
Business profile data models
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class BusinessProfile:
    """Complete business profile for campaign generation"""
    business_id: str
    business_name: str
    industry: str
    description: str
    target_audience: Dict[str, Any]
    monthly_budget: float
    campaign_goals: List[str]
    brand_voice: str
    unique_selling_points: List[str]
    competitors: List[str]
    geographic_focus: List[str]
    created_at: str
    updated_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "business_id": self.business_id,
            "business_name": self.business_name,
            "industry": self.industry,
            "description": self.description,
            "target_audience": self.target_audience,
            "monthly_budget": self.monthly_budget,
            "campaign_goals": self.campaign_goals,
            "brand_voice": self.brand_voice,
            "unique_selling_points": self.unique_selling_points,
            "competitors": self.competitors,
            "geographic_focus": self.geographic_focus,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BusinessProfile":
        """Create from dictionary"""
        return cls(**data)
    
    def validate(self) -> bool:
        """Validate business profile data"""
        required_fields = [
            "business_id", "business_name", "industry", 
            "description", "monthly_budget"
        ]
        
        for field in required_fields:
            if not getattr(self, field):
                return False
                
        if self.monthly_budget <= 0:
            return False
            
        return True


@dataclass 
class BusinessInsights:
    """AI-generated insights about the business"""
    business_id: str
    industry_analysis: str
    target_market_analysis: str
    competitive_advantages: List[str]
    recommended_strategies: List[str]
    risk_factors: List[str]
    growth_opportunities: List[str]
    generated_at: str
    confidence_score: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "business_id": self.business_id,
            "industry_analysis": self.industry_analysis,
            "target_market_analysis": self.target_market_analysis,
            "competitive_advantages": self.competitive_advantages,
            "recommended_strategies": self.recommended_strategies,
            "risk_factors": self.risk_factors,
            "growth_opportunities": self.growth_opportunities,
            "generated_at": self.generated_at,
            "confidence_score": self.confidence_score
        }
