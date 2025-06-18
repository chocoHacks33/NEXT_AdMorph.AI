"""
AI Advertising Agent Framework
Built on Ogilvy's principles with divide-and-conquer agent architecture
Designed to give SMEs access to agency-level advertising intelligence
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
import numpy as np
from enum import Enum

# Import AdMorph components
from admorph_core import (
    BusinessProfile, AdVariantMorph, DemographicSegment,
    AdMorphVoiceAgent, DemographicAnalysisAgent, AdVariantGenerationAgent
)
from swipe_interface import TinderStyleAdReviewer
from meta_api_integration import AdMorphCampaignManager
from agentic_evolution import EvolutionOrchestrator, EvolutionMonitor

# Core Data Models
@dataclass
class DiscoveryBrief:
    """Client brief following Ogilvy's discovery methodology"""
    id: str
    product: str
    audience: str
    goal: str  # 'sales' or 'awareness'
    budget: int
    assets: Dict[str, str]
    brand_personality: str = ""
    competitor_analysis: str = ""
    unique_selling_proposition: str = ""
    emotional_trigger: str = ""

@dataclass
class AdVariant:
    """Individual ad variant with Ogilvy-inspired copy structure"""
    variant_id: str
    headline: str
    body: str
    cta: str
    image_url: str
    aesthetic_score: float
    ogilvy_score: float  # Based on Ogilvy's 38 rules
    emotional_impact: float
    format_type: str  # 'social', 'display', 'video'

@dataclass
class EngagementMetrics:
    """Real-time performance tracking"""
    variant_id: str
    impressions: int
    clicks: int
    ctr: float
    conversions: int
    engagement_rate: float
    timestamp: str
    cost_per_acquisition: float

class AgentRole(Enum):
    COPYWRITER = "copywriter"
    ART_DIRECTOR = "art_director" 
    AESTHETIC_ANALYZER = "aesthetic_analyzer"
    STRATEGIST = "strategist"
    PERFORMANCE_OPTIMIZER = "performance_optimizer"

# Base Agent Architecture
class BaseAgent(ABC):
    """Abstract base for all advertising agents"""
    
    def __init__(self, role: AgentRole, expertise_level: int = 10):
        self.role = role
        self.expertise_level = expertise_level
        self.agent_id = str(uuid.uuid4())
        
    @abstractmethod
    async def execute(self, brief: DiscoveryBrief, context: Dict = None) -> Dict:
        """Execute agent's specialized function"""
        pass
    
    def validate_input(self, data: Any) -> bool:
        """Validate input data quality"""
        return data is not None

# Specialized Agent Implementations
class OgilvyCopywriterAgent(BaseAgent):
    """Master copywriter based on Ogilvy's 38 advertising rules"""
    
    def __init__(self):
        super().__init__(AgentRole.COPYWRITER)
        self.ogilvy_rules = self._load_ogilvy_principles()
    
    def _load_ogilvy_principles(self) -> Dict:
        """Ogilvy's core copywriting principles"""
        return {
            "headline_rules": [
                "Include the selling proposition in your headline",
                "Inject news into your headline",
                "Use testimonial headlines",
                "Make your headline specific",
                "Promise a benefit in your headline"
            ],
            "body_copy_rules": [
                "Make your copy interesting to read",
                "Tell the truth but make it fascinating", 
                "Use short words, short sentences, short paragraphs",
                "Include testimonials",
                "Make your advertisements contemporary"
            ],
            "cta_rules": [
                "Tell the reader exactly what action to take",
                "Make it easy to respond",
                "Create urgency without being pushy"
            ]
        }
    
    async def execute(self, brief: DiscoveryBrief, context: Dict = None) -> Dict:
        """Generate Ogilvy-inspired copy variants"""
        
        # Extract USP and emotional triggers
        usp = await self._extract_usp(brief)
        emotional_hook = await self._identify_emotional_trigger(brief)
        
        # Generate multiple headline variations
        headlines = await self._generate_headlines(brief, usp, emotional_hook)
        
        # Create body copy with Ogilvy's structure
        body_variants = await self._generate_body_copy(brief, usp)
        
        # Craft compelling CTAs
        ctas = await self._generate_ctas(brief)
        
        return {
            "headlines": headlines,
            "body_copy": body_variants,
            "ctas": ctas,
            "usp": usp,
            "emotional_trigger": emotional_hook,
            "ogilvy_compliance_score": await self._score_ogilvy_compliance(headlines, body_variants)
        }
    
    async def _extract_usp(self, brief: DiscoveryBrief) -> str:
        """Extract unique selling proposition using Ogilvy's methodology"""
        # Analyze product benefits vs competitors
        # Find the one thing that makes this product uniquely valuable
        return f"The only {brief.product} that {brief.unique_selling_proposition or 'delivers exceptional value'}"
    
    async def _identify_emotional_trigger(self, brief: DiscoveryBrief) -> str:
        """Identify primary emotional driver for the audience"""
        emotional_map = {
            "business": "success, efficiency, growth",
            "consumer": "happiness, security, status", 
            "health": "vitality, confidence, peace of mind",
            "finance": "security, freedom, prosperity"
        }
        return emotional_map.get(brief.audience.lower(), "satisfaction, value, trust")
    
    async def _generate_headlines(self, brief: DiscoveryBrief, usp: str, emotion: str) -> List[str]:
        """Generate headlines following Ogilvy's proven formulas"""
        templates = [
            f"How {brief.product} Gives You {emotion.split(',')[0].strip()}",
            f"The Secret of {usp}",
            f"They Laughed When I Said {brief.product} Could {emotion.split(',')[1].strip()}... But When They Saw The Results!",
            f"At Last! A {brief.product} That {usp.split('that')[1] if 'that' in usp else 'Works'}",
            f"New Discovery: {brief.product} That {emotion.split(',')[2].strip()}"
        ]
        return templates[:3]  # Return top 3 variants
    
    async def _generate_body_copy(self, brief: DiscoveryBrief, usp: str) -> List[str]:
        """Generate body copy with Ogilvy's structure"""
        body_template = f"""
        Here's what makes {brief.product} different:
        
        {usp}
        
        Our customers tell us they've seen remarkable results. Just last week, one customer said: 
        "This changed everything for my {brief.audience} needs."
        
        Don't wait. Every day you delay is a day without these benefits.
        """
        return [body_template.strip()]
    
    async def _generate_ctas(self, brief: DiscoveryBrief) -> List[str]:
        """Generate compelling calls-to-action"""
        if brief.goal == "sales":
            return ["Order Now", "Get Started Today", "Claim Your Copy"]
        else:
            return ["Learn More", "Download Free Guide", "See How It Works"]
    
    async def _score_ogilvy_compliance(self, headlines: List[str], body: List[str]) -> float:
        """Score copy against Ogilvy's principles"""
        # Simplified scoring - in production, use NLP analysis
        score = 0.8  # Baseline high score since we're following principles
        return score

