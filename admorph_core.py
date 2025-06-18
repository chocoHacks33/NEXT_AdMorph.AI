"""
AdMorph.AI - Advanced AI Agentic Framework for Advertising
Integrates with existing coee.py framework and adds OpenAI-powered agents
"""

import asyncio
import json
import os
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod
from enum import Enum
import requests
from dotenv import load_dotenv
import numpy as np
import base64
from io import BytesIO
from PIL import Image

# Load environment variables
load_dotenv()

# Import base AdVariant from coee.py for compatibility
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

# Enhanced Data Models for AdMorph
@dataclass
class BusinessProfile:
    """Enhanced business profile from voice interaction"""
    business_id: str
    business_name: str
    industry: str
    target_engagement: str  # "awareness", "sales", "leads", "app_installs"
    monthly_budget: float
    target_audience: Dict[str, Any]  # Demographics, interests, behaviors
    brand_themes: Dict[str, List[str]]  # allowed/disallowed themes
    original_ad_assets: List[Dict[str, str]]  # uploaded images, videos, copy
    voice_preferences: Dict[str, str]  # tone, style preferences from voice
    created_at: str
    updated_at: str

@dataclass
class DemographicSegment:
    """Specific demographic segment for ad targeting"""
    segment_id: str
    name: str
    age_range: tuple
    gender: str
    interests: List[str]
    behaviors: List[str]
    location: str
    income_level: str
    education: str
    meta_targeting_spec: Dict[str, Any]

@dataclass
class AdVariantMorph(AdVariant):
    """Extended AdVariant with AdMorph capabilities"""
    demographic_segment: DemographicSegment
    generation_strategy: str
    mutation_history: List[Dict[str, Any]]
    performance_score: float
    trend_alignment: float
    meta_campaign_id: Optional[str] = None
    is_published: bool = False
    swipe_status: str = "pending"  # "pending", "approved", "rejected", "regenerate"

@dataclass
class SwipeDecision:
    """Marketing director's swipe decision"""
    variant_id: str
    decision: str  # "approve", "reject", "regenerate"
    feedback: Optional[str] = None
    timestamp: str = None

