# 🎯 AdMorph.AI - Advanced Agentic Advertising Framework

> **Intelligent advertising that evolves automatically**  
> From voice interaction → AI generation → swipe review → publishing → continuous evolution

AdMorph.AI is a cutting-edge advertising framework that combines David Ogilvy's proven principles with modern AI agents to create, optimize, and evolve advertising campaigns automatically.

## 🌟 Key Features

### 🎤 **Voice-Powered Onboarding**
- Intelligent conversational AI consultation
- Extracts business goals, budget, audience, and brand themes
- Natural language processing for business profiling

### 🎯 **Demographic-Specific Generation**
- Creates unique ad variants for each target segment
- Meta/Facebook API integration for precise targeting
- Age, interest, behavior, and income-based segmentation

### 📱 **Tinder-Style Review Interface**
- Marketing directors swipe through ad variants
- ✅ Approve, ❌ Reject, or 🔄 Regenerate options
- Gallery view of approved ads before launch

### 🚀 **Automatic Publishing**
- Seamless Meta Marketing API integration
- Campaign creation and management
- Real-time performance monitoring

### 🧬 **Agentic Evolution**
- Ads continuously evolve based on performance
- Trend analysis and adaptation
- Automatic mutations when performance drops
- Emergency rollback capabilities

## 🏗️ Architecture

```
Voice Agent → Demographic Analysis → Variant Generation → Swipe Review → Publishing → Evolution
     🎤              🎯                    🎨               📱           🚀          🧬
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone the repository
git clone <repository-url>
cd Agents_admorph

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Setup

Copy `.env.example` to `.env` and configure your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview

# Meta/Facebook Marketing API
META_ACCESS_TOKEN=your_meta_access_token_here
META_APP_ID=your_meta_app_id_here
META_APP_SECRET=your_meta_app_secret_here
META_AD_ACCOUNT_ID=your_ad_account_id_here
```

### 3. Run Demos

#### Option A: Interactive Demo Suite (Recommended)
```bash
streamlit run demo_runner.py
```

#### Option B: Command Line Demos
```bash
# Complete AdMorph workflow
python coee.py 1

# Original Ogilvy agency demo
python coee.py 2

# Agentic evolution only
python coee.py 3
```

#### Option C: Swipe Interface Only
```bash
streamlit run swipe_interface.py
```

## 📋 API Configuration

### OpenAI API Setup
1. Get API key from [OpenAI Platform](https://platform.openai.com/)
2. Add to `.env` file as `OPENAI_API_KEY`

### Meta Marketing API Setup
1. Create a Facebook App at [Facebook Developers](https://developers.facebook.com/)
2. Get Marketing API access
3. Generate access token with `ads_management` permissions
4. Add credentials to `.env` file

## 🎯 Usage Examples

### Complete Workflow
```python
from coee import AIAdvertisingAgency

# Initialize the agency
agency = AIAdvertisingAgency()

# Run complete AdMorph workflow
result = await agency.launch_admorph_campaign()
```

### Voice Interface Only
```python
from admorph_core import AdMorphVoiceAgent

# Initialize voice agent
voice_agent = AdMorphVoiceAgent()

# Start onboarding
result = await voice_agent.execute({"stage": "start"})
```

### Agentic Evolution
```python
from agentic_evolution import EvolutionOrchestrator

# Initialize evolution system
orchestrator = EvolutionOrchestrator()

# Start evolution cycle
result = await orchestrator.start_evolution_cycle(variants, business_profile)
```

## 🧬 How Agentic Evolution Works

1. **Performance Monitoring**: Continuously tracks CTR, conversions, engagement
2. **Trend Analysis**: Analyzes social, cultural, economic, and seasonal trends
3. **Mutation Generation**: Creates improved variants based on performance insights
4. **Auto-Publishing**: Publishes high-confidence mutations automatically
5. **Emergency Controls**: Instant rollback if performance degrades

### Evolution Triggers
- **Low CTR** → More compelling headlines
- **Low Conversion** → Stronger value propositions
- **High Cost** → Targeting optimization
- **Trend Shifts** → Message adaptation
- **Performance Decline** → Emergency rollback

## 📊 System Components

### Core Files
- `coee.py` - Main framework with Ogilvy principles
- `admorph_core.py` - OpenAI-powered agents and data models
- `swipe_interface.py` - Tinder-style review interface
- `meta_api_integration.py` - Facebook/Meta API integration
- `agentic_evolution.py` - Continuous evolution system
- `demo_runner.py` - Comprehensive demo suite

### Agent Types
- **Voice Agent** - Business consultation and profiling
- **Demographic Agent** - Audience segmentation and targeting
- **Variant Generator** - Ad creation for specific segments
- **Copywriter Agent** - Ogilvy-based copy optimization
- **Art Director Agent** - Visual design and composition
- **Performance Agent** - Metrics analysis and optimization
- **Mutation Agent** - Intelligent ad evolution
- **Trend Agent** - Real-world trend analysis

## 🎨 Swipe Interface Features

- **Card-based Design** - Clean, mobile-friendly interface
- **Demographic Info** - Target segment details in sidebar
- **Performance Scores** - Aesthetic, Ogilvy, and emotional impact metrics
- **Batch Operations** - Review multiple variants efficiently
- **Gallery View** - Visual overview of approved ads
- **Export Options** - Save campaigns and generate reports

## 📈 Performance Optimization

### Automatic Optimizations
- **Headline Testing** - A/B test different approaches
- **CTA Optimization** - Improve conversion rates
- **Audience Refinement** - Better demographic targeting
- **Budget Allocation** - Optimize spend across segments
- **Creative Refresh** - Prevent ad fatigue

### Manual Controls
- **Emergency Pause** - Stop all campaigns instantly
- **Rollback** - Return to previous version
- **Budget Adjustment** - Real-time spend control
- **Targeting Override** - Manual audience changes

## 🔧 Development

### Project Structure
```
Agents_admorph/
├── coee.py                 # Main framework
├── admorph_core.py         # Core agents and models
├── swipe_interface.py      # Review interface
├── meta_api_integration.py # Meta API client
├── agentic_evolution.py    # Evolution system
├── demo_runner.py          # Demo suite
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
└── README.md              # This file
```

### Adding New Agents
1. Inherit from `OpenAIAgent` base class
2. Implement `execute()` method
3. Add to orchestrator workflow
4. Update demo suite

### Extending Evolution
1. Add new mutation strategies
2. Implement trend analysis sources
3. Create performance triggers
4. Add monitoring capabilities

## 🚨 Troubleshooting

### Common Issues

**"OpenAI API Error"**
- Check API key in `.env` file
- Verify OpenAI account has credits
- Ensure model access (GPT-4)

**"Meta API Error"**
- Verify Meta app permissions
- Check access token validity
- Confirm ad account ID format

**"Import Errors"**
- Run `pip install -r requirements.txt`
- Check Python version (3.8+)
- Verify all files are present

### Debug Mode
```python
import os
os.environ["DEBUG"] = "true"
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **David Ogilvy** - Foundational advertising principles
- **OpenAI** - GPT-4 language model
- **Meta** - Marketing API platform
- **Streamlit** - Interactive demo interface

---

**Built with ❤️ for the future of advertising**