class ArtDirectorAgent(BaseAgent):
    """Visual creative director focused on aesthetic principles"""
    
    def __init__(self):
        super().__init__(AgentRole.ART_DIRECTOR)
        self.composition_rules = self._load_composition_principles()
    
    def _load_composition_principles(self) -> Dict:
        """Visual design principles for high-converting ads"""
        return {
            "rule_of_thirds": "Place focal points at intersection points",
            "golden_ratio": "Use 1.618 proportions for pleasing layouts",
            "color_psychology": {
                "red": "urgency, passion, energy",
                "blue": "trust, professionalism, calm",
                "green": "growth, money, nature",
                "orange": "enthusiasm, creativity, warmth"
            },
            "typography_hierarchy": "Headline > Subhead > Body > CTA",
            "white_space": "Use generous white space for elegance"
        }
    
    async def execute(self, brief: DiscoveryBrief, context: Dict = None) -> Dict:
        """Generate visual concepts and layouts"""
        
        # Determine optimal color palette
        colors = await self._select_color_palette(brief)
        
        # Create layout specifications
        layouts = await self._generate_layouts(brief)
        
        # Design image concepts
        image_concepts = await self._create_image_concepts(brief)
        
        return {
            "color_palette": colors,
            "layouts": layouts,
            "image_concepts": image_concepts,
            "typography_specs": await self._define_typography(brief),
            "composition_score": 0.85  # High score for following best practices
        }
    
    async def _select_color_palette(self, brief: DiscoveryBrief) -> Dict:
        """Select colors based on psychology and brand"""
        if brief.goal == "sales":
            return {"primary": "#FF4444", "secondary": "#FFFFFF", "accent": "#333333"}
        else:
            return {"primary": "#4A90E2", "secondary": "#F8F9FA", "accent": "#2C3E50"}
    
    async def _generate_layouts(self, brief: DiscoveryBrief) -> List[Dict]:
        """Generate layout options following composition rules"""
        return [
            {
                "name": "Hero Focus",
                "structure": "Large image top, headline overlay, body below",
                "rule_of_thirds": True,
                "golden_ratio": True
            },
            {
                "name": "Split Layout", 
                "structure": "Text left, image right, CTA bottom",
                "rule_of_thirds": True,
                "golden_ratio": False
            }
        ]
    
    async def _create_image_concepts(self, brief: DiscoveryBrief) -> List[str]:
        """Generate image concepts that support the message"""
        return [
            f"Professional photo of {brief.product} in use by {brief.audience}",
            f"Lifestyle shot showing benefits of {brief.product}",
            f"Before/after comparison highlighting {brief.product} impact"
        ]
    
    async def _define_typography(self, brief: DiscoveryBrief) -> Dict:
        """Define typography hierarchy and specs"""
        return {
            "headline": {"font": "Bold Sans", "size": "36px", "weight": "700"},
            "subhead": {"font": "Regular Sans", "size": "18px", "weight": "400"}, 
            "body": {"font": "Regular Sans", "size": "14px", "weight": "400"},
            "cta": {"font": "Bold Sans", "size": "16px", "weight": "600"}
        }

