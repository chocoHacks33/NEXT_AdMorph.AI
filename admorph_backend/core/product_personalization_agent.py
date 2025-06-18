"""
Product Personalization Agent for E-commerce
"""

import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime

from .base_agent import OpenAIAgent
from ..models.products import BaseProduct, ProductVariant, PersonalizationRequest, PersonalizationResult
from ..models.demographics import DemographicSegment


class ProductPersonalizationAgent(OpenAIAgent):
    """AI agent that personalizes product listings for different demographics"""
    
    def __init__(self):
        super().__init__("ProductPersonalizationAgent", model="gpt-4.1")
        self.personalization_principles = [
            "Match language and tone to demographic preferences",
            "Highlight features most relevant to the target audience",
            "Use appropriate price positioning and value messaging",
            "Create urgency and social proof relevant to the demographic",
            "Optimize for platform-specific conversion patterns",
            "Ensure brand consistency while maximizing personalization"
        ]
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute product personalization for given context"""
        try:
            personalization_request = context.get("personalization_request")
            base_product = context.get("base_product")
            
            if not personalization_request or not base_product:
                return {"success": False, "error": "Missing required context"}
            
            # Generate personalized variants for each demographic
            variants = []
            insights = {}
            
            for demographic in personalization_request.target_demographics:
                variant = await self._generate_product_variant(
                    base_product, demographic, personalization_request
                )
                variants.append(variant)
                
                # Generate insights for this demographic
                demographic_insights = await self._analyze_demographic_preferences(
                    demographic, base_product
                )
                insights[demographic.segment_id] = demographic_insights
            
            # Generate A/B testing recommendations
            ab_recommendations = await self._generate_ab_test_recommendations(variants)
            
            # Estimate performance lift
            performance_lift = await self._estimate_performance_lift(base_product, variants)
            
            result = PersonalizationResult(
                request_id=personalization_request.request_id,
                product_id=base_product.product_id,
                generated_variants=variants,
                personalization_insights=insights,
                a_b_test_recommendations=ab_recommendations,
                estimated_performance_lift=performance_lift,
                processing_time=2.5,  # Mock processing time
                generated_at=datetime.now().isoformat()
            )
            
            self.log_execution(context, {"success": True, "variants_generated": len(variants)})
            return {"success": True, "result": result}
            
        except Exception as e:
            error_result = {"success": False, "error": str(e)}
            self.log_execution(context, error_result)
            return error_result
    
    async def _generate_product_variant(
        self, 
        base_product: BaseProduct, 
        demographic: DemographicSegment,
        request: PersonalizationRequest
    ) -> ProductVariant:
        """Generate personalized product variant for specific demographic"""
        
        # Create personalization prompt
        prompt = self._create_personalization_prompt(base_product, demographic, request)
        
        # Get AI response
        messages = [
            self._create_system_message(self._get_personalization_system_prompt()),
            self._create_user_message(prompt)
        ]
        
        response = await self._call_openai(messages, temperature=0.8)
        
        # Parse the response
        try:
            variant_data = self._parse_json_response(response)
        except:
            # Fallback if JSON parsing fails
            variant_data = self._create_fallback_variant(base_product, demographic)
        
        # Create ProductVariant object
        variant = ProductVariant(
            variant_id=str(uuid.uuid4()),
            product_id=base_product.product_id,
            demographic_segment=demographic,
            personalized_title=variant_data.get("title", base_product.name),
            personalized_description=variant_data.get("description", ""),
            highlighted_features=variant_data.get("highlighted_features", base_product.features[:3]),
            price_positioning=variant_data.get("price_positioning", "value"),
            image_prompts=variant_data.get("image_prompts", []),
            generated_images=[],  # Will be populated by image generation service
            call_to_action=variant_data.get("call_to_action", "Buy Now"),
            urgency_messaging=variant_data.get("urgency_messaging"),
            social_proof=variant_data.get("social_proof"),
            personalization_score=variant_data.get("personalization_score", 0.8)
        )
        
        return variant
    
    def _create_personalization_prompt(
        self, 
        product: BaseProduct, 
        demographic: DemographicSegment,
        request: PersonalizationRequest
    ) -> str:
        """Create prompt for product personalization"""
        
        return f"""
        Create a highly personalized, conversion-optimized product listing that speaks directly to this specific demographic's motivations, desires, and pain points.

        📦 PRODUCT ANALYSIS:
        Product: {product.name}
        Category: {product.category} | Brand: {product.brand} | Price: ${product.base_price}

        Core Features: {', '.join(product.features)}
        Technical Specs: {json.dumps(product.specifications, indent=2)}

        👤 DEMOGRAPHIC DEEP DIVE:
        Target: {demographic.name} ({demographic.age_range[0]}-{demographic.age_range[1]} years old)
        Profile: {demographic.gender} | {demographic.location} | {demographic.income_level} income | {demographic.education} education

        Core Interests: {', '.join(demographic.interests)}
        Key Behaviors: {', '.join(demographic.behaviors)}

        🎯 PERSONALIZATION MISSION:
        Goals: {', '.join(request.personalization_goals)}
        Platform: {request.platform_context}
        Brand Voice: {json.dumps(request.brand_guidelines, indent=2) if request.brand_guidelines else "Authentic and engaging"}
        Context: {request.seasonal_context or "Year-round appeal"}

        🧠 PSYCHOLOGICAL INSIGHTS TO LEVERAGE:

        For {demographic.name}:
        - What are their primary motivations and pain points?
        - What language style resonates (casual/professional/technical)?
        - What benefits matter most to their lifestyle?
        - What social proof would they trust?
        - What urgency/scarcity would motivate them?
        - How do they prefer to make purchase decisions?

        ✍️ COPYWRITING REQUIREMENTS:

        1. TITLE: Create a magnetic headline that immediately signals "this is for YOU"
           - Use power words that resonate with this demographic
           - Lead with the primary benefit they care about most
           - Make it feel exclusive and personally relevant

        2. DESCRIPTION: Write compelling copy that:
           - Opens with an emotional hook that addresses their specific situation
           - Transforms features into benefits that matter to THEIR life
           - Uses language and tone that matches their communication style
           - Tells a micro-story they can see themselves in
           - Addresses potential objections specific to this demographic
           - Ends with a compelling reason to act now

        3. FEATURES: Select and reframe the 3 most relevant features as benefits
           - Focus on outcomes, not specifications
           - Use language that resonates with their interests
           - Connect to their specific use cases and lifestyle

        4. POSITIONING: Choose the value proposition that matches their mindset
           - Consider their income level and spending psychology
           - Match their decision-making criteria (quality vs price vs innovation)

        5. SOCIAL PROOF: Create credibility that this demographic would trust
           - Use sources and testimonials they'd relate to
           - Reference communities or authorities they respect

        6. URGENCY: Design scarcity that motivates without feeling manipulative
           - Use time-sensitive offers that align with their behavior patterns
           - Create FOMO that feels authentic to their interests

        Return ONLY valid JSON with this exact structure:
        {{
            "title": "Irresistible product title that screams 'this is for me' (max 60 chars)",
            "description": "Emotionally compelling description that transforms features into lifestyle benefits (150-200 words)",
            "highlighted_features": ["Benefit 1 (not feature)", "Benefit 2 (not feature)", "Benefit 3 (not feature)"],
            "price_positioning": "value|premium|budget|performance",
            "call_to_action": "Action-oriented CTA that matches their motivation",
            "urgency_messaging": "Time-sensitive message that creates authentic urgency",
            "social_proof": "Credible social proof this demographic would trust",
            "image_prompts": ["Lifestyle image prompt showing this demographic using the product", "Detail/feature image prompt highlighting key benefit"],
            "personalization_score": 0.90,
            "reasoning": "Strategic explanation of why these choices will resonate with this specific demographic"
        }}
        """
    
    def _get_personalization_system_prompt(self) -> str:
        """Get enhanced system prompt for high-quality personalization"""
        return """
        You are an elite e-commerce personalization specialist with expertise in:

        🧠 CONSUMER PSYCHOLOGY:
        - Deep understanding of demographic motivations, pain points, and desires
        - Behavioral triggers that drive purchase decisions
        - Emotional resonance and psychological persuasion techniques
        - Cultural nuances and generational preferences

        ✍️ COPYWRITING MASTERY:
        - David Ogilvy's advertising principles
        - Persuasive writing techniques that convert
        - Benefit-focused messaging over feature lists
        - Storytelling that creates emotional connection
        - Power words and psychological triggers

        🎯 CONVERSION OPTIMIZATION:
        - A/B tested messaging strategies
        - Platform-specific best practices (Amazon, Shopify, etc.)
        - Mobile-first copywriting approaches
        - Urgency and scarcity psychology
        - Social proof integration

        📊 DEMOGRAPHIC EXPERTISE:
        - Age-specific communication styles and preferences
        - Income-based value proposition positioning
        - Interest-driven feature prioritization
        - Lifestyle-aligned messaging and tone
        - Education-level appropriate language complexity

        🎨 BRAND VOICE ADAPTATION:
        - Maintaining brand consistency while personalizing
        - Tone modulation for different audiences
        - Cultural sensitivity and inclusivity
        - Premium vs. accessible positioning

        CORE PRINCIPLES:
        1. Lead with benefits, support with features
        2. Create emotional connection before logical justification
        3. Use specific, concrete language over generic claims
        4. Address the demographic's specific pain points
        5. Match the language style to the audience's preferences
        6. Include relevant social proof and urgency
        7. Craft CTAs that resonate with the demographic's motivations

        Your mission: Create product listings that feel like they were written specifically for each individual customer, maximizing both engagement and conversion while maintaining authenticity and brand integrity.

        Always respond with valid JSON and focus on creating genuinely compelling, nuanced copy that speaks directly to the target demographic's heart and mind.
        """
    
    def _create_fallback_variant(self, product: BaseProduct, demographic: DemographicSegment) -> Dict[str, Any]:
        """Create fallback variant if AI generation fails"""
        return {
            "title": f"{product.name} - Perfect for {demographic.name}",
            "description": f"Discover the perfect {product.category.lower()} designed with {demographic.name.lower()} in mind. {product.name} combines quality, performance, and value.",
            "highlighted_features": product.features[:3],
            "price_positioning": "value",
            "call_to_action": "Shop Now",
            "urgency_messaging": "Limited time offer",
            "social_proof": "Trusted by thousands of customers",
            "image_prompts": [
                f"Professional product photo of {product.name} in clean, modern setting",
                f"{product.name} being used by {demographic.name.lower()} in lifestyle context"
            ],
            "personalization_score": 0.6,
            "reasoning": "Fallback personalization due to AI generation error"
        }
    
    async def _analyze_demographic_preferences(
        self, 
        demographic: DemographicSegment, 
        product: BaseProduct
    ) -> Dict[str, Any]:
        """Analyze demographic preferences for insights"""
        
        # Mock analysis - in production, this would use more sophisticated AI
        preferences = {
            "preferred_language_style": "casual" if demographic.age_range[1] < 35 else "professional",
            "key_motivators": demographic.interests[:2],
            "price_sensitivity": "high" if demographic.income_level in ["Low", "Middle"] else "low",
            "decision_factors": ["quality", "price", "reviews"],
            "preferred_social_proof": "peer_reviews" if demographic.age_range[1] < 40 else "expert_endorsements",
            "urgency_responsiveness": "high" if "Early adopters" in demographic.behaviors else "medium"
        }
        
        return preferences
    
    async def _generate_ab_test_recommendations(self, variants: List[ProductVariant]) -> List[Dict[str, Any]]:
        """Generate A/B testing recommendations"""
        
        recommendations = []
        
        if len(variants) >= 2:
            recommendations.append({
                "test_type": "title_comparison",
                "variants": [v.variant_id for v in variants[:2]],
                "metric": "click_through_rate",
                "duration_days": 14,
                "traffic_split": 50
            })
            
            recommendations.append({
                "test_type": "price_positioning",
                "variants": [v.variant_id for v in variants if v.price_positioning != "value"],
                "metric": "conversion_rate",
                "duration_days": 21,
                "traffic_split": 30
            })
        
        return recommendations
    
    async def _estimate_performance_lift(
        self, 
        base_product: BaseProduct, 
        variants: List[ProductVariant]
    ) -> float:
        """Estimate performance lift from personalization"""
        
        # Mock calculation based on personalization scores
        avg_personalization_score = sum(v.personalization_score for v in variants) / len(variants)
        
        # Estimate lift based on industry benchmarks
        # Higher personalization scores typically lead to 15-40% conversion lift
        estimated_lift = (avg_personalization_score - 0.5) * 0.6  # 0.5 baseline, up to 60% lift
        
        return max(0.0, min(estimated_lift, 0.4))  # Cap at 40% lift
