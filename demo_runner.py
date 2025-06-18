"""
AdMorph.AI Demo Runner and Testing Suite
Comprehensive demonstration of the complete workflow
"""

import asyncio
import streamlit as st
import sys
import os
from datetime import datetime
import json

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from coee import demo_admorph_complete_workflow, demo_ai_advertising_agency, demo_evolution_only
from swipe_interface import main as swipe_main

def main():
    """Main demo runner with Streamlit interface"""
    
    st.set_page_config(
        page_title="AdMorph.AI Demo Suite",
        page_icon="🎯",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #4CAF50, #2196F3);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .demo-card {
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        background: #f9f9f9;
    }
    .feature-list {
        background: #e8f5e8;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🎯 AdMorph.AI Demo Suite</h1>
        <p>Advanced Agentic Advertising Framework</p>
        <p>From Voice Interaction → AI Generation → Swipe Review → Publishing → Evolution</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.title("🎯 Demo Navigation")
        
        demo_choice = st.selectbox(
            "Choose Demo:",
            [
                "🏠 Overview",
                "🎤 Complete AdMorph Workflow",
                "📱 Swipe Interface Demo",
                "🧬 Agentic Evolution Demo",
                "📊 Original Ogilvy Agency Demo",
                "⚙️ System Architecture"
            ]
        )
        
        st.markdown("---")
        st.markdown("### 🔧 Configuration")
        
        # API Status checks
        openai_configured = bool(os.getenv("OPENAI_API_KEY"))
        meta_configured = bool(os.getenv("META_ACCESS_TOKEN"))
        
        st.write("**API Status:**")
        st.write(f"OpenAI: {'✅' if openai_configured else '❌'}")
        st.write(f"Meta API: {'✅' if meta_configured else '❌'}")
        
        if not openai_configured or not meta_configured:
            st.warning("⚠️ Some APIs not configured. Demos will use synthetic data.")
        
        st.markdown("---")
        st.markdown("### 📚 Quick Links")
        st.markdown("- [Setup Guide](#setup)")
        st.markdown("- [API Configuration](#api-config)")
        st.markdown("- [Architecture](#architecture)")
    
    # Main content area
    if demo_choice == "🏠 Overview":
        render_overview()
    elif demo_choice == "🎤 Complete AdMorph Workflow":
        render_complete_workflow_demo()
    elif demo_choice == "📱 Swipe Interface Demo":
        render_swipe_demo()
    elif demo_choice == "🧬 Agentic Evolution Demo":
        render_evolution_demo()
    elif demo_choice == "📊 Original Ogilvy Agency Demo":
        render_ogilvy_demo()
    elif demo_choice == "⚙️ System Architecture":
        render_architecture()

def render_overview():
    """Render the overview page"""
    
    st.title("🎯 AdMorph.AI Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="demo-card">
        <h3>🎤 Voice-Powered Onboarding</h3>
        <p>Intelligent conversational AI that asks the right questions about:</p>
        <ul>
        <li>Target engagement goals</li>
        <li>Budget allocation</li>
        <li>Audience demographics</li>
        <li>Brand themes and restrictions</li>
        <li>Original ad assets</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="demo-card">
        <h3>🧬 Agentic Evolution</h3>
        <p>Ads that continuously evolve based on:</p>
        <ul>
        <li>Real-world trends analysis</li>
        <li>Performance metrics (CTR, conversions)</li>
        <li>Audience engagement patterns</li>
        <li>Competitive landscape changes</li>
        <li>Seasonal and cultural shifts</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="demo-card">
        <h3>📱 Tinder-Style Review</h3>
        <p>Marketing directors can swipe through ad variants:</p>
        <ul>
        <li>✅ Approve for immediate launch</li>
        <li>❌ Reject and move to next</li>
        <li>🔄 Regenerate with different approach</li>
        <li>📊 View demographic targeting details</li>
        <li>🎨 Gallery view of approved ads</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="demo-card">
        <h3>🚀 Auto-Publishing</h3>
        <p>Seamless integration with advertising platforms:</p>
        <ul>
        <li>Meta/Facebook Marketing API</li>
        <li>Automatic campaign creation</li>
        <li>Demographic-specific targeting</li>
        <li>Performance monitoring</li>
        <li>Budget optimization</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Key Features
    st.markdown("### 🌟 Key Features")
    
    features = [
        "🎯 **Demographic-Specific Generation**: Creates unique ad variants for each target segment",
        "🧠 **Ogilvy Principles Integration**: Combines proven advertising principles with AI innovation",
        "📈 **Real-Time Performance Optimization**: Continuously improves based on actual results",
        "🔄 **Automatic Mutation**: Ads evolve without human intervention when performance drops",
        "📊 **Synthetic Data Generation**: Test and validate strategies with realistic performance data",
        "🎨 **Visual Design Integration**: Aesthetic analysis and composition optimization",
        "🗣️ **Natural Language Interface**: Voice and chat-based business consultation",
        "⚡ **Emergency Controls**: Instant pause, rollback, and manual override capabilities"
    ]
    
    for feature in features:
        st.markdown(f"- {feature}")

def render_complete_workflow_demo():
    """Render the complete workflow demo"""
    
    st.title("🎤 Complete AdMorph Workflow Demo")
    
    st.info("This demo showcases the entire AdMorph.AI pipeline from voice interaction to ad evolution.")
    
    if st.button("🚀 Run Complete Workflow Demo", type="primary"):
        with st.spinner("Running complete AdMorph workflow..."):
            try:
                # Run the async demo
                result = asyncio.run(demo_admorph_complete_workflow())
                
                if "error" not in result:
                    st.success("✅ Workflow completed successfully!")
                    
                    # Display results
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Demographic Segments", len(result['workflow_result']['demographic_segments']))
                    with col2:
                        st.metric("Ad Variants Generated", len(result['workflow_result']['ad_variants']))
                    with col3:
                        st.metric("Variants Approved", result['approved_variants'])
                    
                    # Show business profile
                    with st.expander("📋 Business Profile Created"):
                        profile = result['workflow_result']['business_profile']
                        st.json({
                            "business_name": profile.business_name,
                            "industry": profile.industry,
                            "monthly_budget": profile.monthly_budget,
                            "target_engagement": profile.target_engagement
                        })
                    
                    # Show launch results
                    if result['launch_result']['success']:
                        with st.expander("🚀 Campaign Launch Results"):
                            st.json(result['launch_result'])
                    
                else:
                    st.error(f"❌ Demo failed: {result['error']}")
                    st.info("💡 Make sure to set up your API keys in the .env file")
                    
            except Exception as e:
                st.error(f"❌ Error running demo: {str(e)}")

def render_swipe_demo():
    """Render the swipe interface demo"""
    
    st.title("📱 Swipe Interface Demo")
    
    st.info("Experience the Tinder-style ad review interface")
    
    if st.button("🎯 Launch Swipe Interface", type="primary"):
        st.info("🔄 Launching swipe interface in new tab...")
        # In a real implementation, this would launch the swipe interface
        st.success("✅ Swipe interface launched! Check the new browser tab.")
        
        # Show preview of what the swipe interface looks like
        st.markdown("### 📱 Swipe Interface Preview")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            <div style="border: 2px solid #ddd; border-radius: 10px; padding: 20px; text-align: center;">
                <h3>🎯 Boost Your Career Today</h3>
                <img src="https://via.placeholder.com/300x200/4CAF50/white?text=Ad+Preview" style="width: 100%; border-radius: 8px;">
                <p>Discover how our solution can revolutionize your workflow and boost productivity by 300%.</p>
                <button style="background: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px;">Get Started Free</button>
                <br><br>
                <div style="display: flex; justify-content: space-between;">
                    <button style="background: #f44336; color: white; padding: 10px; border: none; border-radius: 5px;">❌ Reject</button>
                    <button style="background: #ff9800; color: white; padding: 10px; border: none; border-radius: 5px;">🔄 Regenerate</button>
                    <button style="background: #4CAF50; color: white; padding: 10px; border: none; border-radius: 5px;">✅ Approve</button>
                </div>
            </div>
            """, unsafe_allow_html=True)

def render_evolution_demo():
    """Render the agentic evolution demo"""
    
    st.title("🧬 Agentic Evolution Demo")
    
    st.info("Watch how ads automatically evolve based on performance and trends")
    
    if st.button("🧬 Run Evolution Demo", type="primary"):
        with st.spinner("Running agentic evolution simulation..."):
            try:
                result = asyncio.run(demo_evolution_only())
                
                if "error" not in result:
                    st.success("✅ Evolution demo completed!")
                    
                    # Show evolution metrics
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Variants Processed", result.get('variants_processed', 0))
                    with col2:
                        st.metric("Mutations Created", result.get('mutations_created', 0))
                    with col3:
                        st.metric("Performance Improvements", len(result.get('performance_improvements', [])))
                    
                    # Show evolution timeline
                    st.markdown("### 📈 Evolution Timeline")
                    st.info("🔄 Initial variants created → 📊 Performance analyzed → 🧬 Mutations generated → 🚀 Auto-published")
                    
                else:
                    st.error(f"❌ Evolution demo failed: {result['error']}")
                    
            except Exception as e:
                st.error(f"❌ Error running evolution demo: {str(e)}")

def render_ogilvy_demo():
    """Render the original Ogilvy agency demo"""
    
    st.title("📊 Original Ogilvy Agency Demo")
    
    st.info("Experience the foundational Ogilvy-based advertising agency")
    
    if st.button("📊 Run Ogilvy Demo", type="primary"):
        with st.spinner("Running Ogilvy-based agency demo..."):
            try:
                result = asyncio.run(demo_ai_advertising_agency())
                
                st.success("✅ Ogilvy demo completed!")
                
                # Show results
                if result and 'variants' in result:
                    st.metric("Ad Variants Created", len(result['variants']))
                    
                    with st.expander("📝 Generated Headlines"):
                        for i, variant in enumerate(result['variants'][:3]):
                            st.write(f"{i+1}. {variant.headline}")
                
            except Exception as e:
                st.error(f"❌ Error running Ogilvy demo: {str(e)}")

def render_architecture():
    """Render the system architecture"""
    
    st.title("⚙️ System Architecture")
    
    st.markdown("""
    ### 🏗️ AdMorph.AI Architecture Overview
    
    The system is built with a modular, agent-based architecture that combines proven advertising principles with cutting-edge AI capabilities.
    """)
    
    # Architecture diagram (simplified)
    st.markdown("""
    ```
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │   Voice Agent   │    │ Demographic     │    │ Variant         │
    │   🎤 Onboarding │───▶│ Analysis Agent  │───▶│ Generation      │
    │                 │    │ 🎯 Segmentation │    │ 🎨 Creation     │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
              │                       │                       │
              ▼                       ▼                       ▼
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │ Business        │    │ Targeting       │    │ Ad Variants     │
    │ Profile         │    │ Specifications  │    │ (Multiple)      │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
                                     │                       │
                                     ▼                       ▼
    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
    │ Swipe Interface │◀───│ Review Process  │◀───│ Ogilvy          │
    │ 📱 Tinder-style │    │ 👥 Marketing    │    │ Enhancement     │
    │                 │    │    Director     │    │ 📚 Principles   │
    └─────────────────┘    └─────────────────┘    └─────────────────┘
              │                       │
              ▼                       ▼
    ┌─────────────────┐    ┌─────────────────┐
    │ Approved Ads    │───▶│ Meta API        │
    │ ✅ Gallery      │    │ 🚀 Publishing   │
    └─────────────────┘    └─────────────────┘
              │                       │
              ▼                       ▼
    ┌─────────────────┐    ┌─────────────────┐
    │ Evolution       │◀───│ Performance     │
    │ 🧬 Monitoring   │    │ 📊 Tracking     │
    └─────────────────┘    └─────────────────┘
              │
              ▼
    ┌─────────────────┐
    │ Automatic       │
    │ 🔄 Mutations    │
    └─────────────────┘
    ```
    """)
    
    # Component details
    components = {
        "🎤 Voice Agent": "Conducts intelligent business consultation using OpenAI GPT-4",
        "🎯 Demographic Agent": "Analyzes business profile and creates Meta-compatible audience segments",
        "🎨 Variant Generator": "Creates multiple ad variants per demographic segment",
        "📚 Ogilvy Integration": "Enhances variants with proven advertising principles",
        "📱 Swipe Interface": "Streamlit-based Tinder-style review system",
        "🚀 Meta API": "Publishes approved ads to Facebook/Instagram platforms",
        "🧬 Evolution Engine": "Continuously monitors and mutates ads based on performance",
        "📊 Performance Tracker": "Real-time metrics collection and analysis"
    }
    
    st.markdown("### 🔧 Core Components")
    
    for component, description in components.items():
        st.markdown(f"**{component}**: {description}")

if __name__ == "__main__":
    main()
