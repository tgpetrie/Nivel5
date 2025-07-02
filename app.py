#!/usr/bin/env python3
"""
Interactive Final Exam – Español 5 (Web Version)
------------------------------------------------
• Browser-based Spanish exam with dynamic question generation
• Mexican Spanish vocabulary and grammar concepts
• Auto-grading with instant feedback
"""

from flask import Flask, render_template, request, jsonify, session, redirect
import json
import random
import unicodedata
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'espanol5_mexicano_2025'

# Context processor to make request available in templates
@app.context_processor
def inject_request():
    return dict(request=request)

ACCENTS = {c: None for c in range(0x300, 0x370)}
strip = lambda s: unicodedata.normalize("NFD", s).translate(ACCENTS).lower()

# Mexican Spanish vocabulary and expressions
MEXICAN_VOCAB = {
    'people': ['Lupita', 'Paco', 'Chuy', 'Gaby', 'Memo', 'Lety', 'Toño', 'Nayeli', 'Rafa', 'Ceci'],
    'food': ['tacos', 'pozole', 'mole', 'tamales', 'quesadillas', 'chilaquiles', 'elote', 'esquites'],
    'places': ['el Zócalo', 'Xochimilco', 'Coyoacán', 'la Condesa', 'Polanco', 'Tlatelolco', 'Teotihuacán'],
    'expressions': ['¡Órale!', '¡Qué padre!', '¡No manches!', '¡Está padrísimo!'],
    'activities': ['ir al tianguis', 'ver lucha libre', 'escuchar mariachi', 'bailar jarabe tapatío'],
    'objects': ['rebozo', 'huaraches', 'sombrero', 'guitarra', 'piñata', 'molcajete'],
    'professions': ['taquero', 'mariachi', 'albañil', 'maestra', 'doctor', 'ingeniero']
}

# Official Exam Structure - Based on UNAM Nivel 5 Final Exam
EXAM_SECTIONS = {
    'I': {
        'title': 'Gramática Objetiva',
        'description': 'Selecciona la opción correcta o completa el espacio.',
        'questions_per_page': 5,
        'total_questions': 30,
        'points': 25
    },
    'II': {
        'title': 'Transformaciones',
        'description': 'Reescribe o transforma según se indica.',
        'questions_per_page': 3,
        'total_questions': 12,
        'points': 15
    },
    'III': {
        'title': 'Lectura & Análisis Gramatical',
        'description': 'Lee el texto y responde las preguntas.',
        'questions_per_page': 2,
        'total_questions': 10,
        'points': 20
    },
    'IV': {
        'title': 'Producción Escrita',
        'description': 'Escribe 130-150 palabras sobre el tema dado.',
        'questions_per_page': 1,
        'total_questions': 1,
        'points': 20
    },
    'V': {
        'title': 'Comprensión Auditiva',
        'description': 'Escucha el audio y responde las preguntas.',
        'questions_per_page': 5,
        'total_questions': 5,
        'points': 10,
        'excluded': True  # Audio section excluded per requirements
    },
    'VI': {
        'title': 'Situaciones Comunicativas',
        'description': 'Responde brevemente a las situaciones.',
        'questions_per_page': 3,
        'total_questions': 6,
        'points': 10
    }
}

