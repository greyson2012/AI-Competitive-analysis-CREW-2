"""
Trend Analysis Agent for pattern recognition and forecasting
"""
from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List
import os
from datetime import datetime, date, timedelta
import json

from ..tools.serper_search import serper_tool
from ..config.company_context import COMPANY_CONTEXT, ANALYSIS_PROMPTS
from ..database.supabase_client import db_client
from ..database.models import Trend, Category

class TrendAnalysisAgent:
    """Agent responsible for identifying and analyzing market trends"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-o3",
            temperature=0.2,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.agent = Agent(
            role="Market Trend Forecasting Analyst",
            goal="""Identify emerging trends, analyze historical patterns, and predict future 
            market directions by synthesizing data from multiple sources and applying 
            pattern recognition to market intelligence.""",
            
            backstory=ANALYSIS_PROMPTS["trend_analysis"],
            
            tools=[serper_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            memory=True
        )
    
    async def analyze_market_trends(self) -> Dict[str, Any]:
        """Main method to analyze current and emerging market trends"""
        try:
            # Get historical data for pattern analysis
            historical_findings = await db_client.get_market_findings(
                limit=100,
                start_date=(date.today() - timedelta(days=180))
            )
            
            historical_opportunities = await db_client.get_opportunities(limit=50)
            
            # Search for current trend indicators
            current_trends = await self._search_current_trends()
            
            # Analyze patterns and identify trends
            trend_analysis = await self._analyze_trend_patterns(
                historical_findings, 
                historical_opportunities, 
                current_trends
            )
            
            # Store identified trends in database
            stored_trends = []
            for trend in trend_analysis.get("trends", []):
                try:
                    trend_model = Trend(
                        trend_name=trend.get("trend_name", "")[:255],
                        category=Category(trend.get("category", "market_trend")),
                        momentum_score=float(trend.get("momentum_score", 0.0)),
                        evidence=trend.get("evidence", {}),
                        first_detected=date.today(),
                        prediction=trend.get("prediction", "")
                    )
                    
                    stored_trend = await db_client.insert_trend(trend_model.dict())
                    if stored_trend:
                        stored_trends.append(stored_trend)
                        
                except Exception as e:
                    print(f"Error storing trend: {e}")
                    continue
            
            return {
                "agent": "trend_analysis",
                "timestamp": datetime.now().isoformat(),
                "trends_identified": len(stored_trends),
                "analysis_summary": trend_analysis.get("summary", ""),
                "key_trends": stored_trends,
                "market_predictions": trend_analysis.get("predictions", []),
                "opportunity_indicators": trend_analysis.get("opportunity_indicators", []),
                "risk_factors": trend_analysis.get("risk_factors", [])
            }
            
        except Exception as e:
            print(f"Error in trend analysis: {e}")
            return {
                "agent": "trend_analysis",
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "trends_identified": 0
            }
    
    async def _search_current_trends(self) -> Dict[str, str]:
        """Search for current market trend indicators"""
        trend_searches = {
            "ai_technology": serper_tool._run(
                "AI technology trends 2024 emerging artificial intelligence",
                num_results=15,
                time_range="m",
                search_type="news"
            ),
            "enterprise_adoption": serper_tool._run(
                "enterprise AI adoption trends business automation 2024",
                num_results=12,
                time_range="m"
            ),
            "investment_trends": serper_tool._run(
                "AI investment trends venture capital funding 2024",
                num_results=10,
                time_range="m",
                search_type="news"
            ),
            "regulatory_trends": serper_tool._run(
                "AI regulation policy trends government artificial intelligence",
                num_results=10,
                time_range="m"
            )
        }
        
        return trend_searches
    
    async def _analyze_trend_patterns(self, 
                                    historical_findings: List[Dict[str, Any]], 
                                    historical_opportunities: List[Dict[str, Any]],
                                    current_trends: Dict[str, str]) -> Dict[str, Any]:
        """Analyze patterns to identify and validate trends"""
        
        analysis_prompt = f"""
        Analyze the following data to identify market trends and patterns:
        
        Historical Market Findings (last 6 months):
        {json.dumps(historical_findings[:20], indent=2, default=str)}
        
        Historical Opportunities:
        {json.dumps(historical_opportunities[:10], indent=2, default=str)}
        
        Current Trend Searches:
        {json.dumps(current_trends, indent=2)}
        
        Company Context:
        - Focus areas: {', '.join(COMPANY_CONTEXT['core_competencies'])}
        - Target industries: {', '.join(COMPANY_CONTEXT['target_industries'])}
        - Growth objectives: {', '.join(COMPANY_CONTEXT['growth_objectives'])}
        
        Identify trends and provide analysis in JSON format:
        {{
            "summary": "Executive summary of trend analysis",
            "trends": [
                {{
                    "trend_name": "Name of the identified trend",
                    "category": "ai_research|technology|market_trend|regulation|funding",
                    "momentum_score": 0.85,
                    "evidence": {{
                        "frequency_mentions": 45,
                        "growth_indicators": ["list of growth indicators"],
                        "supporting_data": ["supporting evidence"],
                        "time_span": "duration of trend observation"
                    }},
                    "prediction": "Prediction about trend evolution and impact",
                    "business_relevance": "How this trend affects our business",
                    "opportunity_potential": "Opportunities this trend may create"
                }}
            ],
            "predictions": [
                {{
                    "timeframe": "3-6 months|6-12 months|1-2 years",
                    "prediction": "Specific market prediction",
                    "confidence": 0.75,
                    "impact_level": "low|medium|high"
                }}
            ],
            "opportunity_indicators": ["Signs pointing to new opportunities"],
            "risk_factors": ["Potential risks or trend reversals to monitor"],
            "cross_trend_analysis": "Analysis of how trends interact with each other"
        }}
        
        Calculate momentum scores (0.0-1.0) based on:
        - Frequency of mentions and discussion
        - Growth rate and acceleration
        - Market adoption indicators
        - Investment and development activity
        - Regulatory and policy support
        """
        
        try:
            response = self.llm.invoke(analysis_prompt)
            return json.loads(response.content)
        except Exception as e:
            print(f"Error in trend pattern analysis: {e}")
            return {
                "summary": "Error in trend analysis",
                "trends": [],
                "predictions": []
            }
    
    async def analyze_trend_convergence(self) -> Dict[str, Any]:
        """Analyze how different trends might converge to create opportunities"""
        try:
            recent_trends = await db_client.get_trends(limit=20)
            
            convergence_prompt = f"""
            Analyze potential trend convergences that could create new opportunities:
            
            Recent Trends:
            {json.dumps(recent_trends, indent=2, default=str)}
            
            Our Capabilities: {', '.join(COMPANY_CONTEXT['core_competencies'])}
            
            Identify:
            1. Trends that are converging or reinforcing each other
            2. New opportunities created by trend intersections
            3. Potential disruptions from converging trends
            4. Strategic positioning opportunities
            5. Timeline for convergence impact
            
            Focus on convergences relevant to our business model and capabilities.
            """
            
            response = self.llm.invoke(convergence_prompt)
            
            return {
                "analysis_type": "trend_convergence",
                "convergence_analysis": response.content,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "analysis_type": "trend_convergence",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def forecast_market_direction(self, timeframe: str = "6 months") -> Dict[str, Any]:
        """Generate market direction forecasts based on trend analysis"""
        try:
            # Get comprehensive trend data
            trends = await db_client.get_trends(min_momentum=0.5, limit=15)
            market_findings = await db_client.get_market_findings(
                limit=50,
                start_date=(date.today() - timedelta(days=90))
            )
            
            forecast_prompt = f"""
            Based on trend analysis and market data, provide market direction forecasts:
            
            High-Momentum Trends:
            {json.dumps(trends, indent=2, default=str)}
            
            Recent Market Findings:
            {json.dumps(market_findings[:15], indent=2, default=str)}
            
            Forecast for next {timeframe}:
            
            1. Overall market direction and growth areas
            2. Technology adoption patterns
            3. Competitive landscape evolution
            4. Investment and funding patterns
            5. Regulatory environment changes
            6. Customer behavior and demand shifts
            
            Company Context: {', '.join(COMPANY_CONTEXT['focus_keywords'])}
            Target Industries: {', '.join(COMPANY_CONTEXT['target_industries'])}
            
            Provide specific, actionable forecasts with confidence levels.
            """
            
            response = self.llm.invoke(forecast_prompt)
            
            return {
                "forecast_timeframe": timeframe,
                "market_forecast": response.content,
                "confidence_factors": trends,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "forecast_timeframe": timeframe,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

# Create agent instance
trend_analysis_agent = TrendAnalysisAgent()