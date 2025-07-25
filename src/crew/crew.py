"""
Main CrewAI coordination system for competitive analysis
"""
from crewai import Crew, Task
from typing import Dict, Any
from datetime import datetime
import asyncio
import os

from ..agents.market_intelligence import market_intelligence_agent
from ..agents.competitor_intelligence import competitor_intelligence_agent
from ..agents.trend_analysis import trend_analysis_agent
from ..agents.strategic_synthesis import strategic_synthesis_agent
from ..utils.gmail_client import gmail_client
from ..database.supabase_client import db_client
from ..database.models import AnalysisRun

class CompetitiveAnalysisCrew:
    """Main crew orchestrating all competitive analysis agents"""
    
    def __init__(self):
        self.crew = None
        self._setup_crew()
    
    def _setup_crew(self):
        """Setup the CrewAI crew with agents and tasks"""
        
        # Define tasks for each agent
        market_task = Task(
            description="""
            Conduct comprehensive market intelligence gathering for the AI industry:
            1. Search for recent AI industry news and developments (last 7 days)
            2. Identify funding rounds, acquisitions, and strategic partnerships
            3. Monitor regulatory changes and policy developments
            4. Track emerging technologies and research breakthroughs
            5. Analyze adoption trends in target industries
            
            Focus on developments that could create opportunities or threats.
            """,
            agent=market_intelligence_agent.agent,
            expected_output="Structured market intelligence report with findings and insights"
        )
        
        competitor_task = Task(
            description="""
            Monitor and analyze competitive landscape developments:
            1. Track competitor activities and product launches
            2. Identify pricing changes and positioning shifts
            3. Monitor partnership announcements and strategic moves
            4. Analyze hiring patterns and market indicators
            5. Assess competitive threats and response strategies
            
            Focus on actionable competitive intelligence.
            """,
            agent=competitor_intelligence_agent.agent,
            expected_output="Comprehensive competitive intelligence report with threat analysis"
        )
        
        trend_task = Task(
            description="""
            Analyze market trends and patterns:
            1. Review historical data to identify patterns
            2. Calculate trend momentum scores
            3. Identify cross-industry convergence opportunities
            4. Predict future market directions
            5. Validate trends with evidence
            
            Focus on trends relevant to our business model and capabilities.
            """,
            agent=trend_analysis_agent.agent,
            expected_output="Trend analysis report with momentum scores and predictions",
            context=[market_task, competitor_task]
        )
        
        synthesis_task = Task(
            description="""
            Synthesize all intelligence into strategic recommendations:
            1. Analyze all market intelligence, competitor, and trend data
            2. Identify market gaps and opportunities
            3. Calculate opportunity scores using multi-factor analysis
            4. Develop strategic recommendations with action items
            5. Prioritize initiatives based on impact and feasibility
            
            Provide executive-level strategic insights and recommendations.
            """,
            agent=strategic_synthesis_agent.agent,
            expected_output="Strategic analysis with prioritized opportunities and recommendations",
            context=[market_task, competitor_task, trend_task]
        )
        
        # Create the crew
        self.crew = Crew(
            agents=[
                market_intelligence_agent.agent,
                competitor_intelligence_agent.agent,
                trend_analysis_agent.agent,
                strategic_synthesis_agent.agent
            ],
            tasks=[market_task, competitor_task, trend_task, synthesis_task],
            verbose=True,
            process="sequential"  # Tasks run in sequence for context sharing
        )
    
    async def run_daily_analysis(self) -> Dict[str, Any]:
        """Run the complete daily competitive analysis"""
        start_time = datetime.now()
        print(f"🚀 Starting daily competitive analysis at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Run individual agent analyses in parallel for efficiency
            market_results, competitor_results, trend_results = await asyncio.gather(
                market_intelligence_agent.gather_market_intelligence(),
                competitor_intelligence_agent.monitor_competitors(),
                trend_analysis_agent.analyze_market_trends()
            )
            
            # Run strategic synthesis with all collected data
            strategic_results = await strategic_synthesis_agent.generate_strategic_analysis()
            
            # Compile comprehensive results
            analysis_results = {
                "analysis_date": start_time.date().isoformat(),
                "execution_time": (datetime.now() - start_time).total_seconds(),
                "status": "completed",
                "market_intelligence": market_results,
                "competitor_intelligence": competitor_results,
                "trend_analysis": trend_results,
                "strategic_synthesis": strategic_results,
                "summary": {
                    "findings_count": market_results.get("findings_count", 0),
                    "competitor_updates": len(competitor_results.get("competitor_analyses", {})),
                    "trends_identified": trend_results.get("trends_identified", 0),
                    "opportunities_count": strategic_results.get("new_opportunities", 0)
                }
            }
            
            # Store analysis run record
            await self._store_analysis_run(analysis_results)
            
            # Send daily report email
            await self._send_daily_notifications(analysis_results)
            
            print(f"✅ Daily analysis completed successfully in {analysis_results['execution_time']:.1f} seconds")
            return analysis_results
            
        except Exception as e:
            error_results = {
                "analysis_date": start_time.date().isoformat(),
                "execution_time": (datetime.now() - start_time).total_seconds(),
                "status": "error",
                "error": str(e)
            }
            
            print(f"❌ Daily analysis failed: {e}")
            return error_results
    
    async def _store_analysis_run(self, results: Dict[str, Any]):
        """Store analysis run results in database"""
        try:
            analysis_run = AnalysisRun(
                run_date=datetime.now().date(),
                findings_count=results["summary"]["findings_count"],
                opportunities_identified=results["summary"]["opportunities_count"],
                key_insights=str(results.get("strategic_synthesis", {}).get("strategic_insights", [])),
                recommendations=results.get("strategic_synthesis", {}).get("strategic_recommendations", []),
                execution_time_seconds=results["execution_time"],
                status=results["status"]
            )
            
            await db_client.insert_analysis_run(analysis_run.dict())
            print("📊 Analysis run stored in database")
            
        except Exception as e:
            print(f"Error storing analysis run: {e}")
    
    async def _send_daily_notifications(self, results: Dict[str, Any]):
        """Send daily notifications via email"""
        try:
            # Prepare report data for email
            report_data = {
                "executive_summary": results.get("strategic_synthesis", {}).get("executive_summary", "Daily analysis completed"),
                "findings_count": results["summary"]["findings_count"],
                "opportunities_count": results["summary"]["opportunities_count"],
                "competitor_updates": results["summary"]["competitor_updates"],
                "trends_identified": results["summary"]["trends_identified"],
                "top_opportunities": results.get("strategic_synthesis", {}).get("top_opportunities", []),
                "key_insights": results.get("strategic_synthesis", {}).get("strategic_insights", []),
                "recommendations": results.get("strategic_synthesis", {}).get("strategic_recommendations", [])
            }
            
            # Check for critical alerts
            critical_alerts = self._identify_critical_alerts(results)
            if critical_alerts:
                report_data["critical_alerts"] = critical_alerts
                
                # Send immediate alert for critical items
                for alert in critical_alerts:
                    gmail_client.send_critical_alert(alert)
            
            # Send daily report
            success = gmail_client.send_daily_report(report_data)
            if success:
                print("📧 Daily report sent successfully")
            else:
                print("❌ Failed to send daily report")
                
        except Exception as e:
            print(f"Error sending notifications: {e}")
    
    def _identify_critical_alerts(self, results: Dict[str, Any]) -> list:
        """Identify critical alerts requiring immediate attention"""
        alerts = []
        
        # Check for critical competitive threats
        competitor_results = results.get("competitor_intelligence", {})
        critical_threats = competitor_results.get("critical_threats", [])
        
        for threat in critical_threats:
            if threat.get("impact") in ["high", "critical"]:
                alerts.append({
                    "title": f"Critical Competitive Threat: {threat.get('company')}",
                    "description": threat.get("threat"),
                    "impact_level": threat.get("impact"),
                    "source": "Competitive Intelligence",
                    "recommended_action": "Review competitive response strategy immediately"
                })
        
        # Check for high-value opportunities
        strategic_results = results.get("strategic_synthesis", {})
        top_opportunities = strategic_results.get("top_opportunities", [])
        
        for opp in top_opportunities:
            if opp.get("score", 0) > 0.9 and opp.get("priority") == "high":
                alerts.append({
                    "title": f"High-Value Opportunity: {opp.get('title')}",
                    "description": opp.get("description"),
                    "impact_level": "high",
                    "source": "Strategic Analysis",
                    "recommended_action": "Evaluate opportunity for immediate action"
                })
        
        return alerts
    
    async def run_weekly_summary(self) -> Dict[str, Any]:
        """Generate and send weekly comprehensive summary"""
        try:
            print("📊 Generating weekly summary...")
            
            # Get comprehensive data for the week
            weekly_summary = await db_client.get_analysis_summary(days=7)
            executive_briefing = await strategic_synthesis_agent.generate_executive_briefing()
            portfolio_assessment = await strategic_synthesis_agent.assess_opportunity_portfolio()
            
            summary_data = {
                "period": "weekly",
                "summary": weekly_summary,
                "executive_briefing": executive_briefing,
                "portfolio_assessment": portfolio_assessment,
                "timestamp": datetime.now().isoformat()
            }
            
            # Send weekly summary email
            success = gmail_client.send_weekly_summary(summary_data)
            if success:
                print("📧 Weekly summary sent successfully")
            
            return summary_data
            
        except Exception as e:
            print(f"Error generating weekly summary: {e}")
            return {"error": str(e)}
    
    async def run_quick_analysis(self, topic: str) -> Dict[str, Any]:
        """Run focused analysis on a specific topic"""
        try:
            print(f"🔍 Running quick analysis on: {topic}")
            
            # Run focused analyses
            market_analysis = await market_intelligence_agent.analyze_specific_topic(topic)
            trend_convergence = await trend_analysis_agent.analyze_trend_convergence()
            
            return {
                "topic": topic,
                "market_analysis": market_analysis,
                "trend_convergence": trend_convergence,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error in quick analysis: {e}")
            return {"topic": topic, "error": str(e)}

# Create global crew instance
competitive_analysis_crew = CompetitiveAnalysisCrew()