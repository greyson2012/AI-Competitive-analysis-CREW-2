"""
Company database and search utilities
"""
import json
from typing import List, Dict, Any, Optional
from difflib import SequenceMatcher

# Comprehensive company database organized by industry
COMPANY_DATABASE = {
    "Artificial Intelligence": {
        "companies": [
            {"name": "OpenAI", "type": "AI Research", "description": "Creator of GPT models and ChatGPT"},
            {"name": "Anthropic", "type": "AI Safety", "description": "Constitutional AI and Claude assistant"},
            {"name": "Google DeepMind", "type": "AI Research", "description": "Google's AI research division"},
            {"name": "Meta AI", "type": "AI Research", "description": "Facebook's AI research and products"},
            {"name": "Microsoft AI", "type": "Enterprise AI", "description": "Azure AI and Copilot products"},
            {"name": "Cohere", "type": "NLP", "description": "Enterprise NLP and language models"},
            {"name": "Hugging Face", "type": "AI Platform", "description": "Open-source AI model hub"},
            {"name": "Stability AI", "type": "Generative AI", "description": "Stable Diffusion and generative models"},
            {"name": "Character.AI", "type": "Conversational AI", "description": "AI character and chatbot platform"},
            {"name": "Midjourney", "type": "AI Art", "description": "AI image generation platform"},
            {"name": "Perplexity AI", "type": "AI Search", "description": "AI-powered search and answers"},
            {"name": "Jasper AI", "type": "Content AI", "description": "AI writing and content generation"}
        ]
    },
    "SaaS/Cloud Computing": {
        "companies": [
            {"name": "Salesforce", "type": "CRM", "description": "Leading CRM and customer platform"},
            {"name": "Microsoft 365", "type": "Productivity", "description": "Office suite and collaboration tools"},
            {"name": "Google Workspace", "type": "Productivity", "description": "Business productivity and collaboration"},
            {"name": "Zoom", "type": "Communication", "description": "Video conferencing and communications"},
            {"name": "Slack", "type": "Collaboration", "description": "Team messaging and collaboration"},
            {"name": "Notion", "type": "Productivity", "description": "All-in-one workspace and documentation"},
            {"name": "Figma", "type": "Design", "description": "Collaborative design and prototyping"},
            {"name": "Canva", "type": "Design", "description": "Graphic design and visual content"},
            {"name": "Atlassian", "type": "Development", "description": "Jira, Confluence, and developer tools"},
            {"name": "ServiceNow", "type": "Enterprise", "description": "Digital workflow and IT service management"}
        ]
    },
    "FinTech": {
        "companies": [
            {"name": "PayPal", "type": "Payments", "description": "Digital payments and financial services"},
            {"name": "Square", "type": "Payments", "description": "Point-of-sale and payment processing"},
            {"name": "Stripe", "type": "Payments", "description": "Online payment infrastructure"},
            {"name": "Robinhood", "type": "Trading", "description": "Commission-free stock trading"},
            {"name": "Coinbase", "type": "Crypto", "description": "Cryptocurrency exchange and platform"},
            {"name": "Klarna", "type": "BNPL", "description": "Buy now, pay later services"},
            {"name": "Affirm", "type": "BNPL", "description": "Point-of-sale financing"},
            {"name": "Plaid", "type": "Infrastructure", "description": "Financial data connectivity"},
            {"name": "Chime", "type": "Banking", "description": "Digital banking and financial services"},
            {"name": "SoFi", "type": "Financial Services", "description": "Digital personal finance platform"}
        ]
    },
    "E-commerce": {
        "companies": [
            {"name": "Amazon", "type": "Marketplace", "description": "Global e-commerce and cloud platform"},
            {"name": "Shopify", "type": "Platform", "description": "E-commerce platform and tools"},
            {"name": "Alibaba", "type": "Marketplace", "description": "Chinese e-commerce giant"},
            {"name": "eBay", "type": "Marketplace", "description": "Online auction and marketplace"},
            {"name": "Etsy", "type": "Handmade", "description": "Handmade and vintage marketplace"},
            {"name": "Wayfair", "type": "Furniture", "description": "Online furniture and home goods"},
            {"name": "Instacart", "type": "Grocery", "description": "Grocery delivery service"},
            {"name": "DoorDash", "type": "Food Delivery", "description": "Restaurant delivery platform"},
            {"name": "Uber Eats", "type": "Food Delivery", "description": "Food delivery service"},
            {"name": "Walmart", "type": "Retail", "description": "Retail giant with e-commerce"}
        ]
    },
    "HealthTech": {
        "companies": [
            {"name": "Teladoc", "type": "Telemedicine", "description": "Virtual healthcare and medical consultations"},
            {"name": "Veracyte", "type": "Diagnostics", "description": "Genomic diagnostics and precision medicine"},
            {"name": "10x Genomics", "type": "Genomics", "description": "Single-cell and spatial genomics"},
            {"name": "Moderna", "type": "Biotech", "description": "mRNA therapeutics and vaccines"},
            {"name": "Illumina", "type": "Genomics", "description": "DNA sequencing and array technologies"},
            {"name": "Dexcom", "type": "Medical Devices", "description": "Continuous glucose monitoring"},
            {"name": "Peloton", "type": "Digital Health", "description": "Connected fitness and wellness"},
            {"name": "Livongo", "type": "Chronic Care", "description": "Digital health for chronic conditions"},
            {"name": "Oscar Health", "type": "Insurance", "description": "Technology-driven health insurance"},
            {"name": "Ro", "type": "Digital Health", "description": "Direct-to-consumer healthcare"}
        ]
    },
    "Cybersecurity": {
        "companies": [
            {"name": "CrowdStrike", "type": "Endpoint Security", "description": "Cloud-native endpoint protection"},
            {"name": "Palo Alto Networks", "type": "Network Security", "description": "Next-generation firewall and security"},
            {"name": "Okta", "type": "Identity", "description": "Identity and access management"},
            {"name": "Zscaler", "type": "Cloud Security", "description": "Cloud-based security platform"},
            {"name": "SentinelOne", "type": "Endpoint Security", "description": "AI-powered endpoint protection"},
            {"name": "Fortinet", "type": "Network Security", "description": "Network and content security"},
            {"name": "Check Point", "type": "Network Security", "description": "Cybersecurity solutions"},
            {"name": "Splunk", "type": "SIEM", "description": "Security information and event management"},
            {"name": "Rapid7", "type": "Vulnerability Management", "description": "Security analytics and automation"},
            {"name": "Qualys", "type": "Vulnerability Management", "description": "Cloud security and compliance"}
        ]
    }
}

