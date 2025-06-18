#!/usr/bin/env python3
"""
E-commerce Personalization Demo
"""

import json
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, List, Optional, Any


# Simplified models for demo
@dataclass
class DemographicSegment:
    segment_id: str
    name: str
    age_range: tuple
    interests: List[str]
    behaviors: List[str]
    
    def to_dict(self):
        return {
            "segment_id": self.segment_id,
            "name": self.name,
            "age_range": self.age_range,
            "interests": self.interests,
            "behaviors": self.behaviors
        }


@dataclass 
class BaseProduct:
    product_id: str
    name: str
    base_price: float
    category: str
    features: List[str]
    
    def to_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "base_price": self.base_price,
            "category": self.category,
            "features": self.features
        }


@dataclass
class ProductVariant:
    variant_id: str
    product_id: str
    demographic_segment: DemographicSegment
    personalized_title: str
    personalized_description: str
    highlighted_features: List[str]
    price_positioning: str
    call_to_action: str
    
    def to_dict(self):
        return {
            "variant_id": self.variant_id,
            "product_id": self.product_id,
            "demographic_segment": self.demographic_segment.to_dict(),
            "personalized_title": self.personalized_title,
            "personalized_description": self.personalized_description,
            "highlighted_features": self.highlighted_features,
            "price_positioning": self.price_positioning,
            "call_to_action": self.call_to_action
        }


def create_sample_products():
    """Create sample products"""
    return [
        BaseProduct(
            product_id="wireless-headphones-001",
            name="Premium Wireless Headphones",
            base_price=99.99,
            category="Electronics",
            features=[
                "Bluetooth 5.0 connectivity",
                "20-hour battery life",
                "Active noise cancellation",
                "Quick charge (15min = 3hrs)",
                "Premium leather comfort",
                "Crystal clear calls"
            ]
        ),
        BaseProduct(
            product_id="fitness-tracker-002", 
            name="Smart Fitness Tracker",
            base_price=149.99,
            category="Wearables",
            features=[
                "Heart rate monitoring",
                "GPS tracking", 
                "Sleep analysis",
                "Waterproof design",
                "7-day battery life",
                "Smartphone notifications"
            ]
        )
    ]


def create_sample_demographics():
    """Create sample demographic segments"""
    return [
        DemographicSegment(
            segment_id="young-professionals",
            name="Young Professionals",
            age_range=(25, 35),
            interests=["Technology", "Career Development", "Productivity"],
            behaviors=["Early adopters", "Quality-focused", "Time-conscious"]
        ),
        DemographicSegment(
            segment_id="fitness-enthusiasts",
            name="Fitness Enthusiasts", 
            age_range=(22, 40),
            interests=["Fitness", "Health", "Sports", "Wellness"],
            behaviors=["Health-conscious", "Active lifestyle", "Goal-oriented"]
        ),
        DemographicSegment(
            segment_id="tech-early-adopters",
            name="Tech Early Adopters",
            age_range=(18, 45),
            interests=["Technology", "Gadgets", "Innovation", "Gaming"],
            behaviors=["Early adopters", "Tech-savvy", "Research-driven"]
        )
    ]


