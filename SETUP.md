# CrewAI Competitive Analysis System - Setup Guide

## Quick Start

This guide will help you set up and deploy the CrewAI competitive analysis system in under 30 minutes.

## Prerequisites

- Python 3.8+
- Supabase account (free tier available)
- OpenAI API key
- Serper API key (for web search)
- Gmail account (for notifications)

## Step 1: Environment Setup

1. **Clone and Navigate:**
   ```bash
   cd /path/to/your/project
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration:**
   ```bash
   cp .env.example .env
   ```

## Step 2: Database Setup (Supabase)

1. **Create Supabase Project:**
   - Go to [supabase.com](https://supabase.com)
   - Create new project
   - Wait for setup to complete

2. **Get Credentials:**
   - Go to Settings → API
   - Copy the `URL` and `anon` key
   - Add to `.env` file:
     ```
     SUPABASE_URL=https://your-project.supabase.co
     SUPABASE_KEY=your-anon-key-here
     ```

3. **Setup Database Schema:**
   - Go to SQL Editor in Supabase
   - Run the schema from `setup_database.py` or copy from `src/database/models.py`
   - Verify tables are created in Table Editor

## Step 3: API Keys Configuration

### Required APIs:

1. **OpenAI API Key:**
   - Go to [platform.openai.com](https://platform.openai.com)
   - Create API key
   - Add to `.env`: `OPENAI_API_KEY=sk-...`

2. **Serper API Key:**
   - Go to [serper.dev](https://serper.dev)
   - Sign up and get free API key
   - Add to `.env`: `SERPER_API_KEY=your-key`

### Optional APIs:

3. **Gmail App Password:**
   - Enable 2FA on Gmail
   - Generate app password: Google Account → Security → App passwords
   - Add to `.env`: `GMAIL_PASSWORD=your-app-password`

## Step 4: Company Configuration

Edit `.env` file with your company details:

```env
COMPANY_NAME=Your Company Name
TARGET_INDUSTRIES=Financial Services,Healthcare,E-commerce
COMPETITORS=OpenAI,Anthropic,Google AI
NOTIFICATION_RECIPIENTS=you@company.com,team@company.com
```

## Step 5: Test Installation

1. **Test Database Connection:**
   ```bash
   python setup_database.py
   ```

2. **Test Basic Functionality:**
   ```bash
   python src/crew/main.py quick "AI market trends"
   ```

3. **Launch Dashboard:**
   ```bash
   streamlit run src/ui/app.py
   ```

## Step 6: Production Deployment

### Option A: Local Cron Job

1. **Create Cron Job:**
   ```bash
   crontab -e
   ```

2. **Add Daily 7AM Execution:**
   ```bash
   0 7 * * * cd /path/to/project && python src/crew/main.py daily
   ```

### Option B: Cloud Deployment

Choose your platform:

- **Heroku:** Use `Procfile` and scheduler add-on
- **Railway:** Deploy with cron service
- **Google Cloud:** Use Cloud Functions + Cloud Scheduler
- **AWS:** Use Lambda + EventBridge

## Usage Commands

```bash
# Run daily analysis
python src/crew/main.py daily

# Run weekly summary
python src/crew/main.py weekly

# Quick topic analysis
python src/crew/main.py quick "AI regulation trends"

# Launch dashboard
streamlit run src/ui/app.py
```

## Configuration Options

### Analysis Settings

In `.env` file:
```env
ANALYSIS_TIME=07:00          # Daily execution time
TIMEZONE=America/New_York    # Your timezone
DEBUG_MODE=False            # Enable debug logging
LOG_LEVEL=INFO              # Logging level
```

### Notification Settings

```env
ENABLE_CRITICAL_ALERTS=True     # Immediate alerts for critical items
ENABLE_DAILY_REPORTS=True       # Daily email reports
ENABLE_WEEKLY_SUMMARIES=True    # Weekly comprehensive summaries
```

## Troubleshooting

### Common Issues:

1. **Database Connection Failed:**
   - Verify Supabase URL and key
   - Check internet connection
   - Ensure database schema is created

2. **API Rate Limits:**
   - Check API usage quotas
   - Reduce analysis frequency
   - Consider upgrading API plans

3. **Email Notifications Not Working:**
   - Verify Gmail app password
   - Check recipient email format
   - Enable less secure apps if needed

4. **Search Results Empty:**
   - Verify Serper API key
   - Check API quota
   - Test search queries manually

### Getting Help:

- Check logs in console output
- Review error messages carefully
- Ensure all environment variables are set
- Test individual components separately

## Advanced Configuration

### Custom Competitors

Edit `src/config/company_context.py` to add specific competitors:

```python
"competitors": [
    "Your Specific Competitor 1",
    "Your Specific Competitor 2",
    "Industry Leader Name"
]
```

### Custom Analysis Prompts

Modify prompts in `src/config/company_context.py` to focus on your specific needs.

### Dashboard Customization

Edit `src/ui/app.py` to:
- Add custom visualizations
- Modify color schemes
- Add company branding
- Create custom metrics

## Security Best Practices

1. **Environment Variables:**
   - Never commit `.env` file
   - Use strong, unique API keys
   - Rotate keys regularly

2. **Database Security:**
   - Enable RLS (Row Level Security) in Supabase
   - Use environment-specific databases
   - Regular backups

3. **Access Control:**
   - Limit dashboard access
   - Use VPN for production access
   - Monitor API usage

## Maintenance

### Weekly Tasks:
- Review analysis results for accuracy
- Check API usage and costs
- Update competitor lists if needed

### Monthly Tasks:
- Review and tune agent prompts
- Analyze opportunity success rates
- Update company context and objectives

### Quarterly Tasks:
- Evaluate system ROI and effectiveness
- Consider new data sources
- Upgrade components as needed

## Support

For technical issues or questions:
1. Check the troubleshooting section above
2. Review the comprehensive documentation in `/doc/`
3. Test individual components to isolate issues
4. Check API service status pages

## License

This project is configured for your internal business use. Ensure compliance with all API terms of service.