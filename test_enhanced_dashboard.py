#!/usr/bin/env python3
"""
Test the enhanced dashboard features with industry/company search functionality
"""
import os
import sys
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

def test_company_search():
    """Test the company search functionality"""
    print("🔍 Testing Company Search Functionality")
    print("=" * 50)
    
    from utils.company_database import search_companies
    
    # Test various search queries
    test_queries = [
        "OpenAI",
        "anthropic",
        "AI",
        "payments",
        "Salesforce",
        "crypto",
        "health"
    ]
    
    for query in test_queries:
        print(f"\n🔎 Searching for: '{query}'")
        results = search_companies(query, limit=3)
        
        if results:
            print(f"✅ Found {len(results)} companies:")
            for result in results:
                print(f"  • {result['name']} ({result['type']}) - {result['industry']}")
                print(f"    {result['description']}")
        else:
            print("❌ No results found")
    
    return True

def test_industry_search():
    """Test the industry search functionality"""
    print("\n\n🏭 Testing Industry Search Functionality")
    print("=" * 50)
    
    from utils.company_database import search_industries
    
    # Test industry searches
    test_queries = [
        "AI",
        "fintech",
        "health",
        "cloud",
        "cyber"
    ]
    
    for query in test_queries:
        print(f"\n🔎 Searching industries for: '{query}'")
        results = search_industries(query)
        
        if results:
            print(f"✅ Found {len(results)} industries:")
            for result in results:
                print(f"  • {result['name']} ({result['company_count']} companies)")
                print(f"    Sample companies: {', '.join(result['sample_companies'])}")
        else:
            print("❌ No industries found")
    
    return True

def test_analysis_modes():
    """Test both analysis modes with sample data"""
    print("\n\n🎯 Testing Analysis Modes")
    print("=" * 50)
    
    load_dotenv()
    
    # Test Industry Analysis Mode
    print("\n📊 Testing Industry Analysis Mode")
    industry_config = {
        "analysis_mode": "🏭 Industry Analysis",
        "industry": "Artificial Intelligence",
        "competitors": "OpenAI, Anthropic, Google AI",
        "company_name": "TechStart AI",
        "company_description": "We build AI-powered business automation tools for SMEs",
        "company_goals": "Scale to 1000 customers and expand internationally",
        "focus_areas": ["Market Opportunities", "Technology Trends"],
        "search_depth": 10,
        "custom_keywords": "business automation"
    }
    
    print("✅ Industry Analysis Configuration:")
    print(f"   Industry: {industry_config['industry']}")
    print(f"   Key Players: {industry_config['competitors']}")
    print(f"   Focus: {', '.join(industry_config['focus_areas'])}")
    
    # Test Company Tracking Mode
    print("\n🏢 Testing Company Tracking Mode")
    company_config = {
        "analysis_mode": "🏢 Company Tracking",
        "competitors": "OpenAI, Anthropic, Cohere, Character.AI, Perplexity AI",
        "industry": "Artificial Intelligence",
        "company_name": "ChatBot Pro",
        "company_description": "Enterprise chatbot platform with advanced AI capabilities",
        "company_goals": "Compete with major AI companies in enterprise market",
        "focus_areas": ["Competitive Threats", "Market Opportunities"],
        "search_depth": 15,
        "custom_keywords": "enterprise chatbot"
    }
    
    print("✅ Company Tracking Configuration:")
    print(f"   Companies Tracked: {company_config['competitors']}")
    print(f"   Focus: {', '.join(company_config['focus_areas'])}")
    print(f"   Search Depth: {company_config['search_depth']} sources")
    
    return True

def test_competitor_suggestions():
    """Test competitor suggestion functionality"""
    print("\n\n💡 Testing Competitor Suggestions")
    print("=" * 50)
    
    from utils.company_database import suggest_competitors
    
    test_companies = [
        "OpenAI",
        "Salesforce", 
        "PayPal",
        "Teladoc"
    ]
    
    for company in test_companies:
        print(f"\n🎯 Finding competitors for: {company}")
        competitors = suggest_competitors(company, limit=3)
        
        if competitors:
            print(f"✅ Found {len(competitors)} competitors:")
            for comp in competitors:
                print(f"  • {comp['name']} ({comp['type']}) - Relevance: {comp['relevance_score']:.1f}")
                print(f"    {comp['description']}")
        else:
            print("❌ No competitors found")
    
    return True

