#!/usr/bin/env python3
"""
QUICK START - Run this to start the Student Performance Predictor
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python 3.7+ is installed"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        return False
    print(f"✅ Python {sys.version.split()[0]} found")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"])
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def run_app():
    """Run the Flask application"""
    print("\n🚀 Starting Student Performance Predictor...")
    print("=" * 50)
    print("📊 Server running on: http://localhost:5000")
    print("=" * 50)
    print("\n✅ FIRST TIME SETUP:")
    print("   1. Database created automatically")
    print("   2. ML model will train on first run")
    print("   3. Go to http://localhost:5000")
    print("   4. Click 'Student' → 'Student Signup'")
    print("   5. Create your account")
    print("\n⏸️  Press Ctrl+C to stop the server")
    print("=" * 50 + "\n")
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n✅ Server stopped")

def main():
    print("=" * 50)
    print("🎓 AI-Powered Student Performance Predictor")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return 1
    
    # Install requirements
    if not install_requirements():
        return 1
    
    # Run the app
    run_app()
    return 0

if __name__ == "__main__":
    sys.exit(main())