# OpenAI-Powered Base Agent
class OpenAIAgent(ABC):
    """Base class for OpenAI-powered agents"""
    
    def __init__(self, role: str, model: str = "gpt-4-turbo-preview", temperature: float = 0.7):
        self.role = role
        self.model = model
        self.temperature = temperature
        self.agent_id = str(uuid.uuid4())
        self.conversation_history = []
    
    async def _call_openai(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Make async call to OpenAI API using direct HTTP requests"""
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                return "Error: OpenAI API key not configured"

            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": self.model,
                "messages": messages,
                "temperature": kwargs.get('temperature', self.temperature),
                "max_tokens": kwargs.get('max_tokens', 500)
            }

            response = requests.post(url, headers=headers, json=data, timeout=30)

            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error: API returned {response.status_code}"

        except Exception as e:
            print(f"OpenAI API Error: {e}")
            return f"Error: Unable to process request - {str(e)}"
    
    def _build_system_prompt(self) -> str:
        """Build system prompt for the agent"""
        return f"You are an expert {self.role} with deep knowledge in advertising and marketing."
    
    @abstractmethod
    async def execute(self, input_data: Any, context: Dict = None) -> Dict:
        """Execute the agent's main function"""
        pass

# Voice Interface Agent
class AdMorphVoiceAgent(OpenAIAgent):
    """Intelligent voice/chat interface for business onboarding"""
    
    def __init__(self):
        super().__init__("Voice Interface Specialist", temperature=0.8)
        self.onboarding_flow = self._design_voice_flow()
    
    def _design_voice_flow(self) -> List[Dict[str, str]]:
        """Design conversational flow for business onboarding"""
        return [
            {
                "stage": "greeting",
                "prompt": "Welcome to AdMorph.AI! I'm your AI marketing consultant. I'll help you create ads that adapt and evolve automatically. What's your business name and what do you sell?"
            },
            {
                "stage": "engagement_goals",
                "prompt": "Great! Now, what's your primary goal with advertising? Are you looking to increase brand awareness, drive sales, generate leads, or get app downloads?"
            },
            {
                "stage": "budget_discussion",
                "prompt": "Perfect. What's your monthly advertising budget? This helps me recommend the right strategy and platform mix."
            },
            {
                "stage": "audience_discovery",
                "prompt": "Who is your ideal customer? Tell me about their age, interests, location, and what problems your product solves for them."
            },
            {
                "stage": "brand_themes",
                "prompt": "What themes or messages should your ads always include? And are there any topics or approaches you want to avoid?"
            },
            {
                "stage": "asset_collection",
                "prompt": "Do you have any existing ads, images, or marketing materials you'd like me to use as a starting point? You can upload them now."
            }
        ]
    
    async def execute(self, input_data: Dict, context: Dict = None) -> Dict:
        """Conduct intelligent voice-based onboarding"""
        
        if input_data.get("stage") == "start":
            return await self._start_onboarding()
        
        stage = input_data.get("current_stage", "greeting")
        user_response = input_data.get("user_response", "")
        
        return await self._process_stage_response(stage, user_response)
    
    async def _start_onboarding(self) -> Dict:
        """Start the onboarding process"""
        first_stage = self.onboarding_flow[0]
        return {
            "stage": first_stage["stage"],
            "message": first_stage["prompt"],
            "next_stage": "engagement_goals",
            "progress": 1,
            "total_stages": len(self.onboarding_flow)
        }
    
    async def _process_stage_response(self, stage: str, user_response: str) -> Dict:
        """Process user response and move to next stage"""
        
        # Build context-aware prompt
        system_prompt = f"""
        You are an expert marketing consultant conducting a business onboarding interview.
        Current stage: {stage}
        User response: {user_response}
        
        Your task:
        1. Acknowledge and validate their response
        2. Extract key business information
        3. Ask intelligent follow-up questions if needed
        4. Provide the next stage prompt when ready
        
        Be conversational, professional, and insightful. Show that you understand their business.
        """
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_response}
        ]
        
        ai_response = await self._call_openai(messages)
        
        # Determine next stage
        stage_index = next((i for i, s in enumerate(self.onboarding_flow) if s["stage"] == stage), 0)
        next_stage_index = min(stage_index + 1, len(self.onboarding_flow) - 1)
        next_stage = self.onboarding_flow[next_stage_index]["stage"] if next_stage_index < len(self.onboarding_flow) else "complete"
        
        return {
            "stage": stage,
            "ai_response": ai_response,
            "next_stage": next_stage,
            "progress": stage_index + 1,
            "total_stages": len(self.onboarding_flow),
            "extracted_data": await self._extract_business_data(stage, user_response)
        }
    
    async def _extract_business_data(self, stage: str, response: str) -> Dict:
        """Extract structured business data from user response"""
        
        extraction_prompt = f"""
        Extract structured business information from this user response for stage '{stage}':
        Response: {response}
        
        Return a JSON object with relevant fields for this stage.
        For example:
        - greeting stage: {{"business_name": "...", "product_type": "...", "industry": "..."}}
        - budget stage: {{"monthly_budget": number, "budget_flexibility": "..."}}
        - audience stage: {{"demographics": {{}}, "interests": [], "pain_points": []}}
        
        Only include fields you can confidently extract. Return empty object if unclear.
        """
        
        messages = [
            {"role": "system", "content": "You are a data extraction specialist. Return only valid JSON."},
            {"role": "user", "content": extraction_prompt}
        ]
        
        try:
            response = await self._call_openai(messages, temperature=0.1)
            return json.loads(response)
        except:
            return {}

