#!/usr/bin/env python3
"""Hook UserPromptSubmit / SessionStart: inyecta contexto sin gastar turnos del modelo.

Corre kit/contexto.py con el mensaje del usuario (más el nombre de la carpeta de trabajo) y, si hay
coincidencia real, se lo entrega a Claude como contexto adicional: el estado del proyecto y las
neuronas relacionadas. Sin coincidencia no inyecta nada. Tope de tamaño y sin repetir lo ya inyectado.

Salida: JSON con hookSpecificOutput.additionalContext (exit 0 siempre; un fallo nunca estorba).
"""
import hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
TOPE = 1500  # caracteres inyectados como máximo
SIN_PROYECTO = "(ningún proyecto coincide"
SIN_NEURONAS = "(ninguna;"


def main():
    datos = json.loads(sys.stdin.buffer.read().decode("utf-8-sig", "replace") or "{}")
    evento = datos.get("hook_event_name") or "UserPromptSubmit"
    tema = (datos.get("prompt") or "") + " " + os.path.basename((datos.get("cwd") or "").rstrip("/\\"))
    if len(tema.strip()) < 4:
        return
    r = subprocess.run([sys.executable, str(KIT / "contexto.py"), tema[:600]], capture_output=True,
                       text=True, encoding="utf-8", timeout=20)
    txt = r.stdout.strip()
    if not txt or (SIN_PROYECTO in txt and SIN_NEURONAS in txt):
        return                                   # nada relevante: no se inyecta ruido
    if len(txt) > TOPE:
        txt = txt[:TOPE].rsplit("\n", 1)[0] + "\n…"
    # no repetir lo mismo en la misma sesión
    marca = Path(tempfile.gettempdir()) / ("olm-ctx-" + str(datos.get("session_id", "x"))[:16])
    h = hashlib.sha1(txt.encode("utf-8")).hexdigest()
    try:
        if marca.exists() and marca.read_text() == h:
            return
        marca.write_text(h)
    except OSError:
        pass
    salida = {"hookSpecificOutput": {"hookEventName": evento,
              "additionalContext": "Contexto de la bóveda (inyectado por un hook, no hace falta buscarlo):\n" + txt}}
    sys.stdout.buffer.write(json.dumps(salida, ensure_ascii=False).encode("utf-8"))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
