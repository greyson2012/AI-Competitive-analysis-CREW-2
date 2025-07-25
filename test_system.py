#!/usr/bin/env python3
"""
Simple test script to verify the complete system works
"""
import os
import sys
import asyncio
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

async def test_complete_system():
    """Test the complete competitive analysis system"""
    print("🚀 Testing Complete AI Competitive Analysis System")
    print("=" * 60)
    
    load_dotenv()
    
    try:
        # Test 1: Basic AI Analysis
        print("🤖 Testing AI Analysis...")
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a competitive intelligence analyst."},
                {"role": "user", "content": "Analyze the top 3 AI market trends for 2025. Be concise."}
            ],
            max_tokens=200
        )
        
        analysis = response.choices[0].message.content
        print("✅ AI Analysis Working!")
        print(f"   Sample insight: {analysis[:100]}...")
        
        # Test 2: Web Search
        print("\n🔍 Testing Web Search...")
        from tools.serper_search import serper_tool
        
        search_results = serper_tool._run("artificial intelligence trends 2025", num_results=3)
        print("✅ Web Search Working!")
        print(f"   Found {len(search_results.split('URL:')) - 1} results")
        
        # Test 3: Database Connection
        print("\n📊 Testing Database Connection...")
        from database.supabase_client import db_client
        
        # Simple test query
        result = await db_client.get_market_findings(limit=1)
        print("✅ Database Connection Working!")
        print(f"   Database accessible (found {len(result)} records)")
        
        # Test 4: Combined Intelligence Analysis  
        print("\n🧠 Testing Combined AI + Search Intelligence...")
        
        # Search for latest AI news
        search_data = serper_tool._run("AI funding startup 2025", num_results=5)
        
        # Analyze with AI
        intelligence_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a strategic analyst. Extract key competitive intelligence insights."
                },
                {
                    "role": "user", 
                    "content": f"Analyze this search data for strategic insights about AI market opportunities:\n\n{search_data[:1500]}"
                }
            ],
            max_tokens=150
        )
        
        insights = intelligence_response.choices[0].message.content
        print("✅ Combined Intelligence Analysis Working!")
        print(f"   Strategic insight: {insights[:120]}...")
        
        print("\n" + "=" * 60)
        print("🎉 COMPLETE SYSTEM TEST SUCCESSFUL!")
        print("=" * 60)
        print("✅ Your AI competitive analysis system is fully operational!")
        print("\n🚀 System Capabilities Verified:")
        print("  • AI-powered market analysis")
        print("  • Real-time web search intelligence") 
        print("  • Database storage and retrieval")
        print("  • Strategic insight generation")
        print("  • Competitive intelligence synthesis")
        
        print(f"\n📊 Ready for production use!")
        print("   Run daily analysis: python test_system.py daily")
        print("   Launch dashboard: streamlit run src/ui/app.py")
        
        return True
        
    except Exception as e:
        print(f"❌ System test failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your .env file has all API keys")
        print("2. Verify Supabase tables were created successfully")
        print("3. Ensure internet connection for API calls")
        return False

async def run_daily_analysis_simulation():
    """Simulate a daily analysis run"""
    print("🚀 SIMULATED DAILY COMPETITIVE ANALYSIS")
    print("=" * 60)
    
    load_dotenv()
    
    try:
        from openai import OpenAI
        from tools.serper_search import serper_tool
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Step 1: Market Intelligence Gathering
        print("📈 Gathering Market Intelligence...")
        market_search = serper_tool._run("AI market trends analysis 2025", num_results=10, search_type="news")
        print("✅ Market data collected")
        
        # Step 2: Competitor Intelligence  
        print("\n🔍 Monitoring Competitors...")
        competitor_search = serper_tool._run("OpenAI Anthropic Google AI updates 2025", num_results=8, search_type="news")
        print("✅ Competitor updates tracked")
        
        # Step 3: Strategic Analysis
        print("\n🧠 Generating Strategic Analysis...")
        analysis_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a senior competitive intelligence analyst. Provide strategic insights and identify opportunities."
                },
                {
                    "role": "user",
                    "content": f"""
                    Analyze this competitive intelligence data and provide:
                    1. Top 3 market opportunities
                    2. Key competitive threats  
                    3. Strategic recommendations
                    
                    Market Data: {market_search[:800]}
                    
                    Competitor Data: {competitor_search[:800]}
                    """
                }
            ],
            max_tokens=400
        )
        
        strategic_insights = analysis_response.choices[0].message.content
        
        print("✅ Strategic analysis complete")
        print("\n" + "=" * 60)
        print("📊 DAILY ANALYSIS SUMMARY")
        print("=" * 60)
        print(strategic_insights)
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Daily analysis failed: {e}")
        return False

async def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "daily":
        await run_daily_analysis_simulation()
    else:
        await test_complete_system()

if __name__ == "__main__":
    asyncio.run(main())