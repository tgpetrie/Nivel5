@echo off
REM Web App Launcher for Español 5 Dynamic Exam
REM ============================================

echo 🇲🇽 Español 5 - Dynamic Exam Generator (Web Version) 🇲🇽
echo ==================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.6 or higher.
    pause
    exit /b 1
)

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing Flask...
    pip install flask
    echo.
)

echo 🚀 Starting web server...
echo 📱 The exam will open at: http://localhost:5000
echo.
echo 💡 Press Ctrl+C to stop the server
echo.

REM Start the Flask app
python app.py

pause
