"""
Scheduling system for automated competitive analysis
"""
import schedule
import time
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv
import logging

# Add src to path for imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crew.crew import competitive_analysis_crew

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('competitive_analysis.log'),
        logging.StreamHandler()
    ]
)

class CompetitiveAnalysisScheduler:
    """Scheduler for automated competitive analysis tasks"""
    
    def __init__(self):
        load_dotenv()
        self.analysis_time = os.getenv("ANALYSIS_TIME", "07:00")
        self.timezone = os.getenv("TIMEZONE", "UTC")
        self.running = False
        
        logging.info(f"Scheduler initialized - Daily analysis at {self.analysis_time} {self.timezone}")
    
    def daily_analysis_job(self):
        """Job function for daily analysis"""
        logging.info("🚀 Starting scheduled daily analysis")
        
        try:
            # Create new event loop for async execution
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run the analysis
            results = loop.run_until_complete(competitive_analysis_crew.run_daily_analysis())
            
            # Log results
            if results.get('status') == 'completed':
                summary = results.get('summary', {})
                logging.info(f"✅ Daily analysis completed successfully:")
                logging.info(f"   - Market findings: {summary.get('findings_count', 0)}")
                logging.info(f"   - Opportunities: {summary.get('opportunities_count', 0)}")
                logging.info(f"   - Trends: {summary.get('trends_identified', 0)}")
                logging.info(f"   - Execution time: {results.get('execution_time', 0):.1f}s")
            else:
                logging.error(f"❌ Daily analysis failed: {results.get('error', 'Unknown error')}")
            
            loop.close()
            
        except Exception as e:
            logging.error(f"❌ Error in scheduled daily analysis: {e}")
    
    def weekly_summary_job(self):
        """Job function for weekly summary"""
        logging.info("📊 Starting scheduled weekly summary")
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            results = loop.run_until_complete(competitive_analysis_crew.run_weekly_summary())
            
            if results.get('error'):
                logging.error(f"❌ Weekly summary failed: {results['error']}")
            else:
                logging.info("✅ Weekly summary completed and sent")
            
            loop.close()
            
        except Exception as e:
            logging.error(f"❌ Error in scheduled weekly summary: {e}")
    
    def setup_schedule(self):
        """Set up the scheduled jobs"""
        # Daily analysis at specified time
        schedule.every().day.at(self.analysis_time).do(self.daily_analysis_job)
        
        # Weekly summary on Mondays at 8 AM
        schedule.every().monday.at("08:00").do(self.weekly_summary_job)
        
        # Health check every 6 hours
        schedule.every(6).hours.do(self.health_check)
        
        logging.info("✅ Schedule configured:")
        logging.info(f"   - Daily analysis: Every day at {self.analysis_time}")
        logging.info(f"   - Weekly summary: Mondays at 08:00")
        logging.info(f"   - Health check: Every 6 hours")
    
    def health_check(self):
        """Perform system health check"""
        try:
            from database.supabase_client import db_client
            
            # Test database connection
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            summary = loop.run_until_complete(db_client.get_analysis_summary(days=1))
            loop.close()
            
            logging.info("✅ Health check passed - Database connection OK")
            
        except Exception as e:
            logging.error(f"❌ Health check failed: {e}")
    
    def run(self):
        """Start the scheduler"""
        self.setup_schedule()
        self.running = True
        
        logging.info("🚀 Competitive Analysis Scheduler started")
        logging.info("Press Ctrl+C to stop the scheduler")
        
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            logging.info("🛑 Scheduler stopped by user")
            self.running = False
        except Exception as e:
            logging.error(f"❌ Scheduler error: {e}")
            self.running = False
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        logging.info("🛑 Scheduler stopped")
    
    def run_once(self, job_type: str = "daily"):
        """Run a single job for testing"""
        logging.info(f"🧪 Running single {job_type} job for testing")
        
        if job_type == "daily":
            self.daily_analysis_job()
        elif job_type == "weekly":
            self.weekly_summary_job()
        elif job_type == "health":
            self.health_check()
        else:
            logging.error(f"❌ Unknown job type: {job_type}")

def main():
    """Main function for running the scheduler"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Competitive Analysis Scheduler")
    parser.add_argument(
        "command", 
        choices=["start", "test-daily", "test-weekly", "test-health"],
        help="Command to execute"
    )
    
    args = parser.parse_args()
    
    scheduler = CompetitiveAnalysisScheduler()
    
    if args.command == "start":
        scheduler.run()
    elif args.command == "test-daily":
        scheduler.run_once("daily")
    elif args.command == "test-weekly":
        scheduler.run_once("weekly")
    elif args.command == "test-health":
        scheduler.run_once("health")

if __name__ == "__main__":
    main()