# Comprehensive question bank organized by official UNAM exam sections
EXAM_QUESTIONS = {
    # Section I: Grammar (30 questions) - Based on official CLAVE answers
    'section_I': [
        {
            'question': 'He ___ (leer) tres artículos esta semana.',
            'type': 'fill',
            'answer': 'leído',
            'concept': 'antepresente',
            'section': 'I'
        },
        {
            'question': 'Ricardo ___ (aumentar) mucho de peso últimamente.',
            'type': 'fill',
            'answer': 'ha aumentado',
            'concept': 'antepresente',
            'section': 'I'
        },
        {
            'question': 'Ya ___ (cerrar-ellos) la biblioteca cuando llegamos.',
            'type': 'fill',
            'answer': 'habían cerrado',
            'concept': 'antecopreterito',
            'section': 'I'
        },
        {
            'question': 'Cuando llegué a casa, mi hermana ya ___ (terminar) la tarea.',
            'type': 'fill',
            'answer': 'había terminado',
            'concept': 'antecopreterito',
            'section': 'I'
        },
        {
            'question': 'Lo bueno ___ esta empresa es que tienen buenas prestaciones.',
            'type': 'multiple_choice',
            'options': {'a': 'de', 'b': 'en', 'c': 'por', 'd': 'sobre'},
            'answer': 'a',
            'concept': 'lo_adjetivo',
            'section': 'I'
        },
        {
            'question': 'Lo malo ___ vivir lejos es el tráfico.',
            'type': 'multiple_choice',
            'options': {'a': 'de', 'b': 'en', 'c': 'por', 'd': 'sobre'},
            'answer': 'a',
            'concept': 'lo_adjetivo',
            'section': 'I'
        },
        {
            'question': '*No veo que* los políticos ___ algo para cambiar las cosas.',
            'type': 'multiple_choice',
            'options': {'a': 'hagan', 'b': 'hacen', 'c': 'hicieron', 'd': 'harán'},
            'answer': 'a',
            'concept': 'subjuntivo_percepcion',
            'section': 'I'
        },
        {
            'question': '*Veo que* Sofía ___ muy cansada.',
            'type': 'multiple_choice',
            'options': {'a': 'está', 'b': 'esté', 'c': 'estuviera', 'd': 'estará'},
            'answer': 'a',
            'concept': 'subjuntivo_percepcion',
            'section': 'I'
        },
        {
            'question': 'Creo que la economía ___ estable.',
            'type': 'multiple_choice',
            'options': {'a': 'es', 'b': 'sea', 'c': 'fuera', 'd': 'será'},
            'answer': 'a',
            'concept': 'subjuntivo_opinion',
            'section': 'I'
        },
        {
            'question': 'Dudo que la situación ___ pronto.',
            'type': 'multiple_choice',
            'options': {'a': 'mejora', 'b': 'mejore', 'c': 'mejoró', 'd': 'mejorará'},
            'answer': 'b',
            'concept': 'subjuntivo_opinion',
            'section': 'I'
        },
        {
            'question': 'Necesito que ustedes ___ (entregar) el proyecto mañana.',
            'type': 'fill',
            'answer': 'entreguen',
            'concept': 'subjuntivo_necesidad',
            'section': 'I'
        },
        {
            'question': 'Era importante que Lupita ___ (asistir) a la conferencia.',
            'type': 'fill',
            'answer': 'asistiera',
            'concept': 'subjuntivo_necesidad',
            'section': 'I'
        },
        {
            'question': 'Mi papá me sugirió ___ (participar) en el concurso.',
            'type': 'fill',
            'answer': 'participar',
            'concept': 'infinitivo_vs_subjuntivo',
            'section': 'I'
        },
        {
            'question': 'El profesor pidió que los estudiantes ___ (leer) más libros.',
            'type': 'fill',
            'answer': 'leyeran',
            'concept': 'subjuntivo_necesidad',
            'section': 'I'
        },
        {
            'question': 'Si tuviera más tiempo, ___ (terminar) mi novela.',
            'type': 'fill',
            'answer': 'terminaría',
            'concept': 'condicional',
            'section': 'I'
        },
        {
            'question': 'Llámame en cuanto ___ (comenzar-tú) el proyecto.',
            'type': 'fill',
            'answer': 'comiences',
            'concept': 'temporal_clauses',
            'section': 'I'
        },
        {
            'question': 'Espero que mis padres ___ (visitar) México el próximo año.',
            'type': 'fill',
            'answer': 'visiten',
            'concept': 'subjuntivo_necesidad',
            'section': 'I'
        },
        {
            'question': 'Me gustaría que ellos ___ (visitar) Xochimilco conmigo.',
            'type': 'fill',
            'answer': 'visitaran',
            'concept': 'subjuntivo_necesidad',
            'section': 'I'
        },
        {
            'question': 'Miguel es un empresario ___ trabaja en tecnología verde.',
            'type': 'fill',
            'answer': 'que',
            'concept': 'pronombres_relativos',
            'section': 'I'
        },
        {
            'question': 'El Dr. Robles, ___ trabaja en genética, dará una conferencia.',
            'type': 'fill',
            'answer': 'quien',
            'concept': 'pronombres_relativos',
            'section': 'I'
        },
        {
            'question': 'Andrea es una persona ___ confío plenamente.',
            'type': 'fill',
            'answer': 'en quien',
            'concept': 'pronombres_relativos',
            'section': 'I'
        },
        {
            'question': 'Avísame tan pronto como ___ (estar-tú) listo para salir.',
            'type': 'fill',
            'answer': 'estés',
            'concept': 'temporal_clauses',
            'section': 'I'
        },
        {
            'question': 'Cuando era niño, siempre ___ (comer-yo) tacos los domingos.',
            'type': 'fill',
            'answer': 'comía',
            'concept': 'tiempos_pasados',
            'section': 'I'
        },
        {
            'question': 'Para 2030, la universidad ya ___ (implementar) el nuevo programa.',
            'type': 'fill',
            'answer': 'habrá implementado',
            'concept': 'antefuturo',
            'section': 'I'
        },
        {
            'question': 'Si tengo tiempo libre, ___ (tomar-yo) clases de francés.',
            'type': 'fill',
            'answer': 'tomaré',
            'concept': 'condicional_real',
            'section': 'I'
        },
        {
            'question': 'Si tuviera más dinero, ___ (viajar-yo) por toda Europa.',
            'type': 'fill',
            'answer': 'viajaría',
            'concept': 'condicional',
            'section': 'I'
        },
        {
            'question': 'Si hubieras estudiado medicina, ___ (ser-tú) doctora ahora.',
            'type': 'fill',
            'answer': 'serías',
            'concept': 'condicional',
            'section': 'I'
        },
        {
            'question': 'Ojalá que Xi ___ (poder) visitarnos en México.',
            'type': 'fill',
            'answer': 'pueda',
            'concept': 'subjuntivo_deseo',
            'section': 'I'
        },
        {
            'question': 'Esperamos que los estudiantes ___ (hacer) un buen examen.',
            'type': 'fill',
            'answer': 'hagan',
            'concept': 'subjuntivo_necesidad',
            'section': 'I'
        },
        {
            'question': 'He ___ (abrir) la cuenta de correo electrónico dos veces hoy.',
            'type': 'fill',
            'answer': 'abierto',
            'concept': 'participios_irregulares',
            'section': 'I'
        }
    ],
    
    # Section II: Transformations (12 questions) - Based on official transformations
    'section_II': [
        {
            'question': 'Biden: «No visitaré el Zócalo el lunes». → Transforma a discurso indirecto.',
            'type': 'fill',
            'answer': 'Biden dijo que no visitaría el Zócalo el lunes',
            'concept': 'discurso_indirecto',
            'section': 'II'
        },
        {
            'question': 'Ya habían inaugurado el Tren Maya. → Transforma usando "todavía no".',
            'type': 'fill',
            'answer': 'Todavía no habían inaugurado el Tren Maya',
            'concept': 'antecopreterito',
            'section': 'II'
        },
        {
            'question': 'Si China reduce tarifas, México exportará más aguacate. → Transforma a condicional irreal.',
            'type': 'fill',
            'answer': 'Si China redujera tarifas, México exportaría más aguacate',
            'concept': 'condicional',
            'section': 'II'
        },
        {
            'question': 'Rodrigo es una persona. Yo confío en la persona. → Combina con pronombre relativo.',
            'type': 'fill',
            'answer': 'Rodrigo es una persona en la que confío',
            'concept': 'pronombres_relativos',
            'section': 'II'
        },
        {
            'question': 'Es importante asistir a la junta. → Transforma con sujeto explícito.',
            'type': 'fill',
            'answer': 'Es importante que maestros y alumnos asistan a la junta',
            'concept': 'subjuntivo_necesidad',
            'section': 'II'
        },
        {
            'question': 'El ruido de vivir aquí es malo. → Transforma usando "lo + adjetivo + de".',
            'type': 'fill',
            'answer': 'Lo malo de vivir aquí es el ruido',
            'concept': 'lo_adjetivo',
            'section': 'II'
        },
        {
            'question': 'Cuando termines la tarea, salimos. → Transforma a tiempo pasado habitual.',
            'type': 'fill',
            'answer': 'Cuando terminabas la tarea, salíamos',
            'concept': 'tiempos_pasados',
            'section': 'II'
        },
        {
            'question': 'Para 2027, el proyecto habrá concluido. → Cambia antefuturo a pluscuamperfecto.',
            'type': 'fill',
            'answer': 'Para 2027, el proyecto ya había concluido',
            'concept': 'tiempos_compuestos',
            'section': 'II'
        },
        {
            'question': 'Si hubieras ido, lo habrías visto. → Transforma a condicional real.',
            'type': 'fill',
            'answer': 'Si vas, lo verás',
            'concept': 'condicional_real',
            'section': 'II'
        },
        {
            'question': 'Quería que sus alumnos estudiaran más. → Transforma a presente.',
            'type': 'fill',
            'answer': 'Quiere que sus alumnos estudien más',
            'concept': 'subjuntivo_necesidad',
            'section': 'II'
        },
        {
            'question': 'A mí me encanta que vengas. → Transforma usando pretérito imperfecto de subjuntivo.',
            'type': 'fill',
            'answer': 'A mí me encantaba que vinieras',
            'concept': 'subjuntivo_emocion',
            'section': 'II'
        },
        {
            'question': 'Uso una app. La app corrige mi acento. → Combina con relativa explicativa.',
            'type': 'fill',
            'answer': 'La app, que corrige mi acento, la uso diario',
            'concept': 'oraciones_relativas',
            'section': 'II'
        }
    ],
    
    # Section III: Reading & Analysis (sample questions)
    'section_III': [
        {
            'question': 'Según el texto, ¿cuál es el objetivo principal del proyecto UNAM-EE.UU.?',
            'type': 'multiple_choice',
            'options': {'a': 'Limpiar el Río Grande', 'b': 'Estudiar la biodiversidad', 'c': 'Promover el turismo', 'd': 'Desarrollar tecnología'},
            'answer': 'a',
            'concept': 'comprension_lectora',
            'section': 'III',
            'text': 'Un innovador proyecto binacional entre la UNAM y universidades estadounidenses busca limpiar y restaurar el ecosistema del Río Grande mediante técnicas de biorremediación desarrolladas por estudiantes de ambos países.'
        },
        {
            'question': 'En la frase "la contaminación habrá disminuido", el tiempo verbal indica:',
            'type': 'multiple_choice',
            'options': {'a': 'Una acción pasada', 'b': 'Una acción futura completada', 'c': 'Una acción presente', 'd': 'Una acción condicional'},
            'answer': 'b',
            'concept': 'antefuturo',
            'section': 'III',
            'text': 'Para 2030, según las proyecciones del estudio, la contaminación habrá disminuido significativamente en la región fronteriza.'
        }
    ],
    
    # Section IV: Writing (1 long question)
    'section_IV': [
        {
            'question': 'Escribe un texto de 130-150 palabras sobre "La quesadilla intergaláctica": Imagina que eres un embajador culinario y debes explicar a extraterrestres qué es una quesadilla mexicana. Usa presente de subjuntivo, condicional y vocabulario mexicano específico. Incluye: ingredientes tradicionales, proceso de preparación, y significado cultural.',
            'type': 'essay',
            'answer': '',  # Will be graded manually
            'concept': 'produccion_escrita',
            'section': 'IV'
        }
    ],
    
    # Section V: Audio (excluded but keeping structure for reference)
    'section_V': [
        {
            'question': '¿Dónde se llevó a cabo el reto gastronómico mencionado en el audio?',
            'type': 'short_answer',
            'answer': 'UNAM Polanco',
            'concept': 'comprension_auditiva',
            'section': 'V',
            'audio_script': 'El sábado pasado se llevó a cabo un reto gastronómico en la UNAM Polanco...'
        },
        {
            'question': '¿Cuál fue el ingrediente principal del plato ganador?',
            'type': 'short_answer',
            'answer': 'maíz',
            'concept': 'comprension_auditiva',
            'section': 'V'
        },
        {
            'question': '¿Cómo se llamaba la creación ganadora?',
            'type': 'short_answer',
            'answer': 'ramen elote azul',
            'concept': 'comprension_auditiva',
            'section': 'V'
        },
        {
            'question': '¿Quiénes participaron en el concurso?',
            'type': 'short_answer',
            'answer': 'estudiantes Nivel 5',
            'concept': 'comprension_auditiva',
            'section': 'V'
        },
        {
            'question': '¿Qué habían hecho los estudiantes antes del evento?',
            'type': 'short_answer',
            'answer': 'ya habían subido historias',
            'concept': 'comprension_auditiva',
            'section': 'V'
        }
    ],
    
    # Section VI: Communicative Situations (6 questions)
    'section_VI': [
        {
            'question': 'Tu amigo estadounidense te pregunta qué bebida tradicional mexicana debería probar. Sugiere mezcal usando una construcción de voluntad + pretérito de subjuntivo.',
            'type': 'short_answer',
            'answer': 'Te aconsejé que probaras mezcal artesanal de Oaxaca',
            'concept': 'situaciones_comunicativas',
            'section': 'VI'
        },
        {
            'question': 'Expresa emoción usando imperfecto de subjuntivo sobre músicos rusos tocando balalaika.',
            'type': 'short_answer',
            'answer': 'Me encantaba que tocaran balalaika en las fiestas',
            'concept': 'subjuntivo_emocion',
            'section': 'VI'
        },
        {
            'question': 'Construye una oración usando "tan pronto como" + subjuntivo.',
            'type': 'short_answer',
            'answer': 'Tan pronto como llegues a México, te llevaré al Zócalo',
            'concept': 'temporal_clauses',
            'section': 'VI'
        },
        {
            'question': 'Escribe una oración con pronombre relativo usando el verbo "confiar en".',
            'type': 'short_answer',
            'answer': 'Luis es el traductor en quien confío para documentos importantes',
            'concept': 'pronombres_relativos',
            'section': 'VI'
        },
        {
            'question': 'Crea una oración relativa especificativa sobre una app tecnológica.',
            'type': 'short_answer',
            'answer': 'Uso una app que corrige mi pronunciación en español',
            'concept': 'oraciones_relativas',
            'section': 'VI'
        },
        {
            'question': 'Construye una frase usando "lo + adjetivo + de" para hablar de los tacos.',
            'type': 'short_answer',
            'answer': 'Lo increíble de los tacos mexicanos es su diversidad regional',
            'concept': 'lo_adjetivo',
            'section': 'VI'
        }
    ],

    # Legacy format for concept study (preserved for backwards compatibility)
    'antepresente': [
        {
            'question': 'Ricardo ___ (aumentar) mucho de peso últimamente.',
            'type': 'fill',
            'answer': 'ha aumentado',
            'concept': 'antepresente'
        },
        {
            'question': 'No ___ (revisar-yo) mi correo electrónico hoy.',
            'type': 'fill',
            'answer': 'he revisado',
            'concept': 'antepresente'
        },
        {
            'question': 'Los estudiantes ya ___ (terminar) su proyecto final.',
            'type': 'fill',
            'answer': 'han terminado',
            'concept': 'antepresente'
        },
        {
            'question': 'María ___ (viajar) a muchos países este año.',
            'type': 'fill',
            'answer': 'ha viajado',
            'concept': 'antepresente'
        }
    ],
    'antecopreterito': [
        {
            'question': 'Rebeca ya ___ (nacer) cuando su mamá empezó a trabajar.',
            'type': 'fill',
            'answer': 'había nacido',
            'concept': 'antecopreterito'
        },
        {
            'question': 'Rebeca todavía no ___ (nacer) cuando su mamá empezó a trabajar.',
            'type': 'fill',
            'answer': 'había nacido',
            'concept': 'antecopreterito'
        },
        {
            'question': 'Los invitados ya ___ (llegar) cuando empezó la fiesta.',
            'type': 'fill',
            'answer': 'habían llegado',
            'concept': 'antecopreterito'
        },
        {
            'question': 'Cuando llegué a casa, mi familia ya ___ (cenar).',
            'type': 'fill',
            'answer': 'había cenado',
            'concept': 'antecopreterito'
        }
    ],
    'lo_adjetivo': [
        {
            'question': 'Lo bueno ___ esta empresa es que tienen buenas prestaciones.',
            'type': 'multiple_choice',
            'options': {'a': 'de', 'b': 'en', 'c': 'por', 'd': 'sobre'},
            'answer': 'a',
            'concept': 'lo_adjetivo'
        },
        {
            'question': 'Lo malo ___ vivir lejos es el tráfico.',
            'type': 'multiple_choice',
            'options': {'a': 'de', 'b': 'en', 'c': 'por', 'd': 'sobre'},
            'answer': 'a',
            'concept': 'lo_adjetivo'
        },
        {
            'question': 'Lo interesante ___ este curso es la mezcla cultural.',
            'type': 'multiple_choice',
            'options': {'a': 'de', 'b': 'en', 'c': 'por', 'd': 'sobre'},
            'answer': 'a',
            'concept': 'lo_adjetivo'
        },
        {
            'question': 'Lo difícil ___ aprender español es la gramática.',
            'type': 'multiple_choice',
            'options': {'a': 'de', 'b': 'en', 'c': 'por', 'd': 'sobre'},
            'answer': 'a',
            'concept': 'lo_adjetivo'
        }
    ],
    'subjuntivo_percepcion': [
        {
            'question': '*No veo que* los políticos ___ algo para cambiar las cosas.',
            'type': 'multiple_choice',
            'options': {'a': 'hagan', 'b': 'hacen', 'c': 'hicieron', 'd': 'harán'},
            'answer': 'a',
            'concept': 'subjuntivo_percepcion'
        },
        {
            'question': '*Veo que* Sofía ___ muy cansada.',
            'type': 'multiple_choice',
            'options': {'a': 'está', 'b': 'esté', 'c': 'estuviera', 'd': 'estará'},
            'answer': 'a',
            'concept': 'subjuntivo_percepcion'
        },
        {
            'question': '*No escucho que* los estudiantes ___ en clase.',
            'type': 'multiple_choice',
            'options': {'a': 'participan', 'b': 'participen', 'c': 'participaron', 'd': 'participarán'},
            'answer': 'b',
            'concept': 'subjuntivo_percepcion'
        }
    ],
    'subjuntivo_opinion': [
        {
            'question': 'Dudo que Roberto ___ temprano.',
            'type': 'multiple_choice',
            'options': {'a': 'llega', 'b': 'llegue', 'c': 'llegó', 'd': 'llegará'},
            'answer': 'b',
            'concept': 'subjuntivo_opinion'
        },
        {
            'question': 'Creo que ella ___ (tener) razón.',
            'type': 'fill',
            'answer': 'tiene',
            'concept': 'subjuntivo_opinion'
        },
        {
            'question': 'No creo que ella ___ razón.',
            'type': 'multiple_choice',
            'options': {'a': 'tiene', 'b': 'tenga', 'c': 'tuvo', 'd': 'tendrá'},
            'answer': 'b',
            'concept': 'subjuntivo_opinion'
        },
        {
            'question': 'No pienso que Xi ___ (comprar) churros en el Zócalo.',
            'type': 'fill',
            'answer': 'compre',
            'concept': 'subjuntivo_opinion'
        }
    ],
    'condicional': [
        {
            'question': 'Si tengo tiempo, ___ (tomar-yo) clases de inglés.',
            'type': 'fill',
            'answer': 'tomaré',
            'concept': 'condicional'
        },
        {
            'question': 'Si tuviera tiempo, ___ (tomar-yo) clases de inglés.',
            'type': 'fill',
            'answer': 'tomaría',
            'concept': 'condicional'
        },
        {
            'question': 'Si tuviera dinero, ___ (viajar) por todo México.',
            'type': 'fill',
            'answer': 'viajaría',
            'concept': 'condicional'
        },
        {
            'question': 'Si llueve mañana, no ___ (ir-nosotros) al Zócalo.',
            'type': 'fill',
            'answer': 'iremos',
            'concept': 'condicional'
        }
    ],
    'temporal_clauses': [
        {
            'question': 'Avísame cuando ___ (estar-tú) listo.',
            'type': 'fill',
            'answer': 'estés',
            'concept': 'temporal_clauses'
        },
        {
            'question': 'Cuando el presidente termine, la tasa ya ___ aumentado.',
            'type': 'multiple_choice',
            'options': {'a': 'habrá', 'b': 'habría', 'c': 'ha', 'd': 'hubiera'},
            'answer': 'a',
            'concept': 'temporal_clauses'
        },
        {
            'question': 'En cuanto ___ (llegar) a casa, te llamo.',
            'type': 'fill',
            'answer': 'llegue',
            'concept': 'temporal_clauses'
        },
        {
            'question': 'Tan pronto como ___ (terminar) el trabajo, vamos al cine.',
            'type': 'fill',
            'answer': 'termine',
            'concept': 'temporal_clauses'
        }
    ],
    'subjuntivo_necesidad': [
        {
            'question': 'Es importante que maestros y alumnos ___ a la junta.',
            'type': 'fill',
            'answer': 'asistan',
            'concept': 'subjuntivo_necesidad'
        },
        {
            'question': 'Era importante que maestros y alumnos ___ a la junta.',
            'type': 'fill',
            'answer': 'asistieran',
            'concept': 'subjuntivo_necesidad'
        },
        {
            'question': 'Necesitaba que ustedes ___ (llegar) temprano.',
            'type': 'fill',
            'answer': 'llegaran',
            'concept': 'subjuntivo_necesidad'
        },
        {
            'question': 'Ojalá que el dólar ___ (bajar) pronto.',
            'type': 'fill',
            'answer': 'baje',
            'concept': 'subjuntivo_necesidad'
        }
    ]
}

