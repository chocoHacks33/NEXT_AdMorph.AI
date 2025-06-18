"""
Tinder-style Ad Review Interface for AdMorph.AI
Marketing directors can swipe through ad variants: approve, reject, or regenerate
"""

import streamlit as st
import asyncio
import json
from typing import List, Dict, Optional
from dataclasses import asdict
import uuid
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image

from admorph_core import AdVariantMorph, SwipeDecision, BusinessProfile

class TinderStyleAdReviewer:
    """Tinder-style interface for reviewing ad variants"""
    
    def __init__(self):
        self.current_variant_index = 0
        self.swipe_decisions = []
        self.approved_variants = []
        self.rejected_variants = []
        self.regenerate_requests = []
    
    def initialize_session_state(self):
        """Initialize Streamlit session state"""
        if 'current_variant_index' not in st.session_state:
            st.session_state.current_variant_index = 0
        if 'swipe_decisions' not in st.session_state:
            st.session_state.swipe_decisions = []
        if 'approved_variants' not in st.session_state:
            st.session_state.approved_variants = []
        if 'rejected_variants' not in st.session_state:
            st.session_state.rejected_variants = []
        if 'regenerate_requests' not in st.session_state:
            st.session_state.regenerate_requests = []
        if 'review_complete' not in st.session_state:
            st.session_state.review_complete = False
    
    def render_swipe_interface(self, variants: List[AdVariantMorph], business_profile: BusinessProfile):
        """Render the main swipe interface"""
        
        self.initialize_session_state()
        
        st.title("🎯 AdMorph.AI - Ad Review")
        st.subheader(f"Campaign: {business_profile.business_name}")
        
        # Progress indicator
        total_variants = len(variants)
        current_index = st.session_state.current_variant_index
        
        if current_index >= total_variants:
            self._render_review_complete(variants, business_profile)
            return
        
        # Progress bar
        progress = (current_index) / total_variants
        st.progress(progress)
        st.write(f"Reviewing ad {current_index + 1} of {total_variants}")
        
        # Current variant
        current_variant = variants[current_index]
        
        # Main ad display
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            self._render_ad_card(current_variant)
            
            # Swipe buttons
            st.write("---")
            button_col1, button_col2, button_col3 = st.columns(3)
            
            with button_col1:
                if st.button("❌ Reject", key=f"reject_{current_index}", use_container_width=True):
                    self._handle_swipe_decision("reject", current_variant)
            
            with button_col2:
                if st.button("🔄 Regenerate", key=f"regenerate_{current_index}", use_container_width=True):
                    self._handle_swipe_decision("regenerate", current_variant)
            
            with button_col3:
                if st.button("✅ Approve", key=f"approve_{current_index}", use_container_width=True):
                    self._handle_swipe_decision("approve", current_variant)
        
        # Sidebar with segment info
        with st.sidebar:
            self._render_segment_info(current_variant)
            self._render_review_stats()
    
    def _render_ad_card(self, variant: AdVariantMorph):
        """Render individual ad card"""
        
        # Ad preview container
        with st.container():
            st.markdown("""
            <div style="
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 20px;
                background: white;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin: 10px 0;
            ">
            """, unsafe_allow_html=True)
            
            # Headline
            st.markdown(f"### {variant.headline}")
            
            # Image placeholder (would be actual generated image)
            st.image("https://via.placeholder.com/400x300/4CAF50/white?text=Ad+Image", 
                    caption="Generated Ad Image", use_column_width=True)
            
            # Body copy
            st.write(variant.body)
            
            # Call to action button
            st.button(variant.cta, disabled=True, key=f"cta_preview_{variant.variant_id}")
            
            # Scores
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Aesthetic Score", f"{variant.aesthetic_score:.1%}")
            with col2:
                st.metric("Ogilvy Score", f"{variant.ogilvy_score:.1%}")
            with col3:
                st.metric("Emotional Impact", f"{variant.emotional_impact:.1%}")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    def _render_segment_info(self, variant: AdVariantMorph):
        """Render demographic segment information"""
        
        st.subheader("🎯 Target Segment")
        segment = variant.demographic_segment
        
        st.write(f"**Name:** {segment.name}")
        st.write(f"**Age:** {segment.age_range[0]}-{segment.age_range[1]}")
        st.write(f"**Gender:** {segment.gender}")
        st.write(f"**Income:** {segment.income_level}")
        st.write(f"**Education:** {segment.education}")
        
        if segment.interests:
            st.write("**Interests:**")
            for interest in segment.interests[:3]:  # Show top 3
                st.write(f"• {interest}")
        
        if segment.behaviors:
            st.write("**Behaviors:**")
            for behavior in segment.behaviors[:3]:  # Show top 3
                st.write(f"• {behavior}")
    
    def _render_review_stats(self):
        """Render current review statistics"""
        
        st.subheader("📊 Review Progress")
        
        approved = len(st.session_state.approved_variants)
        rejected = len(st.session_state.rejected_variants)
        regenerate = len(st.session_state.regenerate_requests)
        
        st.metric("Approved", approved)
        st.metric("Rejected", rejected)
        st.metric("Regenerate", regenerate)
        
        if approved + rejected + regenerate > 0:
            approval_rate = approved / (approved + rejected + regenerate) * 100
            st.metric("Approval Rate", f"{approval_rate:.1f}%")
    
    def _handle_swipe_decision(self, decision: str, variant: AdVariantMorph):
        """Handle swipe decision and move to next variant"""
        
        # Create swipe decision record
        swipe_decision = SwipeDecision(
            variant_id=variant.variant_id,
            decision=decision,
            timestamp=datetime.now().isoformat()
        )
        
        # Update session state
        st.session_state.swipe_decisions.append(swipe_decision)
        
        if decision == "approve":
            st.session_state.approved_variants.append(variant)
        elif decision == "reject":
            st.session_state.rejected_variants.append(variant)
        elif decision == "regenerate":
            st.session_state.regenerate_requests.append(variant)
        
        # Move to next variant
        st.session_state.current_variant_index += 1
        
        # Rerun to update interface
        st.rerun()
    
    def _render_review_complete(self, variants: List[AdVariantMorph], business_profile: BusinessProfile):
        """Render completion screen with gallery view"""
        
        st.title("🎉 Review Complete!")
        st.subheader("Your Approved Ads Gallery")
        
        approved_variants = st.session_state.approved_variants
        
        if not approved_variants:
            st.warning("No ads were approved. Would you like to review again or regenerate all variants?")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Review Again"):
                    self._reset_review()
            with col2:
                if st.button("🎨 Regenerate All"):
                    st.info("Regenerating all variants... (This would trigger the regeneration process)")
            return
        
        # Gallery view of approved ads
        st.write(f"**{len(approved_variants)} ads approved for launch**")
        
        # Display approved ads in gallery format
        cols_per_row = 3
        for i in range(0, len(approved_variants), cols_per_row):
            cols = st.columns(cols_per_row)
            
            for j, col in enumerate(cols):
                if i + j < len(approved_variants):
                    variant = approved_variants[i + j]
                    with col:
                        self._render_gallery_card(variant)
        
        # Action buttons
        st.write("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📝 Edit Selected Ads", use_container_width=True):
                st.info("Edit functionality would be implemented here")
        
        with col2:
            if st.button("🚀 Launch Campaign", use_container_width=True):
                self._launch_campaign(approved_variants, business_profile)
        
        with col3:
            if st.button("💾 Save as Draft", use_container_width=True):
                self._save_as_draft(approved_variants, business_profile)
        
        # Show regeneration requests if any
        if st.session_state.regenerate_requests:
            st.subheader("🔄 Regeneration Requests")
            st.write(f"{len(st.session_state.regenerate_requests)} ads marked for regeneration")
            
            if st.button("Generate New Variants"):
                st.info("This would trigger regeneration of the requested variants")
    
    def _render_gallery_card(self, variant: AdVariantMorph):
        """Render compact gallery card for approved ads"""
        
        with st.container():
            st.markdown(f"""
            <div style="
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                margin: 5px;
                background: #f9f9f9;
            ">
            """, unsafe_allow_html=True)
            
            st.write(f"**{variant.headline[:30]}...**")
            st.image("https://via.placeholder.com/200x150/4CAF50/white?text=Ad", use_column_width=True)
            st.write(f"Target: {variant.demographic_segment.name}")
            st.write(f"Score: {variant.aesthetic_score:.1%}")
            
            st.markdown("</div>", unsafe_allow_html=True)
    
    def _reset_review(self):
        """Reset the review process"""
        st.session_state.current_variant_index = 0
        st.session_state.swipe_decisions = []
        st.session_state.approved_variants = []
        st.session_state.rejected_variants = []
        st.session_state.regenerate_requests = []
        st.session_state.review_complete = False
        st.rerun()
    
    def _launch_campaign(self, approved_variants: List[AdVariantMorph], business_profile: BusinessProfile):
        """Launch the approved campaign"""
        st.success(f"🚀 Launching campaign with {len(approved_variants)} ads!")
        st.info("This would integrate with Meta Marketing API to publish the ads")
        
        # Show launch summary
        with st.expander("Launch Summary"):
            st.json({
                "campaign_name": f"{business_profile.business_name}_AdMorph_Campaign",
                "total_ads": len(approved_variants),
                "budget": business_profile.monthly_budget,
                "target_segments": len(set(v.demographic_segment.segment_id for v in approved_variants)),
                "launch_time": datetime.now().isoformat()
            })
    
    def _save_as_draft(self, approved_variants: List[AdVariantMorph], business_profile: BusinessProfile):
        """Save campaign as draft"""
        st.success("💾 Campaign saved as draft!")
        st.info("You can return to review and launch later")

