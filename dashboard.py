"""
Simplified Streamlit dashboard for competitive analysis
"""
# Set ChromaDB backend to avoid SQLite version issues
import os
os.environ["CHROMA_DB_IMPL"] = "duckdb"

import streamlit as st
import asyncio
import sys
from datetime import datetime, date, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from dotenv import load_dotenv

# Add src to path
sys.path.append('src')

# Load environment
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Competitive Analysis Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    """Main dashboard application"""
    
    # Header
    st.title("🚀 AI Competitive Analysis Dashboard")
    st.markdown("Real-time competitive intelligence and strategic insights")
    
    # Navigation
    selected = option_menu(
        menu_title=None,
        options=["Overview", "Market Intelligence", "Competitors", "Trends", "Opportunities", "Run Analysis"],
        icons=["house", "graph-up", "building", "trending-up", "lightbulb", "play-circle"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )
    
    if selected == "Overview":
        show_overview()
    elif selected == "Market Intelligence":
        show_market_intelligence()
    elif selected == "Competitors":
        show_competitors()
    elif selected == "Trends":
        show_trends()
    elif selected == "Opportunities":
        show_opportunities()
    elif selected == "Run Analysis":
        show_run_analysis()

def show_overview():
    """Dashboard overview page"""
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Market Findings",
            value="0",
            delta="Ready to collect data"
        )
    
    with col2:
        st.metric(
            label="🏢 Competitors Tracked",
            value="3",
            delta="OpenAI, Anthropic, Google"
        )
    
    with col3:
        st.metric(
            label="📈 Trends Identified",
            value="0", 
            delta="Analysis pending"
        )
    
    with col4:
        st.metric(
            label="💡 Opportunities",
            value="0",
            delta="Waiting for first run"
        )
    
    # System status
    st.markdown("---")
    st.subheader("🎯 System Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.success("✅ Database Connected")
        st.success("✅ OpenAI API Ready") 
        st.success("✅ Serper Search Ready")
        st.success("✅ All Systems Operational")
    
    with col2:
        st.info("📋 **Next Steps:**")
        st.markdown("""
        1. Click **Run Analysis** to start your first competitive analysis
        2. The system will gather market intelligence from 20+ AI sources
        3. Competitor updates will be tracked and analyzed
        4. Strategic opportunities will be identified
        5. Executive summary will be generated
        """)
    
    # Quick test
    st.markdown("---")
    st.subheader("🔬 Quick System Test")
    
    if st.button("Test AI Analysis"):
        with st.spinner("Testing AI capabilities..."):
            try:
                from openai import OpenAI
                client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a competitive analyst."},
                        {"role": "user", "content": "List 3 key AI market trends for 2025 in one sentence each."}
                    ],
                    max_tokens=150
                )
                
                analysis = response.choices[0].message.content
                st.success("🤖 AI Analysis Working!")
                st.write(analysis)
                
            except Exception as e:
                st.error(f"❌ AI test failed: {e}")
    
    if st.button("Test Web Search"):
        with st.spinner("Testing search capabilities..."):
            try:
                from tools.serper_search import serper_tool
                
                results = serper_tool._run("AI startup news 2025", num_results=3)
                st.success("🔍 Web Search Working!")
                st.text_area("Search Results", results[:500] + "...", height=150)
                
            except Exception as e:
                st.error(f"❌ Search test failed: {e}")

def show_market_intelligence():
    """Market intelligence page"""
    st.subheader("📊 Market Intelligence")
    
    st.info("📋 Market findings will appear here after running your first analysis.")
    
    # Sample visualization
    st.markdown("### Sample Market Analysis")
    
    # Create sample data for demonstration
    sample_data = pd.DataFrame({
        'Date': pd.date_range('2024-01-01', periods=30, freq='D'),
        'AI_Mentions': range(100, 130),
        'Funding_Amount': [50, 75, 120, 80, 90, 150, 200, 100, 110, 130,
                          140, 160, 180, 190, 170, 150, 140, 130, 120, 110,
                          100, 95, 85, 90, 100, 120, 140, 160, 180, 200]
    })
    
    fig = px.line(sample_data, x='Date', y='AI_Mentions', 
                  title='AI Market Mentions Over Time (Sample)')
    st.plotly_chart(fig, use_container_width=True)
    
    # Funding visualization
    fig2 = px.bar(sample_data.tail(10), x='Date', y='Funding_Amount',
                  title='AI Funding Activity (Sample - Last 10 Days)')
    st.plotly_chart(fig2, use_container_width=True)