# Old template system kept for backwards compatibility
GRAMMAR_TEMPLATES = {
    'antepresente': [
        ("{person} ha {verb} {object} muchas veces.", "ha {verb}"),
        ("No he {verb} {food} en mi vida.", "he {verb}"),
        ("{person} ya ha {verb} en {place}.", "ha {verb}")
    ],
    'antecopreterito': [
        ("{person} ya había {verb} cuando {other} llegó.", "había {verb}"),
        ("Todavía no había {verb} cuando empezó la fiesta.", "había {verb}"),
        ("Mi {family} ya había {verb} {food} antes de ir a {place}.", "había {verb}")
    ],
    'lo_adjetivo': [
        ("Lo {adj} de {place} es {complement}.", "de"),
        ("Lo {adj} de comer {food} es {complement}.", "de"),
        ("Lo más {adj} de México es {complement}.", "de")
    ],
    'subjuntivo_percepcion': [
        ("Veo que {person} {verb} mucho.", "Veo que"),
        ("No veo que los políticos {verb_subj} nada.", "No veo que"),
        ("Escucho que {person} {verb} {music}.", "Escucho que")
    ],
    'subjuntivo_opinion': [
        ("Creo que {person} {verb} razón.", "Creo que"),
        ("No creo que {person} {verb_subj} a tiempo.", "No creo que"),
        ("Dudo que {person} {verb_subj} {food}.", "Dudo que")
    ],
    'condicional': [
        ("Si tuviera dinero, {conditional} {activity}.", "{conditional}"),
        ("Si fuera a {place}, {conditional} {food}.", "{conditional}"),
        ("Si {person} viniera, {conditional} muy contentos.", "{conditional}")
    ],
    'temporal_clauses': [
        ("Avísame cuando {subj_verb} listo.", "{subj_verb}"),
        ("En cuanto {subj_verb} el metro, vamos a {place}.", "{subj_verb}"),
        ("Tan pronto como {subj_verb} de trabajar, comemos {food}.", "{subj_verb}")
    ]
}

