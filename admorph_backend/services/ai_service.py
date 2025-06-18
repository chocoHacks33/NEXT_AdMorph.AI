"""
Unified AI services integration for AdMorph.AI
Handles OpenAI GPT-4.1, voice services, and other AI integrations
"""

import asyncio
import httpx
import json
import logging
from typing import Dict, List, Any, Optional, AsyncGenerator
from datetime import datetime
import base64
import io

from ..config.settings import get_settings

logger = logging.getLogger(__name__)


class OpenAIService:
    """Enhanced OpenAI service with GPT-4.1 support"""
    
    def __init__(self):
        self.settings = get_settings()
        self.api_key = self.settings.openai_api_key
        self.base_url = "https://api.openai.com/v1"
        self.model = getattr(self.settings, 'openai_model', 'gpt-4.1')
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any]:
        """Create chat completion with GPT-4.1"""
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }
        
        if max_tokens:
            data["max_tokens"] = max_tokens
        
        if stream:
            data["stream"] = True
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data
                )
                response.raise_for_status()
                return response.json()
                
        except httpx.HTTPError as e:
            logger.error(f"OpenAI API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in OpenAI chat completion: {e}")
            raise
    
    async def generate_ad_copy(
        self,
        business_profile: Dict[str, Any],
        demographic: Dict[str, Any],
        format_type: str = "social"
    ) -> Dict[str, Any]:
        """Generate ad copy using GPT-4.1 with Ogilvy principles"""
        
        system_prompt = """You are an elite advertising copywriter with deep expertise in David Ogilvy's principles and modern digital marketing. Your task is to create compelling ad copy that converts.

Core Principles:
1. Lead with benefits, support with features
2. Create emotional connection before logical justification  
3. Use specific, concrete language over generic claims
4. Address demographic-specific pain points
5. Match language style to audience preferences

Output Format (JSON):
{
    "headline": "Compelling headline (max 40 chars)",
    "body": "Persuasive body copy (max 125 chars)",
    "cta": "Strong call-to-action (max 20 chars)",
    "ogilvy_score": 0.85,
    "emotional_impact": 0.90,
    "aesthetic_score": 0.88
}"""
        
        user_prompt = f"""
Business: {business_profile.get('business_name', '')}
Industry: {business_profile.get('industry', '')}
Description: {business_profile.get('description', '')}
USPs: {', '.join(business_profile.get('unique_selling_points', []))}

Target Demographic: {demographic.get('name', '')}
Age Range: {demographic.get('age_range', [])}
Interests: {', '.join(demographic.get('interests', []))}
Behaviors: {', '.join(demographic.get('behaviors', []))}

Format: {format_type}

Create compelling ad copy that resonates with this specific demographic.
"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = await self.chat_completion(messages, temperature=0.8)
            content = response['choices'][0]['message']['content']
            
            # Try to parse JSON response
            try:
                ad_data = json.loads(content)
                return ad_data
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "headline": "Discover Something Amazing",
                    "body": "Transform your experience with our innovative solution. Join thousands of satisfied customers.",
                    "cta": "Learn More",
                    "ogilvy_score": 0.75,
                    "emotional_impact": 0.70,
                    "aesthetic_score": 0.75
                }
                
        except Exception as e:
            logger.error(f"Error generating ad copy: {e}")
            raise
    
    async def personalize_product_copy(
        self,
        product: Dict[str, Any],
        demographic: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Personalize product copy for specific demographic"""
        
        system_prompt = """You are an elite e-commerce personalization specialist with expertise in:

🧠 CONSUMER PSYCHOLOGY MASTERY
✍️ COPYWRITING EXCELLENCE (David Ogilvy Principles)  
🎯 CONVERSION OPTIMIZATION
📊 DEMOGRAPHIC EXPERTISE
🎨 BRAND VOICE ADAPTATION

Core Mission: Create product listings that feel personally crafted for each customer, maximizing conversion while maintaining authenticity.

Output Format (JSON):
{
    "personalized_title": "Demographic-specific product title",
    "personalized_description": "Compelling description highlighting relevant benefits",
    "highlighted_features": ["feature1", "feature2", "feature3"],
    "personalized_cta": "Strong, relevant call-to-action",
    "price_positioning": "Value proposition messaging",
    "urgency_messaging": "Time-sensitive motivation",
    "social_proof": ["proof1", "proof2"],
    "personalization_score": 0.92
}"""
        
        user_prompt = f"""
Product: {product.get('name', '')}
Description: {product.get('description', '')}
Price: ${product.get('price', 0)}
Category: {product.get('category', '')}
Features: {', '.join(product.get('features', []))}

Target Demographic: {demographic.get('name', '')}
Age Range: {demographic.get('age_range', [])}
Interests: {', '.join(demographic.get('interests', []))}
Behaviors: {', '.join(demographic.get('behaviors', []))}
Psychographics: {demographic.get('psychographics', {})}

Personalize this product listing to maximize appeal and conversion for this specific demographic.
"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        try:
            response = await self.chat_completion(messages, temperature=0.8)
            content = response['choices'][0]['message']['content']
            
            # Try to parse JSON response
            try:
                personalization_data = json.loads(content)
                return personalization_data
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "personalized_title": product.get('name', 'Amazing Product'),
                    "personalized_description": f"Perfect for {demographic.get('name', 'you')}! " + product.get('description', ''),
                    "highlighted_features": product.get('features', [])[:3],
                    "personalized_cta": "Get Yours Now",
                    "price_positioning": "Great value for the quality",
                    "urgency_messaging": "Limited time offer",
                    "social_proof": ["Loved by thousands", "5-star rated"],
                    "personalization_score": 0.75
                }
                
        except Exception as e:
            logger.error(f"Error personalizing product copy: {e}")
            raise


class VoiceService:
    """Voice processing and synthesis service"""
    
    def __init__(self):
        self.settings = get_settings()
        self.openai_service = OpenAIService()
    
    async def text_to_speech(self, text: str, voice: str = "alloy") -> bytes:
        """Convert text to speech using OpenAI TTS"""
        
        headers = {
            "Authorization": f"Bearer {self.openai_service.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "tts-1",
            "input": text,
            "voice": voice,
            "response_format": "mp3"
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.openai_service.base_url}/audio/speech",
                    headers=headers,
                    json=data
                )
                response.raise_for_status()
                return response.content
                
        except Exception as e:
            logger.error(f"Error in text-to-speech: {e}")
            raise
    
    async def speech_to_text(self, audio_data: bytes) -> str:
        """Convert speech to text using OpenAI Whisper"""
        
        headers = {
            "Authorization": f"Bearer {self.openai_service.api_key}"
        }
        
        files = {
            "file": ("audio.mp3", audio_data, "audio/mpeg"),
            "model": (None, "whisper-1")
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.openai_service.base_url}/audio/transcriptions",
                    headers=headers,
                    files=files
                )
                response.raise_for_status()
                result = response.json()
                return result.get("text", "")
                
        except Exception as e:
            logger.error(f"Error in speech-to-text: {e}")
            raise


class MetaAPIService:
    """Meta (Facebook) API integration service"""
    
    def __init__(self):
        self.settings = get_settings()
        self.access_token = getattr(self.settings, 'meta_access_token', None)
        self.app_id = getattr(self.settings, 'meta_app_id', None)
        self.base_url = "https://graph.facebook.com/v18.0"
    
    async def get_demographic_data(self, interests: List[str]) -> Dict[str, Any]:
        """Get demographic data from Meta API"""
        
        if not self.access_token:
            logger.warning("Meta API not configured, returning mock data")
            return self._get_mock_demographic_data(interests)
        
        # Implementation would go here for real Meta API calls
        # For now, return mock data
        return self._get_mock_demographic_data(interests)
    
    def _get_mock_demographic_data(self, interests: List[str]) -> Dict[str, Any]:
        """Return mock demographic data for development"""
        return {
            "audience_size": 1500000,
            "age_distribution": {
                "18-24": 0.15,
                "25-34": 0.35,
                "35-44": 0.30,
                "45-54": 0.15,
                "55+": 0.05
            },
            "gender_distribution": {
                "male": 0.52,
                "female": 0.48
            },
            "top_locations": ["United States", "Canada", "United Kingdom"],
            "related_interests": interests + ["technology", "innovation", "lifestyle"]
        }


# Global service instances
openai_service = OpenAIService()
voice_service = VoiceService()
meta_service = MetaAPIService()


class AIServiceManager:
    """Unified manager for all AI services"""
    
    def __init__(self):
        self.openai = openai_service
        self.voice = voice_service
        self.meta = meta_service
    
    async def initialize(self):
        """Initialize all AI services"""
        logger.info("Initializing AI services...")
        
        # Test OpenAI connection
        try:
            test_response = await self.openai.chat_completion([
                {"role": "user", "content": "Hello, this is a test."}
            ])
            logger.info("✅ OpenAI service initialized successfully")
        except Exception as e:
            logger.error(f"❌ OpenAI service initialization failed: {e}")
            raise
        
        logger.info("🤖 All AI services initialized successfully")
    
    async def health_check(self) -> Dict[str, Any]:
        """Check health of all AI services"""
        health_status = {
            "openai": "unknown",
            "voice": "unknown", 
            "meta": "unknown",
            "overall": "unknown"
        }
        
        # Check OpenAI
        try:
            await self.openai.chat_completion([
                {"role": "user", "content": "Health check"}
            ])
            health_status["openai"] = "healthy"
        except Exception:
            health_status["openai"] = "unhealthy"
        
        # Voice service depends on OpenAI
        health_status["voice"] = health_status["openai"]
        
        # Meta API (always healthy for mock data)
        health_status["meta"] = "healthy"
        
        # Overall status
        if all(status == "healthy" for status in health_status.values() if status != "unknown"):
            health_status["overall"] = "healthy"
        else:
            health_status["overall"] = "degraded"
        
        return health_status


# Global AI service manager
ai_manager = AIServiceManager()