# Demographic Analysis Agent
class DemographicAnalysisAgent(OpenAIAgent):
    """Analyzes business profile and creates demographic segments"""

    def __init__(self):
        super().__init__("Demographic Analysis Specialist", temperature=0.3)
        self.meta_demographics = self._load_meta_targeting_options()

    def _load_meta_targeting_options(self) -> Dict:
        """Load Meta's targeting capabilities"""
        return {
            "age_ranges": [(18, 24), (25, 34), (35, 44), (45, 54), (55, 64), (65, 99)],
            "interests": [
                "Technology", "Fashion", "Health & Fitness", "Travel", "Food & Dining",
                "Business", "Education", "Entertainment", "Sports", "Home & Garden",
                "Automotive", "Finance", "Parenting", "Gaming", "Art & Culture"
            ],
            "behaviors": [
                "Online shoppers", "Frequent travelers", "Small business owners",
                "New parents", "College graduates", "Mobile device users",
                "Social media enthusiasts", "Early technology adopters"
            ],
            "income_levels": ["Low", "Middle", "High", "Top 10%"],
            "education": ["High School", "Some College", "Bachelor's", "Graduate"]
        }

    async def execute(self, business_profile: BusinessProfile, context: Dict = None) -> Dict:
        """Generate demographic segments for the business"""

        # Analyze business and create segments
        segments = await self._generate_demographic_segments(business_profile)

        # Create Meta targeting specifications
        meta_specs = await self._create_meta_targeting_specs(segments)

        return {
            "business_id": business_profile.business_id,
            "demographic_segments": segments,
            "meta_targeting_specs": meta_specs,
            "total_segments": len(segments),
            "estimated_reach": await self._estimate_total_reach(segments)
        }

    async def _generate_demographic_segments(self, profile: BusinessProfile) -> List[DemographicSegment]:
        """Generate relevant demographic segments"""

        analysis_prompt = f"""
        Analyze this business profile and create 3-5 distinct demographic segments for advertising:

        Business: {profile.business_name}
        Industry: {profile.industry}
        Target Audience: {profile.target_audience}
        Budget: ${profile.monthly_budget}

        For each segment, define:
        1. Segment name and description
        2. Age range
        3. Gender preference
        4. Key interests
        5. Behaviors
        6. Income level
        7. Education level

        Make segments distinct and strategically different to maximize ad performance.
        Return as JSON array.
        """

        messages = [
            {"role": "system", "content": "You are a demographic targeting expert. Create distinct, high-value audience segments."},
            {"role": "user", "content": analysis_prompt}
        ]

        try:
            response = await self._call_openai(messages, temperature=0.3)
            segments_data = json.loads(response)

            segments = []
            for i, seg_data in enumerate(segments_data):
                segment = DemographicSegment(
                    segment_id=str(uuid.uuid4()),
                    name=seg_data.get("name", f"Segment {i+1}"),
                    age_range=tuple(seg_data.get("age_range", [25, 45])),
                    gender=seg_data.get("gender", "all"),
                    interests=seg_data.get("interests", []),
                    behaviors=seg_data.get("behaviors", []),
                    location=seg_data.get("location", "United States"),
                    income_level=seg_data.get("income_level", "Middle"),
                    education=seg_data.get("education", "Bachelor's"),
                    meta_targeting_spec={}
                )
                segments.append(segment)

            return segments

        except Exception as e:
            print(f"Error generating segments: {e}")
            return self._create_default_segments()

    def _create_default_segments(self) -> List[DemographicSegment]:
        """Create default segments if AI generation fails"""
        return [
            DemographicSegment(
                segment_id=str(uuid.uuid4()),
                name="Young Professionals",
                age_range=(25, 35),
                gender="all",
                interests=["Technology", "Business", "Career"],
                behaviors=["Online shoppers", "Early adopters"],
                location="United States",
                income_level="Middle",
                education="Bachelor's",
                meta_targeting_spec={}
            ),
            DemographicSegment(
                segment_id=str(uuid.uuid4()),
                name="Established Adults",
                age_range=(35, 50),
                gender="all",
                interests=["Family", "Home", "Finance"],
                behaviors=["Homeowners", "Parents"],
                location="United States",
                income_level="High",
                education="Bachelor's",
                meta_targeting_spec={}
            )
        ]

    async def _create_meta_targeting_specs(self, segments: List[DemographicSegment]) -> Dict:
        """Create Meta API targeting specifications"""
        specs = {}

        for segment in segments:
            specs[segment.segment_id] = {
                "age_min": segment.age_range[0],
                "age_max": segment.age_range[1],
                "genders": [1, 2] if segment.gender == "all" else ([1] if segment.gender == "male" else [2]),
                "interests": segment.interests,
                "behaviors": segment.behaviors,
                "geo_locations": {"countries": ["US"]},
                "income": segment.income_level,
                "education_statuses": [segment.education]
            }

        return specs

    async def _estimate_total_reach(self, segments: List[DemographicSegment]) -> int:
        """Estimate total potential reach across all segments"""
        # Simplified estimation - in production, use Meta's reach estimation API
        base_reach_per_segment = 100000
        return len(segments) * base_reach_per_segment