# Vocabulary sets for templates
VOCAB_SETS = {
    'verbs': ['comer', 'visitar', 'probar', 'conocer', 'estudiar', 'trabajar'],
    'verbs_subj': ['coma', 'visite', 'pruebe', 'conozca', 'estudie', 'trabaje'],
    'verbs_past': ['comido', 'visitado', 'probado', 'conocido', 'estudiado', 'trabajado'],
    'adjectives': ['bueno', 'malo', 'difícil', 'fácil', 'interesante', 'aburrido'],
    'family': ['mamá', 'papá', 'abuela', 'tío', 'prima', 'hermano'],
    'music': ['mariachi', 'rancheras', 'banda', 'cumbia'],
    'conditionals': ['compraría', 'iría', 'comería', 'visitaría', 'estudiaría'],
    'complements': ['la comida', 'la música', 'la gente', 'el ambiente', 'la cultura']
}

class WebQuestionGenerator:
    def __init__(self):
        self.used_questions = set()
    
    def generate_question(self, concept=None):
        """Generate a new question based on grammar concept or random"""
        if concept and concept in EXAM_QUESTIONS:
            available_questions = [q for q in EXAM_QUESTIONS[concept] 
                                 if id(q) not in self.used_questions]
        else:
            # Select from all available questions
            all_questions = []
            for concept_questions in EXAM_QUESTIONS.values():
                all_questions.extend(concept_questions)
            available_questions = [q for q in all_questions 
                                 if id(q) not in self.used_questions]
        
        if not available_questions:
            # Reset if we've used all questions
            self.used_questions.clear()
            if concept and concept in EXAM_QUESTIONS:
                available_questions = EXAM_QUESTIONS[concept]
            else:
                all_questions = []
                for concept_questions in EXAM_QUESTIONS.values():
                    all_questions.extend(concept_questions)
                available_questions = all_questions
        
        if not available_questions:
            return None
            
        question = random.choice(available_questions)
        self.used_questions.add(id(question))
        
        # Return a copy of the question to avoid modifying the original
        return {
            'question': question['question'],
            'answer': question['answer'],
            'type': question['type'],
            'concept': question['concept'],
            'options': question.get('options', {}),
            'section': question.get('section', 'I'),
            'text': question.get('text', '')
        }
    
    def generate_section_questions(self, section_name, num_questions=None):
        """Generate questions for a specific exam section"""
        if section_name not in EXAM_QUESTIONS:
            return []
        
        available_questions = EXAM_QUESTIONS[section_name][:]
        if num_questions is None:
            num_questions = len(available_questions)
        
        # Shuffle and take the requested number
        random.shuffle(available_questions)
        selected_questions = available_questions[:num_questions]
        
        return [
            {
                'question': q['question'],
                'answer': q['answer'],
                'type': q['type'],
                'concept': q['concept'],
                'options': q.get('options', {}),
                'section': q.get('section', 'I'),
                'text': q.get('text', '')
            }
            for q in selected_questions
        ]
    
    def get_all_concepts(self):
        """Get list of all available concepts (legacy format)"""
        return [key for key in EXAM_QUESTIONS.keys() if not key.startswith('section_')]
    
    def get_all_sections(self):
        """Get list of all exam sections"""
        return [key for key in EXAM_QUESTIONS.keys() if key.startswith('section_')]
    
    def generate_full_exam(self):
        """Generate a complete exam with all sections according to official structure"""
        exam_sections = []
        
        for section_key in ['section_I', 'section_II', 'section_III', 'section_IV', 'section_VI']:
            if section_key in EXAM_QUESTIONS:
                section_info = EXAM_SECTIONS.get(section_key.split('_')[1], {})
                questions = self.generate_section_questions(section_key, section_info.get('total_questions'))
                
                exam_sections.append({
                    'section_id': section_key.split('_')[1],
                    'section_info': section_info,
                    'questions': questions
                })
        
        return exam_sections
    
    def generate_exam_section(self, num_questions=15):
        """Generate a mixed section for practice (legacy support)"""
        questions = []
        all_section_questions = []
        
        # Collect questions from all sections (except audio)
        for section_key in ['section_I', 'section_II', 'section_III', 'section_VI']:
            if section_key in EXAM_QUESTIONS:
                all_section_questions.extend(EXAM_QUESTIONS[section_key])
        
        # Shuffle and select
        random.shuffle(all_section_questions)
        selected = all_section_questions[:num_questions]
        
        for q in selected:
            questions.append({
                'question': q['question'],
                'answer': q['answer'],
                'type': q['type'],
                'concept': q['concept'],
                'options': q.get('options', {}),
                'section': q.get('section', 'I'),
                'text': q.get('text', '')
            })
        
        return questions

