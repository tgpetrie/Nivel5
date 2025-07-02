#!/usr/bin/env python3
"""
Interactive Final Exam – Español 5  (Dynamic Question Generator)
----------------------------------------------------------------
• Generates new questions from Mexican Spanish grammar concepts
• Auto-grades objective questions
• Colloquial Mexican Spanish with proper grammar
"""

import textwrap, unicodedata, json, os, sys, random

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

# Grammar concept templates for question generation
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

class QuestionGenerator:
    def __init__(self):
        self.used_combinations = set()
    
    def generate_question(self, concept, question_type='fill'):
        """Generate a new question based on grammar concept"""
        if concept not in GRAMMAR_TEMPLATES:
            return None
        
        template_data = random.choice(GRAMMAR_TEMPLATES[concept])
        template, answer_pattern = template_data
        
        # Fill template with Mexican vocabulary
        filled_template = self._fill_template(template)
        answer = self._extract_answer(filled_template, answer_pattern)
        
        if question_type == 'multiple_choice':
            return self._create_multiple_choice(filled_template, answer, concept)
        else:
            return (filled_template, None, answer)
    
    def _fill_template(self, template):
        """Fill template with random Mexican vocabulary"""
        replacements = {}
        
        # Choose random values for each placeholder
        for key in ['person', 'other']:
            if f'{{{key}}}' in template:
                replacements[key] = random.choice(MEXICAN_VOCAB['people'])
        
        for key in ['place']:
            if f'{{{key}}}' in template:
                replacements[key] = random.choice(MEXICAN_VOCAB['places'])
        
        for key in ['food']:
            if f'{{{key}}}' in template:
                replacements[key] = random.choice(MEXICAN_VOCAB['food'])
        
        for key in ['activity']:
            if f'{{{key}}}' in template:
                replacements[key] = random.choice(MEXICAN_VOCAB['activities'])
        
        for key in ['object']:
            if f'{{{key}}}' in template:
                replacements[key] = random.choice(MEXICAN_VOCAB['objects'])
        
        # Grammar-specific replacements
        for vocab_key, vocab_list in VOCAB_SETS.items():
            if f'{{{vocab_key}}}' in template:
                replacements[vocab_key] = random.choice(vocab_list)
        
        # Apply replacements
        filled = template
        for key, value in replacements.items():
            filled = filled.replace(f'{{{key}}}', value)
        
        return filled
    
    def _extract_answer(self, filled_template, answer_pattern):
        """Extract the correct answer from the pattern"""
        # Simple pattern matching for answer extraction
        if 'ha {verb}' in answer_pattern:
            return random.choice(['ha comido', 'ha visitado', 'ha probado', 'ha estudiado'])
        elif 'había {verb}' in answer_pattern:
            return random.choice(['había comido', 'había visitado', 'había llegado', 'había estudiado'])
        elif answer_pattern == 'de':
            return 'de'
        elif '{conditional}' in answer_pattern:
            return random.choice(VOCAB_SETS['conditionals'])
        elif '{subj_verb}' in answer_pattern:
            return random.choice(['llegues', 'termines', 'estés', 'vengas'])
        else:
            return answer_pattern
    
    def _create_multiple_choice(self, question, correct_answer, concept):
        """Create multiple choice options"""
        options = {'a': correct_answer}
        
        # Generate distractors based on concept
        if concept == 'lo_adjetivo':
            distractors = ['en', 'por', 'con']
        elif concept in ['subjuntivo_percepcion', 'subjuntivo_opinion']:
            distractors = ['viene', 'vino', 'vendrá']
        elif concept == 'condicional':
            distractors = ['compraré', 'compro', 'he comprado']
        else:
            distractors = ['opción1', 'opción2', 'opción3']
        
        for i, distractor in enumerate(distractors[:3]):
            options[chr(98 + i)] = distractor  # b, c, d
        
        return (question, options, 'a')
    
    def generate_exam_section(self, num_questions=10):
        """Generate a complete exam section"""
        concepts = list(GRAMMAR_TEMPLATES.keys())
        questions = []
        
        for i in range(num_questions):
            concept = random.choice(concepts)
            q_type = 'multiple_choice' if i % 3 == 0 else 'fill'
            question = self.generate_question(concept, q_type)
            if question:
                questions.append(question)
        
        return questions

