# 🇲🇽 Examen Final Interactivo – Español 5 (UNAM Polanco)

## ¡Muchas gracias, Luis!

**Sistema de examen web completo con estructura oficial UNAM Nivel 5**

---

## 🎯 Características Principales

### ✅ **Estructura Oficial del Examen**
- **Sección I**: Gramática Objetiva (30 preguntas, 25 pts) - 5 por página
- **Sección II**: Transformaciones (12 preguntas, 15 pts) - 3 por página  
- **Sección III**: Lectura & Análisis (10 preguntas, 20 pts) - 2 por página
- **Sección IV**: Producción Escrita (1 ensayo, 20 pts) - 1 por página
- **Sección V**: Audio (excluida) - reservada para implementación futura
- **Sección VI**: Situaciones Comunicativas (6 preguntas, 10 pts) - 3 por página

### 🎨 **Interfaz Moderna**
- **Tema Visual**: Gradiente inspirado en la bandera mexicana
- **Tipografía**: Raleway para legibilidad profesional
- **Efectos**: UI flotante con sombras suaves y transiciones
- **Responsive**: Adaptado para desktop y móvil
- **Tema Oscuro**: Diseño elegante con acentos verdes y rojos

### 🧠 **Sistema de Retroalimentación**
- **Evaluación Inmediata**: Cada pregunta tiene su botón de verificación
- **Feedback Inteligente**: Explicaciones gramaticales detalladas
- **Seguimiento de Progreso**: Estadísticas en tiempo real
- **Navegación Manual**: Control total del ritmo del examen

### 🌍 **Contexto Internacional**
- **Vocabulario Mexicano**: Auténtico y contextualizado
- **Alcance Global**: Referencias a MX-USA-Rusia-China
- **Banderas**: Iconos internacionales en el header
- **Cultura**: Enlaces a recursos culturales relevantes

---

## 🚀 Instalación y Uso

### **Requisitos**
```bash
pip install flask
```

### **Ejecutar el Examen**
```bash
python app.py
```
Acceder en: **http://localhost:5002**

### **Estructura de Archivos**
```
📁 Nivel 5/
├── 📄 app.py                 # Aplicación principal Flask
├── 📁 templates/
│   ├── 📄 base.html          # Plantilla base con estilos
│   ├── 📄 index.html         # Página principal con conceptos
│   ├── 📄 exam_section.html  # Plantilla de examen seccional
│   ├── 📄 results.html       # Resultados finales
│   └── 📄 concept_study.html # Estudio individual de conceptos
├── 📄 README.md              # Esta documentación
└── 📄 requirements.txt       # Dependencias Python
```

---

## 📚 Conceptos Gramaticales Incluidos

### **Tiempos Verbales**
- **Antepresente** (Pretérito Perfecto): `ha aumentado`, `he leído`
- **Antecopretérito** (Pluscuamperfecto): `había cerrado`, `había terminado`
- **Antefuturo** (Futuro Perfecto): `habrá implementado`

### **Modo Subjuntivo**
- **Subjuntivo de Percepción**: `No veo que hagan...`
- **Subjuntivo de Opinión**: `Dudo que llegue...`
- **Subjuntivo de Necesidad**: `Es importante que asistan...`
- **Subjuntivo de Emoción**: `Me alegra que vengas...`

### **Condicionales**
- **Reales**: `Si tengo tiempo, tomaré clases`
- **Irreales**: `Si tuviera dinero, viajaría`
- **Imposibles**: `Si hubieras estudiado, serías doctora`

### **Estructuras Avanzadas**
- **Lo + Adjetivo**: `Lo bueno de esta empresa...`
- **Pronombres Relativos**: `quien`, `que`, `en quien`
- **Cláusulas Temporales**: `cuando estés listo...`
- **Discurso Indirecto**: `Biden dijo que no visitaría...`

---

## 🎓 Funcionalidades del Sistema

### **Para Estudiantes**
1. **Examen Completo**: Navegación por secciones oficiales
2. **Estudio por Conceptos**: Páginas dedicadas a cada tema gramatical
3. **Práctica Interactiva**: Preguntas generadas dinámicamente
4. **Retroalimentación Inmediata**: Explicaciones detalladas
5. **Seguimiento de Progreso**: Estadísticas personales

### **Para Profesores**
1. **Evaluación Automática**: Secciones I-II auto-calificadas
2. **Reportes Detallados**: Análisis por concepto y sección
3. **Banco de Preguntas**: Basado en examen oficial UNAM
4. **Flexibilidad**: Navegación adaptable al ritmo del estudiante

---