# Initialize generator
generator = WebQuestionGenerator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exam')
def exam():
    """Start a new sectioned exam"""
    # Generate full exam with all sections
    exam_sections = generator.generate_full_exam()
    
    session['exam_sections'] = exam_sections
    session['current_section'] = 0
    session['current_page'] = 0
    session['score'] = 0
    session['answers'] = []
    session['individual_answers'] = {}
    session['individual_score'] = 0
    session['start_time'] = datetime.now().isoformat()
    
    # Start with first section
    return redirect('/exam_section/0/0')

@app.route('/exam_section/<int:section_idx>/<int:page_idx>')
def exam_section(section_idx, page_idx):
    """Display a specific section and page of the exam"""
    exam_sections = session.get('exam_sections', [])
    
    if section_idx >= len(exam_sections):
        return redirect('/exam_complete')
    
    current_section = exam_sections[section_idx]
    section_info = current_section['section_info']
    questions = current_section['questions']
    
    # Calculate pagination
    questions_per_page = section_info.get('questions_per_page', 5)
    total_pages = (len(questions) + questions_per_page - 1) // questions_per_page
    
    if page_idx >= total_pages:
        # Move to next section
        if section_idx + 1 < len(exam_sections):
            return redirect(f'/exam_section/{section_idx + 1}/0')
        else:
            return redirect('/exam_complete')
    
    # Get questions for current page
    start_idx = page_idx * questions_per_page
    end_idx = min(start_idx + questions_per_page, len(questions))
    current_questions = questions[start_idx:end_idx]
    
    # Calculate global question indices for answer tracking
    global_start_idx = 0
    for i in range(section_idx):
        global_start_idx += len(exam_sections[i]['questions'])
    global_start_idx += start_idx
    
    return render_template('exam_section.html', 
                         questions=current_questions,
                         section_info=section_info,
                         section_id=current_section['section_id'],
                         section_idx=section_idx,
                         page_idx=page_idx,
                         total_pages=total_pages,
                         total_sections=len(exam_sections),
                         start_question_idx=global_start_idx,
                         answered_questions=session.get('individual_answers', {}))

