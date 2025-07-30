#!/usr/bin/env python3
"""
Test script to verify ChromaDB SQLite version fix
"""
import os
# Set ChromaDB backend before any other imports
os.environ["CHROMA_DB_IMPL"] = "duckdb"

def test_chromadb_import():
    """Test ChromaDB import with DuckDB backend"""
    try:
        import chromadb
        print("✅ ChromaDB import successful with DuckDB backend")
        return True
    except Exception as e:
        print(f"❌ ChromaDB import failed: {e}")
        return False

def test_streamlit_import():
    """Test Streamlit import"""
    try:
        import streamlit as st
        print("✅ Streamlit import successful")
        return True
    except Exception as e:
        print(f"❌ Streamlit import failed: {e}")
        return False

def test_competitive_engine():
    """Test competitive analysis engine import"""
    try:
        import sys
        sys.path.append('src')
        from analysis.competitive_engine import competitive_engine
        print("✅ Competitive analysis engine import successful")
        return True
    except Exception as e:
        print(f"❌ Competitive analysis engine import failed: {e}")
        return False

def test_openai_connection():
    """Test OpenAI connection"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Test with a simple completion
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=10
        )
        print("✅ OpenAI API connection successful")
        return True
    except Exception as e:
        print(f"❌ OpenAI API connection failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔧 Testing ChromaDB SQLite version fix...\n")
    
    tests = [
        ("ChromaDB Import", test_chromadb_import),
        ("Streamlit Import", test_streamlit_import),
        ("Competitive Engine", test_competitive_engine),
        ("OpenAI Connection", test_openai_connection)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"Running {test_name} test...")
        results[test_name] = test_func()
        print()
    
    # Summary
    print("=" * 50)
    print("TEST RESULTS SUMMARY:")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your Streamlit app should now work without SQLite version issues.")
        print("You can now run: streamlit run dashboard.py")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check the errors above.")

if __name__ == "__main__":
    main()