# Ad Variant Generation Agent
class AdVariantGenerationAgent(OpenAIAgent):
    """Generates ad variants for each demographic segment"""

    def __init__(self):
        super().__init__("Ad Variant Generation Specialist", temperature=0.8)

    async def execute(self, business_profile: BusinessProfile, segments: List[DemographicSegment], context: Dict = None) -> Dict:
        """Generate ad variants for each demographic segment"""

        all_variants = []
        generation_insights = {}

        for segment in segments:
            variants = await self._generate_variants_for_segment(business_profile, segment)
            all_variants.extend(variants)
            generation_insights[segment.segment_id] = {
                "segment_name": segment.name,
                "variants_generated": len(variants),
                "strategy": await self._get_generation_strategy(segment)
            }

        return {
            "business_id": business_profile.business_id,
            "total_variants": len(all_variants),
            "variants": all_variants,
            "generation_insights": generation_insights,
            "created_at": datetime.now().isoformat()
        }

    async def _generate_variants_for_segment(self, profile: BusinessProfile, segment: DemographicSegment) -> List[AdVariantMorph]:
        """Generate 2-3 ad variants for a specific demographic segment"""

        generation_prompt = f"""
        Create 3 distinct ad variants for this demographic segment:

        Business: {profile.business_name} ({profile.industry})
        Product/Service: {profile.target_audience}
        Budget: ${profile.monthly_budget}
        Brand Themes: {profile.brand_themes}

        Target Segment: {segment.name}
        - Age: {segment.age_range[0]}-{segment.age_range[1]}
        - Interests: {', '.join(segment.interests)}
        - Behaviors: {', '.join(segment.behaviors)}
        - Income: {segment.income_level}

        For each variant, create:
        1. Compelling headline (max 40 chars for mobile)
        2. Engaging body copy (max 125 chars)
        3. Strong call-to-action
        4. Image concept description
        5. Emotional hook specific to this demographic

        Make each variant distinctly different in approach while staying true to the brand.
        Return as JSON array with fields: headline, body, cta, image_concept, emotional_hook, strategy.
        """

        messages = [
            {"role": "system", "content": "You are an expert ad copywriter specializing in demographic-specific messaging."},
            {"role": "user", "content": generation_prompt}
        ]

        try:
            response = await self._call_openai(messages, temperature=0.8)
            variants_data = json.loads(response)

            variants = []
            for i, variant_data in enumerate(variants_data):
                variant = AdVariantMorph(
                    variant_id=str(uuid.uuid4()),
                    headline=variant_data.get("headline", ""),
                    body=variant_data.get("body", ""),
                    cta=variant_data.get("cta", "Learn More"),
                    image_url="",  # Will be generated later
                    aesthetic_score=0.8,  # Default score
                    ogilvy_score=0.8,  # Default score
                    emotional_impact=0.8,  # Default score
                    format_type="social",
                    demographic_segment=segment,
                    generation_strategy=variant_data.get("strategy", "demographic_targeted"),
                    mutation_history=[],
                    performance_score=0.0,
                    trend_alignment=0.0,
                    swipe_status="pending"
                )
                variants.append(variant)

            return variants

        except Exception as e:
            print(f"Error generating variants for segment {segment.name}: {e}")
            return self._create_default_variants(profile, segment)

    def _create_default_variants(self, profile: BusinessProfile, segment: DemographicSegment) -> List[AdVariantMorph]:
        """Create default variants if AI generation fails"""
        return [
            AdVariantMorph(
                variant_id=str(uuid.uuid4()),
                headline=f"Perfect for {segment.name}",
                body=f"Discover why {profile.business_name} is the choice for {segment.interests[0] if segment.interests else 'smart people'}.",
                cta="Learn More",
                image_url="",
                aesthetic_score=0.7,
                ogilvy_score=0.7,
                emotional_impact=0.7,
                format_type="social",
                demographic_segment=segment,
                generation_strategy="default",
                mutation_history=[],
                performance_score=0.0,
                trend_alignment=0.0,
                swipe_status="pending"
            )
        ]

    async def _get_generation_strategy(self, segment: DemographicSegment) -> str:
        """Determine the generation strategy used for this segment"""
        if segment.age_range[1] <= 30:
            return "youth_focused_trendy"
        elif segment.income_level in ["High", "Top 10%"]:
            return "premium_value_proposition"
        elif "parents" in [b.lower() for b in segment.behaviors]:
            return "family_oriented"
        else:
            return "general_appeal"
