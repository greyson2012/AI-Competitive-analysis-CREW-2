"""
Competitor Intelligence Agent for competitive analysis
"""
from crewai import Agent
from langchain_openai import ChatOpenAI
from typing import Dict, Any, List
import os
from datetime import datetime, date
import json

from ..tools.serper_search import serper_tool
from ..config.company_context import COMPANY_CONTEXT, ANALYSIS_PROMPTS
from ..database.supabase_client import db_client
from ..database.models import CompetitorUpdate, Category, Priority

class CompetitorIntelligenceAgent:
    """Agent responsible for monitoring competitor activities"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        self.agent = Agent(
            role="Competitive Intelligence Analyst",
            goal="""Monitor and analyze competitor activities, product launches, strategic moves, 
            and market positioning to identify threats and opportunities in the competitive landscape.""",
            
            backstory=ANALYSIS_PROMPTS["competitor_analysis"],
            
            tools=[serper_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            memory=True
        )
    
    async def monitor_competitors(self) -> Dict[str, Any]:
        """Main method to monitor all competitors"""
        try:
            competitors = COMPANY_CONTEXT.get("competitors", [])
            all_updates = []
            competitor_analyses = {}
            
            for competitor in competitors:
                competitor_name = competitor.strip()
                if not competitor_name:
                    continue
                    
                # Search for recent updates about this competitor
                updates = serper_tool.search_competitor_updates(competitor_name, days_back=30)
                
                # Analyze the competitor updates
                analysis = await self._analyze_competitor_updates(competitor_name, updates)
                competitor_analyses[competitor_name] = analysis
                
                # Store updates in database
                for update in analysis.get("updates", []):
                    try:
                        competitor_update = CompetitorUpdate(
                            company_name=competitor_name,
                            update_type=Category(update.get("update_type", "market_trend")),
                            description=update.get("description", ""),
                            impact_level=Priority(update.get("impact_level", "medium")),
                            source_url=update.get("source_url"),
                            detected_date=date.today()
                        )
                        
                        stored_update = await db_client.insert_competitor_update(competitor_update.dict())
                        if stored_update:
                            all_updates.append(stored_update)
                            
                    except Exception as e:
                        print(f"Error storing competitor update: {e}")
                        continue
            
            # Generate overall competitive landscape analysis
            landscape_analysis = await self._analyze_competitive_landscape(competitor_analyses)
            
            return {
                "agent": "competitor_intelligence",
                "timestamp": datetime.now().isoformat(),
                "competitors_monitored": len(competitors),
                "updates_found": len(all_updates),
                "landscape_analysis": landscape_analysis,
                "competitor_analyses": competitor_analyses,
                "critical_threats": self._identify_critical_threats(all_updates),
                "strategic_recommendations": landscape_analysis.get("recommendations", [])
            }
            
        except Exception as e:
            print(f"Error in competitor monitoring: {e}")
            return {
                "agent": "competitor_intelligence",
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "updates_found": 0
            }
    
    async def _analyze_competitor_updates(self, competitor_name: str, search_results: str) -> Dict[str, Any]:
        """Analyze updates for a specific competitor"""
        analysis_prompt = f"""
        Analyze the following search results about {competitor_name} competitor updates:
        
        Search Results:
        {search_results}
        
        Our Company Context:
        - Focus: {', '.join(COMPANY_CONTEXT['core_competencies'])}
        - Target industries: {', '.join(COMPANY_CONTEXT['target_industries'])}
        - Current offerings: {', '.join(COMPANY_CONTEXT['current_offerings'])}
        - Competitive advantages: {', '.join(COMPANY_CONTEXT['competitive_advantages'])}
        
        Provide analysis in JSON format:
        {{
            "competitor_summary": "Brief overview of competitor's recent activities",
            "updates": [
                {{
                    "update_type": "product_launch|funding|partnership|acquisition|regulation",
                    "description": "Description of the update",
                    "impact_level": "low|medium|high|critical",
                    "source_url": "URL if available",
                    "strategic_implications": "How this affects our competitive position",
                    "suggested_response": "Recommended response strategy"
                }}
            ],
            "competitive_threat_level": "low|medium|high|critical",
            "key_differentiators": ["Areas where we still have advantages"],
            "areas_of_concern": ["Areas where competitor is gaining advantage"],
            "response_priority": "immediate|short-term|medium-term|long-term"
        }}
        
        Focus on developments that could impact our market position or create new competitive dynamics.
        """
        
        try:
            response = self.llm.invoke(analysis_prompt)
            return json.loads(response.content)
        except Exception as e:
            print(f"Error analyzing competitor {competitor_name}: {e}")
            return {
                "competitor_summary": f"Error analyzing {competitor_name}",
                "updates": [],
                "competitive_threat_level": "unknown"
            }
    
    async def _analyze_competitive_landscape(self, competitor_analyses: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the overall competitive landscape"""
        landscape_prompt = f"""
        Based on the following competitive analyses, provide an overall competitive landscape assessment:
        
        Competitor Analyses:
        {json.dumps(competitor_analyses, indent=2)}
        
        Our Position:
        - Core competencies: {', '.join(COMPANY_CONTEXT['core_competencies'])}
        - Competitive advantages: {', '.join(COMPANY_CONTEXT['competitive_advantages'])}
        - Growth objectives: {', '.join(COMPANY_CONTEXT['growth_objectives'])}
        
        Provide strategic analysis in JSON format:
        {{
            "landscape_summary": "Overall state of the competitive landscape",
            "market_dynamics": "Key changes in market dynamics and competitive forces",
            "emerging_threats": ["New competitive threats emerging"],
            "market_opportunities": ["Opportunities created by competitive gaps"],
            "competitive_positioning": "Assessment of our current competitive position",
            "strategic_priorities": ["Top strategic priorities to maintain/improve position"],
            "recommendations": [
                {{
                    "action": "Specific recommended action",
                    "rationale": "Why this action is important",
                    "priority": "high|medium|low",
                    "timeline": "immediate|short-term|medium-term|long-term"
                }}
            ]
        }}
        """
        
        try:
            response = self.llm.invoke(landscape_prompt)
            return json.loads(response.content)
        except Exception as e:
            print(f"Error analyzing competitive landscape: {e}")
            return {
                "landscape_summary": "Error in landscape analysis",
                "recommendations": []
            }
    
    def _identify_critical_threats(self, updates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify critical competitive threats requiring immediate attention"""
        critical_threats = []
        
        for update in updates:
            if update.get("impact_level") in ["high", "critical"]:
                critical_threats.append({
                    "company": update.get("company_name"),
                    "threat": update.get("description"),
                    "impact": update.get("impact_level"),
                    "date": update.get("detected_date")
                })
        
        return critical_threats
    
    async def analyze_specific_competitor(self, competitor_name: str) -> Dict[str, Any]:
        """Deep dive analysis of a specific competitor"""
        try:
            # Enhanced search for specific competitor
            recent_updates = serper_tool.search_competitor_updates(competitor_name, days_back=90)
            product_info = serper_tool._run(
                f'"{competitor_name}" products services features pricing AI',
                num_results=15,
                time_range="m"
            )
            
            deep_analysis_prompt = f"""
            Conduct a comprehensive competitive analysis of {competitor_name}:
            
            Recent Updates:
            {recent_updates}
            
            Product Information:
            {product_info}
            
            Analyze:
            1. Business model and revenue streams
            2. Product portfolio and key features
            3. Market positioning and messaging
            4. Pricing strategy and value proposition
            5. Strengths and vulnerabilities
            6. Strategic direction and likely next moves
            7. Competitive threats to our business
            8. Opportunities to compete more effectively
            
            Our context: {', '.join(COMPANY_CONTEXT['core_competencies'])}
            """
            
            response = self.llm.invoke(deep_analysis_prompt)
            
            return {
                "competitor": competitor_name,
                "analysis": response.content,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "competitor": competitor_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

# Create agent instance
competitor_intelligence_agent = CompetitorIntelligenceAgent()