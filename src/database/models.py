"""
Database models and schema definitions for competitive analysis
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, date
from pydantic import BaseModel, Field
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class Category(str, Enum):
    AI_RESEARCH = "ai_research"
    PRODUCT_LAUNCH = "product_launch"
    FUNDING = "funding"
    ACQUISITION = "acquisition"
    PARTNERSHIP = "partnership"
    REGULATION = "regulation"
    TECHNOLOGY = "technology"
    MARKET_TREND = "market_trend"

class MarketFinding(BaseModel):
    """Model for market intelligence findings"""
    id: Optional[str] = None
    date: date = Field(default_factory=date.today)
    category: Category
    title: str = Field(max_length=500)
    summary: str = Field(max_length=2000)
    content: str
    relevance_score: float = Field(ge=0.0, le=1.0)
    source_url: Optional[str] = None
    created_at: Optional[datetime] = None

class CompetitorUpdate(BaseModel):
    """Model for competitor intelligence updates"""
    id: Optional[str] = None
    company_name: str = Field(max_length=255)
    update_type: Category
    description: str
    impact_level: Priority
    source_url: Optional[str] = None
    detected_date: date = Field(default_factory=date.today)
    created_at: Optional[datetime] = None

class Opportunity(BaseModel):
    """Model for identified market opportunities"""
    id: Optional[str] = None
    title: str = Field(max_length=255)
    description: str
    market_gap: str
    score: float = Field(ge=0.0, le=1.0)
    priority: Priority
    potential_revenue: Optional[str] = None
    implementation_complexity: Optional[str] = None
    time_to_market: Optional[str] = None
    created_at: Optional[datetime] = None

class Trend(BaseModel):
    """Model for market trends"""
    id: Optional[str] = None
    trend_name: str = Field(max_length=255)
    category: Category
    momentum_score: float = Field(ge=0.0, le=1.0)
    evidence: Dict[str, Any] = Field(default_factory=dict)
    first_detected: date = Field(default_factory=date.today)
    prediction: Optional[str] = None
    created_at: Optional[datetime] = None

class AnalysisRun(BaseModel):
    """Model for analysis execution tracking"""
    id: Optional[str] = None
    run_date: date = Field(default_factory=date.today)
    findings_count: int = 0
    opportunities_identified: int = 0
    key_insights: Optional[str] = None
    recommendations: Dict[str, Any] = Field(default_factory=dict)
    execution_time_seconds: Optional[float] = None
    status: str = "completed"
    created_at: Optional[datetime] = None

# Database schema creation SQL
DATABASE_SCHEMA = """
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
CREATE INDEX IF NOT EXISTS idx_competitor_updates_company ON competitor_updates(company_name);
CREATE INDEX IF NOT EXISTS idx_opportunities_score ON opportunities(score DESC);
CREATE INDEX IF NOT EXISTS idx_trends_momentum ON trends(momentum_score DESC);
"""

def get_sample_data() -> Dict[str, List[Dict[str, Any]]]:
    """Returns sample data for testing purposes"""
    return {
        "market_findings": [
            {
                "date": "2024-01-20",
                "category": "ai_research", 
                "title": "OpenAI Releases GPT-4 Turbo with Enhanced Capabilities",
                "summary": "OpenAI announced GPT-4 Turbo with improved performance and lower costs.",
                "content": "Detailed analysis of the new model capabilities and market implications...",
                "relevance_score": 0.95,
                "source_url": "https://openai.com/blog/gpt-4-turbo"
            }
        ],
        "competitor_updates": [
            {
                "company_name": "OpenAI",
                "update_type": "product_launch",
                "description": "Released GPT-4 Turbo with competitive pricing",
                "impact_level": "high",
                "source_url": "https://openai.com/blog/gpt-4-turbo",
                "detected_date": "2024-01-20"
            }
        ],
        "opportunities": [
            {
                "title": "Enterprise AI Integration Services",
                "description": "Gap in helping mid-size companies integrate AI solutions",
                "market_gap": "Limited affordable AI consulting for mid-market",
                "score": 0.85,
                "priority": "high"
            }
        ],
        "trends": [
            {
                "trend_name": "Multimodal AI Adoption",
                "category": "technology",
                "momentum_score": 0.78,
                "evidence": {"sources": 5, "mentions": 150, "growth_rate": "45%"},
                "first_detected": "2024-01-15",
                "prediction": "Expected to dominate enterprise AI in 2024"
            }
        ]
    }