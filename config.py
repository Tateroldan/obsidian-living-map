"""Configuración única del mapa vivo. Todo lo demás la importa; nada lleva rutas fijas.

Variables de entorno (opcionales):
  MAPA_BOVEDA  carpeta de la bóveda de Obsidian (por defecto ~/Documents/Boveda)
  MAPA_PUERTO  puerto del servidor local (por defecto 8765)
  MAPA_LOG     archivo de eventos (por defecto events.jsonl junto al código; útil para pruebas)
  MAPA_DECISIONES  nombre de la nota con casillas abiertas (por defecto «Decisiones pendientes»)
"""
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
BOVEDA = os.path.abspath(os.environ.get("MAPA_BOVEDA") or os.path.join(os.path.expanduser("~"), "Documents", "Boveda"))
PUERTO = int(os.environ.get("MAPA_PUERTO") or 8765)
LOG = os.path.abspath(os.environ.get("MAPA_LOG") or os.path.join(AQUI, "events.jsonl"))
OMITIR = {".obsidian", "Adjuntos", ".trash"}
DECISIONES = os.environ.get("MAPA_DECISIONES") or "Decisiones pendientes"  # nota con casillas - [ ]

NOMBRE = os.path.basename(BOVEDA)  # nombre de la bóveda para obsidian://
# fragmento «carpeta-padre/bóveda» en minúsculas con «/»: así el hook reconoce rutas dentro de comandos
MARCA = "/".join(BOVEDA.replace("\\", "/").lower().rstrip("/").split("/")[-2:])
