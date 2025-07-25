"""
Company context configuration for competitive analysis
"""
import os
from typing import Dict, List, Any
from dotenv import load_dotenv

load_dotenv()

def get_company_context() -> Dict[str, Any]:
    """Load company context from environment variables"""
    return {
        "name": os.getenv("COMPANY_NAME", "Your AI Company"),
        "industry": os.getenv("COMPANY_INDUSTRY", "AI/Technology"),
        "core_competencies": [
            "Enterprise AI Solutions",
            "Custom LLM Development", 
            "AI Agent Systems",
            "Data Analytics & ML",
            "AI Strategy Consulting"
        ],
        "target_industries": os.getenv("TARGET_INDUSTRIES", "Financial Services,Healthcare,E-commerce").split(","),
        "current_offerings": [
            "AI Strategy Consulting",
            "Custom AI Agent Development",
            "LLM Fine-tuning Services",
            "AI Integration Solutions",
            "Competitive Intelligence Systems"
        ],
        "competitive_advantages": [
            "Domain expertise in AI agents",
            "Rapid prototyping capabilities",
            "Enterprise-grade security",
            "Cost-effective solutions",
            "Proven track record"
        ],
        "growth_objectives": [
            "Market share expansion",
            "New service development",
            "Geographic expansion",
            "Technology leadership",
            "Strategic partnerships"
        ],
        "competitors": os.getenv("COMPETITORS", "OpenAI,Anthropic,Google AI").split(","),
        "focus_keywords": [
            "artificial intelligence",
            "machine learning",
            "AI agents",
            "enterprise AI",
            "LLM",
            "automation",
            "intelligent systems",
            "AI consulting",
            "competitive intelligence"
        ]
    }

def get_analysis_prompts() -> Dict[str, str]:
    """Get context-aware prompts for different analysis types"""
    context = get_company_context()
    
    return {
        "market_intelligence": f"""
        You are analyzing market intelligence for {context['name']}, a company specializing in {', '.join(context['core_competencies'])}.
        
        Focus on developments that could impact our target industries: {', '.join(context['target_industries'])}.
        
        Key areas of interest:
        - New AI technologies and breakthroughs
        - Funding rounds and acquisitions in AI space
        - Regulatory changes affecting AI deployment
        - Enterprise adoption trends
        - Competitive landscape shifts
        
        Rate relevance from 0.0 to 1.0 based on direct impact to our business.
        """,
        
        "competitor_analysis": f"""
        You are monitoring competitors for {context['name']}.
        
        Primary competitors to track: {', '.join(context['competitors'])}
        
        Focus on:
        - Product launches and feature updates
        - Pricing strategy changes
        - Market positioning shifts
        - Partnership announcements
        - Hiring patterns and team expansion
        - Customer wins and case studies
        
        Assess impact level (low/medium/high/critical) based on threat to our market position.
        """,
        
        "trend_analysis": f"""
        You are identifying trends that could create opportunities for {context['name']}.
        
        Our competitive advantages: {', '.join(context['competitive_advantages'])}
        Our growth objectives: {', '.join(context['growth_objectives'])}
        
        Look for:
        - Emerging technology trends
        - Market gaps and unmet needs
        - Industry adoption patterns
        - Customer behavior shifts
        - Regulatory trends
        
        Calculate momentum score (0.0-1.0) based on trend strength and growth trajectory.
        """,
        
        "strategic_synthesis": f"""
        You are a strategic advisor for {context['name']}, synthesizing intelligence into actionable insights.
        
        Company focus: {context['industry']} serving {', '.join(context['target_industries'])}
        Current offerings: {', '.join(context['current_offerings'])}
        
        Your task:
        1. Identify market opportunities that align with our capabilities
        2. Assess competitive threats and response strategies
        3. Recommend strategic initiatives for growth
        4. Prioritize actions based on impact and feasibility
        
        Score opportunities (0.0-1.0) based on:
        - Market size and growth potential (25%)
        - Competitive landscape favorability (20%)
        - Technical fit with our capabilities (20%)
        - Time to market advantage (15%)
        - Strategic alignment with objectives (20%)
        """
    }

# Global context instance
COMPANY_CONTEXT = get_company_context()
ANALYSIS_PROMPTS = get_analysis_prompts()