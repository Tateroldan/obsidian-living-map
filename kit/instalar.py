#!/usr/bin/env python3
"""Instala el kit del conjunto neuronal: bóveda de ejemplo, agente, skills y reglas para Claude.

Nunca sobrescribe nada que ya exista. Pregunta antes de cada grupo. Sin consola interactiva
(o con --simulacro) solo muestra lo que haría.

  python kit/instalar.py                 pregunta paso a paso
  python kit/instalar.py --simulacro     muestra el plan sin escribir nada
  python kit/instalar.py --si            responde «sí» a todo menos al CLAUDE.md global
  python kit/instalar.py --boveda RUTA   usa esa carpeta (por defecto MAPA_BOVEDA o ~/Documents/Boveda)
"""
import argparse, os, shutil, sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
KIT = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))
from config import BOVEDA  # noqa: E402

INI, FIN = "<!-- olm:inicio", "<!-- olm:fin -->"


def preguntar(texto, auto):
    if auto is not None:
        print(f"{texto} → {'sí' if auto else 'no'}")
        return auto
    if not sys.stdin or not sys.stdin.isatty():
        return False
    try:
        return input(f"{texto} (s/n): ").strip().lower()[:1] in ("s", "y")
    except EOFError:
        return False


def sustituir(texto, boveda):
    return texto.replace("{{BOVEDA}}", str(boveda).replace("\\", "/")).replace("{{HOY}}", date.today().isoformat())


def copiar_arbol(origen, destino, boveda, simulacro, sustituir_marcas=True):
    """Copia solo lo que no existe. Devuelve (copiados, omitidos)."""
    hechos, omitidos = [], []
    for ruta in sorted(origen.rglob("*")):
        if ruta.is_dir():
            continue
        rel = ruta.relative_to(origen)
        dst = destino / rel
        if dst.exists():
            omitidos.append(rel)
            continue
        hechos.append(rel)
        if simulacro:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        if ruta.suffix in (".md", ".json") and sustituir_marcas:
            dst.write_text(sustituir(ruta.read_text(encoding="utf-8"), boveda), encoding="utf-8", newline="\n")
        else:
            shutil.copy2(ruta, dst)
    return hechos, omitidos


def resumen(nombre, hechos, omitidos, simulacro):
    verbo = "copiaría" if simulacro else "copiado"
    print(f"  {nombre}: {verbo} {len(hechos)}, ya existían {len(omitidos)} (no se tocan)")


def main():
    for flujo in (sys.stdout, sys.stderr):  # consolas cp1252 de Windows no soportan → ni acentos
        try:
            flujo.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--boveda", default=BOVEDA)
    ap.add_argument("--claude-dir", default=str(Path.home() / ".claude"))
    ap.add_argument("--simulacro", action="store_true")
    ap.add_argument("--si", action="store_true")
    a = ap.parse_args()
    boveda, claude = Path(a.boveda), Path(a.claude_dir)
    auto = True if a.si else (False if a.simulacro else None)
    sim = a.simulacro or (auto is None and not (sys.stdin and sys.stdin.isatty()))
    if sim and not a.simulacro:
        print("(sin consola interactiva: solo se muestra el plan; usa --si para aplicar)")
        auto = False
    print(f"Bóveda: {boveda}\nClaude:  {claude}\n")

    # 1. Bóveda de ejemplo
    existe = boveda.is_dir() and any(boveda.iterdir())
    print("1. Bóveda de ejemplo" + (" (la carpeta ya tiene notas: solo se agregan archivos que falten)" if existe else ""))
    if preguntar("¿Crear/completar la bóveda de ejemplo?", auto if not sim else False) or a.simulacro:
        h, o = copiar_arbol(KIT / "boveda-ejemplo", boveda, boveda, a.simulacro)
        resumen("bóveda", h, o, a.simulacro)

    # 2. Reglas del validador y el router
    print("\n2. Reglas del validador y el router (reglas.json)")
    dst = RAIZ / "reglas.json"
    if dst.exists():
        print("  reglas.json ya existe: no se toca")
    elif preguntar("¿Crear reglas.json a partir de reglas.ejemplo.json?", auto if not sim else False) or a.simulacro:
        if not a.simulacro:
            shutil.copy2(RAIZ / "reglas.ejemplo.json", dst)
        print("  " + ("crearía" if a.simulacro else "creado") + " reglas.json (ajústalo a tu bóveda)")

    # 3. Agente y skills
    print("\n3. Agente y skills de Claude")
    if preguntar("¿Instalar el agente bibliotecario y las skills verificar-web y cierre-de-tarea?", auto if not sim else False) or a.simulacro:
        h, o = copiar_arbol(KIT / "claude" / "agentes", claude / "agents", boveda, a.simulacro)
        resumen("agentes", h, o, a.simulacro)
        h, o = copiar_arbol(KIT / "claude" / "skills", claude / "skills", boveda, a.simulacro, sustituir_marcas=False)
        resumen("skills", h, o, a.simulacro)

    # 4. CLAUDE.md global (siempre pregunta, incluso con --si)
    print("\n4. Reglas para Claude (CLAUDE.md global)")
    plantilla = sustituir((KIT / "claude" / "CLAUDE.plantilla.md").read_text(encoding="utf-8"), boveda)
    destino = claude / "CLAUDE.md"
    actual = destino.read_text(encoding="utf-8") if destino.exists() else ""
    if INI in actual:
        print("  tu CLAUDE.md ya tiene el bloque del kit: no se toca")
    else:
        print("  Se agregaría este bloque al FINAL de " + str(destino) + " (con copia .bak antes):\n")
        print("  " + plantilla.replace("\n", "\n  ")[:1200] + "\n  [...]\n")
        if not a.simulacro and not sim and preguntar("¿Agregar el bloque a tu CLAUDE.md global?", None):
            claude.mkdir(parents=True, exist_ok=True)
            if destino.exists():
                shutil.copy2(destino, destino.with_suffix(".md.bak"))
            destino.write_text(actual.rstrip("\n") + ("\n\n" if actual else "") + plantilla, encoding="utf-8")
            print("  agregado (copia en CLAUDE.md.bak)")
        else:
            print("  no se modificó. Si lo quieres, pega kit/claude/CLAUDE.plantilla.md a mano.")

    # 5. Hooks
    print("\n5. Hooks (no se editan solos): agrégalos a", claude / "settings.json", "con /hooks o a mano:")
    print(f'   hook.py   → PostToolUse  python "{RAIZ / "hook.py"}"')
    print(f'   validar.py → PostToolUse (Write|Edit)  python "{RAIZ / "validar.py"}"')
    print(f'   diario.py → SessionEnd   python "{RAIZ / "diario.py"}"')
    print("\nListo. Abre el mapa con abrir.cmd y mira la araña recorrer tu bóveda.")


if __name__ == "__main__":
    main()
