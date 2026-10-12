#!/usr/bin/env python3
"""Hook Stop: compuerta barata para que el cierre deje una neurona solo cuando vale la pena.

Lee la transcripción de la sesión (sin modelo). Si se editó código fuera de la bóveda y NO se escribió
ninguna neurona, bloquea UNA sola vez con un mensaje corto que ya trae los archivos tocados, para que
Claude no tenga que reconstruirlos. Si no hubo ediciones de código, no hace nada (cierre gratis).

Nunca bloquea dos veces (respeta stop_hook_active y deja una marca por sesión).
"""
import json, os, sys, tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RAIZ))
from config import BOVEDA  # noqa: E402
from reglas import V, IDIOMA  # noqa: E402

HERRAMIENTAS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
TEXTO = {
    "es": ("Cierre: se editaron archivos ({n}): {lista}. Si hubo una técnica, una trampa o una decisión que aplicarías en otro "
           "proyecto, crea AHORA la neurona en {carpeta}/ (3 líneas, con {conecta} a otra neurona) y actualiza el estado del "
           "proyecto, todo en un solo mensaje. Si no hubo nada reutilizable, responde exactamente: NINGUNA."),
    "en": ("Wrap-up: files were edited ({n}): {lista}. If there was a technique, a gotcha or a decision you would apply in "
           "another project, create the learning NOW in {carpeta}/ (3 lines, with {conecta} to another learning) and update "
           "the project state, all in one message. If nothing was reusable, reply exactly: NONE."),
}


def archivos_editados(ruta):
    out = []
    try:
        for linea in open(ruta, encoding="utf-8", errors="replace"):
            try:
                e = json.loads(linea)
            except ValueError:
                continue
            c = (e.get("message") or {}).get("content")
            if not isinstance(c, list):
                continue
            for b in c:
                if isinstance(b, dict) and b.get("type") == "tool_use" and b.get("name") in HERRAMIENTAS:
                    p = (b.get("input") or {}).get("file_path") or (b.get("input") or {}).get("notebook_path")
                    if p:
                        out.append(str(p).replace("\\", "/"))
    except OSError:
        pass
    return out


def main():
    datos = json.loads(sys.stdin.buffer.read().decode("utf-8-sig", "replace") or "{}")
    if datos.get("stop_hook_active"):
        return
    sid = str(datos.get("session_id", "x"))[:16]
    marca = Path(tempfile.gettempdir()) / ("olm-cierre-" + sid)
    if marca.exists():
        return
    base = str(BOVEDA).replace("\\", "/").rstrip("/").lower() + "/"
    editados = archivos_editados(datos.get("transcript_path") or "")
    en_boveda = [p for p in editados if p.lower().startswith(base)]
    codigo = list(dict.fromkeys(p for p in editados if not p.lower().startswith(base)))
    ya_hay_neurona = any(("/" + V["aprendizajes"].lower() + "/") in p.lower() for p in en_boveda)
    if not codigo or ya_hay_neurona:
        return
    try:
        marca.write_text("1")
    except OSError:
        pass
    nombres = ", ".join(os.path.basename(p) for p in codigo[:6]) + ("…" if len(codigo) > 6 else "")
    motivo = TEXTO.get(IDIOMA, TEXTO["es"]).format(n=len(codigo), lista=nombres, carpeta=V["aprendizajes"], conecta=V["conecta"])
    sys.stdout.buffer.write(json.dumps({"decision": "block", "reason": motivo}, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