def personalize_product(product: BaseProduct, demographic: DemographicSegment) -> ProductVariant:
    """Generate personalized product variant (mock AI generation)"""
    
    # Mock personalization logic based on demographic
    if "fitness" in demographic.name.lower():
        if "headphones" in product.name.lower():
            return ProductVariant(
                variant_id=f"variant-{product.product_id}-{demographic.segment_id}",
                product_id=product.product_id,
                demographic_segment=demographic,
                personalized_title="Wireless Sport Headphones - Sweat-Proof for Intense Workouts",
                personalized_description="Push your limits with these ultra-secure, sweat-resistant headphones designed for athletes. With 20-hour battery life and secure fit, they'll stay with you through your toughest training sessions.",
                highlighted_features=["Sweat-proof design", "Secure athletic fit", "20-hour battery"],
                price_positioning="performance",
                call_to_action="Get Yours Now"
            )
        else:  # fitness tracker
            return ProductVariant(
                variant_id=f"variant-{product.product_id}-{demographic.segment_id}",
                product_id=product.product_id,
                demographic_segment=demographic,
                personalized_title="Advanced Fitness Tracker - Your Personal Training Coach",
                personalized_description="Take your fitness to the next level with advanced heart rate monitoring, GPS tracking, and personalized workout insights. Perfect for serious athletes and fitness enthusiasts.",
                highlighted_features=["Heart rate zones", "GPS tracking", "Workout analysis"],
                price_positioning="performance",
                call_to_action="Start Training"
            )
    
    elif "professional" in demographic.name.lower():
        if "headphones" in product.name.lower():
            return ProductVariant(
                variant_id=f"variant-{product.product_id}-{demographic.segment_id}",
                product_id=product.product_id,
                demographic_segment=demographic,
                personalized_title="Premium Wireless Headphones - Crystal Clear Calls & Noise Cancellation",
                personalized_description="Elevate your professional presence with premium audio quality and advanced noise cancellation. Perfect for important calls, focus work, and premium music experience.",
                highlighted_features=["Noise cancellation", "Clear calls", "Premium quality"],
                price_positioning="premium",
                call_to_action="Upgrade Your Audio"
            )
        else:  # fitness tracker
            return ProductVariant(
                variant_id=f"variant-{product.product_id}-{demographic.segment_id}",
                product_id=product.product_id,
                demographic_segment=demographic,
                personalized_title="Smart Health Monitor - Stay Productive & Healthy",
                personalized_description="Balance your busy professional life with smart health monitoring. Track stress, sleep quality, and activity to maintain peak performance in your career.",
                highlighted_features=["Stress monitoring", "Sleep analysis", "Smart notifications"],
                price_positioning="premium",
                call_to_action="Invest in Your Health"
            )
    
    else:  # tech early adopters
        if "headphones" in product.name.lower():
            return ProductVariant(
                variant_id=f"variant-{product.product_id}-{demographic.segment_id}",
                product_id=product.product_id,
                demographic_segment=demographic,
                personalized_title="Next-Gen Wireless Headphones - Latest Bluetooth 5.0 Technology",
                personalized_description="Experience cutting-edge audio technology with the latest Bluetooth 5.0, advanced codecs, and innovative features. Perfect for tech enthusiasts who demand the best.",
                highlighted_features=["Bluetooth 5.0", "Advanced codecs", "Latest tech"],
                price_positioning="value",
                call_to_action="Get Latest Tech"
            )
        else:  # fitness tracker
            return ProductVariant(
                variant_id=f"variant-{product.product_id}-{demographic.segment_id}",
                product_id=product.product_id,
                demographic_segment=demographic,
                personalized_title="Smart Wearable Tech - Advanced Sensors & AI Insights",
                personalized_description="Discover the future of wearable technology with advanced sensors, AI-powered insights, and seamless smartphone integration. The perfect gadget for tech innovators.",
                highlighted_features=["AI insights", "Advanced sensors", "Smart integration"],
                price_positioning="value",
                call_to_action="Experience Innovation"
            )


def run_demo():
    """Run the e-commerce personalization demo"""
    print("🛍️ E-COMMERCE PERSONALIZATION DEMO")
    print("=" * 50)
    
    # Create sample data
    products = create_sample_products()
    demographics = create_sample_demographics()
    
    print(f"\n📦 Sample Products ({len(products)}):")
    for product in products:
        print(f"   • {product.name} - ${product.base_price}")
    
    print(f"\n👥 Target Demographics ({len(demographics)}):")
    for demo in demographics:
        print(f"   • {demo.name}: {demo.age_range[0]}-{demo.age_range[1]} years")
    
    print(f"\n🎯 PERSONALIZATION RESULTS:")
    print("=" * 50)
    
    # Generate personalized variants
    for product in products:
        print(f"\n📱 PRODUCT: {product.name}")
        print("-" * 40)
        
        for demographic in demographics:
            variant = personalize_product(product, demographic)
            
            print(f"\n👤 TARGET: {demographic.name}")
            print(f"📝 Title: {variant.personalized_title}")
            print(f"📄 Description: {variant.personalized_description[:100]}...")
            print(f"⭐ Key Features: {', '.join(variant.highlighted_features)}")
            print(f"💰 Price Position: {variant.price_positioning}")
            print(f"🔘 CTA: {variant.call_to_action}")
    
    print(f"\n🎉 DEMO COMPLETE!")
    print("=" * 50)
    print("✅ Product personalization system working!")
    print("✅ Different variants generated for each demographic")
    print("✅ Personalized titles, descriptions, and features")
    print("✅ Appropriate price positioning and CTAs")
    print("\n💡 This demonstrates how the same product can be")
    print("   personalized for different customer segments!")
    
    # Show JSON output example
    print(f"\n📊 SAMPLE API RESPONSE:")
    print("-" * 30)
    sample_variant = personalize_product(products[0], demographics[0])
    print(json.dumps(sample_variant.to_dict(), indent=2))


if __name__ == "__main__":
    run_demo()