@app.route('/next_section')
def next_section():
    """Navigate to next exam section"""
    exam_sections = session.get('exam_sections', [])
    current_section = session.get('current_section', 0)
    
    if current_section + 1 < len(exam_sections):
        return redirect(f'/exam_section/{current_section + 1}/0')
    else:
        return redirect('/exam_complete')

@app.route('/previous_section')
def previous_section():
    """Navigate to previous exam section"""
    current_section = session.get('current_section', 0)
    
    if current_section > 0:
        return redirect(f'/exam_section/{current_section - 1}/0')
    else:
        return redirect('/exam')

@app.route('/submit_question', methods=['POST'])
def submit_question():
    """Handle individual question submissions for instant feedback"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'})
    
    question_index = data.get('question_index')
    user_answer = data.get('answer', '').strip()
    
    # Get all questions from all sections
    exam_sections = session.get('exam_sections', [])
    all_questions = []
    for section in exam_sections:
        all_questions.extend(section['questions'])
    
    if question_index is None or question_index >= len(all_questions):
        return jsonify({'error': 'Invalid question index'})
    
    question = all_questions[question_index]
    correct_answer = question['answer']
    
    # Check if answer is correct
    if question['type'] == 'multiple_choice':
        is_correct = user_answer.lower() == correct_answer.lower()
    elif question['type'] in ['essay', 'short_answer']:
        # For essays and short answers, we'll accept any non-empty answer as "attempted"
        is_correct = len(user_answer.strip()) > 0
        correct_answer = "Respuesta evaluada manualmente"
    else:
        is_correct = strip(user_answer) == strip(correct_answer)
    
    # Initialize session data if needed
    if 'individual_answers' not in session:
        session['individual_answers'] = {}
    if 'individual_score' not in session:
        session['individual_score'] = 0
    
    # Store/update individual answer
    previous_answer = session['individual_answers'].get(str(question_index))
    session['individual_answers'][str(question_index)] = {
        'question': question['question'],
        'user_answer': user_answer,
        'correct_answer': correct_answer,
        'is_correct': is_correct,
        'concept': question['concept'],
        'section': question.get('section', 'I')
    }
    
    # Update score (subtract previous if it was correct, add new if correct)
    if previous_answer and previous_answer['is_correct']:
        session['individual_score'] -= 1
    if is_correct:
        session['individual_score'] += 1
    
    response = {
        'is_correct': is_correct,
        'correct_answer': correct_answer,
        'explanation': get_concept_explanation(question['concept']),
        'total_score': session['individual_score'],
        'total_answered': len(session['individual_answers']),
        'total_questions': len(all_questions),
        'question_type': question['type']
    }
    
    return jsonify(response)

# Legacy route removed - replaced with exam_section

@app.route('/exam_complete')
def exam_complete():
    """Show final results when user manually finishes the exam"""
    individual_answers = session.get('individual_answers', {})
    exam_sections = session.get('exam_sections', [])
    
    # Collect all questions from all sections
    all_questions = []
    for section in exam_sections:
        all_questions.extend(section['questions'])
    
    # Convert individual answers to the format expected by results template
    answers = []
    for i, question in enumerate(all_questions):
        answer_data = individual_answers.get(str(i))
        if answer_data:
            answers.append(answer_data)
        else:
            # Question was not answered
            answers.append({
                'question': question['question'],
                'user_answer': '',
                'correct_answer': question['answer'],
                'is_correct': False,
                'concept': question['concept'],
                'section': question.get('section', 'I')
            })
    
    session['answers'] = answers
    session['score'] = session.get('individual_score', 0)
    
    return redirect('/results')

@app.route('/results')
def results():
    answers = session.get('answers', [])
    score = session.get('score', 0)
    total = len(answers)
    
    if total == 0:
        return redirect('/')
    
    percentage = round((score / total) * 100, 1)
    
    return render_template('results.html', 
                         answers=answers, 
                         score=score, 
                         total=total, 
                         percentage=percentage)

@app.route('/generate_new')
def generate_new():
    """Generate new questions via AJAX"""
    questions = generator.generate_exam_section(15)
    return jsonify({'questions': questions})

# Individual Grammar Concept Routes
@app.route('/concept/<concept_name>')
def concept_study(concept_name):
    """Study page for individual grammar concepts"""
    if concept_name not in GRAMMAR_TEMPLATES:
        return redirect('/')
    
    # Generate 5 practice questions for this concept
    practice_questions = []
    for i in range(5):
        q_type = 'multiple_choice' if i % 2 == 0 else 'fill'
        question = generator.generate_question(concept_name)
        if question:
            practice_questions.append(question)
    
    # Get concept information
    concept_info = get_concept_info(concept_name)
    
    return render_template('concept_study.html', 
                         concept_name=concept_name,
                         concept_info=concept_info,
                         questions=practice_questions)

@app.route('/concept/<concept_name>/practice', methods=['POST'])
def concept_practice(concept_name):
    """Handle practice question submissions for individual concepts"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data received'})
    
    user_answer = data.get('answer', '').strip()
    question_data = data.get('question')
    
    if not question_data:
        return jsonify({'error': 'No question data'})
    
    correct_answer = question_data['answer']
    
    # Check if answer is correct
    if question_data['type'] == 'multiple_choice':
        is_correct = user_answer.lower() == correct_answer.lower()
    else:
        is_correct = strip(user_answer) == strip(correct_answer)
    
    # Generate a new practice question
    q_type = 'multiple_choice' if random.choice([True, False]) else 'fill'
    new_question = generator.generate_question(concept_name)
    
    return jsonify({
        'is_correct': is_correct,
        'correct_answer': correct_answer,
        'explanation': get_concept_explanation(concept_name),
        'new_question': new_question
    })

