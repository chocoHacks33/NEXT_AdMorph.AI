"""
Product and e-commerce personalization service
"""

import uuid
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from ..database.connection import product_repo, business_repo, db_manager
from ..core.product_personalization_agent import ProductPersonalizationAgent
from ..models.demographics import DemographicSegment
from ..models.business import BusinessProfile

logger = logging.getLogger(__name__)


class ProductService:
    """Service for product management and personalization"""
    
    def __init__(self):
        self.personalization_agent = ProductPersonalizationAgent()
        self.active_jobs = {}  # Track background jobs
    
    async def get_products(self) -> List[Dict[str, Any]]:
        """Get all products"""
        try:
            query = """
            SELECT bp.*, b.business_name 
            FROM base_products bp
            LEFT JOIN business_profiles b ON bp.business_id = b.business_id
            ORDER BY bp.created_at DESC
            """
            results = await db_manager.execute_query(query)
            
            # Convert to BaseProduct objects for consistency
            products = []
            for result in results:
                product_data = {
                    'product_id': result['product_id'],
                    'business_id': str(result['business_id']),
                    'name': result['name'],
                    'description': result['description'],
                    'price': float(result['price']) if result['price'] else 0.0,
                    'category': result['category'],
                    'features': result['features'] or [],
                    'images': result['images'] or [],
                    'platform': result['platform'],
                    'platform_product_id': result['platform_product_id'],
                    'business_name': result.get('business_name', '')
                }
                products.append(product_data)
            
            return products
            
        except Exception as e:
            logger.error(f"Error getting products: {e}")
            raise
    
    async def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific product"""
        try:
            query = """
            SELECT bp.*, b.business_name 
            FROM base_products bp
            LEFT JOIN business_profiles b ON bp.business_id = b.business_id
            WHERE bp.product_id = $1
            """
            result = await db_manager.execute_one(query, product_id)
            
            if not result:
                return None
            
            return {
                'product_id': result['product_id'],
                'business_id': str(result['business_id']),
                'name': result['name'],
                'description': result['description'],
                'price': float(result['price']) if result['price'] else 0.0,
                'category': result['category'],
                'features': result['features'] or [],
                'images': result['images'] or [],
                'platform': result['platform'],
                'platform_product_id': result['platform_product_id'],
                'business_name': result.get('business_name', '')
            }
            
        except Exception as e:
            logger.error(f"Error getting product {product_id}: {e}")
            raise
    
    async def create_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new product"""
        try:
            # Generate product ID if not provided
            if 'product_id' not in product_data:
                product_data['product_id'] = f"product-{uuid.uuid4().hex[:8]}"
            
            # Create in database
            product_id = await product_repo.create_product(product_data)
            
            # Return created product
            return await self.get_product(product_id)
            
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            raise
    
    async def get_product_variants(self, product_id: str) -> List[Dict[str, Any]]:
        """Get all variants for a product"""
        try:
            return await product_repo.get_product_variants(product_id)
        except Exception as e:
            logger.error(f"Error getting product variants for {product_id}: {e}")
            raise
    
    async def personalize_product_async(self, job_id: str, personalization_request: Any):
        """Run product personalization in background"""
        try:
            logger.info(f"Starting product personalization job {job_id}")
            
            # Update job status
            self.active_jobs[job_id] = {
                'status': 'running',
                'progress': 0,
                'started_at': datetime.now().isoformat()
            }
            
            # Get the base product
            product = await self.get_product(personalization_request.product_id)
            if not product:
                raise ValueError(f"Product {personalization_request.product_id} not found")
            
            # Convert to BaseProduct object for agent
            from ..models.ads import BaseProduct  # Import here to avoid circular imports
            base_product = BaseProduct(
                product_id=product['product_id'],
                name=product['name'],
                description=product['description'],
                price=product['price'],
                category=product['category'],
                features=product['features'],
                images=product['images']
            )
            
            # Update progress
            self.active_jobs[job_id]['progress'] = 25
            
            # Run personalization agent
            context = {
                'personalization_request': personalization_request,
                'base_product': base_product
            }
            
            result = await self.personalization_agent.execute(context)
            
            if result.get('success'):
                personalization_result = result['result']
                
                # Update progress
                self.active_jobs[job_id]['progress'] = 75
                
                # Save variants to database
                for variant in personalization_result.generated_variants:
                    variant_data = {
                        'product_id': product['product_id'],
                        'demographic_segment_id': variant.demographic_segment.segment_id if variant.demographic_segment else None,
                        'personalized_title': variant.personalized_title,
                        'personalized_description': variant.personalized_description,
                        'highlighted_features': variant.highlighted_features,
                        'personalized_cta': variant.personalized_cta,
                        'price_positioning': variant.price_positioning,
                        'urgency_messaging': variant.urgency_messaging,
                        'social_proof': variant.social_proof,
                        'personalization_score': variant.personalization_score,
                        'conversion_lift_estimate': variant.conversion_lift_estimate
                    }
                    await product_repo.create_variant(variant_data)
                
                # Complete job
                self.active_jobs[job_id].update({
                    'status': 'completed',
                    'progress': 100,
                    'completed_at': datetime.now().isoformat(),
                    'result': personalization_result.to_dict()
                })
                
                logger.info(f"Product personalization job {job_id} completed successfully")
                
            else:
                raise Exception("Personalization agent failed")
                
        except Exception as e:
            logger.error(f"Product personalization job {job_id} failed: {e}")
            self.active_jobs[job_id].update({
                'status': 'failed',
                'error': str(e),
                'completed_at': datetime.now().isoformat()
            })
            raise
    
    async def get_personalization_result(self, job_id: str) -> Dict[str, Any]:
        """Get personalization job result"""
        if job_id not in self.active_jobs:
            raise ValueError(f"Job {job_id} not found")
        
        job_data = self.active_jobs[job_id]
        
        if job_data['status'] == 'completed':
            return {
                'status': 'completed',
                'result': job_data['result']
            }
        elif job_data['status'] == 'failed':
            return {
                'status': 'failed',
                'error': job_data['error']
            }
        else:
            return {
                'status': job_data['status'],
                'progress': job_data['progress']
            }
    
    async def create_sample_demographics(self) -> List[DemographicSegment]:
        """Create sample demographic segments for testing"""
        demographics = [
            DemographicSegment(
                segment_id="demo-fitness-enthusiasts",
                name="Fitness Enthusiasts",
                age_range=[22, 40],
                gender="mixed",
                income_range="$40k-$80k",
                interests=["fitness", "health", "wellness", "sports"],
                behaviors=["gym_membership", "health_app_usage", "supplement_purchases"],
                psychographics={"lifestyle": "active", "values": ["health", "performance"]}
            ),
            DemographicSegment(
                segment_id="demo-business-professionals",
                name="Business Professionals",
                age_range=[28, 45],
                gender="mixed",
                income_range="$60k-$120k",
                interests=["business", "technology", "productivity", "networking"],
                behaviors=["linkedin_usage", "business_travel", "premium_subscriptions"],
                psychographics={"lifestyle": "busy", "values": ["efficiency", "success"]}
            ),
            DemographicSegment(
                segment_id="demo-tech-early-adopters",
                name="Tech Early Adopters",
                age_range=[25, 35],
                gender="mixed",
                income_range="$50k-$100k",
                interests=["technology", "gadgets", "innovation", "gaming"],
                behaviors=["early_tech_adoption", "online_reviews", "social_sharing"],
                psychographics={"lifestyle": "digital", "values": ["innovation", "convenience"]}
            )
        ]
        return demographics
    
    async def run_ab_test(self, variant_ids: List[str], test_config: Dict[str, Any]) -> Dict[str, Any]:
        """Run A/B test on product variants"""
        try:
            # Create A/B test record
            test_id = str(uuid.uuid4())
            
            # Simulate A/B test results for demo
            import random
            
            winner_id = random.choice(variant_ids)
            improvement = random.uniform(5.0, 25.0)
            significance = random.uniform(0.95, 0.99)
            
            result = {
                'test_id': test_id,
                'winner': winner_id,
                'improvement': improvement,
                'statistical_significance': significance,
                'confidence_level': test_config.get('confidence_level', 0.95),
                'test_duration_days': test_config.get('duration_days', 14)
            }
            
            logger.info(f"A/B test {test_id} completed with winner {winner_id[:8]}...")
            return result
            
        except Exception as e:
            logger.error(f"Error running A/B test: {e}")
            raise


# Global service instance
product_service = ProductService()
