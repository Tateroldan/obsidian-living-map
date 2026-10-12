#!/usr/bin/env python3
"""Contexto en una sola llamada, sin tokens de modelo.

Dado un tema (palabras clave de la tarea), imprime en un solo paso lo que Claude necesita para
empezar: el estado del proyecto que coincide y las neuronas relacionadas con una línea de resumen.
Sustituye a abrir el índice, listar carpetas, leer la nota del proyecto y buscar neuronas (4-5 turnos).

Uso:  python kit/contexto.py "price calculator csv excel"   [--boveda RUTA] [--max 6]
"""
import argparse, os, re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from config import BOVEDA, OMITIR  # noqa: E402
from reglas import V  # noqa: E402

STOP = {"the", "and", "for", "with", "that", "this", "from", "una", "los", "las", "del", "con", "para", "por", "que", "como",
        "mis", "mi", "my", "in", "to", "of", "a", "an", "is", "it", "on", "en", "de", "la", "el", "un", "se", "me", "add", "fix",
        "how", "are", "you", "today", "hello", "please", "what", "when", "can", "will", "would", "should", "need", "want",
        "make", "use", "using", "new", "hola", "favor", "puedes", "quiero", "necesito", "hacer", "hoy", "work", "code"}
FM = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n?", re.S)


def palabras(texto):
    return [w for w in re.findall(r"[\wáéíóúñü]{3,}", texto.lower()) if w not in STOP]


def notas(boveda):
    for raiz, dirs, archivos in os.walk(boveda):
        dirs[:] = [d for d in dirs if d not in OMITIR and not d.startswith(".") and d != V.get("plantillas", "Plantillas")
                   and d not in ("Templates", "Plantillas")]
        for a in archivos:
            if a.endswith(".md"):
                yield Path(raiz) / a


def leer(p):
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def puntaje(nombre, cuerpo, kw):
    n, b = nombre.lower(), cuerpo.lower()
    return sum(3 * (w in n) + min(2, b.count(w)) for w in kw)


def seccion(txt, titulo, tope=12):
    m = re.search(r"^#{1,4}[ \t]+" + re.escape(titulo) + r"[ \t]*$", txt, re.M)
    if not m:
        return []
    out = []
    for linea in txt[m.end():].splitlines()[1:]:
        if re.match(r"^#{1,4}[ \t]", linea) or linea.startswith("**" + V["conecta"]):
            break
        if linea.strip() and not linea.strip().startswith("<!--"):
            out.append(linea.rstrip()[:260] + ("…" if len(linea.rstrip()) > 260 else ""))
        if len(out) >= tope:
            break
    return out


def resumen(txt):
    cuerpo = FM.sub("", txt, 1)
    for linea in cuerpo.splitlines():
        s = linea.strip()
        if s and not s.startswith("#") and not s.startswith("**" + V["conecta"]):
            return re.sub(r"\s+", " ", s)[:150]
    return ""


def main():
    for f in (sys.stdout, sys.stderr):
        try:
            f.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("tema", nargs="+")
    ap.add_argument("--boveda", default=BOVEDA)
    ap.add_argument("--max", type=int, default=6)
    a = ap.parse_args()
    boveda = Path(a.boveda)
    kw = palabras(" ".join(a.tema))
    if not kw:
        print("(sin palabras clave útiles)")
        return
    titulo_estado = V.get("estado_claude", "Estado para Claude")
    proyectos, neuronas = [], []
    for p in notas(boveda):
        txt = leer(p)
        rel = p.relative_to(boveda).as_posix()
        es_neurona = rel.startswith(V["aprendizajes"] + "/")
        if es_neurona:
            s = puntaje(p.stem, txt, kw)
            if s >= 4 or any(w in p.stem.lower() for w in kw):   # evita coincidencias sueltas de palabras comunes
                neuronas.append((s, p.stem, resumen(txt)))
        elif seccion(txt, titulo_estado, 1):
            s = puntaje(p.stem, txt[:800], kw)
            if s >= 4 or any(w in p.stem.lower() for w in kw):
                proyectos.append((s, p, txt))
    print(f"# Contexto para: {' '.join(a.tema)}  (bóveda: {boveda})")
    if proyectos:
        proyectos.sort(key=lambda x: -x[0])
        for _, p, txt in proyectos[:2]:
            print(f"\n## Proyecto [[{p.stem}]]  ({p.relative_to(boveda).as_posix()})")
            for l in re.findall(r"^\*\*(?:Code|Código|Goal|Objetivo|Next step|Siguiente paso):\*\*.*$", txt, re.M)[:3]:
                print(l)
            print(f"### {titulo_estado}")
            print("\n".join(seccion(txt, titulo_estado)))
    else:
        print(f"\n(ningún proyecto coincide; abre {V['inicio']}.md y elige la nota del proyecto)")
    print(f"\n## {V['aprendizajes']} relacionadas")
    if neuronas:
        neuronas.sort(key=lambda x: (-x[0], x[1]))
        for _, nombre, res in neuronas[:a.max]:
            print(f"- [[{nombre}]]: {res}")
    else:
        print("(ninguna; si esta tarea deja una técnica o trampa reutilizable, crea la neurona al terminar)")


if __name__ == "__main__":
    main()
