"""
Agentic Ad Evolution System for AdMorph.AI
Continuously mutates ads based on real-world trends, engagement metrics, CTR, and conversion rates
"""

import asyncio
import json
import uuid
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import numpy as np
from abc import ABC, abstractmethod

from admorph_core import AdVariantMorph, EngagementMetrics, OpenAIAgent
from meta_api_integration import MetaMarketingAPIClient

@dataclass
class TrendData:
    """Current trend information for ad optimization"""
    trend_id: str
    category: str  # 'social', 'cultural', 'economic', 'seasonal'
    description: str
    keywords: List[str]
    sentiment: str  # 'positive', 'negative', 'neutral'
    relevance_score: float
    expiry_date: str
    source: str

@dataclass
class MutationRule:
    """Rules for how ads should mutate based on performance"""
    rule_id: str
    trigger_condition: str  # 'low_ctr', 'low_conversion', 'high_cost', 'trend_shift'
    mutation_type: str  # 'headline', 'body', 'cta', 'image', 'targeting'
    strategy: str
    confidence_threshold: float

@dataclass
class EvolutionMetrics:
    """Metrics tracking ad evolution performance"""
    variant_id: str
    generation: int
    parent_variant_id: Optional[str]
    mutation_type: str
    performance_improvement: float
    trend_alignment_score: float
    created_at: str

class SyntheticDataGenerator:
    """Generates realistic synthetic performance data for testing"""
    
    def __init__(self):
        self.base_metrics = {
            "ctr_range": (0.005, 0.08),
            "conversion_rate_range": (0.01, 0.15),
            "engagement_rate_range": (0.02, 0.12),
            "cost_per_click_range": (0.50, 5.00)
        }
    
    def generate_performance_data(self, variant: AdVariantMorph, days: int = 7) -> List[EngagementMetrics]:
        """Generate synthetic performance data for a variant over time"""
        
        metrics = []
        base_date = datetime.now() - timedelta(days=days)
        
        # Simulate performance evolution over time
        for day in range(days):
            current_date = base_date + timedelta(days=day)
            
            # Add some randomness and trends
            trend_factor = 1 + (day * 0.02)  # Slight improvement over time
            noise_factor = random.uniform(0.8, 1.2)
            
            # Generate base metrics
            impressions = random.randint(1000, 10000)
            ctr = random.uniform(*self.base_metrics["ctr_range"]) * trend_factor * noise_factor
            clicks = int(impressions * ctr)
            conversion_rate = random.uniform(*self.base_metrics["conversion_rate_range"]) * trend_factor
            conversions = int(clicks * conversion_rate)
            engagement_rate = random.uniform(*self.base_metrics["engagement_rate_range"]) * trend_factor
            cpc = random.uniform(*self.base_metrics["cost_per_click_range"]) / trend_factor
            
            metric = EngagementMetrics(
                variant_id=variant.variant_id,
                impressions=impressions,
                clicks=clicks,
                ctr=ctr,
                conversions=conversions,
                engagement_rate=engagement_rate,
                timestamp=current_date.isoformat(),
                cost_per_acquisition=cpc * (1/conversion_rate) if conversion_rate > 0 else 100.0
            )
            metrics.append(metric)
        
        return metrics
    
    def generate_trend_data(self) -> List[TrendData]:
        """Generate current trend data"""
        
        trends = [
            TrendData(
                trend_id=str(uuid.uuid4()),
                category="social",
                description="Sustainability and eco-consciousness trending",
                keywords=["sustainable", "eco-friendly", "green", "environment"],
                sentiment="positive",
                relevance_score=0.85,
                expiry_date=(datetime.now() + timedelta(days=30)).isoformat(),
                source="social_media_analysis"
            ),
            TrendData(
                trend_id=str(uuid.uuid4()),
                category="economic",
                description="Cost-saving and value-focused messaging",
                keywords=["save money", "affordable", "value", "budget-friendly"],
                sentiment="neutral",
                relevance_score=0.78,
                expiry_date=(datetime.now() + timedelta(days=45)).isoformat(),
                source="economic_indicators"
            ),
            TrendData(
                trend_id=str(uuid.uuid4()),
                category="cultural",
                description="Remote work and flexibility emphasis",
                keywords=["remote", "flexible", "work from home", "freedom"],
                sentiment="positive",
                relevance_score=0.72,
                expiry_date=(datetime.now() + timedelta(days=60)).isoformat(),
                source="workplace_trends"
            ),
            TrendData(
                trend_id=str(uuid.uuid4()),
                category="seasonal",
                description="Holiday season preparation and planning",
                keywords=["holiday", "season", "preparation", "planning", "gifts"],
                sentiment="positive",
                relevance_score=0.90,
                expiry_date=(datetime.now() + timedelta(days=90)).isoformat(),
                source="seasonal_analysis"
            )
        ]
        
        return trends

