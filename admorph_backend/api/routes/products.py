"""
Product personalization API routes
"""

import uuid
import asyncio
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

from ...models.products import BaseProduct, PersonalizationRequest, ProductVariant
from ...models.demographics import DemographicSegment
from ...services.product_service import ProductService


# Initialize router and service
router = APIRouter(prefix="/api/products", tags=["products"])
product_service = ProductService()


# Pydantic models for API requests/responses
class ProductCreateRequest(BaseModel):
    name: str
    base_price: float
    category: str
    brand: str
    features: List[str]
    specifications: Dict[str, Any]
    base_images: List[str]
    inventory_count: int


class PersonalizationRequestModel(BaseModel):
    product_id: str
    target_demographics: List[Dict[str, Any]]
    personalization_goals: List[str]
    platform_context: str
    brand_guidelines: Optional[Dict[str, Any]] = None
    competitor_analysis: Optional[List[str]] = None
    seasonal_context: Optional[str] = None


class PerformanceUpdateRequest(BaseModel):
    views: int = 0
    purchases: int = 0


class ABTestRequest(BaseModel):
    variant_ids: List[str]
    test_config: Dict[str, Any]


# API Routes
@router.get("/", response_model=List[Dict[str, Any]])
async def get_products():
    """Get all products"""
    try:
        products = await product_service.get_products()
        return [product.to_dict() for product in products]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{product_id}", response_model=Dict[str, Any])
async def get_product(product_id: str):
    """Get specific product by ID"""
    try:
        product = await product_service.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=Dict[str, Any])
async def create_product(request: ProductCreateRequest):
    """Create new product"""
    try:
        product_data = request.dict()
        product = await product_service.create_product(product_data)
        return product.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{product_id}/personalize", response_model=Dict[str, Any])
async def personalize_product(
    product_id: str, 
    request: PersonalizationRequestModel,
    background_tasks: BackgroundTasks
):
    """Generate personalized product variants"""
    try:
        # Validate product exists
        product = await product_service.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Create personalization request
        job_id = str(uuid.uuid4())
        
        # Convert demographics from dict to DemographicSegment objects
        demographics = []
        for demo_data in request.target_demographics:
            demographic = DemographicSegment.from_dict(demo_data)
            demographics.append(demographic)
        
        personalization_request = PersonalizationRequest(
            request_id=job_id,
            product_id=product_id,
            target_demographics=demographics,
            personalization_goals=request.personalization_goals,
            platform_context=request.platform_context,
            brand_guidelines=request.brand_guidelines,
            competitor_analysis=request.competitor_analysis,
            seasonal_context=request.seasonal_context
        )
        
        # Start background personalization job
        background_tasks.add_task(
            product_service.personalize_product_async,
            job_id,
            personalization_request
        )
        
        return {
            "job_id": job_id,
            "status": "processing",
            "message": "Personalization job started",
            "estimated_completion": "2-3 minutes"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs/{job_id}", response_model=Dict[str, Any])
async def get_personalization_job(job_id: str):
    """Get personalization job status and results"""
    try:
        result = await product_service.get_personalization_result(job_id)
        if not result:
            raise HTTPException(status_code=404, detail="Job not found")
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{product_id}/variants", response_model=List[Dict[str, Any]])
async def get_product_variants(product_id: str):
    """Get all variants for a product"""
    try:
        variants = await product_service.get_product_variants(product_id)
        return [variant.to_dict() for variant in variants]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/variants/{variant_id}", response_model=Dict[str, Any])
async def get_variant(variant_id: str):
    """Get specific variant by ID"""
    try:
        variant = await product_service.get_variant(variant_id)
        if not variant:
            raise HTTPException(status_code=404, detail="Variant not found")
        return variant.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/variants/{variant_id}/performance", response_model=Dict[str, Any])
async def update_variant_performance(variant_id: str, request: PerformanceUpdateRequest):
    """Update variant performance metrics"""
    try:
        variant = await product_service.update_variant_performance(
            variant_id, request.views, request.purchases
        )
        if not variant:
            raise HTTPException(status_code=404, detail="Variant not found")
        return variant.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{product_id}/performance", response_model=Dict[str, Any])
async def get_product_performance(product_id: str, time_period: str = "7d"):
    """Get product performance metrics"""
    try:
        metrics = await product_service.get_performance_metrics(product_id, time_period)
        if not metrics:
            raise HTTPException(status_code=404, detail="Performance data not found")
        return metrics.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ab-test", response_model=Dict[str, Any])
async def run_ab_test(request: ABTestRequest):
    """Run A/B test between product variants"""
    try:
        # Validate variants exist
        for variant_id in request.variant_ids:
            variant = await product_service.get_variant(variant_id)
            if not variant:
                raise HTTPException(status_code=404, detail=f"Variant {variant_id} not found")
        
        # Run A/B test
        test_results = await product_service.run_ab_test(
            request.variant_ids, request.test_config
        )
        
        return test_results
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/demo/demographics", response_model=List[Dict[str, Any]])
async def get_sample_demographics():
    """Get sample demographic segments for testing"""
    try:
        demographics = await product_service.create_sample_demographics()
        return [demo.to_dict() for demo in demographics]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{product_id}/quick-personalize", response_model=Dict[str, Any])
async def quick_personalize_demo(product_id: str):
    """Quick personalization demo with sample demographics"""
    try:
        # Get product
        product = await product_service.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Get sample demographics
        demographics = await product_service.create_sample_demographics()
        
        # Create personalization request
        job_id = str(uuid.uuid4())
        personalization_request = PersonalizationRequest(
            request_id=job_id,
            product_id=product_id,
            target_demographics=demographics,
            personalization_goals=["increase_conversion", "highlight_features"],
            platform_context="shopify",
            brand_guidelines={"tone": "friendly", "style": "modern"},
            seasonal_context="summer"
        )
        
        # Run personalization synchronously for demo
        await product_service.personalize_product_async(job_id, personalization_request)
        
        # Get results
        result = await product_service.get_personalization_result(job_id)
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
