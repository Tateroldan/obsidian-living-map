"""Hook PostToolUse (Write|Edit): valida la nota de la bóveda que Claude acaba de escribir.
Sin tokens y sin bloquear: si todo está bien no dice nada; si no, exit 2 y el aviso llega a Claude.
Revisa: 4 propiedades con valores permitidos (reglas.json), al menos un enlace, tamaño, enlaces rotos,
mezclas de temas prohibidas (reglas.json) y llaves/secretos pegados. Idea tomada de obsidian-mind (validación al escribir)."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import BOVEDA


def _reglas():
    """reglas.json (tuyo, fuera del repo) o, si no existe, reglas.ejemplo.json."""
    aqui = os.path.dirname(os.path.abspath(__file__))
    for nombre in ("reglas.json", "reglas.ejemplo.json"):
        try:
            with open(os.path.join(aqui, nombre), encoding="utf-8") as f:
                return json.load(f)
        except OSError:
            continue
    return {}


R = _reglas()
OMITIR = set(R.get("omitir", [".obsidian", ".trash"]))
EXENTAS = set(R.get("exentas", []))
TIPOS = set(R.get("tipos", []))
AREAS = set(R.get("areas", []))
ESTADOS = set(R.get("estados", []))
MAX_LINEAS = R.get("max_lineas", 400)
NO_MEZCLAR = R.get("no_mezclar", [])
LINK = re.compile(r"(?<!!)\[\[([^\]|#^]+)")
SECRETOS = re.compile(
    r"sk-[A-Za-z0-9_-]{20,}|AIza[0-9A-Za-z_-]{35}|gh[pousr]_[A-Za-z0-9]{36,}|xox[abprs]-[A-Za-z0-9-]{10,}"
    r"|rpa_[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|(?i:api[_ -]?key|token|secret|password)[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9_\-/+]{20,}")


def propiedades(txt):
    m = re.match(r"\A---\r?\n(.*?)\r?\n---", txt, re.S)
    props = {}
    if m:
        for l in m.group(1).splitlines():
            if ":" in l:
                k, v = l.split(":", 1)
                props[k.strip()] = v.strip().strip("\"'")
    return props, (txt[m.end():] if m else txt)


def nombres_existentes():
    ok = set()
    for raiz, dirs, archivos in os.walk(BOVEDA):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for a in archivos:
            ok.add(a.lower())
            if a.endswith(".md"):
                ok.add(a[:-3].lower())
    return ok


def revisar(ruta):
    rel = os.path.relpath(ruta, BOVEDA).replace("\\", "/")
    if rel.startswith("..") or rel in EXENTAS or not rel.endswith(".md"):
        return []
    if set(rel.split("/")[:-1]) & OMITIR or rel.startswith(("00 Diario/", "00 Bandeja/")):
        return []
    txt = open(ruta, encoding="utf-8", errors="replace").read()
    props, cuerpo = propiedades(txt)
    p = []
    if not props:
        p.append("sin propiedades (faltan tipo/area/estado/creado)")
    else:
        for k, vals in (("tipo", TIPOS), ("area", AREAS), ("estado", ESTADOS)):
            v = props.get(k)
            if not v:
                p.append(f"falta `{k}`")
            elif v not in vals:
                p.append(f"`{k}: {v}` no es un valor permitido ({' · '.join(sorted(vals))})")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", props.get("creado", "")):
            p.append("`creado` debe ser AAAA-MM-DD")
    enlaces = [e.strip().removesuffix(".md") for e in LINK.findall(cuerpo) if e.strip(" .")]   # [[...]] = ejemplo, no enlace
    if not enlaces:
        p.append("no enlaza a ninguna nota (toda nota enlaza al menos a otra)")
    else:
        ok = nombres_existentes()
        rotos = sorted({e for e in enlaces if e.split("/")[-1].lower() not in ok})
        if rotos:
            p.append("enlaces rotos: " + ", ".join(f"[[{r}]]" for r in rotos[:6]))
    n = txt.count("\n") + 1
    if n > MAX_LINEAS:
        p.append(f"{n} líneas: divídela (tope {MAX_LINEAS})")
    if SECRETOS.search(txt):
        p.append("parece contener una llave/secreto: quítalo de la nota")
    for r in NO_MEZCLAR:
        en_zona = props.get("area") == r.get("area") or (r.get("carpeta") and rel.startswith(r["carpeta"]))
        if en_zona and re.search(r["prohibido"], cuerpo, re.I):
            p.append(r.get("aviso", "mezcla de temas no permitida"))
    return p


def main():
    data = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace"))
    ruta = (data.get("tool_input") or {}).get("file_path") or ""
    if not ruta or not os.path.exists(ruta):
        return 0
    ruta = os.path.abspath(ruta)
    if os.path.commonpath([ruta.lower(), BOVEDA.lower()]) != BOVEDA.lower():
        return 0
    p = revisar(ruta)
    if p:
        nombre = os.path.relpath(ruta, BOVEDA).replace("\\", "/")
        sys.stderr.write(f"validar.py · {nombre}:\n" + "\n".join("- " + x for x in p) + "\n")
        return 2
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)   # nunca estorbar a Claude por un fallo del validador
