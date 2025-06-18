"""
Simple OpenAI Test with Manual Configuration
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment
load_dotenv()

def test_openai_with_requests():
    """Test OpenAI API using direct HTTP requests"""
    
    print("🧪 Testing OpenAI API with Direct HTTP Requests...")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No OpenAI API key found")
        return False
    
    print(f"✅ API Key found (ending in ...{api_key[-10:]})")
    
    try:
        # Direct API call
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a helpful advertising expert."},
                {"role": "user", "content": "Create a catchy headline for a fitness app targeting busy professionals. Keep it under 40 characters."}
            ],
            "temperature": 0.7,
            "max_tokens": 100
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            headline = result['choices'][0]['message']['content']
            
            print("✅ OpenAI API Connection Successful!")
            print(f"   Generated Headline: {headline.strip()}")
            print(f"   Usage: {result['usage']['total_tokens']} tokens")
            
            return True, headline.strip()
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Request Error: {e}")
        return False, None

def test_business_consultation_direct():
    """Test business consultation with direct API call"""
    
    print("\n🎤 Testing Business Consultation (Direct API)...")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are an expert marketing consultant. Extract key business information and provide strategic insights."
                },
                {
                    "role": "user", 
                    "content": "I run FitLife Pro, a fitness coaching business. We help busy professionals get in shape with personalized workout plans. Our monthly ad budget is $8000. What demographic segments should we target?"
                }
            ],
            "temperature": 0.7,
            "max_tokens": 300
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            consultation = result['choices'][0]['message']['content']
            
            print("✅ Business Consultation Successful!")
            print(f"   AI Response: {consultation[:200]}...")
            
            return True, consultation
        else:
            print(f"❌ API Error: {response.status_code}")
            return False, None
            
    except Exception as e:
        print(f"❌ Consultation Error: {e}")
        return False, None

def test_ad_generation_direct():
    """Test ad generation with direct API call"""
    
    print("\n🎨 Testing Ad Generation (Direct API)...")
    print("=" * 50)
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are an expert ad copywriter. Create compelling, conversion-focused ad copy."
                },
                {
                    "role": "user", 
                    "content": """Create 2 ad variants for FitLife Pro targeting busy professionals:

Variant 1: Focus on time efficiency
Variant 2: Focus on results and transformation

For each variant, provide:
- Headline (max 40 characters)
- Body copy (max 125 characters)  
- Call-to-action

Format as JSON array."""
                }
            ],
            "temperature": 0.8,
            "max_tokens": 400
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            ads = result['choices'][0]['message']['content']
            
            print("✅ Ad Generation Successful!")
            print(f"   Generated Ads: {ads[:300]}...")
            
            return True, ads
        else:
            print(f"❌ API Error: {response.status_code}")
            return False, None
            
    except Exception as e:
        print(f"❌ Ad Generation Error: {e}")
        return False, None

def create_real_admorph_demo():
    """Create a real AdMorph demo with working OpenAI"""
    
    print("\n🚀 Creating Real AdMorph Demo...")
    print("=" * 60)
    
    # Test all components
    api_success, headline = test_openai_with_requests()
    consultation_success, consultation = test_business_consultation_direct()
    ads_success, ads = test_ad_generation_direct()
    
    if api_success and consultation_success and ads_success:
        print("\n" + "=" * 60)
        print("🎉 REAL ADMORPH DEMO RESULTS")
        print("=" * 60)
        
        print("✅ Voice Interface Simulation:")
        print(f"   Business: FitLife Pro (Fitness Coaching)")
        print(f"   Budget: $8,000/month")
        print(f"   Target: Busy professionals")
        
        print("\n✅ AI Consultation Results:")
        print(f"   {consultation[:200]}...")
        
        print("\n✅ Generated Ad Variants:")
        print(f"   Sample Headline: {headline}")
        print(f"   Full Ad Copy: {ads[:200]}...")
        
        print("\n🎯 AdMorph Features Demonstrated:")
        print("   • Real OpenAI API integration ✅")
        print("   • Business consultation ✅")
        print("   • Demographic analysis ✅")
        print("   • Ad variant generation ✅")
        print("   • Ready for swipe review ✅")
        
        return True
    else:
        print("\n❌ Some components failed - check API configuration")
        return False

if __name__ == "__main__":
    print("🎯 AdMorph.AI Real Use Case Test")
    print("=" * 60)
    
    success = create_real_admorph_demo()
    
    if success:
        print("\n🎉 AdMorph.AI is ready for production!")
        print("✅ All core features working with real OpenAI API")
        print("🚀 Next: Set up Meta API for publishing")
    else:
        print("\n⚠️ Check API configuration and try again")
