-- Competitive Analysis System Database Schema
-- Copy and paste this entire file into your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Market findings table
CREATE TABLE IF NOT EXISTS market_findings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date DATE NOT NULL,
    category VARCHAR(50) NOT NULL,
    title TEXT NOT NULL,
    summary TEXT NOT NULL,
    content TEXT NOT NULL,
    relevance_score DECIMAL(3,2) NOT NULL CHECK (relevance_score >= 0 AND relevance_score <= 1),
    source_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Competitor updates table
CREATE TABLE IF NOT EXISTS competitor_updates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_name VARCHAR(255) NOT NULL,
    update_type VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    impact_level VARCHAR(20) NOT NULL,
    source_url TEXT,
    detected_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Opportunities table
CREATE TABLE IF NOT EXISTS opportunities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    market_gap TEXT NOT NULL,
    score DECIMAL(3,2) NOT NULL CHECK (score >= 0 AND score <= 1),
    priority VARCHAR(20) NOT NULL,
    potential_revenue VARCHAR(50),
    implementation_complexity VARCHAR(50),
    time_to_market VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Trends table
CREATE TABLE IF NOT EXISTS trends (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    trend_name VARCHAR(255) NOT NULL,
    category VARCHAR(50) NOT NULL,
    momentum_score DECIMAL(3,2) NOT NULL CHECK (momentum_score >= 0 AND momentum_score <= 1),
    evidence JSON,
    first_detected DATE NOT NULL,
    prediction TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Analysis runs table
CREATE TABLE IF NOT EXISTS analysis_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    run_date DATE NOT NULL,
    findings_count INTEGER DEFAULT 0,
    opportunities_identified INTEGER DEFAULT 0,
    key_insights TEXT,
    recommendations JSON,
    execution_time_seconds DECIMAL(8,2),
    status VARCHAR(20) DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_market_findings_date ON market_findings(date DESC);
CREATE INDEX IF NOT EXISTS idx_market_findings_category ON market_findings(category);
CREATE INDEX IF NOT EXISTS idx_market_findings_relevance ON market_findings(relevance_score DESC);

CREATE INDEX IF NOT EXISTS idx_competitor_updates_company ON competitor_updates(company_name);
CREATE INDEX IF NOT EXISTS idx_competitor_updates_date ON competitor_updates(detected_date DESC);
CREATE INDEX IF NOT EXISTS idx_competitor_updates_impact ON competitor_updates(impact_level);

CREATE INDEX IF NOT EXISTS idx_opportunities_score ON opportunities(score DESC);
CREATE INDEX IF NOT EXISTS idx_opportunities_priority ON opportunities(priority);
CREATE INDEX IF NOT EXISTS idx_opportunities_date ON opportunities(created_at DESC);

CREATE INDEX IF NOT EXISTS idx_trends_momentum ON trends(momentum_score DESC);
CREATE INDEX IF NOT EXISTS idx_trends_category ON trends(category);
CREATE INDEX IF NOT EXISTS idx_trends_date ON trends(first_detected DESC);

CREATE INDEX IF NOT EXISTS idx_analysis_runs_date ON analysis_runs(run_date DESC);
CREATE INDEX IF NOT EXISTS idx_analysis_runs_status ON analysis_runs(status);

-- Insert sample data for testing
INSERT INTO market_findings (date, category, title, summary, content, relevance_score, source_url) VALUES
('2024-01-20', 'ai_research', 'OpenAI Releases GPT-4 Turbo with Enhanced Capabilities', 'OpenAI announced GPT-4 Turbo with improved performance and lower costs.', 'OpenAI has released GPT-4 Turbo, featuring enhanced capabilities including longer context windows, improved accuracy, and reduced pricing. This represents a significant advancement in large language model technology with potential implications for enterprise AI adoption.', 0.95, 'https://openai.com/blog/gpt-4-turbo'),
('2024-01-19', 'funding', 'AI Startup Raises $50M Series B for Enterprise Solutions', 'New AI company secures major funding round for B2B AI platform.', 'An emerging AI startup focused on enterprise automation solutions has successfully raised $50M in Series B funding, led by prominent venture capital firms. The funding will accelerate product development and market expansion.', 0.78, 'https://techcrunch.com/example'),
('2024-01-18', 'regulation', 'EU AI Act Implementation Guidelines Released', 'European Union provides detailed guidance on AI Act compliance.', 'The European Union has released comprehensive implementation guidelines for the AI Act, providing clarity on compliance requirements for AI systems deployed in EU markets. This will significantly impact how AI companies operate in Europe.', 0.82, 'https://ec.europa.eu/example');

INSERT INTO competitor_updates (company_name, update_type, description, impact_level, source_url, detected_date) VALUES
('OpenAI', 'product_launch', 'Released GPT-4 Turbo with competitive pricing and enhanced capabilities', 'high', 'https://openai.com/blog/gpt-4-turbo', '2024-01-20'),
('Anthropic', 'partnership', 'Announced strategic partnership with major cloud provider for enterprise AI', 'medium', 'https://anthropic.com/news/partnership', '2024-01-19'),
('Google AI', 'product_launch', 'Launched new Gemini Pro model with multimodal capabilities', 'high', 'https://deepmind.google/gemini', '2024-01-18');

INSERT INTO opportunities (title, description, market_gap, score, priority, potential_revenue, implementation_complexity, time_to_market) VALUES
('Enterprise AI Integration Services', 'Comprehensive AI integration consulting for mid-market companies lacking internal AI expertise', 'Limited affordable AI consulting for companies with 100-1000 employees', 0.85, 'high', '$500K-2M annually', 'medium', '3-6 months'),
('Industry-Specific AI Solutions', 'Vertical AI solutions tailored for healthcare, finance, and manufacturing sectors', 'Generic AI tools lacking industry-specific customization and compliance', 0.78, 'high', '$1M-5M annually', 'high', '6-12 months'),
('AI Training and Certification Platform', 'Online platform for AI skills development and certification for professionals', 'Gap in structured, practical AI education for working professionals', 0.72, 'medium', '$200K-800K annually', 'medium', '4-8 months');

INSERT INTO trends (trend_name, category, momentum_score, evidence, first_detected, prediction) VALUES
('Multimodal AI Adoption', 'technology', 0.88, '{"sources": 15, "mentions": 250, "growth_rate": "65%", "investment": "$2.3B"}', '2024-01-15', 'Multimodal AI will become standard for enterprise applications by 2025, driving demand for integration services'),
('AI Regulation Compliance', 'regulation', 0.75, '{"regulatory_changes": 8, "compliance_demand": "high", "market_size": "$500M"}', '2024-01-10', 'Growing regulatory requirements will create significant demand for AI compliance consulting and tools'),
('Edge AI Deployment', 'technology', 0.82, '{"hardware_adoption": "45%", "latency_requirements": "critical", "cost_reduction": "30%"}', '2024-01-12', 'Edge AI deployment will accelerate as latency and privacy concerns drive on-device processing needs');

INSERT INTO analysis_runs (run_date, findings_count, opportunities_identified, key_insights, recommendations, execution_time_seconds, status) VALUES
('2024-01-20', 12, 3, 'Market showing increased AI adoption in enterprise sector with focus on compliance and integration', '["Develop compliance-focused AI solutions", "Expand integration service offerings", "Monitor regulatory developments closely"]', 45.7, 'completed');