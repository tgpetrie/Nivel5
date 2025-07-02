
#!/usr/bin/env python3
"""
Interactive Final Exam – Español 5  (MX‑USA‑Rusia‑China Edition)
----------------------------------------------------------------
• Runs in the terminal.
• Section I (30 Q) auto‑grades.
• Sections II & VI capture free responses for teacher review.
• Sections III, IV, V show instructions and pause.
"""

import textwrap, unicodedata, json, os, sys

ACCENTS = {c: None for c in range(0x300, 0x370)}
strip = lambda s: unicodedata.normalize("NFD", s).translate(ACCENTS).lower()

SECTION_I = [
    # (prompt, {'a':'', 'b':'', ...} OR None, correct)
    ("Lo sorprendente ___ la cumbia rusa es que la bailan en la Plaza Roja.",
     {'a': 'de', 'b': 'en', 'c': 'por', 'd': 'sobre'}, 'a'),
    ("AMLO ha comido mole mil veces, pero todavía no ___ salsa tártara.", None, "ha probado"),
    ("No creo que los pingüinos de Alaska ___ votar en CDMX.",
     {'a':'pueden','b':'puedan','c':'pudieron','d':'podrán'}, 'b'),
    ("Xi ___ (visitar) la Basílica cuando Putin aterrizó en Santa Lucía.", None, "había visitado"),
    ("Avísame tan pronto como ___ (terminar‑tú) tu visa rusa.", None, "termines"),
    ("Lo bueno ___ vivir en Moscú es el ballet.", 
     {'a': 'de', 'b': 'por', 'c': 'en', 'd': 'sobre'}, 'a'),
    ("Dudo que los mariachis ___ tocar balalaikas.",
     {'a': 'saben', 'b': 'sepan', 'c': 'sabían', 'd': 'sabrán'}, 'b'),
    ("Si tuviéramos más yuan, ___ (comprar) jade auténtico.", None, "compraríamos"),
    ("Para 2030, la NASA ___ (descubrir) vida en Marte.",
     {'a': 'descubrirá', 'b': 'habrá descubierto', 'c': 'descubriría', 'd': 'hubiera descubierto'}, 'b'),
    ("Me alegra que Putin ___ (aprender) español en Guadalajara.", None, "aprenda"),
]

HEADER = "¡Muchas gracias, Luis!"
FOOTER = "Tom Petrie  •  Guía de Estudio y Práctica  •  UNAM Polanco Nivel 5 2025"

def pause():
    input("\\nPresiona Enter para continuar…\\n")

def run_section_I():
    print("\\n—— SECCIÓN I – Gramática objetiva ——\\n")
    score = 0
    for idx, (prompt, opts, correct) in enumerate(SECTION_I, 1):
        print(f"{idx}. {prompt}")
        if opts:
            for k,v in opts.items(): print(f"   {k}) {v}")
            ans = input("→ ").strip().lower()
            ok = ans == correct
        else:
            ans = input("→ ").strip()
            ok = strip(ans) == strip(correct)
        if ok:
            print("   ✅ Correcto\\n"); score += 1
        else:
            print(f"   ❌ Incorrecto. Respuesta: {correct}\\n")
    print(f"Puntaje Sección I: {score}/{len(SECTION_I)}")
    return score

def run_section_free(title, prompts):
    print(f"\\n—— {title} ——\\n")
    answers = {}
    for p in prompts:
        ans = input(p + "\\n→ ")
        answers[p] = ans
    pause()
    return answers

def main():
    os.system('cls' if os.name=='nt' else 'clear')
    print(f"{HEADER.center(70)}\\n")
    print("Examen Final – Español 5   (MX‑USA‑Rusia‑China)".center(70))
    print("Duración sugerida: 90 min   •   Valor: 100 pts".center(70))
    pause()

    total = run_section_I()

    # Sections II & VI – capture only
    sec2 = run_section_free("SECCIÓN II – Transformaciones",
        ["Biden: «No visitaré el Zócalo el lunes».  → ",
         "Ya habían inaugurado el Tren Maya.  → ",
         "Si China reduce tarifas, México exportará más aguacate.  → "])

    sec3_notice = textwrap.fill(
        "SECCIÓN III – Lectura: abre tu cuadernillo, lee el texto sobre la cumbre "
        "en Cancún y responde las preguntas 21‑30 en la hoja aparte.", 70)
    print("\\n"+sec3_notice); pause()

    sec4_notice = textwrap.fill(
        "SECCIÓN IV – Producción escrita: redacta 130‑150 palabras según la guía. "
        "Escribe en tu procesador o a mano y entrégalo al profesor.", 70)
    print("\\n"+sec4_notice); pause()

    sec5_notice = textwrap.fill(
        "SECCIÓN V – Comprensión auditiva: el profesor reproducirá el audio. "
        "Marca tus respuestas en la hoja.", 70)
    print("\\n"+sec5_notice); pause()

    sec6 = run_section_free("SECCIÓN VI – Situaciones comunicativas",
        ["Sugerir a tu amigo gringo que pruebe mezcal.",
         "Expresar emoción (impf. subj.) sobre balalaikas.",
         "Frase con tan pronto como + subj. para visitar la Muralla.",
         "Oración con relativo y «confiar en».",
         "Oración especificativa sobre una app.",
         "Lo + adj + de sobre tacos o dumplings."])

    # summary
    print("\\nEXAMEN COMPLETADO.")
    print(f"Puntaje automático (Sección I): {total}/{len(SECTION_I)}")
    print("Secciones II y VI guardadas para revisión manual.")
    pause()

    # Optionally save free‑response to file
    if input("¿Guardar respuestas abiertas en JSON? (s/n) ").lower().startswith('s'):
        with open('respuestas_libres.json','w',encoding='utf-8') as f:
            json.dump({'II':sec2,'VI':sec6}, f, ensure_ascii=False, indent=2)
        print("Archivo respuestas_libres.json guardado.")

    print(f"\\n{FOOTER.center(70)}\\n")

if __name__ == '__main__':
    main()