class AestheticAnalyzerAgent(BaseAgent):
    """Analyze and score visual aesthetics using proven principles"""
    
    def __init__(self):
        super().__init__(AgentRole.AESTHETIC_ANALYZER)
    
    async def execute(self, brief: DiscoveryBrief, context: Dict = None) -> Dict:
        """Analyze aesthetic quality of ad variants"""
        
        if not context or "layout" not in context:
            return {"aesthetic_score": 0.5, "recommendations": []}
        
        # Score composition elements
        composition_score = await self._score_composition(context["layout"])
        color_score = await self._score_color_harmony(context.get("colors", {}))
        typography_score = await self._score_typography(context.get("typography", {}))
        
        overall_score = (composition_score + color_score + typography_score) / 3
        
        return {
            "aesthetic_score": overall_score,
            "composition_score": composition_score,
            "color_score": color_score,
            "typography_score": typography_score,
            "recommendations": await self._generate_recommendations(overall_score)
        }
    
    async def _score_composition(self, layout: Dict) -> float:
        """Score layout composition using design principles"""
        score = 0.5  # Base score
        
        if layout.get("rule_of_thirds"):
            score += 0.2
        if layout.get("golden_ratio"):
            score += 0.15
        if "white_space" in layout:
            score += 0.15
            
        return min(score, 1.0)
    
    async def _score_color_harmony(self, colors: Dict) -> float:
        """Score color palette harmony and psychology alignment"""
        return 0.8  # Simplified - would use color theory algorithms
    
    async def _score_typography(self, typography: Dict) -> float:
        """Score typography hierarchy and readability"""
        return 0.85  # Simplified scoring
    
    async def _generate_recommendations(self, score: float) -> List[str]:
        """Generate improvement recommendations"""
        if score < 0.6:
            return [
                "Improve visual hierarchy with better typography contrast",
                "Apply rule of thirds to key elements",
                "Increase white space for better readability"
            ]
        elif score < 0.8:
            return [
                "Fine-tune color balance",
                "Optimize element positioning"
            ]
        else:
            return ["Excellent aesthetic quality - no major improvements needed"]

# Core Orchestration Engine
class AdAgencyOrchestrator:
    """Main orchestrator that coordinates all agents"""
    
    def __init__(self):
        self.agents = {
            AgentRole.COPYWRITER: OgilvyCopywriterAgent(),
            AgentRole.ART_DIRECTOR: ArtDirectorAgent(),
            AgentRole.AESTHETIC_ANALYZER: AestheticAnalyzerAgent()
        }
        self.active_campaigns = {}
    
    async def process_brief(self, brief: DiscoveryBrief) -> Dict:
        """Main processing pipeline - orchestrate all agents"""
        
        # Stage 1: Strategic Copy Development
        copy_results = await self.agents[AgentRole.COPYWRITER].execute(brief)
        
        # Stage 2: Visual Direction
        art_results = await self.agents[AgentRole.ART_DIRECTOR].execute(brief)
        
        # Stage 3: Aesthetic Analysis
        aesthetic_context = {
            "layout": art_results["layouts"][0],
            "colors": art_results["color_palette"],
            "typography": art_results["typography_specs"]
        }
        aesthetic_results = await self.agents[AgentRole.AESTHETIC_ANALYZER].execute(
            brief, aesthetic_context
        )
        
        # Stage 4: Assemble Ad Variants
        variants = await self._create_ad_variants(brief, copy_results, art_results, aesthetic_results)
        
        return {
            "brief_id": brief.id,
            "variants": variants,
            "copy_analysis": copy_results,
            "visual_analysis": art_results,
            "aesthetic_analysis": aesthetic_results,
            "processing_timestamp": datetime.now().isoformat()
        }
    
    async def _create_ad_variants(self, brief: DiscoveryBrief, copy: Dict, art: Dict, aesthetic: Dict) -> List[AdVariant]:
        """Combine all agent outputs into final ad variants"""
        variants = []
        
        for i, headline in enumerate(copy["headlines"]):
            variant = AdVariant(
                variant_id=str(uuid.uuid4()),
                headline=headline,
                body=copy["body_copy"][0],  # Use first body copy variant
                cta=copy["ctas"][0],
                image_url=f"generated_image_{i+1}.jpg",  # Placeholder
                aesthetic_score=aesthetic["aesthetic_score"],
                ogilvy_score=copy["ogilvy_compliance_score"],
                emotional_impact=0.8,  # Simplified scoring
                format_type="social"
            )
            variants.append(variant)
        
        return variants