def get_concept_info(concept_name):
    """Get detailed information about a grammar concept"""
    concept_details = {
        'antepresente': {
            'title': 'Antepresente (Pretérito Perfecto)',
            'description': 'Se usa para expresar acciones pasadas que tienen relevancia en el presente.',
            'formula': 'haber (presente) + participio pasado',
            'examples': [
                'He comido tacos muchas veces.',
                'Lupita ha visitado Xochimilco.',
                '¿Has probado el pozole?'
            ],
            'tips': 'Recuerda que se usa cuando la acción pasada afecta el presente.'
        },
        'antecopreterito': {
            'title': 'Antecopretérito (Pluscuamperfecto)',
            'description': 'Expresa una acción pasada anterior a otra acción también pasada.',
            'formula': 'haber (imperfecto) + participio pasado',
            'examples': [
                'Paco ya había llegado cuando empezó la fiesta.',
                'Habíamos comido antes de ir al Zócalo.',
                'Gaby había estudiado mucho para el examen.'
            ],
            'tips': 'Se usa para mostrar que una acción ocurrió antes que otra en el pasado.'
        },
        'lo_adjetivo': {
            'title': 'Lo + Adjetivo',
            'description': 'Construcción para expresar la cualidad abstracta de algo.',
            'formula': 'Lo + adjetivo + de + sustantivo/lugar',
            'examples': [
                'Lo bueno de México es la comida.',
                'Lo difícil de aprender chino es la escritura.',
                'Lo bonito de Xochimilco son las trajineras.'
            ],
            'tips': 'Siempre usa "de" después del adjetivo.'
        },
        'subjuntivo_percepcion': {
            'title': 'Subjuntivo de Percepción',
            'description': 'Se usa subjuntivo en oraciones negativas con verbos de percepción.',
            'formula': 'No + verbo percepción + que + subjuntivo',
            'examples': [
                'Veo que Lupita come tacos. (indicativo)',
                'No veo que Lupita coma tacos. (subjuntivo)',
                'Escucho que hay mariachi en la plaza.'
            ],
            'tips': 'Afirmativo = indicativo, Negativo = subjuntivo.'
        },
        'subjuntivo_opinion': {
            'title': 'Subjuntivo de Opinión',
            'description': 'Se usa subjuntivo en oraciones negativas con verbos de opinión.',
            'formula': 'No + verbo opinión + que + subjuntivo',
            'examples': [
                'Creo que Paco viene. (indicativo)',
                'No creo que Paco venga. (subjuntivo)',
                'Dudo que llueva en el desierto.'
            ],
            'tips': 'Creer afirmativo = indicativo, Creer negativo = subjuntivo.'
        },
        'condicional': {
            'title': 'Condicional (Si + Imperfecto Subjuntivo)',
            'description': 'Expresa situaciones hipotéticas o irreales.',
            'formula': 'Si + imperfecto subjuntivo + condicional',
            'examples': [
                'Si tuviera dinero, compraría una casa.',
                'Si fuera a México, comería pozole.',
                'Si Lupita viniera, estaríamos felices.'
            ],
            'tips': 'Situaciones hipotéticas o poco probables.'
        },
        'temporal_clauses': {
            'title': 'Cláusulas Temporales',
            'description': 'Se usa subjuntivo cuando la acción es futura o hipotética.',
            'formula': 'cuando/en cuanto/tan pronto como + subjuntivo (futuro)',
            'examples': [
                'Cuando llegues, empezaremos.',
                'En cuanto termine, te llamo.',
                'Tan pronto como salga el sol, partimos.'
            ],
            'tips': 'Presente = indicativo, Futuro = subjuntivo.'
        }
    }
    
    return concept_details.get(concept_name, {
        'title': concept_name.replace('_', ' ').title(),
        'description': 'Concepto de gramática española.',
        'examples': [],
        'tips': 'Practica con los ejemplos.'
    })

