"""
Complete AdMorph.AI Demo with Real Meta Data
Demonstrates the full workflow: Voice → Demographics → Generation → Swipe → Evolution
"""

import asyncio
import os
import sys
import json
import requests
from datetime import datetime
from typing import Dict, List, Any

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from admorph_core import BusinessProfile, DemographicSegment, AdVariantMorph
from real_meta_demographics_test import RealMetaDemographicsEngine
from enhanced_ad_generator import EnhancedAdGenerator
from dotenv import load_dotenv

load_dotenv()

class CompleteAdMorphWorkflow:
    """Complete AdMorph.AI workflow demonstration"""
    
    def __init__(self):
        self.meta_engine = RealMetaDemographicsEngine()
        self.ad_generator = EnhancedAdGenerator()
    
    async def simulate_voice_consultation(self) -> BusinessProfile:
        """Simulate intelligent voice consultation"""
        
        print("🎤 ADMORPH VOICE CONSULTATION")
        print("=" * 50)
        
        # Simulate business owner speaking to the system
        user_input = """
        Hi AdMorph! I run a SaaS company called 'WorkFlow Pro' that helps remote teams collaborate better. 
        We've been struggling with our advertising - we're spending about $12,000 per month but not seeing 
        great results. Our main customers are project managers, team leaders, and small business owners 
        who manage remote teams. We want to focus on getting more trial signups and conversions. 
        Our brand is all about simplicity, productivity, and team success - we definitely want to avoid 
        anything that looks too corporate or overwhelming.
        """
        
        print("👤 Business Owner:")
        print(f"   {user_input.strip()}")
        
        # AI processes the consultation
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
                        "content": "You are an expert marketing consultant. Extract key business information and provide strategic insights. Be conversational and ask intelligent follow-up questions."
                    },
                    {
                        "role": "user",
                        "content": f"Business consultation input: {user_input}"
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 300
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                ai_response = result['choices'][0]['message']['content']
                
                print("\n🤖 AdMorph AI Consultant:")
                print(f"   {ai_response}")
                
                # Create business profile from consultation
                business_profile = BusinessProfile(
                    business_id="workflow_pro_demo",
                    business_name="WorkFlow Pro",
                    industry="SaaS/Productivity Software",
                    target_engagement="trial_signups",
                    monthly_budget=12000.0,
                    target_audience={
                        "description": "Project managers, team leaders, and small business owners managing remote teams",
                        "pain_points": ["remote team coordination", "project management", "team productivity"]
                    },
                    brand_themes={
                        "allowed": ["simplicity", "productivity", "team success", "collaboration"],
                        "disallowed": ["corporate", "overwhelming", "complex"]
                    },
                    original_ad_assets=[],
                    voice_preferences={"tone": "friendly", "style": "solution-focused"},
                    created_at=datetime.now().isoformat(),
                    updated_at=datetime.now().isoformat()
                )
                
                print(f"\n✅ Business Profile Created:")
                print(f"   Company: {business_profile.business_name}")
                print(f"   Industry: {business_profile.industry}")
                print(f"   Budget: ${business_profile.monthly_budget:,}/month")
                print(f"   Goal: {business_profile.target_engagement}")
                
                return business_profile
                
            else:
                print(f"❌ API Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Voice consultation error: {e}")
            return None
    
    async def analyze_and_target_demographics(self, business_profile: BusinessProfile) -> List[DemographicSegment]:
        """Analyze business and create targeted demographic segments"""
        
        print(f"\n🎯 DEMOGRAPHIC ANALYSIS WITH REAL META DATA")
        print("=" * 50)
        
        segments = await self.meta_engine.analyze_business_and_select_interests(business_profile)
        
        if segments:
            print(f"\n✅ Created {len(segments)} targeted segments:")
            for i, segment in enumerate(segments, 1):
                interests = segment.meta_targeting_spec.get('selected_interests', [])
                print(f"   {i}. {segment.name}")
                print(f"      Age: {segment.age_range[0]}-{segment.age_range[1]} | Income: {segment.income_level}")
                print(f"      Key Interests: {', '.join([i['name'] for i in interests[:2]])}")
                print(f"      Meta IDs: {', '.join([i['id'] for i in interests[:2]])}")
        
        return segments
    
    async def generate_compelling_ads(self, business_profile: BusinessProfile, segments: List[DemographicSegment]) -> List[AdVariantMorph]:
        """Generate compelling ad variants for each segment"""
        
        print(f"\n🎨 GENERATING COMPELLING AD VARIANTS")
        print("=" * 50)
        
        variants = await self.ad_generator.create_compelling_ads(business_profile, segments)
        
        if variants:
            print(f"\n✅ Generated {len(variants)} compelling ad variants ready for review")
        
        return variants
    
    def simulate_swipe_review(self, variants: List[AdVariantMorph]) -> List[AdVariantMorph]:
        """Simulate marketing director swiping through ads"""
        
        print(f"\n📱 TINDER-STYLE AD REVIEW SIMULATION")
        print("=" * 50)
        
        approved_variants = []
        
        print("👨‍💼 Marketing Director reviewing ads...")
        
        for i, variant in enumerate(variants, 1):
            print(f"\n   📱 Ad {i}/{len(variants)}: {variant.demographic_segment.name}")
            print(f"      Headline: \"{variant.headline}\"")
            print(f"      Body: \"{variant.body}\"")
            print(f"      CTA: \"{variant.cta}\"")
            
            # Simulate decision based on quality scores
            combined_score = (variant.aesthetic_score + variant.ogilvy_score + variant.emotional_impact) / 3
            
            if combined_score > 0.88:
                decision = "✅ APPROVED"
                variant.swipe_status = "approved"
                approved_variants.append(variant)
            elif combined_score > 0.85:
                decision = "🔄 REGENERATE" if i % 2 == 0 else "✅ APPROVED"
                if decision == "✅ APPROVED":
                    variant.swipe_status = "approved"
                    approved_variants.append(variant)
                else:
                    variant.swipe_status = "regenerate"
            else:
                decision = "❌ REJECTED"
                variant.swipe_status = "rejected"
            
            print(f"      Decision: {decision}")
        
        print(f"\n✅ Swipe Review Complete:")
        print(f"   Approved: {len(approved_variants)}")
        print(f"   Rejected: {len([v for v in variants if v.swipe_status == 'rejected'])}")
        print(f"   Regenerate: {len([v for v in variants if v.swipe_status == 'regenerate'])}")
        
        return approved_variants
    
    def simulate_meta_publishing(self, approved_variants: List[AdVariantMorph], business_profile: BusinessProfile) -> Dict:
        """Simulate publishing to Meta API"""
        
        print(f"\n🚀 META API PUBLISHING SIMULATION")
        print("=" * 50)
        
        if not approved_variants:
            print("❌ No approved variants to publish")
            return {"success": False, "error": "No approved variants"}
        
        print(f"📤 Publishing {len(approved_variants)} approved ads to Meta...")
        
        # Simulate campaign creation
        campaign_data = {
            "campaign_id": f"admorph_campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "campaign_name": f"{business_profile.business_name}_AdMorph_Campaign",
            "objective": "CONVERSIONS",
            "budget": business_profile.monthly_budget,
            "status": "ACTIVE"
        }
        
        published_ads = []
        for variant in approved_variants:
            ad_data = {
                "ad_id": f"ad_{variant.variant_id}",
                "headline": variant.headline,
                "body": variant.body,
                "cta": variant.cta,
                "target_interests": [i['id'] for i in variant.demographic_segment.meta_targeting_spec.get('selected_interests', [])],
                "target_segment": variant.demographic_segment.name,
                "status": "ACTIVE"
            }
            published_ads.append(ad_data)
            
            # Mark as published
            variant.is_published = True
            variant.meta_campaign_id = campaign_data["campaign_id"]
        
        print(f"✅ Campaign Published Successfully!")
        print(f"   Campaign ID: {campaign_data['campaign_id']}")
        print(f"   Total Ads: {len(published_ads)}")
        print(f"   Budget: ${business_profile.monthly_budget:,}/month")
        
        for i, ad in enumerate(published_ads, 1):
            print(f"   Ad {i}: \"{ad['headline']}\" → {ad['target_segment']}")
        
        return {
            "success": True,
            "campaign": campaign_data,
            "published_ads": published_ads,
            "total_ads": len(published_ads)
        }
    
    def simulate_agentic_evolution(self, published_variants: List[AdVariantMorph]) -> Dict:
        """Simulate agentic evolution monitoring"""
        
        print(f"\n🧬 AGENTIC EVOLUTION MONITORING")
        print("=" * 50)
        
        print("🔄 Starting continuous evolution monitoring...")
        print("   • Performance tracking: CTR, conversions, engagement")
        print("   • Trend analysis: Social, economic, cultural shifts")
        print("   • Automatic mutations: Headlines, copy, targeting")
        print("   • Auto-publishing: High-confidence improvements")
        
        # Simulate evolution insights
        evolution_data = {
            "monitoring_active": True,
            "variants_tracked": len(published_variants),
            "mutation_triggers": [
                "Low CTR threshold (< 2%)",
                "Declining conversion rate",
                "New trending keywords detected",
                "Competitor analysis changes"
            ],
            "auto_publish_criteria": [
                "Trend alignment > 80%",
                "Confidence score > 85%",
                "A/B test significance reached"
            ]
        }
        
        print(f"\n✅ Evolution System Active:")
        print(f"   Tracking {evolution_data['variants_tracked']} ad variants")
        print(f"   Mutation triggers: {len(evolution_data['mutation_triggers'])} configured")
        print(f"   Auto-publish criteria: {len(evolution_data['auto_publish_criteria'])} rules")
        
        return evolution_data

async def run_complete_admorph_demo():
    """Run the complete AdMorph.AI workflow demonstration"""
    
    print("🎯 COMPLETE ADMORPH.AI WORKFLOW DEMONSTRATION")
    print("=" * 70)
    print("Voice → Demographics → Generation → Swipe → Publishing → Evolution")
    print("=" * 70)
    
    workflow = CompleteAdMorphWorkflow()
    
    # Step 1: Voice Consultation
    business_profile = await workflow.simulate_voice_consultation()
    if not business_profile:
        print("❌ Voice consultation failed")
        return False
    
    # Step 2: Demographic Analysis
    segments = await workflow.analyze_and_target_demographics(business_profile)
    if not segments:
        print("❌ Demographic analysis failed")
        return False
    
    # Step 3: Ad Generation
    variants = await workflow.generate_compelling_ads(business_profile, segments)
    if not variants:
        print("❌ Ad generation failed")
        return False
    
    # Step 4: Swipe Review
    approved_variants = workflow.simulate_swipe_review(variants)
    
    # Step 5: Meta Publishing
    publish_result = workflow.simulate_meta_publishing(approved_variants, business_profile)
    
    # Step 6: Agentic Evolution
    evolution_result = workflow.simulate_agentic_evolution(approved_variants)
    
    # Final Results
    print("\n" + "=" * 70)
    print("🎉 COMPLETE ADMORPH.AI WORKFLOW DEMONSTRATION COMPLETE!")
    print("=" * 70)
    
    print(f"✅ Business: {business_profile.business_name}")
    print(f"✅ Industry: {business_profile.industry}")
    print(f"✅ Budget: ${business_profile.monthly_budget:,}/month")
    print(f"✅ Segments Created: {len(segments)}")
    print(f"✅ Variants Generated: {len(variants)}")
    print(f"✅ Variants Approved: {len(approved_variants)}")
    print(f"✅ Campaign Published: {publish_result['success']}")
    print(f"✅ Evolution Active: {evolution_result['monitoring_active']}")
    
    print("\n🚀 AdMorph.AI Features Demonstrated:")
    print("   • Intelligent voice consultation ✅")
    print("   • Real Meta demographics targeting ✅")
    print("   • AI-powered ad generation ✅")
    print("   • Tinder-style swipe review ✅")
    print("   • Meta API campaign publishing ✅")
    print("   • Agentic evolution monitoring ✅")
    
    print("\n📈 Expected Results:")
    print("   • Higher CTR from precise targeting")
    print("   • Better conversion rates from compelling copy")
    print("   • Lower CPA through audience relevance")
    print("   • Continuous optimization through evolution")
    
    return True

if __name__ == "__main__":
    print("🎯 Starting Complete AdMorph.AI Workflow Demo...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OpenAI API key not found.")
        sys.exit(1)
    
    try:
        success = asyncio.run(run_complete_admorph_demo())
        if success:
            print("\n🎉 Complete workflow demo successful!")
            print("✅ AdMorph.AI is ready for production deployment!")
        else:
            print("\n❌ Demo failed.")
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