## 🔧 Configuración Avanzada

### **Personalizar Preguntas**
Editar en `app.py` la variable `EXAM_QUESTIONS`:
```python
'section_I': [
    {
        'question': 'Tu pregunta aquí ___ (verbo).',
        'type': 'fill',  # 'multiple_choice', 'essay', 'short_answer'
        'answer': 'respuesta_correcta',
        'concept': 'concepto_gramatical',
        'section': 'I'
    }
]
```

### **Ajustar Paginación**
Modificar en `EXAM_SECTIONS`:
```python
'questions_per_page': 5  # Número de preguntas por página
```

### **Cambiar Estilos**
Personalizar CSS en `templates/base.html` o `templates/exam_section.html`

---

## 📊 Sistema de Evaluación

### **Puntuación Automática**
- ✅ **Correcta**: +1 punto
- ❌ **Incorrecta**: 0 puntos, muestra respuesta correcta
- 📝 **Ensayos**: Marcados como "intentados" para revisión manual

### **Tipos de Retroalimentación**
- 🟢 **Verde**: Respuesta correcta con explicación
- 🔴 **Rojo**: Respuesta incorrecta con corrección
- 🟡 **Naranja**: Ensayos/respuestas largas registradas

---

## 🌟 Ejemplos de Uso

### **Pregunta de Antepresente**
```
He ___ (leer) tres artículos esta semana.
→ Respuesta: "leído"
💡 Explicación: El antepresente conecta acciones pasadas con el presente.
```

### **Pregunta de Subjuntivo**
```
Dudo que Roberto ___ temprano.
a) llega  b) llegue  c) llegó
→ Respuesta: b) "llegue"
💡 Explicación: Los verbos de opinión negativos requieren subjuntivo.
```

### **Transformación**
```
Biden: «No visitaré el Zócalo». → Discurso indirecto
→ Respuesta: "Biden dijo que no visitaría el Zócalo"
💡 Explicación: El discurso indirecto cambia tiempos y pronombres.
```

---

## 🔗 Enlaces Culturales

### **Vocabulario Mexicano**
- 🌮 **Comida**: tacos, pozole, mole, tamales, quesadillas
- 🏛️ **Lugares**: Zócalo, Xochimilco, Coyoacán, Polanco
- 👥 **Nombres**: Lupita, Paco, Gaby, Memo, Nayeli
- 🎉 **Expresiones**: ¡Órale!, ¡Qué padre!, ¡No manches!

### **Contexto Internacional**
- 🇺🇸 **USA**: Referencias académicas y culturales
- 🇷🇺 **Rusia**: Elementos de intercambio cultural (balalaika)
- 🇨🇳 **China**: Contexto comercial y turístico (Xi, churros)

---

## 💾 Backup y Mantenimiento

### **Crear Backup**
```bash
zip -r exam_backup_$(date +%Y%m%d).zip . -x "*.pyc" "__pycache__/*"
```

### **Actualizar Contenido**
1. Modificar preguntas en `EXAM_QUESTIONS`
2. Añadir conceptos en `get_concept_info()`
3. Actualizar explicaciones en `get_concept_explanation()`

---

## 👨‍🏫 Créditos

**Tom Petrie** • Guía de Estudio y Práctica • UNAM Polanco Nivel 5 2025

### **Basado en:**
- 📋 Examen Final Oficial UNAM Nivel 5
- 🎯 Metodología Comunicativa Internacional
- 🇲🇽 Contexto Cultural Mexicano Auténtico
- 🌐 Enfoque Intercultural (MX-USA-Rusia-China)

---

## 🆘 Solución de Problemas

### **El servidor no inicia**
```bash
# Verificar que Flask esté instalado
pip install flask

# Verificar puerto disponible
python app.py
```

### **Preguntas no cargan**
- Verificar sintaxis en `EXAM_QUESTIONS`
- Comprobar que todas las llaves tengan valores válidos
- Revisar logs de Flask en la terminal

### **Estilos no se ven**
- Refrescar navegador (Ctrl+F5)
- Verificar que `templates/base.html` existe
- Comprobar rutas de archivos CSS

---

## 🚀 Futuras Mejoras

- [ ] **Sección V**: Implementación completa de audio
- [ ] **Base de Datos**: Persistencia de resultados
- [ ] **Múltiples Idiomas**: Interfaz en inglés/chino/ruso
- [ ] **Análisis Avanzado**: Estadísticas detalladas por concepto
- [ ] **Exportación**: PDF de resultados
- [ ] **Modo Profesor**: Panel de administración

---

*¡Éxito en tu examen! 🎓*