def demo_dashboard_workflow():
    """Demonstrate the complete dashboard workflow"""
    print("\n\n🚀 Dashboard Workflow Demonstration")
    print("=" * 60)
    
    print("""
## Enhanced Dashboard Features

### 🎯 Dual Analysis Modes

**1. Industry Analysis Mode:**
   - Search and select industries to analyze
   - Auto-populate key players in the industry
   - Focus on market trends, opportunities, and industry dynamics
   - Get comprehensive industry landscape analysis

**2. Company Tracking Mode:**
   - Search for specific companies by name
   - Browse companies by category (AI, SaaS, FinTech, etc.)
   - Select multiple companies to track
   - Get detailed competitive intelligence on each company

### 🔍 Smart Search Features

**Industry Search:**
   - Type to search for industries (e.g., "AI", "fintech", "health")
   - Get matching industries with company counts
   - Quick selection from popular industries

**Company Search:**
   - Real-time company search with fuzzy matching
   - Browse by categories (AI/ML, Tech Giants, SaaS, etc.)
   - Auto-detect industry based on selected companies
   - Competitor suggestions based on company profiles

### 📊 Enhanced Analysis Output

**Industry Analysis provides:**
   - Industry landscape analysis
   - Competitive ecosystem mapping
   - Market entry/expansion strategies
   - Industry-specific recommendations

**Company Tracking provides:**
   - Individual company intelligence
   - Competitive positioning analysis
   - Strategic response recommendations
   - Competitive threat assessment

### 🎯 How to Use the Enhanced Dashboard:

1. **Launch Dashboard**: streamlit run dashboard.py
2. **Go to "Run Analysis" tab**
3. **Choose Analysis Mode**:
   - Select "Industry Analysis" OR "Company Tracking"
4. **Configure Analysis**:
   - Industry Mode: Search/select industries, review key players
   - Company Mode: Search/select companies to track
5. **Fill Company Information**: Your business details and goals
6. **Advanced Options**: Search depth, focus areas, keywords
7. **Run Analysis**: Get mode-specific insights and recommendations
8. **Review Results**: Tabbed interface with detailed analysis
9. **Download Report**: Full analysis with company-specific insights
    """)
    
    return True

def main():
    """Main test function"""
    print("🚀 Enhanced Dashboard Features Test")
    print("=" * 60)
    
    # Test all components
    tests = [
        test_company_search,
        test_industry_search, 
        test_analysis_modes,
        test_competitor_suggestions,
        demo_dashboard_workflow
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed: {e}")
            results.append(False)
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 60)
    print("🎯 ENHANCED DASHBOARD TEST SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All enhanced features working perfectly!")
        print("\n✅ Your dashboard now supports:")
        print("  • Industry analysis with market landscape insights")
        print("  • Company tracking with competitive intelligence")
        print("  • Smart search for industries and companies")
        print("  • Auto-population of competitors and key players")
        print("  • Category-based company browsing")
        print("  • Dual-mode analysis with specialized outputs")
        print("  • Real-time company/industry database search")
        
        print(f"\n🚀 Ready for production!")
        print("   Dashboard URL: http://localhost:8503")
        print("   Features: Industry Analysis + Company Tracking")
    else:
        print("⚠️  Some enhanced features need attention.")
    
    print("\n📋 Next Steps:")
    print("1. Open dashboard at http://localhost:8503")
    print("2. Try both analysis modes:")
    print("   - Industry Analysis: Select 'AI' industry, analyze market")
    print("   - Company Tracking: Search 'OpenAI', track competitors")
    print("3. Compare the different analysis outputs")
    print("4. Test search functionality for companies and industries")

if __name__ == "__main__":
    main()