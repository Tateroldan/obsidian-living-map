"""Arranque automático opcional (Windows): un .vbs en la carpeta Inicio que lanza el servidor sin ventana.

La primera vez que se abre el mapa desde una consola se pregunta una sola vez; la respuesta queda en
preferencias.json (no se sube). Después se cambia con:
  python server.py --autoarranque on | off | estado
"""
import json, os, subprocess, sys

from config import AQUI
from reglas import M

PREFS = os.path.join(AQUI, "preferencias.json")
NOMBRE_VBS = "obsidian-living-map.vbs"


def _inicio():
    base = os.environ.get("APPDATA")
    return os.path.join(base, "Microsoft", "Windows", "Start Menu", "Programs", "Startup") if base else None


def _vbs():
    d = _inicio()
    return os.path.join(d, NOMBRE_VBS) if d else None


def _leer():
    try:
        with open(PREFS, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def _guardar(p):
    with open(PREFS, "w", encoding="utf-8") as f:
        json.dump(p, f, indent=2)


def activo():
    v = _vbs()
    return bool(v) and os.path.exists(v)


def activar():
    v = _vbs()
    if not v or os.name != "nt":
        return False
    exe = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
    if not os.path.exists(exe):
        exe = sys.executable
    srv = os.path.join(AQUI, "server.py")
    cuerpo = 'CreateObject("WScript.Shell").Run """%s"" ""%s""", 0, False\r\n' % (exe, srv)
    with open(v, "w", encoding="utf-8") as f:
        f.write(cuerpo)
    return True


def desactivar():
    v = _vbs()
    if v and os.path.exists(v):
        os.remove(v)


def preguntar_primera_vez():
    """Solo en consola, solo en Windows y solo si nunca se ha contestado."""
    if os.name != "nt" or "autoarranque" in _leer() or not sys.stdin or not sys.stdin.isatty():
        return
    try:
        r = input(M["aa_pregunta"]).strip().lower()
    except EOFError:
        return
    si = r[:1] in tuple(M["aa_si_letras"])
    _guardar({**_leer(), "autoarranque": si})
    if si:
        activar()
    print(M["aa_si_ok"] if si else M["aa_no_ok"])


def comando(arg):
    """--autoarranque on|off|estado → mensaje para imprimir."""
    if arg == "on":
        ok = activar()
        if ok:
            _guardar({**_leer(), "autoarranque": True})
        return M["aa_on"] if ok else M["aa_solo_win"]
    if arg == "off":
        desactivar()
        _guardar({**_leer(), "autoarranque": False})
        return M["aa_off"]
    return M["aa_estado"].format(e=M["aa_activado"] if activo() else M["aa_desactivado"])
