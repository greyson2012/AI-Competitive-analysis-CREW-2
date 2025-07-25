#!/usr/bin/env python3
"""
Deployment script for competitive analysis system
"""
import os
import sys
import subprocess
import asyncio
from pathlib import Path

def check_python_version():
    """Check Python version compatibility"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_environment_file():
    """Check if .env file exists and is configured"""
    print("\n⚙️  Checking environment configuration...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        print("   Copy .env.example to .env and configure your API keys")
        return False
    
    # Check for required variables
    with open(env_file) as f:
        content = f.read()
    
    required_vars = ["SUPABASE_URL", "SUPABASE_KEY", "OPENAI_API_KEY", "SERPER_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if f"{var}=your_" in content or f"{var}=" not in content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Configure these variables in .env: {', '.join(missing_vars)}")
        return False
    
    print("✅ Environment file configured")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    directories = ["logs", "data", "temp"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Directories created")
    return True

async def test_system():
    """Run system tests"""
    print("\n🧪 Running system tests...")
    
    try:
        # Add src to path for testing
        sys.path.append(str(Path("src").absolute()))
        
        # Import test function
        from test_integration import test_imports, test_database_connection
        
        # Test imports
        if not test_imports():
            return False
        
        # Test database
        if not await test_database_connection():
            return False
        
        print("✅ System tests passed")
        return True
        
    except Exception as e:
        print(f"❌ System tests failed: {e}")
        return False

def setup_database():
    """Setup database schema"""
    print("\n🗄️  Setting up database...")
    
    try:
        subprocess.run([sys.executable, "setup_database.py"], check=True)
        print("✅ Database setup completed")
        return True
    except subprocess.CalledProcessError:
        print("⚠️  Database setup had issues - please run manually if needed")
        return True  # Don't fail deployment for this

def create_startup_scripts():
    """Create startup scripts for different platforms"""
    print("\n📜 Creating startup scripts...")
    
    # Unix/Linux/Mac script
    unix_script = """#!/bin/bash
# Competitive Analysis System - Startup Script

echo "🚀 Starting Competitive Analysis System..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please configure your environment."
    exit 1
fi

# Start the scheduler in background
echo "🕒 Starting scheduler..."
python src/utils/scheduler.py start &
SCHEDULER_PID=$!

# Start the dashboard
echo "📊 Starting dashboard..."
streamlit run src/ui/app.py --server.headless true --server.port 8501 &
DASHBOARD_PID=$!

echo "✅ System started successfully!"
echo "   Dashboard: http://localhost:8501"
echo "   Scheduler PID: $SCHEDULER_PID"
echo "   Dashboard PID: $DASHBOARD_PID"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap 'echo "🛑 Stopping services..."; kill $SCHEDULER_PID $DASHBOARD_PID; exit' INT
wait
"""
    
    with open("start.sh", "w") as f:
        f.write(unix_script)
    os.chmod("start.sh", 0o755)
    
    # Windows script
    windows_script = """@echo off
REM Competitive Analysis System - Startup Script

echo 🚀 Starting Competitive Analysis System...

REM Activate virtual environment if it exists
if exist "venv\\Scripts\\activate.bat" (
    call venv\\Scripts\\activate.bat
    echo ✅ Virtual environment activated
)

REM Check if .env exists
if not exist ".env" (
    echo ❌ .env file not found. Please configure your environment.
    pause
    exit /b 1
)

REM Start the services
echo 🕒 Starting scheduler...
start "Scheduler" python src\\utils\\scheduler.py start

echo 📊 Starting dashboard...
start "Dashboard" streamlit run src\\ui\\app.py --server.headless true --server.port 8501

echo ✅ System started successfully!
echo    Dashboard: http://localhost:8501
echo.
echo Press any key to continue...
pause
"""
    
    with open("start.bat", "w") as f:
        f.write(windows_script)
    
    print("✅ Startup scripts created (start.sh, start.bat)")
    return True

def display_next_steps():
    """Display next steps for the user"""
    print("\n" + "="*60)
    print("🎉 DEPLOYMENT COMPLETE!")
    print("="*60)
    print("\n📋 Next Steps:")
    print("1. Configure your .env file with API keys")
    print("2. Set up your Supabase database schema")
    print("3. Test the system:")
    print("   python test_integration.py")
    print("\n🚀 To Start the System:")
    print("   ./start.sh        (Linux/Mac)")
    print("   start.bat         (Windows)")
    print("   OR manually:")
    print("   python src/utils/scheduler.py start &")
    print("   streamlit run src/ui/app.py")
    print("\n📊 Dashboard will be available at: http://localhost:8501")
    print("\n🔧 Manual Commands:")
    print("   python src/crew/main.py daily     # Run daily analysis")
    print("   python src/crew/main.py quick AI  # Quick analysis")
    print("   python src/utils/scheduler.py test-daily  # Test run")
    print("\n📚 Documentation:")
    print("   - SETUP.md for detailed setup instructions")
    print("   - README.md for system overview")
    print("   - /doc/ folder for comprehensive documentation")

async def main():
    """Main deployment function"""
    print("🚀 Competitive Analysis System - Deployment Script")
    print("="*60)
    
    # Pre-deployment checks
    if not check_python_version():
        return
    
    if not check_environment_file():
        print("\n💡 To fix: Copy .env.example to .env and configure your API keys")
        return
    
    # Installation steps
    if not install_dependencies():
        return
    
    if not create_directories():
        return
    
    setup_database()  # This can have issues but shouldn't fail deployment
    
    if not create_startup_scripts():
        return
    
    # System tests
    if not await test_system():
        print("\n⚠️  Some tests failed, but deployment is complete.")
        print("   You may need to configure API keys or database settings.")
    
    display_next_steps()

if __name__ == "__main__":
    asyncio.run(main())