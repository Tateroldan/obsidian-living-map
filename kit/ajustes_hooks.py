"""Agrega los hooks recomendados al settings.json de Claude Code / Adds the recommended hooks to Claude Code's settings.json.

Usa el mismo Python que corre el instalador (evita python vs python3 y el PATH), guarda copia .bak
y no duplica: si un hook ya apunta al mismo archivo, lo deja como está.
"""
import json, shutil, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# (evento, matcher, script): solo los recomendados; los de kit/hooks/ siguen siendo opcionales
RECOMENDADOS = [
    ("PostToolUse", "Read|Write|Edit|Grep|Glob|Bash|PowerShell", RAIZ / "hook.py"),
    ("PostToolUse", "Write|Edit", RAIZ / "validar.py"),
    ("SessionEnd", None, RAIZ / "diario.py"),
]


def comando(script):
    return '"%s" "%s"' % (Path(sys.executable).as_posix(), script.as_posix())


def plan(ajustes):
    """Lista de (evento, matcher, comando) que faltan en `ajustes`."""
    faltan = []
    for evento, matcher, script in RECOMENDADOS:
        ya = any(script.name in h.get("command", "") and str(script.parent.as_posix()) in h.get("command", "").replace("\\", "/")
                 for g in ajustes.get("hooks", {}).get(evento, []) for h in g.get("hooks", []))
        if not ya:
            faltan.append((evento, matcher, comando(script)))
    return faltan


def aplicar(ruta, simulacro=False):
    """Devuelve la lista de comandos agregados (o que se agregarían)."""
    ruta = Path(ruta)
    try:
        ajustes = json.loads(ruta.read_text(encoding="utf-8")) if ruta.exists() else {}
    except ValueError:
        raise SystemExit("settings.json no es JSON válido / is not valid JSON: %s" % ruta)
    faltan = plan(ajustes)
    if simulacro or not faltan:
        return faltan
    for evento, matcher, cmd in faltan:
        grupo = {"hooks": [{"type": "command", "command": cmd}]}
        if matcher:
            grupo = {"matcher": matcher, **grupo}
        ajustes.setdefault("hooks", {}).setdefault(evento, []).append(grupo)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    if ruta.exists():
        shutil.copy2(ruta, ruta.with_suffix(".json.bak"))
    ruta.write_text(json.dumps(ajustes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return faltan
