#!/usr/bin/env python3
"""
Quick test script to verify API keys work without complex dependencies
"""
import os
import requests
from dotenv import load_dotenv

def test_openai_api():
    """Test OpenAI API connection"""
    print("🧪 Testing OpenAI API...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OpenAI API key not found")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Simple API test
        response = requests.get(
            "https://api.openai.com/v1/models", 
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            models = response.json()
            print(f"✅ OpenAI API working - Found {len(models.get('data', []))} models")
            return True
        else:
            print(f"❌ OpenAI API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ OpenAI API test failed: {e}")
        return False

def test_serper_api():
    """Test Serper search API"""
    print("\n🧪 Testing Serper API...")
    
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        print("❌ Serper API key not found")
        return False
    
    try:
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "q": "AI news test",
            "num": 3
        }
        
        response = requests.post(
            "https://google.serper.dev/search",
            headers=headers,
            json=data,
            timeout=15
        )
        
        if response.status_code == 200:
            results = response.json()
            organic_count = len(results.get("organic", []))
            print(f"✅ Serper API working - Found {organic_count} search results")
            return True
        else:
            print(f"❌ Serper API error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Serper API test failed: {e}")
        return False

def test_supabase_connection():
    """Test Supabase connection"""
    print("\n🧪 Testing Supabase connection...")
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("❌ Supabase credentials not found")
        return False
    
    try:
        # Test basic connection to Supabase REST API
        headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        
        # Try to access the API (this should work even if no tables exist)
        response = requests.get(
            f"{url}/rest/v1/",
            headers=headers,
            timeout=10
        )
        
        if response.status_code in [200, 404]:  # 404 is fine, means API is accessible
            print("✅ Supabase connection working")
            return True
        else:
            print(f"❌ Supabase connection error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Supabase connection test failed: {e}")
        return False

def test_ai_completion():
    """Test a simple AI completion"""
    print("\n🧪 Testing AI completion...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OpenAI API key not found")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": "Summarize the current state of AI market in one sentence."}
            ],
            "max_tokens": 50
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            message = result["choices"][0]["message"]["content"]
            print(f"✅ AI completion working")
            print(f"   Sample response: {message[:100]}...")
            return True
        else:
            print(f"❌ AI completion error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ AI completion test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Competitive Analysis System - Quick API Test")
    print("=" * 60)
    
    load_dotenv()
    
    # Run all tests
    tests = [
        test_openai_api,
        test_serper_api,
        test_supabase_connection,
        test_ai_completion
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All API tests passed! Your system is ready to run.")
        print("\nNext steps:")
        print("1. Install dependencies: pip install crewai openai supabase requests python-dotenv")
        print("2. Set up database schema in Supabase")
        print("3. Test full system: python src/crew/main.py quick 'AI trends'")
    else:
        print("⚠️  Some API tests failed. Please check your configuration.")

if __name__ == "__main__":
    main()