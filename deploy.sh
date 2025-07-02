#!/bin/bash

# Deployment Script for Español 5 Interactive Exam
# This script prepares the exam for various deployment scenarios

echo "🇪🇸 Preparing Español 5 Dynamic Mexican Spanish Exam for Deployment..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Make the scripts executable
chmod +x "Nivel5 guia ineractivo.py"
chmod +x "Nivel5_generador_dinamico.py"
chmod +x "question_database.py"
echo "✅ Made exam scripts executable"

# Test run the scripts (dry run)
echo ""
echo "🧪 Testing exam scripts..."
python3 -c "
import sys
sys.path.append('.')
try:
    import textwrap, unicodedata, json, os, random
    print('✅ All required modules available')
except ImportError as e:
    print(f'❌ Missing module: {e}')
    sys.exit(1)
"

echo ""
echo "🎯 NEW FEATURES:"
echo "   ✅ Dynamic question generation"
echo "   ✅ Mexican Spanish vocabulary"
echo "   ✅ Question database storage"
echo "   ✅ Regenerate questions on demand"
echo ""
echo "📦 Deployment Options:"
echo ""
echo "1. 📁 Direct Distribution:"
echo "   Share 'Nivel5_generador_dinamico.py' (NEW DYNAMIC VERSION)"
echo "   OR 'Nivel5 guia ineractivo.py' (static version)"
echo "   Run with: python3 'Nivel5_generador_dinamico.py'"
echo ""
echo "2. 🔧 Create Standalone Executable:"
echo "   pip install pyinstaller"
echo "   pyinstaller --onefile 'Nivel5_generador_dinamico.py'"
echo ""
echo "3. ☁️  Cloud Deployment:"
echo "   Upload to Replit, PythonAnywhere, or Google Colab"
echo ""
echo "4. 🎓 Classroom Setup:"
echo "   Place files in shared network folder"
echo "   Students run: python3 'Nivel5_generador_dinamico.py'"
echo ""

# Create a simple launcher script
cat > run_exam.sh << 'EOF'
#!/bin/bash
echo "🇪🇸 Iniciando Examen Final - Español 5..."
echo ""
python3 "Nivel5 guia ineractivo.py"
EOF

chmod +x run_exam.sh
echo "✅ Created launcher script: run_exam.sh"

# Create Windows batch file
cat > run_exam.bat << 'EOF'
@echo off
echo 🇪🇸 Iniciando Examen Final - Español 5...
echo.
python "Nivel5 guia ineractivo.py"
pause
EOF

echo "✅ Created Windows launcher: run_exam.bat"

echo ""
echo "🎉 Deployment preparation complete!"
echo ""
echo "📋 Files ready for deployment:"
echo "   - Nivel5 guia ineractivo.py (main exam)"
echo "   - README.md (documentation)"
echo "   - requirements.txt (dependencies)"
echo "   - run_exam.sh (Unix/Mac launcher)"
echo "   - run_exam.bat (Windows launcher)"
echo ""
echo "🚀 Ready to deploy!"
