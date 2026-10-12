"""Servidor local del mapa vivo: http://127.0.0.1:8765"""
import json, os, re, sys, threading, webbrowser
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import salud
from config import AQUI, BOVEDA, PUERTO, LOG, OMITIR, DECISIONES

LINK = re.compile(r"\[\[([^\]|#^]+)")
# solo se sirve la pagina y sus piezas: ni events.jsonl ni los .py salen por HTTP
ESTATICOS = re.compile(r"^/(index\.html|[\w-]+\.js|(fuentes|vendor)/[\w-]+\.[\w.]+)?$")
HOSTS = {"127.0.0.1:%d" % PUERTO, "localhost:%d" % PUERTO}


_cache = {"firma": None, "datos": None}


def firma():
    n, mx = 0, 0.0
    for raiz, dirs, archivos in os.walk(BOVEDA):
        dirs[:] = [d for d in dirs if d not in OMITIR and not d.startswith(".")]
        for a in archivos:
            if a.endswith(".md"):
                try:
                    mx = max(mx, os.stat(os.path.join(raiz, a)).st_mtime)
                except OSError:
                    continue
                n += 1
    return (n, mx)


def grafo():
    f = firma()
    if _cache["firma"] == f and _cache["datos"] is not None:
        return _cache["datos"]
    datos = _construir()
    _cache["firma"], _cache["datos"] = f, datos
    return datos


def _construir():
    notas = {}
    for raiz, dirs, archivos in os.walk(BOVEDA):
        dirs[:] = [d for d in dirs if d not in OMITIR and not d.startswith(".")]
        for a in archivos:
            if not a.endswith(".md"):
                continue
            ruta = os.path.join(raiz, a)
            rel = os.path.relpath(ruta, BOVEDA).replace("\\", "/")[:-3]
            try:
                txt = open(ruta, encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            m = re.search(r"^area:[ \t]*([^\s]+)[ \t]*$", txt, re.M)
            area = m.group(1).strip() if m else (rel.split("/")[0] if "/" in rel else "raiz")
            notas[rel] = {"id": rel, "title": rel.split("/")[-1], "area": area.lower(),
                          "folder": rel.split("/")[0] if "/" in rel else "",
                          "words": len(txt.split()), "links": LINK.findall(txt)}
    por_nombre = {n.split("/")[-1].lower(): n for n in notas}
    aristas = set()
    for n in notas.values():
        for l in n.pop("links"):
            l = l.strip().removesuffix(".md")
            dest = l if l in notas else por_nombre.get(l.split("/")[-1].lower())
            if dest and dest != n["id"]:
                aristas.add(tuple(sorted((n["id"], dest))))
    return {"vault": os.path.basename(BOVEDA), "decisiones": DECISIONES, "nodes": list(notas.values()), "links": [{"source": a, "target": b} for a, b in aristas]}


_ev = {"off": 0, "n": 0, "items": []}
_ev_lock = threading.Lock()


def eventos(desde):
    with _ev_lock:  # varias pestañas piden a la vez
        return _eventos(desde)


def _eventos(desde):
    if not os.path.exists(LOG):
        return [], 0
    if os.path.getsize(LOG) < _ev["off"]:  # log truncado: reiniciar
        _ev.update(off=0, n=0, items=[])
    with open(LOG, "rb") as f:
        f.seek(_ev["off"])
        datos = f.read()
    fin = datos.rfind(b"\n") + 1  # solo lineas completas
    for l in datos[:fin].splitlines():
        _ev["n"] += 1
        try:
            e = json.loads(l.decode("utf-8"))
            p = e["path"]
        except (ValueError, KeyError):
            _ev["items"].append(None)
            continue
        i = p.lower().find("documents/boveda")
        rel = p[i + len("documents/boveda"):].strip("/") if i >= 0 else p
        e["id"] = rel[:-3] if rel.endswith(".md") else rel
        _ev["items"].append(e)
    _ev["off"] += fin
    return [e for e in _ev["items"][desde:] if e], _ev["n"]


def decisiones():
    ruta = os.path.join(BOVEDA, DECISIONES + ".md")
    try:
        txt = open(ruta, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    return [m.group(1).strip() for m in re.finditer(r"^[ \t]*[-*] \[ \][ \t]+(.+?)[ \t]*$", txt, re.M)]


class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=AQUI, **k)

    def log_message(self, *a):
        pass

    def _json(self, obj):
        b = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        u = urlparse(self.path)
        if self.headers.get("Host", "") not in HOSTS:  # corta el DNS rebinding
            return self.send_error(403)
        if u.path == "/graph":
            return self._json(grafo())
        if u.path == "/events":
            try:
                desde = max(0, int(parse_qs(u.query).get("since", ["0"])[0]))
            except ValueError:
                desde = 0
            ev, n = eventos(desde)
            return self._json({"events": ev, "next": n})
        if u.path == "/decisiones":
            return self._json(decisiones())
        if u.path == "/salud":
            try:
                return self._json(salud.calcular())
            except Exception as ex:
                return self._json({"error": str(ex), "total": 0, "huerfanas": [], "nunca": [], "top": []})
        if not ESTATICOS.match(u.path):
            return self.send_error(404)
        return super().do_GET()


if __name__ == "__main__":
    url = "http://127.0.0.1:%d" % PUERTO
    try:
        srv = ThreadingHTTPServer(("127.0.0.1", PUERTO), H)
    except OSError:  # puerto ocupado: casi siempre es el mapa que ya estaba abierto
        print("El puerto %d ya está en uso; abro el mapa que ya corre." % PUERTO)
        if "--abrir" in sys.argv:
            webbrowser.open(url)
        sys.exit(0)
    print("Mapa vivo en %s  (Ctrl+C para cerrar)" % url)
    if "--abrir" in sys.argv:  # el navegador se abre cuando el servidor ya escucha
        webbrowser.open(url)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
