"""
Serper API integration for intelligent web search
"""
import os
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

class SerperSearchInput(BaseModel):
    """Input schema for Serper search tool"""
    query: str = Field(..., description="Search query to execute")
    num_results: int = Field(default=10, description="Number of results to return (max 100)")
    time_range: str = Field(default="", description="Time range: d (day), w (week), m (month), y (year)")
    search_type: str = Field(default="search", description="Type: search, news, images, videos")

class SerperSearchTool(BaseTool):
    """Advanced web search tool using Serper API"""
    
    name: str = "serper_search"
    description: str = """
    Perform intelligent web searches using Google Search API.
    Useful for finding recent news, research papers, company updates, and market intelligence.
    Can search for specific time ranges and different content types.
    """
    args_schema: type = SerperSearchInput

    def __init__(self):
        super().__init__()
        
    def _get_api_key(self):
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            raise ValueError("SERPER_API_KEY environment variable is required")
        return api_key

    def _run(self, query: str, num_results: int = 10, time_range: str = "", search_type: str = "search") -> str:
        """Execute search and return formatted results"""
        try:
            api_key = self._get_api_key()
            base_url = "https://google.serper.dev"
            headers = {
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            }
            
            # Prepare search payload
            payload = {
                "q": query,
                "num": min(num_results, 100)  # API limit
            }
            
            # Add time range if specified
            if time_range:
                payload["tbs"] = f"qdr:{time_range}"
            
            # Choose endpoint based on search type
            endpoint = f"{base_url}/{search_type}"
            
            # Make API request
            response = requests.post(endpoint, headers=headers, json=payload)
            response.raise_for_status()
            
            data = response.json()
            
            # Format results based on search type
            if search_type == "news":
                return self._format_news_results(data, query)
            else:
                return self._format_search_results(data, query)
                
        except requests.exceptions.RequestException as e:
            return f"Search error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

    def _format_search_results(self, data: Dict[str, Any], query: str) -> str:
        """Format regular search results"""
        results = []
        results.append(f"Search Results for: '{query}'")
        results.append(f"Total Results: {data.get('searchInformation', {}).get('totalResults', 'Unknown')}")
        results.append("=" * 50)
        
        organic_results = data.get("organic", [])
        
        for i, result in enumerate(organic_results, 1):
            title = result.get("title", "No title")
            link = result.get("link", "No link")
            snippet = result.get("snippet", "No description")
            
            results.append(f"\n{i}. {title}")
            results.append(f"   URL: {link}")
            results.append(f"   Description: {snippet}")
            
            # Add additional context if available
            if "sitelinks" in result:
                results.append("   Related links:")
                for sitelink in result["sitelinks"][:3]:  # Limit to 3
                    results.append(f"   - {sitelink.get('title', '')}: {sitelink.get('link', '')}")
        
        return "\n".join(results)

    def _format_news_results(self, data: Dict[str, Any], query: str) -> str:
        """Format news search results"""
        results = []
        results.append(f"News Results for: '{query}'")
        results.append("=" * 50)
        
        news_results = data.get("news", [])
        
        for i, article in enumerate(news_results, 1):
            title = article.get("title", "No title")
            link = article.get("link", "No link")
            snippet = article.get("snippet", "No description")
            date = article.get("date", "No date")
            source = article.get("source", "Unknown source")
            
            results.append(f"\n{i}. {title}")
            results.append(f"   Source: {source}")
            results.append(f"   Date: {date}")
            results.append(f"   URL: {link}")
            results.append(f"   Summary: {snippet}")
        
        return "\n".join(results)

    def search_ai_news(self, days_back: int = 7) -> str:
        """Search for recent AI industry news"""
        time_range = "d" if days_back <= 1 else "w" if days_back <= 7 else "m"
        query = "artificial intelligence AI news technology breakthrough startup funding"
        return self._run(query, num_results=20, time_range=time_range, search_type="news")

    def search_competitor_updates(self, company_name: str, days_back: int = 30) -> str:
        """Search for updates about a specific competitor"""
        time_range = "w" if days_back <= 7 else "m"
        query = f'"{company_name}" AI artificial intelligence update news announcement product launch'
        return self._run(query, num_results=15, time_range=time_range, search_type="news")

    def search_market_trends(self, industry: str = "artificial intelligence") -> str:
        """Search for market trends in specified industry"""
        query = f"{industry} market trends growth forecast analysis report 2024"
        return self._run(query, num_results=15, time_range="m", search_type="search")

    def search_research_papers(self, topic: str) -> str:
        """Search for recent research papers on a topic"""
        query = f'"{topic}" research paper arxiv "machine learning" "artificial intelligence" filetype:pdf'
        return self._run(query, num_results=10, time_range="m", search_type="search")

# Create tool instance
serper_tool = SerperSearchTool()

# Helper functions for common searches
def search_ai_industry_news(days_back: int = 7) -> str:
    """Quick function to search for AI industry news"""
    return serper_tool.search_ai_news(days_back)

def search_company_updates(company: str, days_back: int = 30) -> str:
    """Quick function to search for company updates"""
    return serper_tool.search_competitor_updates(company, days_back)

def search_emerging_technologies() -> str:
    """Search for emerging AI technologies"""
    query = "emerging AI technologies 2024 breakthrough innovation new artificial intelligence"
    return serper_tool._run(query, num_results=15, time_range="m", search_type="news")