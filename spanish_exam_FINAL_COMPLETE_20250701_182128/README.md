# Español 5 - Dynamic Final Exam Generator 🇲🇽

A comprehensive Spanish exam application with **dynamic question generation** using authentic Mexican Spanish vocabulary and expressions. Available in both **terminal** and **web browser** versions.

## � NEW: Dynamic Question Generation

This exam now features **revolutionary dynamic content**:
- ✨ **New questions every time** - No two exams are the same
- 🇲🇽 **Authentic Mexican Spanish** - Names, places, food, and expressions
- 📚 **Concept-based generation** - Questions focus on grammar concepts, not memorized examples
- 🔄 **Unlimited practice** - Generate as many exam variations as needed

## 🎯 Features

### Core Features
- **Dynamic Content**: Generate new questions each time based on grammar concepts
- **Mexican Vocabulary**: Lupita, Paco, pozole, tacos, Xochimilco, ¡Órale!, etc.
- **Auto-grading**: Immediate feedback for objective questions
- **Concept Coverage**: Antepresente, subjuntivo, condicional, and more
- **Multiple Formats**: Both terminal and web browser versions

### Grammar Concepts Covered
- 🔹 **Antepresente** - He comido, has visitado...
- 🔹 **Antecopretérito** - Había llegado, habías comido...
- 🔹 **"Lo + adjetivo"** - Lo bueno de México es...
- 🔹 **Subjuntivo de percepción** - Veo que... / No veo que...
- 🔹 **Subjuntivo de opinión** - Creo que... / No creo que...
- 🔹 **Condicional** - Si tuviera dinero, compraría...
- 🔹 **Cláusulas temporales** - Cuando llegues, en cuanto termines...

## 🚀 Quick Start

### Option 1: Web Browser Version (Recommended)

1. **Install dependencies:**
   ```bash
   pip install flask
   ```

2. **Run the web app:**
   ```bash
   python app.py
   ```

3. **Open your browser:**
   - Go to `http://localhost:5000`
   - Take the exam with a beautiful web interface
   - Get instant feedback and detailed results

### Option 2: Terminal Version

1. **Run the terminal app:**
   ```bash
   python Nivel5_generador_dinamico.py
   ```

2. **Choose from the menu:**
   - Take a full exam (15 questions)
   - Practice specific concepts
   - Regenerate new questions anytime

### Prerequisites
- Python 3.6 or higher
- Flask (for web version only)

## 🌐 Web Version Features

The browser-based version includes:
- 📱 **Responsive design** - Works on desktop, tablet, and mobile
- 🎨 **Beautiful interface** - Modern, Mexican-themed design
- ⚡ **Real-time feedback** - Instant grading with explanations
- 📊 **Detailed results** - Score breakdown by concept
- 🖨️ **Printable results** - Save or print your performance report
## 📋 Available Files

### Main Applications
- **`app.py`** - Web browser version (Flask)
- **`Nivel5_generador_dinamico.py`** - Terminal version
- **`requirements.txt`** - Dependencies for web version

### Deployment Scripts
- **`deploy.sh`** / **`deploy.bat`** - Setup scripts for distribution
- **`run_exam.sh`** / **`run_exam.bat`** - Quick launcher scripts

### Legacy Files
- **`espanol5_quiz.py`** - Original static quiz
- **`espanol5_study_app.py`** - Original study app
- **`Nivel5 guia ineractivo.py`** - Original interactive guide

## 🔧 Deployment Options

### 1. Web Application Deployment

**For Production:**
```bash
# Install production WSGI server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

**For Development:**
```bash
python app.py
```

### 2. Terminal Application Distribution

**Using the deployment scripts:**
```bash
# Unix/macOS
chmod +x deploy.sh
./deploy.sh

# Windows
deploy.bat
```

**Direct distribution:**
Share `Nivel5_generador_dinamico.py` with students who have Python.

### 3. Standalone Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile Nivel5_generador_dinamico.py
```

## 🎓 How It Works

### Dynamic Question Generation

1. **Concept Selection**: System randomly selects grammar concepts
2. **Template Filling**: Templates are filled with Mexican vocabulary
3. **Answer Generation**: Correct answers are generated based on grammar rules
4. **Variety Assurance**: No two exams will have identical questions

### Mexican Spanish Integration

The system uses authentic Mexican vocabulary:
- **Names**: Lupita, Paco, Chuy, Gaby, Memo, Lety...
- **Places**: Zócalo, Xochimilco, Coyoacán, Condesa...
- **Food**: Tacos, pozole, mole, tamales, chilaquiles...
- **Expressions**: ¡Órale!, ¡Qué padre!, ¡No manches!...

## 📊 Exam Experience

### Terminal Version
```
=== EXAMEN DINÁMICO DE ESPAÑOL 5 ===
🇲🇽 Gramática y Vocabulario Mexicano 🇲🇽

1. ¿Quieres hacer el examen completo? (15 preguntas)
2. ¿Practicar conceptos específicos?
3. ¿Ver estadísticas?
4. ¿Generar nuevas preguntas?
5. Salir

Opción: _
```

### Web Version
- Modern, responsive interface
- Progress tracking
- Instant feedback
- Detailed results with concept breakdown
- Printable score reports

## 📁 File Output

The applications can save:
- **Student responses** (JSON format)
- **Score reports** (printable)
- **Practice sessions** (terminal version)

## 🌐 Cultural Integration

This exam features culturally authentic content:
- 🇲🇽 **Mexican culture**: Real places, food, names, and expressions
- 📚 **Academic rigor**: University-level grammar concepts
- 🗣️ **Colloquial language**: Natural, spoken Mexican Spanish

## 🐛 Troubleshooting

**Character encoding issues?**
- Ensure your terminal supports UTF-8 encoding
- On Windows, try: `chcp 65001` before running

**Permission denied?**
- Make the file executable: `chmod +x "Nivel5 guia ineractivo.py"`

**Python not found?**
- Install Python from [python.org](https://python.org)
- Ensure Python is in your system PATH

## 📞 Support

For technical issues or questions about deployment, contact the instructor.

## 📄 License

Educational use only. Created for UNAM Polanco Spanish program.

---

**¡Buena suerte en tu examen!** 🍀