class TrendAnalysisAgent(OpenAIAgent):
    """Agent that analyzes current trends and their relevance to ads"""
    
    def __init__(self):
        super().__init__("Trend Analysis Specialist", temperature=0.3)
        self.trend_sources = ["social_media", "news", "search_trends", "economic_data"]
    
    async def execute(self, business_profile: Any, current_trends: List[TrendData], context: Dict = None) -> Dict:
        """Analyze trends and determine relevance to business"""
        
        relevant_trends = await self._filter_relevant_trends(business_profile, current_trends)
        trend_insights = await self._generate_trend_insights(business_profile, relevant_trends)
        
        return {
            "relevant_trends": relevant_trends,
            "trend_insights": trend_insights,
            "trend_alignment_score": await self._calculate_trend_alignment(business_profile, relevant_trends),
            "recommended_adaptations": await self._recommend_adaptations(business_profile, relevant_trends)
        }
    
    async def _filter_relevant_trends(self, business_profile: Any, trends: List[TrendData]) -> List[TrendData]:
        """Filter trends relevant to the business"""
        
        analysis_prompt = f"""
        Analyze which of these trends are most relevant to this business:
        
        Business: {business_profile.business_name}
        Industry: {business_profile.industry}
        Target Audience: {business_profile.target_audience}
        
        Trends to analyze:
        {json.dumps([asdict(trend) for trend in trends], indent=2)}
        
        Return a JSON array of trend_ids that are highly relevant (relevance_score > 0.7) to this business.
        Consider industry alignment, audience interests, and business goals.
        """
        
        messages = [
            {"role": "system", "content": "You are a trend analysis expert. Identify relevant trends for businesses."},
            {"role": "user", "content": analysis_prompt}
        ]
        
        try:
            response = await self._call_openai(messages)
            relevant_trend_ids = json.loads(response)
            return [trend for trend in trends if trend.trend_id in relevant_trend_ids]
        except:
            # Fallback: return trends with high relevance scores
            return [trend for trend in trends if trend.relevance_score > 0.7]
    
    async def _generate_trend_insights(self, business_profile: Any, trends: List[TrendData]) -> Dict[str, str]:
        """Generate insights about how trends affect the business"""
        
        insights = {}
        for trend in trends:
            insight_prompt = f"""
            How should {business_profile.business_name} adapt their advertising to align with this trend?
            
            Trend: {trend.description}
            Keywords: {', '.join(trend.keywords)}
            Sentiment: {trend.sentiment}
            
            Provide specific, actionable advice for ad messaging and positioning.
            """
            
            messages = [
                {"role": "system", "content": "You are an advertising strategist providing trend-based recommendations."},
                {"role": "user", "content": insight_prompt}
            ]
            
            try:
                response = await self._call_openai(messages, temperature=0.4)
                insights[trend.trend_id] = response
            except:
                insights[trend.trend_id] = f"Consider incorporating {trend.keywords[0]} messaging"
        
        return insights
    
    async def _calculate_trend_alignment(self, business_profile: Any, trends: List[TrendData]) -> float:
        """Calculate overall trend alignment score"""
        if not trends:
            return 0.0
        
        total_score = sum(trend.relevance_score for trend in trends)
        return min(total_score / len(trends), 1.0)
    
    async def _recommend_adaptations(self, business_profile: Any, trends: List[TrendData]) -> List[str]:
        """Recommend specific adaptations based on trends"""
        
        adaptations = []
        for trend in trends[:3]:  # Top 3 trends
            if trend.category == "social":
                adaptations.append(f"Incorporate {trend.keywords[0]} messaging in headlines")
            elif trend.category == "economic":
                adaptations.append(f"Emphasize value proposition with {trend.keywords[0]} focus")
            elif trend.category == "cultural":
                adaptations.append(f"Align messaging with {trend.description}")
        
        return adaptations

