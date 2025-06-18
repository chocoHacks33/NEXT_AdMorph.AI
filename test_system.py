"""
AdMorph.AI System Tests
Basic validation and testing suite
"""

import asyncio
import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Any

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    
    print("🧪 Testing imports...")
    
    try:
        from admorph_core import (
            BusinessProfile, AdVariantMorph, DemographicSegment,
            AdMorphVoiceAgent, DemographicAnalysisAgent, AdVariantGenerationAgent
        )
        print("✅ admorph_core imports successful")
    except Exception as e:
        print(f"❌ admorph_core import failed: {e}")
        return False
    
    try:
        from swipe_interface import TinderStyleAdReviewer
        print("✅ swipe_interface imports successful")
    except Exception as e:
        print(f"❌ swipe_interface import failed: {e}")
        return False
    
    try:
        from meta_api_integration import MetaMarketingAPIClient, AdMorphCampaignManager
        print("✅ meta_api_integration imports successful")
    except Exception as e:
        print(f"❌ meta_api_integration import failed: {e}")
        return False
    
    try:
        from agentic_evolution import EvolutionOrchestrator, EvolutionMonitor
        print("✅ agentic_evolution imports successful")
    except Exception as e:
        print(f"❌ agentic_evolution import failed: {e}")
        return False
    
    try:
        from coee import AIAdvertisingAgency, AdMorphIntegratedOrchestrator
        print("✅ coee imports successful")
    except Exception as e:
        print(f"❌ coee import failed: {e}")
        return False
    
    return True

def test_environment():
    """Test environment configuration"""
    
    print("\n🔧 Testing environment configuration...")
    
    # Check for .env file
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("⚠️ .env file not found (using .env.example)")
    
    # Check API keys
    openai_key = os.getenv("OPENAI_API_KEY")
    meta_token = os.getenv("META_ACCESS_TOKEN")
    
    if openai_key:
        print("✅ OpenAI API key configured")
    else:
        print("⚠️ OpenAI API key not configured")
    
    if meta_token:
        print("✅ Meta API token configured")
    else:
        print("⚠️ Meta API token not configured")
    
    return True

async def test_voice_agent():
    """Test voice agent functionality"""
    
    print("\n🎤 Testing Voice Agent...")
    
    try:
        from admorph_core import AdMorphVoiceAgent
        
        agent = AdMorphVoiceAgent()
        
        # Test start onboarding
        result = await agent.execute({"stage": "start"})
        
        if "message" in result and "stage" in result:
            print("✅ Voice agent onboarding start successful")
            return True
        else:
            print("❌ Voice agent returned unexpected format")
            return False
            
    except Exception as e:
        print(f"❌ Voice agent test failed: {e}")
        return False