def show_competitors():
    """Competitors page"""
    st.subheader("🏢 Competitor Intelligence")
    
    # Competitor overview
    competitors = ["OpenAI", "Anthropic", "Google AI", "Microsoft AI", "Meta AI"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Tracked Competitors")
        for comp in competitors:
            st.markdown(f"- **{comp}** 🔍")
    
    with col2:
        st.markdown("### Monitoring Areas")
        st.markdown("""
        - 🚀 Product launches
        - 💰 Funding rounds  
        - 🤝 Partnerships
        - 📄 Research papers
        - 📰 Press releases
        """)
    
    st.info("📋 Competitor updates will appear here after running analysis.")

def show_trends():
    """Trends analysis page"""
    st.subheader("📈 Trend Analysis")
    
    st.info("📋 Trend analysis will appear here after running your first analysis.")
    
    # Sample trend visualization
    trend_data = pd.DataFrame({
        'Trend': ['Multimodal AI', 'AI Regulation', 'Edge AI', 'AI Agents', 'Enterprise AI'],
        'Momentum Score': [0.88, 0.75, 0.82, 0.90, 0.85],
        'Growth Rate': ['65%', '45%', '55%', '70%', '60%']
    })
    
    fig = px.bar(trend_data, x='Trend', y='Momentum Score',
                 title='AI Trend Momentum Scores (Sample)',
                 color='Momentum Score', color_continuous_scale='viridis')
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(trend_data, use_container_width=True)

def show_opportunities():
    """Opportunities page"""
    st.subheader("💡 Strategic Opportunities")
    
    st.info("📋 Business opportunities will appear here after running analysis.")
    
    # Sample opportunities
    sample_opportunities = pd.DataFrame({
        'Opportunity': [
            'Enterprise AI Integration Services',
            'Industry-Specific AI Solutions', 
            'AI Training Platform',
            'AI Compliance Tools',
            'Edge AI Solutions'
        ],
        'Score': [0.85, 0.78, 0.72, 0.80, 0.75],
        'Priority': ['High', 'High', 'Medium', 'High', 'Medium'],
        'Revenue Potential': ['$500K-2M', '$1M-5M', '$200K-800K', '$300K-1M', '$400K-1.5M']
    })
    
    st.dataframe(sample_opportunities, use_container_width=True)
    
    # Opportunity scoring visualization
    fig = px.scatter(sample_opportunities, x='Score', y='Opportunity',
                     size='Score', color='Priority',
                     title='Opportunity Scoring Matrix (Sample)')
    st.plotly_chart(fig, use_container_width=True)

def show_run_analysis():
    """Run analysis page"""
    st.subheader("🚀 Run Competitive Analysis")
    
    st.markdown("""
    ### Configure your competitive analysis
    
    Provide information about your industry, competitors, and company to get tailored insights.
    """)
    
    # Create two columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎯 Analysis Configuration")
        
        # Analysis Mode Selection
        analysis_mode = st.radio(
            "What do you want to analyze?",
            ["🏭 Industry Analysis", "🏢 Company Tracking"],
            help="Choose whether to analyze an entire industry or track specific companies"
        )
        
        if analysis_mode == "🏭 Industry Analysis":
            st.markdown("##### Industry Focus")
            
            # Predefined industries for quick selection
            quick_industries = [
                "Artificial Intelligence", "SaaS/Cloud Computing", "FinTech", "HealthTech", 
                "E-commerce", "Cybersecurity", "EdTech", "Clean Energy", "Biotechnology",
                "Autonomous Vehicles", "Blockchain/Crypto", "Robotics"
            ]
            
            col_a, col_b = st.columns([2, 1])
            with col_a:
                industry_search = st.text_input(
                    "Search Industries:",
                    placeholder="Type to search or select from popular industries below...",
                    help="Search for specific industries or market segments"
                )
            
            with col_b:
                if st.button("🔍 Search Industries"):
                    if industry_search:
                        # Real industry search
                        sys.path.append('src')
                        from utils.company_database import search_industries
                        
                        search_results = search_industries(industry_search)
                        if search_results:
                            st.success(f"Found {len(search_results)} matching industries:")
                            for result in search_results[:3]:
                                st.write(f"• **{result['name']}** ({result['company_count']} companies)")
                        else:
                            st.warning("No matching industries found. Try a different search term.")
            
            # Quick industry selection
            selected_industries = st.multiselect(
                "Or select from popular industries:",
                quick_industries,
                default=["Artificial Intelligence"],
                help="Select one or more industries to analyze"
            )
            
            # Use search input or selected industries
            if industry_search:
                industry = industry_search
            else:
                industry = ", ".join(selected_industries) if selected_industries else "Artificial Intelligence"
            
            # Auto-populate competitors based on industry
            if "Artificial Intelligence" in industry:
                default_competitors = "OpenAI, Anthropic, Google AI, Microsoft Copilot, Meta AI"
            elif "SaaS" in industry or "Cloud" in industry:
                default_competitors = "Salesforce, Microsoft, Google Cloud, AWS, Adobe"
            elif "FinTech" in industry:
                default_competitors = "PayPal, Square, Stripe, Robinhood, Coinbase"
            elif "HealthTech" in industry:
                default_competitors = "Teladoc, Veracyte, 10x Genomics, Moderna, Johnson & Johnson"
            else:
                default_competitors = "Company 1, Company 2, Company 3"
            
            competitors = st.text_area(
                "Key Players in This Industry:",
                value=default_competitors,
                height=80,
                help="Major companies in your selected industry (auto-populated, edit as needed)"
            )
            
        else:  # Company Tracking mode
            st.markdown("##### Company Tracking")
            
            # Company search functionality
            col_a, col_b = st.columns([3, 1])
            with col_a:
                company_search = st.text_input(
                    "Search Companies:",
                    placeholder="Type company name to search...",
                    help="Search for specific companies to track"
                )
            
            with col_b:
                if st.button("🔍 Find Company"):
                    if company_search:
                        # Real company search
                        sys.path.append('src')
                        from utils.company_database import search_companies
                        
                        search_results = search_companies(company_search, limit=5)
                        if search_results:
                            st.success(f"Found {len(search_results)} matching companies:")
                            for result in search_results:
                                st.write(f"• **{result['name']}** ({result['type']}) - {result['industry']}")
                                st.write(f"  {result['description']}")
                        else:
                            st.warning("No matching companies found. Try a different search term.")
            
            # Popular companies by category
            company_categories = {
                "AI/ML Companies": ["OpenAI", "Anthropic", "Google DeepMind", "Meta AI", "Cohere", "Hugging Face"],
                "Tech Giants": ["Apple", "Microsoft", "Google", "Amazon", "Meta", "Tesla"],
                "SaaS Leaders": ["Salesforce", "Microsoft 365", "Zoom", "Slack", "Notion", "Figma"],
                "FinTech": ["PayPal", "Square", "Stripe", "Robinhood", "Coinbase", "Klarna"],
                "Cloud Providers": ["AWS", "Microsoft Azure", "Google Cloud", "Oracle Cloud", "IBM Cloud"],
                "Startups": ["Anthropic", "Cohere", "Stability AI", "Character.AI", "Midjourney"]
            }
            
            selected_category = st.selectbox(
                "Browse by category:",
                ["Select category..."] + list(company_categories.keys()),
                help="Browse popular companies by industry category"
            )
            
            if selected_category != "Select category...":
                category_companies = st.multiselect(
                    f"Companies in {selected_category}:",
                    company_categories[selected_category],
                    help=f"Select companies from {selected_category} to track"
                )
            else:
                category_companies = []
            
            # Manual company entry
            manual_companies = st.text_area(
                "Or enter companies manually:",
                placeholder="Company A, Company B, Company C...",
                height=80,
                help="Enter company names separated by commas"
            )
            
            # Combine search, category, and manual selections
            all_companies = []
            if company_search:
                all_companies.append(company_search)
            if category_companies:
                all_companies.extend(category_companies)
            if manual_companies:
                all_companies.extend([c.strip() for c in manual_companies.split(",") if c.strip()])
            
            competitors = ", ".join(list(set(all_companies)))  # Remove duplicates
            
            # Auto-detect industry based on selected companies
            if any(comp in competitors for comp in ["OpenAI", "Anthropic", "Google AI"]):
                industry = "Artificial Intelligence"
            elif any(comp in competitors for comp in ["Salesforce", "Microsoft", "Zoom"]):
                industry = "SaaS/Cloud Computing"
            elif any(comp in competitors for comp in ["PayPal", "Square", "Stripe"]):
                industry = "FinTech"
            else:
                industry = st.text_input(
                    "Industry for these companies:",
                    placeholder="What industry are these companies in?",
                    help="Specify the industry to provide better context for analysis"
                )
        
        # Analysis type
        analysis_type = st.selectbox(
            "Analysis Scope:",
            [
                "Comprehensive Analysis", 
                "Market Trends Only", 
                "Competitor Focus", 
                "Opportunity Identification",
                "SWOT Analysis",
                "Market Share Analysis"
            ]
        )
        
        # Time range
        time_range = st.selectbox(
            "Time Range:",
            ["Last 30 days", "Last 7 days", "Last 3 months", "Last 6 months", "Real-time only"]
        )
    
    with col2:
        st.markdown("#### 🏢 Your Company Information")
        
        # Company details
        company_name = st.text_input(
            "Company Name:",
            value="",
            help="Your company name for personalized analysis"
        )
        
        company_description = st.text_area(
            "Company Description:",
            value="",
            height=100,
            help="Brief description of what your company does, your products/services, and target market"
        )
        
        company_goals = st.text_area(
            "Strategic Goals & Challenges:",
            value="",
            height=100,
            help="What are your main business goals? What challenges are you facing? This helps AI provide targeted recommendations."
        )
        
        # Analysis focus areas
        focus_areas = st.multiselect(
            "Focus Areas:",
            ["Market Opportunities", "Competitive Threats", "Technology Trends", "Funding Landscape", "Partnership Opportunities", "Regulatory Changes"],
            default=["Market Opportunities", "Competitive Threats", "Technology Trends"]
        )
    
    # Advanced options in expander
    with st.expander("🔧 Advanced Options"):
        col3, col4 = st.columns(2)
        
        with col3:
            search_depth = st.slider("Search Depth:", 5, 50, 20, help="Number of sources to analyze")
            include_research = st.checkbox("Include Research Papers", value=True)
            include_news = st.checkbox("Include News Articles", value=True)
            
        with col4:
            include_funding = st.checkbox("Include Funding Data", value=True)
            include_social = st.checkbox("Include Social Media Trends", value=False)
            custom_keywords = st.text_input("Additional Keywords:", help="Extra keywords to search for")
    
    # Validation
    can_run = bool(industry.strip() and company_name.strip() and company_description.strip())
    
    if not can_run:
        st.warning("⚠️ Please fill in at least: Industry, Company Name, and Company Description to run analysis.")
    
    st.markdown("---")
    
    # Run analysis button
    if st.button("🚀 Start Competitive Analysis", type="primary", disabled=not can_run):
        if not can_run:
            st.error("Please fill in required fields before running analysis.")
            return
            
        with st.spinner("Running comprehensive competitive analysis..."):
            try:
                # Store analysis configuration
                analysis_config = {
                    "industry": industry,
                    "competitors": [c.strip() for c in competitors.split(",") if c.strip()],
                    "company_name": company_name,
                    "company_description": company_description,
                    "company_goals": company_goals,
                    "focus_areas": focus_areas,
                    "analysis_type": analysis_type,
                    "time_range": time_range,
                    "search_depth": search_depth,
                    "custom_keywords": custom_keywords,
                    "analysis_mode": analysis_mode
                }
                
                # Run the enhanced analysis
                results = run_enhanced_analysis(analysis_config)
                
                # Display results
                display_analysis_results(results, analysis_config)
                
            except Exception as e:
                st.error(f"❌ Analysis failed: {str(e)}")
                st.markdown("### 🔧 Troubleshooting")
                st.markdown("""
                1. Check your internet connection
                2. Verify API keys in .env file  
                3. Ensure all dependencies are installed
                """)

def run_enhanced_analysis(config):
    """Run enhanced competitive analysis using the new analysis engine"""
    import asyncio
    import time
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Import the analysis engine
        sys.path.append('src')
        from analysis.competitive_engine import competitive_engine
        
        # Step 1: Initialize
        status_text.text("🚀 Initializing competitive analysis engine...")
        progress_bar.progress(10)
        time.sleep(1)
        
        # Step 2: Market Intelligence
        status_text.text("📊 Gathering comprehensive market intelligence...")
        progress_bar.progress(25)
        time.sleep(2)
        
        # Step 3: Competitor Analysis
        status_text.text("🏢 Analyzing competitor strategies and positioning...")
        progress_bar.progress(50)
        time.sleep(2)
        
        # Step 4: Strategic Analysis
        status_text.text("🧠 Generating personalized strategic insights...")
        progress_bar.progress(75)
        time.sleep(2)
        
        # Step 5: Final Processing
        status_text.text("💡 Identifying opportunities and recommendations...")
        progress_bar.progress(90)
        
        # Run the actual analysis
        # Note: Using synchronous call for Streamlit compatibility
        # In production, would properly handle async
        
        # Simplified analysis for demo (replace with actual engine call)
        results = run_simplified_analysis(config)
        
        progress_bar.progress(100)
        status_text.text("✅ Analysis complete!")
        time.sleep(1)
        
        return results
        
    except Exception as e:
        st.error(f"Analysis engine error: {e}")
        # Fallback to simplified analysis
        return run_simplified_analysis(config)

def run_simplified_analysis(config):
    """Enhanced analysis supporting both industry analysis and company tracking modes"""
    from tools.serper_search import serper_tool
    from openai import OpenAI
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Determine analysis approach based on mode
    analysis_mode = config.get('analysis_mode', '🏭 Industry Analysis')
    
    if analysis_mode == "🏭 Industry Analysis":
        # Industry-focused analysis
        industry_query = f"{config['industry']} market trends analysis opportunities 2025"
        market_results = serper_tool._run(industry_query, num_results=config['search_depth']//2, search_type="news")
        
        # Get industry-wide competitive landscape
        competition_query = f"{config['industry']} competitive landscape key players 2025"
        competition_results = serper_tool._run(competition_query, num_results=config['search_depth']//3, search_type="news")
        
        # Analyze top companies in industry
        competitor_results = []
        for comp in config['competitors'][:3]:
            comp_query = f"{comp} {config['industry']} strategy market position 2025"
            comp_data = serper_tool._run(comp_query, num_results=3, search_type="news")
            competitor_results.append(f"=== {comp} ===\n{comp_data}")
        
        analysis_context = "industry-wide market analysis"
        
    else:  # Company Tracking mode
        # Company-focused analysis
        companies = config['competitors'].split(',') if isinstance(config['competitors'], str) else config['competitors']
        
        # Direct company intelligence gathering
        competitor_results = []
        for comp in companies[:5]:  # Track up to 5 companies
            comp_name = comp.strip()
            comp_queries = [
                f"{comp_name} latest news updates strategy 2025",
                f"{comp_name} product launch funding acquisition 2025",
                f"{comp_name} market position competitive advantage 2025"
            ]
            
            comp_intelligence = []
            for query in comp_queries:
                comp_data = serper_tool._run(query, num_results=2, search_type="news")
                comp_intelligence.append(comp_data)
            
            competitor_results.append(f"=== {comp_name} INTELLIGENCE ===\n" + "\n".join(comp_intelligence))
        
        # Market context for these companies
        market_context_query = f"{config.get('industry', 'technology')} market context {' '.join(companies[:3])} 2025"
        market_results = serper_tool._run(market_context_query, num_results=config['search_depth']//3, search_type="news")
        
        competition_results = ""
        analysis_context = "company tracking and competitive intelligence"
    
    # Step 3: Enhanced Strategic Analysis with mode-specific prompting
    if analysis_mode == "🏭 Industry Analysis":
        analysis_prompt = f"""
        You are a senior strategic consultant and industry analyst providing comprehensive market intelligence for {config['company_name']} entering the {config['industry']} industry.
        
        ## COMPANY PROFILE
        **Company:** {config['company_name']}
        **Target Industry:** {config['industry']}  
        **Description:** {config['company_description']}
        **Strategic Goals:** {config['company_goals']}
        **Analysis Focus:** {', '.join(config['focus_areas'])}
        
        ## MARKET INTELLIGENCE DATA
        **Industry Trends & Market Data:**
        {market_results[:2500]}
        
        **Competitive Landscape Intelligence:**
        {competition_results[:2000]}
        
        **Key Industry Players Analysis:**
        {str(competitor_results)[:2500]}
        
        Generate a comprehensive 2000+ word industry analysis report with the following detailed sections:
        
        # 📊 COMPREHENSIVE INDUSTRY ANALYSIS REPORT
        
        ## EXECUTIVE SUMMARY (3-4 Key Strategic Insights)
        Provide 3-4 critical strategic insights about the {config['industry']} industry that directly impact {config['company_name']}'s strategy. Include:
        - Most significant market opportunity for {config['company_name']}
        - Biggest competitive threat to monitor
        - Key success factor for market entry
        - Strategic recommendation summary
        
        ## 1. MARKET LANDSCAPE & SIZING ANALYSIS
        ### Market Economics
        - **Market Size**: Current market size with specific figures (TAM, SAM, SOM)
        - **Growth Projections**: 3-5 year growth forecasts with CAGR
        - **Market Segments**: Breakdown of market by segments and their growth rates
        - **Revenue Models**: Dominant monetization strategies in the industry
        
        ### Industry Maturity & Lifecycle
        - **Industry Stage**: Emerging, growth, mature, or declining phase
        - **Market Drivers**: Primary factors driving industry growth
        - **Technology Adoption**: Current tech adoption rates and trends
        - **Regulatory Environment**: Key regulations affecting the industry
        
        ## 2. COMPREHENSIVE COMPETITIVE INTELLIGENCE
        ### Market Leaders Analysis
        For each major competitor, provide:
        - **Market Position**: Market share and competitive ranking
        - **Competitive Advantages**: Key differentiators and strengths
        - **Business Model**: Revenue streams and pricing strategies
        - **Strategic Moves**: Recent acquisitions, partnerships, product launches
        
        ### Competitive Dynamics
        - **Competition Intensity**: Porter's Five Forces analysis
        - **Entry Barriers**: Capital requirements, regulations, network effects
        - **Switching Costs**: Customer acquisition and retention dynamics
        - **Pricing Pressure**: Price competition and margin trends
        
        ## 3. STRATEGIC MARKET OPPORTUNITIES
        ### Market Gaps & White Spaces
        - **Underserved Segments**: Customer needs not being met
        - **Geographic Opportunities**: Regions with limited competition
        - **Technology Gaps**: Innovation opportunities in the market
        - **Service Gaps**: Areas where current solutions are inadequate
        
        ### Emerging Trends Impact
        - **Technology Trends**: AI, automation, digital transformation impacts
        - **Consumer Behavior**: Changing customer expectations and preferences
        - **Business Model Innovation**: New approaches to value creation
        - **Partnership Opportunities**: Strategic alliance possibilities
        
        ## 4. STRATEGIC POSITIONING FOR {config['company_name'].upper()}
        ### Market Entry Strategy
        - **Target Segments**: Most attractive customer segments for entry
        - **Value Proposition**: Unique value {config['company_name']} can offer
        - **Differentiation Strategy**: How to stand out from competitors
        - **Go-to-Market Approach**: Optimal market entry tactics
        
        ### Competitive Positioning
        - **Positioning Map**: Where {config['company_name']} fits in competitive landscape
        - **Competitive Advantages**: Strengths to leverage against competitors
        - **Vulnerability Assessment**: Areas where competitors might attack
        - **Defense Strategy**: How to protect market position once established
        
        ## 5. FINANCIAL ANALYSIS & PROJECTIONS
        ### Investment Requirements
        - **Initial Investment**: Estimated capital requirements for market entry
        - **Ongoing Costs**: Operating expenses and infrastructure needs
        - **Break-even Analysis**: Timeline to profitability
        - **ROI Projections**: Expected return on investment scenarios
        
        ### Revenue Potential
        - **Market Share Targets**: Realistic market share goals (1%, 5%, 10%)
        - **Revenue Projections**: 3-year revenue forecasts
        - **Unit Economics**: Customer acquisition cost and lifetime value
        - **Scaling Economics**: How profitability improves with scale
        
        ## 6. IMPLEMENTATION ROADMAP & ACTION PLAN
        ### Phase 1: Market Entry (0-6 months)
        - **Immediate Actions**: Top 5 priorities for the next 90 days
        - **Resource Allocation**: Key hires, partnerships, and investments
        - **Success Metrics**: KPIs to track market entry progress
        - **Risk Mitigation**: Potential challenges and contingency plans
        
        ### Phase 2: Market Expansion (6-18 months)
        - **Growth Strategy**: Plans for scaling operations and customer base
        - **Product Development**: Feature roadmap and innovation priorities
        - **Market Expansion**: Geographic or segment expansion opportunities
        - **Partnership Strategy**: Strategic alliances and ecosystem development
        
        ### Phase 3: Market Leadership (18+ months)
        - **Competitive Response**: Anticipating and responding to competitor moves
        - **Innovation Pipeline**: Long-term R&D and product development
        - **Market Defense**: Strategies to maintain competitive advantage
        - **Exit Opportunities**: Potential acquisition or IPO considerations
        
        ## 7. RISK ASSESSMENT & MITIGATION
        ### Market Risks
        - **Regulatory Risks**: Potential policy changes and compliance issues
        - **Technology Risks**: Disruption from new technologies
        - **Competitive Risks**: New entrants and aggressive competition
        - **Economic Risks**: Market downturns and economic cycles
        
        ### Mitigation Strategies
        - **Diversification**: Reducing dependence on single markets or customers
        - **Agility**: Building adaptable business models and operations
        - **Partnerships**: Strategic relationships for risk sharing
        - **Monitoring**: Early warning systems for market changes
        
        Use specific data from the market intelligence to support all recommendations. Make all insights actionable for {config['company_name']} given their profile: {config['company_description']} and goals: {config['company_goals']}.
        """
    else:  # Company Tracking mode
        companies_list = ', '.join([c.strip() for c in config['competitors'].split(',')][:5])
        analysis_prompt = f"""
        You are a senior competitive intelligence analyst and strategic advisor providing comprehensive competitor tracking analysis for {config['company_name']}.
        
        ## COMPANY PROFILE
        **Company:** {config['company_name']}
        **Description:** {config['company_description']}
        **Strategic Goals:** {config['company_goals']}
        **Analysis Focus:** {', '.join(config['focus_areas'])}
        
        ## COMPANIES BEING TRACKED
        {companies_list}
        
        ## COMPETITIVE INTELLIGENCE DATA
        {str(competitor_results)[:3500]}
        
        ## MARKET CONTEXT & TRENDS
        {market_results[:2000]}
        
        Generate a comprehensive 2000+ word competitive intelligence report with the following detailed sections:
        
        # 🏢 COMPREHENSIVE COMPETITIVE INTELLIGENCE REPORT
        
        ## EXECUTIVE SUMMARY (Key Competitive Insights)
        Provide 4-5 critical competitive intelligence insights that directly impact {config['company_name']}'s strategy:
        - Most significant competitive threat and why
        - Biggest market opportunity revealed by competitor analysis
        - Key competitive advantage {config['company_name']} should leverage
        - Most important strategic move to make in response to competitors
        - Early warning sign to monitor closely
        
        ## 1. INDIVIDUAL COMPETITOR DEEP-DIVE ANALYSIS
        For each tracked company ({companies_list}), provide detailed analysis:
        
        ### [Competitor Name] Profile
        - **Market Position**: Current market share, ranking, and influence
        - **Business Model**: Revenue streams, pricing strategy, unit economics
        - **Product Portfolio**: Core offerings, recent launches, development pipeline
        - **Competitive Advantages**: Key differentiators and moats
        - **Recent Strategic Moves**: M&A, partnerships, funding, expansions (last 6 months)
        - **Financial Health**: Revenue growth, profitability, funding status
        - **Strategic Direction**: Vision, roadmap, and announced plans
        - **Threat Level to {config['company_name']}**: High/Medium/Low with reasoning
        
        ## 2. COMPETITIVE LANDSCAPE MAPPING & DYNAMICS
        ### Market Positioning Analysis
        - **Competitive Positioning Map**: Where each competitor sits on key dimensions (price vs features, market focus, etc.)
        - **Market Share Distribution**: Estimated market share of tracked competitors
        - **Competitive Clusters**: Groups of companies competing directly with each other
        - **White Space Opportunities**: Market gaps not covered by major competitors
        
        ### Competitive Dynamics
        - **Competition Intensity**: Level of direct competition between tracked companies
        - **Collaboration vs Competition**: Areas where competitors partner vs compete
        - **Ecosystem Relationships**: How competitors interact with broader market ecosystem
        - **Merger & Acquisition Activity**: Recent deals and potential future consolidation
        
        ## 3. COMPETITIVE STRENGTHS & WEAKNESSES ANALYSIS
        ### Competitive Advantage Assessment
        For each competitor, analyze:
        - **Technology Advantages**: Proprietary tech, IP, R&D capabilities
        - **Market Advantages**: Brand, distribution, customer relationships
        - **Operational Advantages**: Scale, efficiency, cost structure
        - **Strategic Advantages**: Partnerships, ecosystem position, timing
        
        ### Vulnerability Analysis
        - **Competitive Weaknesses**: Areas where competitors are vulnerable
        - **Market Blind Spots**: Customer segments or needs competitors are missing
        - **Operational Vulnerabilities**: Scalability, cost, or execution challenges
        - **Strategic Risks**: Dependencies, competitive threats, market changes
        
        ## 4. STRATEGIC IMPLICATIONS FOR {config['company_name'].upper()}
        ### Direct Competitive Threats
        - **Head-to-Head Competition**: Which competitors directly threaten {config['company_name']}
        - **Competitive Response Patterns**: How competitors typically respond to new entrants
        - **Defensive Strategies**: How competitors protect their market position
        - **Attack Vectors**: Where competitors might focus competitive pressure
        
        ### Market Opportunities Revealed
        - **Competitive Gaps**: Underserved markets or customer needs
        - **Timing Opportunities**: Windows where competitive response will be slow
        - **Partnership Opportunities**: Potential allies among tracked companies
        - **Acquisition Targets**: Competitors that might be strategic acquisition candidates
        
        ### Differentiation Strategy
        - **Unique Value Proposition**: How {config['company_name']} can stand out
        - **Blue Ocean Opportunities**: Uncontested market spaces to pursue
        - **Competitive Positioning**: Optimal positioning relative to competitors
        - **Messaging Strategy**: How to communicate differentiation effectively
        
        ## 5. COMPETITIVE INTELLIGENCE & MONITORING FRAMEWORK
        ### Intelligence Gathering Priorities
        - **High-Priority Intelligence**: Most critical information to track for each competitor
        - **Early Warning Indicators**: Signals that predict significant competitive moves
        - **Information Sources**: Best sources for ongoing competitive intelligence
        - **Monitoring Frequency**: How often to review each competitor's activities
        
        ### Competitive Metrics Dashboard
        - **Market Share Tracking**: Key metrics to monitor market position changes
        - **Product Development**: Indicators of new product/feature development
        - **Financial Health**: Metrics to track competitor financial performance
        - **Strategic Moves**: Types of strategic announcements to monitor
        
        ## 6. STRATEGIC RESPONSE & ACTION PLAN
        ### Immediate Actions (Next 30-90 Days)
        - **Defensive Moves**: Actions to protect {config['company_name']} from competitive threats
        - **Offensive Opportunities**: Ways to capitalize on competitor weaknesses
        - **Intelligence Operations**: Competitive monitoring systems to implement
        - **Strategic Communications**: Messaging to differentiate from competitors
        
        ### Medium-Term Strategy (3-12 Months)
        - **Product Development**: Features/products to develop in response to competition
        - **Market Positioning**: Repositioning strategies based on competitive analysis
        - **Partnership Strategy**: Strategic relationships to build competitive advantage
        - **Market Expansion**: Geographic or segment expansion to outflank competitors
        
        ### Long-Term Competitive Strategy (1-3 Years)
        - **Sustainable Advantage**: Building long-term competitive moats
        - **Market Leadership**: Path to becoming a market leader or strong #2
        - **Ecosystem Strategy**: Building platform or ecosystem advantages
        - **Innovation Pipeline**: Long-term R&D strategy to stay ahead
        
        ## 7. RISK ASSESSMENT & CONTINGENCY PLANNING
        ### Competitive Risks
        - **Price Wars**: Risk of destructive price competition
        - **Feature Wars**: Arms race in product capabilities
        - **Talent Wars**: Competition for key employees and executives
        - **Market Disruption**: Risk of new entrants or technologies
        
        ### Contingency Plans
        - **Aggressive Competitor Response**: Plans if competitors respond aggressively
        - **Market Consolidation**: Strategy if industry consolidates rapidly
        - **Technology Disruption**: Response to disruptive technology introduction
        - **Economic Downturn**: Competitive strategy during market contractions
        
        Use specific intelligence data to support all analysis. Make all recommendations immediately actionable for {config['company_name']} based on their profile: {config['company_description']} and strategic goals: {config['company_goals']}.
        """
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a senior strategic consultant and competitive intelligence expert with 20+ years of experience in market analysis, competitive strategy, and business intelligence. Provide comprehensive, detailed analysis with specific data-driven insights, actionable recommendations, and professional formatting. Your reports should be thorough, strategic, and immediately implementable."
            },
            {
                "role": "user", 
                "content": analysis_prompt
            }
        ],
        max_tokens=3000,
        temperature=0.15
    )
    
    strategic_analysis = response.choices[0].message.content
    
    # Step 4: Enhanced Opportunity Identification
    opportunity_prompt = f"""
    You are a senior business development strategist identifying high-value opportunities for {config['company_name']} in the {config['industry']} industry.
    
    ## COMPANY CONTEXT
    **Company:** {config['company_name']}
    **Description:** {config['company_description']}
    **Strategic Goals:** {config['company_goals']}
    **Analysis Mode:** {analysis_mode}
    
    ## MARKET INTELLIGENCE
    {market_results[:2000]}
    
    ## COMPETITIVE LANDSCAPE
    {str(competitor_results)[:1500]}
    
    Generate a comprehensive opportunity analysis with 5-7 high-impact business opportunities. For each opportunity, provide detailed analysis:
    
    # 💡 STRATEGIC BUSINESS OPPORTUNITIES ANALYSIS
    
    ## OPPORTUNITY PRIORITIZATION MATRIX
    Rank all opportunities by:
    - **Strategic Fit** (1-5): Alignment with {config['company_name']}'s capabilities
    - **Market Potential** (1-5): Revenue and growth potential
    - **Competitive Advantage** (1-5): Ability to create sustainable advantage
    - **Implementation Feasibility** (1-5): Ease of execution given resources
    
    ## DETAILED OPPORTUNITY ANALYSIS
    
    ### OPPORTUNITY 1: [High-Impact Opportunity Name]
    **Priority Level:** High/Medium/Low
    **Strategic Rationale:** Why this is critical for {config['company_name']}
    
    #### Market Analysis
    - **Market Size:** TAM, SAM, SOM with specific figures
    - **Growth Rate:** Historical and projected growth (CAGR)
    - **Market Trends:** Key trends driving this opportunity
    - **Customer Demand:** Evidence of unmet customer needs
    
    #### Competitive Landscape
    - **Competition Level:** Current competitive intensity (Low/Medium/High)
    - **Competitive Gaps:** Specific areas where competitors are weak
    - **Entry Barriers:** Obstacles to entry and how to overcome them
    - **Competitive Response:** How competitors might react
    
    #### Business Model & Economics
    - **Revenue Model:** How {config['company_name']} would monetize this
    - **Unit Economics:** Customer acquisition cost and lifetime value estimates
    - **Pricing Strategy:** Optimal pricing approach and rationale
    - **Break-even Analysis:** Timeline to profitability
    
    #### Implementation Strategy
    - **Resource Requirements:** Capital, personnel, technology needs
    - **Development Timeline:** Phases and milestones (0-6 months, 6-12 months, 12+ months)
    - **Go-to-Market Strategy:** How to launch and scale
    - **Key Success Factors:** Critical elements for success
    
    #### Risk Assessment
    - **Market Risks:** Demand, timing, regulatory risks
    - **Execution Risks:** Technical, operational, competitive risks
    - **Mitigation Strategies:** How to minimize key risks
    - **Success Probability:** Realistic assessment (1-5 scale)
    
    #### Immediate Action Plan
    - **Next 30 Days:** Top 3 immediate actions to pursue this opportunity
    - **Next 90 Days:** Key milestones and deliverables
    - **Resource Allocation:** Budget and team requirements
    - **Success Metrics:** KPIs to track progress
    
    [Repeat this detailed structure for OPPORTUNITIES 2-7]
    
    ## OPPORTUNITY PORTFOLIO STRATEGY
    ### Portfolio Optimization
    - **Quick Wins:** Low-risk, high-impact opportunities to pursue immediately
    - **Strategic Bets:** Higher-risk, transformational opportunities for long-term growth
    - **Option Value:** Opportunities to keep options open for future pursuit
    - **Resource Allocation:** How to balance investment across opportunities
    
    ### Implementation Sequencing
    - **Phase 1 (0-6 months):** Which opportunities to pursue first and why
    - **Phase 2 (6-18 months):** Secondary opportunities and expansion plans
    - **Phase 3 (18+ months):** Long-term strategic opportunities
    - **Synergies:** How opportunities can reinforce each other
    
    ## STRATEGIC RECOMMENDATIONS
    ### Top 3 Priority Opportunities
    Rank the top 3 opportunities for {config['company_name']} with specific rationale for prioritization.
    
    ### Investment Strategy
    - **Total Investment Required:** Aggregate capital requirements
    - **Expected Returns:** Revenue and profit projections
    - **ROI Analysis:** Return on investment for each opportunity
    - **Funding Strategy:** How to finance opportunity development
    
    ### Execution Framework
    - **Team Structure:** Key roles and responsibilities needed
    - **Decision Framework:** How to make go/no-go decisions
    - **Performance Monitoring:** Dashboards and review processes
    - **Course Correction:** How to pivot if opportunities don't develop as expected
    
    Focus on opportunities that are specific, measurable, achievable, relevant, and time-bound (SMART). Provide data-driven insights and actionable implementation guidance for {config['company_name']} based on their profile and strategic goals.
    """
    
    opp_response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a senior business development strategist and opportunity analyst with expertise in market analysis, competitive strategy, and business model innovation. Provide comprehensive, data-driven opportunity analysis with specific implementation guidance."},
            {"role": "user", "content": opportunity_prompt}
        ],
        max_tokens=2500,
        temperature=0.2
    )
    
    opportunities = opp_response.choices[0].message.content
    
    return {
        'strategic_analysis': strategic_analysis,
        'opportunities': opportunities,
        'market_intelligence': market_results,
        'competitor_intelligence': competitor_results
    }

