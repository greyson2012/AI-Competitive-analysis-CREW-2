#!/usr/bin/env python3
"""
Integration test script for competitive analysis system
"""
import os
import sys
import asyncio
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test all imports work correctly"""
    print("🧪 Testing imports...")
    
    try:
        from database.supabase_client import db_client
        print("✅ Database client imported")
        
        from agents.market_intelligence import market_intelligence_agent
        print("✅ Market intelligence agent imported")
        
        from agents.competitor_intelligence import competitor_intelligence_agent
        print("✅ Competitor intelligence agent imported")
        
        from agents.trend_analysis import trend_analysis_agent
        print("✅ Trend analysis agent imported")
        
        from agents.strategic_synthesis import strategic_synthesis_agent
        print("✅ Strategic synthesis agent imported")
        
        from tools.serper_search import serper_tool
        print("✅ Search tool imported")
        
        from utils.gmail_client import gmail_client
        print("✅ Gmail client imported")
        
        from crew.crew import competitive_analysis_crew
        print("✅ Crew orchestrator imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

async def test_database_connection():
    """Test database connection"""
    print("\n🧪 Testing database connection...")
    
    try:
        from database.supabase_client import db_client
        
        # Test basic connection
        is_connected = await db_client.check_connection()
        if is_connected:
            print("✅ Database connection successful")
            
            # Test basic queries
            summary = await db_client.get_analysis_summary(days=1)
            print(f"✅ Analysis summary retrieved: {len(summary)} data points")
            
            return True
        else:
            print("❌ Database connection failed")
            return False
            
    except Exception as e:
        print(f"❌ Database test error: {e}")
        return False

async def test_search_functionality():
    """Test search functionality"""
    print("\n🧪 Testing search functionality...")
    
    try:
        from tools.serper_search import serper_tool
        
        # Test basic search
        results = serper_tool._run("AI news test", num_results=3)
        if results and len(results) > 100:  # Basic check for content
            print("✅ Search functionality working")
            return True
        else:
            print("❌ Search returned no results")
            return False
            
    except Exception as e:
        print(f"❌ Search test error: {e}")
        return False

async def test_email_configuration():
    """Test email configuration"""
    print("\n🧪 Testing email configuration...")
    
    try:
        from utils.gmail_client import gmail_client
        
        if gmail_client.enabled:
            print("✅ Gmail client configured and enabled")
            print(f"   Recipients: {len(gmail_client.notification_recipients)}")
        else:
            print("⚠️  Gmail client disabled (no credentials)")
        
        return True
        
    except Exception as e:
        print(f"❌ Email test error: {e}")
        return False

async def test_agents():
    """Test individual agents"""
    print("\n🧪 Testing agent functionality...")
    
    try:
        # Test market intelligence agent
        from agents.market_intelligence import market_intelligence_agent
        test_result = await market_intelligence_agent.analyze_specific_topic("AI trends")
        if test_result and not test_result.get('error'):
            print("✅ Market intelligence agent working")
        else:
            print("⚠️  Market intelligence agent has issues")
        
        # Test strategic synthesis agent
        from agents.strategic_synthesis import strategic_synthesis_agent
        briefing = await strategic_synthesis_agent.generate_executive_briefing()
        if briefing and not briefing.get('error'):
            print("✅ Strategic synthesis agent working")
        else:
            print("⚠️  Strategic synthesis agent has issues")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent test error: {e}")
        return False

def test_environment_variables():
    """Test environment variable configuration"""
    print("\n🧪 Testing environment variables...")
    
    load_dotenv()
    
    required_vars = [
        "SUPABASE_URL",
        "SUPABASE_KEY", 
        "OPENAI_API_KEY",
        "SERPER_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("   Copy .env.example to .env and configure these variables")
        return False
    else:
        print("✅ All required environment variables configured")
        return True

async def run_quick_test():
    """Run a quick end-to-end test"""
    print("\n🧪 Running quick end-to-end test...")
    
    try:
        from crew.crew import competitive_analysis_crew
        
        # Run a quick analysis
        results = await competitive_analysis_crew.run_quick_analysis("AI market test")
        
        if results and not results.get('error'):
            print("✅ End-to-end test successful")
            print(f"   Test completed for topic: {results.get('topic')}")
            return True
        else:
            print(f"❌ End-to-end test failed: {results.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"❌ End-to-end test error: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 Competitive Analysis System - Integration Test")
    print("=" * 60)
    
    # Check environment first
    if not test_environment_variables():
        print("\n❌ Environment configuration failed. Please configure .env file first.")
        return
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Check your Python environment.")
        return
    
    # Test async components
    test_results = []
    
    test_results.append(await test_database_connection())
    test_results.append(await test_search_functionality())
    test_results.append(await test_email_configuration())
    test_results.append(await test_agents())
    test_results.append(await run_quick_test())
    
    # Summary
    passed = sum(test_results)
    total = len(test_results)
    
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for use.")
        print("\nNext steps:")
        print("1. Run: python src/crew/main.py quick 'AI trends'")
        print("2. Run: streamlit run src/ui/app.py")
        print("3. Set up scheduling with: python src/utils/scheduler.py start")
    else:
        print("⚠️  Some tests failed. Please address the issues above.")
        print("\nCommon fixes:")
        print("1. Ensure all API keys are configured in .env")
        print("2. Verify Supabase database is set up")
        print("3. Check internet connection for search tests")

if __name__ == "__main__":
    asyncio.run(main())