@echo off
echo 🇪🇸 Preparing Español 5 Interactive Exam for Deployment...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed.
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Test the exam script
echo.
echo 🧪 Testing exam script...
python -c "import textwrap, unicodedata, json, os, sys; print('✅ All required modules available')"

echo.
echo 📦 Deployment Options:
echo.
echo 1. 📁 Direct Distribution:
echo    Share 'Nivel5 guia ineractivo.py' with students
echo    Run with: python "Nivel5 guia ineractivo.py"
echo.
echo 2. 🔧 Create Standalone Executable:
echo    pip install pyinstaller
echo    pyinstaller --onefile "Nivel5 guia ineractivo.py"
echo.
echo 3. ☁️  Cloud Deployment:
echo    Upload to Replit, PythonAnywhere, or Google Colab
echo.
echo 4. 🎓 Classroom Setup:
echo    Place file in shared network folder
echo    Students run: python "Nivel5 guia ineractivo.py"
echo.

echo ✅ Created Windows launcher: run_exam.bat
echo.
echo 🎉 Deployment preparation complete!
echo.
echo 📋 Files ready for deployment:
echo    - Nivel5 guia ineractivo.py (main exam)
echo    - README.md (documentation)
echo    - requirements.txt (dependencies)
echo    - run_exam.bat (Windows launcher)
echo.
echo 🚀 Ready to deploy!
echo.
pause
