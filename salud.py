"""Salud de la bóveda: huérfanas, nunca tocadas por Claude y más tocadas.
Uso: `python salud.py` escribe Boveda/_Sistema/Salud de la bóveda.md. server.py usa calcular()."""
import json, os, re, time
from config import BOVEDA, LOG, OMITIR, MARCA
from reglas import V, M
LINK = re.compile(r"\[\[([^\]|#^]+)")
NOTA = V["salud"]   # id de este informe (no cuenta ni sus enlaces)


def _notas():
    """{id: [destinos crudos]} de todas las notas; ignora los enlaces que salen del informe."""
    out = {}
    for raiz, dirs, archivos in os.walk(BOVEDA):
        dirs[:] = [d for d in dirs if d not in OMITIR and not d.startswith(".")]
        for a in archivos:
            if not a.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(raiz, a), BOVEDA).replace("\\", "/")[:-3]
            try:
                txt = open(os.path.join(raiz, a), encoding="utf-8", errors="replace").read()
            except OSError:
                continue
            out[rel] = [] if rel == NOTA else LINK.findall(txt)
    return out


def _toques(log=LOG):
    """{id: nº de eventos} contando cada evento de events.jsonl que apunta a una nota."""
    c = {}
    if not os.path.exists(log):
        return c
    for l in open(log, encoding="utf-8", errors="replace"):
        try:
            p = json.loads(l)["path"].replace("\\", "/")
        except (ValueError, KeyError, AttributeError):
            continue
        i = p.lower().find(MARCA)
        rel = p[i + len(MARCA):].strip("/") if i >= 0 else p
        rel = rel[:-3] if rel.endswith(".md") else rel
        if rel:
            c[rel] = c.get(rel, 0) + 1
    return c


def calcular(log=LOG, top=10):
    notas = _notas()
    nombre = {n.split("/")[-1].lower(): n for n in notas}
    con_enlace = set()
    for n, ls in notas.items():
        for l in ls:
            l = l.strip().removesuffix(".md")
            d = l if l in notas else nombre.get(l.split("/")[-1].lower())
            if d and d != n:
                con_enlace.update((n, d))
    toq = _toques(log)
    low = {n.lower(): n for n in notas}
    tocadas = {}
    for k, v in toq.items():
        n = k if k in notas else low.get(k.lower())
        if n:
            tocadas[n] = tocadas.get(n, 0) + v
    ids = sorted(n for n in notas if n != NOTA)
    return {"total": len(ids),
            "huerfanas": [n for n in ids if n not in con_enlace],
            "nunca": [n for n in ids if n not in tocadas],
            "top": [{"id": n, "n": v} for n, v in sorted(tocadas.items(), key=lambda x: -x[1])[:top] if n != NOTA]}


def _lista(ids, tope=150):
    if not ids:
        return ["- " + M["s_ninguna"]]
    r = [f"- [[{n}]]" for n in ids[:tope]]
    if len(ids) > tope:
        r.append("- " + M["s_mas"].format(n=len(ids) - tope))
    return r


def escribir():
    d = calcular()
    ruta = os.path.join(BOVEDA, *(NOTA + ".md").split("/"))
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    creado = time.strftime("%Y-%m-%d")
    if os.path.exists(ruta):
        m = re.search(r"^" + re.escape(V["creado"]) + r":[ \t]*(\S+)", open(ruta, encoding="utf-8", errors="replace").read(), re.M)
        creado = m.group(1) if m else creado
    L = ["---", f"{V['tipo']}: {V['sistema']}", f"{V['area']}: {V['sistema']}", f"{V['estado']}: {V['activo']}",
         f"{V['creado']}: {creado}", "---", "",
         "# " + M["s_titulo"], "",
         M["s_gen"].format(fecha=time.strftime("%Y-%m-%d %H:%M"), total=d["total"], h=len(d["huerfanas"]), n=len(d["nunca"])), "",
         M["s_biblio"], "",
         "## " + M["s_huerf"], ""] + _lista(d["huerfanas"]) + \
        ["", "## " + M["s_nunca"], ""] + _lista(d["nunca"]) + \
        ["", "## " + M["s_top"], ""] + ([f"- [[{x['id']}]] · {x['n']}" for x in d["top"]] or ["- " + M["s_sin_ev"]]) + [""]
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L))
    return ruta, d


if __name__ == "__main__":
    r, d = escribir()
    print(M["s_cli"].format(r=r, t=d["total"], h=len(d["huerfanas"]), n=len(d["nunca"])))