class PerformanceAnalysisAgent(OpenAIAgent):
    """Agent that analyzes ad performance and identifies optimization opportunities"""
    
    def __init__(self):
        super().__init__("Performance Analysis Specialist", temperature=0.2)
    
    async def execute(self, variant: AdVariantMorph, metrics: List[EngagementMetrics], context: Dict = None) -> Dict:
        """Analyze performance and identify issues"""
        
        performance_analysis = await self._analyze_performance_patterns(metrics)
        optimization_opportunities = await self._identify_optimization_opportunities(variant, metrics)
        mutation_recommendations = await self._recommend_mutations(variant, performance_analysis)
        
        return {
            "variant_id": variant.variant_id,
            "performance_analysis": performance_analysis,
            "optimization_opportunities": optimization_opportunities,
            "mutation_recommendations": mutation_recommendations,
            "performance_score": await self._calculate_performance_score(metrics),
            "needs_mutation": await self._needs_mutation(metrics)
        }
    
    async def _analyze_performance_patterns(self, metrics: List[EngagementMetrics]) -> Dict[str, Any]:
        """Analyze performance patterns over time"""
        
        if not metrics:
            return {"error": "No metrics available"}
        
        # Calculate trends
        ctrs = [m.ctr for m in metrics]
        conversions = [m.conversions for m in metrics]
        
        ctr_trend = "improving" if ctrs[-1] > ctrs[0] else "declining"
        conversion_trend = "improving" if conversions[-1] > conversions[0] else "declining"
        
        avg_ctr = np.mean(ctrs)
        avg_conversion_rate = np.mean([m.conversions / max(m.clicks, 1) for m in metrics])
        
        return {
            "avg_ctr": avg_ctr,
            "avg_conversion_rate": avg_conversion_rate,
            "ctr_trend": ctr_trend,
            "conversion_trend": conversion_trend,
            "total_impressions": sum(m.impressions for m in metrics),
            "total_conversions": sum(m.conversions for m in metrics)
        }
    
    async def _identify_optimization_opportunities(self, variant: AdVariantMorph, metrics: List[EngagementMetrics]) -> List[str]:
        """Identify specific optimization opportunities"""
        
        opportunities = []
        latest_metrics = metrics[-1] if metrics else None
        
        if not latest_metrics:
            return ["Insufficient data for analysis"]
        
        if latest_metrics.ctr < 0.02:
            opportunities.append("Low CTR - consider more compelling headlines")
        
        if latest_metrics.conversions / max(latest_metrics.clicks, 1) < 0.05:
            opportunities.append("Low conversion rate - strengthen value proposition")
        
        if latest_metrics.cost_per_acquisition > 50:
            opportunities.append("High CPA - optimize targeting or messaging")
        
        if latest_metrics.engagement_rate < 0.03:
            opportunities.append("Low engagement - make content more interactive")
        
        return opportunities if opportunities else ["Performance is within acceptable ranges"]
    
    async def _recommend_mutations(self, variant: AdVariantMorph, analysis: Dict[str, Any]) -> List[Dict[str, str]]:
        """Recommend specific mutations based on performance"""
        
        recommendations = []
        
        if analysis.get("avg_ctr", 0) < 0.02:
            recommendations.append({
                "type": "headline",
                "strategy": "increase_urgency",
                "reason": "Low CTR indicates headline needs more compelling hook"
            })
        
        if analysis.get("avg_conversion_rate", 0) < 0.05:
            recommendations.append({
                "type": "cta",
                "strategy": "strengthen_action",
                "reason": "Low conversion rate suggests weak call-to-action"
            })
        
        if analysis.get("ctr_trend") == "declining":
            recommendations.append({
                "type": "body",
                "strategy": "refresh_messaging",
                "reason": "Declining CTR indicates message fatigue"
            })
        
        return recommendations
    
    async def _calculate_performance_score(self, metrics: List[EngagementMetrics]) -> float:
        """Calculate overall performance score (0-1)"""
        
        if not metrics:
            return 0.0
        
        latest = metrics[-1]
        
        # Normalize metrics to 0-1 scale
        ctr_score = min(latest.ctr / 0.05, 1.0)  # 5% CTR = perfect score
        conversion_score = min((latest.conversions / max(latest.clicks, 1)) / 0.1, 1.0)  # 10% conversion = perfect
        engagement_score = min(latest.engagement_rate / 0.08, 1.0)  # 8% engagement = perfect
        
        # Weighted average
        return (ctr_score * 0.4 + conversion_score * 0.4 + engagement_score * 0.2)
    
    async def _needs_mutation(self, metrics: List[EngagementMetrics]) -> bool:
        """Determine if variant needs mutation"""
        
        if len(metrics) < 3:
            return False  # Need enough data
        
        performance_score = await self._calculate_performance_score(metrics)
        
        # Check for declining trends
        recent_ctrs = [m.ctr for m in metrics[-3:]]
        is_declining = recent_ctrs[-1] < recent_ctrs[0]
        
        return performance_score < 0.6 or is_declining

