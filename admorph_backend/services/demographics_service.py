"""
Demographics analysis service
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from ..models.demographics import DemographicSegment, SegmentAnalysis


class DemographicsService:
    """Service for demographic analysis and segment management"""
    
    def __init__(self):
        # In-memory storage for demo
        self.segments_storage = {}
        self.analysis_jobs = {}
    
    async def analyze_demographics_async(self, job_id: str, business_data: Dict[str, Any]):
        """Analyze business and create demographic segments (async)"""
        try:
            # Mock analysis - in production, use AI agents
            segments = await self._generate_mock_segments(business_data)
            
            analysis = SegmentAnalysis(
                business_id=business_data.get("business_id", "unknown"),
                segments=segments,
                total_estimated_reach=sum(s.estimated_reach or 0 for s in segments),
                segment_overlap_analysis={"overlap_percentage": 15.5},
                recommendations=[
                    "Focus on the 25-40 age group for highest engagement",
                    "Consider expanding to mobile-first demographics",
                    "Test video content for younger segments"
                ],
                confidence_scores={s.segment_id: 0.8 for s in segments},
                generated_at=datetime.now().isoformat()
            )
            
            self.analysis_jobs[job_id] = {
                "status": "completed",
                "result": analysis.to_dict(),
                "completed_at": datetime.now().isoformat()
            }
            
            # Store segments
            for segment in segments:
                self.segments_storage[segment.segment_id] = segment
                
        except Exception as e:
            self.analysis_jobs[job_id] = {
                "status": "failed",
                "error": str(e),
                "completed_at": datetime.now().isoformat()
            }
    
    async def _generate_mock_segments(self, business_data: Dict[str, Any]) -> List[DemographicSegment]:
        """Generate mock demographic segments"""
        industry = business_data.get("industry", "technology")
        
        segments = [
            DemographicSegment(
                segment_id=str(uuid.uuid4()),
                name="Young Professionals",
                age_range=(25, 35),
                gender="all",
                interests=["Technology", "Career Development", "Innovation"],
                behaviors=["Early adopters", "Tech-savvy"],
                location="United States",
                income_level="High",
                education="Bachelor's",
                meta_targeting_spec={
                    "meta_id": "6002884511422",
                    "category": "Small business",
                    "relevance_score": 0.9
                },
                estimated_reach=150000,
                created_at=datetime.now().isoformat()
            ),
            DemographicSegment(
                segment_id=str(uuid.uuid4()),
                name="Digital Natives",
                age_range=(18, 28),
                gender="all",
                interests=["Social Media", "Mobile Apps", "Digital Content"],
                behaviors=["Mobile-first", "Social media active"],
                location="United States",
                income_level="Middle",
                education="High School",
                meta_targeting_spec={
                    "meta_id": "6003127206524",
                    "category": "Digital marketing",
                    "relevance_score": 0.85
                },
                estimated_reach=200000,
                created_at=datetime.now().isoformat()
            )
        ]
        
        return segments
    
    async def get_segments(self, business_id: str) -> List[DemographicSegment]:
        """Get demographic segments for business"""
        # Filter segments by business_id
        segments = [
            segment for segment in self.segments_storage.values()
            if hasattr(segment, 'business_id') and getattr(segment, 'business_id', None) == business_id
        ]
        return segments
    
    async def get_analysis_result(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get demographic analysis results"""
        return self.analysis_jobs.get(job_id)
    
    async def create_segment(self, segment_data: Dict[str, Any]) -> DemographicSegment:
        """Create custom demographic segment"""
        segment = DemographicSegment.from_dict(segment_data)
        
        if not segment.validate():
            raise ValueError("Invalid segment data")
        
        self.segments_storage[segment.segment_id] = segment
        return segment
    
    async def update_segment(self, segment_id: str, segment_data: Dict[str, Any]) -> Optional[DemographicSegment]:
        """Update demographic segment"""
        if segment_id not in self.segments_storage:
            return None
        
        segment = self.segments_storage[segment_id]
        
        # Update fields
        for key, value in segment_data.items():
            if hasattr(segment, key):
                setattr(segment, key, value)
        
        return segment
    
    async def delete_segment(self, segment_id: str) -> bool:
        """Delete demographic segment"""
        if segment_id in self.segments_storage:
            del self.segments_storage[segment_id]
            return True
        return False