def get_concept_explanation(concept_name):
    """Get explanation for correct/incorrect answers"""
    explanations = {
        'antepresente': 'El antepresente (pretérito perfecto) conecta acciones pasadas con el presente.',
        'antecopreterito': 'El antecopretérito (pluscuamperfecto) muestra una acción pasada anterior a otra pasada.',
        'antefuturo': 'El antefuturo (futuro perfecto) expresa una acción que estará completada en el futuro.',
        'lo_adjetivo': 'La construcción "lo + adjetivo + de" expresa cualidades abstractas.',
        'subjuntivo_percepcion': 'Los verbos de percepción negativos requieren subjuntivo.',
        'subjuntivo_opinion': 'Los verbos de opinión negativos requieren subjuntivo.',
        'subjuntivo_necesidad': 'Las expresiones de necesidad, duda y deseo requieren subjuntivo.',
        'subjuntivo_emocion': 'Las expresiones de emoción requieren subjuntivo.',
        'subjuntivo_deseo': 'Las expresiones de deseo (ojalá, esperar) requieren subjuntivo.',
        'condicional': 'Las oraciones condicionales irreales usan subjuntivo + condicional.',
        'condicional_real': 'Las oraciones condicionales reales usan indicativo + futuro.',
        'temporal_clauses': 'Las cláusulas temporales futuras requieren subjuntivo.',
        'tiempos_pasados': 'El pretérito e imperfecto expresan diferentes aspectos del pasado.',
        'tiempos_compuestos': 'Los tiempos compuestos usan auxiliar haber + participio.',
        'pronombres_relativos': 'Los pronombres relativos (que, quien, el cual) conectan oraciones.',
        'oraciones_relativas': 'Las oraciones relativas especifican o explican información.',
        'discurso_indirecto': 'El discurso indirecto reporta las palabras de otra persona.',
        'infinitivo_vs_subjuntivo': 'Usa infinitivo cuando el sujeto es el mismo, subjuntivo cuando cambia.',
        'participios_irregulares': 'Algunos participios tienen formas irregulares (abierto, escrito, hecho).',
        'comprension_lectora': 'Identifica ideas principales y detalles específicos en el texto.',
        'comprension_auditiva': 'Enfócate en palabras clave y contexto en el audio.',
        'produccion_escrita': 'Organiza ideas coherentemente usando vocabulario específico y gramática correcta.',
        'situaciones_comunicativas': 'Adapta tu respuesta al contexto y usa estructuras apropiadas.'
    }
    return explanations.get(concept_name, 'Revisa las reglas gramaticales específicas.')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
