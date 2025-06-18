"""
Campaign management data models
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime
from .ads import AdVariantMorph


@dataclass
class CampaignConfig:
    """Configuration for campaign creation"""
    campaign_id: str
    business_id: str
    campaign_name: str
    objective: str  # "CONVERSIONS", "TRAFFIC", "AWARENESS", etc.
    budget_amount: float
    budget_type: str  # "DAILY", "LIFETIME"
    bid_strategy: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: str = "PAUSED"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "campaign_id": self.campaign_id,
            "business_id": self.business_id,
            "campaign_name": self.campaign_name,
            "objective": self.objective,
            "budget_amount": self.budget_amount,
            "budget_type": self.budget_type,
            "bid_strategy": self.bid_strategy,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CampaignConfig":
        """Create from dictionary"""
        return cls(**data)


@dataclass
class CampaignResult:
    """Result of campaign creation and management"""
    campaign_id: str
    meta_campaign_id: Optional[str]
    business_id: str
    status: str
    variants_published: List[AdVariantMorph]
    created_at: str
    launched_at: Optional[str] = None
    paused_at: Optional[str] = None
    total_spend: float = 0.0
    total_impressions: int = 0
    total_clicks: int = 0
    total_conversions: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "campaign_id": self.campaign_id,
            "meta_campaign_id": self.meta_campaign_id,
            "business_id": self.business_id,
            "status": self.status,
            "variants_published": [variant.to_dict() for variant in self.variants_published],
            "created_at": self.created_at,
            "launched_at": self.launched_at,
            "paused_at": self.paused_at,
            "total_spend": self.total_spend,
            "total_impressions": self.total_impressions,
            "total_clicks": self.total_clicks,
            "total_conversions": self.total_conversions
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CampaignResult":
        """Create from dictionary"""
        # Handle variants_published conversion
        if data.get("variants_published"):
            data["variants_published"] = [
                AdVariantMorph.from_dict(variant) if isinstance(variant, dict) else variant
                for variant in data["variants_published"]
            ]
        return cls(**data)
    
    def update_performance(self, spend: float, impressions: int, clicks: int, conversions: int):
        """Update campaign performance metrics"""
        self.total_spend += spend
        self.total_impressions += impressions
        self.total_clicks += clicks
        self.total_conversions += conversions
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get campaign performance summary"""
        ctr = (self.total_clicks / self.total_impressions) if self.total_impressions > 0 else 0
        conversion_rate = (self.total_conversions / self.total_clicks) if self.total_clicks > 0 else 0
        cost_per_click = (self.total_spend / self.total_clicks) if self.total_clicks > 0 else 0
        cost_per_conversion = (self.total_spend / self.total_conversions) if self.total_conversions > 0 else 0
        
        return {
            "total_spend": self.total_spend,
            "total_impressions": self.total_impressions,
            "total_clicks": self.total_clicks,
            "total_conversions": self.total_conversions,
            "ctr": ctr,
            "conversion_rate": conversion_rate,
            "cost_per_click": cost_per_click,
            "cost_per_conversion": cost_per_conversion,
            "variants_count": len(self.variants_published)
        }


@dataclass
class CampaignEvolution:
    """Campaign evolution tracking"""
    campaign_id: str
    evolution_cycle_id: str
    started_at: str
    completed_at: Optional[str] = None
    mutations_created: int = 0
    performance_improvements: List[Dict[str, Any]] = None
    trend_alignments: List[Dict[str, Any]] = None
    status: str = "running"  # "running", "completed", "paused", "failed"
    
    def __post_init__(self):
        if self.performance_improvements is None:
            self.performance_improvements = []
        if self.trend_alignments is None:
            self.trend_alignments = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "campaign_id": self.campaign_id,
            "evolution_cycle_id": self.evolution_cycle_id,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "mutations_created": self.mutations_created,
            "performance_improvements": self.performance_improvements,
            "trend_alignments": self.trend_alignments,
            "status": self.status
        }
    
    def add_mutation(self, variant_id: str, mutation_type: str, improvement_score: float):
        """Add mutation record"""
        self.mutations_created += 1
        self.performance_improvements.append({
            "variant_id": variant_id,
            "mutation_type": mutation_type,
            "improvement_score": improvement_score,
            "timestamp": datetime.now().isoformat()
        })
    
    def complete_cycle(self):
        """Mark evolution cycle as completed"""
        self.completed_at = datetime.now().isoformat()
        self.status = "completed"
