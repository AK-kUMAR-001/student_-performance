#!/bin/bash
# Quick Start Script for Student Performance Predictor

echo "=========================================="
echo "Student Performance Predictor - Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Install requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🗄️  Initializing database..."
python3 app.py &
sleep 2
kill $!

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To start the application, run:"
echo "  python3 app.py"
echo ""
echo "Then open http://localhost:5000 in your browser"
echo ""
echo "Test Accounts:"
echo "  - Create a new student account via signup"
echo "  - Staff/HOD: Add through database"
echo ""
echo "Documentation: See README.md"
echo "=========================================="
