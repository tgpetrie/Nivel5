#!/bin/bash
# Web App Launcher for Español 5 Dynamic Exam
# ============================================

echo "🇲🇽 Español 5 - Dynamic Exam Generator (Web Version) 🇲🇽"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.6 or higher."
    exit 1
fi

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Installing Flask..."
    pip install flask
    echo ""
fi

echo "🚀 Starting web server..."
echo "📱 The exam will open at: http://localhost:5000"
echo ""
echo "💡 Press Ctrl+C to stop the server"
echo ""

# Start the Flask app
python3 app.py
