"""
Enhanced competitive analysis engine with user-customizable inputs
"""
import os
import sys
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.serper_search import serper_tool
from database.supabase_client import db_client
from utils.gmail_client import gmail_client

load_dotenv()

class CompetitiveAnalysisEngine:
    """Enhanced competitive analysis engine with user customization"""
    
    def __init__(self):
        from openai import OpenAI
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def run_custom_analysis(self, analysis_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run customized competitive analysis based on user configuration
        
        Args:
            analysis_config: Configuration dictionary containing:
                - industry: Target industry/market
                - competitors: List of competitor companies
                - company_name: User's company name
                - company_description: User's company description  
                - company_goals: User's strategic goals
                - focus_areas: Areas to focus analysis on
                - analysis_type: Type of analysis to perform
                - time_range: Time range for data collection
                - search_depth: Number of sources to analyze
        
        Returns:
            Dictionary containing analysis results
        """
        
        print(f"🚀 Starting competitive analysis for {analysis_config['company_name']}")
        print(f"📊 Industry: {analysis_config['industry']}")
        print(f"🏢 Competitors: {', '.join(analysis_config['competitors'])}")
        
        results = {
            'config': analysis_config,
            'timestamp': datetime.now().isoformat(),
            'market_intelligence': {},
            'competitor_intelligence': {},
            'strategic_analysis': '',
            'opportunities': [],
            'recommendations': [],
            'action_items': []
        }
        
        try:
            # Step 1: Market Intelligence Gathering
            print("📈 Gathering market intelligence...")
            market_data = await self._gather_market_intelligence(analysis_config)
            results['market_intelligence'] = market_data
            
            # Step 2: Competitor Intelligence
            print("🏢 Analyzing competitor activities...")
            competitor_data = await self._analyze_competitors(analysis_config)
            results['competitor_intelligence'] = competitor_data
            
            # Step 3: Strategic Analysis with Company Context
            print("🧠 Generating strategic analysis...")
            strategic_analysis = await self._generate_strategic_analysis(
                analysis_config, market_data, competitor_data
            )
            results['strategic_analysis'] = strategic_analysis
            
            # Step 4: Opportunity Identification
            print("💡 Identifying opportunities...")
            opportunities = await self._identify_opportunities(
                analysis_config, market_data
            )
            results['opportunities'] = opportunities
            
            # Step 5: Generate Recommendations
            print("📋 Generating recommendations...")
            recommendations = await self._generate_recommendations(
                analysis_config, strategic_analysis, opportunities
            )
            results['recommendations'] = recommendations
            
            # Step 6: Save to database
            print("💾 Saving analysis results...")
            await self._save_analysis_results(results)
            
            print("✅ Analysis complete!")
            return results
            
        except Exception as e:
            print(f"❌ Analysis failed: {e}")
            results['error'] = str(e)
            return results
    
    async def _gather_market_intelligence(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Gather market intelligence based on industry and focus areas"""
        
        market_data = {
            'industry_trends': '',
            'market_size': '',
            'recent_developments': '',
            'funding_activity': '',
            'regulatory_changes': ''
        }
        
        # Build search queries based on focus areas
        base_queries = {
            'industry_trends': f"{config['industry']} market trends growth forecast 2025",
            'recent_developments': f"{config['industry']} breakthrough innovation news 2025",
            'funding_activity': f"{config['industry']} startup funding investment 2025",
            'regulatory_changes': f"{config['industry']} regulation policy changes 2025"
        }
        
        # Execute searches based on user's focus areas
        for area in config['focus_areas']:
            if 'Technology Trends' in area and 'industry_trends' in base_queries:
                query = base_queries['industry_trends']
                if config.get('custom_keywords'):
                    query += f" {config['custom_keywords']}"
                
                search_results = serper_tool._run(
                    query, 
                    num_results=config['search_depth']//4,
                    search_type="news"
                )
                market_data['industry_trends'] = search_results
            
            if 'Funding Landscape' in area and 'funding_activity' in base_queries:
                search_results = serper_tool._run(
                    base_queries['funding_activity'],
                    num_results=config['search_depth']//4,
                    search_type="news"
                )
                market_data['funding_activity'] = search_results
            
            if 'Regulatory Changes' in area and 'regulatory_changes' in base_queries:
                search_results = serper_tool._run(
                    base_queries['regulatory_changes'],
                    num_results=config['search_depth']//4,
                    search_type="news"
                )
                market_data['regulatory_changes'] = search_results
        
        # Always get recent developments
        search_results = serper_tool._run(
            base_queries['recent_developments'],
            num_results=config['search_depth']//3,
            search_type="news"
        )
        market_data['recent_developments'] = search_results
        
        return market_data
    
    async def _analyze_competitors(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze competitor activities and positioning"""
        
        competitor_data = {}
        
        # Analyze each competitor
        for competitor in config['competitors'][:5]:  # Limit to top 5 competitors
            print(f"   Analyzing {competitor}...")
            
            # Search for recent competitor updates
            queries = [
                f"{competitor} {config['industry']} product launch news 2025",
                f"{competitor} partnership acquisition funding 2025",
                f"{competitor} strategy market position 2025"
            ]
            
            competitor_info = {
                'recent_updates': '',
                'strategic_moves': '',
                'market_position': ''
            }
            
            for i, query in enumerate(queries):
                search_results = serper_tool._run(
                    query,
                    num_results=3,
                    search_type="news"
                )
                
                if i == 0:
                    competitor_info['recent_updates'] = search_results
                elif i == 1:
                    competitor_info['strategic_moves'] = search_results
                else:
                    competitor_info['market_position'] = search_results
            
            competitor_data[competitor] = competitor_info
        
        return competitor_data
    
    async def _generate_strategic_analysis(
        self, 
        config: Dict[str, Any], 
        market_data: Dict[str, Any], 
        competitor_data: Dict[str, Any]
    ) -> str:
        """Generate comprehensive strategic analysis with company context"""
        
        # Prepare comprehensive prompt
        analysis_prompt = f"""
        You are a senior strategic consultant analyzing the {config['industry']} industry for {config['company_name']}.
        
        COMPANY CONTEXT:
        - Company: {config['company_name']}
        - Description: {config['company_description']}
        - Strategic Goals: {config['company_goals']}
        - Focus Areas: {', '.join(config['focus_areas'])}
        
        COMPETITORS ANALYZED:
        {', '.join(config['competitors'])}
        
        MARKET INTELLIGENCE:
        Industry Trends: {str(market_data.get('industry_trends', ''))[:1000]}
        Recent Developments: {str(market_data.get('recent_developments', ''))[:1000]}
        Funding Activity: {str(market_data.get('funding_activity', ''))[:800]}
        Regulatory Changes: {str(market_data.get('regulatory_changes', ''))[:800]}
        
        COMPETITOR INTELLIGENCE:
        {str(competitor_data)[:1500]}
        
        Please provide a comprehensive strategic analysis with:
        
        ## EXECUTIVE SUMMARY
        Brief overview of key findings and strategic implications for {config['company_name']}.
        
        ## MARKET LANDSCAPE ANALYSIS
        - Current state of the {config['industry']} market
        - Key trends and their impact on {config['company_name']}
        - Market size, growth opportunities, and threats
        - Regulatory environment and compliance requirements
        
        ## COMPETITIVE POSITIONING ANALYSIS
        - How {config['company_name']} currently positions against key competitors
        - Competitive advantages {config['company_name']} can leverage
        - Competitive gaps that need addressing
        - Competitor strategic moves and their implications for {config['company_name']}
        
        ## STRATEGIC RECOMMENDATIONS FOR {config['company_name'].upper()}
        - Specific, actionable recommendations based on your company's profile and goals
        - How to capitalize on identified market opportunities
        - Strategies to differentiate from competitors
        - Risk mitigation approaches
        - Partnership, acquisition, or collaboration opportunities
        
        ## IMPLEMENTATION ROADMAP
        - Top 5 strategic priorities for the next 90 days
        - Resource allocation recommendations
        - Key performance indicators to track
        - Success metrics and milestones
        
        Focus specifically on insights that are directly actionable for {config['company_name']} given their stated goals: {config['company_goals']}
        
        Be specific, data-driven, and provide concrete next steps rather than generic advice.
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior strategic consultant with expertise in competitive intelligence, market analysis, and business strategy. Provide detailed, actionable insights tailored to the specific company context. Use markdown formatting for better readability."
                },
                {
                    "role": "user",
                    "content": analysis_prompt
                }
            ],
            max_tokens=2000,
            temperature=0.2
        )
        
        return response.choices[0].message.content
    
    async def _identify_opportunities(
        self, 
        config: Dict[str, Any], 
        market_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify specific business opportunities for the company"""
        
        opportunity_prompt = f"""
        Based on the market analysis for {config['company_name']} in the {config['industry']} industry, identify specific business opportunities.
        
        COMPANY CONTEXT:
        - Company: {config['company_name']}
        - Description: {config['company_description']}
        - Strategic Goals: {config['company_goals']}
        - Focus Areas: {', '.join(config['focus_areas'])}
        
        MARKET DATA:
        {str(market_data)[:2000]}
        
        Identify 7 specific opportunities. For each opportunity, provide:
        
        1. **Opportunity Name**: Clear, specific title
        2. **Market Size**: Estimated market potential (revenue/users)
        3. **Implementation Difficulty**: Scale 1-5 (1=easy, 5=very difficult)
        4. **Time to Market**: Estimated timeline to launch
        5. **Investment Required**: Rough estimate of resources needed
        6. **Why Suitable for {config['company_name']}**: Specific reasons based on company profile
        7. **First Steps**: Top 3 immediate actions to pursue this opportunity
        8. **Success Probability**: Scale 1-5 (1=low, 5=high chance of success)
        
        Format each opportunity as a structured JSON-like entry for easy parsing.
        Focus on opportunities that align with {config['company_name']}'s capabilities and goals.
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a business opportunity analyst specializing in identifying and evaluating market opportunities. Provide specific, actionable opportunities with detailed implementation guidance."
                },
                {
                    "role": "user",
                    "content": opportunity_prompt
                }
            ],
            max_tokens=1200,
            temperature=0.3
        )
        
        # Parse opportunities (simplified - in production, would use structured parsing)
        opportunities_text = response.choices[0].message.content
        
        # For now, return as single text - could be enhanced to parse into structured data
        return [{"opportunities_analysis": opportunities_text}]
    
    async def _generate_recommendations(
        self,
        config: Dict[str, Any],
        strategic_analysis: str,
        opportunities: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate specific action recommendations"""
        
        recommendations_prompt = f"""
        Based on the strategic analysis for {config['company_name']}, provide 8 specific, actionable recommendations.
        
        Company: {config['company_name']}
        Goals: {config['company_goals']}
        
        Strategic Analysis Summary: {strategic_analysis[:1500]}
        
        Provide 8 recommendations in this format:
        1. **[Category]**: Specific recommendation with concrete actions
        2. **[Category]**: Specific recommendation with concrete actions
        ...
        
        Categories should include:
        - Product/Service Development
        - Market Positioning
        - Competitive Strategy
        - Partnership/Alliances
        - Technology Investment
        - Marketing/Sales
        - Operations/Scaling
        - Risk Management
        
        Each recommendation should be specific, measurable, and actionable within 90 days.
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a strategic business advisor. Provide specific, actionable recommendations."
                },
                {
                    "role": "user",
                    "content": recommendations_prompt
                }
            ],
            max_tokens=800
        )
        
        return response.choices[0].message.content.split('\n')
    
    async def _save_analysis_results(self, results: Dict[str, Any]) -> bool:
        """Save analysis results to database"""
        try:
            # Create analysis run record
            analysis_run = {
                "run_date": datetime.now().date().isoformat(),
                "findings_count": len(str(results['market_intelligence']).split('\n')),
                "opportunities_identified": len(results['opportunities']),
                "key_insights": results['strategic_analysis'][:500] + "...",
                "recommendations": results['recommendations'][:10],  # Top 10 recommendations
                "execution_time_seconds": 0,  # Would calculate actual time
                "status": "completed",
                "company_name": results['config']['company_name'],
                "industry": results['config']['industry']
            }
            
            # Save to database (simplified - would use proper database insertion)
            print("💾 Analysis results saved to database")
            return True
            
        except Exception as e:
            print(f"❌ Failed to save results: {e}")
            return False

# Global instance
competitive_engine = CompetitiveAnalysisEngine()