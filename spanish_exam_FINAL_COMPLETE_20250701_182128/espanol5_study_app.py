
#!/usr/bin/env python3
'''
Español 5 – Interactive Study Guide
-----------------------------------
• Stores questions locally in SQLite.
• Can import new questions from a remote JSON feed (optional).
• Randomises each quiz session.
'''

import sqlite3, random, json, os, requests, sys
from pathlib import Path

DB_PATH = Path(__file__).with_suffix('.db')
REMOTE_JSON_URL = 'https://example.com/espanol5_questions.json'  # <-- replace with real endpoint

def init_db(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS questions (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   qtype TEXT NOT NULL,               -- 'mc' or 'fill'
                   question TEXT NOT NULL,
                   option_a TEXT, option_b TEXT,
                   option_c TEXT, option_d TEXT,
                   correct TEXT NOT NULL,
                   explanation TEXT
                 )''')
    conn.commit()

def seed_sample(conn):
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM questions')
    if c.fetchone()[0]:
        return  # already seeded
    samples = [
        ('mc', 'Lo sorprendente ___ este proyecto es la rapidez de los resultados.',
         'de', 'en', 'por', 'sobre', 'a', 'La locución fija es “lo + adj. + de”.'),
        ('fill', 'Rebeca ya ___ (nacer) cuando su madre empezó a trabajar.', None, None, None, None,
         'había nacido', 'Pluscuamperfecto porque es un pasado anterior a otro pasado.'),
        ('mc', 'Dudo que los políticos ___ algo para cambiar la situación.',
         'hacen', 'harán', 'hagan', 'hicieron', 'c', 'Subjuntivo por la duda.'),
        ('fill', 'Avísame tan pronto como ___ (estar‑tú) listo.', None, None, None, None,
         'estés', 'Subjuntivo porque la acción está en el futuro.'),
        ('mc', 'Cuando el director termine su mandato, la tasa de desempleo ya ___ aumentado.',
         'habrá', 'habría', 'ha', 'hubiera', 'a', 'Futuro perfecto (antefuturo).'),
    ]
    for row in samples:
        c.execute('''INSERT INTO questions (qtype,question,option_a,option_b,
                     option_c,option_d,correct,explanation)
                     VALUES (?,?,?,?,?,?,?,?)''', row)
    conn.commit()

def fetch_remote(conn):
    try:
        print('🔄  Intentando descargar preguntas nuevas...')
        r = requests.get(REMOTE_JSON_URL, timeout=5)
        r.raise_for_status()
        data = r.json()  # expect list of dicts with same keys
        c = conn.cursor()
        added = 0
        for q in data:
            # simple dedup by question text
            c.execute('SELECT 1 FROM questions WHERE question=?', (q['question'],))
            if not c.fetchone():
                c.execute('''INSERT INTO questions (qtype,question,option_a,option_b,
                             option_c,option_d,correct,explanation)
                             VALUES (?,?,?,?,?,?,?,?)''',
                          (q['qtype'], q['question'], q.get('option_a'),
                           q.get('option_b'), q.get('option_c'), q.get('option_d'),
                           q['correct'], q.get('explanation')))
                added += 1
        conn.commit()
        print(f'✅  Importadas {added} preguntas nuevas.')
    except Exception as e:
        print(f'⚠️  No se pudo actualizar desde la web ({e}). Usando banco local.')

def get_random_questions(conn, n=10):
    c = conn.cursor()
    c.execute('SELECT * FROM questions ORDER BY RANDOM() LIMIT ?', (n,))
    return c.fetchall()

def run_quiz(conn):
    print('\\n=== Iniciando quiz ===')
    rows = get_random_questions(conn)
    score = 0
    for idx, row in enumerate(rows, 1):
        qtype, question = row[1], row[2]
        if qtype == 'mc':
            opts = {'a': row[3], 'b': row[4], 'c': row[5], 'd': row[6]}
            print(f'\\n{idx}. {question}')
            for label, text in opts.items():
                print(f'  {label}) {text}')
            ans = input('Tu respuesta: ').strip().lower()
            correct = row[7]
            if ans == correct:
                print('✔️  Correcto')
                score += 1
            else:
                print(f'❌  Incorrecto. Correcta: {correct}) {opts[correct]}')
            if row[8]:
                print('   ✏️  Explicación:', row[8])
        else:  # fill
            user = input(f'\\n{idx}. {question}\\nTu respuesta: ').strip()
            if user.lower() == row[7].lower():
                print('✔️  Correcto')
                score += 1
            else:
                print(f'❌  Incorrecto. Correcta: {row[7]}')
            if row[8]:
                print('   ✏️  Explicación:', row[8])
    print(f'\\n== Resultado final: {score}/{len(rows)} aciertos ==')

def add_question(conn):
    c = conn.cursor()
    qtype = input('Tipo (mc/fill): ').strip()
    question = input('Pregunta: ').strip()
    if qtype == 'mc':
        option_a = input('a) ').strip()
        option_b = input('b) ').strip()
        option_c = input('c) ').strip()
        option_d = input('d) ').strip()
        correct = input('Letra correcta (a/b/c/d): ').strip().lower()
    else:
        option_a=option_b=option_c=option_d=None
        correct = input('Respuesta correcta: ').strip()
    explanation = input('Explicación (opcional): ').strip()
    c.execute('''INSERT INTO questions (qtype,question,option_a,option_b,option_c,option_d,correct,explanation)
                 VALUES (?,?,?,?,?,?,?,?)''',
              (qtype,question,option_a,option_b,option_c,option_d,correct,explanation or None))
    conn.commit()
    print('✅  Pregunta añadida.')

def main_menu(conn):
    while True:
        print('\\n--- Menú ---')
        print('1) Empezar quiz')
        print('2) Añadir pregunta')
        print('3) Sincronizar con la web')
        print('4) Salir')
        choice = input('Elige opción: ').strip()
        if choice == '1':
            run_quiz(conn)
        elif choice == '2':
            add_question(conn)
        elif choice == '3':
            fetch_remote(conn)
        elif choice == '4':
            break
        else:
            print('Opción inválida.')

def main():
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    seed_sample(conn)
    main_menu(conn)
    conn.close()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\\nHasta luego.')