# Streamlit App Entry Point
def main():
    """Main Streamlit app entry point"""
    
    st.set_page_config(
        page_title="AdMorph.AI - Ad Review",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
        height: 60px;
        font-size: 18px;
        font-weight: bold;
    }
    .stProgress .st-bo {
        background-color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize the reviewer
    reviewer = TinderStyleAdReviewer()
    
    # For demo purposes, create sample data
    # In production, this would come from the AdMorph pipeline
    if 'demo_variants' not in st.session_state:
        st.session_state.demo_variants = create_demo_variants()
        st.session_state.demo_business_profile = create_demo_business_profile()
    
    # Render the interface
    reviewer.render_swipe_interface(
        st.session_state.demo_variants,
        st.session_state.demo_business_profile
    )

def create_demo_variants():
    """Create demo variants for testing"""
    # This would be replaced with actual variants from the AdMorph pipeline
    from admorph_core import DemographicSegment
    
    demo_segment = DemographicSegment(
        segment_id="demo_segment_1",
        name="Young Professionals",
        age_range=(25, 35),
        gender="all",
        interests=["Technology", "Career", "Business"],
        behaviors=["Online shoppers", "Early adopters"],
        location="United States",
        income_level="Middle",
        education="Bachelor's",
        meta_targeting_spec={}
    )
    
    variants = []
    headlines = [
        "Boost Your Career Today",
        "The Future of Work is Here",
        "Join 10,000+ Professionals",
        "Transform Your Business Now"
    ]
    
    for i, headline in enumerate(headlines):
        variant = AdVariantMorph(
            variant_id=str(uuid.uuid4()),
            headline=headline,
            body=f"Discover how our solution can revolutionize your workflow and boost productivity by 300%.",
            cta="Get Started Free",
            image_url="",
            aesthetic_score=0.85 + (i * 0.02),
            ogilvy_score=0.82 + (i * 0.03),
            emotional_impact=0.78 + (i * 0.04),
            format_type="social",
            demographic_segment=demo_segment,
            generation_strategy="professional_focused",
            mutation_history=[],
            performance_score=0.0,
            trend_alignment=0.0,
            swipe_status="pending"
        )
        variants.append(variant)
    
    return variants

def create_demo_business_profile():
    """Create demo business profile"""
    return BusinessProfile(
        business_id="demo_business_1",
        business_name="TechFlow Solutions",
        industry="Software",
        target_engagement="sales",
        monthly_budget=5000.0,
        target_audience={"description": "Small business owners and professionals"},
        brand_themes={"allowed": ["innovation", "efficiency", "growth"], "disallowed": ["aggressive", "pushy"]},
        original_ad_assets=[],
        voice_preferences={"tone": "professional", "style": "modern"},
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat()
    )

if __name__ == "__main__":
    main()
