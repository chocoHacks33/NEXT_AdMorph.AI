"""
Test OpenAI Integration with Real API Key
"""

import asyncio
import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from admorph_core import AdMorphVoiceAgent, DemographicAnalysisAgent, AdVariantGenerationAgent, BusinessProfile, DemographicSegment

async def test_voice_agent_real():
    """Test voice agent with real OpenAI API"""
    
    print("🎤 Testing Voice Agent with Real OpenAI API...")
    print("=" * 50)
    
    agent = AdMorphVoiceAgent()
    
    # Test business consultation
    test_input = {
        "current_stage": "greeting",
        "user_response": "Hi, I run a fitness coaching business called FitLife Pro. We help busy professionals get in shape with personalized workout plans and nutrition guidance."
    }
    
    try:
        result = await agent.execute(test_input)
        
        print("✅ Voice Agent Response:")
        print(f"   AI Response: {result.get('ai_response', 'No response')[:200]}...")
        print(f"   Next Stage: {result.get('next_stage', 'Unknown')}")
        print(f"   Extracted Data: {result.get('extracted_data', {})}")
        
        return True
        
    except Exception as e:
        print(f"❌ Voice Agent Test Failed: {e}")
        return False

async def test_demographic_agent_real():
    """Test demographic agent with real OpenAI API"""
    
    print("\n🎯 Testing Demographic Agent with Real OpenAI API...")
    print("=" * 50)
    
    agent = DemographicAnalysisAgent()
    
    # Create realistic business profile
    business_profile = BusinessProfile(
        business_id="test_fitness_123",
        business_name="FitLife Pro",
        industry="Health & Fitness",
        target_engagement="sales",
        monthly_budget=8000.0,
        target_audience={
            "description": "Busy professionals aged 25-45 who want to get in shape but lack time",
            "pain_points": ["lack of time", "don't know where to start", "need accountability"]
        },
        brand_themes={
            "allowed": ["motivation", "results", "convenience", "professional"],
            "disallowed": ["intimidating", "extreme", "unrealistic"]
        },
        original_ad_assets=[],
        voice_preferences={"tone": "motivational", "style": "professional"},
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    try:
        result = await agent.execute(business_profile)
        
        print("✅ Demographic Analysis Results:")
        print(f"   Total Segments: {result.get('total_segments', 0)}")
        print(f"   Estimated Reach: {result.get('estimated_reach', 0):,}")
        
        segments = result.get('demographic_segments', [])
        for i, segment in enumerate(segments[:3]):  # Show first 3
            print(f"   Segment {i+1}: {segment.name}")
            print(f"      Age: {segment.age_range[0]}-{segment.age_range[1]}")
            print(f"      Interests: {', '.join(segment.interests[:3])}")
        
        return True, segments
        
    except Exception as e:
        print(f"❌ Demographic Agent Test Failed: {e}")
        return False, []

async def test_variant_generator_real():
    """Test ad variant generation with real OpenAI API"""
    
    print("\n🎨 Testing Ad Variant Generator with Real OpenAI API...")
    print("=" * 50)
    
    agent = AdVariantGenerationAgent()
    
    # Create test business profile and segment
    business_profile = BusinessProfile(
        business_id="test_fitness_123",
        business_name="FitLife Pro",
        industry="Health & Fitness",
        target_engagement="sales",
        monthly_budget=8000.0,
        target_audience={
            "description": "Busy professionals who want to get in shape"
        },
        brand_themes={
            "allowed": ["motivation", "results", "convenience"],
            "disallowed": ["intimidating", "extreme"]
        },
        original_ad_assets=[],
        voice_preferences={"tone": "motivational"},
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )
    
    test_segment = DemographicSegment(
        segment_id="busy_professionals",
        name="Busy Professionals",
        age_range=(28, 42),
        gender="all",
        interests=["Fitness", "Health", "Career", "Productivity"],
        behaviors=["Busy lifestyle", "Health conscious", "Goal oriented"],
        location="United States",
        income_level="High",
        education="Bachelor's",
        meta_targeting_spec={}
    )
    
    try:
        result = await agent.execute(business_profile, [test_segment])
        
        print("✅ Ad Variant Generation Results:")
        print(f"   Total Variants: {result.get('total_variants', 0)}")
        
        variants = result.get('variants', [])
        for i, variant in enumerate(variants[:3]):  # Show first 3
            print(f"\n   Variant {i+1}:")
            print(f"      Headline: {variant.headline}")
            print(f"      Body: {variant.body[:100]}...")
            print(f"      CTA: {variant.cta}")
            print(f"      Target: {variant.demographic_segment.name}")
            print(f"      Scores: Aesthetic={variant.aesthetic_score:.2f}, Ogilvy={variant.ogilvy_score:.2f}")
        
        return True, variants
        
    except Exception as e:
        print(f"❌ Variant Generator Test Failed: {e}")
        return False, []

async def test_complete_workflow():
    """Test complete workflow with real OpenAI API"""
    
    print("\n🚀 Testing Complete AdMorph Workflow...")
    print("=" * 60)
    
    # Test each component
    voice_success = await test_voice_agent_real()
    demo_success, segments = await test_demographic_agent_real()
    variant_success, variants = await test_variant_generator_real()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 REAL API TEST SUMMARY")
    print("=" * 60)
    
    tests = [
        ("Voice Agent", voice_success),
        ("Demographic Agent", demo_success),
        ("Variant Generator", variant_success)
    ]
    
    passed = sum(1 for _, success in tests if success)
    total = len(tests)
    
    for test_name, success in tests:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed with real OpenAI API")
    
    if passed == total:
        print("🎉 All OpenAI integrations working perfectly!")
        print("\n🚀 Ready for production use with:")
        print(f"   • {len(segments)} demographic segments generated")
        print(f"   • {len(variants)} ad variants created")
        print("   • Real AI-powered business consultation")
        print("   • Intelligent demographic analysis")
        print("   • Creative ad generation")
    else:
        print("⚠️ Some tests failed. Check API key and network connection.")
    
    return passed == total

if __name__ == "__main__":
    print("🧪 AdMorph.AI Real OpenAI API Integration Test")
    print("=" * 60)
    
    # Check if API key is configured
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        print("Make sure you have a .env file with your API key")
        sys.exit(1)
    
    print(f"✅ OpenAI API Key configured (ending in ...{api_key[-10:]})")
    
    try:
        success = asyncio.run(test_complete_workflow())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test runner failed: {e}")
        sys.exit(1)