def search_companies(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Search for companies by name or description
    
    Args:
        query: Search query string
        limit: Maximum number of results to return
    
    Returns:
        List of matching companies with similarity scores
    """
    if not query or len(query.strip()) < 2:
        return []
    
    query = query.lower().strip()
    results = []
    
    # Search through all companies in all industries
    for industry, data in COMPANY_DATABASE.items():
        for company in data["companies"]:
            # Calculate similarity scores
            name_similarity = SequenceMatcher(None, query, company["name"].lower()).ratio()
            desc_similarity = SequenceMatcher(None, query, company["description"].lower()).ratio()
            type_similarity = SequenceMatcher(None, query, company["type"].lower()).ratio()
            
            # Check for exact matches or partial matches
            exact_match = query in company["name"].lower()
            partial_match = any(word in company["name"].lower() for word in query.split())
            desc_match = query in company["description"].lower()
            
            # Calculate overall score
            max_similarity = max(name_similarity, desc_similarity, type_similarity)
            
            if exact_match:
                score = 1.0
            elif partial_match:
                score = 0.8 + max_similarity * 0.2
            elif desc_match:
                score = 0.6 + max_similarity * 0.4
            elif max_similarity > 0.3:
                score = max_similarity
            else:
                continue
            
            results.append({
                "name": company["name"],
                "type": company["type"],
                "description": company["description"],
                "industry": industry,
                "score": score
            })
    
    # Sort by score and return top results
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:limit]

def search_industries(query: str) -> List[Dict[str, Any]]:
    """
    Search for industries by name or related terms
    
    Args:
        query: Search query string
    
    Returns:
        List of matching industries with company counts
    """
    if not query or len(query.strip()) < 2:
        return []
    
    query = query.lower().strip()
    results = []
    
    for industry, data in COMPANY_DATABASE.items():
        # Calculate similarity with industry name
        similarity = SequenceMatcher(None, query, industry.lower()).ratio()
        
        # Check for partial matches
        partial_match = any(word in industry.lower() for word in query.split())
        exact_match = query in industry.lower()
        
        if exact_match:
            score = 1.0
        elif partial_match:
            score = 0.8
        elif similarity > 0.3:
            score = similarity
        else:
            continue
        
        results.append({
            "name": industry,
            "company_count": len(data["companies"]),
            "sample_companies": [c["name"] for c in data["companies"][:3]],
            "score": score
        })
    
    # Sort by score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results

def get_industry_companies(industry: str) -> List[Dict[str, Any]]:
    """
    Get all companies in a specific industry
    
    Args:
        industry: Industry name
    
    Returns:
        List of companies in the industry
    """
    if industry in COMPANY_DATABASE:
        return COMPANY_DATABASE[industry]["companies"]
    
    # Try fuzzy matching
    for ind_name, data in COMPANY_DATABASE.items():
        if industry.lower() in ind_name.lower() or ind_name.lower() in industry.lower():
            return data["companies"]
    
    return []

def get_all_industries() -> List[str]:
    """Get list of all available industries"""
    return list(COMPANY_DATABASE.keys())

def get_popular_companies(category: str = None, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Get popular companies, optionally filtered by category
    
    Args:
        category: Optional category to filter by
        limit: Maximum number of companies to return
    
    Returns:
        List of popular companies
    """
    all_companies = []
    
    if category and category in COMPANY_DATABASE:
        industry_data = COMPANY_DATABASE[category]
        for company in industry_data["companies"]:
            company_copy = company.copy()
            company_copy["industry"] = category
            all_companies.append(company_copy)
    else:
        # Get companies from all industries
        for industry, data in COMPANY_DATABASE.items():
            for company in data["companies"]:
                company_copy = company.copy()
                company_copy["industry"] = industry
                all_companies.append(company_copy)
    
    return all_companies[:limit]

def suggest_competitors(company_name: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Suggest competitors for a given company
    
    Args:
        company_name: Name of the company to find competitors for
        limit: Maximum number of competitors to suggest
    
    Returns:
        List of potential competitors
    """
    # Find the company's industry first
    target_industry = None
    target_type = None
    
    for industry, data in COMPANY_DATABASE.items():
        for company in data["companies"]:
            if company_name.lower() in company["name"].lower() or company["name"].lower() in company_name.lower():
                target_industry = industry
                target_type = company["type"]
                break
        if target_industry:
            break
    
    if not target_industry:
        return []
    
    # Get competitors from the same industry, preferring same type
    competitors = []
    industry_companies = COMPANY_DATABASE[target_industry]["companies"]
    
    for company in industry_companies:
        if company["name"].lower() != company_name.lower():
            # Prefer same type, but include others too
            score = 1.0 if company["type"] == target_type else 0.7
            competitor = company.copy()
            competitor["industry"] = target_industry
            competitor["relevance_score"] = score
            competitors.append(competitor)
    
    # Sort by relevance and return top results
    competitors.sort(key=lambda x: x["relevance_score"], reverse=True)
    return competitors[:limit]