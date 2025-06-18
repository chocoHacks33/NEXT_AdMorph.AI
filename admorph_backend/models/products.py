"""
E-commerce product personalization data models
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from .demographics import DemographicSegment


@dataclass
class BaseProduct:
    """Base product information"""
    product_id: str
    name: str
    base_price: float
    category: str
    brand: str
    features: List[str]
    specifications: Dict[str, Any]
    base_images: List[str]
    inventory_count: int
    created_at: str
    updated_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "base_price": self.base_price,
            "category": self.category,
            "brand": self.brand,
            "features": self.features,
            "specifications": self.specifications,
            "base_images": self.base_images,
            "inventory_count": self.inventory_count,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseProduct":
        """Create from dictionary"""
        return cls(**data)


@dataclass
class ProductVariant:
    """Personalized product variant for specific demographic"""
    variant_id: str
    product_id: str
    demographic_segment: DemographicSegment
    personalized_title: str
    personalized_description: str
    highlighted_features: List[str]
    price_positioning: str  # "value", "premium", "budget", "performance"
    image_prompts: List[str]
    generated_images: List[str]
    call_to_action: str
    urgency_messaging: Optional[str] = None
    social_proof: Optional[str] = None
    personalization_score: float = 0.0
    conversion_rate: float = 0.0
    view_count: int = 0
    purchase_count: int = 0
    created_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "variant_id": self.variant_id,
            "product_id": self.product_id,
            "demographic_segment": self.demographic_segment.to_dict(),
            "personalized_title": self.personalized_title,
            "personalized_description": self.personalized_description,
            "highlighted_features": self.highlighted_features,
            "price_positioning": self.price_positioning,
            "image_prompts": self.image_prompts,
            "generated_images": self.generated_images,
            "call_to_action": self.call_to_action,
            "urgency_messaging": self.urgency_messaging,
            "social_proof": self.social_proof,
            "personalization_score": self.personalization_score,
            "conversion_rate": self.conversion_rate,
            "view_count": self.view_count,
            "purchase_count": self.purchase_count,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProductVariant":
        """Create from dictionary"""
        if isinstance(data.get("demographic_segment"), dict):
            data["demographic_segment"] = DemographicSegment.from_dict(data["demographic_segment"])
        return cls(**data)
    
    def update_performance(self, views: int = 0, purchases: int = 0):
        """Update performance metrics"""
        self.view_count += views
        self.purchase_count += purchases
        if self.view_count > 0:
            self.conversion_rate = self.purchase_count / self.view_count


@dataclass
class PersonalizationRequest:
    """Request for product personalization"""
    request_id: str
    product_id: str
    target_demographics: List[DemographicSegment]
    personalization_goals: List[str]  # ["increase_conversion", "highlight_features", "price_optimize"]
    platform_context: str  # "amazon", "shopify", "woocommerce", "custom"
    brand_guidelines: Optional[Dict[str, Any]] = None
    competitor_analysis: Optional[List[str]] = None
    seasonal_context: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "request_id": self.request_id,
            "product_id": self.product_id,
            "target_demographics": [demo.to_dict() for demo in self.target_demographics],
            "personalization_goals": self.personalization_goals,
            "platform_context": self.platform_context,
            "brand_guidelines": self.brand_guidelines,
            "competitor_analysis": self.competitor_analysis,
            "seasonal_context": self.seasonal_context
        }


@dataclass
class PersonalizationResult:
    """Result of product personalization process"""
    request_id: str
    product_id: str
    generated_variants: List[ProductVariant]
    personalization_insights: Dict[str, Any]
    a_b_test_recommendations: List[Dict[str, Any]]
    estimated_performance_lift: float
    processing_time: float
    generated_at: str
    status: str = "completed"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "request_id": self.request_id,
            "product_id": self.product_id,
            "generated_variants": [variant.to_dict() for variant in self.generated_variants],
            "personalization_insights": self.personalization_insights,
            "a_b_test_recommendations": self.a_b_test_recommendations,
            "estimated_performance_lift": self.estimated_performance_lift,
            "processing_time": self.processing_time,
            "generated_at": self.generated_at,
            "status": self.status
        }


@dataclass
class ProductPerformanceMetrics:
    """Performance tracking for product variants"""
    product_id: str
    variant_id: str
    time_period: str
    total_views: int
    unique_views: int
    total_purchases: int
    conversion_rate: float
    average_time_on_page: float
    bounce_rate: float
    revenue_generated: float
    cost_per_acquisition: float
    return_on_ad_spend: float
    demographic_breakdown: Dict[str, Dict[str, float]]
    timestamp: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "product_id": self.product_id,
            "variant_id": self.variant_id,
            "time_period": self.time_period,
            "total_views": self.total_views,
            "unique_views": self.unique_views,
            "total_purchases": self.total_purchases,
            "conversion_rate": self.conversion_rate,
            "average_time_on_page": self.average_time_on_page,
            "bounce_rate": self.bounce_rate,
            "revenue_generated": self.revenue_generated,
            "cost_per_acquisition": self.cost_per_acquisition,
            "return_on_ad_spend": self.return_on_ad_spend,
            "demographic_breakdown": self.demographic_breakdown,
            "timestamp": self.timestamp
        }
    
    def calculate_performance_score(self) -> float:
        """Calculate overall performance score (0-1)"""
        # Weighted scoring based on key e-commerce metrics
        conversion_score = min(self.conversion_rate / 0.05, 1.0)  # 5% conversion = perfect
        engagement_score = min((1 - self.bounce_rate), 1.0)  # Low bounce rate = good
        revenue_score = min(self.return_on_ad_spend / 4.0, 1.0)  # 4x ROAS = perfect
        
        # Weighted average
        return (conversion_score * 0.5 + engagement_score * 0.2 + revenue_score * 0.3)
