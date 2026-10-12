"""Hook SessionEnd: resume en la nota diaria de la boveda lo que toco la sesion.
Sin dependencias, silencioso, siempre exit 0.
Uso de prueba: python diario.py --prueba SALIDA.md  (copia la nota de hoy ahi y escribe en la copia)
"""
import json, os, re, sys, shutil
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import BOVEDA, LOG as EVENTOS
CODIGO = (".py", ".js", ".ts", ".html", ".css", ".json", ".pyw", ".cmd", ".ps1")


def norm(p):
    return (p or "").replace("\\", "/").rstrip("/")


def enlace(path):
    """[[nombre]] si es una nota .md de la boveda; None si no sirve."""
    p = norm(path)
    base = norm(BOVEDA).lower() + "/"
    if not p.lower().startswith(base) or not p.lower().endswith(".md"):
        return None
    nombre = p[len(base):-3]
    nombre = nombre.rsplit("/", 1)[-1]
    return "[[%s]]" % nombre if nombre.strip() else None


def lugar(path):
    """Para busquedas: nota -> [[x]]; carpeta de la boveda -> `ruta/`."""
    e = enlace(path)
    if e:
        return e
    p = norm(path)
    base = norm(BOVEDA)
    if p.lower() == base.lower():
        return "`Boveda/`"
    if p.lower().startswith(base.lower() + "/"):
        return "`%s`" % p[len(base) + 1:]
    return None


def lista(items, maximo=15):
    vistos = []
    for i in items:
        if i and i not in vistos:
            vistos.append(i)
    extra = len(vistos) - maximo
    txt = ", ".join(vistos[:maximo])
    return txt + (" +%d más" % extra if extra > 0 else "")


def leer_eventos(sid):
    out = []
    with open(EVENTOS, encoding="utf-8", errors="replace") as f:
        for linea in f:
            try:
                e = json.loads(linea)
            except Exception:
                continue
            s = e.get("session") or ""
            if s and (sid == s or sid.startswith(s) or s.startswith(sid)):
                out.append(e)
    return out


def construir(sid, cwd, eventos):
    leidas = [enlace(e.get("path")) for e in eventos if e.get("verb") == "read"]
    escritas = [enlace(e.get("path")) for e in eventos if e.get("verb") == "write"]
    busq = [lugar(e.get("path")) for e in eventos if e.get("verb") == "search"]
    leidas, escritas, busq = [[x for x in l if x] for l in (leidas, escritas, busq)]
    if not (leidas or escritas or busq):
        return None  # no toco ninguna nota de la boveda
    ts = [e["t"] for e in eventos if isinstance(e.get("t"), (int, float))]
    hm = lambda t: datetime.fromtimestamp(t).strftime("%H:%M")
    h1, h2 = (hm(min(ts)), hm(max(ts))) if ts else ("??:??", "??:??")
    proyecto = os.path.basename(norm(cwd)) or "(desconocido)"
    codigo = [os.path.basename(norm(e.get("path"))) for e in eventos
              if e.get("verb") == "write" and norm(e.get("path")).lower().endswith(CODIGO)
              and not norm(e.get("path")).lower().startswith(norm(BOVEDA).lower())]
    L = ["## Sesión %s–%s (auto)" % (h1, h2), "<!-- sesion:%s -->" % sid,
         "- Proyecto: %s" % proyecto]
    if leidas:
        L.append("- Notas leídas: " + lista(leidas))
    if escritas:
        L.append("- Notas escritas: " + lista(escritas))
    if busq:
        L.append("- Búsquedas: " + lista(busq))
    if codigo:
        L.append("- Código tocado: " + lista(["`%s`" % c for c in codigo]))
    return "\n".join(L) + "\n"


def escribir(ruta, hoy, sid, bloque):
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as f:
            txt = f.read()
    else:
        txt = "---\ntipo: diario\narea: personal\nestado: activo\ncreado: %s\n---\n# %s\n" % (hoy, hoy)
    marca = "<!-- sesion:%s -->" % sid
    i = txt.find(marca)
    if i >= 0:
        ini = txt.rfind("\n## ", 0, i) + 1  # inicio del encabezado de esa seccion
        fin = txt.find("\n## ", i)
        resto = txt[fin + 1:] if fin >= 0 else ""
        txt = txt[:ini] + bloque + ("\n" + resto if resto else "")
    else:
        txt = txt.rstrip("\n") + "\n\n" + bloque
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    tmp = ruta + ".tmp"  # escritura atómica: la nota nunca queda a medias
    try:
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            f.write(txt)
        os.replace(tmp, ruta)
    except OSError:
        with open(ruta, "w", encoding="utf-8", newline="\n") as f:
            f.write(txt)


def main():
    try:
        datos = json.loads(sys.stdin.buffer.read().decode("utf-8-sig", "replace") or "{}")
    except Exception:
        datos = {}
    sid = datos.get("session_id") or ""
    if not sid:
        return
    eventos = leer_eventos(sid)
    bloque = construir(sid, datos.get("cwd") or "", eventos)
    if not bloque:
        return
    hoy = datetime.now().strftime("%Y-%m-%d")
    ruta = os.path.join(BOVEDA, "00 Diario", hoy + ".md")
    if "--prueba" in sys.argv:
        destino = sys.argv[sys.argv.index("--prueba") + 1]
        if os.path.exists(ruta) and not os.path.exists(destino):
            shutil.copyfile(ruta, destino)
        ruta = destino
    escribir(ruta, hoy, sid, bloque)


if __name__ == "__main__":
    try:
        main()
    except BaseException:
        pass
    sys.exit(0)
