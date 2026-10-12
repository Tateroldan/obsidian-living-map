#!/usr/bin/env python3
"""Instala el kit del conjunto neuronal / Installs the neural-set kit.

Bóveda de ejemplo, agente, skills y reglas para Claude, en español o inglés.
Example vault, agent, skills and Claude rules, in Spanish or English.
Nunca sobrescribe nada que ya exista / Never overwrites anything that already exists.

  python kit/instalar.py                 pregunta paso a paso / asks step by step
  python kit/instalar.py --lang en       English kit (default: es)
  python kit/instalar.py --simulacro     muestra el plan sin escribir / shows the plan, writes nothing
  python kit/instalar.py --si            responde «sí» a todo menos al CLAUDE.md / yes to all but CLAUDE.md
  python kit/instalar.py --boveda RUTA   carpeta de la bóveda / vault folder (default MAPA_BOVEDA or ~/Documents/Boveda)
"""
import argparse, os, shutil, sys
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
KIT = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))
from config import BOVEDA  # noqa: E402

INI = "<!-- olm:inicio"
FUENTES = {  # idioma -> (bóveda de ejemplo, carpeta claude, reglas de ejemplo, plantilla CLAUDE.md)
    "es": (KIT / "boveda-ejemplo", KIT / "claude", RAIZ / "reglas.ejemplo.json", "CLAUDE.plantilla.md"),
    "en": (KIT / "en" / "example-vault", KIT / "en" / "claude", RAIZ / "reglas.ejemplo.en.json", "CLAUDE.template.md"),
}
T = {
    "es": dict(
        boveda="Bóveda", claude="Claude", s1="1. Bóveda de ejemplo", s1b=" (la carpeta ya tiene notas: solo se agregan archivos que falten)",
        q1="¿Crear/completar la bóveda de ejemplo?", n_boveda="bóveda", s2="2. Reglas del validador y el router (reglas.json)",
        existe="  reglas.json ya existe: no se toca", q2="¿Crear reglas.json a partir del ejemplo?",
        crearia="crearía", creado="creado", reglas_ok=" reglas.json (ajústalo a tu bóveda)",
        s3="3. Agente y skills de Claude", q3="¿Instalar el agente y las skills?", n_agentes="agentes", n_skills="skills",
        s4="4. Reglas para Claude (CLAUDE.md global)", ya_bloque="  tu CLAUDE.md ya tiene el bloque del kit: no se toca",
        agregaria="  Se agregaría este bloque al FINAL de {d} (con copia .bak antes):",
        q4="¿Agregar el bloque a tu CLAUDE.md global?", agregado="  agregado (copia en CLAUDE.md.bak)",
        no_mod="  no se modificó. Si lo quieres, pega kit/{p} a mano.",
        s5="5. Hooks (no se editan solos): agrégalos a {d} con /hooks o a mano:",
        fin="Listo. Abre el mapa con abrir.cmd y mira la araña recorrer tu bóveda.",
        sin_tty="(sin consola interactiva: solo se muestra el plan; usa --si para aplicar)",
        copiaria="copiaría", copiado="copiado", ya="ya existían {n} (no se tocan)", si="sí", no="no", sn="s/n"),
    "en": dict(
        boveda="Vault", claude="Claude", s1="1. Example vault", s1b=" (the folder already has notes: only missing files are added)",
        q1="Create/complete the example vault?", n_boveda="vault", s2="2. Validator and router rules (reglas.json)",
        existe="  reglas.json already exists: left alone", q2="Create reglas.json from the example?",
        crearia="would create", creado="created", reglas_ok=" reglas.json (adjust it to your vault)",
        s3="3. Claude agent and skills", q3="Install the agent and the skills?", n_agentes="agents", n_skills="skills",
        s4="4. Rules for Claude (global CLAUDE.md)", ya_bloque="  your CLAUDE.md already has the kit block: left alone",
        agregaria="  This block would be added at the END of {d} (a .bak copy is made first):",
        q4="Add the block to your global CLAUDE.md?", agregado="  added (copy in CLAUDE.md.bak)",
        no_mod="  not modified. If you want it, paste kit/{p} by hand.",
        s5="5. Hooks (not edited automatically): add them to {d} with /hooks or by hand:",
        fin="Done. Open the map with abrir.cmd and watch the spider walk your vault.",
        sin_tty="(no interactive console: only the plan is shown; use --si to apply)",
        copiaria="would copy", copiado="copied", ya="{n} already existed (left alone)", si="yes", no="no", sn="y/n"),
}


def preguntar(texto, auto, t):
    if auto is not None:
        print(f"{texto} -> {t['si'] if auto else t['no']}")
        return auto
    if not sys.stdin or not sys.stdin.isatty():
        return False
    try:
        return input(f"{texto} ({t['sn']}): ").strip().lower()[:1] in ("s", "y")
    except EOFError:
        return False


