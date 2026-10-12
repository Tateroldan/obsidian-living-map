#!/usr/bin/env python3
"""Router de 00 Bandeja: decide area/tipo/prioridad con reglas, sin tokens.

Primera pasada barata. Lo seguro (confianza >= umbral) se mueve; lo ambiguo queda para el
bibliotecario (modelo barato) y lo que mezcla temas prohibidos, para el humano.
Por defecto es simulacro: no toca nada. Con --aplicar mueve y agrega propiedades.
Nunca borra ni sobrescribe; si el destino existe, no mueve.

Las áreas y sus palabras viven en reglas.json (clave "router"); sin él usa reglas.ejemplo.json.
Uso:  python kit/router_bandeja.py [--boveda RUTA] [--aplicar] [--umbral 0.85] [--json]
"""
import argparse, json, os, re, sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from config import BOVEDA  # noqa: E402
from reglas import V, M, S  # noqa: E402

TIPOS = [  # (valor de la propiedad, regex); las señales dependen del idioma de reglas.json
    ("prompt", re.compile(S["prompt"], re.I | re.M)),
    (V["aprendizaje"], re.compile(S["aprendizaje"], re.I)),
    ("plan", re.compile(S["plan"], re.I)),
    ("script", re.compile(r"```|\bdef \w+\(|\bfunction\b")),
]
FECHA = re.compile(S["fecha"], re.I)
URGENTE = re.compile(S["urgente"], re.I)
FM = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n?", re.S)


def cargar_reglas():
    """Devuelve (areas {area: (carpeta, [palabras])}, mezclas [[a, b]], umbral)."""
    r = {}
    for nombre in ("reglas.json", "reglas.ejemplo.json"):  # el primero que tenga "router"
        try:
            with open(RAIZ / nombre, encoding="utf-8") as f:
                r = json.load(f).get("router", {})
        except (OSError, ValueError):
            continue
        if r:
            break
    areas = {a: (v.get("carpeta", a), [p.lower() for p in v.get("palabras", [])]) for a, v in r.get("areas", {}).items()}
    return areas, r.get("no_mezclar", []), float(r.get("umbral", 0.85))


def propiedades(texto):
    m = FM.match(texto)
    props = {}
    if m:
        for linea in m.group(1).splitlines():
            if ":" in linea:
                k, v = linea.split(":", 1)
                props[k.strip()] = v.strip()
    return props, texto[m.end():] if m else texto


def decidir(nombre, texto, areas, mezclas, umbral):
    props, cuerpo = propiedades(texto)
    low = (nombre + "\n" + cuerpo).lower()
    puntos = {a: sum(len(re.findall(r"(?<!\w)" + re.escape(p), low)) for p in pal) for a, (_, pal) in areas.items()}
    if props.get(V["area"]) in areas:  # ya la puso el usuario: manda
        puntos[props[V["area"]]] = max(puntos.values(), default=0) + 5
    if not puntos:
        return dict(area="?", tipo=V["proyecto"], confianza=0.0, decision="bibliotecario", prioridad="normal",
                    fecha_limite=False, tiene_enlace=False, destino=M["r_sin_area"], props=props, cuerpo=cuerpo)
    orden = sorted(puntos.items(), key=lambda x: -x[1]) + [("", 0)]
    (a1, p1), (_, p2) = orden[0], orden[1]
    total = sum(puntos.values())
    # margen frente a la 2.ª área x fuerza de la evidencia (3 aciertos = evidencia plena)
    conf = 0.0 if p1 == 0 else round(min(0.95, (p1 - p2) / max(total, 1) * min(1.0, p1 / 3)), 2)
    mezcla = any(puntos.get(a, 0) > 0 and puntos.get(b, 0) > 0 for a, b in mezclas)
    tipo = props.get(V["tipo"]) or next((t for t, rx in TIPOS if rx.search(cuerpo)), None)
    if tipo is None:             # sin señal de tipo: va a su área como proyecto y pierde confianza
        tipo, conf = V["proyecto"], round(max(conf - 0.1, 0.0), 2)
    if mezcla:
        decision = "humano"          # mezcla prohibida por las reglas
    elif conf >= umbral and p1:
        decision = "mover"
    else:
        decision = "bibliotecario"   # ambigua: segunda pasada con modelo barato
    return dict(area=a1 if p1 else "?", tipo=tipo, confianza=conf, decision=decision,
                prioridad="alta" if URGENTE.search(cuerpo) else "normal",
                fecha_limite=bool(FECHA.search(cuerpo)), tiene_enlace=bool(re.search(r"\[\[[^\]]+\]\]", cuerpo)),
                destino=V["aprendizajes"] if tipo == V["aprendizaje"] else (areas[a1][0] if p1 else M["r_sin_area"]),
                props=props, cuerpo=cuerpo)


def aplicar(ruta, d, boveda):
    destino = boveda / d["destino"] / ruta.name
    if destino.exists():
        return M["r_destino"]
    props = dict(d["props"])
    props.setdefault(V["tipo"], d["tipo"])
    props.setdefault(V["area"], d["area"])
    props.setdefault(V["estado"], V["activo"])
    props.setdefault(V["creado"], date.fromtimestamp(ruta.stat().st_mtime).isoformat())
    cuerpo = d["cuerpo"].rstrip("\n")
    if not d["tiene_enlace"]:
        cuerpo += "\n\n**" + V["conecta"] + "** [[" + V["inicio"] + "]]"
    fm = "\n".join(f"{k}: {v}" for k, v in props.items())
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(f"---\n{fm}\n---\n{cuerpo}\n", encoding="utf-8")
    ruta.unlink()
    return M["r_movida"].format(d=d["destino"])


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    areas, mezclas, umbral0 = cargar_reglas()
    ap = argparse.ArgumentParser()
    ap.add_argument("--boveda", default=BOVEDA)
    ap.add_argument("--aplicar", action="store_true")
    ap.add_argument("--umbral", type=float, default=umbral0)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    boveda = Path(a.boveda)
    bandeja = boveda / V["bandeja"]
    notas = sorted(bandeja.glob("*.md")) if bandeja.is_dir() else []
    salida = []
    for ruta in notas:
        d = decidir(ruta.stem, ruta.read_text(encoding="utf-8"), areas, mezclas, a.umbral)
        r = dict(nota=ruta.name, **{k: d[k] for k in ("area", "tipo", "confianza", "decision", "prioridad", "fecha_limite", "destino")})
        if a.aplicar and d["decision"] == "mover":
            r["resultado"] = aplicar(ruta, d, boveda)
        salida.append(r)
    if a.json:
        print(json.dumps(salida, ensure_ascii=False, indent=1))
        return
    if not salida:
        print(M["r_vacia"])
        return
    for r in salida:
        print(f"{r['decision']:<13} {r['confianza']:.2f}  {r['area']:<14} {r['tipo']:<11} {r['prioridad']:<6}"
              f"{' ' + M['r_fecha'] if r['fecha_limite'] else ''}  {r['nota']} -> {r['destino']}  {r.get('resultado', '')}")
    cuenta = {k: sum(1 for r in salida if r["decision"] == k) for k in ("mover", "bibliotecario", "humano")}
    print("\n" + M["r_fin"].format(n=len(salida), m=cuenta["mover"], b=cuenta["bibliotecario"], h=cuenta["humano"],
                                  estado=M["r_aplicado"] if a.aplicar else M["r_simulacro"]))


if __name__ == "__main__":
    sys.exit(main())
