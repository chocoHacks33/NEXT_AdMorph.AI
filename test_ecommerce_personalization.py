#!/usr/bin/env python3
"""
Comprehensive test suite for e-commerce product personalization
"""

import asyncio
import json
import time
import sys
import os
from typing import Dict, Any, List

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from admorph_backend.models.products import BaseProduct, PersonalizationRequest
from admorph_backend.models.demographics import DemographicSegment
from admorph_backend.services.product_service import ProductService
from admorph_backend.core.product_personalization_agent import ProductPersonalizationAgent


class EcommercePersonalizationTester:
    """Comprehensive tester for e-commerce personalization functionality"""
    
    def __init__(self):
        self.product_service = ProductService()
        self.personalization_agent = ProductPersonalizationAgent()
        self.test_results = []
    
    async def run_all_tests(self):
        """Run comprehensive test suite"""
        print("🧪 Starting E-commerce Personalization Test Suite")
        print("=" * 60)
        
        # Test 1: Basic Product Management
        await self.test_product_management()
        
        # Test 2: Demographic Segments
        await self.test_demographic_segments()
        
        # Test 3: Product Personalization
        await self.test_product_personalization()
        
        # Test 4: Performance Tracking
        await self.test_performance_tracking()
        
        # Test 5: A/B Testing
        await self.test_ab_testing()
        
        # Test 6: Real-world Scenarios
        await self.test_real_world_scenarios()
        
        # Print summary
        self.print_test_summary()
    
    async def test_product_management(self):
        """Test basic product management functionality"""
        print("\n📦 Testing Product Management...")
        
        try:
            # Test getting products
            products = await self.product_service.get_products()
            assert len(products) > 0, "Should have sample products"
            print(f"✅ Found {len(products)} sample products")
            
            # Test getting specific product
            product_id = products[0].product_id
            product = await self.product_service.get_product(product_id)
            assert product is not None, "Should retrieve specific product"
            print(f"✅ Retrieved product: {product.name}")
            
            # Test creating new product
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
            
            new_product = await self.product_service.create_product(new_product_data)
            assert new_product.name == "Test Smart Watch", "Should create product correctly"
            print(f"✅ Created new product: {new_product.product_id}")
            
            self.test_results.append({"test": "Product Management", "status": "PASSED"})
            
        except Exception as e:
            print(f"❌ Product Management test failed: {e}")
            self.test_results.append({"test": "Product Management", "status": "FAILED", "error": str(e)})
    
    async def test_demographic_segments(self):
        """Test demographic segment creation and management"""
        print("\n👥 Testing Demographic Segments...")
        
        try:
            # Get sample demographics
            demographics = await self.product_service.create_sample_demographics()
            assert len(demographics) >= 3, "Should have multiple demographic segments"
            print(f"✅ Created {len(demographics)} demographic segments")
            
            # Test demographic properties
            for demo in demographics:
                assert demo.segment_id, "Should have segment ID"
                assert demo.name, "Should have name"
                assert len(demo.interests) > 0, "Should have interests"
                assert len(demo.behaviors) > 0, "Should have behaviors"
                print(f"✅ Validated demographic: {demo.name}")
            
            self.test_results.append({"test": "Demographic Segments", "status": "PASSED"})
            
        except Exception as e:
            print(f"❌ Demographic Segments test failed: {e}")
            self.test_results.append({"test": "Demographic Segments", "status": "FAILED", "error": str(e)})
    
    async def test_product_personalization(self):
        """Test core product personalization functionality"""
        print("\n🎯 Testing Product Personalization...")
        
        try:
            # Get test product and demographics
            products = await self.product_service.get_products()
            product = products[0]  # Use first sample product
            demographics = await self.product_service.create_sample_demographics()
            
            # Create personalization request
            request = PersonalizationRequest(
                request_id="test-personalization-001",
                product_id=product.product_id,
                target_demographics=demographics[:2],  # Use first 2 demographics
                personalization_goals=["increase_conversion", "highlight_features"],
                platform_context="shopify",
                brand_guidelines={"tone": "friendly", "style": "modern"}
            )
            
            # Test personalization agent directly
            context = {
                "personalization_request": request,
                "base_product": product
            }
            
            result = await self.personalization_agent.execute(context)
            assert result["success"], "Personalization should succeed"
            
            personalization_result = result["result"]
            assert len(personalization_result.generated_variants) == 2, "Should generate 2 variants"
            print(f"✅ Generated {len(personalization_result.generated_variants)} personalized variants")
            
            # Test variant properties
            for variant in personalization_result.generated_variants:
                assert variant.personalized_title, "Should have personalized title"
                assert variant.personalized_description, "Should have personalized description"
                assert len(variant.highlighted_features) > 0, "Should have highlighted features"
                assert variant.call_to_action, "Should have call to action"
                print(f"✅ Validated variant for {variant.demographic_segment.name}")
                print(f"   Title: {variant.personalized_title[:50]}...")
            
            self.test_results.append({"test": "Product Personalization", "status": "PASSED"})
            
        except Exception as e:
            print(f"❌ Product Personalization test failed: {e}")
            self.test_results.append({"test": "Product Personalization", "status": "FAILED", "error": str(e)})
    
    async def test_performance_tracking(self):
        """Test performance tracking functionality"""
        print("\n📊 Testing Performance Tracking...")
        
        try:
            # Get test product
            products = await self.product_service.get_products()
            product_id = products[0].product_id
            
            # Test performance metrics
            metrics = await self.product_service.get_performance_metrics(product_id)
            assert metrics is not None, "Should return performance metrics"
            assert metrics.total_views > 0, "Should have view data"
            assert metrics.conversion_rate >= 0, "Should have conversion rate"
            print(f"✅ Retrieved performance metrics: {metrics.total_views} views, {metrics.conversion_rate:.1%} conversion")
            
            # Test variant performance update
            # First create a variant by running personalization
            demographics = await self.product_service.create_sample_demographics()
            request = PersonalizationRequest(
                request_id="test-performance-001",
                product_id=product_id,
                target_demographics=[demographics[0]],
                personalization_goals=["increase_conversion"],
                platform_context="amazon"
            )
            
            await self.product_service.personalize_product_async("test-job-001", request)
            variants = await self.product_service.get_product_variants(product_id)
            
            if variants:
                variant = variants[0]
                updated_variant = await self.product_service.update_variant_performance(
                    variant.variant_id, views=100, purchases=5
                )
                assert updated_variant.view_count == 100, "Should update view count"
                assert updated_variant.purchase_count == 5, "Should update purchase count"
                assert updated_variant.conversion_rate == 0.05, "Should calculate conversion rate"
                print(f"✅ Updated variant performance: {updated_variant.conversion_rate:.1%} conversion")
            
            self.test_results.append({"test": "Performance Tracking", "status": "PASSED"})
            
        except Exception as e:
            print(f"❌ Performance Tracking test failed: {e}")
            self.test_results.append({"test": "Performance Tracking", "status": "FAILED", "error": str(e)})
    
    async def test_ab_testing(self):
        """Test A/B testing functionality"""
        print("\n🔬 Testing A/B Testing...")
        
        try:
            # Create test variants
            products = await self.product_service.get_products()
            product_id = products[0].product_id
            demographics = await self.product_service.create_sample_demographics()
            
            request = PersonalizationRequest(
                request_id="test-ab-001",
                product_id=product_id,
                target_demographics=demographics[:2],
                personalization_goals=["increase_conversion"],
                platform_context="shopify"
            )
            
            await self.product_service.personalize_product_async("test-ab-job", request)
            variants = await self.product_service.get_product_variants(product_id)
            
            if len(variants) >= 2:
                # Run A/B test
                test_config = {
                    "duration_days": 14,
                    "traffic_split": 50,
                    "metric": "conversion_rate"
                }
                
                test_results = await self.product_service.run_ab_test(
                    [variants[0].variant_id, variants[1].variant_id],
                    test_config
                )
                
                assert test_results["test_id"], "Should have test ID"
                assert "winner" in test_results, "Should determine winner"
                assert "statistical_significance" in test_results, "Should calculate significance"
                print(f"✅ A/B test completed: Winner is {test_results['winner'][:8]}...")
                print(f"   Improvement: {test_results['improvement']:.1f}%")
            
            self.test_results.append({"test": "A/B Testing", "status": "PASSED"})
            
        except Exception as e:
            print(f"❌ A/B Testing test failed: {e}")
            self.test_results.append({"test": "A/B Testing", "status": "FAILED", "error": str(e)})
    
    async def test_real_world_scenarios(self):
        """Test real-world e-commerce scenarios"""
        print("\n🌍 Testing Real-world Scenarios...")
        
        try:
            # Scenario 1: Fitness tracker for different demographics
            fitness_tracker = None
            products = await self.product_service.get_products()
            for product in products:
                if "fitness" in product.name.lower() or "tracker" in product.name.lower():
                    fitness_tracker = product
                    break
            
            if fitness_tracker:
                print(f"📱 Testing with: {fitness_tracker.name}")
                
                # Create diverse demographics
                demographics = [
                    DemographicSegment(
                        segment_id="athletes",
                        name="Professional Athletes",
                        age_range=(20, 35),
                        gender="all",
                        interests=["Sports", "Performance", "Training"],
                        behaviors=["Goal-oriented", "Data-driven", "Competitive"],
                        location="United States",
                        income_level="High",
                        education="High School"
                    ),
                    DemographicSegment(
                        segment_id="health-conscious",
                        name="Health-conscious Professionals",
                        age_range=(30, 50),
                        gender="all",
                        interests=["Health", "Wellness", "Work-life balance"],
                        behaviors=["Health-focused", "Busy lifestyle", "Quality-oriented"],
                        location="United States",
                        income_level="High",
                        education="Bachelor's"
                    )
                ]
                
                # Test personalization for each demographic
                for demo in demographics:
                    request = PersonalizationRequest(
                        request_id=f"scenario-{demo.segment_id}",
                        product_id=fitness_tracker.product_id,
                        target_demographics=[demo],
                        personalization_goals=["increase_conversion", "highlight_features"],
                        platform_context="amazon",
                        seasonal_context="summer"
                    )
                    
                    context = {
                        "personalization_request": request,
                        "base_product": fitness_tracker
                    }
                    
                    result = await self.personalization_agent.execute(context)
                    assert result["success"], f"Should personalize for {demo.name}"
                    
                    variant = result["result"].generated_variants[0]
                    print(f"✅ {demo.name}:")
                    print(f"   Title: {variant.personalized_title}")
                    print(f"   Key Features: {', '.join(variant.highlighted_features[:2])}")
                    print(f"   Price Position: {variant.price_positioning}")
            
            self.test_results.append({"test": "Real-world Scenarios", "status": "PASSED"})
            
        except Exception as e:
            print(f"❌ Real-world Scenarios test failed: {e}")
            self.test_results.append({"test": "Real-world Scenarios", "status": "FAILED", "error": str(e)})
    
    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 60)
        print("🎯 E-COMMERCE PERSONALIZATION TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["status"] == "PASSED")
        failed = sum(1 for result in self.test_results if result["status"] == "FAILED")
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {(passed/len(self.test_results)*100):.1f}%")
        
        print("\nDetailed Results:")
        for result in self.test_results:
            status_icon = "✅" if result["status"] == "PASSED" else "❌"
            print(f"{status_icon} {result['test']}: {result['status']}")
            if result["status"] == "FAILED":
                print(f"   Error: {result.get('error', 'Unknown error')}")
        
        if failed == 0:
            print("\n🎉 ALL TESTS PASSED! E-commerce personalization is working perfectly!")
        else:
            print(f"\n⚠️  {failed} test(s) failed. Please review the errors above.")


async def main():
    """Run the comprehensive test suite"""
    tester = EcommercePersonalizationTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
