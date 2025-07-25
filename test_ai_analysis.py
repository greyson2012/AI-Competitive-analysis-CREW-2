#!/usr/bin/env python3
"""
Test AI analysis without database dependency
"""
import os
import sys
import asyncio
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

async def test_ai_analysis():
    """Test AI analysis capabilities"""
    print("🤖 Testing AI Analysis...")
    print("=" * 40)
    
    load_dotenv()
    
    try:
        # Test OpenAI integration
        from openai import OpenAI
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Simple market analysis test
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a competitive intelligence analyst specializing in AI markets."
                },
                {
                    "role": "user", 
                    "content": "Analyze the current AI market trends in 2024. Focus on: 1) Major developments, 2) Key competitive moves, 3) Emerging opportunities. Be concise."
                }
            ],
            max_tokens=300
        )
        
        analysis = response.choices[0].message.content
        
        print("✅ AI Analysis Working!")
        print(f"   Model: {response.model}")
        print(f"   Usage: {response.usage.total_tokens} tokens")
        print("\n📊 Sample Analysis:")
        print("-" * 40)
        print(analysis[:500] + "..." if len(analysis) > 500 else analysis)
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"❌ AI Analysis failed: {e}")
        return False

async def test_search_integration():
    """Test search + AI integration"""
    print("\n🔍 Testing Search + AI Integration...")
    print("=" * 40)
    
    try:
        from tools.serper_search import serper_tool
        from openai import OpenAI
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Search for AI news
        print("🔎 Searching for AI news...")
        search_results = serper_tool._run("AI startup funding 2024", num_results=3)
        
        # Analyze with AI
        print("🤖 Analyzing search results...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a competitive intelligence analyst. Analyze search results and extract key insights about AI funding trends."
                },
                {
                    "role": "user",
                    "content": f"Analyze these search results and provide 3 key insights about AI funding in 2024:\n\n{search_results[:2000]}"
                }
            ],
            max_tokens=200
        )
        
        insights = response.choices[0].message.content
        
        print("✅ Search + AI Integration Working!")
        print("\n💡 Key Insights:")
        print("-" * 40)
        print(insights)
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"❌ Search + AI Integration failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🚀 AI Competitive Analysis - Core Functionality Test")
    print("=" * 60)
    
    # Run tests
    test1 = await test_ai_analysis()
    test2 = await test_search_integration()
    
    # Summary
    passed = sum([test1, test2])
    total = 2
    
    print("\n" + "=" * 60)
    print("🎯 CORE FUNCTIONALITY TEST SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 Core AI functionality is working perfectly!")
        print("\n✅ Your system can:")
        print("  • Perform web searches for competitive intelligence")
        print("  • Analyze market data with AI")
        print("  • Generate strategic insights")
        print("  • Extract key information from search results")
        print("\n🔥 Ready for full deployment once database is set up!")
    else:
        print("⚠️  Some core tests failed. Check your API configuration.")

if __name__ == "__main__":
    asyncio.run(main())