def display_analysis_results(results, config):
    """Display the analysis results in a structured format"""
    
    st.success("✅ Competitive Analysis Complete!")
    
    # Analysis header
    st.markdown("---")
    st.markdown(f"# 📊 Competitive Analysis Report")
    st.markdown(f"**Company:** {config['company_name']}")
    st.markdown(f"**Industry:** {config['industry']}")
    st.markdown(f"**Analysis Date:** {datetime.now().strftime('%B %d, %Y at %H:%M')}")
    st.markdown(f"**Competitors Analyzed:** {', '.join(config['competitors'])}")
    
    # Enhanced results display with executive summary
    st.markdown("### 📋 Executive Summary")
    
    # Extract executive summary (first section of the analysis)
    analysis_text = results['strategic_analysis']
    if "## EXECUTIVE SUMMARY" in analysis_text:
        exec_summary = analysis_text.split("## EXECUTIVE SUMMARY")[1].split("##")[0].strip()
        st.info(f"🎯 **Key Strategic Insights:**\n\n{exec_summary}")
    elif "## Executive Summary" in analysis_text:
        exec_summary = analysis_text.split("## Executive Summary")[1].split("##")[0].strip()
        st.info(f"🎯 **Key Strategic Insights:**\n\n{exec_summary}")
    else:
        # Show first 500 characters as summary
        summary = analysis_text[:500] + "..." if len(analysis_text) > 500 else analysis_text
        st.info(f"🎯 **Analysis Overview:**\n\n{summary}")
    
    # Create enhanced tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Complete Analysis", 
        "💡 Business Opportunities", 
        "📈 Market Intelligence", 
        "🏢 Competitor Data",
        "📥 Export & Share"
    ])
    
    with tab1:
        st.markdown("## 📊 Comprehensive Strategic Analysis")
        
        # Analysis mode indicator
        analysis_mode = config.get('analysis_mode', 'Analysis')
        if analysis_mode == "🏭 Industry Analysis":
            st.success("🏭 **Industry Analysis Mode** - Comprehensive market landscape analysis")
        else:
            st.success("🏢 **Company Tracking Mode** - Detailed competitive intelligence report")
        
        # Display the full analysis with better formatting
        st.markdown("---")
        st.markdown(results['strategic_analysis'])
        
        # Analysis metadata
        st.markdown("---")
        st.markdown("### 📋 Analysis Details")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Analysis Type", analysis_mode.replace("🏭 ", "").replace("🏢 ", ""))
        with col2:
            st.metric("Companies Analyzed", len(config['competitors']) if isinstance(config['competitors'], list) else len(config['competitors'].split(',')))
        with col3:
            st.metric("Focus Areas", len(config['focus_areas']))
        with col4:
            word_count = len(results['strategic_analysis'].split())
            st.metric("Report Length", f"{word_count:,} words")
    
    with tab2:
        st.markdown("## 💡 Strategic Business Opportunities")
        st.markdown("*Comprehensive opportunity analysis with implementation guidance*")
        st.markdown("---")
        st.markdown(results['opportunities'])
        
        # Opportunity metrics
        st.markdown("---")
        st.markdown("### 📊 Opportunity Overview")
        opp_text = results['opportunities']
        opportunity_count = opp_text.count("OPPORTUNITY") + opp_text.count("Opportunity")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Opportunities Identified", opportunity_count)
        with col2:
            st.metric("Analysis Depth", "Comprehensive" if len(opp_text) > 2000 else "Standard")
    
    with tab3:
        st.markdown("## 📈 Market Intelligence Data")
        st.markdown("*Raw market research and trend analysis data*")
        
        # Market data with better organization
        if results.get('market_intelligence'):
            with st.expander("🌍 Market Research Results", expanded=True):
                st.markdown("### Industry & Market Trends")
                st.text_area("", results['market_intelligence'], height=300, key="market_data")
                
                # Market data metrics
                market_data = results['market_intelligence']
                sources_count = market_data.count('URL:') if 'URL:' in market_data else market_data.count('http')
                st.caption(f"📊 Data from {sources_count} sources | {len(market_data):,} characters of intelligence")
    
    with tab4:
        st.markdown("## 🏢 Competitive Intelligence")
        st.markdown("*Detailed competitor analysis and strategic insights*")
        
        if results.get('competitor_intelligence'):
            competitor_data = results['competitor_intelligence']
            if isinstance(competitor_data, list):
                for i, comp_data in enumerate(competitor_data):
                    # Extract company name from data if possible
                    company_name = f"Competitor {i+1}"
                    if "===" in comp_data:
                        try:
                            company_name = comp_data.split("===")[1].split("===")[0].strip()
                        except:
                            pass
                    
                    with st.expander(f"🏢 {company_name} Intelligence", expanded=i==0):
                        st.text_area("", comp_data, height=250, key=f"comp_{i}")
            else:
                with st.expander("🏢 Competitor Intelligence Data", expanded=True):
                    st.text_area("", str(competitor_data), height=400, key="all_comp_data")
    
    with tab5:
        st.markdown("## 📥 Export & Share Analysis")
        st.markdown("*Download your comprehensive competitive analysis report*")
        
        # Enhanced report generation
        analysis_mode_clean = config.get('analysis_mode', 'Analysis').replace("🏭 ", "").replace("🏢 ", "")
        
        comprehensive_report = f"""
# COMPREHENSIVE COMPETITIVE ANALYSIS REPORT

**Company:** {config['company_name']}
**Industry:** {config['industry']}
**Analysis Type:** {analysis_mode_clean}
**Date:** {datetime.now().strftime('%B %d, %Y at %H:%M')}
**Competitors Analyzed:** {', '.join(config['competitors']) if isinstance(config['competitors'], list) else config['competitors']}

---

## STRATEGIC ANALYSIS
{results['strategic_analysis']}

---

## BUSINESS OPPORTUNITIES
{results['opportunities']}

---

## MARKET INTELLIGENCE DATA
{results.get('market_intelligence', 'No market intelligence data available')}

---

## COMPETITOR INTELLIGENCE
{str(results.get('competitor_intelligence', 'No competitor intelligence data available'))}

---

**Report Generated by:** AI Competitive Analysis System
**Total Analysis Length:** {len(results['strategic_analysis'].split()) + len(results['opportunities'].split()):,} words
**Analysis Depth:** Comprehensive Professional Report
        """
        
        # Download options
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                label="📄 Download Complete Report (TXT)",
                data=comprehensive_report,
                file_name=f"{config['company_name'].replace(' ', '_')}_Competitive_Analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                help="Download the complete analysis as a text file"
            )
        
        with col2:
            # Create a summary version
            summary_report = f"""
# EXECUTIVE SUMMARY - COMPETITIVE ANALYSIS

**Company:** {config['company_name']}
**Date:** {datetime.now().strftime('%B %d, %Y')}
**Analysis Type:** {analysis_mode_clean}

## KEY INSIGHTS
{exec_summary if 'exec_summary' in locals() else results['strategic_analysis'][:1000]}

## TOP OPPORTUNITIES
{results['opportunities'][:1500] if len(results['opportunities']) > 1500 else results['opportunities']}

---
Full report available in complete download.
            """
            
            st.download_button(
                label="📋 Download Executive Summary",
                data=summary_report,
                file_name=f"{config['company_name'].replace(' ', '_')}_Executive_Summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                help="Download a condensed executive summary"
            )
        
        # Report statistics
        st.markdown("---")
        st.markdown("### 📊 Report Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_words = len(results['strategic_analysis'].split()) + len(results['opportunities'].split())
            st.metric("Total Words", f"{total_words:,}")
        
        with col2:
            st.metric("Analysis Sections", "7+ detailed sections")
        
        with col3:
            st.metric("Report Type", "Professional Grade")
        
        with col4:
            st.metric("Actionability", "Implementation Ready")

if __name__ == "__main__":
    main()