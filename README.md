# 🚀 AI Competitive Analysis Agent

A sophisticated, automated competitive intelligence system built with CrewAI that monitors the AI industry, tracks competitors, identifies trends, and delivers strategic insights through a beautiful dashboard and email reports.

## ✨ Features

### 🤖 Intelligent AI Agents
- **Market Intelligence Agent**: Scans industry news, research, and developments using Serper API
- **Competitor Intelligence Agent**: Monitors competitor activities and strategic moves
- **Trend Analysis Agent**: Identifies patterns and forecasts market directions
- **Strategic Synthesis Agent**: Generates actionable business recommendations

### 📊 Beautiful Dashboard
- Real-time competitive intelligence visualization
- Interactive opportunity scoring and filtering
- Market trend analysis with momentum tracking
- Competitive landscape monitoring
- Executive-level insights and recommendations

### 📧 Automated Reporting
- Daily HTML email reports with key insights
- Critical alert notifications for urgent developments
- Weekly comprehensive summaries
- Professional email templates with embedded visualizations

### 🗄️ Comprehensive Data Management
- Supabase database for historical analysis
- Structured data models for findings, opportunities, and trends
- Advanced pattern recognition using historical data
- Performance tracking and analytics

## 🛠️ Technology Stack

- **CrewAI**: Multi-agent orchestration framework
- **OpenAI GPT-4**: Advanced reasoning and analysis
- **Serper API**: Intelligent web search capabilities
- **Supabase**: PostgreSQL database with real-time features
- **Streamlit**: Beautiful, interactive dashboard
- **Gmail SMTP**: Professional email notifications
- **Plotly**: Interactive data visualizations
- **Python 3.11+**: Modern Python features and performance

## 🚀 Quick Start

### Prerequisites

1. **Python 3.11+** installed
2. **API Keys** (see setup section)
3. **Supabase Project** configured
4. **Gmail App Password** set up

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd competitive-analysis-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

4. **Set up Supabase database**
   ```sql
   -- Run the schema from src/database/models.py in your Supabase SQL editor
   ```

5. **Run the dashboard**
   ```bash
   streamlit run src/ui/app.py
   ```

### Required API Keys

1. **OpenAI API Key**
   - Go to [OpenAI API](https://platform.openai.com/api-keys)
   - Create new API key
   - Add to `.env` as `OPENAI_API_KEY`

2. **Serper API Key**
   - Go to [Serper.dev](https://serper.dev)
   - Sign up and get API key
   - Add to `.env` as `SERPER_API_KEY`

3. **Supabase Configuration**
   - Create project at [Supabase](https://supabase.com)
   - Get URL and anon key from Settings > API
   - Add to `.env` as `SUPABASE_URL` and `SUPABASE_KEY`

4. **Gmail App Password**
   - Enable 2FA on your Gmail account
   - Generate App Password in Google Account settings
   - Add to `.env` as `GMAIL_APP_PASSWORD`

## 📖 Usage

### Dashboard Interface

```bash
# Start the beautiful Streamlit dashboard
streamlit run src/ui/app.py
```

The dashboard provides:
- **Executive Overview**: Key metrics and insights
- **Opportunities Explorer**: Interactive opportunity analysis
- **Market Intelligence**: Latest industry developments
- **Trend Analysis**: Emerging trends with momentum scores
- **Competitive Landscape**: Competitor monitoring and alerts

### Command Line Operations

```bash
# Run daily analysis
python src/crew/main.py daily

# Generate weekly summary
python src/crew/main.py weekly

# Quick analysis on specific topic
python src/crew/main.py quick "enterprise AI adoption"
```

### Automated Scheduling

```bash
# Start the scheduler (runs daily at 7 AM)
python src/utils/scheduler.py start

# Test individual components
python src/utils/scheduler.py test-daily
python src/utils/scheduler.py test-weekly
```

## ⚙️ Configuration

### Company Context

Edit `src/config/company_context.py` to customize:

```python
company_context = {
    "name": "Your AI Company",
    "core_competencies": ["AI Solutions", "ML Consulting"],
    "target_industries": ["Healthcare", "Finance"],
    "competitors": ["OpenAI", "Anthropic"],
    # ... more configuration
}
```

### Email Templates

Customize email templates in `src/utils/gmail_client.py`:
- Daily report styling
- Critical alert formatting
- Weekly summary layout

### Analysis Parameters

Adjust analysis focus in `.env`:
```bash
COMPANY_NAME=Your Company Name
TARGET_INDUSTRIES=Healthcare,Finance,E-commerce
COMPETITORS=OpenAI,Anthropic,Google AI
ANALYSIS_TIME=07:00
```

## 📊 Dashboard Features

### Key Metrics Overview
- Market findings count with trend indicators
- Active opportunities with priority distribution
- High-momentum trends tracking
- Competitive threat assessment

### Interactive Opportunities
- Filterable opportunity cards with scoring
- Dynamic priority and timeline visualization
- Implementation complexity assessment
- Revenue potential estimates

### Market Intelligence
- Real-time news and development tracking
- Relevance scoring for business impact
- Category-based trend analysis
- Source attribution and verification

### Competitive Monitoring
- Competitor activity volume tracking
- Impact level assessment
- Strategic response recommendations
- Timeline-based competitor analysis

## 🔒 Security & Privacy

- **API Key Protection**: Environment variables for sensitive data
- **Database Security**: Supabase RLS (Row Level Security) ready
- **Email Security**: Gmail App Passwords for authentication
- **Data Encryption**: HTTPS/TLS for all API communications

## 📈 Performance & Scaling

- **Caching**: Streamlit caching for dashboard performance
- **Async Operations**: Non-blocking database and API calls
- **Rate Limiting**: Built-in API rate limit management
- **Error Handling**: Comprehensive error recovery and logging

## 🧪 Testing

```bash
# Test database connection
python -c "from src.database.supabase_client import db_client; print('DB Connected!')"

# Test Serper search
python -c "from src.tools.serper_search import serper_tool; print(serper_tool.search_ai_news(1))"

# Test email system
python -c "from src.utils.gmail_client import gmail_client; print('Email configured!')"
```

## 📋 Roadmap

### Phase 1 ✅
- Core agent implementation
- Database integration
- Basic dashboard
- Email notifications

### Phase 2 🚧
- Advanced visualizations
- Custom alert rules
- Competitor deep-dive analysis
- API rate optimization

### Phase 3 📅
- Machine learning trend prediction
- Automated response recommendations
- Integration with business tools
- Advanced reporting features

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 💰 Cost Optimization

### Estimated Monthly Costs
- **OpenAI API**: $100-200 (primary cost)
- **Serper API**: $20-50 (search operations)
- **Supabase**: Free tier (sufficient for most use cases)
- **Gmail**: Free (using existing account)
- **Total**: ~$120-250/month

### Cost Reduction Tips
- Use GPT-3.5-turbo for simpler tasks
- Implement intelligent caching
- Batch API requests when possible
- Monitor usage with built-in analytics

## 📞 Support

For questions, issues, or feature requests:
- Create an issue in this repository
- Check the documentation in `/docs`
- Review the CLAUDE.md file for development context

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Built with ❤️ using CrewAI, OpenAI, and modern Python technologies.**

*Transform your competitive intelligence with AI-powered automation and beautiful visualizations.*