# AdMorph Engine - Dynamic Ad Evolution
class AdMorphEngine:
    """Continuously evolve ads based on performance data"""
    
    def __init__(self):
        self.performance_history = {}
        self.mutation_strategies = self._load_mutation_strategies()
    
    def _load_mutation_strategies(self) -> Dict:
        """Define how to mutate ad elements based on performance"""
        return {
            "low_ctr": [
                "Test more compelling headlines",
                "Increase emotional intensity",
                "Test different CTA wording"
            ],
            "low_conversion": [
                "Strengthen value proposition",
                "Add urgency elements",
                "Test different audience angles"
            ],
            "high_engagement_low_conversion": [
                "Improve landing page alignment",
                "Test stronger CTAs",
                "Add testimonials or proof"
            ]
        }
    
    async def analyze_performance(self, metrics: List[EngagementMetrics]) -> Dict:
        """Analyze performance and suggest optimizations"""
        
        performance_insights = {}
        
        for metric in metrics:
            # Identify performance patterns
            if metric.ctr < 0.02:  # Low CTR
                performance_insights[metric.variant_id] = {
                    "issue": "low_ctr",
                    "recommendations": self.mutation_strategies["low_ctr"]
                }
            elif metric.engagement_rate > 0.05 and metric.conversions < 10:
                performance_insights[metric.variant_id] = {
                    "issue": "high_engagement_low_conversion", 
                    "recommendations": self.mutation_strategies["high_engagement_low_conversion"]
                }
        
        return performance_insights
    
    async def mutate_ads(self, variants: List[AdVariant], performance_data: Dict) -> List[AdVariant]:
        """Generate mutated variants based on performance insights"""
        
        mutated_variants = []
        
        for variant in variants:
            if variant.variant_id in performance_data:
                insight = performance_data[variant.variant_id]
                
                # Create mutated version
                new_variant = AdVariant(
                    variant_id=str(uuid.uuid4()),
                    headline=await self._mutate_headline(variant.headline, insight),
                    body=variant.body,
                    cta=await self._mutate_cta(variant.cta, insight),
                    image_url=variant.image_url,
                    aesthetic_score=variant.aesthetic_score,
                    ogilvy_score=variant.ogilvy_score,
                    emotional_impact=variant.emotional_impact * 1.1,  # Increase emotional impact
                    format_type=variant.format_type
                )
                mutated_variants.append(new_variant)
        
        return mutated_variants
    
    async def _mutate_headline(self, original: str, insight: Dict) -> str:
        """Mutate headline based on performance insight"""
        if insight["issue"] == "low_ctr":
            # Add more compelling elements
            return f"URGENT: {original}"
        return original
    
    async def _mutate_cta(self, original: str, insight: Dict) -> str:
        """Mutate CTA based on performance insight"""
        if insight["issue"] == "low_conversion":
            cta_variants = {
                "Learn More": "Get Instant Access",
                "Sign Up": "Start Free Trial",
                "Buy Now": "Get Yours Today"
            }
            return cta_variants.get(original, original)
        return original

# Client Interface & Onboarding
class SMEOnboardingExperience:
    """Unique onboarding experience designed like the best salesman"""
    
    def __init__(self):
        self.onboarding_steps = self._design_onboarding_flow()
    
    def _design_onboarding_flow(self) -> List[Dict]:
        """Design onboarding like a master salesman's consultation"""
        return [
            {
                "step": "rapport_building",
                "message": "I've helped over 10,000 businesses like yours break through their advertising plateau. What's the biggest challenge you're facing with your current marketing?",
                "purpose": "Build trust and identify pain points"
            },
            {
                "step": "problem_amplification", 
                "message": "I understand. Most business owners tell me they're frustrated because they know their product is great, but they can't seem to get their message across in a way that makes people stop and take notice. Is that what you're experiencing?",
                "purpose": "Amplify the problem they're experiencing"
            },
            {
                "step": "vision_creation",
                "message": "Imagine if every ad you ran felt like it was created by the top advertising agencies - the kind that charge $50,000 per month. What would that mean for your business?",
                "purpose": "Paint a picture of the desired outcome"
            },
            {
                "step": "credibility_establishment",
                "message": "The framework I'm about to share with you is built on David Ogilvy's proven principles - the same ones that built brands like Rolls-Royce and Dove. These aren't new, untested theories. They're time-tested strategies that have generated billions in sales.",
                "purpose": "Establish credibility and authority"
            },
            {
                "step": "brief_collection",
                "message": "Let's dive into your specific situation. I need to understand three critical things about your business...",
                "purpose": "Collect detailed brief information"
            }
        ]
    
    async def conduct_onboarding(self) -> DiscoveryBrief:
        """Conduct the full onboarding experience"""
        
        print("=== WELCOME TO YOUR AI ADVERTISING AGENCY ===\n")
        
        # Execute onboarding flow
        for step in self.onboarding_steps[:-1]:  # Skip the last step for now
            print(f"🎯 {step['message']}\n")
            input("Press Enter to continue...")
            print()
        
        # Collect detailed brief
        print("🎯 Let's dive into your specific situation. I need to understand three critical things about your business...\n")
        
        product = input("1. What exactly are you selling? (Be specific): ")
        audience = input("2. Who is your ideal customer? (Demographics, psychographics): ")
        goal = input("3. What's your primary goal? (sales/awareness): ")
        budget = int(input("4. What's your monthly advertising budget? $"))
        
        # Create and return the brief
        brief = DiscoveryBrief(
            id=str(uuid.uuid4()),
            product=product,
            audience=audience,
            goal=goal,
            budget=budget,
            assets={"logoUrl": ""}
        )
        
        print(f"\n✅ Perfect! I have everything I need to create advertising that works for {product}.")
        print("Now watch as I coordinate my team of specialists to build your campaign...\n")
        
        return brief

