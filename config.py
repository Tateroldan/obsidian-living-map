"""Configuración única del mapa vivo. Todo lo demás la importa; nada lleva rutas fijas.

Variables de entorno (opcionales):
  MAPA_BOVEDA  carpeta de la bóveda (si falta: la de preferencias.json; si no, ~/Documents/Boveda)
  MAPA_PUERTO  puerto del servidor local (por defecto 8765)
  MAPA_LOG     archivo de eventos (por defecto events.jsonl junto al código; útil para pruebas)
  MAPA_DECISIONES  nombre de la nota con casillas abiertas (por defecto «Decisiones pendientes»)
"""
import json, os

from reglas import V

AQUI = os.path.dirname(os.path.abspath(__file__))
PREFS = os.path.join(AQUI, "preferencias.json")  # no se sube; lo escriben kit/instalar.py y autoarranque.py


def _boveda_guardada():
    try:
        with open(PREFS, encoding="utf-8") as f:
            return json.load(f).get("boveda")
    except (OSError, ValueError, AttributeError):
        return None


# orden: variable de entorno > la que guardó el instalador > ~/Documents/Boveda
BOVEDA = os.path.abspath(os.environ.get("MAPA_BOVEDA") or _boveda_guardada()
                         or os.path.join(os.path.expanduser("~"), "Documents", "Boveda"))
PUERTO = int(os.environ.get("MAPA_PUERTO") or 8765)
LOG = os.path.abspath(os.environ.get("MAPA_LOG") or os.path.join(AQUI, "events.jsonl"))
OMITIR = {".obsidian", "Adjuntos", ".trash"}
DECISIONES = os.environ.get("MAPA_DECISIONES") or V["decisiones"]  # nota con casillas - [ ]

NOMBRE = os.path.basename(BOVEDA)  # nombre de la bóveda para obsidian://
# fragmento «carpeta-padre/bóveda» en minúsculas con «/»: así el hook reconoce rutas dentro de comandos
MARCA = "/".join(BOVEDA.replace("\\", "/").lower().rstrip("/").split("/")[-2:])
