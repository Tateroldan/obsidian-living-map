"""Consulta el grafo de la bóveda sin leer notas: vecinos hasta N saltos y camino más corto.
Sin tokens. Idea tomada de C2B/ASM (brain_neighbors, brain_path). Reusa salud._notas().
Uso:
  python vecinos.py "Pregunta, no adivines" [--prof 2]
  python vecinos.py --camino "Mapa vivo" "Guardias con hooks sin tokens"
  python vecinos.py --tema "tokens"        # notas cuyo nombre contiene el tema, con sus enlaces entrantes"""
import argparse, os, sys
from collections import deque
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import salud

TOPE = 40


def grafo():
    notas = salud._notas()
    nombre = {n.split("/")[-1].lower(): n for n in notas}
    sale = {n: set() for n in notas}
    entra = {n: set() for n in notas}
    for n, ls in notas.items():
        for l in ls:
            l = l.strip().removesuffix(".md")
            d = l if l in notas else nombre.get(l.split("/")[-1].lower())
            if d and d != n:
                sale[n].add(d)
                entra[d].add(n)
    return notas, sale, entra


def buscar(notas, q):
    ql = q.lower().removesuffix(".md")
    exacta = [n for n in notas if n.lower() == ql or n.split("/")[-1].lower() == ql]
    return exacta or sorted(n for n in notas if ql in n.lower())


def elegir(notas, q):
    c = buscar(notas, q)
    if not c:
        sys.exit(f"Sin coincidencias para «{q}».")
    if len(c) > 1 and not any(n.split("/")[-1].lower() == q.lower() for n in c):
        sys.exit("Varias coincidencias, sé más preciso:\n" + "\n".join("- " + n for n in c[:15]))
    return c[0]


def vecinos(sale, entra, ini, prof):
    vistos, cola, capas = {ini}, deque([(ini, 0)]), {}
    while cola:
        n, d = cola.popleft()
        if d == prof:
            continue
        for m in sorted(sale[n] | entra[n]):
            if m not in vistos:
                vistos.add(m)
                capas.setdefault(d + 1, []).append(m)
                cola.append((m, d + 1))
    return capas


def camino(sale, entra, a, b):
    previo, cola = {a: None}, deque([a])
    while cola:
        n = cola.popleft()
        if n == b:
            r = []
            while n is not None:
                r.append(n)
                n = previo[n]
            return r[::-1]
        for m in sorted(sale[n] | entra[n]):
            if m not in previo:
                previo[m] = n
                cola.append(m)
    return None


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("nota", nargs="?")
    ap.add_argument("--prof", type=int, default=1)
    ap.add_argument("--camino", nargs=2, metavar=("DE", "A"))
    ap.add_argument("--tema")
    a = ap.parse_args()
    notas, sale, entra = grafo()
    if a.tema:
        c = buscar(notas, a.tema)
        print(f"{len(c)} notas con «{a.tema}» en el nombre:")
        for n in c[:TOPE]:
            print(f"- {n}  (←{len(entra[n])} →{len(sale[n])})")
        return
    if a.camino:
        de, para = elegir(notas, a.camino[0]), elegir(notas, a.camino[1])
        r = camino(sale, entra, de, para)
        print(" → ".join(r) if r else f"Sin camino entre «{de}» y «{para}».")
        return
    if not a.nota:
        ap.print_help()
        return
    ini = elegir(notas, a.nota)
    capas = vecinos(sale, entra, ini, a.prof)
    print(f"{ini}  (←{len(entra[ini])} entran, →{len(sale[ini])} salen)")
    mostrado = 0
    for d in sorted(capas):
        print(f"\nSalto {d}:")
        for n in capas[d]:
            if mostrado >= TOPE:
                print(f"… y {sum(len(v) for v in capas.values()) - mostrado} más (usa --prof menor)")
                return
            print(f"- {n}")
            mostrado += 1


if __name__ == "__main__":
    main()