def sustituir(texto, boveda):
    return (texto.replace("{{BOVEDA}}", str(boveda).replace("\\", "/")).replace("{{HOY}}", date.today().isoformat())
            .replace("{{REPO}}", str(RAIZ).replace("\\", "/")))


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


def resumen(nombre, hechos, omitidos, simulacro, t):
    verbo = t["copiaria"] if simulacro else t["copiado"]
    print(f"  {nombre}: {verbo} {len(hechos)}, " + t["ya"].format(n=len(omitidos)))


def elegir_idioma(pedido):
    if pedido:
        return pedido
    if sys.stdin and sys.stdin.isatty():
        try:
            r = input("Idioma del kit / Kit language (es/en) [es]: ").strip().lower()
            return "en" if r.startswith("en") else "es"
        except EOFError:
            pass
    return "es"


def main():
    for flujo in (sys.stdout, sys.stderr):  # consolas cp1252 de Windows no soportan acentos ni flechas
        try:
            flujo.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    ap = argparse.ArgumentParser()
    ap.add_argument("--boveda", default=BOVEDA)
    ap.add_argument("--claude-dir", default=str(Path.home() / ".claude"))
    ap.add_argument("--lang", choices=("es", "en"))
    ap.add_argument("--simulacro", action="store_true")
    ap.add_argument("--si", action="store_true")
    a = ap.parse_args()
    lang = elegir_idioma(a.lang)
    t = T[lang]
    vault_src, claude_src, reglas_src, plantilla = FUENTES[lang]
    boveda, claude = Path(a.boveda), Path(a.claude_dir)
    auto = True if a.si else (False if a.simulacro else None)
    sim = a.simulacro or (auto is None and not (sys.stdin and sys.stdin.isatty()))
    if sim and not a.simulacro:
        print(t["sin_tty"])
        auto = False
    print(f"{t['boveda']}: {boveda}\n{t['claude']}:  {claude}\n")

    # 1. Bóveda de ejemplo
    existe = boveda.is_dir() and any(boveda.iterdir())
    print(t["s1"] + (t["s1b"] if existe else ""))
    if preguntar(t["q1"], auto if not sim else False, t) or a.simulacro:
        h, o = copiar_arbol(vault_src, boveda, boveda, a.simulacro)
        resumen(t["n_boveda"], h, o, a.simulacro, t)

    # 2. Reglas del validador y el router
    print("\n" + t["s2"])
    dst = RAIZ / "reglas.json"
    if dst.exists():
        print(t["existe"])
    elif preguntar(t["q2"], auto if not sim else False, t) or a.simulacro:
        if not a.simulacro:
            shutil.copy2(reglas_src, dst)
        print("  " + (t["crearia"] if a.simulacro else t["creado"]) + t["reglas_ok"])

    # 3. Agente y skills
    print("\n" + t["s3"])
    if preguntar(t["q3"], auto if not sim else False, t) or a.simulacro:
        carpeta_agentes = claude_src / ("agents" if (claude_src / "agents").exists() else "agentes")
        h, o = copiar_arbol(carpeta_agentes, claude / "agents", boveda, a.simulacro)
        resumen(t["n_agentes"], h, o, a.simulacro, t)
        h, o = copiar_arbol(claude_src / "skills", claude / "skills", boveda, a.simulacro, sustituir_marcas=False)
        resumen(t["n_skills"], h, o, a.simulacro, t)

    # 4. CLAUDE.md global (siempre pregunta, incluso con --si)
    print("\n" + t["s4"])
    texto = sustituir((claude_src / plantilla).read_text(encoding="utf-8"), boveda)
    destino = claude / "CLAUDE.md"
    actual = destino.read_text(encoding="utf-8") if destino.exists() else ""
    if INI in actual:
        print(t["ya_bloque"])
    else:
        print(t["agregaria"].format(d=destino) + "\n")
        print("  " + texto.replace("\n", "\n  ")[:1200] + "\n  [...]\n")
        if not a.simulacro and not sim and preguntar(t["q4"], None, t):
            claude.mkdir(parents=True, exist_ok=True)
            if destino.exists():
                shutil.copy2(destino, destino.with_suffix(".md.bak"))
            destino.write_text(actual.rstrip("\n") + ("\n\n" if actual else "") + texto, encoding="utf-8")
            print(t["agregado"])
        else:
            print(t["no_mod"].format(p=str((claude_src / plantilla).relative_to(KIT)).replace("\\", "/")))

    # 5. Hooks
    print("\n" + t["s5"].format(d=claude / "settings.json"))
    print(f'   hook.py    -> PostToolUse  python "{RAIZ / "hook.py"}"')
    print(f'   validar.py -> PostToolUse (Write|Edit)  python "{RAIZ / "validar.py"}"')
    print(f'   diario.py  -> SessionEnd   python "{RAIZ / "diario.py"}"')
    print("\n" + t["fin"])


if __name__ == "__main__":
    main()
