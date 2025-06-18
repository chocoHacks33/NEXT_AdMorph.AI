"""
Ad variant and performance data models
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime
from .demographics import DemographicSegment


@dataclass
class AdVariant:
    """Base ad variant with Ogilvy-inspired copy structure"""
    variant_id: str
    headline: str
    body: str
    cta: str  # Call to action
    image_url: str
    aesthetic_score: float
    ogilvy_score: float  # Based on Ogilvy's 38 rules
    emotional_impact: float
    format_type: str  # 'social', 'display', 'video'
    created_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "variant_id": self.variant_id,
            "headline": self.headline,
            "body": self.body,
            "cta": self.cta,
            "image_url": self.image_url,
            "aesthetic_score": self.aesthetic_score,
            "ogilvy_score": self.ogilvy_score,
            "emotional_impact": self.emotional_impact,
            "format_type": self.format_type,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AdVariant":
        """Create from dictionary"""
        return cls(**data)


@dataclass
class AdVariantMorph(AdVariant):
    """Extended AdVariant with AdMorph capabilities"""
    demographic_segment: Optional[DemographicSegment] = None
    generation_strategy: str = "default"
    mutation_history: List[Dict[str, Any]] = None
    performance_score: float = 0.0
    trend_alignment: float = 0.0
    meta_campaign_id: Optional[str] = None
    is_published: bool = False
    swipe_status: str = "pending"  # "pending", "approved", "rejected", "regenerate"

    def __post_init__(self):
        if self.mutation_history is None:
            self.mutation_history = []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        base_dict = super().to_dict()
        base_dict.update({
            "demographic_segment": self.demographic_segment.to_dict(),
            "generation_strategy": self.generation_strategy,
            "mutation_history": self.mutation_history,
            "performance_score": self.performance_score,
            "trend_alignment": self.trend_alignment,
            "meta_campaign_id": self.meta_campaign_id,
            "is_published": self.is_published,
            "swipe_status": self.swipe_status
        })
        return base_dict
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AdVariantMorph":
        """Create from dictionary"""
        # Handle demographic_segment conversion
        if isinstance(data.get("demographic_segment"), dict):
            data["demographic_segment"] = DemographicSegment.from_dict(data["demographic_segment"])
        return cls(**data)
    
    def add_mutation(self, mutation_type: str, changes: Dict[str, Any], reason: str):
        """Add mutation to history"""
        mutation_record = {
            "timestamp": datetime.now().isoformat(),
            "mutation_type": mutation_type,
            "changes": changes,
            "reason": reason,
            "previous_performance": self.performance_score
        }
        self.mutation_history.append(mutation_record)
    
    def update_performance(self, new_score: float):
        """Update performance score"""
        self.performance_score = new_score


@dataclass
class EngagementMetrics:
    """Real-time performance tracking"""
    variant_id: str
    impressions: int
    clicks: int
    ctr: float  # Click-through rate
    conversions: int
    engagement_rate: float
    timestamp: str
    cost_per_acquisition: float
    spend: float
    revenue: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "variant_id": self.variant_id,
            "impressions": self.impressions,
            "clicks": self.clicks,
            "ctr": self.ctr,
            "conversions": self.conversions,
            "engagement_rate": self.engagement_rate,
            "timestamp": self.timestamp,
            "cost_per_acquisition": self.cost_per_acquisition,
            "spend": self.spend,
            "revenue": self.revenue
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EngagementMetrics":
        """Create from dictionary"""
        return cls(**data)
    
    def calculate_roi(self) -> Optional[float]:
        """Calculate return on investment"""
        if self.revenue and self.spend > 0:
            return (self.revenue - self.spend) / self.spend
        return None
    
    def calculate_performance_score(self) -> float:
        """Calculate overall performance score (0-1)"""
        # Weighted scoring based on key metrics
        ctr_score = min(self.ctr / 0.02, 1.0)  # 2% CTR = perfect score
        engagement_score = min(self.engagement_rate / 0.05, 1.0)  # 5% engagement = perfect
        conversion_score = min(self.conversions / max(self.clicks, 1) / 0.1, 1.0)  # 10% conversion = perfect
        
        # Weighted average
        return (ctr_score * 0.4 + engagement_score * 0.3 + conversion_score * 0.3)
