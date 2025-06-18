#!/usr/bin/env python3
"""
Basic functionality test for e-commerce personalization (no OpenAI required)
"""

import asyncio
import sys
import os
from typing import Dict, Any, List

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from admorph_backend.models.products import BaseProduct, PersonalizationRequest, ProductVariant
from admorph_backend.models.demographics import DemographicSegment
from admorph_backend.services.product_service import ProductService


async def test_basic_functionality():
    """Test basic functionality without OpenAI calls"""
    print("🧪 Testing E-commerce Personalization Basic Functionality")
    print("=" * 60)
    
    # Initialize service
    product_service = ProductService()
    
    # Test 1: Product Management
    print("\n📦 Testing Product Management...")
    try:
        # Get sample products
        products = await product_service.get_products()
        print(f"✅ Found {len(products)} sample products")
        
        # Get specific product
        if products:
            product = await product_service.get_product(products[0].product_id)
            print(f"✅ Retrieved product: {product.name}")
        
        # Create new product
        new_product_data = {
            "name": "Test Smart Watch",
            "base_price": 199.99,
            "category": "Wearables",
            "brand": "TestBrand",
            "features": ["Heart rate monitoring", "GPS", "Waterproof"],
            "specifications": {"battery_life": "5 days", "display": "OLED"},
            "base_images": ["test-image.jpg"],
            "inventory_count": 100
        }
        
        new_product = await product_service.create_product(new_product_data)
        print(f"✅ Created new product: {new_product.product_id}")
        
    except Exception as e:
        print(f"❌ Product Management test failed: {e}")
        return False
    
    # Test 2: Demographics
    print("\n👥 Testing Demographics...")
    try:
        demographics = await product_service.create_sample_demographics()
        print(f"✅ Created {len(demographics)} demographic segments")
        
        for demo in demographics:
            print(f"   - {demo.name}: {demo.age_range[0]}-{demo.age_range[1]} years")
            
    except Exception as e:
        print(f"❌ Demographics test failed: {e}")
        return False
    
    # Test 3: Data Models
    print("\n📊 Testing Data Models...")
    try:
        # Test BaseProduct model
        product_dict = products[0].to_dict()
        product_from_dict = BaseProduct.from_dict(product_dict)
        assert product_from_dict.product_id == products[0].product_id
        print("✅ BaseProduct serialization works")
        
        # Test DemographicSegment model
        demo_dict = demographics[0].to_dict()
        demo_from_dict = DemographicSegment.from_dict(demo_dict)
        assert demo_from_dict.segment_id == demographics[0].segment_id
        print("✅ DemographicSegment serialization works")
        
        # Test ProductVariant model
        variant = ProductVariant(
            variant_id="test-variant-001",
            product_id=products[0].product_id,
            demographic_segment=demographics[0],
            personalized_title="Test Personalized Title",
            personalized_description="Test description",
            highlighted_features=["Feature 1", "Feature 2"],
            price_positioning="value",
            image_prompts=["Test prompt"],
            generated_images=[],
            call_to_action="Buy Now"
        )
        
        variant_dict = variant.to_dict()
        variant_from_dict = ProductVariant.from_dict(variant_dict)
        assert variant_from_dict.variant_id == variant.variant_id
        print("✅ ProductVariant serialization works")
        
    except Exception as e:
        print(f"❌ Data Models test failed: {e}")
        return False
    
    # Test 4: Performance Tracking
    print("\n📈 Testing Performance Tracking...")
    try:
        # Test performance metrics
        metrics = await product_service.get_performance_metrics(products[0].product_id)
        print(f"✅ Performance metrics: {metrics.total_views} views, {metrics.conversion_rate:.1%} conversion")
        
        # Test variant performance update
        variant.update_performance(views=100, purchases=5)
        assert variant.view_count == 100
        assert variant.purchase_count == 5
        assert variant.conversion_rate == 0.05
        print("✅ Variant performance tracking works")
        
    except Exception as e:
        print(f"❌ Performance Tracking test failed: {e}")
        return False
    
    # Test 5: A/B Testing (Mock)
    print("\n🔬 Testing A/B Testing...")
    try:
        # Create mock variants
        variant1_id = "test-variant-001"
        variant2_id = "test-variant-002"
        
        test_config = {
            "duration_days": 14,
            "traffic_split": 50,
            "metric": "conversion_rate"
        }
        
        test_results = await product_service.run_ab_test([variant1_id, variant2_id], test_config)
        print(f"✅ A/B test completed: Winner is {test_results['winner'][:8]}...")
        print(f"   Improvement: {test_results['improvement']:.1f}%")
        
    except Exception as e:
        print(f"❌ A/B Testing test failed: {e}")
        return False
    
    # Test 6: API Data Structures
    print("\n🔌 Testing API Data Structures...")
    try:
        # Test PersonalizationRequest
        request = PersonalizationRequest(
            request_id="test-request-001",
            product_id=products[0].product_id,
            target_demographics=demographics[:2],
            personalization_goals=["increase_conversion", "highlight_features"],
            platform_context="shopify",
            brand_guidelines={"tone": "friendly", "style": "modern"}
        )
        
        request_dict = request.to_dict()
        assert request_dict["request_id"] == "test-request-001"
        assert len(request_dict["target_demographics"]) == 2
        print("✅ PersonalizationRequest structure works")
        
    except Exception as e:
        print(f"❌ API Data Structures test failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ALL BASIC FUNCTIONALITY TESTS PASSED!")
    print("✅ Product management works")
    print("✅ Demographics system works") 
    print("✅ Data models work")
    print("✅ Performance tracking works")
    print("✅ A/B testing framework works")
    print("✅ API structures work")
    print("\n🚀 E-commerce personalization system is ready!")
    print("💡 To test AI generation, add OpenAI API key and run full test suite")
    
    return True


async def main():
    """Run the basic functionality test"""
    success = await test_basic_functionality()
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
