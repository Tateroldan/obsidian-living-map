"""Sigue la guía para principiantes en una máquina recién creada (lo corre el CI, NO tu computadora).

Usa las rutas reales por defecto (~/Documents/Boveda y ~/.claude), así que se niega a correr fuera del CI.
Pasos: instalar con --si --claude-md --hooks, revisar lo instalado, correr el hook tal como quedó en
settings.json, arrancar el servidor y ver que el grafo y la araña (eventos) respondan.
"""
import http.client, json, os, shlex, socket, subprocess, sys, time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
for flujo in (sys.stdout, sys.stderr):  # consolas cp1252 de Windows
    try:
        flujo.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if os.environ.get("CI") != "true":
    sys.exit("solo en el CI: usa ~/Documents/Boveda y ~/.claude reales")

casa = Path.home()
boveda, claude = casa / "Documents" / "Boveda", casa / ".claude"
lang = sys.argv[1] if len(sys.argv) > 1 else "es"
inicio = "Inicio.md" if lang == "es" else "Home.md"
puerto = int(os.environ.get("MAPA_PUERTO") or 8765)


def paso(texto):
    print("\n== " + texto, flush=True)


def revisar(condicion, texto):
    if not condicion:
        sys.exit("FALLA: " + texto)
    print("   ok: " + texto)


paso("1. instalar como dice la guía")
p = subprocess.run([sys.executable, str(RAIZ / "kit" / "instalar.py"), "--lang", lang, "--si", "--claude-md", "--hooks"],
                   stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8")
print(p.stdout[-1500:], p.stderr[-1500:])
revisar(p.returncode == 0, "el instalador termina sin error")

paso("2. lo instalado")
revisar((boveda / inicio).exists(), "bóveda de ejemplo en %s" % boveda)
md = (claude / "CLAUDE.md").read_text(encoding="utf-8")
revisar("olm:inicio" in md and "{{" not in md, "bloque del kit en CLAUDE.md, sin marcas sin sustituir")
ajustes = json.loads((claude / "settings.json").read_text(encoding="utf-8"))
cmds = [h["command"] for g in ajustes["hooks"]["PostToolUse"] for h in g["hooks"]]
revisar(any("hook.py" in c for c in cmds), "hook del mapa en settings.json")

paso("3. el hook, tal como quedó en settings.json, anota una lectura")
log = Path(os.environ.get("MAPA_LOG") or RAIZ / "events.jsonl")
cmd = next(c for c in cmds if "hook.py" in c)
evento = json.dumps({"tool_name": "Read", "tool_input": {"file_path": str(boveda / inicio)}, "session_id": "ci"})
subprocess.run(shlex.split(cmd, posix=True), input=evento, text=True, encoding="utf-8", check=True)
revisar(log.exists() and inicio[:-3] in log.read_text(encoding="utf-8"), "events.jsonl tiene la lectura")

paso("4. el servidor responde")
srv = subprocess.Popen([sys.executable, str(RAIZ / "server.py")])
try:
    for _ in range(100):
        try:
            socket.create_connection(("127.0.0.1", puerto), timeout=0.2).close()
            break
        except OSError:
            time.sleep(0.1)
    for ruta in ("/graph", "/events?since=0", "/"):
        c = http.client.HTTPConnection("127.0.0.1", puerto, timeout=10)
        c.request("GET", ruta)
        r = c.getresponse()
        cuerpo = r.read()
        revisar(r.status == 200, "GET %s -> 200" % ruta)
        if ruta == "/graph":
            revisar(len(json.loads(cuerpo)["nodes"]) > 5, "el grafo trae las notas de ejemplo")
        if ruta.startswith("/events"):
            revisar(inicio[:-3].encode() in cuerpo, "la araña recibe el evento")
finally:
    srv.terminate()
    srv.wait(timeout=10)
print("\nmáquina limpia: todo ok", flush=True)
