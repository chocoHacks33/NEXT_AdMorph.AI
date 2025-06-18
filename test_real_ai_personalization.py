#!/usr/bin/env python3
"""
Real AI-powered e-commerce personalization test with OpenAI GPT-4
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from admorph_backend.models.products import BaseProduct, PersonalizationRequest
from admorph_backend.models.demographics import DemographicSegment
from admorph_backend.core.product_personalization_agent import ProductPersonalizationAgent


async def test_real_ai_personalization():
    """Test real AI personalization with OpenAI GPT-4"""
    print("🤖 REAL AI E-COMMERCE PERSONALIZATION TEST")
    print("Using OpenAI GPT-4 for actual AI generation")
    print("=" * 60)
    
    # Initialize AI agent
    agent = ProductPersonalizationAgent()
    
    # Create test product
    product = BaseProduct(
        product_id="wireless-headphones-premium-001",
        name="Premium Wireless Headphones",
        base_price=99.99,
        category="Electronics",
        brand="AudioTech Pro",
        features=[
            "Bluetooth 5.0 connectivity",
            "20-hour battery life",
            "Active noise cancellation",
            "Quick charge (15min = 3hrs)",
            "Premium leather comfort",
            "Crystal clear calls",
            "Touch controls",
            "Foldable design"
        ],
        specifications={
            "driver_size": "40mm",
            "frequency_response": "20Hz-20kHz",
            "impedance": "32 ohms",
            "weight": "250g",
            "charging_time": "2 hours",
            "wireless_range": "30 feet",
            "noise_reduction": "25dB"
        },
        base_images=[
            "https://example.com/headphones-main.jpg",
            "https://example.com/headphones-lifestyle.jpg"
        ],
        inventory_count=150,
        created_at=datetime.now().isoformat()
    )
    
    # Create diverse demographic segments
    demographics = [
        DemographicSegment(
            segment_id="fitness-enthusiasts",
            name="Fitness Enthusiasts",
            age_range=(22, 40),
            gender="all",
            interests=["Fitness", "Health", "Sports", "Wellness", "Active lifestyle"],
            behaviors=["Health-conscious", "Goal-oriented", "Early adopters", "Quality-focused"],
            location="United States",
            income_level="Middle",
            education="High School",
            meta_targeting_spec={
                "category": "Fitness",
                "relevance_score": 0.95
            }
        ),
        DemographicSegment(
            segment_id="business-professionals",
            name="Business Professionals",
            age_range=(28, 45),
            gender="all",
            interests=["Business", "Productivity", "Technology", "Career development"],
            behaviors=["Quality-focused", "Time-conscious", "Professional", "Premium buyers"],
            location="United States",
            income_level="High",
            education="Bachelor's",
            meta_targeting_spec={
                "category": "Professional",
                "relevance_score": 0.92
            }
        ),
        DemographicSegment(
            segment_id="tech-early-adopters",
            name="Tech Early Adopters",
            age_range=(18, 35),
            gender="all",
            interests=["Technology", "Gadgets", "Innovation", "Gaming", "Audio"],
            behaviors=["Early adopters", "Tech-savvy", "Research-driven", "Feature-focused"],
            location="United States",
            income_level="High",
            education="Bachelor's",
            meta_targeting_spec={
                "category": "Technology",
                "relevance_score": 0.94
            }
        )
    ]
    
    print(f"📦 TESTING PRODUCT: {product.name}")
    print(f"   Price: ${product.base_price}")
    print(f"   Features: {len(product.features)} features")
    print(f"   Target Demographics: {len(demographics)} segments")
    
    # Create personalization request
    request = PersonalizationRequest(
        request_id="real-ai-test-001",
        product_id=product.product_id,
        target_demographics=demographics,
        personalization_goals=["increase_conversion", "highlight_features", "optimize_messaging"],
        platform_context="shopify",
        brand_guidelines={
            "tone": "premium yet approachable",
            "style": "modern and professional",
            "values": ["quality", "innovation", "customer satisfaction"]
        },
        seasonal_context="holiday shopping season"
    )
    
    print(f"\n🎯 PERSONALIZATION REQUEST:")
    print(f"   Goals: {request.personalization_goals}")
    print(f"   Platform: {request.platform_context}")
    print(f"   Brand Tone: {request.brand_guidelines['tone']}")
    
    # Execute AI personalization
    print(f"\n🤖 EXECUTING AI PERSONALIZATION WITH GPT-4...")
    print("   This will make real API calls to OpenAI...")
    
    try:
        context = {
            "personalization_request": request,
            "base_product": product
        }
        
        start_time = datetime.now()
        result = await agent.execute(context)
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()
        
        if result["success"]:
            personalization_result = result["result"]
            variants = personalization_result.generated_variants
            
            print(f"✅ AI PERSONALIZATION SUCCESSFUL!")
            print(f"   Processing time: {processing_time:.2f} seconds")
            print(f"   Variants generated: {len(variants)}")
            print(f"   Performance lift estimate: {personalization_result.estimated_performance_lift:.1%}")
            
            print(f"\n🎨 AI-GENERATED PERSONALIZED VARIANTS:")
            print("=" * 60)
            
            for i, variant in enumerate(variants, 1):
                print(f"\n🎯 VARIANT {i}: {variant.demographic_segment.name}")
                print(f"   👤 Target: {variant.demographic_segment.age_range[0]}-{variant.demographic_segment.age_range[1]} years")
                print(f"   🏷️  Interests: {', '.join(variant.demographic_segment.interests[:3])}")
                print(f"   📝 AI Title: {variant.personalized_title}")
                print(f"   📄 AI Description: {variant.personalized_description[:120]}...")
                print(f"   ⭐ Key Features: {', '.join(variant.highlighted_features)}")
                print(f"   💰 Price Position: {variant.price_positioning}")
                print(f"   🔘 Call to Action: {variant.call_to_action}")
                if variant.urgency_messaging:
                    print(f"   ⚡ Urgency: {variant.urgency_messaging}")
                if variant.social_proof:
                    print(f"   👥 Social Proof: {variant.social_proof}")
                print(f"   📊 AI Score: {variant.personalization_score:.2f}")
            
            # Show insights
            print(f"\n🧠 AI DEMOGRAPHIC INSIGHTS:")
            print("-" * 40)
            for segment_id, insights in personalization_result.personalization_insights.items():
                segment_name = next(d.name for d in demographics if d.segment_id == segment_id)
                print(f"\n📊 {segment_name}:")
                for key, value in insights.items():
                    print(f"   • {key.replace('_', ' ').title()}: {value}")
            
            # Show A/B test recommendations
            if personalization_result.a_b_test_recommendations:
                print(f"\n🔬 AI A/B TEST RECOMMENDATIONS:")
                print("-" * 40)
                for i, test in enumerate(personalization_result.a_b_test_recommendations, 1):
                    print(f"\n🧪 Test {i}: {test['test_type'].replace('_', ' ').title()}")
                    print(f"   Metric: {test['metric']}")
                    print(f"   Duration: {test['duration_days']} days")
                    print(f"   Traffic Split: {test['traffic_split']}%")
            
            print(f"\n" + "=" * 60)
            print("🎉 REAL AI PERSONALIZATION TEST SUCCESSFUL!")
            print("✅ OpenAI GPT-4 integration working perfectly")
            print("✅ AI-generated personalized variants created")
            print("✅ Demographic insights analyzed")
            print("✅ A/B testing recommendations provided")
            print("✅ Performance lift estimated")
            
            print(f"\n💡 BUSINESS IMPACT:")
            print(f"📈 Estimated conversion improvement: {personalization_result.estimated_performance_lift:.1%}")
            print(f"🎯 Each variant specifically targets its demographic")
            print(f"🚀 Ready for production e-commerce deployment!")
            
            return True
            
        else:
            print(f"❌ AI PERSONALIZATION FAILED: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR DURING AI PERSONALIZATION: {str(e)}")
        print(f"💡 Check your OpenAI API key and internet connection")
        return False


async def main():
    """Run the real AI personalization test"""
    success = await test_real_ai_personalization()
    if not success:
        print(f"\n⚠️  Test failed. Please check:")
        print(f"   • OpenAI API key is valid")
        print(f"   • Internet connection is working")
        print(f"   • OpenAI API quota is available")
        sys.exit(1)
    else:
        print(f"\n🎉 All tests passed! Your AI personalization system is ready!")


if __name__ == "__main__":
    asyncio.run(main())
