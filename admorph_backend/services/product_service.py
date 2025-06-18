"""
Product personalization service
"""

import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..models.products import (
    BaseProduct, ProductVariant, PersonalizationRequest, 
    PersonalizationResult, ProductPerformanceMetrics
)
from ..models.demographics import DemographicSegment
from ..core.product_personalization_agent import ProductPersonalizationAgent


class ProductService:
    """Service for product personalization and management"""
    
    def __init__(self):
        # In-memory storage for demo - replace with database in production
        self.products_storage = {}
        self.variants_storage = {}
        self.personalization_jobs = {}
        self.performance_storage = {}
        
        # Initialize AI agent
        self.personalization_agent = ProductPersonalizationAgent()
        
        # Load sample products for testing
        self._load_sample_products()
    
    def _load_sample_products(self):
        """Load sample products for testing"""
        sample_products = [
            BaseProduct(
                product_id="wireless-headphones-001",
                name="Premium Wireless Headphones",
                base_price=99.99,
                category="Electronics",
                brand="AudioTech",
                features=[
                    "Bluetooth 5.0 connectivity",
                    "20-hour battery life", 
                    "Active noise cancellation",
                    "Quick charge (15min = 3hrs)",
                    "Premium leather comfort",
                    "Crystal clear calls"
                ],
                specifications={
                    "driver_size": "40mm",
                    "frequency_response": "20Hz-20kHz",
                    "impedance": "32 ohms",
                    "weight": "250g",
                    "charging_time": "2 hours",
                    "wireless_range": "30 feet"
                },
                base_images=[
                    "https://example.com/headphones-main.jpg",
                    "https://example.com/headphones-side.jpg"
                ],
                inventory_count=150,
                created_at=datetime.now().isoformat()
            ),
            BaseProduct(
                product_id="fitness-tracker-002",
                name="Smart Fitness Tracker",
                base_price=149.99,
                category="Wearables",
                brand="FitLife",
                features=[
                    "Heart rate monitoring",
                    "GPS tracking",
                    "Sleep analysis",
                    "Waterproof design",
                    "7-day battery life",
                    "Smartphone notifications"
                ],
                specifications={
                    "display": "1.4 inch AMOLED",
                    "water_resistance": "5ATM",
                    "sensors": ["Heart rate", "GPS", "Accelerometer", "Gyroscope"],
                    "compatibility": ["iOS", "Android"],
                    "weight": "45g",
                    "charging_method": "Magnetic dock"
                },
                base_images=[
                    "https://example.com/tracker-main.jpg",
                    "https://example.com/tracker-sport.jpg"
                ],
                inventory_count=200,
                created_at=datetime.now().isoformat()
            )
        ]
        
        for product in sample_products:
            self.products_storage[product.product_id] = product
    
    async def get_products(self) -> List[BaseProduct]:
        """Get all products"""
        return list(self.products_storage.values())
    
    async def get_product(self, product_id: str) -> Optional[BaseProduct]:
        """Get specific product by ID"""
        return self.products_storage.get(product_id)
    
    async def create_product(self, product_data: Dict[str, Any]) -> BaseProduct:
        """Create new product"""
        if "product_id" not in product_data:
            product_data["product_id"] = str(uuid.uuid4())
        if "created_at" not in product_data:
            product_data["created_at"] = datetime.now().isoformat()
        
        product = BaseProduct.from_dict(product_data)
        self.products_storage[product.product_id] = product
        return product
    
    async def personalize_product_async(
        self, 
        job_id: str, 
        personalization_request: PersonalizationRequest
    ):
        """Generate personalized product variants (async)"""
        try:
            # Get base product
            base_product = self.products_storage.get(personalization_request.product_id)
            if not base_product:
                raise ValueError(f"Product {personalization_request.product_id} not found")
            
            # Execute personalization with AI agent
            context = {
                "personalization_request": personalization_request,
                "base_product": base_product
            }
            
            result = await self.personalization_agent.execute(context)
            
            if result["success"]:
                personalization_result = result["result"]
                
                # Store variants
                for variant in personalization_result.generated_variants:
                    self.variants_storage[variant.variant_id] = variant
                
                # Store job result
                self.personalization_jobs[job_id] = {
                    "status": "completed",
                    "result": personalization_result.to_dict(),
                    "completed_at": datetime.now().isoformat()
                }
            else:
                self.personalization_jobs[job_id] = {
                    "status": "failed",
                    "error": result["error"],
                    "completed_at": datetime.now().isoformat()
                }
                
        except Exception as e:
            self.personalization_jobs[job_id] = {
                "status": "failed",
                "error": str(e),
                "completed_at": datetime.now().isoformat()
            }
    
    async def get_personalization_result(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get personalization job result"""
        return self.personalization_jobs.get(job_id)
    
    async def get_product_variants(self, product_id: str) -> List[ProductVariant]:
        """Get all variants for a product"""
        variants = [
            variant for variant in self.variants_storage.values()
            if variant.product_id == product_id
        ]
        return variants
    
    async def get_variant(self, variant_id: str) -> Optional[ProductVariant]:
        """Get specific variant by ID"""
        return self.variants_storage.get(variant_id)
    
    async def update_variant_performance(
        self, 
        variant_id: str, 
        views: int = 0, 
        purchases: int = 0
    ) -> Optional[ProductVariant]:
        """Update variant performance metrics"""
        variant = self.variants_storage.get(variant_id)
        if variant:
            variant.update_performance(views, purchases)
            return variant
        return None
    
    async def get_performance_metrics(
        self, 
        product_id: str, 
        time_period: str = "7d"
    ) -> Optional[ProductPerformanceMetrics]:
        """Get performance metrics for product"""
        
        # Mock performance data - in production, this would come from analytics
        metrics = ProductPerformanceMetrics(
            product_id=product_id,
            variant_id="all",
            time_period=time_period,
            total_views=1250,
            unique_views=980,
            total_purchases=45,
            conversion_rate=0.036,
            average_time_on_page=125.5,
            bounce_rate=0.35,
            revenue_generated=4499.55,
            cost_per_acquisition=15.50,
            return_on_ad_spend=3.2,
            demographic_breakdown={
                "young_professionals": {"views": 450, "purchases": 18, "conversion_rate": 0.04},
                "fitness_enthusiasts": {"views": 380, "purchases": 15, "conversion_rate": 0.039},
                "tech_early_adopters": {"views": 420, "purchases": 12, "conversion_rate": 0.029}
            },
            timestamp=datetime.now().isoformat()
        )
        
        return metrics
    
    async def create_sample_demographics(self) -> List[DemographicSegment]:
        """Create sample demographic segments for testing"""
        demographics = [
            DemographicSegment(
                segment_id="young-professionals",
                name="Young Professionals",
                age_range=(25, 35),
                gender="all",
                interests=["Technology", "Career Development", "Productivity"],
                behaviors=["Early adopters", "Quality-focused", "Time-conscious"],
                location="United States",
                income_level="High",
                education="Bachelor's",
                meta_targeting_spec={
                    "category": "Professional",
                    "relevance_score": 0.9
                }
            ),
            DemographicSegment(
                segment_id="fitness-enthusiasts",
                name="Fitness Enthusiasts",
                age_range=(22, 40),
                gender="all",
                interests=["Fitness", "Health", "Sports", "Wellness"],
                behaviors=["Health-conscious", "Active lifestyle", "Goal-oriented"],
                location="United States",
                income_level="Middle",
                education="High School",
                meta_targeting_spec={
                    "category": "Fitness",
                    "relevance_score": 0.95
                }
            ),
            DemographicSegment(
                segment_id="tech-early-adopters",
                name="Tech Early Adopters",
                age_range=(18, 45),
                gender="all",
                interests=["Technology", "Gadgets", "Innovation", "Gaming"],
                behaviors=["Early adopters", "Tech-savvy", "Research-driven"],
                location="United States",
                income_level="High",
                education="Bachelor's",
                meta_targeting_spec={
                    "category": "Technology",
                    "relevance_score": 0.92
                }
            )
        ]
        
        return demographics
    
    async def run_ab_test(
        self, 
        variant_ids: List[str], 
        test_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run A/B test between variants"""
        
        # Mock A/B test results
        test_results = {
            "test_id": str(uuid.uuid4()),
            "variant_ids": variant_ids,
            "test_config": test_config,
            "results": {
                variant_ids[0]: {
                    "views": 500,
                    "purchases": 25,
                    "conversion_rate": 0.05,
                    "confidence": 0.95
                },
                variant_ids[1]: {
                    "views": 500,
                    "purchases": 18,
                    "conversion_rate": 0.036,
                    "confidence": 0.85
                }
            },
            "winner": variant_ids[0],
            "statistical_significance": True,
            "improvement": 38.9,
            "started_at": datetime.now().isoformat(),
            "completed_at": datetime.now().isoformat()
        }
        
        return test_results
