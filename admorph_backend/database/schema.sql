-- =============================================================================
-- 🤖 AdMorph.AI Unified Database Schema
-- =============================================================================
-- Complete database schema for the integrated AdMorph.AI platform
-- Supports: Advertising, E-commerce Personalization, Analytics, A/B Testing
-- =============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- 👤 BUSINESS & USER MANAGEMENT
-- =============================================================================

-- Business profiles table
CREATE TABLE business_profiles (
    business_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_name VARCHAR(255) NOT NULL,
    industry VARCHAR(100) NOT NULL,
    description TEXT,
    target_audience JSONB,
    monthly_budget DECIMAL(12,2),
    campaign_goals TEXT[],
    brand_voice VARCHAR(100),
    unique_selling_points TEXT[],
    competitors TEXT[],
    geographic_focus TEXT[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Business insights table (AI-generated)
CREATE TABLE business_insights (
    insight_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID REFERENCES business_profiles(business_id) ON DELETE CASCADE,
    industry_analysis TEXT,
    target_market_analysis TEXT,
    competitive_advantages TEXT[],
    recommended_strategies TEXT[],
    risk_factors TEXT[],
    growth_opportunities TEXT[],
    confidence_score DECIMAL(3,2),
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- 🎯 DEMOGRAPHIC & AUDIENCE MANAGEMENT
-- =============================================================================

-- Demographic segments table
CREATE TABLE demographic_segments (
    segment_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID REFERENCES business_profiles(business_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    age_range_min INTEGER,
    age_range_max INTEGER,
    gender VARCHAR(50),
    income_range VARCHAR(100),
    interests TEXT[],
    behaviors TEXT[],
    location_data JSONB,
    psychographics JSONB,
    size_estimate INTEGER,
    meta_targeting_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- 🎨 AD MANAGEMENT & VARIANTS
-- =============================================================================

-- Ad variants table
CREATE TABLE ad_variants (
    variant_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID REFERENCES business_profiles(business_id) ON DELETE CASCADE,
    demographic_segment_id UUID REFERENCES demographic_segments(segment_id),
    headline VARCHAR(500) NOT NULL,
    body TEXT NOT NULL,
    cta VARCHAR(200) NOT NULL,
    image_url VARCHAR(500),
    aesthetic_score DECIMAL(3,2),
    ogilvy_score DECIMAL(3,2),
    emotional_impact DECIMAL(3,2),
    format_type VARCHAR(50) DEFAULT 'social',
    generation_strategy VARCHAR(100) DEFAULT 'default',
    mutation_history JSONB DEFAULT '[]',
    performance_score DECIMAL(3,2) DEFAULT 0.0,
    trend_alignment DECIMAL(3,2) DEFAULT 0.0,
    meta_campaign_id VARCHAR(255),
    is_published BOOLEAN DEFAULT FALSE,
    swipe_status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Ad performance metrics table
CREATE TABLE ad_performance_metrics (
    metric_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    variant_id UUID REFERENCES ad_variants(variant_id) ON DELETE CASCADE,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    ctr DECIMAL(5,4) DEFAULT 0.0,
    conversions INTEGER DEFAULT 0,
    engagement_rate DECIMAL(5,4) DEFAULT 0.0,
    cost_per_acquisition DECIMAL(10,2) DEFAULT 0.0,
    spend DECIMAL(10,2) DEFAULT 0.0,
    revenue DECIMAL(10,2),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- 🛍️ E-COMMERCE PERSONALIZATION
-- =============================================================================

-- Base products table
CREATE TABLE base_products (
    product_id VARCHAR(255) PRIMARY KEY,
    business_id UUID REFERENCES business_profiles(business_id) ON DELETE CASCADE,
    name VARCHAR(500) NOT NULL,
    description TEXT,
    price DECIMAL(10,2),
    category VARCHAR(255),
    features TEXT[],
    images TEXT[],
    platform VARCHAR(100), -- 'shopify', 'amazon', 'woocommerce', etc.
    platform_product_id VARCHAR(255),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Product variants (personalized versions)
CREATE TABLE product_variants (
    variant_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id VARCHAR(255) REFERENCES base_products(product_id) ON DELETE CASCADE,
    demographic_segment_id UUID REFERENCES demographic_segments(segment_id),
    personalized_title VARCHAR(500),
    personalized_description TEXT,
    highlighted_features TEXT[],
    personalized_cta VARCHAR(200),
    price_positioning VARCHAR(100),
    urgency_messaging VARCHAR(500),
    social_proof TEXT[],
    personalization_score DECIMAL(3,2),
    conversion_lift_estimate DECIMAL(5,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Product performance tracking
CREATE TABLE product_performance (
    performance_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    variant_id UUID REFERENCES product_variants(variant_id) ON DELETE CASCADE,
    views INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    purchases INTEGER DEFAULT 0,
    revenue DECIMAL(10,2) DEFAULT 0.0,
    conversion_rate DECIMAL(5,4) DEFAULT 0.0,
    bounce_rate DECIMAL(5,4) DEFAULT 0.0,
    time_on_page INTEGER DEFAULT 0,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- 🧪 A/B TESTING & EXPERIMENTATION
-- =============================================================================

-- A/B tests table
CREATE TABLE ab_tests (
    test_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID REFERENCES business_profiles(business_id) ON DELETE CASCADE,
    test_name VARCHAR(255) NOT NULL,
    test_type VARCHAR(50) NOT NULL, -- 'ad_variant', 'product_variant'
    variant_ids UUID[],
    test_config JSONB,
    status VARCHAR(50) DEFAULT 'running', -- 'running', 'completed', 'paused'
    winner_variant_id UUID,
    statistical_significance DECIMAL(5,4),
    improvement_percentage DECIMAL(5,2),
    start_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    end_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- A/B test results table
CREATE TABLE ab_test_results (
    result_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    test_id UUID REFERENCES ab_tests(test_id) ON DELETE CASCADE,
    variant_id UUID,
    participants INTEGER,
    conversions INTEGER,
    conversion_rate DECIMAL(5,4),
    confidence_interval JSONB,
    p_value DECIMAL(10,8),
    recorded_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- 🚀 CAMPAIGNS & PUBLISHING
-- =============================================================================

-- Campaigns table
CREATE TABLE campaigns (
    campaign_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID REFERENCES business_profiles(business_id) ON DELETE CASCADE,
    campaign_name VARCHAR(255) NOT NULL,
    campaign_type VARCHAR(50) NOT NULL, -- 'advertising', 'ecommerce'
    platform VARCHAR(100), -- 'meta', 'shopify', 'amazon', etc.
    platform_campaign_id VARCHAR(255),
    budget DECIMAL(10,2),
    start_date TIMESTAMP WITH TIME ZONE,
    end_date TIMESTAMP WITH TIME ZONE,
    status VARCHAR(50) DEFAULT 'draft', -- 'draft', 'active', 'paused', 'completed'
    objectives TEXT[],
    target_demographics UUID[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Campaign performance summary
CREATE TABLE campaign_performance (
    performance_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    campaign_id UUID REFERENCES campaigns(campaign_id) ON DELETE CASCADE,
    total_spend DECIMAL(10,2) DEFAULT 0.0,
    total_revenue DECIMAL(10,2) DEFAULT 0.0,
    total_impressions INTEGER DEFAULT 0,
    total_clicks INTEGER DEFAULT 0,
    total_conversions INTEGER DEFAULT 0,
    average_ctr DECIMAL(5,4) DEFAULT 0.0,
    average_conversion_rate DECIMAL(5,4) DEFAULT 0.0,
    roi DECIMAL(5,2) DEFAULT 0.0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- 🤖 AI AGENT INTERACTIONS & JOBS
-- =============================================================================

-- Agent sessions table (for chat and voice interactions)
CREATE TABLE agent_sessions (
    session_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID REFERENCES business_profiles(business_id),
    session_type VARCHAR(50) NOT NULL, -- 'chat', 'voice', 'onboarding'
    agent_type VARCHAR(100), -- 'business_analysis', 'ad_generation', etc.
    conversation_history JSONB DEFAULT '[]',
    session_data JSONB,
    status VARCHAR(50) DEFAULT 'active', -- 'active', 'completed', 'abandoned'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Background jobs table
CREATE TABLE background_jobs (
    job_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID REFERENCES business_profiles(business_id),
    job_type VARCHAR(100) NOT NULL, -- 'ad_generation', 'product_personalization', etc.
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'running', 'completed', 'failed'
    input_data JSONB,
    result_data JSONB,
    error_message TEXT,
    progress_percentage INTEGER DEFAULT 0,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =============================================================================
-- 📊 ANALYTICS & REPORTING
-- =============================================================================

-- Daily analytics summary
CREATE TABLE daily_analytics (
    analytics_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID REFERENCES business_profiles(business_id) ON DELETE CASCADE,
    date DATE NOT NULL,
    total_impressions INTEGER DEFAULT 0,
    total_clicks INTEGER DEFAULT 0,
    total_conversions INTEGER DEFAULT 0,
    total_spend DECIMAL(10,2) DEFAULT 0.0,
    total_revenue DECIMAL(10,2) DEFAULT 0.0,
    average_ctr DECIMAL(5,4) DEFAULT 0.0,
    average_conversion_rate DECIMAL(5,4) DEFAULT 0.0,
    roi DECIMAL(5,2) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(business_id, date)
);

-- =============================================================================
-- 🔍 INDEXES FOR PERFORMANCE
-- =============================================================================

-- Business profiles indexes
CREATE INDEX idx_business_profiles_industry ON business_profiles(industry);
CREATE INDEX idx_business_profiles_created_at ON business_profiles(created_at);

-- Ad variants indexes
CREATE INDEX idx_ad_variants_business_id ON ad_variants(business_id);
CREATE INDEX idx_ad_variants_demographic_segment_id ON ad_variants(demographic_segment_id);
CREATE INDEX idx_ad_variants_performance_score ON ad_variants(performance_score);
CREATE INDEX idx_ad_variants_created_at ON ad_variants(created_at);

-- Product variants indexes
CREATE INDEX idx_product_variants_product_id ON product_variants(product_id);
CREATE INDEX idx_product_variants_demographic_segment_id ON product_variants(demographic_segment_id);
CREATE INDEX idx_product_variants_personalization_score ON product_variants(personalization_score);

-- Performance metrics indexes
CREATE INDEX idx_ad_performance_metrics_variant_id ON ad_performance_metrics(variant_id);
CREATE INDEX idx_ad_performance_metrics_timestamp ON ad_performance_metrics(timestamp);
CREATE INDEX idx_product_performance_variant_id ON product_performance(variant_id);
CREATE INDEX idx_product_performance_timestamp ON product_performance(timestamp);

-- Campaign indexes
CREATE INDEX idx_campaigns_business_id ON campaigns(business_id);
CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_campaigns_platform ON campaigns(platform);

-- Analytics indexes
CREATE INDEX idx_daily_analytics_business_id_date ON daily_analytics(business_id, date);
CREATE INDEX idx_daily_analytics_date ON daily_analytics(date);

-- =============================================================================
-- 🔄 TRIGGERS FOR AUTOMATIC UPDATES
-- =============================================================================

-- Update timestamp trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update triggers to relevant tables
CREATE TRIGGER update_business_profiles_updated_at BEFORE UPDATE ON business_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_demographic_segments_updated_at BEFORE UPDATE ON demographic_segments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_ad_variants_updated_at BEFORE UPDATE ON ad_variants FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_base_products_updated_at BEFORE UPDATE ON base_products FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_product_variants_updated_at BEFORE UPDATE ON product_variants FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_campaigns_updated_at BEFORE UPDATE ON campaigns FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_agent_sessions_updated_at BEFORE UPDATE ON agent_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- 📝 SAMPLE DATA FOR DEVELOPMENT
-- =============================================================================

-- Insert sample business profile
INSERT INTO business_profiles (
    business_name, industry, description, target_audience, monthly_budget,
    campaign_goals, brand_voice, unique_selling_points, competitors, geographic_focus
) VALUES (
    'TechStart Solutions',
    'Technology',
    'AI-powered business automation tools for small businesses',
    '{"age_range": [25, 45], "interests": ["technology", "business", "automation"]}',
    5000.00,
    ARRAY['increase_brand_awareness', 'generate_leads', 'drive_conversions'],
    'professional_friendly',
    ARRAY['AI-powered automation', '24/7 support', 'Easy integration'],
    ARRAY['Zapier', 'Microsoft Power Automate', 'IFTTT'],
    ARRAY['United States', 'Canada', 'United Kingdom']
);

-- =============================================================================
-- ✅ SCHEMA COMPLETE
-- =============================================================================
-- This schema supports:
-- ✅ Business profile management
-- ✅ AI-powered ad generation and optimization
-- ✅ E-commerce product personalization
-- ✅ A/B testing and experimentation
-- ✅ Multi-platform campaign management
-- ✅ Real-time performance analytics
-- ✅ Agent interactions and background jobs
-- ✅ Comprehensive reporting and insights
-- =============================================================================
