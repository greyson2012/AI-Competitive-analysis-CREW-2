-- TABLES ONLY - Run this first to create tables without data
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