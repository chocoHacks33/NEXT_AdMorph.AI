"""
Ad generation service
"""

from typing import Dict, Any, Optional
from datetime import datetime
import uuid

from ..models.ads import AdVariantMorph
from ..models.demographics import DemographicSegment


class GenerationService:
    """Service for ad generation and regeneration"""
    
    def __init__(self):
        # In-memory storage for demo
        self.generation_jobs = {}
    
    async def generate_ads_async(self, job_id: str, generation_request: Dict[str, Any]):
        """Generate ad variants for business and demographics (async)"""
        try:
            business_profile = generation_request.get("businessProfile", {})
            segments = generation_request.get("segments", [])
            
            # Mock ad generation
            generated_ads = []
            
            for i, segment_data in enumerate(segments):
                if isinstance(segment_data, dict):
                    segment = DemographicSegment.from_dict(segment_data)
                else:
                    segment = segment_data
                
                # Generate 2-3 variants per segment
                for j in range(2):
                    variant = AdVariantMorph(
                        variant_id=str(uuid.uuid4()),
                        headline=f"Perfect Solution for {segment.name}",
                        body=f"Discover how our innovative approach transforms {segment.interests[0] if segment.interests else 'your business'} with cutting-edge technology.",
                        cta="Learn More",
                        image_url="",
                        aesthetic_score=0.85 + (j * 0.05),
                        ogilvy_score=0.82 + (j * 0.03),
                        emotional_impact=0.88 + (j * 0.04),
                        format_type="social",
                        demographic_segment=segment,
                        generation_strategy="ai_powered",
                        mutation_history=[],
                        performance_score=0.0,
                        trend_alignment=0.85,
                        created_at=datetime.now().isoformat()
                    )
                    generated_ads.append(variant)
            
            self.generation_jobs[job_id] = {
                "status": "completed",
                "ads": [ad.to_dict() for ad in generated_ads],
                "total_generated": len(generated_ads),
                "completed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.generation_jobs[job_id] = {
                "status": "failed",
                "error": str(e),
                "completed_at": datetime.now().isoformat()
            }
    
    async def regenerate_ad_async(self, job_id: str, ad_id: str, regeneration_request: Dict[str, Any]):
        """Regenerate specific ad variant (async)"""
        try:
            feedback = regeneration_request.get("feedback", "")
            
            # Mock regeneration
            regenerated_ad = AdVariantMorph(
                variant_id=str(uuid.uuid4()),
                headline="Enhanced Solution Based on Your Feedback",
                body="Our improved approach addresses your specific needs with advanced features and proven results.",
                cta="Get Started",
                image_url="",
                aesthetic_score=0.90,
                ogilvy_score=0.88,
                emotional_impact=0.92,
                format_type="social",
                demographic_segment=DemographicSegment(
                    segment_id="regenerated",
                    name="Refined Audience",
                    age_range=(25, 45),
                    gender="all",
                    interests=["Innovation", "Quality"],
                    behaviors=["Value-conscious"],
                    location="United States",
                    income_level="Middle",
                    education="Bachelor's",
                    meta_targeting_spec={}
                ),
                generation_strategy="regenerated_with_feedback",
                mutation_history=[{
                    "timestamp": datetime.now().isoformat(),
                    "mutation_type": "regeneration",
                    "feedback": feedback,
                    "original_ad_id": ad_id
                }],
                performance_score=0.0,
                trend_alignment=0.88,
                created_at=datetime.now().isoformat()
            )
            
            self.generation_jobs[job_id] = {
                "status": "completed",
                "regenerated_ad": regenerated_ad.to_dict(),
                "original_ad_id": ad_id,
                "completed_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.generation_jobs[job_id] = {
                "status": "failed",
                "error": str(e),
                "completed_at": datetime.now().isoformat()
            }
    
    async def get_generation_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get generation job status"""
        return self.generation_jobs.get(job_id)
