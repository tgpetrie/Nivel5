
import sys

def ask_mcq(question, options, correct):
    print("\\n" + question)
    for label, text in options.items():
        print(f"  {label}) {text}")
    ans = input("Tu respuesta: ").strip().lower()
    if ans == correct:
        print("✔️  Correcto\\n")
        return 1
    else:
        print(f"❌  Incorrecto. Respuesta correcta: {correct}) {options[correct]}\\n")
        return 0

def ask_fill(question, correct, normaliser=lambda s: s):
    resp = input("\\n" + question + "\\nTu respuesta: ").strip()
    if normaliser(resp) == normaliser(correct):
        print("✔️  Correcto\\n")
        return 1
    else:
        print(f"❌  Incorrecto. Respuesta correcta: {correct}\\n")
        return 0

def main():
    print("=== Quiz interactivo – Repaso Español 5 ===")
    score = 0
    total = 0

    # Sección I – Gramática objetiva
    print("\\nSECCIÓN I – Gramática objetiva")
    q1_opts = {"a": "de", "b": "en", "c": "por", "d": "sobre"}
    score += ask_mcq("1. Lo sorprendente ___ este proyecto es la rapidez de los resultados.", q1_opts, "a"); total += 1

    score += ask_fill("2. Ricardo ha aumentado mucho de peso últimamente, pero todavía no ___ a un nutriólogo.", "ha ido"); total += 1

    q3_opts = {"a": "haya", "b": "ha", "c": "hubiera", "d": "habría"}
    score += ask_mcq("3. No creo que Mariana ___ preparado el informe tan pronto.", q3_opts, "a"); total += 1

    score += ask_fill("4. Rebeca ya ___ (nacer) cuando su madre empezó a trabajar como supervisora.", "había nacido"); total += 1

    score += ask_fill("5. Avísame tan pronto como ___ (estar‑tú) listo.", "estés"); total += 1

    q6_opts = {"a": "de", "b": "por", "c": "en", "d": "sobre"}
    score += ask_mcq("6. Lo malo ___ vivir lejos es el tráfico diario.", q6_opts, "a"); total += 1

    q7_opts = {"a": "hacen", "b": "harán", "c": "hagan", "d": "hicieron"}
    score += ask_mcq("7. Dudo que los políticos ___ algo para cambiar la situación.", q7_opts, "c"); total += 1

    score += ask_fill("8. Si tuviéramos más tiempo, ___ (viajar‑nosotros) a Oaxaca.", "viajaríamos"); total += 1

    q9_opts = {"a": "habrá", "b": "habría", "c": "ha", "d": "hubiera"}
    score += ask_mcq("9. Cuando el director termine su mandato, la tasa de desempleo ya ___ aumentado.", q9_opts, "a"); total += 1

    score += ask_fill("10. Me alegra que tus padres ___ (confiar) en nuestro plan.", "confíen"); total += 1

    # Resultado
    print(f"=== Resultado: {score}/{total} aciertos ===")
    if score == total:
        print("¡Excelente, dominio total de la sección!")
    elif score >= total * 0.7:
        print("¡Buen trabajo! Revisa los errores menores.")
    else:
        print("Conviene repasar los temas señalados.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\\nQuiz terminado.")