# Initialize generator
generator = QuestionGenerator()

# Generate dynamic questions for Section I
SECTION_I = generator.generate_exam_section(15)

HEADER = "¡Órale! Examen de Español Mexicano"
FOOTER = "Tom Petrie  •  Español Nivel 5  •  UNAM Polanco 2025"

def pause():
    input("\nPresiona Enter para continuar…\n")

def run_section_I():
    print("\n—— SECCIÓN I – Gramática del Español Mexicano ——\n")
    score = 0
    for idx, (prompt, opts, correct) in enumerate(SECTION_I, 1):
        print(f"{idx}. {prompt}")
        if opts:
            for k,v in opts.items(): 
                print(f"   {k}) {v}")
            ans = input("→ ").strip().lower()
            ok = ans == correct
        else:
            ans = input("→ ").strip()
            ok = strip(ans) == strip(correct)
        if ok:
            print("   ✅ ¡Órale! Correcto\n"); score += 1
        else:
            print(f"   ❌ No está bien. Respuesta: {correct}\n")
    print(f"Puntaje Sección I: {score}/{len(SECTION_I)}")
    return score

def run_section_free(title, prompts):
    print(f"\n—— {title} ——\n")
    answers = {}
    for p in prompts:
        ans = input(p + "\n→ ")
        answers[p] = ans
    pause()
    return answers

def regenerate_questions():
    """Regenerate all questions with new vocabulary"""
    global SECTION_I
    print("\n🔄 Generando nuevas preguntas con vocabulario mexicano...\n")
    SECTION_I = generator.generate_exam_section(15)
    print("✅ ¡Listo! Nuevas preguntas generadas.\n")
    pause()

def main():
    os.system('cls' if os.name=='nt' else 'clear')
    print(f"{HEADER.center(70)}\n")
    print("Examen Final – Español Mexicano Nivel 5".center(70))
    print("Duración sugerida: 90 min   •   Valor: 100 pts".center(70))
    print("(Preguntas generadas dinámicamente)".center(70))
    
    while True:
        print("\n¿Qué quieres hacer?")
        print("1. Tomar examen")
        print("2. Generar nuevas preguntas")
        print("3. Salir")
        
        choice = input("\nElige opción (1-3): ").strip()
        
        if choice == '1':
            pause()
            total = run_section_I()
            
            # Mexican-themed free response sections
            sec2 = run_section_free("SECCIÓN II – Transformaciones Mexicanas",
                ["AMLO: «Voy a inaugurar el Tren Maya mañana».  → (discurso indirecto)",
                 "Ya habían comido pozole cuando llegamos.  → (usar 'todavía no')",
                 "Si tuviera tiempo, visitaría Teotihuacán.  → (condicional real)"])
            
            sec6 = run_section_free("SECCIÓN VI – Situaciones Comunicativas Mexicanas",
                ["Sugerir a tu amigo que pruebe tacos al pastor.",
                 "Expresar emoción sobre ver mariachis en Garibaldi.",
                 "Frase con 'tan pronto como' para ir al Zócalo.",
                 "Oración con 'confiar en' sobre un taquero.",
                 "Lo + adjetivo + de sobre vivir en CDMX."])
            
            print("\n¡EXAMEN COMPLETADO!")
            print(f"Puntaje automático: {total}/{len(SECTION_I)}")
            
            # Save responses
            if input("¿Guardar respuestas en JSON? (s/n) ").lower().startswith('s'):
                with open('respuestas_mexicanas.json','w',encoding='utf-8') as f:
                    json.dump({'Sección_II':sec2,'Sección_VI':sec6}, f, ensure_ascii=False, indent=2)
                print("Archivo 'respuestas_mexicanas.json' guardado.")
            
            print(f"\n{FOOTER.center(70)}\n")
            break
            
        elif choice == '2':
            regenerate_questions()
            
        elif choice == '3':
            print("\n¡Hasta luego! 🇲🇽")
            break
            
        else:
            print("\nOpción no válida. Intenta de nuevo.")

if __name__ == '__main__':
    main()
