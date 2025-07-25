"""
Supabase client for competitive analysis data management
"""
import os
from typing import Dict, List, Optional, Any
from datetime import datetime, date
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseClient:
    """Handles all database operations for the competitive analysis system"""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            raise ValueError("Supabase URL and KEY must be set in environment variables")
        
        self.client: Client = create_client(self.url, self.key)
    
    # Market Findings Operations
    async def insert_market_finding(self, finding: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a new market finding"""
        try:
            result = self.client.table("market_findings").insert(finding).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error inserting market finding: {e}")
            return None
    
    async def get_market_findings(self, 
                                limit: int = 50,
                                category: Optional[str] = None,
                                start_date: Optional[date] = None) -> List[Dict[str, Any]]:
        """Retrieve market findings with optional filtering"""
        try:
            query = self.client.table("market_findings").select("*")
            
            if category:
                query = query.eq("category", category)
            if start_date:
                query = query.gte("date", start_date.isoformat())
            
            result = query.order("created_at", desc=True).limit(limit).execute()
            return result.data or []
        except Exception as e:
            print(f"Error retrieving market findings: {e}")
            return []
    
    # Competitor Updates Operations
    async def insert_competitor_update(self, update: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a new competitor update"""
        try:
            result = self.client.table("competitor_updates").insert(update).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error inserting competitor update: {e}")
            return None
    
    async def get_competitor_updates(self, 
                                   company_name: Optional[str] = None,
                                   limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve competitor updates"""
        try:
            query = self.client.table("competitor_updates").select("*")
            
            if company_name:
                query = query.eq("company_name", company_name)
            
            result = query.order("created_at", desc=True).limit(limit).execute()
            return result.data or []
        except Exception as e:
            print(f"Error retrieving competitor updates: {e}")
            return []
    
    # Opportunities Operations
    async def insert_opportunity(self, opportunity: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a new market opportunity"""
        try:
            result = self.client.table("opportunities").insert(opportunity).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error inserting opportunity: {e}")
            return None
    
    async def get_opportunities(self, 
                              min_score: Optional[float] = None,
                              limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve opportunities with optional filtering"""
        try:
            query = self.client.table("opportunities").select("*")
            
            if min_score:
                query = query.gte("score", min_score)
            
            result = query.order("score", desc=True).limit(limit).execute()
            return result.data or []
        except Exception as e:
            print(f"Error retrieving opportunities: {e}")
            return []
    
    # Trends Operations
    async def insert_trend(self, trend: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a new trend"""
        try:
            result = self.client.table("trends").insert(trend).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error inserting trend: {e}")
            return None
    
    async def get_trends(self, 
                        category: Optional[str] = None,
                        min_momentum: Optional[float] = None,
                        limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieve trends with optional filtering"""
        try:
            query = self.client.table("trends").select("*")
            
            if category:
                query = query.eq("category", category)
            if min_momentum:
                query = query.gte("momentum_score", min_momentum)
            
            result = query.order("momentum_score", desc=True).limit(limit).execute()
            return result.data or []
        except Exception as e:
            print(f"Error retrieving trends: {e}")
            return []
    
    # Analysis Runs Operations
    async def insert_analysis_run(self, run_data: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a new analysis run record"""
        try:
            result = self.client.table("analysis_runs").insert(run_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error inserting analysis run: {e}")
            return None
    
    async def get_analysis_runs(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Retrieve recent analysis runs"""
        try:
            result = self.client.table("analysis_runs").select("*").order("created_at", desc=True).limit(limit).execute()
            return result.data or []
        except Exception as e:
            print(f"Error retrieving analysis runs: {e}")
            return []
    
    # Utility Operations
    async def check_connection(self) -> bool:
        """Test database connection"""
        try:
            result = self.client.table("market_findings").select("count", count="exact").limit(1).execute()
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False
    
    async def get_latest_findings_by_category(self) -> Dict[str, int]:
        """Get count of findings by category from last 7 days"""
        try:
            from datetime import timedelta
            start_date = (datetime.now() - timedelta(days=7)).date()
            
            findings = await self.get_market_findings(start_date=start_date, limit=1000)
            category_counts = {}
            
            for finding in findings:
                category = finding.get('category', 'unknown')
                category_counts[category] = category_counts.get(category, 0) + 1
            
            return category_counts
        except Exception as e:
            print(f"Error getting category breakdown: {e}")
            return {}
    
    async def get_top_opportunities(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top-scoring opportunities"""
        try:
            result = self.client.table("opportunities").select("*").order("score", desc=True).limit(limit).execute()
            return result.data or []
        except Exception as e:
            print(f"Error retrieving top opportunities: {e}")
            return []
    
    async def get_high_momentum_trends(self, min_momentum: float = 0.7) -> List[Dict[str, Any]]:
        """Get trends with high momentum scores"""
        try:
            result = self.client.table("trends").select("*").gte("momentum_score", min_momentum).order("momentum_score", desc=True).execute()
            return result.data or []
        except Exception as e:
            print(f"Error retrieving high momentum trends: {e}")
            return []
    
    async def get_critical_competitor_updates(self) -> List[Dict[str, Any]]:
        """Get competitor updates with high or critical impact"""
        try:
            result = self.client.table("competitor_updates").select("*").in_("impact_level", ["high", "critical"]).order("created_at", desc=True).limit(20).execute()
            return result.data or []
        except Exception as e:
            print(f"Error retrieving critical updates: {e}")
            return []
    
    # Analytics Operations
    async def get_analysis_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive analysis summary for the last N days"""
        try:
            from datetime import timedelta
            start_date = (datetime.now() - timedelta(days=days)).date()
            
            # Get counts for each table
            findings = await self.get_market_findings(start_date=start_date, limit=1000)
            opportunities = await self.get_opportunities(limit=1000)
            trends = await self.get_trends(limit=1000)
            competitor_updates = await self.get_competitor_updates(limit=1000)
            
            # Calculate additional metrics
            high_value_opportunities = len([o for o in opportunities if o.get('score', 0) > 0.7])
            high_momentum_trends = len([t for t in trends if t.get('momentum_score', 0) > 0.7])
            critical_updates = len([u for u in competitor_updates if u.get('impact_level') in ['high', 'critical']])
            
            return {
                "period_days": days,
                "start_date": start_date.isoformat(),
                "market_findings": len(findings),
                "opportunities": len(opportunities),
                "trends": len(trends),
                "competitor_updates": len(competitor_updates),
                "high_value_opportunities": high_value_opportunities,
                "high_momentum_trends": high_momentum_trends,
                "critical_competitor_updates": critical_updates,
                "category_breakdown": await self.get_latest_findings_by_category(),
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error getting analysis summary: {e}")
            return {
                "period_days": days,
                "error": str(e),
                "last_updated": datetime.now().isoformat()
            }
    
    async def cleanup_old_data(self, days_to_keep: int = 90) -> Dict[str, int]:
        """Clean up data older than specified days"""
        try:
            from datetime import timedelta
            cutoff_date = (datetime.now() - timedelta(days=days_to_keep)).date()
            
            # Delete old records from each table
            findings_deleted = self.client.table("market_findings").delete().lt("date", cutoff_date.isoformat()).execute()
            updates_deleted = self.client.table("competitor_updates").delete().lt("detected_date", cutoff_date.isoformat()).execute()
            runs_deleted = self.client.table("analysis_runs").delete().lt("run_date", cutoff_date.isoformat()).execute()
            
            return {
                "findings_deleted": len(findings_deleted.data) if findings_deleted.data else 0,
                "updates_deleted": len(updates_deleted.data) if updates_deleted.data else 0,
                "runs_deleted": len(runs_deleted.data) if runs_deleted.data else 0,
                "cutoff_date": cutoff_date.isoformat()
            }
        except Exception as e:
            print(f"Error cleaning up old data: {e}")
            return {"error": str(e)}

# Initialize global client instance
db_client = SupabaseClient()