class AdMutationAgent(OpenAIAgent):
    """Agent that performs intelligent mutations on ad variants"""
    
    def __init__(self):
        super().__init__("Ad Mutation Specialist", temperature=0.7)
        self.mutation_strategies = self._load_mutation_strategies()
    
    def _load_mutation_strategies(self) -> Dict[str, Dict[str, List[str]]]:
        """Load mutation strategies for different ad elements"""
        return {
            "headline": {
                "increase_urgency": ["Add time-sensitive words", "Include scarcity elements", "Use action verbs"],
                "emotional_appeal": ["Add emotional triggers", "Use personal pronouns", "Include benefits"],
                "curiosity_gap": ["Create mystery", "Ask questions", "Tease solutions"]
            },
            "body": {
                "strengthen_benefits": ["Highlight key benefits", "Add social proof", "Include statistics"],
                "refresh_messaging": ["Change angle", "Update examples", "Modernize language"],
                "add_urgency": ["Include deadlines", "Limited availability", "Act now messaging"]
            },
            "cta": {
                "strengthen_action": ["More specific verbs", "Add value proposition", "Create urgency"],
                "reduce_friction": ["Softer language", "Lower commitment", "Free trial focus"]
            }
        }
    
    async def execute(self, variant: AdVariantMorph, mutation_recommendations: List[Dict[str, str]], trend_data: List[TrendData], context: Dict = None) -> Dict:
        """Execute mutations on ad variant"""
        
        mutated_variants = []
        
        for recommendation in mutation_recommendations:
            mutated_variant = await self._create_mutation(variant, recommendation, trend_data)
            if mutated_variant:
                mutated_variants.append(mutated_variant)
        
        return {
            "original_variant_id": variant.variant_id,
            "mutated_variants": mutated_variants,
            "mutation_count": len(mutated_variants),
            "mutation_timestamp": datetime.now().isoformat()
        }
    
    async def _create_mutation(self, original: AdVariantMorph, recommendation: Dict[str, str], trends: List[TrendData]) -> Optional[AdVariantMorph]:
        """Create a single mutation based on recommendation"""
        
        mutation_type = recommendation["type"]
        strategy = recommendation["strategy"]
        
        # Build mutation prompt
        trend_context = ""
        if trends:
            trend_keywords = []
            for trend in trends[:2]:  # Use top 2 trends
                trend_keywords.extend(trend.keywords[:2])
            trend_context = f"Current trends to consider: {', '.join(trend_keywords)}"
        
        mutation_prompt = f"""
        Mutate this ad element based on the strategy:
        
        Original {mutation_type}: {getattr(original, mutation_type)}
        Strategy: {strategy}
        Reason: {recommendation.get('reason', '')}
        {trend_context}
        
        Create an improved version that addresses the performance issue while maintaining brand consistency.
        Target audience: {original.demographic_segment.name}
        
        Return only the new {mutation_type} text, nothing else.
        """
        
        messages = [
            {"role": "system", "content": f"You are an expert ad copywriter specializing in {mutation_type} optimization."},
            {"role": "user", "content": mutation_prompt}
        ]
        
        try:
            new_content = await self._call_openai(messages, temperature=0.7)
            new_content = new_content.strip().strip('"')
            
            # Create mutated variant
            mutated_variant = AdVariantMorph(
                variant_id=str(uuid.uuid4()),
                headline=new_content if mutation_type == "headline" else original.headline,
                body=new_content if mutation_type == "body" else original.body,
                cta=new_content if mutation_type == "cta" else original.cta,
                image_url=original.image_url,
                aesthetic_score=original.aesthetic_score,
                ogilvy_score=original.ogilvy_score,
                emotional_impact=original.emotional_impact * 1.1,  # Slight boost for mutation
                format_type=original.format_type,
                demographic_segment=original.demographic_segment,
                generation_strategy=f"mutation_{strategy}",
                mutation_history=original.mutation_history + [{
                    "parent_id": original.variant_id,
                    "mutation_type": mutation_type,
                    "strategy": strategy,
                    "timestamp": datetime.now().isoformat()
                }],
                performance_score=0.0,
                trend_alignment=0.8,  # Higher for trend-aligned mutations
                swipe_status="pending"
            )
            
            return mutated_variant

        except Exception as e:
            print(f"Error creating mutation: {e}")
            return None

