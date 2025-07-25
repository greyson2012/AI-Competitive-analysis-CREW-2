"""
Main entry point for the competitive analysis system
"""
import asyncio
import sys
import os
from datetime import datetime
from dotenv import load_dotenv

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crew import competitive_analysis_crew
from database.supabase_client import db_client

async def run_daily_analysis():
    """Run the daily competitive analysis"""
    print("=" * 60)
    print("🚀 COMPETITIVE ANALYSIS SYSTEM - DAILY RUN")
    print("=" * 60)
    
    try:
        # Test database connection
        print("🔌 Testing database connection...")
        test_summary = await db_client.get_analysis_summary(days=1)
        print("✅ Database connection successful")
        
        # Run the daily analysis
        results = await competitive_analysis_crew.run_daily_analysis()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 ANALYSIS SUMMARY")
        print("=" * 60)
        print(f"Status: {results.get('status', 'unknown')}")
        print(f"Execution Time: {results.get('execution_time', 0):.1f} seconds")
        
        if results.get('status') == 'completed':
            summary = results.get('summary', {})
            print(f"Market Findings: {summary.get('findings_count', 0)}")
            print(f"Competitor Updates: {summary.get('competitor_updates', 0)}")
            print(f"Trends Identified: {summary.get('trends_identified', 0)}")
            print(f"New Opportunities: {summary.get('opportunities_count', 0)}")
        
        print("=" * 60)
        return results
        
    except Exception as e:
        print(f"❌ Error in daily analysis: {e}")
        return {"status": "error", "error": str(e)}

async def run_weekly_summary():
    """Run the weekly summary analysis"""
    print("=" * 60)
    print("📊 COMPETITIVE ANALYSIS SYSTEM - WEEKLY SUMMARY")
    print("=" * 60)
    
    try:
        results = await competitive_analysis_crew.run_weekly_summary()
        print("✅ Weekly summary completed")
        return results
        
    except Exception as e:
        print(f"❌ Error in weekly summary: {e}")
        return {"status": "error", "error": str(e)}

async def run_quick_analysis(topic: str):
    """Run a quick focused analysis on a specific topic"""
    print("=" * 60)
    print(f"🔍 QUICK ANALYSIS: {topic.upper()}")
    print("=" * 60)
    
    try:
        results = await competitive_analysis_crew.run_quick_analysis(topic)
        print("✅ Quick analysis completed")
        return results
        
    except Exception as e:
        print(f"❌ Error in quick analysis: {e}")
        return {"status": "error", "error": str(e)}

def main():
    """Main function with command line argument handling"""
    load_dotenv()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py daily          # Run daily analysis")
        print("  python main.py weekly         # Run weekly summary")
        print("  python main.py quick <topic>  # Run quick analysis on topic")
        return
    
    command = sys.argv[1].lower()
    
    if command == "daily":
        asyncio.run(run_daily_analysis())
    elif command == "weekly":
        asyncio.run(run_weekly_summary())
    elif command == "quick" and len(sys.argv) > 2:
        topic = " ".join(sys.argv[2:])
        asyncio.run(run_quick_analysis(topic))
    else:
        print("Invalid command. Use 'daily', 'weekly', or 'quick <topic>'")

if __name__ == "__main__":
    main()