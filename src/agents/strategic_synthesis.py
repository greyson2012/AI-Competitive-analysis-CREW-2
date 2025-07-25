"""
Strategic Synthesis Agent for comprehensive analysis and recommendations
"""
from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List
import os
from datetime import datetime, date, timedelta
import json

from ..config.company_context import COMPANY_CONTEXT, ANALYSIS_PROMPTS
from ..database.supabase_client import db_client
from ..database.models import Opportunity, Priority

class StrategicSynthesisAgent:
    """Agent responsible for synthesizing insights into strategic recommendations"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-o3",
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.agent = Agent(
            role="Strategic Business Advisor",
            goal="""Synthesize market intelligence, competitive analysis, and trend data into 
            strategic recommendations and actionable business opportunities that align 
            with company capabilities and growth objectives.""",
            
            backstory=ANALYSIS_PROMPTS["strategic_synthesis"],
            
            tools=[],  # This agent primarily analyzes existing data
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            memory=True
        )
    
    async def generate_strategic_analysis(self) -> Dict[str, Any]:
        """Main method to synthesize all intelligence into strategic recommendations"""
        try:
            # Gather all relevant data
            recent_findings = await db_client.get_market_findings(
                limit=30,
                start_date=(date.today() - timedelta(days=30))
            )
            
            competitor_updates = await db_client.get_competitor_updates(limit=20)
            current_trends = await db_client.get_trends(min_momentum=0.4, limit=15)
            existing_opportunities = await db_client.get_opportunities(limit=10)
            
            # Generate comprehensive strategic analysis
            strategic_analysis = await self._synthesize_intelligence(
                recent_findings, competitor_updates, current_trends, existing_opportunities
            )
            
            # Identify and score new opportunities
            new_opportunities = await self._identify_opportunities(strategic_analysis)
            
            # Store new opportunities in database
            stored_opportunities = []
            for opportunity in new_opportunities:
                try:
                    opp_model = Opportunity(
                        title=opportunity.get("title", "")[:255],
                        description=opportunity.get("description", ""),
                        market_gap=opportunity.get("market_gap", ""),
                        score=float(opportunity.get("score", 0.0)),
                        priority=Priority(opportunity.get("priority", "medium")),
                        potential_revenue=opportunity.get("potential_revenue"),
                        implementation_complexity=opportunity.get("implementation_complexity"),
                        time_to_market=opportunity.get("time_to_market")
                    )
                    
                    stored_opp = await db_client.insert_opportunity(opp_model.dict())
                    if stored_opp:
                        stored_opportunities.append(stored_opp)
                        
                except Exception as e:
                    print(f"Error storing opportunity: {e}")
                    continue
            
            return {
                "agent": "strategic_synthesis",
                "timestamp": datetime.now().isoformat(),
                "executive_summary": strategic_analysis.get("executive_summary", ""),
                "strategic_insights": strategic_analysis.get("strategic_insights", []),
                "new_opportunities": len(stored_opportunities),
                "top_opportunities": stored_opportunities[:5],
                "strategic_recommendations": strategic_analysis.get("recommendations", []),
                "competitive_positioning": strategic_analysis.get("competitive_positioning", ""),
                "risk_assessment": strategic_analysis.get("risk_assessment", []),
                "action_plan": strategic_analysis.get("action_plan", [])
            }
            
        except Exception as e:
            print(f"Error in strategic synthesis: {e}")
            return {
                "agent": "strategic_synthesis",
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "new_opportunities": 0
            }
    
    async def _synthesize_intelligence(self,
                                     market_findings: List[Dict[str, Any]],
                                     competitor_updates: List[Dict[str, Any]],
                                     trends: List[Dict[str, Any]],
                                     existing_opportunities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Synthesize all intelligence data into strategic insights"""
        
        synthesis_prompt = f"""
        As a strategic advisor, synthesize the following intelligence data into actionable strategic insights:
        
        MARKET INTELLIGENCE (Last 30 days):
        {json.dumps(market_findings[:15], indent=2, default=str)}
        
        COMPETITOR UPDATES:
        {json.dumps(competitor_updates[:15], indent=2, default=str)}
        
        MARKET TRENDS:
        {json.dumps(trends[:10], indent=2, default=str)}
        
        EXISTING OPPORTUNITIES:
        {json.dumps(existing_opportunities[:5], indent=2, default=str)}
        
        COMPANY CONTEXT:
        - Name: {COMPANY_CONTEXT['name']}
        - Core competencies: {', '.join(COMPANY_CONTEXT['core_competencies'])}
        - Target industries: {', '.join(COMPANY_CONTEXT['target_industries'])}
        - Competitive advantages: {', '.join(COMPANY_CONTEXT['competitive_advantages'])}
        - Growth objectives: {', '.join(COMPANY_CONTEXT['growth_objectives'])}
        - Current offerings: {', '.join(COMPANY_CONTEXT['current_offerings'])}
        
        Provide strategic analysis in JSON format:
        {{
            "executive_summary": "3-4 sentence summary of key strategic insights",
            "strategic_insights": [
                "Key insight 1 with business implications",
                "Key insight 2 with business implications",
                "Key insight 3 with business implications"
            ],
            "market_dynamics": "Analysis of current market dynamics and forces",
            "competitive_positioning": "Assessment of our competitive position and recommendations",
            "opportunity_themes": [
                {{
                    "theme": "Major opportunity theme",
                    "description": "Detailed description",
                    "market_drivers": ["What's driving this opportunity"],
                    "alignment_score": 0.85,
                    "potential_impact": "high|medium|low"
                }}
            ],
            "recommendations": [
                {{
                    "action": "Specific strategic recommendation",
                    "rationale": "Why this is important now",
                    "priority": "high|medium|low",
                    "timeline": "immediate|short-term|medium-term|long-term",
                    "resources_required": "Estimated resources needed",
                    "expected_outcome": "What success looks like"
                }}
            ],
            "risk_assessment": [
                {{
                    "risk": "Identified strategic risk",
                    "impact": "high|medium|low",
                    "probability": "high|medium|low",
                    "mitigation": "Recommended mitigation strategy"
                }}
            ],
            "action_plan": [
                {{
                    "phase": "Phase 1: Discovery|Phase 2: Development|Phase 3: Launch",
                    "actions": ["Specific actions for this phase"],
                    "timeline": "Timeline estimate",
                    "success_metrics": ["How to measure success"]
                }}
            ]
        }}
        
        Focus on actionable insights that leverage our competitive advantages and align with growth objectives.
        """
        
        try:
            response = self.llm.invoke(synthesis_prompt)
            return json.loads(response.content)
        except Exception as e:
            print(f"Error in intelligence synthesis: {e}")
            return {
                "executive_summary": "Error in strategic synthesis",
                "strategic_insights": [],
                "recommendations": []
            }
    
    async def _identify_opportunities(self, strategic_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify specific business opportunities based on strategic analysis"""
        
        opportunity_prompt = f"""
        Based on the strategic analysis, identify specific, actionable business opportunities:
        
        Strategic Analysis:
        {json.dumps(strategic_analysis, indent=2)}
        
        Company Capabilities:
        - Core competencies: {', '.join(COMPANY_CONTEXT['core_competencies'])}
        - Competitive advantages: {', '.join(COMPANY_CONTEXT['competitive_advantages'])}
        - Current offerings: {', '.join(COMPANY_CONTEXT['current_offerings'])}
        
        Identify opportunities and provide detailed analysis in JSON format:
        {{
            "opportunities": [
                {{
                    "title": "Opportunity title (max 255 chars)",
                    "description": "Detailed description of the opportunity",
                    "market_gap": "Specific market gap this addresses",
                    "score": 0.85,
                    "priority": "high|medium|low",
                    "potential_revenue": "$500K-1M annually",
                    "implementation_complexity": "low|medium|high",
                    "time_to_market": "3-6 months",
                    "strategic_rationale": "Why this opportunity aligns with our strategy",
                    "market_validation": "Evidence supporting market demand",
                    "competitive_advantage": "How we can win in this space",
                    "key_success_factors": ["Critical factors for success"],
                    "risks_and_challenges": ["Main risks and mitigation strategies"]
                }}
            ]
        }}
        
        Score opportunities (0.0-1.0) based on:
        - Market size and growth potential (25%)
        - Competitive landscape favorability (20%)
        - Technical fit with our capabilities (20%)
        - Time to market advantage (15%)
        - Strategic alignment with objectives (20%)
        
        Focus on opportunities we can realistically pursue given our resources and capabilities.
        """
        
        try:
            response = self.llm.invoke(opportunity_prompt)
            result = json.loads(response.content)
            return result.get("opportunities", [])
        except Exception as e:
            print(f"Error identifying opportunities: {e}")
            return []
    
    async def generate_executive_briefing(self) -> Dict[str, Any]:
        """Generate executive-level briefing for leadership team"""
        try:
            # Get latest analysis data
            analysis_summary = await db_client.get_analysis_summary(days=30)
            top_opportunities = await db_client.get_opportunities(min_score=0.7, limit=5)
            critical_trends = await db_client.get_trends(min_momentum=0.7, limit=5)
            recent_threats = await db_client.get_competitor_updates(limit=10)
            
            briefing_prompt = f"""
            Create an executive briefing for the leadership team:
            
            ANALYSIS SUMMARY (Last 30 days):
            {json.dumps(analysis_summary, indent=2)}
            
            TOP OPPORTUNITIES:
            {json.dumps(top_opportunities, indent=2, default=str)}
            
            CRITICAL TRENDS:
            {json.dumps(critical_trends, indent=2, default=str)}
            
            RECENT COMPETITIVE DEVELOPMENTS:
            {json.dumps(recent_threats, indent=2, default=str)}
            
            Create a concise executive briefing covering:
            1. Key strategic insights (3-4 bullet points)
            2. Critical decisions required (immediate actions needed)
            3. Top 3 opportunities with business case
            4. Competitive threats requiring attention
            5. Strategic recommendations with timelines
            
            Format for executive consumption - clear, concise, action-oriented.
            Company: {COMPANY_CONTEXT['name']}
            """
            
            response = self.llm.invoke(briefing_prompt)
            
            return {
                "briefing_type": "executive",
                "briefing_content": response.content,
                "data_sources": {
                    "opportunities": len(top_opportunities),
                    "trends": len(critical_trends),
                    "competitive_updates": len(recent_threats)
                },
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "briefing_type": "executive",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def assess_opportunity_portfolio(self) -> Dict[str, Any]:
        """Assess the current portfolio of identified opportunities"""
        try:
            all_opportunities = await db_client.get_opportunities(limit=50)
            
            portfolio_prompt = f"""
            Assess our current opportunity portfolio for strategic balance and prioritization:
            
            All Opportunities:
            {json.dumps(all_opportunities, indent=2, default=str)}
            
            Company Resources and Focus:
            - Core competencies: {', '.join(COMPANY_CONTEXT['core_competencies'])}
            - Growth objectives: {', '.join(COMPANY_CONTEXT['growth_objectives'])}
            
            Provide portfolio analysis covering:
            1. Portfolio balance (short vs long-term, risk levels, market segments)
            2. Resource allocation recommendations
            3. Prioritization framework application
            4. Portfolio gaps and overlaps
            5. Strategic coherence assessment
            6. Recommendations for portfolio optimization
            """
            
            response = self.llm.invoke(portfolio_prompt)
            
            return {
                "analysis_type": "opportunity_portfolio",
                "portfolio_size": len(all_opportunities),
                "portfolio_analysis": response.content,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "analysis_type": "opportunity_portfolio",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

# Create agent instance
strategic_synthesis_agent = StrategicSynthesisAgent()