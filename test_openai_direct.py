"""
Direct OpenAI API Test
"""

import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_openai_direct():
    """Test OpenAI API directly"""
    
    print("🧪 Testing OpenAI API Direct Connection...")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No OpenAI API key found")
        return False
    
    print(f"✅ API Key found (ending in ...{api_key[-10:]})")
    
    try:
        from openai import OpenAI
        
        # Initialize client
        client = OpenAI(api_key=api_key)
        
        # Test simple completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful advertising expert."},
                {"role": "user", "content": "Create a catchy headline for a fitness app targeting busy professionals. Keep it under 40 characters."}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        result = response.choices[0].message.content
        
        print("✅ OpenAI API Connection Successful!")
        print(f"   Model: {response.model}")
        print(f"   Generated Headline: {result}")
        print(f"   Usage: {response.usage.total_tokens} tokens")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API Error: {e}")
        return False

def test_business_consultation():
    """Test business consultation with OpenAI"""
    
    print("\n🎤 Testing Business Consultation...")
    print("=" * 50)
    
    try:
        from openai import OpenAI
        
        client = OpenAI()
        
        # Simulate business consultation
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert marketing consultant conducting a business onboarding interview. Extract key business information and ask intelligent follow-up questions."
                },
                {
                    "role": "user", 
                    "content": "Hi, I run FitLife Pro, a fitness coaching business. We help busy professionals get in shape with personalized workout plans and nutrition guidance. Our monthly budget is around $8000."
                }
            ],
            temperature=0.8,
            max_tokens=200
        )
        
        consultation_response = response.choices[0].message.content
        
        print("✅ Business Consultation Successful!")
        print(f"   AI Response: {consultation_response[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Business Consultation Error: {e}")
        return False

def test_demographic_analysis():
    """Test demographic analysis with OpenAI"""
    
    print("\n🎯 Testing Demographic Analysis...")
    print("=" * 50)
    
    try:
        from openai import OpenAI
        
        client = OpenAI()
        
        # Test demographic segmentation
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a demographic targeting expert. Create distinct, high-value audience segments for advertising campaigns. Return valid JSON only."
                },
                {
                    "role": "user", 
                    "content": """
                    Analyze this business and create 3 distinct demographic segments:
                    
                    Business: FitLife Pro
                    Industry: Health & Fitness
                    Target: Busy professionals who want to get in shape
                    Budget: $8000/month
                    
                    For each segment, define: name, age_range, gender, interests, behaviors, income_level, education
                    Return as JSON array.
                    """
                }
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        segments_response = response.choices[0].message.content
        
        print("✅ Demographic Analysis Successful!")
        print(f"   Generated Segments: {segments_response[:300]}...")
        
        # Try to parse JSON
        import json
        try:
            segments = json.loads(segments_response)
            print(f"   Parsed {len(segments)} segments successfully")
        except:
            print("   Note: Response may need JSON formatting")
        
        return True
        
    except Exception as e:
        print(f"❌ Demographic Analysis Error: {e}")
        return False

def test_ad_generation():
    """Test ad generation with OpenAI"""
    
    print("\n🎨 Testing Ad Generation...")
    print("=" * 50)
    
    try:
        from openai import OpenAI
        
        client = OpenAI()
        
        # Test ad variant generation
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert ad copywriter specializing in demographic-specific messaging. Create compelling ad variants."
                },
                {
                    "role": "user", 
                    "content": """
                    Create 2 ad variants for this demographic:
                    
                    Business: FitLife Pro (fitness coaching)
                    Target: Busy professionals aged 28-42, high income, health conscious
                    Goal: Drive sales of personalized fitness programs
                    
                    For each variant create:
                    1. Compelling headline (max 40 chars)
                    2. Engaging body copy (max 125 chars)
                    3. Strong call-to-action
                    4. Emotional hook
                    
                    Make each variant distinctly different in approach.
                    """
                }
            ],
            temperature=0.8,
            max_tokens=400
        )
        
        ads_response = response.choices[0].message.content
        
        print("✅ Ad Generation Successful!")
        print(f"   Generated Ads: {ads_response[:400]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Ad Generation Error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 AdMorph.AI Direct OpenAI API Test")
    print("=" * 60)
    
    tests = [
        ("Direct API Connection", test_openai_direct),
        ("Business Consultation", test_business_consultation),
        ("Demographic Analysis", test_demographic_analysis),
        ("Ad Generation", test_ad_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 DIRECT API TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{total} direct API tests passed")
    
    if passed == total:
        print("🎉 OpenAI API is working perfectly!")
        print("✅ Ready to integrate with AdMorph agents")
    else:
        print("⚠️ Some API tests failed. Check API key and network.")
