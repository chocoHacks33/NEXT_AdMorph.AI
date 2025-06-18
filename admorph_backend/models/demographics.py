"""
Demographic segment data models
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Tuple


@dataclass
class DemographicSegment:
    """Specific demographic segment for ad targeting"""
    segment_id: str
    name: str
    age_range: Tuple[int, int]
    gender: str  # "all", "male", "female"
    interests: List[str]
    behaviors: List[str]
    location: str
    income_level: str  # "Low", "Middle", "High", "Very High"
    education: str
    meta_targeting_spec: Dict[str, Any]
    estimated_reach: Optional[int] = None
    created_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "segment_id": self.segment_id,
            "name": self.name,
            "age_range": list(self.age_range),
            "gender": self.gender,
            "interests": self.interests,
            "behaviors": self.behaviors,
            "location": self.location,
            "income_level": self.income_level,
            "education": self.education,
            "meta_targeting_spec": self.meta_targeting_spec,
            "estimated_reach": self.estimated_reach,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DemographicSegment":
        """Create from dictionary"""
        # Convert age_range back to tuple if it's a list
        if isinstance(data.get("age_range"), list):
            data["age_range"] = tuple(data["age_range"])
        return cls(**data)
    
    def validate(self) -> bool:
        """Validate demographic segment data"""
        if not all([self.segment_id, self.name, self.age_range]):
            return False
            
        if len(self.age_range) != 2 or self.age_range[0] >= self.age_range[1]:
            return False
            
        if self.gender not in ["all", "male", "female"]:
            return False
            
        return True
    
    def get_meta_targeting(self) -> Dict[str, Any]:
        """Get Meta API compatible targeting specification"""
        targeting = {
            "age_min": self.age_range[0],
            "age_max": self.age_range[1],
            "geo_locations": {
                "countries": ["US"] if self.location == "United States" else [self.location]
            }
        }
        
        # Add gender targeting
        if self.gender != "all":
            targeting["genders"] = [1] if self.gender == "male" else [2]
        
        # Add interest targeting from meta_targeting_spec
        if self.meta_targeting_spec.get("meta_id"):
            targeting["interests"] = [{"id": self.meta_targeting_spec["meta_id"]}]
        
        # Add custom audiences if specified
        if "custom_audiences" in self.meta_targeting_spec:
            targeting["custom_audiences"] = self.meta_targeting_spec["custom_audiences"]
            
        return targeting


@dataclass
class SegmentAnalysis:
    """Analysis results for demographic segments"""
    business_id: str
    segments: List[DemographicSegment]
    total_estimated_reach: int
    segment_overlap_analysis: Dict[str, Any]
    recommendations: List[str]
    confidence_scores: Dict[str, float]
    generated_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API serialization"""
        return {
            "business_id": self.business_id,
            "segments": [segment.to_dict() for segment in self.segments],
            "total_estimated_reach": self.total_estimated_reach,
            "segment_overlap_analysis": self.segment_overlap_analysis,
            "recommendations": self.recommendations,
            "confidence_scores": self.confidence_scores,
            "generated_at": self.generated_at
        }
