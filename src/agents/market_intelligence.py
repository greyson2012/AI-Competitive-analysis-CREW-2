"""
Market Intelligence Agent for competitive analysis
"""
from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import Dict, Any
import os
from datetime import datetime, date
import json

from ..tools.serper_search import serper_tool
from ..config.company_context import COMPANY_CONTEXT, ANALYSIS_PROMPTS
from ..database.supabase_client import db_client
from ..database.models import MarketFinding, Category

class MarketIntelligenceAgent:
    """Agent responsible for gathering and analyzing market intelligence"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.agent = Agent(
            role="AI Market Intelligence Specialist",
            goal="""Discover and analyze the latest developments in the AI industry that could impact 
            business strategy, focusing on technology breakthroughs, funding activities, 
            and market trends relevant to our target industries.""",
            
            backstory=ANALYSIS_PROMPTS["market_intelligence"],
            
            tools=[serper_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            memory=True
        )
    
    async def gather_market_intelligence(self) -> Dict[str, Any]:
        """Main method to gather and analyze market intelligence"""
        try:
            # Search for recent AI industry developments
            ai_news = serper_tool.search_ai_news(days_back=7)
            emerging_tech = serper_tool._run(
                "emerging AI technologies 2024 breakthrough innovation",
                num_results=15,
                time_range="m",
                search_type="news"
            )
            funding_news = serper_tool._run(
                "AI startup funding venture capital investment 2024",
                num_results=10,
                time_range="w",
                search_type="news"
            )
            
            # Analyze the findings using OpenAI
            analysis_prompt = f"""
            Based on the following market intelligence data, analyze and extract key findings:
            
            Recent AI News:
            {ai_news}
            
            Emerging Technologies:
            {emerging_tech}
            
            Funding News:
            {funding_news}
            
            Company Context:
            - Our focus: {', '.join(COMPANY_CONTEXT['core_competencies'])}
            - Target industries: {', '.join(COMPANY_CONTEXT['target_industries'])}
            - Current offerings: {', '.join(COMPANY_CONTEXT['current_offerings'])}
            
            Please provide a JSON response with the following structure:
            {{
                "executive_summary": "Brief summary of key developments",
                "findings": [
                    {{
                        "title": "Finding title",
                        "summary": "Brief summary",
                        "content": "Detailed analysis",
                        "category": "ai_research|product_launch|funding|regulation|market_trend",
                        "relevance_score": 0.85,
                        "source_url": "URL if available",
                        "implications": "Business implications"
                    }}
                ],
                "key_insights": ["List of key insights"],
                "recommended_actions": ["List of recommended actions"]
            }}
            
            Rate relevance from 0.0 to 1.0 based on potential impact to our business model.
            Focus on developments that could create opportunities or pose threats.
            """
            
            response = self.llm.invoke(analysis_prompt)
            analysis = json.loads(response.content)
            
            # Store findings in database
            stored_findings = []
            for finding in analysis.get("findings", []):
                try:
                    # Create MarketFinding model
                    market_finding = MarketFinding(
                        date=date.today(),
                        category=Category(finding.get("category", "market_trend")),
                        title=finding.get("title", "")[:500],  # Truncate if too long
                        summary=finding.get("summary", "")[:2000],
                        content=finding.get("content", ""),
                        relevance_score=float(finding.get("relevance_score", 0.0)),
                        source_url=finding.get("source_url")
                    )
                    
                    # Store in database
                    stored_finding = await db_client.insert_market_finding(market_finding.dict())
                    if stored_finding:
                        stored_findings.append(stored_finding)
                        
                except Exception as e:
                    print(f"Error storing finding: {e}")
                    continue
            
            return {
                "agent": "market_intelligence",
                "timestamp": datetime.now().isoformat(),
                "executive_summary": analysis.get("executive_summary", ""),
                "findings_count": len(stored_findings),
                "key_insights": analysis.get("key_insights", []),
                "recommended_actions": analysis.get("recommended_actions", []),
                "findings": stored_findings
            }
            
        except Exception as e:
            print(f"Error in market intelligence gathering: {e}")
            return {
                "agent": "market_intelligence",
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "findings_count": 0
            }
    
    async def analyze_specific_topic(self, topic: str, context: str = "") -> Dict[str, Any]:
        """Analyze a specific market topic in detail"""
        try:
            # Search for topic-specific information
            search_results = serper_tool._run(
                f"{topic} AI artificial intelligence market analysis 2024",
                num_results=20,
                time_range="m"
            )
            
            analysis_prompt = f"""
            Analyze the following information about "{topic}" in the context of the AI market:
            
            Search Results:
            {search_results}
            
            Additional Context:
            {context}
            
            Company Focus: {', '.join(COMPANY_CONTEXT['core_competencies'])}
            
            Provide analysis focusing on:
            1. Market size and growth potential
            2. Key players and competitive landscape
            3. Technology trends and innovations
            4. Business opportunities and threats
            5. Relevance to our business model
            
            Return a structured analysis with insights and recommendations.
            """
            
            response = self.llm.invoke(analysis_prompt)
            
            return {
                "topic": topic,
                "analysis": response.content,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "topic": topic,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

# Create agent instance
market_intelligence_agent = MarketIntelligenceAgent()