async def test_demographic_agent():
    """Test demographic analysis agent"""
    
    print("\n🎯 Testing Demographic Agent...")
    
    try:
        from admorph_core import DemographicAnalysisAgent, BusinessProfile
        
        agent = DemographicAnalysisAgent()
        
        # Create test business profile
        test_profile = BusinessProfile(
            business_id="test_123",
            business_name="Test Business",
            industry="Technology",
            target_engagement="sales",
            monthly_budget=5000.0,
            target_audience={"description": "Tech professionals"},
            brand_themes={"allowed": ["innovation"], "disallowed": []},
            original_ad_assets=[],
            voice_preferences={},
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        result = await agent.execute(test_profile)
        
        if "demographic_segments" in result and len(result["demographic_segments"]) > 0:
            print(f"✅ Demographic agent created {len(result['demographic_segments'])} segments")
            return True
        else:
            print("❌ Demographic agent failed to create segments")
            return False
            
    except Exception as e:
        print(f"❌ Demographic agent test failed: {e}")
        return False

async def test_variant_generator():
    """Test ad variant generation"""
    
    print("\n🎨 Testing Variant Generator...")
    
    try:
        from admorph_core import AdVariantGenerationAgent, BusinessProfile, DemographicSegment
        
        agent = AdVariantGenerationAgent()
        
        # Create test data
        test_profile = BusinessProfile(
            business_id="test_123",
            business_name="Test Business",
            industry="Technology",
            target_engagement="sales",
            monthly_budget=5000.0,
            target_audience={"description": "Tech professionals"},
            brand_themes={"allowed": ["innovation"], "disallowed": []},
            original_ad_assets=[],
            voice_preferences={},
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        test_segment = DemographicSegment(
            segment_id="test_segment",
            name="Test Segment",
            age_range=(25, 40),
            gender="all",
            interests=["Technology"],
            behaviors=["Early adopters"],
            location="United States",
            income_level="Middle",
            education="Bachelor's",
            meta_targeting_spec={}
        )
        
        result = await agent.execute(test_profile, [test_segment])
        
        if "variants" in result and len(result["variants"]) > 0:
            print(f"✅ Variant generator created {len(result['variants'])} variants")
            return True
        else:
            print("❌ Variant generator failed to create variants")
            return False
            
    except Exception as e:
        print(f"❌ Variant generator test failed: {e}")
        return False

async def test_evolution_system():
    """Test agentic evolution system"""
    
    print("\n🧬 Testing Evolution System...")
    
    try:
        from agentic_evolution import SyntheticDataGenerator, TrendAnalysisAgent
        from admorph_core import BusinessProfile
        
        # Test synthetic data generation
        data_gen = SyntheticDataGenerator()
        trends = data_gen.generate_trend_data()
        
        if len(trends) > 0:
            print(f"✅ Generated {len(trends)} trend data points")
        else:
            print("❌ Failed to generate trend data")
            return False
        
        # Test trend analysis
        trend_agent = TrendAnalysisAgent()
        test_profile = BusinessProfile(
            business_id="test_123",
            business_name="Test Business",
            industry="Technology",
            target_engagement="sales",
            monthly_budget=5000.0,
            target_audience={"description": "Tech professionals"},
            brand_themes={"allowed": ["innovation"], "disallowed": []},
            original_ad_assets=[],
            voice_preferences={},
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        
        result = await trend_agent.execute(test_profile, trends)
        
        if "relevant_trends" in result:
            print(f"✅ Trend analysis identified {len(result['relevant_trends'])} relevant trends")
            return True
        else:
            print("❌ Trend analysis failed")
            return False
            
    except Exception as e:
        print(f"❌ Evolution system test failed: {e}")
        return False

def test_data_models():
    """Test data model creation"""
    
    print("\n📊 Testing Data Models...")
    
    try:
        from admorph_core import BusinessProfile, AdVariantMorph, DemographicSegment
        
        # Test BusinessProfile
        profile = BusinessProfile(
            business_id="test_123",
            business_name="Test Business",
            industry="Technology",
            target_engagement="sales",
            monthly_budget=5000.0,
            target_audience={"description": "Tech professionals"},
            brand_themes={"allowed": ["innovation"], "disallowed": []},
            original_ad_assets=[],
            voice_preferences={},
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )
        print("✅ BusinessProfile creation successful")
        
        # Test DemographicSegment
        segment = DemographicSegment(
            segment_id="test_segment",
            name="Test Segment",
            age_range=(25, 40),
            gender="all",
            interests=["Technology"],
            behaviors=["Early adopters"],
            location="United States",
            income_level="Middle",
            education="Bachelor's",
            meta_targeting_spec={}
        )
        print("✅ DemographicSegment creation successful")
        
        # Test AdVariantMorph
        variant = AdVariantMorph(
            variant_id="test_variant",
            headline="Test Headline",
            body="Test body copy",
            cta="Test CTA",
            image_url="",
            aesthetic_score=0.8,
            ogilvy_score=0.8,
            emotional_impact=0.8,
            format_type="social",
            demographic_segment=segment,
            generation_strategy="test",
            mutation_history=[],
            performance_score=0.0,
            trend_alignment=0.0,
            swipe_status="pending"
        )
        print("✅ AdVariantMorph creation successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Data model test failed: {e}")
        return False

async def run_all_tests():
    """Run all system tests"""
    
    print("🎯 AdMorph.AI System Tests")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Environment Tests", test_environment),
        ("Data Model Tests", test_data_models),
        ("Voice Agent Tests", test_voice_agent),
        ("Demographic Agent Tests", test_demographic_agent),
        ("Variant Generator Tests", test_variant_generator),
        ("Evolution System Tests", test_evolution_system)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
    else:
        print("⚠️ Some tests failed. Check configuration and dependencies.")
    
    return passed == total

if __name__ == "__main__":
    print("🧪 Starting AdMorph.AI System Tests...")
    
    try:
        success = asyncio.run(run_all_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test runner failed: {e}")
        sys.exit(1)
