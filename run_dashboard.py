#!/usr/bin/env python3
"""
Dashboard startup script with ChromaDB SQLite fix
"""
import os
import sys
import subprocess

# Set ChromaDB backend to avoid SQLite version issues
os.environ["CHROMA_DB_IMPL"] = "duckdb"

def main():
    """Start the Streamlit dashboard with proper environment setup"""
    print("🚀 Starting AI Competitive Analysis Dashboard...")
    print("🔧 Environment: ChromaDB backend set to DuckDB (SQLite compatibility fix)")
    
    try:
        # Start Streamlit with the dashboard
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "dashboard.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting dashboard: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check that your .env file contains valid API keys")
        print("3. Try running: streamlit run dashboard.py manually")

if __name__ == "__main__":
    main()