# Enhanced AdMorph Integration
class AdMorphIntegratedOrchestrator(AdAgencyOrchestrator):
    """Enhanced orchestrator that integrates AdMorph capabilities with Ogilvy principles"""

    def __init__(self):
        super().__init__()
        # AdMorph components
        self.voice_agent = AdMorphVoiceAgent()
        self.demographic_agent = DemographicAnalysisAgent()
        self.variant_generator = AdVariantGenerationAgent()
        self.evolution_orchestrator = EvolutionOrchestrator()
        self.campaign_manager = AdMorphCampaignManager()

    async def process_admorph_workflow(self, voice_input: Dict) -> Dict:
        """Complete AdMorph workflow from voice input to published ads"""

        # Stage 1: Voice-based business profiling
        business_profile = await self._create_business_profile_from_voice(voice_input)

        # Stage 2: Demographic analysis and segmentation
        demographic_analysis = await self.demographic_agent.execute(business_profile)

        # Stage 3: Generate ad variants for each segment using both Ogilvy and AdMorph
        all_variants = await self._generate_enhanced_variants(business_profile, demographic_analysis)

        # Stage 4: Return for swipe review
        return {
            "business_profile": business_profile,
            "demographic_segments": demographic_analysis["demographic_segments"],
            "ad_variants": all_variants,
            "ready_for_review": True,
            "workflow_stage": "swipe_review"
        }

    async def _create_business_profile_from_voice(self, voice_input: Dict) -> BusinessProfile:
        """Create business profile from voice interaction data"""

        # Extract data from voice interaction
        extracted_data = voice_input.get("extracted_data", {})

        return BusinessProfile(
            business_id=str(uuid.uuid4()),
            business_name=extracted_data.get("business_name", "Unknown Business"),
            industry=extracted_data.get("industry", "General"),
            target_engagement=extracted_data.get("goal", "sales"),
            monthly_budget=float(extracted_data.get("monthly_budget", 5000)),
            target_audience=extracted_data.get("target_audience", {}),
            brand_themes=extracted_data.get("brand_themes", {"allowed": [], "disallowed": []}),
            original_ad_assets=extracted_data.get("assets", []),
            voice_preferences=extracted_data.get("voice_preferences", {}),
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

    async def _generate_enhanced_variants(self, business_profile: BusinessProfile, demographic_analysis: Dict) -> List[AdVariantMorph]:
        """Generate enhanced variants combining Ogilvy principles with demographic targeting"""

        # Convert business profile to DiscoveryBrief for Ogilvy agents
        discovery_brief = DiscoveryBrief(
            id=business_profile.business_id,
            product=business_profile.business_name,
            audience=str(business_profile.target_audience),
            goal=business_profile.target_engagement,
            budget=int(business_profile.monthly_budget),
            assets={"logoUrl": ""}
        )

        # Get Ogilvy-based copy insights
        ogilvy_copy = await self.agents[AgentRole.COPYWRITER].execute(discovery_brief)
        ogilvy_art = await self.agents[AgentRole.ART_DIRECTOR].execute(discovery_brief)

        # Generate AdMorph variants for each demographic segment
        variant_results = await self.variant_generator.execute(
            business_profile,
            demographic_analysis["demographic_segments"]
        )

        # Enhance variants with Ogilvy insights
        enhanced_variants = []
        for variant in variant_results["variants"]:
            # Apply Ogilvy scoring and enhancements
            variant.ogilvy_score = ogilvy_copy["ogilvy_compliance_score"]

            # Enhance headline with Ogilvy principles if score is low
            if variant.ogilvy_score < 0.7:
                enhanced_headline = await self._enhance_with_ogilvy(variant.headline, ogilvy_copy)
                variant.headline = enhanced_headline
                variant.ogilvy_score = 0.8  # Improved score

            enhanced_variants.append(variant)

        return enhanced_variants

    async def _enhance_with_ogilvy(self, original_text: str, ogilvy_insights: Dict) -> str:
        """Enhance text using Ogilvy principles"""

        # Simple enhancement - in production, use more sophisticated NLP
        if "usp" in ogilvy_insights:
            usp = ogilvy_insights["usp"]
            if "only" in usp.lower() and "only" not in original_text.lower():
                return f"The Only {original_text}"

        return original_text

# Main Application Interface
class AIAdvertisingAgency:
    """Main application interface - the complete AI advertising agency with AdMorph integration"""

    def __init__(self):
        self.orchestrator = AdMorphIntegratedOrchestrator()  # Enhanced orchestrator
        self.morph_engine = AdMorphEngine()
        self.onboarding = SMEOnboardingExperience()
        self.active_campaigns = {}

        # AdMorph components
        self.voice_agent = AdMorphVoiceAgent()
        self.swipe_reviewer = TinderStyleAdReviewer()
        self.campaign_manager = AdMorphCampaignManager()
        self.evolution_monitor = None
    
    async def launch_campaign(self) -> Dict:
        """Complete campaign launch flow"""

        # Step 1: Onboarding Experience
        brief = await self.onboarding.conduct_onboarding()

        # Step 2: Agent Orchestration
        print("🔄 Coordinating copywriter, art director, and aesthetic analyzer...")
        campaign_results = await self.orchestrator.process_brief(brief)

        # Step 3: Present Results
        await self._present_campaign_results(campaign_results)

        # Step 4: Store for ongoing optimization
        self.active_campaigns[brief.id] = {
            "brief": brief,
            "results": campaign_results,
            "launch_date": datetime.now()
        }

        return campaign_results

    async def launch_admorph_campaign(self) -> Dict:
        """Complete AdMorph campaign launch flow with voice interface and evolution"""

        print("🎯 Welcome to AdMorph.AI - Intelligent Advertising Evolution")
        print("=" * 60)

        # Step 1: Voice-based Business Profiling
        print("🎤 Starting voice-based business consultation...")
        voice_result = await self._conduct_voice_onboarding()

        # Step 2: AdMorph Workflow Processing
        print("🧠 Processing business profile and generating demographic segments...")
        workflow_result = await self.orchestrator.process_admorph_workflow(voice_result)

        # Step 3: Present variants for swipe review
        print(f"✨ Generated {len(workflow_result['ad_variants'])} ad variants across {len(workflow_result['demographic_segments'])} segments")
        print("📱 Ready for swipe review interface...")

        # Step 4: Simulate swipe decisions (in production, this would be the actual swipe interface)
        approved_variants = await self._simulate_swipe_decisions(workflow_result['ad_variants'])

        # Step 5: Launch approved variants
        if approved_variants:
            print(f"🚀 Launching {len(approved_variants)} approved variants...")
            launch_result = await self.campaign_manager.launch_approved_variants(
                approved_variants,
                workflow_result['business_profile']
            )

            # Step 6: Start evolution monitoring
            if launch_result["success"]:
                print("🧬 Starting agentic evolution monitoring...")
                await self._start_evolution_monitoring(approved_variants, workflow_result['business_profile'])

            return {
                "workflow_result": workflow_result,
                "approved_variants": len(approved_variants),
                "launch_result": launch_result,
                "evolution_started": launch_result["success"]
            }
        else:
            print("❌ No variants approved for launch")
            return {
                "workflow_result": workflow_result,
                "approved_variants": 0,
                "launch_result": {"success": False, "error": "No approved variants"},
                "evolution_started": False
            }

    async def _conduct_voice_onboarding(self) -> Dict:
        """Conduct voice-based onboarding simulation"""

        # Simulate voice interaction stages
        stages = [
            {
                "stage": "greeting",
                "user_response": "Hi, I run TechFlow Solutions, we make project management software for small teams"
            },
            {
                "stage": "engagement_goals",
                "user_response": "We want to drive sales and get more customers to try our software"
            },
            {
                "stage": "budget_discussion",
                "user_response": "Our monthly ad budget is around $8000"
            },
            {
                "stage": "audience_discovery",
                "user_response": "Our ideal customers are small business owners, team leaders, and project managers aged 25-45 who struggle with team coordination"
            },
            {
                "stage": "brand_themes",
                "user_response": "We want to emphasize efficiency, simplicity, and team collaboration. Avoid anything too technical or overwhelming"
            }
        ]

        # Process each stage
        extracted_data = {}
        for stage_data in stages:
            result = await self.voice_agent.execute({
                "current_stage": stage_data["stage"],
                "user_response": stage_data["user_response"]
            })

            if result.get("extracted_data"):
                extracted_data.update(result["extracted_data"])

        # Combine all extracted data
        final_extracted_data = {
            "business_name": "TechFlow Solutions",
            "industry": "Software",
            "goal": "sales",
            "monthly_budget": 8000,
            "target_audience": {
                "description": "Small business owners, team leaders, project managers",
                "age_range": [25, 45],
                "pain_points": ["team coordination", "project management"]
            },
            "brand_themes": {
                "allowed": ["efficiency", "simplicity", "collaboration"],
                "disallowed": ["technical", "overwhelming"]
            }
        }

        return {
            "extracted_data": final_extracted_data,
            "voice_preferences": {"tone": "professional", "style": "friendly"}
        }

    async def _simulate_swipe_decisions(self, variants: List[AdVariantMorph]) -> List[AdVariantMorph]:
        """Simulate swipe decisions for demo purposes"""

        print("📱 Simulating marketing director swipe decisions...")

        approved_variants = []

        for i, variant in enumerate(variants):
            # Simulate decision based on scores
            combined_score = (variant.aesthetic_score + variant.ogilvy_score + variant.emotional_impact) / 3

            if combined_score > 0.75:
                decision = "approve"
                approved_variants.append(variant)
            elif combined_score > 0.6:
                decision = "approve" if i % 2 == 0 else "regenerate"  # Approve every other
                if decision == "approve":
                    approved_variants.append(variant)
            else:
                decision = "reject"

            print(f"   Variant {i+1}: '{variant.headline[:30]}...' -> {decision.upper()}")
            variant.swipe_status = decision

        print(f"✅ {len(approved_variants)} variants approved for launch")
        return approved_variants

    async def _start_evolution_monitoring(self, variants: List[AdVariantMorph], business_profile: BusinessProfile):
        """Start the agentic evolution monitoring"""

        self.evolution_monitor = EvolutionMonitor(self.orchestrator.evolution_orchestrator)

        # Start evolution cycle
        evolution_result = await self.orchestrator.evolution_orchestrator.start_evolution_cycle(
            variants, business_profile
        )

        print(f"🧬 Evolution cycle started - {evolution_result['mutations_created']} initial mutations created")

        # Start background monitoring (in production, this would run continuously)
        # For demo, we'll just show that it's started
        print("📊 Background evolution monitoring active...")

        return evolution_result
    
    async def _present_campaign_results(self, results: Dict):
        """Present campaign results to the client"""
        
        print("\n" + "="*60)
        print("🎉 YOUR ADVERTISING CAMPAIGN IS READY!")
        print("="*60)
        
        print(f"\n📊 CAMPAIGN OVERVIEW:")
        print(f"• Generated {len(results['variants'])} high-quality ad variants")
        print(f"• Average Ogilvy compliance score: {results['variants'][0].ogilvy_score:.1%}")
        print(f"• Average aesthetic score: {results['variants'][0].aesthetic_score:.1%}")
        
        print(f"\n✍️ BEST PERFORMING HEADLINES:")
        for i, variant in enumerate(results['variants'][:3], 1):
            print(f"{i}. {variant.headline}")
        
        print(f"\n🎨 VISUAL DIRECTION:")
        colors = results['visual_analysis']['color_palette']
        print(f"• Color palette: {colors['primary']} (primary), {colors['secondary']} (secondary)")
        print(f"• Layout style: {results['visual_analysis']['layouts'][0]['name']}")
        
        print(f"\n🔥 NEXT STEPS:")
        print("• Launch these ads across your preferred platforms")
        print("• I'll monitor performance and automatically optimize")
        print("• Expect to see improved engagement within 48 hours")
        
        print("\n" + "="*60)
    
    async def optimize_campaign(self, campaign_id: str, metrics: List[EngagementMetrics]) -> Dict:
        """Ongoing campaign optimization using AdMorph engine"""
        
        if campaign_id not in self.active_campaigns:
            return {"error": "Campaign not found"}
        
        # Analyze performance
        performance_insights = await self.morph_engine.analyze_performance(metrics)
        
        # Generate optimized variants
        current_variants = self.active_campaigns[campaign_id]["results"]["variants"]
        optimized_variants = await self.morph_engine.mutate_ads(current_variants, performance_insights)
        
        # Update campaign
        self.active_campaigns[campaign_id]["optimized_variants"] = optimized_variants
        
        return {
            "campaign_id": campaign_id,
            "performance_insights": performance_insights,
            "new_variants": len(optimized_variants),
            "optimization_timestamp": datetime.now().isoformat()
        }

# Example Usage & Demo
async def demo_ai_advertising_agency():
    """Demonstrate the complete AI advertising agency experience"""

    print("🚀 Initializing AI Advertising Agency...")
    print("Built on David Ogilvy's proven principles + Modern AI")
    print("Giving SMEs access to agency-level advertising intelligence\n")

    # Initialize the agency
    agency = AIAdvertisingAgency()

    # For demo purposes, create a sample brief instead of full onboarding
    sample_brief = DiscoveryBrief(
        id=str(uuid.uuid4()),
        product="Project Management Software for Small Teams",
        audience="Small business owners and team leaders",
        goal="sales",
        budget=5000,
        assets={"logoUrl": ""},
        unique_selling_proposition="The only project management tool that actually saves time instead of creating more work"
    )

    print("📋 Processing sample brief for Project Management Software...")

    # Process the brief through all agents
    results = await agency.orchestrator.process_brief(sample_brief)

    # Present results
    await agency._present_campaign_results(results)

    # Simulate performance data and optimization
    sample_metrics = [
        EngagementMetrics(
            variant_id=results["variants"][0].variant_id,
            impressions=10000,
            clicks=150,
            ctr=0.015,  # Low CTR
            conversions=8,
            engagement_rate=0.02,
            timestamp=datetime.now().isoformat(),
            cost_per_acquisition=45.0
        )
    ]

    print("\n🔄 Simulating performance optimization...")
    optimization_results = await agency.optimize_campaign(sample_brief.id, sample_metrics)
    print(f"✅ Generated {optimization_results['new_variants']} optimized variants")

    return results

async def demo_admorph_complete_workflow():
    """Demonstrate the complete AdMorph.AI workflow"""

    print("🎯 AdMorph.AI Complete Workflow Demo")
    print("=" * 60)
    print("From Voice Interaction → Demographic Analysis → Ad Generation → Swipe Review → Publishing → Evolution")
    print("=" * 60)

    # Initialize the enhanced agency
    agency = AIAdvertisingAgency()

    try:
        # Run the complete AdMorph workflow
        result = await agency.launch_admorph_campaign()

        print("\n" + "=" * 60)
        print("🎉 ADMORPH WORKFLOW COMPLETE!")
        print("=" * 60)

        print(f"✅ Business Profile Created: {result['workflow_result']['business_profile'].business_name}")
        print(f"✅ Demographic Segments: {len(result['workflow_result']['demographic_segments'])}")
        print(f"✅ Ad Variants Generated: {len(result['workflow_result']['ad_variants'])}")
        print(f"✅ Variants Approved: {result['approved_variants']}")
        print(f"✅ Campaign Launched: {result['launch_result']['success']}")
        print(f"✅ Evolution Started: {result['evolution_started']}")

        if result['launch_result']['success']:
            print(f"\n📊 Campaign Details:")
            print(f"   Campaign ID: {result['launch_result']['campaign_id']}")
            print(f"   Total Ads: {result['launch_result']['total_ads']}")
            print(f"   Estimated Reach: {result['launch_result']['estimated_reach']['estimated_monthly_reach']:,}")

        print("\n🧬 Agentic Evolution Features:")
        print("   • Continuous performance monitoring")
        print("   • Automatic trend analysis and adaptation")
        print("   • Real-time ad mutations based on performance")
        print("   • Emergency rollback capabilities")
        print("   • Synthetic data generation for testing")

        print("\n🎯 AdMorph.AI Integration Features:")
        print("   • Voice-based business onboarding")
        print("   • Demographic-specific ad generation")
        print("   • Tinder-style swipe review interface")
        print("   • Meta Marketing API integration")
        print("   • Ogilvy principles + AI-powered optimization")

        return result

    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("Note: This demo requires OpenAI API key and Meta API credentials")
        print("Set up your .env file with the required API keys to run the full demo")

        return {"error": str(e)}

async def demo_evolution_only():
    """Demonstrate just the agentic evolution system"""

    print("🧬 AdMorph.AI Agentic Evolution Demo")
    print("=" * 50)

    from agentic_evolution import demo_agentic_evolution

    try:
        result = await demo_agentic_evolution()
        return result
    except Exception as e:
        print(f"Evolution demo error: {e}")
        return {"error": str(e)}

# Run the demo
if __name__ == "__main__":
    print("🎯 AdMorph.AI - Advanced Agentic Advertising Framework")
    print("=" * 60)
    print("Choose a demo to run:")
    print("1. Complete AdMorph Workflow (Voice → Swipe → Publish → Evolve)")
    print("2. Original Ogilvy-based Agency Demo")
    print("3. Agentic Evolution System Only")
    print("=" * 60)

    import sys

    if len(sys.argv) > 1:
        demo_choice = sys.argv[1]
    else:
        demo_choice = input("Enter choice (1-3): ").strip()

    async def run_selected_demo():
        if demo_choice == "1":
            return await demo_admorph_complete_workflow()
        elif demo_choice == "2":
            return await demo_ai_advertising_agency()
        elif demo_choice == "3":
            return await demo_evolution_only()
        else:
            print("Invalid choice. Running complete AdMorph workflow...")
            return await demo_admorph_complete_workflow()

    # Run the selected demo
    import asyncio
    try:
        result = asyncio.run(run_selected_demo())
        print("\n✅ Demo completed successfully!")
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("\nNote: Make sure to:")
        print("1. Install requirements: pip install -r requirements.txt")
        print("2. Set up .env file with API keys (see .env.example)")
        print("3. Configure Meta Marketing API credentials")