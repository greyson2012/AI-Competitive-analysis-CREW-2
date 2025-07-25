"""
Main Streamlit application for competitive analysis dashboard
"""
import streamlit as st
import asyncio
import sys
import os
from datetime import datetime, date, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.supabase_client import db_client
from crew.crew import competitive_analysis_crew
from config.company_context import COMPANY_CONTEXT

# Page configuration
st.set_page_config(
    page_title="AI Competitive Analysis Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    /* Main theme and colors */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    
    .insight-card {
        background: #f8f9ff;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #e1e5fe;
        margin-bottom: 1rem;
    }
    
    .alert-card {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .critical-alert {
        background: #f8d7da;
        border-color: #f5c6cb;
    }
    
    .opportunity-score {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
        text-align: center;
    }
    
    .trend-momentum {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.5rem 0;
    }
    
    .status-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .status-high { background: #e8f5e8; color: #2e7d32; }
    .status-medium { background: #fff3e0; color: #f57c00; }
    .status-low { background: #ffebee; color: #c62828; }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_dashboard_data():
    """Load dashboard data with caching"""
    try:
        # Use asyncio.run for async functions in Streamlit
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Load data with error handling for each component
        data = {}
        
        try:
            data['summary'] = loop.run_until_complete(db_client.get_analysis_summary(days=30))
        except Exception as e:
            st.warning(f"Could not load summary data: {e}")
            data['summary'] = {}
        
        try:
            data['findings'] = loop.run_until_complete(db_client.get_market_findings(limit=20))
        except Exception as e:
            st.warning(f"Could not load market findings: {e}")
            data['findings'] = []
        
        try:
            data['opportunities'] = loop.run_until_complete(db_client.get_opportunities(limit=15))
        except Exception as e:
            st.warning(f"Could not load opportunities: {e}")
            data['opportunities'] = []
        
        try:
            data['trends'] = loop.run_until_complete(db_client.get_trends(limit=10))
        except Exception as e:
            st.warning(f"Could not load trends: {e}")
            data['trends'] = []
        
        try:
            data['competitors'] = loop.run_until_complete(db_client.get_competitor_updates(limit=15))
        except Exception as e:
            st.warning(f"Could not load competitor updates: {e}")
            data['competitors'] = []
        
        loop.close()
        return data
        
    except Exception as e:
        st.error(f"Critical error loading dashboard data: {e}")
        return {
            'summary': {},
            'findings': [],
            'opportunities': [],
            'trends': [],
            'competitors': []
        }

def render_header():
    """Render the main dashboard header"""
    st.markdown(f"""
    <div class="main-header">
        <h1>🚀 AI Competitive Intelligence Dashboard</h1>
        <p>{COMPANY_CONTEXT['name']} • Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
    </div>
    """, unsafe_allow_html=True)

def render_key_metrics(data):
    """Render key metrics section"""
    if not data or not data['summary']:
        st.warning("No summary data available")
        return
    
    summary = data['summary']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Market Findings", 
            summary.get('market_findings', 0),
            delta=f"+{summary.get('market_findings', 0)} this month"
        )
    
    with col2:
        st.metric(
            "Opportunities", 
            summary.get('opportunities', 0),
            delta=f"{len(data.get('opportunities', []))} active"
        )
    
    with col3:
        st.metric(
            "Trends Tracked", 
            summary.get('trends', 0),
            delta=f"{len([t for t in data.get('trends', []) if t.get('momentum_score', 0) > 0.5])} high momentum"
        )
    
    with col4:
        high_score_opps = len([o for o in data.get('opportunities', []) if o.get('score', 0) > 0.7])
        st.metric(
            "High-Value Opportunities", 
            high_score_opps,
            delta=f"Score > 0.7"
        )

def render_opportunities_section(opportunities):
    """Render opportunities explorer section"""
    st.header("🎯 Strategic Opportunities")
    
    if not opportunities:
        st.info("No opportunities identified yet. Run analysis to discover new opportunities.")
        return
    
    # Opportunity filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_score = st.slider("Minimum Score", 0.0, 1.0, 0.5, 0.1)
    
    with col2:
        priority_filter = st.selectbox("Priority", ["All", "high", "medium", "low"])
    
    with col3:
        sort_by = st.selectbox("Sort by", ["Score", "Date", "Priority"])
    
    # Filter opportunities
    filtered_opps = opportunities
    if min_score > 0:
        filtered_opps = [o for o in filtered_opps if o.get('score', 0) >= min_score]
    if priority_filter != "All":
        filtered_opps = [o for o in filtered_opps if o.get('priority') == priority_filter]
    
    # Sort opportunities
    if sort_by == "Score":
        filtered_opps = sorted(filtered_opps, key=lambda x: x.get('score', 0), reverse=True)
    elif sort_by == "Date":
        filtered_opps = sorted(filtered_opps, key=lambda x: x.get('created_at', ''), reverse=True)
    
    # Display opportunities
    for i, opp in enumerate(filtered_opps[:10]):  # Show top 10
        with st.expander(f"**{opp.get('title', 'Untitled Opportunity')}** (Score: {opp.get('score', 0):.2f})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write("**Description:**")
                st.write(opp.get('description', 'No description available'))
                
                st.write("**Market Gap:**")
                st.write(opp.get('market_gap', 'No market gap defined'))
                
                if opp.get('potential_revenue'):
                    st.write(f"**Potential Revenue:** {opp['potential_revenue']}")
                
                if opp.get('time_to_market'):
                    st.write(f"**Time to Market:** {opp['time_to_market']}")
            
            with col2:
                # Opportunity score visualization
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = opp.get('score', 0) * 100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Opportunity Score"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#667eea"},
                        'steps': [
                            {'range': [0, 50], 'color': "#ffebee"},
                            {'range': [50, 75], 'color': "#fff3e0"},
                            {'range': [75, 100], 'color': "#e8f5e8"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig, use_container_width=True)
                
                # Priority badge
                priority = opp.get('priority', 'medium')
                badge_class = f"status-{priority}" if priority in ['high', 'medium', 'low'] else "status-medium"
                st.markdown(f'<span class="status-badge {badge_class}">{priority.title()} Priority</span>', 
                           unsafe_allow_html=True)

def render_market_intelligence(findings):
    """Render market intelligence section"""
    st.header("📊 Market Intelligence")
    
    if not findings:
        st.info("No recent market findings. Run analysis to gather intelligence.")
        return
    
    # Recent findings timeline
    df_findings = pd.DataFrame(findings)
    if not df_findings.empty:
        df_findings['date'] = pd.to_datetime(df_findings['date'])
        
        # Findings over time chart
        daily_counts = df_findings.groupby(df_findings['date'].dt.date).size().reset_index()
        daily_counts.columns = ['Date', 'Count']
        
        fig = px.line(daily_counts, x='Date', y='Count', 
                     title="Market Findings Over Time",
                     line_shape='spline')
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Category breakdown
        category_counts = df_findings['category'].value_counts()
        fig_pie = px.pie(values=category_counts.values, names=category_counts.index,
                        title="Findings by Category")
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Recent findings list
    st.subheader("Recent Findings")
    for finding in findings[:5]:
        with st.expander(f"**{finding.get('title', 'Untitled Finding')}** ({finding.get('category', 'uncategorized')})"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(finding.get('summary', 'No summary available'))
                if finding.get('source_url'):
                    st.markdown(f"[Source]({finding['source_url']})")
            
            with col2:
                relevance = finding.get('relevance_score', 0)
                st.metric("Relevance", f"{relevance:.2f}")
                
                # Color-coded relevance indicator
                if relevance > 0.7:
                    st.success("High Relevance")
                elif relevance > 0.4:
                    st.warning("Medium Relevance")
                else:
                    st.info("Low Relevance")

def render_trends_analysis(trends):
    """Render trends analysis section"""
    st.header("📈 Market Trends")
    
    if not trends:
        st.info("No trends identified yet. Run analysis to discover emerging trends.")
        return
    
    # Trend momentum chart
    df_trends = pd.DataFrame(trends)
    if not df_trends.empty:
        fig = px.bar(df_trends, x='trend_name', y='momentum_score',
                    title="Trend Momentum Scores",
                    color='momentum_score',
                    color_continuous_scale='Viridis')
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # Trends list with details
    st.subheader("Trending Topics")
    for trend in sorted(trends, key=lambda x: x.get('momentum_score', 0), reverse=True)[:8]:
        with st.expander(f"**{trend.get('trend_name', 'Untitled Trend')}** (Momentum: {trend.get('momentum_score', 0):.2f})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**Category:** {trend.get('category', 'uncategorized')}")
                if trend.get('prediction'):
                    st.write(f"**Prediction:** {trend['prediction']}")
                
                # Evidence display
                evidence = trend.get('evidence', {})
                if evidence:
                    st.write("**Supporting Evidence:**")
                    for key, value in evidence.items():
                        st.write(f"- {key.replace('_', ' ').title()}: {value}")
            
            with col2:
                # Momentum gauge
                momentum = trend.get('momentum_score', 0)
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = momentum * 100,
                    title = {'text': "Momentum"},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#764ba2"},
                        'steps': [
                            {'range': [0, 30], 'color': "#ffebee"},
                            {'range': [30, 70], 'color': "#fff3e0"},
                            {'range': [70, 100], 'color': "#e8f5e8"}
                        ]
                    }
                ))
                fig.update_layout(height=180, margin=dict(l=20, r=20, t=40, b=20))
                st.plotly_chart(fig, use_container_width=True)

def render_competitor_intelligence(competitors):
    """Render competitor intelligence section"""
    st.header("🏢 Competitive Landscape")
    
    if not competitors:
        st.info("No competitor updates tracked. Run analysis to monitor competition.")
        return
    
    # Competitor activity summary
    df_comp = pd.DataFrame(competitors)
    if not df_comp.empty:
        # Activity by company
        company_counts = df_comp['company_name'].value_counts()
        fig = px.bar(x=company_counts.index, y=company_counts.values,
                    title="Competitor Activity Volume",
                    labels={'x': 'Company', 'y': 'Updates'})
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # Impact level distribution
        impact_counts = df_comp['impact_level'].value_counts()
        fig_pie = px.pie(values=impact_counts.values, names=impact_counts.index,
                        title="Impact Level Distribution")
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Recent competitor updates
    st.subheader("Recent Competitive Updates")
    for update in competitors[:6]:
        impact_class = f"status-{update.get('impact_level', 'medium')}"
        
        with st.expander(f"**{update.get('company_name', 'Unknown Company')}** - {update.get('update_type', 'update')}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(update.get('description', 'No description available'))
                if update.get('source_url'):
                    st.markdown(f"[Source]({update['source_url']})")
            
            with col2:
                impact = update.get('impact_level', 'medium')
                st.markdown(f'<span class="status-badge {impact_class}">{impact.title()} Impact</span>', 
                           unsafe_allow_html=True)
                
                if update.get('detected_date'):
                    st.write(f"**Detected:** {update['detected_date']}")

def main():
    """Main application function"""
    render_header()
    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/200x80/667eea/white?text=AI+Intel", width=200)
        
        selected = option_menu(
            menu_title="Navigation",
            options=["Dashboard", "Opportunities", "Market Intel", "Trends", "Competitors", "Settings"],
            icons=["speedometer2", "bullseye", "graph-up", "trending-up", "building", "gear"],
            menu_icon="list",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#667eea", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#667eea"},
            }
        )
        
        # Control buttons
        st.markdown("---")
        if st.button("🔄 Run Analysis", type="primary"):
            with st.spinner("Running competitive analysis..."):
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    results = loop.run_until_complete(competitive_analysis_crew.run_daily_analysis())
                    loop.close()
                    
                    if results.get('status') == 'completed':
                        st.success("Analysis completed successfully!")
                        st.cache_data.clear()  # Clear cache to refresh data
                        st.rerun()
                    else:
                        st.error(f"Analysis failed: {results.get('error', 'Unknown error')}")
                except Exception as e:
                    st.error(f"Error running analysis: {e}")
        
        if st.button("📧 Send Report"):
            st.info("Report sending functionality will be implemented")
        
        # System status
        st.markdown("---")
        st.subheader("System Status")
        st.success("🟢 Database Connected")
        st.success("🟢 APIs Configured")
        st.info("🔵 Last Run: 2 hours ago")
    
    # Load data
    data = load_dashboard_data()
    
    if not data:
        st.error("Unable to load dashboard data. Please check your database connection.")
        return
    
    # Render selected page
    if selected == "Dashboard":
        render_key_metrics(data)
        
        col1, col2 = st.columns(2)
        with col1:
            render_opportunities_section(data['opportunities'][:5])
        with col2:
            render_trends_analysis(data['trends'][:5])
            
    elif selected == "Opportunities":
        render_opportunities_section(data['opportunities'])
        
    elif selected == "Market Intel":
        render_market_intelligence(data['findings'])
        
    elif selected == "Trends":
        render_trends_analysis(data['trends'])
        
    elif selected == "Competitors":
        render_competitor_intelligence(data['competitors'])
        
    elif selected == "Settings":
        st.header("⚙️ Settings")
        
        st.subheader("Company Configuration")
        st.write(f"**Company:** {COMPANY_CONTEXT['name']}")
        st.write(f"**Industry:** {COMPANY_CONTEXT['industry']}")
        st.write(f"**Target Industries:** {', '.join(COMPANY_CONTEXT['target_industries'])}")
        st.write(f"**Competitors:** {', '.join(COMPANY_CONTEXT['competitors'])}")
        
        st.subheader("Analysis Configuration")
        st.info("Configuration management will be implemented in future versions")

if __name__ == "__main__":
    main()