class EvolutionOrchestrator:
    """Orchestrates the complete ad evolution process"""

    def __init__(self):
        self.trend_agent = TrendAnalysisAgent()
        self.performance_agent = PerformanceAnalysisAgent()
        self.mutation_agent = AdMutationAgent()
        self.data_generator = SyntheticDataGenerator()
        self.meta_client = MetaMarketingAPIClient()

        self.evolution_history = {}
        self.active_variants = {}

    async def start_evolution_cycle(self, variants: List[AdVariantMorph], business_profile: Any) -> Dict[str, Any]:
        """Start continuous evolution cycle for ad variants"""

        evolution_results = {
            "cycle_id": str(uuid.uuid4()),
            "started_at": datetime.now().isoformat(),
            "variants_processed": 0,
            "mutations_created": 0,
            "performance_improvements": [],
            "trend_alignments": []
        }

        # Get current trends
        current_trends = self.data_generator.generate_trend_data()
        trend_analysis = await self.trend_agent.execute(business_profile, current_trends)

        for variant in variants:
            # Generate or get performance data
            if variant.variant_id not in self.active_variants:
                # Generate synthetic performance data for new variants
                performance_data = self.data_generator.generate_performance_data(variant)
                self.active_variants[variant.variant_id] = {
                    "variant": variant,
                    "performance_history": performance_data,
                    "last_mutation": None
                }
            else:
                # Get real performance data from Meta API
                performance_data = await self._get_real_performance_data(variant)
                self.active_variants[variant.variant_id]["performance_history"].extend(performance_data)

            # Analyze performance
            performance_analysis = await self.performance_agent.execute(
                variant,
                self.active_variants[variant.variant_id]["performance_history"]
            )

            evolution_results["variants_processed"] += 1

            # Check if mutation is needed
            if performance_analysis["needs_mutation"]:
                # Create mutations
                mutation_result = await self.mutation_agent.execute(
                    variant,
                    performance_analysis["mutation_recommendations"],
                    trend_analysis["relevant_trends"]
                )

                evolution_results["mutations_created"] += len(mutation_result["mutated_variants"])

                # Store mutations for testing
                for mutated_variant in mutation_result["mutated_variants"]:
                    self.active_variants[mutated_variant.variant_id] = {
                        "variant": mutated_variant,
                        "performance_history": [],
                        "last_mutation": datetime.now()
                    }

                # Auto-publish high-confidence mutations
                await self._auto_publish_mutations(mutation_result["mutated_variants"], business_profile)

        return evolution_results

    async def _get_real_performance_data(self, variant: AdVariantMorph) -> List[EngagementMetrics]:
        """Get real performance data from Meta API"""

        if not variant.meta_campaign_id:
            return []

        try:
            performance = await self.meta_client.get_campaign_performance(variant.meta_campaign_id)

            if "error" not in performance:
                # Convert Meta performance to EngagementMetrics
                metric = EngagementMetrics(
                    variant_id=variant.variant_id,
                    impressions=performance.get("impressions", 0),
                    clicks=performance.get("clicks", 0),
                    ctr=performance.get("ctr", 0.0),
                    conversions=performance.get("conversions", 0),
                    engagement_rate=performance.get("ctr", 0.0),  # Simplified
                    timestamp=datetime.now().isoformat(),
                    cost_per_acquisition=performance.get("cost_per_conversion", 0.0)
                )
                return [metric]
        except Exception as e:
            print(f"Error getting real performance data: {e}")

        return []

    async def _auto_publish_mutations(self, mutations: List[AdVariantMorph], business_profile: Any):
        """Automatically publish high-confidence mutations"""

        high_confidence_mutations = [
            m for m in mutations
            if m.trend_alignment > 0.7 and len(m.mutation_history) <= 2
        ]

        if high_confidence_mutations:
            try:
                # Publish to Meta API
                result = await self.meta_client.publish_campaign(high_confidence_mutations, business_profile)

                if result["success"]:
                    for mutation in high_confidence_mutations:
                        mutation.is_published = True
                        mutation.meta_campaign_id = result.get("campaign_id")

                    print(f"Auto-published {len(high_confidence_mutations)} high-confidence mutations")

            except Exception as e:
                print(f"Error auto-publishing mutations: {e}")

    async def get_evolution_insights(self, time_period_days: int = 30) -> Dict[str, Any]:
        """Get insights about ad evolution performance"""

        insights = {
            "total_variants": len(self.active_variants),
            "total_mutations": 0,
            "performance_improvements": [],
            "top_performing_mutations": [],
            "trend_adoption_rate": 0.0,
            "avg_performance_improvement": 0.0
        }

        for variant_id, data in self.active_variants.items():
            variant = data["variant"]

            # Count mutations
            insights["total_mutations"] += len(variant.mutation_history)

            # Calculate performance improvements
            if len(data["performance_history"]) > 1:
                initial_performance = data["performance_history"][0].ctr
                latest_performance = data["performance_history"][-1].ctr
                improvement = (latest_performance - initial_performance) / initial_performance * 100

                insights["performance_improvements"].append({
                    "variant_id": variant_id,
                    "improvement_percentage": improvement,
                    "mutation_count": len(variant.mutation_history)
                })

        # Calculate averages
        if insights["performance_improvements"]:
            insights["avg_performance_improvement"] = np.mean([
                p["improvement_percentage"] for p in insights["performance_improvements"]
            ])

        return insights

    async def emergency_rollback(self, variant_id: str) -> Dict[str, Any]:
        """Emergency rollback to previous version if mutation performs poorly"""

        if variant_id not in self.active_variants:
            return {"success": False, "error": "Variant not found"}

        variant = self.active_variants[variant_id]["variant"]

        if not variant.mutation_history:
            return {"success": False, "error": "No previous version to rollback to"}

        # Find parent variant
        parent_id = variant.mutation_history[-1]["parent_id"]

        if parent_id in self.active_variants:
            # Pause current variant
            if variant.meta_campaign_id:
                await self.meta_client.pause_campaign(variant.meta_campaign_id)

            # Reactivate parent
            parent_variant = self.active_variants[parent_id]["variant"]
            if parent_variant.meta_campaign_id:
                await self.meta_client.resume_campaign(parent_variant.meta_campaign_id)

            return {
                "success": True,
                "rolled_back_to": parent_id,
                "paused_variant": variant_id
            }

        return {"success": False, "error": "Parent variant not found"}

class EvolutionMonitor:
    """Monitors evolution process and provides real-time insights"""

    def __init__(self, orchestrator: EvolutionOrchestrator):
        self.orchestrator = orchestrator
        self.monitoring_active = False

    async def start_monitoring(self, check_interval_minutes: int = 60):
        """Start continuous monitoring of ad evolution"""

        self.monitoring_active = True

        while self.monitoring_active:
            try:
                # Check all active variants
                alerts = await self._check_for_alerts()

                if alerts:
                    await self._handle_alerts(alerts)

                # Wait for next check
                await asyncio.sleep(check_interval_minutes * 60)

            except Exception as e:
                print(f"Monitoring error: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error

    async def _check_for_alerts(self) -> List[Dict[str, Any]]:
        """Check for performance alerts"""

        alerts = []

        for variant_id, data in self.orchestrator.active_variants.items():
            variant = data["variant"]
            performance_history = data["performance_history"]

            if len(performance_history) < 2:
                continue

            latest_performance = performance_history[-1]

            # Check for performance drops
            if len(performance_history) >= 3:
                recent_avg = np.mean([m.ctr for m in performance_history[-3:]])
                previous_avg = np.mean([m.ctr for m in performance_history[-6:-3]]) if len(performance_history) >= 6 else recent_avg

                if recent_avg < previous_avg * 0.8:  # 20% drop
                    alerts.append({
                        "type": "performance_drop",
                        "variant_id": variant_id,
                        "severity": "high",
                        "message": f"CTR dropped by {((previous_avg - recent_avg) / previous_avg * 100):.1f}%"
                    })

            # Check for high costs
            if latest_performance.cost_per_acquisition > 100:
                alerts.append({
                    "type": "high_cost",
                    "variant_id": variant_id,
                    "severity": "medium",
                    "message": f"CPA is ${latest_performance.cost_per_acquisition:.2f}"
                })

        return alerts

    async def _handle_alerts(self, alerts: List[Dict[str, Any]]):
        """Handle performance alerts"""

        for alert in alerts:
            print(f"ALERT: {alert['type']} - {alert['message']} (Variant: {alert['variant_id']})")

            if alert["severity"] == "high":
                # Trigger emergency mutation or rollback
                if alert["type"] == "performance_drop":
                    await self.orchestrator.emergency_rollback(alert["variant_id"])

    def stop_monitoring(self):
        """Stop the monitoring process"""
        self.monitoring_active = False

# Demo and Testing Functions
async def demo_agentic_evolution():
    """Demonstrate the agentic evolution system"""

    print("🧬 Starting AdMorph.AI Agentic Evolution Demo")
    print("=" * 50)

    # Initialize system
    orchestrator = EvolutionOrchestrator()
    monitor = EvolutionMonitor(orchestrator)

    # Create demo variants (would come from main AdMorph pipeline)
    from admorph_core import DemographicSegment, BusinessProfile

    demo_segment = DemographicSegment(
        segment_id="demo_segment",
        name="Tech Professionals",
        age_range=(25, 40),
        gender="all",
        interests=["Technology", "Innovation"],
        behaviors=["Early adopters"],
        location="United States",
        income_level="High",
        education="Bachelor's",
        meta_targeting_spec={}
    )

    demo_business = BusinessProfile(
        business_id="demo_business",
        business_name="AI Solutions Inc",
        industry="Technology",
        target_engagement="sales",
        monthly_budget=10000.0,
        target_audience={"description": "Tech professionals"},
        brand_themes={"allowed": ["innovation", "efficiency"], "disallowed": ["outdated"]},
        original_ad_assets=[],
        voice_preferences={"tone": "professional"},
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )

    demo_variant = AdVariantMorph(
        variant_id=str(uuid.uuid4()),
        headline="Revolutionize Your Workflow",
        body="Discover how AI can transform your business processes and boost productivity.",
        cta="Get Started",
        image_url="",
        aesthetic_score=0.8,
        ogilvy_score=0.75,
        emotional_impact=0.7,
        format_type="social",
        demographic_segment=demo_segment,
        generation_strategy="initial",
        mutation_history=[],
        performance_score=0.0,
        trend_alignment=0.6,
        swipe_status="approved"
    )

    # Run evolution cycle
    print("🔄 Running evolution cycle...")
    evolution_result = await orchestrator.start_evolution_cycle([demo_variant], demo_business)

    print(f"✅ Evolution cycle complete!")
    print(f"   Variants processed: {evolution_result['variants_processed']}")
    print(f"   Mutations created: {evolution_result['mutations_created']}")

    # Get insights
    print("\n📊 Getting evolution insights...")
    insights = await orchestrator.get_evolution_insights()

    print(f"   Total variants: {insights['total_variants']}")
    print(f"   Total mutations: {insights['total_mutations']}")
    print(f"   Avg performance improvement: {insights['avg_performance_improvement']:.1f}%")

    print("\n🧬 Agentic Evolution Demo Complete!")

    return evolution_result

if __name__ == "__main__":
    asyncio.run(demo_agentic_evolution())
